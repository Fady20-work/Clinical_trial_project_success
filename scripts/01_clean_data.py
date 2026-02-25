import pandas as pd
import numpy as np
from datetime import datetime

def clean_clinical_trials_data():
  
    df = pd.read_csv('data/raw/clinical_trials_raw.csv')
    print(f"Loaded {len(df)} trials from raw data")

    df['start_date'] = pd.to_datetime(df['start_date'])
    df['completion_date'] = pd.to_datetime(df['completion_date'])

    df['start_year'] = df['start_date'].dt.year
    df['completion_year'] = df['completion_date'].dt.year

    def categorize_enrollment(n):
        if n < 30:
            return 'Very Small (<30)'
        elif n < 100:
            return 'Small (30-100)'
        elif n < 300:
            return 'Medium (100-300)'
        elif n < 500:
            return 'Large (300-500)'
        else:
            return 'Very Large (500+)'

    df['enrollment_category'] = df['enrollment'].apply(categorize_enrollment)

    df['complexity_score'] = 0

    blinding_scores = {
        'Open Label': 0,
        'Single Blind': 1,
        'Double Blind': 2,
        'Triple Blind': 3,
        'Quadruple Blind': 4
    }
    df['complexity_score'] += df['blinding'].map(blinding_scores)

    # Randomization adds complexity (recruitment, stratification)
    df.loc[df['allocation'] == 'Randomized', 'complexity_score'] += 2
        
        # Complex intervention models
    intervention_complexity = {
        'Single Group Assignment': 0,
        'Parallel Assignment': 1,
        'Sequential Assignment': 2,
        'Crossover Assignment': 3,
        'Factorial Assignment': 4
    }
    df['complexity_score'] += df['intervention_model'].map(intervention_complexity).fillna(0)
        
        # Multi-region adds complexity (regulatory, coordination)
    df['region_count'] = df['regions'].str.count(',') + 1
    df.loc[df['region_count'] >= 3, 'complexity_score'] += 2
    df.loc[df['region_count'] == 2, 'complexity_score'] += 1

    def categorize_complexity(score):
        if score <= 3:
            return 'Low'
        elif score <= 6:
            return 'Medium'
        else:
            return 'High'
        
    df['enrollment_per_site'] = (df['enrollment'] / df['number_of_sites']).round(1)
    df['enrollment_rate'] = (df['enrollment'] / df['duration_months']).round(2)

    def categorize_duration(months):
        if months < 12:
            return 'Short (<1 year)'
        elif months < 24:
            return 'Medium (1-2 years)'
        elif months < 36:
            return 'Long (2-3 years)'
        else:
            return 'Very Long (3+ years)'

    # Calculate expected duration for each phase
    phase_median_duration = df.groupby('phase')['duration_months'].median()
    df['expected_duration'] = df['phase'].map(phase_median_duration)

    # On-time completion
    df['completed_on_time'] = df['duration_months'] <= df['expected_duration']

    # Overall success
    df['trial_success'] = df['primary_endpoint_met'] & df['completed_on_time']

    def categorize_risk(row):
        risk_score = 0
        
        if row['enrollment'] > 300:
            risk_score += 2          # Big trial = operational risk
        
        if row['region_count'] >= 3:
            risk_score += 2          # Multi-region = coordination risk
        
        if row['phase'] == 'Phase 3':
            risk_score += 1          # High stakes
        
        if row['complexity_score'] > 6:
            risk_score += 1          # Hard to execute
        
        if risk_score <= 2:
            return 'Low Risk'
        elif risk_score <= 4:
            return 'Medium Risk'
        else:
            return 'High Risk'
        
    df['estimated_cost_millions'] = (
        (df['enrollment'] * 3000 +                    # $3K per patient
        df['number_of_sites'] * 50000 * df['duration_months'])  # $50K per site per month
        / 1000000
    ).round(2)

    df['cost_per_patient_thousands'] = (
        df['estimated_cost_millions'] * 1000 / df['enrollment']
    ).round(1)

# ========================================================================
    # 9. SAVE CLEANED DATA
    # ========================================================================
    output_path = 'data/processed/clinical_trials_clean.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Cleaning complete!")
    print(f"✓ Saved to {output_path}")
    
    # ========================================================================
    # 10. SHOW SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print("CLEANED DATASET SUMMARY")
    print("="*70)
    
    print(f"\n📊 TOTAL TRIALS: {len(df)}")
    
    print(f"\n📊 COMPLEXITY DISTRIBUTION:")
    print(df['complexity_category'].value_counts())
    
    print(f"\n📊 RISK DISTRIBUTION:")
    print(df['risk_category'].value_counts())
    
    print(f"\n📊 SUCCESS METRICS:")
    print(f"  Primary Endpoint Met: {df['primary_endpoint_met'].mean()*100:.1f}%")
    print(f"  Completed On Time: {df['completed_on_time'].mean()*100:.1f}%")
    print(f"  Overall Success: {df['trial_success'].mean()*100:.1f}%")
    
    print(f"\n📊 COST ANALYSIS:")
    print(f"  Average Cost: ${df['estimated_cost_millions'].mean():.1f}M")
    print(f"  Median Cost: ${df['estimated_cost_millions'].median():.1f}M")
    print(f"  Total Investment: ${df['estimated_cost_millions'].sum():.0f}M")
    
    print(f"\n📊 EFFICIENCY METRICS:")
    print(f"  Avg Enrollment/Site: {df['enrollment_per_site'].mean():.1f} patients")
    print(f"  Avg Enrollment Rate: {df['enrollment_rate'].mean():.1f} patients/month")
    print(f"  Avg Cost/Patient: ${df['cost_per_patient_thousands'].mean():.0f}K")
    
    print("\n" + "="*70)
    print("✅ Data ready for analysis!")
    print("="*70)
    
    return df

# Run the cleaning script
if __name__ == "__main__":
    df_clean = clean_clinical_trials_data()
