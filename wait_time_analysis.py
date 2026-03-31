import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/Users/varna/Desktop/Personal/Portfolio/Healthcare_analytics/healthcare/train_data.csv")

# ── 1. Basic overview ──────────────────────────────────────
print(f"Total patients: {df.shape[0]:,}")
print(f"Departments: {df['Department'].nunique()}")
print(f"Unique stay categories: {df['Stay'].nunique()}")

# ── 2. Map Stay to numeric midpoints for correlation ───────
stay_map = {
    '0-10': 5, '11-20': 15, '21-30': 25, '31-40': 35,
    '41-50': 45, '51-60': 55, '61-70': 65, '71-80': 75,
    '81-90': 85, '91-100': 95, 'More than 100 Days': 110
}
df['Stay_Numeric'] = df['Stay'].map(stay_map)

# ── 3. Avg stay by department ──────────────────────────────
print("\nAvg stay (days) by department:")
dept_avg = df.groupby('Department')['Stay_Numeric'].mean().round(1).sort_values(ascending=False)
print(dept_avg)

# ── 4. Avg stay by severity ────────────────────────────────
print("\nAvg stay (days) by severity:")
severity_avg = df.groupby('Severity of Illness')['Stay_Numeric'].mean().round(1).sort_values(ascending=False)
print(severity_avg)

# ── 5. Avg stay by admission type ─────────────────────────
print("\nAvg stay (days) by admission type:")
admission_avg = df.groupby('Type of Admission')['Stay_Numeric'].mean().round(1).sort_values(ascending=False)
print(admission_avg)

# ── 6. Avg stay by age group ───────────────────────────────
print("\nAvg stay (days) by age group:")
age_avg = df.groupby('Age')['Stay_Numeric'].mean().round(1)
print(age_avg)

# ── 7. Deposit vs stay correlation ────────────────────────
correlation = df['Admission_Deposit'].corr(df['Stay_Numeric'])
print(f"\nCorrelation between deposit and stay: {correlation:.3f}")

# ── 8. Bottleneck — dept + severity combo ─────────────────
print("\nTop 10 highest avg stay — dept + severity combo:")
bottleneck = df.groupby(['Department','Severity of Illness'])['Stay_Numeric'].mean().round(1)
print(bottleneck.sort_values(ascending=False).head(10))

# ── 9. Visitors impact on stay ────────────────────────────
print("\nAvg stay by number of visitors:")
visitors = df.groupby('Visitors with Patient')['Stay_Numeric'].mean().round(1)
print(visitors)

# ── 10. Plot 1 — Avg stay by department ───────────────────
plt.figure(figsize=(10,5))
dept_avg.plot(kind='bar', color='#2196F3')
plt.title('Average length of stay by department (days)')
plt.xlabel('Department')
plt.ylabel('Avg stay (days)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/Users/varna/Desktop/Personal/Portfolio/Healthcare_analytics/healthcare/images/avg_stay_by_dept.png')
print("\nChart 1 saved!")

# ── 11. Plot 2 — Avg stay by severity + admission type ────
fig, axes = plt.subplots(1, 2, figsize=(12,5))

severity_avg.plot(kind='bar', ax=axes[0], color='#F44336')
axes[0].set_title('Avg stay by severity of illness')
axes[0].set_xlabel('Severity')
axes[0].set_ylabel('Avg stay (days)')
axes[0].tick_params(axis='x', rotation=0)

admission_avg.plot(kind='bar', ax=axes[1], color='#4CAF50')
axes[1].set_title('Avg stay by admission type')
axes[1].set_xlabel('Admission type')
axes[1].set_ylabel('Avg stay (days)')
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('/Users/varna/Desktop/Personal/Portfolio/Healthcare_analytics/healthcare/images/stay_by_severity_admission.png')
print("Chart 2 saved!")

# ── 12. Plot 3 — Heatmap dept vs severity ─────────────────
plt.figure(figsize=(10,6))
heatmap_data = df.groupby(['Department','Severity of Illness'])['Stay_Numeric'].mean().unstack()
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('Avg stay heatmap — department vs severity (days)')
plt.tight_layout()
plt.savefig('/Users/varna/Desktop/Personal/Portfolio/Healthcare_analytics/healthcare/images/heatmap_dept_severity.png')
print("Chart 3 saved!")

# ── 13. Plot 4 — Avg stay by age group ────────────────────
plt.figure(figsize=(10,5))
age_order = ['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100']
age_avg.reindex(age_order).plot(kind='bar', color='#9C27B0')
plt.title('Average length of stay by patient age group (days)')
plt.xlabel('Age group')
plt.ylabel('Avg stay (days)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/Users/varna/Desktop/Personal/Portfolio/Healthcare_analytics/healthcare/images/stay_by_age.png')
print("Chart 4 saved!")

print("\nAll done!")