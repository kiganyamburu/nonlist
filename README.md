# Cost of Equity Estimation for Non-Listed Firms

## Project Overview
This project estimates the cost of equity (Re) for non-listed firms using market data from publicly traded companies in the same industries.

## Current Status
✅ Project instructions understood  
✅ Non-listed firms data available (`nonlist.csv`)  
✅ Python program ready (`cost_of_equity_estimation.py`)  
⏳ **WAITING FOR DATA**: CRSP and Compustat files needed

## Required Data Files

You need to obtain two data files from your professor/TA:

### 1. CRSP Data: `crsp_monthly_returns.csv`
- **Period**: January 2015 - December 2020 (72 months)
- **Variables**: CUSIP, date, RET, EWRETD
- **Filters**: Non-missing CUSIP and RET

### 2. Compustat Data: `compustat_2020.csv`
- **Period**: Fiscal Year 2020
- **Variables**: FYEAR, FYR, CUSIP, SIC, DT, PRCC_F, CSHO
- **Filters**: FYR=12, non-missing values, positive prices and shares

## How to Get the Data

### Option 1: Email Your Professor/TA (Recommended)
Use the template in `email_template.txt` to request the data files.

### Option 2: Download from WRDS Yourself
If you have WRDS access, see `DATA_ACQUISITION_GUIDE.md` for detailed instructions.

## Project Files

```
nonlist/
├── cost_of_equity_estimation.py    # Main analysis program (READY TO RUN)
├── nonlist.csv                      # Non-listed firms data (PROVIDED)
├── email_template.txt               # Email template for requesting data
├── DATA_ACQUISITION_GUIDE.md        # Detailed guide for obtaining data
├── download_wrds_data.py            # Script to download from WRDS (if you have access)
├── README.md                        # This file
│
├── crsp_monthly_returns.csv         # ⏳ NEED TO OBTAIN
└── compustat_2020.csv               # ⏳ NEED TO OBTAIN
```

## Once You Have the Data

### Step 1: Place the files in this directory
```
c:\Users\nduta\OneDrive\Desktop\Projects\nonlist\
```

### Step 2: Ensure you have required Python libraries
```bash
pip install pandas statsmodels
```

### Step 3: Run the program
```bash
python cost_of_equity_estimation.py
```

### Step 4: Review the output
The program will:
- Load and validate all data
- Estimate betas for public firms
- Calculate industry average un-levered betas
- Compute cost of equity for all 26 non-listed firms (A-Z)
- Save results to `cost_of_equity_results.csv`

## Expected Output

The program will display:
1. Data loading confirmations
2. Descriptive statistics
3. Beta estimation results
4. Industry analysis
5. **Final table with cost of equity for each firm**

Example output:
```
Firm  Industry  D/E Ratio  Industry Beta  Firm Beta  Cost of Equity (%)
A     357       0.080      0.8234         0.8692     11.45
B     357       0.120      0.8234         0.8924     11.64
...
```

## Methodology

1. **Estimate Betas**: Run OLS regression for each public firm
   - Model: `RET = intercept + β × Market_Return + error`

2. **Un-lever Betas**: Remove financial leverage effect
   - Formula: `β₀ = β / (1 + (1-T) × D/E)`

3. **Industry Averages**: Calculate mean un-levered beta by industry
   - Only industries with ≥5 firms

4. **Re-lever Betas**: Apply non-listed firms' leverage
   - Formula: `β_levered = β₀ × (1 + (1-T) × D/E)`

5. **CAPM**: Calculate cost of equity
   - Formula: `Re = Rf + β_levered × MRP`
   - Rf = 4.5%, MRP = 8%

## Parameters Used

- **Tax Rate**: 30%
- **Beta of Debt**: 0 (risk-free debt assumption)
- **Risk-Free Rate**: 4.5%
- **Market Risk Premium**: 8%
- **Minimum Observations**: 30 monthly returns per firm
- **Minimum Industry Size**: 5 firms

## Troubleshooting

**Error: File not found**
- Ensure data files are in the correct directory
- Check filenames match exactly: `crsp_monthly_returns.csv` and `compustat_2020.csv`

**Error: Module not found**
- Install required libraries: `pip install pandas statsmodels`

**Warning: Firms without industry beta**
- Some non-listed firms may be in industries with <5 public firms
- These will show as missing in the output

## Submission

For Blackboard submission:
- Submit: `cost_of_equity_estimation.py`
- The code includes detailed comments explaining every step
- Ready for grading once you have the data files

## Questions?

If you encounter any issues:
1. Check that all data files are in the correct location
2. Verify Python libraries are installed
3. Review error messages carefully
4. Contact your TA or professor for data-related issues

---

**Next Step**: Send the email to your professor/TA to request the data files!
