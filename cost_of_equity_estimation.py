"""
Cost of Equity Estimation for Non-Listed Firms
Project 2 - Fall 2025

This program estimates the cost of equity for non-listed firms using:
1. Market data from publicly traded firms (CRSP)
2. Financial data from Compustat
3. Industry classification and leverage ratios

Author: [Your Name]
Date: December 2025
"""

# ============================================================================
# IMPORT LIBRARIES
# ============================================================================

import pandas as pd
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("COST OF EQUITY ESTIMATION FOR NON-LISTED FIRMS")
print("=" * 80)

# ============================================================================
# STEP 1: READ DATA FILES
# ============================================================================

print("\n[STEP 1] Loading data files...")

# Load CRSP data (monthly stock returns)
try:
    crsp = pd.read_csv('crsp_data.csv')
    print(f"✓ Loaded CRSP data: {len(crsp):,} observations")
except FileNotFoundError:
    print("✗ Error: 'crsp_data.csv' not found")
    print("  Please ensure the CRSP data file is in the current directory")
    exit(1)

# Load Compustat data (firm financials)
try:
    compustat = pd.read_csv('compustat_data.csv')
    print(f"✓ Loaded Compustat data: {len(compustat):,} firms")
except FileNotFoundError:
    print("✗ Error: 'compustat_data.csv' not found")
    print("  Please ensure the Compustat data file is in the current directory")
    exit(1)

# Load non-listed firms data
try:
    nl = pd.read_csv('nonlist.csv')
    print(f"✓ Loaded non-listed firms data: {len(nl)} firms")
except FileNotFoundError:
    print("✗ Error: 'nonlist.csv' not found")
    exit(1)

# ============================================================================
# STEP 2: DISPLAY FIRST AND LAST ROWS
# ============================================================================

print("\n[STEP 2] Inspecting data...")

print("\nCRSP Data - First 5 rows:")
print(crsp.head())
print("\nCRSP Data - Last 5 rows:")
print(crsp.tail())

print("\nCompustat Data - First 5 rows:")
print(compustat.head())
print("\nCompustat Data - Last 5 rows:")
print(compustat.tail())

print("\nNon-Listed Firms Data:")
print(nl)

# ============================================================================
# STEP 3: CHECK VARIABLE TYPES
# ============================================================================

print("\n[STEP 3] Checking variable types...")

print("\nCRSP Data Types:")
print(crsp.dtypes)

print("\nCompustat Data Types:")
print(compustat.dtypes)

print("\nNon-Listed Firms Data Types:")
print(nl.dtypes)

# ============================================================================
# STEP 4: DESCRIPTIVE STATISTICS
# ============================================================================

print("\n[STEP 4] Descriptive statistics...")

print("\nCRSP Data Summary:")
print(crsp.describe())

print("\nCompustat Data Summary:")
print(compustat.describe())

print("\nNon-Listed Firms Summary:")
print(nl.describe())

# ============================================================================
# STEP 5: FILTER FIRMS WITH AT LEAST 30 MONTHLY RETURNS
# ============================================================================

print("\n[STEP 5] Filtering firms with at least 30 monthly returns...")

# Count observations per CUSIP
obs_count = crsp.groupby('CUSIP').size()
print(f"Total unique firms before filtering: {len(obs_count):,}")

# Keep only firms with at least 30 observations
valid_cusips = obs_count[obs_count >= 30].index
crsp_filtered = crsp[crsp['CUSIP'].isin(valid_cusips)].copy()

print(f"Firms with >= 30 observations: {len(valid_cusips):,}")
print(f"Total observations after filtering: {len(crsp_filtered):,}")

# ============================================================================
# STEP 6: ESTIMATE MARKET MODEL AND EXTRACT BETAS
# ============================================================================

print("\n[STEP 6] Estimating market model and extracting betas...")
print("Running OLS regression: RET = intercept + beta × ewretd + error")

# Method 1: Define a function to run OLS regression
def estimate_beta(group):
    """
    Estimate beta using OLS regression with intercept.
    
    Model: RET_it = intercept + beta_i × Market_return_t + error_it
    
    Parameters:
    -----------
    group : DataFrame
        Group of observations for a single firm (CUSIP)
    
    Returns:
    --------
    Series : Regression parameters (intercept and beta)
    """
    # Prepare dependent variable (y) and independent variable (x)
    y = group['RET']
    x = group['ewretd']
    
    # Add constant (intercept) to the model
    x = sm.add_constant(x)
    
    # Run OLS regression
    model = sm.OLS(y, x).fit()
    
    # Return regression parameters
    return model.params

# Apply the function to each firm (grouped by CUSIP)
params = crsp_filtered.groupby('CUSIP').apply(estimate_beta).reset_index()

print(f"✓ Estimated betas for {len(params):,} firms")

# ============================================================================
# STEP 7: RENAME BETA COLUMN
# ============================================================================

print("\n[STEP 7] Processing beta estimates...")

print("\nParameters dataframe (first 10 rows):")
print(params.head(10))

# Rename the market index coefficient to 'beta'
# The coefficient name is 'ewretd' (same as the independent variable)
params.rename(columns={'ewretd': 'beta'}, inplace=True)

print("\nAfter renaming (first 10 rows):")
print(params.head(10))

# ============================================================================
# STEP 8: PROCESS COMPUSTAT DATA
# ============================================================================

print("\n[STEP 8] Processing Compustat data...")

# Extract first 8 digits of CUSIP for matching with CRSP
compustat['CUSIP'] = compustat['cusip'].astype(str).str[:8]
print("✓ Extracted 8-digit CUSIP")

# Create 3-digit SIC code
compustat['sic3'] = compustat['sic'].astype(str).str[:3].astype(int)
print("✓ Created 3-digit SIC code (sic3)")

# Calculate D/E ratio: Total Debt / Market Value of Equity
# Market Value of Equity = Price per Share × Shares Outstanding
compustat['DE'] = compustat['dt'] / (compustat['prcc_f'] * compustat['csho'])
print("✓ Calculated D/E ratio")

# Keep only necessary columns
compustat_clean = compustat[['CUSIP', 'sic3', 'DE']].copy()
print(f"✓ Cleaned Compustat data: {len(compustat_clean)} firms")

print("\nCompustat data (first 10 rows):")
print(compustat_clean.head(10))

# ============================================================================
# STEP 9: MERGE BETAS WITH COMPUSTAT DATA
# ============================================================================

print("\n[STEP 9] Merging beta estimates with Compustat data...")

# Merge on CUSIP
merged = pd.merge(params, compustat_clean, on='CUSIP', how='inner')

print(f"✓ Merged data: {len(merged)} firms")
print(f"  (Lost {len(params) - len(merged)} firms due to no Compustat match)")

print("\nMerged dataframe (first 10 rows):")
print(merged.head(10))

# ============================================================================
# STEP 10: UN-LEVER BETAS
# ============================================================================

print("\n[STEP 10] Un-levering betas...")

# Parameters
TAX_RATE = 0.30  # 30% tax rate
BETA_DEBT = 0    # Assume debt is risk-free

# Un-levering formula: beta0 = beta_levered / (1 + (1 - tax_rate) × D/E)
# This removes the effect of financial leverage, leaving only business risk
merged['beta0'] = merged['beta'] / (1 + (1 - TAX_RATE) * merged['DE'])

print(f"✓ Calculated un-levered betas (beta0)")
print(f"  Tax rate: {TAX_RATE:.0%}")
print(f"  Beta of debt: {BETA_DEBT}")

print("\nData with un-levered betas (first 10 rows):")
print(merged[['CUSIP', 'beta', 'DE', 'beta0']].head(10))

# ============================================================================
# STEP 11: COUNT FIRMS PER INDUSTRY
# ============================================================================

print("\n[STEP 11] Counting firms per industry...")

# Count firms in each industry (sic3)
industry_counts = merged.groupby('sic3').size().sort_values(ascending=False)

print(f"\nTotal industries: {len(industry_counts)}")
print(f"\nTop 10 industries by firm count:")
print(industry_counts.head(10))

print(f"\nIndustries with < 5 firms: {(industry_counts < 5).sum()}")
print(f"Industries with >= 5 firms: {(industry_counts >= 5).sum()}")

# ============================================================================
# STEP 12: FILTER INDUSTRIES WITH AT LEAST 5 FIRMS
# ============================================================================

print("\n[STEP 12] Filtering industries with at least 5 firms...")

# Keep only industries with at least 5 observations
valid_industries = industry_counts[industry_counts >= 5].index
merged_filtered = merged[merged['sic3'].isin(valid_industries)].copy()

print(f"✓ Kept {len(valid_industries)} industries")
print(f"✓ Retained {len(merged_filtered)} firms")
print(f"  (Dropped {len(merged) - len(merged_filtered)} firms in small industries)")

# ============================================================================
# STEP 13: CALCULATE INDUSTRY AVERAGE UN-LEVERED BETAS
# ============================================================================

print("\n[STEP 13] Calculating industry average un-levered betas...")

# Calculate mean un-levered beta for each industry
ibetas = merged_filtered.groupby('sic3')['beta0'].mean().reset_index()
ibetas.columns = ['sic3', 'industry_beta0']

print(f"✓ Calculated industry betas for {len(ibetas)} industries")

print("\nIndustry betas (ibetas dataframe):")
print(ibetas)

# ============================================================================
# STEP 14: LOAD AND INSPECT NON-LISTED FIRMS DATA
# ============================================================================

print("\n[STEP 14] Inspecting non-listed firms data...")

print("\nNon-listed firms:")
print(nl)

print("\nData types:")
print(nl.dtypes)

# ============================================================================
# STEP 15: MERGE INDUSTRY BETAS WITH NON-LISTED FIRMS
# ============================================================================

print("\n[STEP 15] Merging industry betas with non-listed firms...")

# Merge on sic3 (industry code)
nl_with_betas = pd.merge(nl, ibetas, on='sic3', how='left')

print(f"✓ Merged data for {len(nl_with_betas)} non-listed firms")

# Check for firms without industry beta (no matching industry)
missing_betas = nl_with_betas['industry_beta0'].isna().sum()
if missing_betas > 0:
    print(f"\n⚠ Warning: {missing_betas} firms have no matching industry beta")
    print("These firms are in industries with < 5 public firms:")
    print(nl_with_betas[nl_with_betas['industry_beta0'].isna()])

print("\nNon-listed firms with industry betas:")
print(nl_with_betas)

# ============================================================================
# STEP 16: CALCULATE COST OF EQUITY
# ============================================================================

print("\n[STEP 16] Calculating cost of equity...")

# Parameters
RISK_FREE_RATE = 0.045  # 4.5%
MARKET_RISK_PREMIUM = 0.08  # 8%

print(f"\nAssumptions:")
print(f"  Risk-free rate (Rf): {RISK_FREE_RATE:.1%}")
print(f"  Market risk premium (MRP): {MARKET_RISK_PREMIUM:.1%}")
print(f"  Tax rate: {TAX_RATE:.0%}")
print(f"  Beta of debt: {BETA_DEBT}")

# Method 1: Lever up the beta, then use CAPM
print("\n--- Method 1: Re-lever beta, then apply CAPM ---")

# Re-levering formula: beta_levered = beta0 × (1 + (1 - tax_rate) × D/E)
nl_with_betas['beta_levered'] = nl_with_betas['industry_beta0'] * (1 + (1 - TAX_RATE) * nl_with_betas['de'])

# CAPM formula: Re = Rf + beta_levered × MRP
nl_with_betas['Re'] = RISK_FREE_RATE + nl_with_betas['beta_levered'] * MARKET_RISK_PREMIUM

print("\nCost of Equity Results:")
print(nl_with_betas[['Firm', 'sic3', 'de', 'industry_beta0', 'beta_levered', 'Re']])

# ============================================================================
# STEP 17: DISPLAY FINAL RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("FINAL RESULTS - COST OF EQUITY FOR NON-LISTED FIRMS")
print("=" * 80)

# Create a clean output dataframe
results = nl_with_betas[['Firm', 'sic3', 'de', 'industry_beta0', 'beta_levered', 'Re']].copy()
results.columns = ['Firm', 'Industry (SIC3)', 'D/E Ratio', 'Industry Beta (Unlevered)', 'Firm Beta (Levered)', 'Cost of Equity']

# Convert cost of equity to percentage
results['Cost of Equity (%)'] = results['Cost of Equity'] * 100
results = results.drop('Cost of Equity', axis=1)

# Round for better display
results['D/E Ratio'] = results['D/E Ratio'].round(3)
results['Industry Beta (Unlevered)'] = results['Industry Beta (Unlevered)'].round(4)
results['Firm Beta (Levered)'] = results['Firm Beta (Levered)'].round(4)
results['Cost of Equity (%)'] = results['Cost of Equity (%)'].round(2)

print("\n", results.to_string(index=False))

# Summary statistics
print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print(f"\nTotal non-listed firms analyzed: {len(results)}")
print(f"Average Cost of Equity: {results['Cost of Equity (%)'].mean():.2f}%")
print(f"Minimum Cost of Equity: {results['Cost of Equity (%)'].min():.2f}%")
print(f"Maximum Cost of Equity: {results['Cost of Equity (%)'].max():.2f}%")
print(f"Median Cost of Equity: {results['Cost of Equity (%)'].median():.2f}%")

# Save results to CSV
output_file = 'cost_of_equity_results.csv'
results.to_csv(output_file, index=False)
print(f"\n✓ Results saved to: {output_file}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
