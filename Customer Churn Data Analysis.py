# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 15:13:53 2026

@author: admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Wrangling & Integration

# Upload the dataset

Cust_Data = pd.read_csv(r'D:\01. Portfolio projects\Python Practice\Project 7 (Customer Churn)/telecom_customer_churn.csv')
 
Population_Data = pd.read_csv(r'D:\01. Portfolio projects\Python Practice\Project 7 (Customer Churn)/telecom_zipcode_population.csv')

# Merge both dataset

Merged_Data = pd.merge(Cust_Data, Population_Data, how='left', on= 'Zip Code')

# Understand the data

print(Merged_Data.info())

print(Merged_Data.head())

print(Merged_Data.describe())

print(Merged_Data.isnull().sum())

print(Merged_Data.duplicated().sum())

# Handling Missing Values

Merged_Data['Offer'].fillna('None', inplace=True)

Merged_Data['Avg Monthly Long Distance Charges'].fillna(0, inplace=True)

Merged_Data['Avg Monthly GB Download'].fillna(0, inplace=True)

Merged_Data['Multiple Lines'].fillna('No', inplace=True)

Intnet_Col = ['Internet Type', 'Online Security','Online Backup', 'Device Protection Plan','Premium Tech Support','Streaming TV', 'Streaming Movies','Streaming Music', 'Unlimited Data'  ]

for Col in Intnet_Col:
    Merged_Data[Col].fillna('No', inplace=True)
    
Merged_Data['Churn Category'].fillna('Not Applicable', inplace=True)
Merged_Data['Churn Reason'].fillna('Not Applicable', inplace=True)

print("Missing Values after cleaning:")
print(Merged_Data.isnull().sum())

# 2.EDA

# Target Variable Analysis

tva = Merged_Data.groupby('Customer Status')['Customer ID'].count().reset_index()
tva=tva.rename(columns={'Customer ID': 'No_of_customers'})

tva['Percentage'] = tva['No_of_customers'] / (tva['No_of_customers'].sum()) * 100

print(tva)

# Target Variable Analysis - Visual

fig, ax1 = plt.subplots(figsize=(16,10))

sns.barplot(data=tva, x='Customer Status', y='No_of_customers', ax=ax1, color = 'cyan')
ax1.set_ylabel('No of Customers')
ax1.set_title('Customer Status Distribution')

ax2=ax1.twinx()
sns.lineplot(data=tva, x='Customer Status', y='Percentage', ax=ax2, color='red')
ax2.set_ylabel('percentage')
ax2.set_ylim(0,100)

for index, row in tva.iterrows():
    ax1.text(index, row['No_of_customers'], f"{row['No_of_customers']}", ha = 'center', va='bottom', fontsize=12)
    ax2.text(index, row['Percentage']-5, f"{row['Percentage']:.1f}%", ha='center', va='bottom', fontsize=12)

plt.show()

# Demographic Analysis

Merged_Data['Age_Group'] = pd.cut(Merged_Data['Age'], bins=[0,30,60,100], labels=['Young(0-30)', 'Adult[31-60]', 'Senior[60+]'])

Age_Churn_rate = Merged_Data.groupby(['Age_Group','Customer Status']).size().unstack()

Age_Churn_rate['Churn_rate'] = (Age_Churn_rate['Churned'] / (Age_Churn_rate['Churned'] + Age_Churn_rate['Joined'] +Age_Churn_rate['Stayed'])) * 100

Age_Churn_rate_wide = Age_Churn_rate.reset_index()

Age_Churn_rate_long = Age_Churn_rate_wide.melt(id_vars = 'Age_Group',
                                               value_vars = ['Churned', 'Joined', 'Stayed'],
                                               var_name = 'Customer Status',
                                               value_name = 'Count')
fig, ax1 = plt.subplots(figsize=(16,10))

sns.barplot(data = Age_Churn_rate_long, x= 'Age_Group', y='Count', hue ='Customer Status', ax=ax1)
ax1.set_ylabel('No of Customers')
ax1.set_title('Customer Status by Age group with churn rate')

ax2= ax1.twinx()
sns.lineplot(data = Age_Churn_rate_wide , x= 'Age_Group', y ='Churn_rate', color = 'Pink', ax=ax2)
ax2.set_ylabel("Churn rate(%)")
ax2.set_ylim(0,100)

 
for index, row in Age_Churn_rate_wide.iterrows():
    ax2.text(index, row['Churn_rate']+5, f"{row['Churn_rate']:.1f}%", ha='center', va = 'top')

plt.show() 

# Service Analysis

svc_analysis = Merged_Data.groupby(['Internet Type', 'Customer Status']).size().unstack()
svc_analysis['Churn_rate'] = (svc_analysis['Churned'] / (svc_analysis['Churned'] + svc_analysis['Joined'] + svc_analysis['Stayed'])) * 100

Contract_analysis = Merged_Data.groupby(['Contract', 'Customer Status']).size().unstack()

Contract_analysis['Churn_rate'] = (Contract_analysis['Churned'] / (Contract_analysis['Churned'] + Contract_analysis['Joined'] + Contract_analysis['Stayed'])) * 100



# Financial Analysis
plt.figure(figsize=(16,10))
sns.histplot(Merged_Data, x='Monthly Charge', bins=25, hue='Customer Status', multiple='stack')
plt.xlabel('Monthly Charges ($)')
plt.ylabel('No of Customers')
plt.title('Distribution of monthly charges')
plt.show()

#Findling Mean

print(Merged_Data.groupby('Customer Status')['Monthly Charge'].mean())

# Churn Reason Analysis

Churn_df = Merged_Data[Merged_Data['Customer Status'] == 'Churned']

Chrun_category = Churn_df.groupby('Churn Category')['Customer ID'].count().sort_values(ascending = False).reset_index()
Chrun_category.columns = ['Churn Category', 'Count']
plt.figure(figsize=(16,10))
sns.barplot(data=Chrun_category, x = 'Count', y = 'Churn Category')
plt.tight_layout()
plt.show()


Chrun_analysis_1 = Churn_df.groupby('Churn Reason')['Customer ID'].count().sort_values(ascending = False).reset_index()
Chrun_analysis_1.columns = ['Churn Reason', 'Count']
Chrun_analysis_1['Percentage'] = (Chrun_analysis_1['Count'] / len(Churn_df)) * 100

plt.figure(figsize=(16,10))
sns.barplot(data=Chrun_analysis_1.head(10), x = 'Count', y = 'Churn Reason')
plt.tight_layout()
plt.show()







