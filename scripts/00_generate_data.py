# ============================================================================
# SYNTHETIC DATA GENERATION
# ============================================================================
# This script generates FAKE clinical trial data for portfolio demonstration
# NO real trial data, NO confidential information, NO company data
# Patterns based on public ClinicalTrials.gov statistics
# ============================================================================
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_trial_data(n_trials=1000):

    print(f"Generating {n_trials} synthetic clinical trials...")
    trials = []

    phases = ['Phase 1','Phase 2','Phase 3','Phase 4']
    phase_weights = [0.25 , 0.40 , 0.25 , 0.10]
    
    cancer_types = ['Breast Cancer', 'Lung Cancer', 'Colorectal Cancer', 'Prostate Cancer',
        'Melanoma', 'Leukemia', 'Lymphoma', 'Pancreatic Cancer']
    
    sponsors = [ "OncoPharm Therapeutics", "Global BioResearch", "Apex Oncology Labs", "NovaCure Biotech", "Helix Therapeutics",
    "Clinical Research Group A","MedTrials International"]

    for i in range(n_trials):
        trial_id = f"TRIAL-{str(i+1).zfill(4)}"
        phase = random.choices(phases , phase_weights)[0]
        cancer_type = random.choice(cancer_types)
        sponsor = random.choice(sponsors)

        # ------------------------
        # Phase-Dependent Blinding (Advanced Logic)
        # ------------------------

        if phase == 'Phase 1':
            blinding_type = random.choices(["Open Label" , "Single Blind"] , weights=[0.80 , 0.20])[0]
        elif phase == 'Phase 3':
            blinding_type = random.choices(["Double Blind" , "Triple Blind"] , weights =[0.75 , 0.25])[0]
        else:
            blinding_type = random.choices(["Open Label" , "Single Blind" , "Double Blind"] , weights =[0.30 , 0.20 , 0.50])[0]

        # ------------------------
        # Enrollment Modeling
        # ------------------------

        if phase == 'Phase 1':
                target_enrollment = int(np.random.normal(30, 10))
        elif phase == 'Phase 2':
            target_enrollment = int(np.random.normal(100, 30))
        elif phase == 'Phase 3':
            target_enrollment = int(np.random.normal(400, 100))
        else:
            target_enrollment = int(np.random.normal(200, 60))

        target_enrollment = max(15, target_enrollment)

        enrollment_achievement = np.random.beta(12, 1)
        actual_enrollment = int(target_enrollment * enrollment_achievement)
        actual_enrollment = max(10, actual_enrollment)

            # ------------------------
            # Duration Modeling
            # ------------------------

        if phase == 'Phase 1':
            duration_months = int(np.random.normal(18, 5))
        elif phase == 'Phase 2':
            duration_months = int(np.random.normal(28, 8))
        elif phase == 'Phase 3':
            duration_months = int(np.random.normal(48, 12))
        else:
            duration_months = int(np.random.normal(36, 10))

        duration_months = max(6, duration_months)

        # ------------------------
        # Operational Complexity
        # ------------------------

        if actual_enrollment < 40:
            number_of_sites = random.randint(1, 3)
        elif actual_enrollment < 150:
            number_of_sites = random.randint(2, 8)
        elif actual_enrollment < 400:
            number_of_sites = random.randint(5, 20)
        else:
            number_of_sites = random.randint(15, 50)

        if number_of_sites <= 3:
            regions = 1
        elif number_of_sites <= 10:
            regions = random.choices([1, 2], weights=[0.6, 0.4])[0]
        else:
            regions = random.choices([1, 2, 3], weights=[0.2, 0.5, 0.3])[0]

        # ------------------------
        # Dates
        # ------------------------

        start_year = random.randint(2018, 2023)
        start_month = random.randint(1, 12)
        start_day = random.randint(1, 28)

        start_date = datetime(start_year, start_month, start_day)
        end_date = start_date + timedelta(days=duration_months * 30)

        # ------------------------
        # Success Metrics
        # ------------------------

        enrollment_met_target = actual_enrollment >= (target_enrollment * 0.90)

        if phase == 'Phase 3':
            primary_endpoint_met = random.choices([True, False], weights=[0.50, 0.50])[0]
        elif phase == 'Phase 2':
            primary_endpoint_met = random.choices([True, False], weights=[0.65, 0.35])[0]
        else:
            primary_endpoint_met = random.choices([True, False], weights=[0.70, 0.30])[0]

        # ------------------------
        # Trial Record
        # ------------------------

        trial = {
            'trial_id': trial_id,
            'Phase': phase,
            'cancer_type': cancer_type,
            'sponsor': sponsor,
            'blinding_type': blinding_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'duration_months': duration_months,
            'target_enrollment': target_enrollment,
            'actual_enrollment': actual_enrollment,
            'number_of_sites': number_of_sites,
            'regions': regions,
            'enrollment_met_target': enrollment_met_target,
            'primary_endpoint_met': primary_endpoint_met
        }

        trials.append(trial)

    df = pd.DataFrame(trials)

    # Save dataset
    df.to_csv('data/raw/clinical_trials_raw.csv', index=False)

    # ------------------------
    # Summary Output
    # ------------------------

    print("✓ Dataset generated successfully")
    print(f"✓ Total Trials: {len(df)}")
    print("\nPhase Distribution:")
    print(df['Phase'].value_counts())

    print(f"\nAverage Duration: {df['duration_months'].mean():.1f} months")
    print(f"Average Enrollment: {df['actual_enrollment'].mean():.0f} patients")
    print(f"Enrollment Target Met: {df['enrollment_met_target'].mean()*100:.1f}%")
    print(f"Primary Endpoint Met: {df['primary_endpoint_met'].mean()*100:.1f}%")

    return df

if __name__ == "__main__":
    df = generate_trial_data(1000)
    print("\nData generation complete.\n")