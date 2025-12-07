# Data Acquisition Guide for CRSP and Compustat

## Overview
You need two datasets from **WRDS (Wharton Research Data Services)**:
1. **CRSP** - Stock market data (monthly returns)
2. **Compustat** - Company financial data

## Prerequisites

### 1. WRDS Access
- **Check if your university has WRDS subscription** (most business schools do)
- Go to: https://wrds-www.wharton.upenn.edu/
- If you don't have an account, register using your university email
- Your institution must be a WRDS subscriber

### 2. Request Access (if needed)
- Contact your university library or finance department
- Ask for WRDS access for academic research
- Mention you need CRSP and Compustat databases

---

## Method 1: Download via WRDS Web Interface (Recommended for Beginners)

### A. Getting CRSP Data

1. **Log in to WRDS**: https://wrds-www.wharton.upenn.edu/

2. **Navigate to CRSP**:
   - Click on "CRSP" in the left menu
   - Select "Stock / Security Files"
   - Choose "Monthly Stock File"

3. **Set Date Range**:
   - Start Date: `2015-01`
   - End Date: `2020-12`

4. **Select Variables**:
   - `CUSIP` (Company identifier)
   - `RET` (Holding period return)
   - `EWRETD` (Equal-weighted return including distributions)

5. **Set Conditions/Filters**:
   - CUSIP: Not missing
   - RET: Not missing

6. **Query Options**:
   - Output Format: **CSV**
   - Compression: None (or ZIP if file is large)

7. **Submit Query** and download the file
   - Save as: `crsp_monthly_returns.csv`

### B. Getting Compustat Data

1. **Navigate to Compustat**:
   - Click on "Compustat" in the left menu
   - Select "Compustat - Capital IQ"
   - Choose "Fundamentals Annual"

2. **Set Date Range**:
   - Fiscal Year: `2020`

3. **Select Variables**:
   - `FYEAR` (Fiscal year)
   - `FYR` (Fiscal year end)
   - `CUSIP` (Company identifier)
   - `SIC` (Standard Industry Classification code)
   - `DT` (Total debt including current)
   - `PRCC_F` (Price close - annual - fiscal)
   - `CSHO` (Common shares outstanding)

4. **Set Conditions/Filters**:
   - FYEAR = 2020
   - FYR = 12
   - CUSIP: Not missing
   - SIC: Not missing
   - DT >= 0
   - PRCC_F > 0
   - CSHO > 0

5. **Query Options**:
   - Output Format: **CSV**
   - Compression: None

6. **Submit Query** and download the file
   - Save as: `compustat_2020.csv`

---

## Method 2: Using WRDS Python API (Advanced)

If you have WRDS access, you can download data programmatically:

### Setup
```bash
pip install wrds
```

### Python Script
```python
import wrds

# Connect to WRDS (will prompt for username/password)
db = wrds.Connection()

# Get CRSP data
crsp_query = """
SELECT cusip, date, ret, ewretd
FROM crsp.msf
WHERE date BETWEEN '2015-01-01' AND '2020-12-31'
  AND cusip IS NOT NULL
  AND ret IS NOT NULL
"""
crsp_data = db.raw_sql(crsp_query)
crsp_data.to_csv('crsp_monthly_returns.csv', index=False)

# Get Compustat data
compustat_query = """
SELECT fyear, fyr, cusip, sic, dt, prcc_f, csho
FROM comp.funda
WHERE fyear = 2020
  AND fyr = 12
  AND cusip IS NOT NULL
  AND sic IS NOT NULL
  AND dt >= 0
  AND prcc_f > 0
  AND csho > 0
"""
compustat_data = db.raw_sql(compustat_query)
compustat_data.to_csv('compustat_2020.csv', index=False)

db.close()
```

---

## Method 3: Alternative Sources (If No WRDS Access)

### For Students Without WRDS:

1. **Ask Your Professor**:
   - They may have already prepared the datasets
   - Common for course projects

2. **Use Sample Data**:
   - Some professors provide sample datasets for assignments
   - Check your course materials or Blackboard

3. **Request from Teaching Assistant**:
   - TAs often have access to course datasets

4. **Library Data Services**:
   - University libraries sometimes provide data extraction services
   - Schedule an appointment with a data librarian

---

## After Downloading

1. **Save files to project directory**:
   ```
   c:\Users\nduta\OneDrive\Desktop\Projects\nonlist\crsp_monthly_returns.csv
   c:\Users\nduta\OneDrive\Desktop\Projects\nonlist\compustat_2020.csv
   ```

2. **Verify the files**:
   - Check that files are not empty
   - Open in Excel/text editor to verify columns
   - Ensure data looks reasonable

3. **Let me know when ready**:
   - Once you have the files, I'll write the complete Python program

---

## Expected File Structure

### crsp_monthly_returns.csv
```
CUSIP,date,RET,EWRETD
00724F10,2015-01-31,0.0234,0.0156
00724F10,2015-02-28,0.0123,0.0178
...
```

### compustat_2020.csv
```
FYEAR,FYR,CUSIP,SIC,DT,PRCC_F,CSHO
2020,12,00724F101,3571,1234.5,45.67,100.2
...
```

---

## Troubleshooting

**Problem**: Can't access WRDS
- **Solution**: Contact your university library or IT help desk

**Problem**: Missing variables in query
- **Solution**: Check variable names in WRDS documentation

**Problem**: Query times out
- **Solution**: Try smaller date ranges or fewer variables

**Problem**: Files too large
- **Solution**: Use compression (ZIP) or download in chunks

---

## Next Steps

Once you have the data files:
1. Place them in the project directory
2. Let me know the exact filenames
3. I'll create the complete Python program to analyze the data
