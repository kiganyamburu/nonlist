# Quick Start Guide

## You Are Here: ✅ Code Ready | ⏳ Waiting for Data

### What You Need to Do Next

**Step 1: Send Email to Professor/TA**
```
Open: email_template.txt
Fill in: Professor/TA name and your details
Send the email
```

**Step 2: Wait for Data Files**
You need two files:
- `crsp_monthly_returns.csv`
- `compustat_2020.csv`

**Step 3: Place Files in Project Directory**
```
c:\Users\nduta\OneDrive\Desktop\Projects\nonlist\
```

**Step 4: Install Libraries (if not already installed)**
```bash
pip install pandas statsmodels
```

**Step 5: Run the Program**
```bash
python cost_of_equity_estimation.py
```

**Step 6: Submit to Blackboard**
```
Submit: cost_of_equity_estimation.py
```

---

## File Overview

| File | Status | Purpose |
|------|--------|---------|
| `cost_of_equity_estimation.py` | ✅ Ready | Main program to submit |
| `nonlist.csv` | ✅ Have it | Non-listed firms data |
| `crsp_monthly_returns.csv` | ⏳ Need it | Stock market data |
| `compustat_2020.csv` | ⏳ Need it | Company financials |
| `email_template.txt` | ✅ Ready | Email to send |
| `README.md` | ✅ Ready | Full documentation |

---

## What the Program Does

1. Loads CRSP and Compustat data
2. Estimates betas for public firms (OLS regression)
3. Un-levers betas to remove leverage effect
4. Calculates industry average betas
5. Re-levers betas for non-listed firms
6. Computes cost of equity using CAPM
7. Outputs results table and CSV file

---

## Expected Runtime

- With typical dataset sizes: 1-3 minutes
- Most time spent on beta estimation (OLS regressions)

---

## Need Help?

- **Data issues**: Contact professor/TA
- **Code issues**: Check README.md troubleshooting section
- **WRDS access**: See DATA_ACQUISITION_GUIDE.md
