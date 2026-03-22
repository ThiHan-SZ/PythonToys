import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'GEADatawork\Group2_GEA.csv')

df = df.iloc[:,:26]

# Convert BMI to numeric, turning "NA" strings and invalid values into NaN
df["BMI"] = pd.to_numeric(df["BMI"], errors="coerce")

print(df.head(4))

# Optionally, also replace 0 BMI with NaN (biologically implausible)
df["BMI"] = df["BMI"].replace(0, pd.NA)

df.dropna(inplace=True)

print(df)

bmi_by_country = (
    df.groupby("Country")["BMI"]
    .agg(
        count="count",       # non-NaN entries only
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max",
        q25=lambda x: x.quantile(0.25),
        q75=lambda x: x.quantile(0.75)
    )
    .round(2)
    .reset_index()
)
bmi_by_country.to_csv(r'GEADatawork\bmi_by_country.csv', index=False)
print(bmi_by_country)

ExpGroup = df.loc[df["PA_Days"] > 0]

ExpGroup["University"] = ExpGroup["University"].replace({"NTU Singapore - National Institute of Education": "NTU Singapore",})

ExpGroup_UNIs = pd.get_dummies(ExpGroup, columns=["University"], prefix="", prefix_sep="")

corr_matrix = ExpGroup_UNIs.corr(numeric_only=True)

# --- Plot 1: Box + Strip ---
plt.figure(figsize=(12, 6))                          
sns.boxplot(data=df, x="Country", y="BMI", palette="Set2")
sns.stripplot(data=df, x="Country", y="BMI", color="black", alpha=0.3, size=3)
plt.title("BMI Distribution by Country")
plt.xlabel("Country")
plt.ylabel("BMI")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
#plt.show()                                           

# --- Plot 2: Correlation Heatmap ---
plt.figure(figsize=(14, 10))                         
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title("Correlation Matrix")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()                                           

