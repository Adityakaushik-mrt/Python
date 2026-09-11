# 👥 HR Analytics & Attrition Analysis Dashboard

![HR Dashboard Preview](https://github.com/Adityakaushik-mrt/Python/blob/main/HR%20Analysis/dash.PNG?raw=true)

An exploratory data analysis (EDA) and visualization dashboard built using Python. This project evaluates organizational turnover patterns, education backgrounds, marital status attrition rates, and role-based satisfaction scores to assist HR business partners in talent retention strategies.

---

## 📌 Business Insights Uncovered

1. **Attrition by Department:**
   * **R&D** accounts for the largest share of turnover (**65.4%**), followed by **Sales** (**30.3%**), while **HR** accounts for **4.3%**.
2. **High-Risk Roles (Treemap Analysis):**
   * Turnover is heavily concentrated in frontline and operational roles: **Laboratory Technicians (62)**, **Sales Executives (57)**, and **Research Scientists (47)**.
3. **Marital Status & Turnover:**
   * **Single employees** display the highest relative attrition rate (**115 out of 465**, ~24.7%), compared to married (**84 out of 673**, ~12.5%) and divorced cohorts.
4. **Workforce Pipeline:**
   * The majority of the workforce holds degrees in **Life Sciences (606)** and **Medical (464)** fields.
   * Peak headcount is concentrated in the **25–34 age bracket** across both male and female talent.
5. **Role Satisfaction:**
   * Heatmap analysis flags specific roles with low satisfaction scores (Rating 1 & 2), identifying priority areas for HR pulse checks and manager coaching.

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn, Squarify (for Treemap plotting)

---

## 📂 Project Structure

hr-analytics-dashboard/
│
├── assets/
│   └── hr_dashboard_preview.png   # Dashboard screenshot
├── data/
│   └── hr_employee_data.csv       # Source dataset
├── hr_dashboard.py                # Main plotting script
├── requirements.txt               # Dependencies
└── README.md
