# ============================================================================
# DATA CLEANING & ANALYSIS
# ============================================================================
# This script cleans the raw trial data and adds basic calculated fields
# Focuses on enrollment rates, success metrics, and operational categories
# ============================================================================

import pandas as pd
import numpy as np

def clean_trial_data(df):

    print("Loading raw trial data...")
    df = pd.read_csv('data/raw/clinical_trials_raw.csv')
    print(f"✓ Loaded {len(df)} trials")

# ========================================================================
# 1. CONVERT DATES
# ========================================================================

    print("\n1. Converting dates...")

    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    df['start_year'] = df['start_date'].dt.year
    df['end_year'] = df['end_date'].dt.year

    print("✓ Dates converted to year format")

# ========================================================================
# 2. CALCULATE ENROLLMENT METRICS
# ========================================================================

    print("\n2. Calculating enrollment metrics...")

    df['enrollment_rate'] = (df['actual_enrollment'] / df['duration_months']).round(2)

    df['patients_per_site'] = (df['actual_enrollment'] / df['number_of_sites']).round(1)

    df['enrollment_achievement_pct'] = ((df['actual_enrollment'] / df['target_enrollment']) * 100).round(1)

    print("✓ Enrollment metrics calculated")

# ========================================================================
# 3. CREATE OPERATIONAL CATEGORIES
# ========================================================================

    print("\n3. Creating operational categories...")

    df['is_multi_site'] = df['number_of_sites'] > 1

    df['is_multi_region'] = df['regions'] > 1

# Trial size categories

    def categorize_size(enrollment):
        if enrollment < 50:
            return 'Small (<50)'
        elif enrollment < 150 :
            return 'medium (50-150)'
        elif enrollment < 400 :
            return 'large (150-400)'
        else:
            return 'very large (400+)'

    df['size_category'] = df['actual_enrollment'].apply(categorize_size)

# Duration categories

    def categorize_duration(months):
        if months < 18:
            return 'short(<18mo)'
        elif months < 36:
            return 'medium(18-36mo)'
        else:
            return 'long(36mo+)'
    
    df['duration_category'] = df['duration_months'].apply(categorize_duration)

    print("✓ Categories created")

# ========================================================================
# 4. SUCCESS INDICATORS
# ========================================================================

    print("]n4. Calculating success indicators...")

    df['overall_success'] = (df['enrollment_met_target'] & df['primary_endpoint_met'])

    # Enrollment success level

    def enrollment_success_level(pct):
        if pct >= 100:
            return 'Exceeded Target'
        elif pct >= 90:
            return 'Met Target'
        elif pct >= 75:
            return 'Near Target'
        else:
            return 'Below Target'
    
    df['enrollment_success_level'] = df['enrollment_achievement_pct'].apply(enrollment_success_level)

# ========================================================================
# 5. SAVE CLEANED DATA
# ========================================================================

    output_path = 'data/processed/clinical_trials_processed.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✓ Cleaned data saved to {output_path}")

# ========================================================================
# 6. SUMMARY STATISTICS
# ========================================================================

    print(f"\nTotal Trials : {len(df)}")

    print(f"\n📊 ENROLLMENT METRICS:")
    print(f"  Average Enrollment Rate: {df['enrollment_rate'].mean():.1f} patients/month")
    print(f"  Average Patients per Site: {df['patients_per_site'].mean():.1f}")
    print(f"  Average Achievement: {df['enrollment_achievement_pct'].mean():.1f}%")
    
    print(f"\n📊 OPERATIONAL BREAKDOWN:")
    print(f"  Multi-Site Trials: {df['is_multi_site'].sum()} ({df['is_multi_site'].mean()*100:.1f}%)")
    print(f"  Multi-Region Trials: {df['is_multi_region'].sum()} ({df['is_multi_region'].mean()*100:.1f}%)")
    
    print(f"\n📊 SIZE DISTRIBUTION:")
    print(df['size_category'].value_counts().to_string())
    
    print(f"\n📊 DURATION DISTRIBUTION:")
    print(df['duration_category'].value_counts().to_string())
    
    print(f"\n📊 ENROLLMENT SUCCESS:")
    print(df['enrollment_success_level'].value_counts().to_string())
    
    print(f"\n📊 SUCCESS RATES:")
    print(f"  Enrollment Target Met: {df['enrollment_met_target'].mean()*100:.1f}%")
    print(f"  Primary Endpoint Met: {df['primary_endpoint_met'].mean()*100:.1f}%")
    print(f"  Overall Success (Both): {df['overall_success'].mean()*100:.1f}%")
    
    print("\n" + "="*70)
    print("✅ Data cleaning complete!")
    print("="*70)
    
    return df

if __name__ == "__main__":
    df_clean = clean_trial_data('data/processed/clinical_trials_processed.csv')
    print("\nNext step: Create summary analysis tables\n")