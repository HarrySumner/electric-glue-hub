"""
Utility functions for AV Campaign Analyser
Handles file upload, data validation, and chart generation
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Tuple, Optional, List, Dict
from datetime import datetime
import streamlit as st


class DataValidator:
    """Validates uploaded data for AV Campaign Analyser"""

    REQUIRED_FIELDS = ['date', 'bookings']
    OPTIONAL_FIELDS = ['revenue', 'postcode', 'search_impressions', 'search_clicks', 'brand_searches']
    DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, List[str], pd.DataFrame]:
        """
        Validate uploaded DataFrame.

        Args:
            df: Raw DataFrame from upload

        Returns:
            (is_valid, error_messages, cleaned_df)
        """
        errors = []

        # Check if DataFrame is empty
        if df.empty:
            return False, ["File is empty"], df

        # Check for required fields
        missing_fields = [field for field in DataValidator.REQUIRED_FIELDS
                         if field not in df.columns]

        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")
            return False, errors, df

        # Clean DataFrame
        df = df.copy()

        # Parse date column
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            # Check for invalid dates
            invalid_dates = df['date'].isna().sum()
            if invalid_dates > 0:
                errors.append(f"Warning: {invalid_dates} rows have invalid dates and will be removed")
                df = df.dropna(subset=['date'])
        except Exception as e:
            errors.append(f"Error parsing dates: {str(e)}")
            return False, errors, df

        # Validate bookings column
        try:
            df['bookings'] = pd.to_numeric(df['bookings'], errors='coerce')

            # Check for invalid bookings
            invalid_bookings = df['bookings'].isna().sum()
            if invalid_bookings > 0:
                errors.append(f"Warning: {invalid_bookings} rows have invalid booking values and will be set to 0")
                df['bookings'] = df['bookings'].fillna(0)

            # Check for negative bookings
            negative_bookings = (df['bookings'] < 0).sum()
            if negative_bookings > 0:
                errors.append(f"Warning: {negative_bookings} rows have negative bookings and will be set to 0")
                df.loc[df['bookings'] < 0, 'bookings'] = 0

        except Exception as e:
            errors.append(f"Error validating bookings: {str(e)}")
            return False, errors, df

        # Validate optional numeric fields
        numeric_fields = ['revenue', 'search_impressions', 'search_clicks', 'brand_searches']
        for field in numeric_fields:
            if field in df.columns:
                try:
                    df[field] = pd.to_numeric(df[field], errors='coerce').fillna(0)
                except Exception:
                    errors.append(f"Warning: Could not parse {field} as numeric, skipping")

        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)

        # Check date range
        date_range = (df['date'].max() - df['date'].min()).days
        if date_range < 7:
            errors.append("Warning: Dataset covers less than 7 days, anomaly detection may not be accurate")

        is_valid = len([e for e in errors if not e.startswith("Warning:")]) == 0

        return is_valid, errors, df

    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict:
        """Get summary statistics for uploaded data"""
        return {
            'total_rows': len(df),
            'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
            'total_days': (df['date'].max() - df['date'].min()).days + 1,
            'total_bookings': int(df['bookings'].sum()),
            'avg_bookings_per_day': float(df['bookings'].mean()),
            'has_postcode': 'postcode' in df.columns,
            'has_search_data': 'search_impressions' in df.columns or 'search_clicks' in df.columns,
            'unique_postcodes': df['postcode'].nunique() if 'postcode' in df.columns else 0
        }


class FileUploader:
    """Handles multi-file upload for CSV and XLSX formats"""

    @staticmethod
    def load_file(uploaded_file) -> Tuple[bool, Optional[pd.DataFrame], List[str]]:
        """
        Load uploaded file (CSV or XLSX).

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            (success, dataframe, error_messages)
        """
        errors = []

        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()

            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            else:
                return False, None, [f"Unsupported file format: {file_extension}. Please upload CSV or XLSX files."]

            # Validate the DataFrame
            is_valid, validation_errors, cleaned_df = DataValidator.validate_dataframe(df)

            if not is_valid:
                return False, None, validation_errors

            return True, cleaned_df, validation_errors  # validation_errors may contain warnings

        except Exception as e:
            return False, None, [f"Error reading file: {str(e)}"]

    @staticmethod
    def merge_dataframes(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Merge multiple DataFrames from different files.

        Args:
            dataframes: List of validated DataFrames

        Returns:
            Merged DataFrame
        """
        if len(dataframes) == 1:
            return dataframes[0]

        # Concatenate all DataFrames
        merged = pd.concat(dataframes, ignore_index=True)

        # Group by date and sum bookings (in case of duplicate dates)
        grouped = merged.groupby('date', as_index=False).agg({
            'bookings': 'sum',
            **{col: 'sum' for col in merged.columns if col in ['revenue', 'search_impressions', 'search_clicks', 'brand_searches']},
            **{col: 'first' for col in merged.columns if col in ['postcode']}
        })

        return grouped.sort_values('date').reset_index(drop=True)


class ChartGenerator:
    """Generates Plotly charts for AV Campaign Analyser"""

    @staticmethod
    def create_timeline_chart(
        df: pd.DataFrame,
        anomaly_dates: Optional[List[str]] = None,
        campaign_start: Optional[str] = None,
        campaign_end: Optional[str] = None
    ) -> go.Figure:
        """
        Create timeline chart showing conversions over time.

        Args:
            df: DataFrame with 'date' and 'bookings' columns
            anomaly_dates: List of dates to highlight as anomalies
            campaign_start: Campaign start date (YYYY-MM-DD)
            campaign_end: Campaign end date (YYYY-MM-DD)

        Returns:
            Plotly figure
        """
        fig = go.Figure()

        # Main timeline
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['bookings'],
            mode='lines+markers',
            name='Bookings',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))

        # Highlight anomalies
        if anomaly_dates:
            anomaly_df = df[df['date'].astype(str).isin(anomaly_dates)]
            fig.add_trace(go.Scatter(
                x=anomaly_df['date'],
                y=anomaly_df['bookings'],
                mode='markers',
                name='Anomalies',
                marker=dict(size=12, color='red', symbol='x')
            ))

        # Highlight campaign period
        if campaign_start and campaign_end:
            fig.add_vrect(
                x0=campaign_start, x1=campaign_end,
                fillcolor="green", opacity=0.1,
                layer="below", line_width=0,
                annotation_text="Campaign Period",
                annotation_position="top left"
            )

        fig.update_layout(
            title='Conversion Timeline',
            xaxis_title='Date',
            yaxis_title='Bookings',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )

        return fig

    @staticmethod
    def create_regional_comparison_chart(
        campaign_avg: float,
        control_avg: float,
        uplift_pct: float
    ) -> go.Figure:
        """
        Create bar chart comparing campaign vs control regions.

        Args:
            campaign_avg: Average bookings in campaign regions
            control_avg: Average bookings in control regions
            uplift_pct: Percentage uplift

        Returns:
            Plotly figure
        """
        fig = go.Figure()

        colors = ['green' if uplift_pct > 0 else 'red', 'gray']

        fig.add_trace(go.Bar(
            x=['Campaign Regions', 'Control Regions'],
            y=[campaign_avg, control_avg],
            marker_color=colors,
            text=[f'{campaign_avg:.1f}', f'{control_avg:.1f}'],
            textposition='auto'
        ))

        fig.update_layout(
            title=f'Regional Performance Comparison (Uplift: {uplift_pct:+.1f}%)',
            yaxis_title='Avg Bookings per Day',
            template='plotly_white',
            height=400,
            showlegend=False
        )

        return fig

    @staticmethod
    def create_anomaly_heatmap(df: pd.DataFrame, z_scores: pd.Series) -> go.Figure:
        """
        Create heatmap showing anomaly scores over time.

        Args:
            df: DataFrame with 'date' column
            z_scores: Series of z-scores

        Returns:
            Plotly figure
        """
        # Create DataFrame for heatmap
        df_plot = df.copy()
        df_plot['z_score'] = z_scores
        df_plot['week'] = df_plot['date'].dt.isocalendar().week
        df_plot['day_of_week'] = df_plot['date'].dt.day_name()

        # Pivot for heatmap
        pivot = df_plot.pivot_table(
            values='z_score',
            index='day_of_week',
            columns='week',
            aggfunc='mean'
        )

        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=[f'Week {w}' for w in pivot.columns],
            y=pivot.index,
            colorscale='RdYlGn_r',
            zmid=0
        ))

        fig.update_layout(
            title='Anomaly Score Heatmap (Red = High Spike)',
            template='plotly_white',
            height=400
        )

        return fig

    @staticmethod
    def create_postcode_breakdown_chart(breakdown_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Create bar chart of top regions by bookings.

        Args:
            breakdown_df: DataFrame from RegionalAnalyzer.get_region_breakdown()
            top_n: Number of top regions to show

        Returns:
            Plotly figure
        """
        top_regions = breakdown_df.head(top_n)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=top_regions['postcode_prefix'],
            y=top_regions['total_conversions'],
            marker_color='steelblue',
            text=top_regions['total_conversions'],
            textposition='auto'
        ))

        fig.update_layout(
            title=f'Top {top_n} Regions by Total Bookings',
            xaxis_title='Postcode Prefix',
            yaxis_title='Total Bookings',
            template='plotly_white',
            height=400
        )

        return fig


# Export utilities
def export_to_csv(df: pd.DataFrame, filename: str = "av_analysis_export.csv") -> bytes:
    """Export DataFrame to CSV bytes for download"""
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(df: pd.DataFrame, filename: str = "av_analysis_export.xlsx") -> bytes:
    """Export DataFrame to Excel bytes for download"""
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Analysis')
    return output.getvalue()
