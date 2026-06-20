import pandas as pd
import matplotlib.pyplot as plt

# load vaccination data
df = pd.read_csv("country_vaccinations.csv")
df['date'] = pd.to_datetime(df['date'])

print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Countries: {df['country'].nunique()}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")

# missing data check
print("\nMissing values:")
print(df.isnull().sum())

# top 10 by raw numbers
latest = df.groupby('country')['people_vaccinated'].max().dropna()
top10 = latest.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top10.plot(kind='barh', color='#0077b6')
plt.title('Top 10 Countries by Total People Vaccinated')
plt.xlabel('People Vaccinated')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_vaccinated.png')

# top 10 by % of population - fairer comparison
latest_pct = df.groupby('country')['people_vaccinated_per_hundred'].max().dropna()
top10_pct = latest_pct.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top10_pct.plot(kind='barh', color='#2ecc71')
plt.title('Top 10 Countries by % of Population Vaccinated')
plt.xlabel('People Vaccinated per 100')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_vaccinated_per_hundred.png')

# which vaccines dominated?
df2 = pd.read_csv("country_vaccinations_by_manufacturer.csv")
top_vaccines = df2.groupby('vaccine')['total_vaccinations'].max().sort_values(ascending=False).head(8)

plt.figure(figsize=(10, 6))
top_vaccines.plot(kind='barh', color='#e74c3c')
plt.title('Most Used COVID-19 Vaccines Worldwide')
plt.xlabel('Total Vaccinations')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_vaccines.png')

# vaccination progress over time
countries = ['United States', 'United Kingdom', 'India', 'Brazil', 'Canada']
plt.figure(figsize=(12, 6))

for country in countries:
    data = df[df['country'] == country].dropna(subset=['people_vaccinated_per_hundred'])
    plt.plot(data['date'], data['people_vaccinated_per_hundred'], label=country)

plt.title('Vaccination Progress Over Time')
plt.xlabel('Date')
plt.ylabel('% of Population Vaccinated')
plt.legend()
plt.tight_layout()
plt.savefig('vaccination_progress.png')

print("\nAll charts saved!")