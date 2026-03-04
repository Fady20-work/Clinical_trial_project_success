# ============================================================================
# CREATE SUMMARY TABLES
# ============================================================================
# Creates pre-aggregated tables for Power BI
# Makes dashboard building way faster
# ============================================================================

import pandas as pd

def create_summary_tables():
    
    print("Loading cleaned data...")
    df = pd.read_csv('data/processed/clinical_trials_processed.csv')
    print(f"Got {len(df)} trials\n")
    
# ========================================================================
# PHASE SUMMARY (most important one)
# ========================================================================
    print("Creating phase summary...")
    
    phase_stats = df.groupby('Phase').agg({
        'trial_id': 'count',
        'duration_months': 'mean',
        'actual_enrollment': 'mean',
        'enrollment_rate': 'mean',
        'patients_per_site': 'mean',
        'enrollment_achievement_pct': 'mean',
        'enrollment_met_target': 'mean',
        'primary_endpoint_met': 'mean',
        'overall_success': 'mean'
    }).round(1)
    
    # Rename columns to something readable
    phase_stats.columns = [
        'Trial_Count',
        'Avg_Duration_Months',
        'Avg_Enrollment',
        'Avg_Enrollment_Rate',
        'Avg_Patients_Per_Site',
        'Avg_Achievement_Pct',
        'Enrollment_Success_Rate',
        'Endpoint_Success_Rate',
        'Overall_Success_Rate'
    ]
    
    # Convert to percentages
    for col in ['Enrollment_Success_Rate', 'Endpoint_Success_Rate', 'Overall_Success_Rate']:
        phase_stats[col] = (phase_stats[col] * 100).round(1)
    
    phase_stats = phase_stats.reset_index()
    phase_stats.to_csv('data/processed/summary_by_phase.csv', index=False)
    print("✓ summary_by_phase.csv")
    
    # ========================================================================
    # YEAR TRENDS
    # ========================================================================
    print("Creating year trends...")
    
    by_year = df.groupby('start_year').agg({
        'trial_id': 'count',
        'duration_months': 'mean',
        'actual_enrollment': 'mean',
        'enrollment_met_target': 'mean',
        'primary_endpoint_met': 'mean',
        'overall_success': 'mean'
    }).round(1)
    
    by_year.columns = [
        'Trial_Count',
        'Avg_Duration_Months',
        'Avg_Enrollment',
        'Enrollment_Success_Rate',
        'Endpoint_Success_Rate',
        'Overall_Success_Rate'
    ]
    
    # Convert success rates to %
    by_year['Enrollment_Success_Rate'] *= 100
    by_year['Endpoint_Success_Rate'] *= 100
    by_year['Overall_Success_Rate'] *= 100
    by_year = by_year.round(1)
    
    by_year = by_year.reset_index()
    by_year.rename(columns={'start_year': 'Year'}, inplace=True)
    by_year.to_csv('data/processed/summary_by_year.csv', index=False)
    print("✓ summary_by_year.csv")
    
    # ========================================================================
    # CANCER TYPE BREAKDOWN
    # ========================================================================
    print("Creating cancer type breakdown...")
    
    cancer_df = df.groupby('cancer_type').agg({
        'trial_id': 'count',
        'duration_months': 'mean',
        'actual_enrollment': ['mean', 'sum'],
        'enrollment_met_target': 'mean',
        'primary_endpoint_met': 'mean',
        'overall_success': 'mean'
    }).round(1)
    
    cancer_df.columns = [
        'Trial_Count',
        'Avg_Duration_Months',
        'Avg_Enrollment',
        'Total_Enrollment',
        'Enrollment_Success_Rate',
        'Endpoint_Success_Rate',
        'Overall_Success_Rate'
    ]
    
    # Percentages again
    cancer_df['Enrollment_Success_Rate'] = (cancer_df['Enrollment_Success_Rate'] * 100).round(1)
    cancer_df['Endpoint_Success_Rate'] = (cancer_df['Endpoint_Success_Rate'] * 100).round(1)
    cancer_df['Overall_Success_Rate'] = (cancer_df['Overall_Success_Rate'] * 100).round(1)
    
    cancer_df = cancer_df.reset_index()
    cancer_df = cancer_df.sort_values('Trial_Count', ascending=False)
    cancer_df.to_csv('data/processed/summary_by_cancer_type.csv', index=False)
    print("✓ summary_by_cancer_type.csv")
    
    # ========================================================================
    # SIZE CATEGORIES
    # ========================================================================
    print("Creating size summary...")
    
    size_df = df.groupby('size_category').agg({
        'trial_id': 'count',
        'duration_months': 'mean',
        'actual_enrollment': 'mean',
        'enrollment_rate': 'mean',
        'enrollment_met_target': 'mean',
        'overall_success': 'mean'
    }).round(1)
    
    size_df.columns = [
        'Trial_Count',
        'Avg_Duration_Months',
        'Avg_Enrollment',
        'Avg_Enrollment_Rate',
        'Enrollment_Success_Rate',
        'Overall_Success_Rate'
    ]
    
    size_df['Enrollment_Success_Rate'] = (size_df['Enrollment_Success_Rate'] * 100).round(1)
    size_df['Overall_Success_Rate'] = (size_df['Overall_Success_Rate'] * 100).round(1)
    
    size_df = size_df.reset_index()
    size_df.to_csv('data/processed/summary_by_size.csv', index=False)
    print("✓ summary_by_size.csv")
    
    # ========================================================================
    # MULTI-SITE COMPARISON
    # ========================================================================
    print("Creating site comparison...")
    
    site_comparison = df.groupby('is_multi_site').agg({
        'trial_id': 'count',
        'duration_months': 'mean',
        'actual_enrollment': 'mean',
        'enrollment_rate': 'mean',
        'patients_per_site': 'mean',
        'enrollment_met_target': 'mean',
        'overall_success': 'mean'
    }).round(1)
    
    site_comparison.columns = [
        'Trial_Count',
        'Avg_Duration_Months',
        'Avg_Enrollment',
        'Avg_Enrollment_Rate',
        'Avg_Patients_Per_Site',
        'Enrollment_Success_Rate',
        'Overall_Success_Rate'
    ]
    
    site_comparison['Enrollment_Success_Rate'] = (site_comparison['Enrollment_Success_Rate'] * 100).round(1)
    site_comparison['Overall_Success_Rate'] = (site_comparison['Overall_Success_Rate'] * 100).round(1)
    
    site_comparison = site_comparison.reset_index()
    site_comparison['is_multi_site'] = site_comparison['is_multi_site'].map({
        True: 'Multi-Site',
        False: 'Single-Site'
    })
    site_comparison.to_csv('data/processed/summary_by_site_type.csv', index=False)
    print("✓ summary_by_site_type.csv")
    
    # Done!
    print("\n" + "="*60)
    print("All summaries created successfully!")
    print("="*60)
    print("\nFiles saved in: data/processed/")
    print("Ready for Power BI!\n")
    
    # Quick preview
    print("Preview of phase summary:")
    print(phase_stats.head())

if __name__ == "__main__":
    create_summary_tables()