"""
WRDS Data Download Script for Cost of Equity Project

This script downloads CRSP and Compustat data from WRDS using the Python API.
You need a WRDS account to use this script.

Installation:
    pip install wrds

Usage:
    python download_wrds_data.py

Note: You will be prompted for your WRDS username and password.
"""

import wrds
import pandas as pd
import sys

def download_crsp_data(db):
    """
    Download CRSP monthly stock data (2015-2020)
    
    Variables:
    - CUSIP: Company identifier
    - date: Date of observation
    - RET: Holding period return
    - EWRETD: Equal-weighted return including distributions
    """
    print("Downloading CRSP data...")
    print("Date range: 2015-01 to 2020-12")
    
    crsp_query = """
    SELECT cusip, date, ret, ewretd
    FROM crsp.msf
    WHERE date BETWEEN '2015-01-01' AND '2020-12-31'
      AND cusip IS NOT NULL
      AND ret IS NOT NULL
    ORDER BY cusip, date
    """
    
    try:
        crsp_data = db.raw_sql(crsp_query)
        print(f"✓ Downloaded {len(crsp_data):,} observations")
        print(f"✓ Unique firms: {crsp_data['cusip'].nunique():,}")
        return crsp_data
    except Exception as e:
        print(f"✗ Error downloading CRSP data: {e}")
        return None


def download_compustat_data(db):
    """
    Download Compustat annual fundamental data (2020)
    
    Variables:
    - FYEAR: Fiscal year
    - FYR: Fiscal year end
    - CUSIP: Company identifier
    - SIC: Standard Industry Classification code
    - DT: Total debt including current
    - PRCC_F: Price close - annual - fiscal
    - CSHO: Common shares outstanding
    """
    print("\nDownloading Compustat data...")
    print("Fiscal year: 2020")
    
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
      AND indfmt = 'INDL'
      AND datafmt = 'STD'
      AND popsrc = 'D'
      AND consol = 'C'
    """
    
    try:
        compustat_data = db.raw_sql(compustat_query)
        print(f"✓ Downloaded {len(compustat_data):,} firms")
        print(f"✓ Unique industries (SIC): {compustat_data['sic'].nunique():,}")
        return compustat_data
    except Exception as e:
        print(f"✗ Error downloading Compustat data: {e}")
        return None


def main():
    """Main function to download and save data"""
    
    print("=" * 60)
    print("WRDS Data Download for Cost of Equity Project")
    print("=" * 60)
    
    # Connect to WRDS
    print("\nConnecting to WRDS...")
    print("You will be prompted for your WRDS username and password.")
    
    try:
        db = wrds.Connection()
        print("✓ Successfully connected to WRDS")
    except Exception as e:
        print(f"✗ Failed to connect to WRDS: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a WRDS account")
        print("2. Check your username and password")
        print("3. Verify your institution has WRDS subscription")
        sys.exit(1)
    
    # Download CRSP data
    crsp_data = download_crsp_data(db)
    if crsp_data is None:
        print("\n✗ Failed to download CRSP data. Exiting.")
        db.close()
        sys.exit(1)
    
    # Download Compustat data
    compustat_data = download_compustat_data(db)
    if compustat_data is None:
        print("\n✗ Failed to download Compustat data. Exiting.")
        db.close()
        sys.exit(1)
    
    # Close connection
    db.close()
    print("\n✓ Closed WRDS connection")
    
    # Save data to CSV files
    print("\nSaving data to CSV files...")
    
    try:
        crsp_filename = 'crsp_monthly_returns.csv'
        crsp_data.to_csv(crsp_filename, index=False)
        print(f"✓ Saved CRSP data to: {crsp_filename}")
        
        compustat_filename = 'compustat_2020.csv'
        compustat_data.to_csv(compustat_filename, index=False)
        print(f"✓ Saved Compustat data to: {compustat_filename}")
    except Exception as e:
        print(f"✗ Error saving files: {e}")
        sys.exit(1)
    
    # Display summary statistics
    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)
    
    print("\nCRSP Data:")
    print(f"  - Total observations: {len(crsp_data):,}")
    print(f"  - Unique firms (CUSIP): {crsp_data['cusip'].nunique():,}")
    print(f"  - Date range: {crsp_data['date'].min()} to {crsp_data['date'].max()}")
    print(f"  - Average return: {crsp_data['ret'].mean():.4f}")
    
    print("\nCompustat Data:")
    print(f"  - Total firms: {len(compustat_data):,}")
    print(f"  - Unique industries: {compustat_data['sic'].nunique():,}")
    print(f"  - Average total debt: ${compustat_data['dt'].mean():,.2f}M")
    print(f"  - Average stock price: ${compustat_data['prcc_f'].mean():.2f}")
    
    print("\n" + "=" * 60)
    print("✓ Data download complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify the CSV files were created")
    print("2. Open them to check the data looks correct")
    print("3. Run the main analysis script: cost_of_equity_estimation.py")


if __name__ == "__main__":
    main()
