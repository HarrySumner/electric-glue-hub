"""
Orchestrator Agent - Coordinates the multi-agent workflow
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

from agents.data_agent import DataAgent
from agents.validation_agent import ValidationAgent
from agents.analysis_agent import AnalysisAgent
from agents.interpretation_agent import InterpretationAgent


class WorkflowState(Enum):
    """Workflow state machine."""
    INITIALIZED = "initialized"
    DATA_INGESTED = "data_ingested"
    DATA_VALIDATED = "data_validated"
    ANALYSIS_COMPLETE = "analysis_complete"
    INTERPRETATION_COMPLETE = "interpretation_complete"
    FAILED = "failed"
    COMPLETED = "completed"


class OrchestratorAgent:
    """
    Orchestrator agent that coordinates the multi-agent workflow.

    Workflow:
    1. DATA AGENT: Ingest and prepare data
    2. VALIDATION AGENT: Check quality and detect confounders
    3. ANALYSIS AGENT: Fit BSTS model and compute causal effects
    4. INTERPRETATION AGENT: Generate plain-English insights

    Handles:
    - State management
    - Error recovery
    - Progress tracking
    - Results aggregation
    """

    def __init__(self, llm_provider: str = 'openai'):
        """
        Initialize orchestrator with all agents.

        Parameters
        ----------
        llm_provider : str, default 'openai'
            LLM provider for interpretation agent
        """
        self.data_agent = DataAgent()
        self.validation_agent = ValidationAgent()
        self.analysis_agent = AnalysisAgent()
        self.interpretation_agent = InterpretationAgent(provider=llm_provider)

        self.state = WorkflowState.INITIALIZED
        self.results = {
            'data': None,
            'validation': None,
            'analysis': None,
            'interpretation': None
        }
        self.errors = []

        print("🤖 Orchestrator Agent initialized")
        print("   📊 Data Agent ready")
        print("   ✅ Validation Agent ready")
        print("   🔬 Analysis Agent ready")
        print("   💬 Interpretation Agent ready")

    def run_full_analysis(
        self,
        file_path: Optional[str] = None,
        data: Optional[pd.DataFrame] = None,
        target_col: str = None,
        date_col: str = None,
        covariate_cols: Optional[List[str]] = None,
        pre_period: Tuple[str, str] = None,
        post_period: Tuple[str, str] = None,
        intervention_date: Optional[str] = None,
        business_context: Optional[Dict] = None,
        auto_suggest: bool = True
    ) -> Dict:
        """
        Run complete end-to-end causal impact analysis.

        Parameters
        ----------
        file_path : str, optional
            Path to CSV or Excel file (if not providing data directly)
        data : pd.DataFrame, optional
            Pre-loaded data (if not providing file_path)
        target_col : str
            Target metric column name
        date_col : str, optional
            Date column name (auto-detected if not provided)
        covariate_cols : list of str, optional
            Covariate columns (auto-suggested if not provided)
        pre_period : tuple of str
            (start_date, end_date) for pre-intervention
        post_period : tuple of str
            (start_date, end_date) for post-intervention
        intervention_date : str, optional
            Date of intervention (for validation checks)
        business_context : dict, optional
            Business context for interpretation
        auto_suggest : bool, default True
            Auto-suggest columns and covariates

        Returns
        -------
        dict with complete results from all agents
        """
        print("\n" + "=" * 80)
        print("🚀 STARTING TV CAMPAIGN IMPACT ANALYSIS")
        print("=" * 80 + "\n")

        try:
            # STEP 1: Data Ingestion
            print("📊 STEP 1: DATA INGESTION")
            print("-" * 80)

            if file_path:
                ingest_result = self.data_agent.ingest(file_path)
                if not ingest_result['success']:
                    self._handle_error("Data ingestion failed", ingest_result.get('error'))
                    return self._format_results()

                print(f"✅ Data loaded: {ingest_result['shape'][0]} rows × {ingest_result['shape'][1]} columns")

                # Auto-suggestions
                if auto_suggest:
                    suggestions = ingest_result['suggestions']
                    if not date_col:
                        date_col = suggestions['date_column']
                    if not target_col:
                        target_col = suggestions['target_metric']
                    if not covariate_cols:
                        covariate_cols = suggestions['covariates']

                    print(f"\n🔍 Auto-detected:")
                    print(f"   Date column: {date_col}")
                    print(f"   Target metric: {target_col}")
                    print(f"   Covariates: {', '.join(covariate_cols) if covariate_cols else 'None'}")

            elif data is not None:
                self.data_agent.raw_data = data
                print(f"✅ Data provided: {data.shape[0]} rows × {data.shape[1]} columns")
            else:
                self._handle_error("No data provided", "Must provide either file_path or data")
                return self._format_results()

            # Prepare data
            prepared_data = self.data_agent.prepare_for_analysis(
                date_col=date_col,
                target_col=target_col,
                covariate_cols=covariate_cols,
                handle_missing='interpolate'
            )

            self.results['data'] = {
                'prepared_data': prepared_data,
                'metadata': self.data_agent.metadata,
                'summary_stats': self.data_agent.get_summary_stats()
            }
            self.state = WorkflowState.DATA_INGESTED

            print(f"✅ Data prepared: {len(prepared_data)} time periods")
            print(f"   Date range: {prepared_data.index.min()} to {prepared_data.index.max()}")

            # STEP 2: Validation
            print("\n✅ STEP 2: DATA VALIDATION")
            print("-" * 80)

            if not intervention_date and post_period:
                intervention_date = post_period[0]

            validation_result = self.validation_agent.validate(
                data=prepared_data,
                target_col=target_col,
                covariate_cols=covariate_cols,
                intervention_date=intervention_date
            )

            self.results['validation'] = validation_result
            self.state = WorkflowState.DATA_VALIDATED

            print(f"✅ Validation complete: Score {validation_result['score']}/100")

            if validation_result['warnings']:
                print(f"\n⚠️  {len(validation_result['warnings'])} warnings:")
                for warning in validation_result['warnings'][:5]:
                    print(f"   {warning}")

            if validation_result['score'] < 40:
                print("\n🚨 LOW DATA QUALITY - Proceeding with caution")
                self.errors.append("Low data quality score")

            # STEP 3: Analysis
            print("\n🔬 STEP 3: BAYESIAN CAUSAL ANALYSIS")
            print("-" * 80)

            analysis_result = self.analysis_agent.analyze(
                data=prepared_data,
                target_col=target_col,
                pre_period=pre_period,
                post_period=post_period,
                covariate_cols=covariate_cols,
                niter=2000,
                nburn=1000
            )

            if not analysis_result['success']:
                self._handle_error("Analysis failed", analysis_result.get('error'))
                return self._format_results()

            self.results['analysis'] = analysis_result
            self.state = WorkflowState.ANALYSIS_COMPLETE

            print("\n" + self.analysis_agent.get_summary())

            # STEP 4: Interpretation
            print("\n💬 STEP 4: INTERPRETATION & INSIGHTS")
            print("-" * 80)

            interpretation_result = self.interpretation_agent.interpret(
                analysis_results=analysis_result,
                validation_results=validation_result,
                business_context=business_context
            )

            if not interpretation_result['success']:
                self._handle_error("Interpretation failed", interpretation_result.get('error'))
                return self._format_results()

            self.results['interpretation'] = interpretation_result
            self.state = WorkflowState.INTERPRETATION_COMPLETE

            print("\n📝 Executive Summary:")
            print(interpretation_result['executive_summary'])

            print("\n💡 Key Findings:")
            for finding in interpretation_result['key_findings'][:3]:
                print(f"   • {finding}")

            # Mark as completed
            self.state = WorkflowState.COMPLETED

            print("\n" + "=" * 80)
            print("✅ ANALYSIS COMPLETE!")
            print("=" * 80)

            return self._format_results()

        except Exception as e:
            self._handle_error("Unexpected error in workflow", str(e))
            return self._format_results()

    def _handle_error(self, stage: str, error: str):
        """Handle errors and update state."""
        self.state = WorkflowState.FAILED
        error_msg = f"[{stage}] {error}"
        self.errors.append(error_msg)
        print(f"\n❌ ERROR: {error_msg}")

    def _format_results(self) -> Dict:
        """Format results for return."""
        return {
            'success': self.state == WorkflowState.COMPLETED,
            'state': self.state.value,
            'errors': self.errors,
            **self.results
        }

    def get_report(self, format: str = 'markdown', include_technical: bool = True) -> str:
        """
        Generate comprehensive report.

        Parameters
        ----------
        format : str, default 'markdown'
            Output format: 'markdown', 'html', or 'text'
        include_technical : bool, default True
            Include technical methodology details

        Returns
        -------
        str : Formatted report
        """
        if self.state != WorkflowState.COMPLETED:
            return f"Analysis not complete. Current state: {self.state.value}"

        interpretation = self.results['interpretation']

        if format == 'markdown':
            return self.interpretation_agent.generate_client_report(
                interpretation,
                include_technical=include_technical
            )

        elif format == 'text':
            return self._format_text_report(interpretation)

        elif format == 'html':
            return self._format_html_report(interpretation)

        else:
            return "Unsupported format"

    def _format_text_report(self, interpretation: Dict) -> str:
        """Generate plain text report."""
        report = f"""
{'=' * 80}
TV CAMPAIGN IMPACT ANALYSIS REPORT
{'=' * 80}

EXECUTIVE SUMMARY
{'-' * 80}
{interpretation['executive_summary']}

KEY FINDINGS
{'-' * 80}
"""
        for i, finding in enumerate(interpretation['key_findings'], 1):
            report += f"{i}. {finding}\n"

        report += f"""
RECOMMENDATIONS
{'-' * 80}
"""
        for i, rec in enumerate(interpretation['recommendations'], 1):
            report += f"{i}. {rec}\n"

        report += f"""
FULL ANALYSIS
{'-' * 80}
{interpretation['narrative']}

IMPORTANT CAVEATS
{'-' * 80}
"""
        for i, caveat in enumerate(interpretation['caveats'], 1):
            report += f"{i}. {caveat}\n"

        report += f"\n{'=' * 80}\nGenerated by Electric Glue TV Campaign Impact Analyzer\n{'=' * 80}\n"

        return report

    def _format_html_report(self, interpretation: Dict) -> str:
        """Generate HTML report with Electric Glue branding."""
        from config.branding import BRAND_COLORS

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TV Campaign Impact Analysis</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, {BRAND_COLORS['background_light']} 0%, #ffffff 100%);
        }}
        .header {{
            background: linear-gradient(135deg, {BRAND_COLORS['primary']} 0%, {BRAND_COLORS['secondary']} 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: {BRAND_COLORS['secondary']};
            border-bottom: 3px solid {BRAND_COLORS['primary']};
            padding-bottom: 10px;
        }}
        ul {{
            line-height: 1.8;
        }}
        .footer {{
            text-align: center;
            color: {BRAND_COLORS['text_secondary']};
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📺 TV Campaign Impact Analysis Report</h1>
        <p>Powered by Electric Glue Agentic AI</p>
    </div>

    <div class="section">
        <h2>Executive Summary</h2>
        <p>{interpretation['executive_summary']}</p>
    </div>

    <div class="section">
        <h2>Key Findings</h2>
        <ul>
"""
        for finding in interpretation['key_findings']:
            html += f"            <li>{finding}</li>\n"

        html += f"""
        </ul>
    </div>

    <div class="section">
        <h2>Recommendations</h2>
        <ul>
"""
        for rec in interpretation['recommendations']:
            html += f"            <li>{rec}</li>\n"

        html += f"""
        </ul>
    </div>

    <div class="section">
        <h2>Full Analysis</h2>
        <p>{interpretation['narrative']}</p>
    </div>

    <div class="section">
        <h2>Important Caveats</h2>
        <ul>
"""
        for caveat in interpretation['caveats']:
            html += f"            <li>{caveat}</li>\n"

        html += """
        </ul>
    </div>

    <div class="footer">
        <p><strong>Electric Glue</strong> - Where AI Meets Marketing Science</p>
        <p>Generated by TV Campaign Impact Analyzer v1.0</p>
    </div>
</body>
</html>
"""
        return html

    def export_results(
        self,
        output_dir: str,
        formats: List[str] = ['csv', 'markdown', 'html']
    ):
        """
        Export all results to files.

        Parameters
        ----------
        output_dir : str
            Directory to save results
        formats : list of str
            Output formats: 'csv', 'excel', 'markdown', 'html', 'json'
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n📤 Exporting results to {output_dir}/")

        # Export detailed results
        if 'csv' in formats or 'excel' in formats:
            detailed = self.analysis_agent.get_detailed_results()
            if 'csv' in formats:
                csv_path = os.path.join(output_dir, 'detailed_results.csv')
                detailed.to_csv(csv_path, index=False)
                print(f"   ✅ CSV exported: {csv_path}")

            if 'excel' in formats:
                excel_path = os.path.join(output_dir, 'detailed_results.xlsx')
                self.analysis_agent.export_results(excel_path, format='excel')
                print(f"   ✅ Excel exported: {excel_path}")

        # Export reports
        if 'markdown' in formats:
            md_path = os.path.join(output_dir, 'report.md')
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(self.get_report(format='markdown'))
            print(f"   ✅ Markdown report: {md_path}")

        if 'html' in formats:
            html_path = os.path.join(output_dir, 'report.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(self.get_report(format='html'))
            print(f"   ✅ HTML report: {html_path}")

        # Export JSON (all results)
        if 'json' in formats:
            import json
            json_path = os.path.join(output_dir, 'full_results.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self._format_results(), f, indent=2, default=str)
            print(f"   ✅ JSON results: {json_path}")

        print("✅ Export complete!")


# Example usage
if __name__ == '__main__':
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(llm_provider='openai')

    # Run full analysis on sample data
    results = orchestrator.run_full_analysis(
        file_path='sample_data/nielsen_tv_sample.csv',  # Will be created by data_agent
        auto_suggest=True,  # Auto-detect columns
        pre_period=('2024-01-01', '2024-07-18'),
        post_period=('2024-07-19', '2024-12-31'),
        intervention_date='2024-07-19',
        business_context={
            'campaign_name': 'Nielsen Summer TV Campaign',
            'campaign_budget': 450000,
            'target_metric_name': 'bookings',
            'industry': 'Travel & Leisure'
        }
    )

    if results['success']:
        print("\n" + "=" * 80)
        print("RESULTS SUMMARY")
        print("=" * 80)

        # Export results
        orchestrator.export_results(
            output_dir='output',
            formats=['csv', 'markdown', 'html', 'json']
        )

        print("\n📊 View your results in the 'output' directory!")
    else:
        print(f"\n❌ Analysis failed. Errors: {results['errors']}")
