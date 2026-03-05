# 🧬 Clinical Trial Success Analysis

**Author:** Fady Girbash
**LinkedIn:** [linkedin.com/in/fady-girbash](https://www.linkedin.com/in/fady-girbash)

---

## ⚠️ Important: Synthetic Data Only

All 1,000 clinical trials are **computer-generated** using Python. No real trial data, no confidential information. Built for portfolio demonstration while respecting pharmaceutical industry confidentiality requirements.

---

## 📊 Project Overview

End-to-end data pipeline analyzing synthetic oncology trials (2018-2023) to identify success drivers.

**Key Finding:** Multi-site trials take 72% longer but achieve 10% better enrollment success rates - risk diversification justifies the extended timeline.

---

## 🛠️ Tech Stack

- **Python** (Pandas, NumPy) - Data generation, cleaning, aggregation
- **Power BI** (DAX) - Interactive dashboard
- **Git/GitHub** - Version control

---

## 📁 Project Structure
```
├── data/
│   ├── raw/                      # Original generated data
│   └── processed/                # Cleaned data + 5 summary tables
├── scripts/
│   ├── 00_generate_data.py       # Generate 1,000 synthetic trials
│   ├── 01_clean_and_analyze.py   # Feature engineering
│   └── 02_create_summaries.py    # Pre-aggregated tables
├── dashboards/
│   └── Clinical_Trial_Dashboard_Final.pbix
└── README.md
```

---

## 🚀 Quick Start
```bash
# Generate data
python scripts/00_generate_data.py

# Clean and transform
python scripts/01_clean_and_analyze.py

# Create summaries
python scripts/02_create_summaries.py

# Open Power BI dashboard
# dashboards/Clinical_Trial_Dashboard_Final.pbix
```

---

## 📈 Key Metrics

**Dataset:**
- 1,000 synthetic oncology trials
- 4 phases (Phase 1-4)
- 8 cancer types
- 2018-2023 timeframe

**Success Rates:**
- Overall: 43% (both enrollment + endpoint met)
- Enrollment target met: 70%
- Primary endpoint met: 62%

**Operational Insights:**
- Multi-site trials: 93% of all trials
- Average duration: 30 months
- Phase 3: Longest (47 mo), lowest success (29%)

---

## 💡 Key Insights

1. **Multi-Site Trade-off:** +72% duration, +10% enrollment success
2. **Phase 3 Challenge:** 48 months average, only 29% overall success
3. **Size Doesn't Predict Speed:** Large trials can still be enrollment-efficient

---

## 📊 Dashboard Features

**Interactive visualizations:**
- Executive KPI overview (4 cards)
- Success rates by phase (clustered columns)
- Duration analysis (horizontal bars)
- Multi-site comparison (side-by-side)
- Time trends (2018-2023)
- Cancer type breakdown

**Interactivity:**
- Phase filtering across all visuals
- Cross-filtering between charts
- Drill-down capabilities

---

## 🧠 Skills Demonstrated

**Technical:**
- Python data pipelines (ETL)
- Data modeling (star schema)
- Power BI (DAX, relationships, interactivity)
- Git/GitHub workflow

**Domain Knowledge:**
- Clinical trial operations 
- Realistic blinding patterns by phase
- Enrollment distributions
- Multi-site coordination challenges

---

## 📸 Screenshots

<<<<<<< HEAD
![Dashboard Overview]

![Clinical_trial_project_success\screenshots\Clinical_trial_project overview.png](<screenshots/Clinical_trial_project overview.png>)

![screenshots/Key Insights.png](<screenshots/Key Insights.png>)
=======
![Dashboard Overview](![Clinical_trial_project_success\screenshots\Clinical_trial_project overview.png](<screenshots/Clinical_trial_project overview.png>))
>>>>>>> 455be2ad594391f72daf5bef076c002d60b53c03

# 📝 Next Steps

- [ ] Add predictive modeling (ML) # not sure #
- [ ] SQL database integration
- [ ] Web deployment (Power BI Service)
- [ ] Additional cancer types
- [ ] Real-time data refresh simulation

<<<<<<< HEAD
---

=======
>>>>>>> 455be2ad594391f72daf5bef076c002d60b53c03
**Status:** ✅ Complete | **Last Updated:** March 2026
