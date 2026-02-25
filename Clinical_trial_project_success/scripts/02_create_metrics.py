import pandas as pd

def create_analysis_metrics():
    # Load cleaned data
    df = pd.read_csv('data/processed/clinical_trials_clean.csv')
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['completion_date'] = pd.to_datetime(df['completion_date'])
    
    print(f"Creating analysis metrics from {len(df)} trials...")

    phase_metrics = df.groupby('phase').agg({
        'nct_id': 'count',
        'duration_months': ['mean', 'median', 'std'],
        'enrollment': ['mean', 'median', 'std'],
        'complexity_score': 'mean',
        'estimated_cost_millions': ['mean', 'median', 'sum'],
        'primary_endpoint_met': 'mean',
        'completed_on_time': 'mean',
        'trial_success': 'mean',
        'dropout_rate_percent': 'mean',
        'sae_per_100_patients': 'mean',
        'enrollment_rate': 'mean'
    }).round(2)

    # Flatten column names
    phase_metrics.columns = ['_'.join(col).strip() for col in phase_metrics.columns]
    phase_metrics = phase_metrics.reset_index()

    # Rename for clarity
    phase_metrics.columns = [
        'Phase', 'Trial_Count',
        'Avg_Duration', 'Median_Duration', 'StdDev_Duration',
        'Avg_Enrollment', 'Median_Enrollment', 'StdDev_Enrollment',
        'Avg_Complexity',
        'Avg_Cost_Millions', 'Median_Cost_Millions', 'Total_Cost_Millions',
        'Endpoint_Success_Rate', 'OnTime_Success_Rate', 'Overall_Success_Rate',
        'Avg_Dropout_Rate', 'Avg_SAE_Rate', 'Avg_Enrollment_Rate'
    ]

    phase_metrics.to_csv('data/processed/metrics_by_phase.csv', index=False)
    print("✓ Created: metrics_by_phase.csv")

    # ========================================================================
    # 2. METRICS BY YEAR
    # ========================================================================
    print("📊 Generating metrics by year...")

    year_metrics = df.groupby('start_year').agg({
        'nct_id': 'count',
        'duration_months': 'mean',
        'enrollment': 'mean',
        'estimated_cost_millions': ['mean', 'sum'],
        'primary_endpoint_met': 'mean',
        'trial_success': 'mean'
    }).round(2)

    year_metrics.columns = ['_'.join(col).strip() for col in year_metrics.columns]
    year_metrics = year_metrics.reset_index()
    year_metrics.columns = [
        'Year', 'Trial_Count', 'Avg_Duration', 'Avg_Enrollment',
        'Avg_Cost_Millions', 'Total_Investment_Millions',
        'Endpoint_Success_Rate', 'Overall_Success_Rate'
    ]

    year_metrics.to_csv('data/processed/metrics_by_year.csv', index=False)
    print("✓ Created: metrics_by_year.csv")

    # ========================================================================
    # 3. METRICS BY CANCER TYPE
    # ========================================================================
    print("📊 Generating metrics by cancer type...")

    cancer_metrics = df.groupby('cancer_type').agg({
        'nct_id': 'count',
        'duration_months': 'mean',
        'enrollment': ['mean', 'sum'],
        'estimated_cost_millions': 'sum',
        'primary_endpoint_met': 'mean',
        'trial_success': 'mean'
    }).round(2)

    cancer_metrics.columns = ['_'.join(col).strip() for col in cancer_metrics.columns]
    cancer_metrics = cancer_metrics.reset_index()
    cancer_metrics.columns = [
        'Cancer_Type', 'Trial_Count', 'Avg_Duration',
        'Avg_Enrollment', 'Total_Enrollment',
        'Total_Investment_Millions', 'Endpoint_Success_Rate', 'Overall_Success_Rate'
    ]

    # Sort by trial count
    cancer_metrics = cancer_metrics.sort_values('Trial_Count', ascending=False)
    cancer_metrics.to_csv('data/processed/metrics_by_cancer_type.csv', index=False)
    print("✓ Created: metrics_by_cancer_type.csv")

    # ========================================================================
    # 4. METRICS BY SPONSOR
    # ========================================================================
    print("📊 Generating metrics by sponsor...")

    sponsor_metrics = df.groupby('sponsor').agg({
        'nct_id': 'count',
        'duration_months': 'mean',
        'enrollment': 'mean',
        'estimated_cost_millions': 'sum',
        'primary_endpoint_met': 'mean',
        'trial_success': 'mean'
    }).round(2)

    sponsor_metrics.columns = ['_'.join(col).strip() for col in sponsor_metrics.columns]
    sponsor_metrics = sponsor_metrics.reset_index()
    sponsor_metrics.columns = [
        'Sponsor', 'Trial_Count', 'Avg_Duration', 'Avg_Enrollment',
        'Total_Investment_Millions', 'Endpoint_Success_Rate', 'Overall_Success_Rate'
    ]

    # Sort by trial count
    sponsor_metrics = sponsor_metrics.sort_values('Trial_Count', ascending=False)
    sponsor_metrics.to_csv('data/processed/metrics_by_sponsor.csv', index=False)
    print("✓ Created: metrics_by_sponsor.csv")

    # ========================================================================
    # 5. COMPLEXITY ANALYSIS
    # ========================================================================
    print("📊 Generating complexity analysis...")

    complexity_analysis = df.groupby('complexity_category').agg({
        'duration_months': 'mean',
        'enrollment': 'mean',
        'estimated_cost_millions': 'mean',
        'nct_id': 'count',
        'trial_success': 'mean',
        'dropout_rate_percent': 'mean'
    }).round(2)

    complexity_analysis = complexity_analysis.reset_index()
    complexity_analysis.columns = [
        'Complexity_Level', 'Avg_Duration', 'Avg_Enrollment',
        'Avg_Cost_Millions', 'Trial_Count', 'Success_Rate', 'Avg_Dropout_Rate'
    ]

    complexity_analysis.to_csv('data/processed/complexity_analysis.csv', index=False)
    print("✓ Created: complexity_analysis.csv")

    # ========================================================================
    # 6. RISK ANALYSIS
    # ========================================================================
    print("📊 Generating risk analysis...")

    risk_analysis = df.groupby('risk_category').agg({
        'duration_months': 'mean',
        'enrollment': 'mean',
        'estimated_cost_millions': 'mean',
        'nct_id': 'count',
        'trial_success': 'mean',
        'dropout_rate_percent': 'mean',
        'sae_per_100_patients': 'mean'
    }).round(2)

    risk_analysis = risk_analysis.reset_index()
    risk_analysis.columns = [
        'Risk_Level', 'Avg_Duration', 'Avg_Enrollment',
        'Avg_Cost_Millions', 'Trial_Count', 'Success_Rate',
        'Avg_Dropout_Rate', 'Avg_SAE_Rate'
    ]

    risk_analysis.to_csv('data/processed/risk_analysis.csv', index=False)
    print("✓ Created: risk_analysis.csv")

    # ========================================================================
    # 7. SUCCESS FACTORS COMPARISON
    # ========================================================================
    print("📊 Generating success factors analysis...")

    success_comparison = df.groupby('trial_success').agg({
        'duration_months': 'mean',
        'enrollment': 'mean',
        'complexity_score': 'mean',
        'number_of_sites': 'mean',
        'region_count': 'mean',
        'dropout_rate_percent': 'mean',
        'sae_per_100_patients': 'mean',
        'estimated_cost_millions': 'mean'
    }).round(2)

    success_comparison = success_comparison.reset_index()
    success_comparison['trial_success'] = success_comparison['trial_success'].map({
        True: 'Successful', False: 'Unsuccessful'
    })
    success_comparison.columns = [
        'Trial_Outcome', 'Avg_Duration', 'Avg_Enrollment',
        'Avg_Complexity', 'Avg_Sites', 'Avg_Regions',
        'Avg_Dropout_Rate', 'Avg_SAE_Rate', 'Avg_Cost_Millions'
    ]

    success_comparison.to_csv('data/processed/success_factors_analysis.csv', index=False)
    print("✓ Created: success_factors_analysis.csv")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print("✅ ALL ANALYSIS FILES CREATED")
    print("="*70)

    print("\n📊 Ready for Power BI:")
    print("  1. clinical_trials_clean.csv - Main dataset")
    print("  2. metrics_by_phase.csv - Phase comparison")
    print("  3. metrics_by_year.csv - Yearly trends")
    print("  4. metrics_by_cancer_type.csv - Cancer analysis")
    print("  5. metrics_by_sponsor.csv - Sponsor performance")
    print("  6. complexity_analysis.csv - Complexity impact")
    print("  7. risk_analysis.csv - Risk assessment")
    print("  8. success_factors_analysis.csv - Success drivers")

    print("\n📁 All files saved in: data/processed/")
    print("\n🎯 Next Step: Import these into Power BI Desktop!")
    print("="*70)

    # Run the script
    if __name__ == "__main__":
        create_analysis_metrics()