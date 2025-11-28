# AV Campaign Analyser

Audio-Visual Campaign Impact Analyzer with anomaly detection and regional uplift analysis.

## Features

✅ **Multi-file Upload** - Upload CSV and Excel files (merged automatically)
✅ **Anomaly Detection** - Identify conversion spikes from PR events (Dragons Den, influencer posts)
✅ **Anomaly Triage** - Review and exclude spikes from campaign analysis
✅ **Regional Analysis** - Compare campaign regions vs control regions
✅ **Interactive UI** - User-friendly forms for all inputs
✅ **Visualizations** - Timeline charts, regional comparisons, breakdowns
✅ **Light Theme** - Clean, professional interface
✅ **Export** - Download results as CSV or Excel

## Quick Start

### 1. Install Dependencies

```bash
cd c:/Users/harry/OneDrive/Desktop/EG/electric-glue-hub
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Run the App

```bash
streamlit run av_campaign_analyser/app.py
```

The app will open in your browser at http://localhost:8501

## Usage Guide

### Step 1: Upload Data

**Required columns:**
- `date` - Date in YYYY-MM-DD, DD/MM/YYYY, or MM/DD/YYYY format
- `bookings` - Number of conversions/bookings per day

**Optional columns:**
- `postcode` - Customer postcode (required for regional analysis)
- `revenue` - Revenue per day
- `search_impressions` - Google search impressions
- `search_clicks` - Google search clicks
- `brand_searches` - Brand-specific search volume

**Supported formats:** CSV (.csv), Excel (.xlsx, .xls)

**Multi-file upload:** Upload multiple files and they will be merged automatically

### Step 2: Detect Anomalies

1. Adjust **detection sensitivity** (lower = more sensitive)
2. Set **baseline window** (number of days for comparison)
3. Click **"Detect Anomalies"**

**What it does:** Uses z-score analysis to find conversion spikes that are significantly higher than the baseline.

### Step 3: Triage Anomalies

For each detected anomaly:
1. Review the date, conversions, z-score, and increase %
2. Check **"Exclude from analysis"** if this was a PR event (not campaign impact)
3. Optionally add a reason (e.g., "Dragons Den appearance")

**Why exclude?** PR events cause one-time spikes that aren't related to your AV campaign. Excluding them gives more accurate regional analysis.

### Step 4: Regional Analysis

**Configure the analysis:**

1. **Campaign Regions** - Enter postcode prefixes where your AV campaign aired
   - Example: `SW, W1, E, N` (London areas)
   - Comma-separated list
   - View available regions in the "Available Postcode Regions" expander

2. **Campaign Period** - Select start and end dates
   - Use date pickers to select the period when AV campaign was live

3. **Uplift Threshold** - Minimum % uplift to consider significant (default: 10%)

4. Click **"Run Regional Analysis"**

**Results:**
- Campaign region avg vs control region avg (bookings per day)
- Uplift percentage
- Significance flag
- Interpretation (positive/moderate/negative impact)
- Bar chart comparison

### Step 5: Visualizations

**Timeline Chart:**
- Shows bookings over time
- Red X markers = detected anomalies
- Green shaded area = campaign period (if regional analysis run)

**Regional Breakdown:**
- Top regions by total bookings
- Adjustable number of regions to display

### Step 6: Export

Download your analysis results:
- **CSV** - Plain text, works everywhere
- **Excel** - Formatted spreadsheet

Export includes:
- Original data
- `is_anomaly` flag (if anomalies detected)
- `excluded_from_analysis` flag (if dates excluded)

## Data Requirements

### Minimum Requirements
- At least 7 days of data (for baseline calculation)
- `date` and `bookings` columns

### For Regional Analysis
- `postcode` column with UK postcodes (e.g., "SW1 1AA", "E1 6AN")
- At least 2 distinct postcode regions

### Data Quality Tips
- No missing dates in the campaign period
- Consistent date format across files
- Non-negative booking values
- Valid UK postcode format (if using regional analysis)

## Example Data Format

**CSV Example:**

```csv
date,bookings,postcode,revenue
2024-06-01,23,SW1 1AA,1150.00
2024-06-02,25,E1 6AN,1250.00
2024-06-03,22,W1A 1AA,1100.00
```

**Excel Example:**

| date       | bookings | postcode | revenue |
|------------|----------|----------|---------|
| 2024-06-01 | 23       | SW1 1AA  | 1150.00 |
| 2024-06-02 | 25       | E1 6AN   | 1250.00 |
| 2024-06-03 | 22       | W1A 1AA  | 1100.00 |

## Configuration

Edit [config.py](config.py) to change default settings:

```python
# Anomaly detection sensitivity (std deviations)
ANOMALY_THRESHOLD_STD_DEV = 2.5

# Regional uplift threshold (%)
REGIONAL_UPLIFT_THRESHOLD = 10
```

## Troubleshooting

**Problem: "ANTHROPIC_API_KEY not set in environment"**
**Solution:** Create `.env` file in project root with your API key

**Problem: "Regional analysis not available"**
**Solution:** Ensure your data has a `postcode` column

**Problem: "No anomalies detected"**
**Solution:**
- Lower the detection sensitivity slider (try 2.0 or 1.5)
- Ensure you have at least 7 days of data
- Check if your data has any real spikes

**Problem: "File upload error"**
**Solution:**
- Ensure file has `date` and `bookings` columns
- Check date format (YYYY-MM-DD works best)
- Verify no completely empty rows

**Problem: "Invalid postcode prefix"**
**Solution:**
- Use 1-2 letter prefixes only (SW, E, N, W1, EC)
- Comma-separated (e.g., "SW, E, N")
- No spaces in individual prefixes

## Architecture

```
av_campaign_analyser/
├── app.py                  # Main Streamlit UI
├── config.py              # Configuration and API keys
├── anomaly_detection.py   # Z-score based spike detection
├── regional_analysis.py   # Regional uplift calculator
├── utils.py               # File upload, validation, charts
└── README.md              # This file
```

## How It Works

### Anomaly Detection
1. Calculate rolling mean and std dev (backward-looking window)
2. Compute z-score for each date: `(actual - baseline_mean) / baseline_std`
3. Flag dates where z-score > threshold (default: 2.5)
4. User triages flagged dates (exclude PR events)

### Regional Analysis
1. Extract postcode prefix (SW1 1AA → SW)
2. Segment data: campaign regions vs control regions
3. Calculate avg bookings/day for each segment (during campaign period)
4. Compute uplift: `((campaign_avg - control_avg) / control_avg) * 100`
5. Flag as significant if uplift > threshold (default: 10%)

## Use Cases

**1. Dragons Den Effect**
- Upload booking data
- Detect spike on air date
- Exclude Dragons Den date
- Run regional analysis to see actual AV campaign impact

**2. TV Campaign ROI**
- Upload data with campaign period clearly defined
- Exclude any PR spikes
- Compare London (campaign region) vs rest of UK (control)
- Measure regional uplift %

**3. Multi-channel Attribution**
- Upload data with search metrics
- Detect organic spikes (influencer posts)
- Isolate paid AV campaign impact
- Export for further analysis

## Technical Details

**Dependencies:**
- Streamlit 1.32.0+ (UI framework)
- Pandas 2.0.0+ (data manipulation)
- Plotly 5.18.0+ (interactive charts)
- NumPy 1.24.0+ (numerical operations)
- OpenPyXL 3.1.0+ (Excel support)

**Performance:**
- Handles datasets up to 10,000 rows efficiently
- Anomaly detection: <1 second for typical datasets
- Regional analysis: <1 second for typical datasets

**Browser Compatibility:**
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Support

**Documentation:**
- [TRUSTCHECK_IMPLEMENTATION.md](../TRUSTCHECK_IMPLEMENTATION.md)
- [FINAL_DELIVERY_SUMMARY.md](../FINAL_DELIVERY_SUMMARY.md)

**Common Questions:**
- See sidebar "Help" section in the app
- Check "Common Issues" expander

## Version History

**v1.0** (November 2024)
- Initial release
- Multi-file upload (CSV, XLSX)
- Anomaly detection with triage
- Regional analysis with user input forms
- Timeline and regional visualizations
- Light theme UI
- Export functionality

## License

Part of Electric Glue AI Tools
© 2024 Electric Glue

---

**Built with:** Streamlit + Claude Code Assistant
**Last Updated:** November 28, 2024
