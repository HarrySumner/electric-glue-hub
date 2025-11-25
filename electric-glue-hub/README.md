# ⚡ Electric Glue Marketing Intelligence Platform

**Version:** 3.0.0
**Critical Innovation:** QA Housekeeping Agent with Synthetic Testing

A comprehensive marketing intelligence suite with **integrated QA validation** and **synthetic testing** to prevent AI hallucinations and ensure all outputs are grounded in verified facts.

---

## 🚨 Critical Mission Statement

**If the QA Housekeeping Agent fails to catch a fabrication, the entire project is considered a failure.**

This is the baseline quality standard for all future work. The QA system is tested continuously with synthetic test cases and displays real-time health status via a traffic light system.

---

## 🚀 Features

### 1. Scout - Marketing Intelligence Assistant
AI-powered research tool that gathers comprehensive business intelligence with multi-perspective analysis.

**Three Strategic Perspectives:**
- 😈 **Devil's Advocate**: Risk analysis, what could go wrong, hidden costs
- 🌟 **Optimist**: Growth opportunities, untapped potential, quick wins
- ⚖️ **Realist**: Practical constraints, trade-offs, MVP approach

**Quality Assurance:**
- ✅ **QA Housekeeping Agent**: Every output validated for fabrications before display
- ✅ **Fact-Constrained Mode**: All claims must be grounded in verified sources with citations
- ✅ **Deep Web Research**: Gathers 100+ sources automatically
- ✅ **Quality Enforcement**: Minimum 10 sources, 30 facts per analysis
- 🚦 **Synthetic Testing**: Continuous validation of QA agent with traffic light status

### 2. Causal Impact Analyzer
Bayesian structural time series (BSTS) analysis for measuring true campaign impact.

**Key Features:**
- Campaign-specific analysis with 90-day measurement windows
- Deterministic results (fixed random seeds for reproducibility)
- Confidence intervals and statistical significance testing
- Counterfactual forecasting
- Client-ready visualizations

### 3. QA Housekeeping Agent (Critical Innovation)

**The baseline operator deployed across all future projects.**

#### Validation Checks

**CRITICAL Severity (Blocks Output):**
1. **Fabrication Detection** - Any statistic/metric without source citation
2. **Data Integrity** - Claims must match underlying data
3. **Statistical Validity** - Statistical claims must be mathematically correct

**HIGH Severity (3+ blocks output):**
4. **Citation Validation** - All factual claims must have [Fact #X] references
5. **Fact Reference Validation** - Cited fact numbers must exist
6. **Contradiction Detection** - Conflicting claims across sections

**MEDIUM/LOW Severity (Warnings only):**
7. **Completeness** - All required sections present
8. **Interpretation Accuracy** - Conclusions match data

#### Decision Logic

```
BLOCK   → Any CRITICAL issues → Output NOT shown to user
WARN    → HIGH/MEDIUM issues → Output shown with warnings
APPROVE → No issues → Clean output
```

#### Synthetic Testing System

The QA agent is continuously tested with synthetic test cases to ensure it catches all categories of errors:

**Test Categories:**
- ✅ **Fabrication Detection**: Catches made-up statistics
- ✅ **Missing Citations**: Catches factual claims without sources
- ✅ **Invalid References**: Catches citations to non-existent facts
- ✅ **Data Mismatches**: Catches statistical claim contradictions
- ✅ **Clean Outputs**: Properly approves valid outputs

**Traffic Light Status:**
- 🟢 **GREEN**: All tests passing (≥95% accuracy)
- 🟡 **YELLOW**: Some tests failing (80-94% accuracy)
- 🔴 **RED**: Critical failures (<80% accuracy)

---

## 📁 Project Structure

```
electric-glue-hub/
├── app.py                             # Hub homepage
├── pages/
│   ├── 2_Causal_Impact_Analyzer.py    # Product 1: Simplified causal impact
│   ├── 3_Connected_Budget_Optimizer.py # Product 2: Budget optimizer
│   ├── 4_Marketing_Intelligence.py    # Product 3: Scout with QA
│   └── 6_Settings.py                  # Settings
├── tv-campaign-impact-analyzer/       # Full TV campaign analyzer (subfolder)
│   ├── agents/                        # 5 specialized agents
│   ├── streamlit_app/                 # Standalone TV app
│   ├── core/                          # Core analysis engine
│   ├── run_app.py                     # Standalone launcher
│   └── README.md                      # TV analyzer docs
├── agents/
│   ├── perspective_agents.py          # Three perspective agents (Devil, Optimist, Realist)
│   ├── scout_research_agent.py        # Scout orchestrator with QA integration
│   └── qa_housekeeping_agent.py       # QA validation agent
├── config/
│   ├── branding.py                    # Electric Glue branding
│   ├── fact_constrained_prompts.py    # Fact-constrained prompts for perspectives
│   ├── qa_prompts.py                  # QA validation prompts
│   ├── scout_prompts.py               # Scout research prompts
│   └── branding.py                    # UI theme/styling
├── models/
│   └── qa_models.py                   # QA validation data structures
├── tests/
│   └── test_qa_synthetic.py           # Synthetic test suite for QA agent
├── utils/                             # Utility functions
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
└── run_hub.py                         # Quick launcher script
```

---

## 🔧 Installation

### Prerequisites
- Python 3.9+
- Anthropic API key (for Claude)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/electric-glue-hub.git
cd electric-glue-hub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py --server.port=8505
```

The platform will be available at `http://localhost:8505`

**Note:** Electric Glue Hub runs on port 8505 to avoid conflicts with other client projects.

---

## 🎯 Usage

### Scout Research with QA Validation

1. Navigate to **Scout** from the homepage
2. Enter a company name or topic
3. Select research depth (Quick, Balanced, Deep Dive)
4. All three perspectives are analyzed automatically
5. **QA Validation runs automatically:**
   - 🟢 Blocked outputs show critical errors
   - 🟡 Approved outputs show with warnings
   - ✅ Clean outputs show with validation badge

### QA Health Monitoring

1. Navigate to **QA Health Monitor** from sidebar
2. View real-time synthetic test results
3. Traffic light status shows QA agent health:
   - 🟢 **GREEN**: System operational (≥95% tests passing)
   - 🟡 **YELLOW**: Degraded performance (80-94% passing)
   - 🔴 **RED**: Critical failure (<80% passing)
4. Run tests on-demand to verify QA agent accuracy

### Causal Impact Analysis (Simplified)

1. Navigate to **Causal Impact Analyzer** from the homepage
2. Upload time series CSV with date and KPI columns
3. Define campaign start/end dates
4. System calculates 90-day measurement window
5. Get statistical analysis with visualizations

### TV Campaign Impact Analyzer (Full Multi-Agent System)

The full TV Campaign Impact Analyzer is available as a subfolder with 5 specialized agents:

1. **Standalone Mode:**
   ```bash
   cd tv-campaign-impact-analyzer
   python run_app.py
   ```
   Access at: `http://localhost:8501`

2. **Features:**
   - 5 specialized agents (Data Validation, Analysis, Interpretation, QA, Reporting)
   - Client-ready reports with executive summaries
   - Advanced BSTS modeling for TV, Radio, OOH campaigns
   - Deterministic results with fixed random seeds

3. **Documentation:**
   See [tv-campaign-impact-analyzer/README.md](tv-campaign-impact-analyzer/README.md) for full details

---

## 🛡️ QA Validation System Architecture

### Integration Flow

```
User Query
    ↓
Scout Research (gather sources, extract facts)
    ↓
Multi-Perspective Analysis (Devil's Advocate, Optimist, Realist)
    ↓
QA Housekeeping Agent Validation ← [CRITICAL GATE]
    ↓
    ├─ BLOCK → Show errors, do not show output
    ├─ WARN  → Show output with warnings
    └─ APPROVE → Show clean output
    ↓
Display to User
```

### Code Integration Example

```python
# In scout_research_agent.py
qa_result = self.qa_agent.validate_scout_output(
    output_content=final_output,
    company_name=query,
    verified_facts=verified_facts_text,
    sources_used=sources
)

if qa_result.should_block():
    # CRITICAL issues found - DO NOT show output to user
    return {
        'qa_blocked': True,
        'qa_issues': qa_result.get_critical_issues(),
        'message': 'Output contains fabricated statistics'
    }
```

### Validation Examples

**❌ BLOCKED Example:**
```
Output: "Revenue grew 45% YoY"
Verified Facts: [No revenue data present]
Decision: BLOCK
Reason: FABRICATION - statistic without source citation
```

**✅ APPROVED Example:**
```
Output: "Company raised $10M Series A [Fact #5]"
Verified Facts: "5. Company raised $10M Series A (Source: TechCrunch, 2024-03-15)"
Decision: APPROVE
Reason: Claim matches verified fact with proper citation
```

---

## 🧪 Synthetic Testing System

### Purpose
Continuously validate that the QA Housekeeping Agent correctly identifies fabrications, missing citations, and other errors.

### Test Categories

1. **Fabrication Detection (CRITICAL)**
   - Test: Output contains "Revenue is $50M" without source
   - Expected: BLOCK with FABRICATION issue

2. **Missing Citations (HIGH)**
   - Test: Factual claim "Based in London" without [Fact #X]
   - Expected: WARN or BLOCK with MISSING_CITATION issue

3. **Invalid References (HIGH)**
   - Test: Output cites [Fact #99] but only 10 facts exist
   - Expected: BLOCK with INVALID_REFERENCE issue

4. **Data Integrity (CRITICAL)**
   - Test: Claims "Sample size: 100" when actual data has 50 rows
   - Expected: BLOCK with DATA_INTEGRITY issue

5. **Clean Output (Control)**
   - Test: All claims properly cited with valid fact numbers
   - Expected: APPROVE with no issues

### Running Tests

```bash
# Command line
python -m pytest tests/test_qa_synthetic.py -v

# Or use the UI
Navigate to QA Health Monitor page → Click "Run Synthetic Tests"
```

### Traffic Light Interpretation

- 🟢 **GREEN (≥95%)**: QA system is catching all test fabrications correctly
- 🟡 **YELLOW (80-94%)**: Some test cases failing - investigate immediately
- 🔴 **RED (<80%)**: Critical failure - QA system not reliable, halt deployments

---

## 📊 Perspective Agents Details

### 😈 Devil's Advocate
- **Focus**: Risks, vulnerabilities, failure modes
- **Output Format**: Risk register, stress tests, downside scenarios
- **Example Insight**: "70% dependency on single channel creates systemic risk if Instagram algorithm changes"
- **Key Questions**: What could go wrong? Where are we vulnerable? What's the downside?

### 🌟 Optimist
- **Focus**: Growth opportunities, quick wins, untapped potential
- **Output Format**: Scaling opportunities, expansion ideas, upside scenarios
- **Example Insight**: "Lookalike audiences show 85% similarity to best converters - £200K+ expansion opportunity"
- **Key Questions**: Where's the opportunity? What's the upside? How can we grow faster?

### ⚖️ Realist
- **Focus**: Practical constraints, trade-offs, MVP approach
- **Output Format**: Incremental improvements, realistic milestones, pragmatic actions
- **Example Insight**: "Fix attribution first (15-20% data loss), then scale top channel, then test creative"
- **Key Questions**: What's actually doable? What are the trade-offs? What's the MVP?

---

## 🔬 Technical Implementation

### Fact-Constrained Prompts
All perspective agents use prompts that:
- Accept only verified facts as input
- Require [Fact #X] citations for all claims
- Acknowledge data gaps explicitly
- Never fabricate statistics or metrics

### QA Configuration

```python
qa_config = QAConfig(
    enabled=True,                    # Always on in production
    block_on_critical=True,          # Block if any CRITICAL issues
    block_on_high_count=3,           # Block if 3+ HIGH issues
    check_fabrication=True,          # Detect fabricated statistics
    check_citations=True,            # Validate all citations
    check_fact_references=True,      # Verify fact numbers exist
    check_contradictions=True,       # Detect conflicting claims
    log_all_validations=True,        # Log every validation
    log_directory="logs/qa_validation"
)
```

### Validation Logging
All QA validations are logged to `logs/qa_validation/` with:
- Timestamp
- Decision (APPROVE/BLOCK/WARN)
- Issues found with severity
- Output content length
- Company/topic analyzed

---

## 📈 Future Enhancements

- [ ] Integrate QA validation into Causal Impact (requires agent refactor)
- [ ] Add code generation validation for Causal Impact outputs
- [ ] Build QA analytics dashboard (failure pattern analysis)
- [ ] Implement auto-retry with LLM-based fixes for blocked outputs
- [ ] Add adversarial testing (red team attacks on QA system)
- [ ] Multi-language support for QA validation
- [ ] Custom QA rules per client/industry

---

## 🤝 Contributing

**Quality Standards:**
1. All outputs MUST pass QA validation
2. No fabricated statistics allowed - ever
3. All claims must cite sources with [Fact #X] format
4. Test QA system with adversarial examples
5. Synthetic tests must maintain ≥95% pass rate

**Pull Request Checklist:**
- [ ] All new features include QA validation
- [ ] Synthetic tests added for new validation rules
- [ ] Traffic light dashboard updated if QA logic changes
- [ ] Documentation updated with examples

---

## 📄 License

MIT License

---

## 👥 Contact

**Harry Sumner**
GitHub: [@HarrySumner](https://github.com/HarrySumner)

---

## 🚨 Critical Reminder

**The QA Housekeeping Agent is the foundation of trust in this system.**

If it fails to catch fabrications, users receive false information, and the entire platform's credibility is destroyed. The synthetic testing system exists to ensure this never happens.

**Monitor the traffic light. Keep it green. 🟢**
