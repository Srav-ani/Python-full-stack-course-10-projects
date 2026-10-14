import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(r"C:\Users\Satish Vadlapati\OneDrive\Desktop\Zomato Dataset.csv", delimiter=',')
print(data)

#DATA SHAPE
data.shape
print(data.shape)

#DATA INFO
data.info
print(data.info)

# DATA ISNULL FUNCTION

data.isnull()
print(data.isnull())

# DATA ISNULL FUNCTION inculde SUM 
data.isnull().sum()
print(data.isnull().sum())

print(data.columns)
data.drop(data.columns[0],axis=1,inplace=True)
data.info()
print(data.info())

#EDA
data.head()
print(data.head())
data.describe(include='all')
print(data.describe)

#Converting Rate for two from object to integer datatype

def remove_comma(x):
    x = x.replace(",","")
    return x
data['multiple_deliveries'] = pd.to_numeric(data['multiple_deliveries'],errors='coerce').fillna(0).astype(int)
data.City.value_counts()
print(data.columns.tolist())
data.City.value_counts()
print(data.City.value_counts())

data.City.value_counts().plot(kind="pie")
plt.show()
#Delivery Person Count
print(data['Delivery_person_ID'].value_counts())

#City Wise Max Deliverirs Bar Plot
rates=data.groupby('City').agg({'multiple_deliveries':'max'})
rates.plot(kind='bar')
plt.show()

#Group matrix variables logic 
City_mean=data.groupby("City").agg({'Time_taken (min)':'mean'}).reset_index()
print(City_mean)

#plotting average computational graph

plt.figure(figsize=(8,6))
sns.barplot(data=City_mean, x='City', y='Time_taken (min)',palette='magma')
plt.title('Average Time Taken By City Type',fontsize=15,fontweight='bold')
plt.ylabel('Mean Time (min)')
plt.show()

#Converting Overall Rating to Float Datatype

def to_float(x):
    if x=="-":
        x = None
    elif x=="New":
        x = None
    else:
        x = float(x)
    return x
data['Overall_Rating'] = data['Delivery_person_Ratings'].apply(to_float)
print(data['Overall_Rating'].head())

#types = set()
#for row,items in data.iterrows():
    #if pd.notna(items['Type_of_vehicle']):
        #for item  in items['Type_of_vehicle'].split(','):
            #types.add(item.strip())
            #print(types)
#types, len(types)
#print(types, len(types))
types = set()
for row,items in data.iterrows():
    for item in items['Type_of_order'].split(","):
        if item not in types:
            types.add(item)

types, len(types)
print(types, len(types))

#Food Orders Count Plot Check 

plt.figure(figsize=(8,6))
sns.countplot(data=data, x='Type_of_order')
plt.title('Total Orders Count by Food Category',fontsize=15,fontweight='bold')
plt.xlabel('Food Category')
plt.ylabel('Number of Orders')
plt.show()

# 1 Numerical Columns List Select 

numerical_cols = ['Delivery_person_Age','Overall_Rating','multiple_deliveries','Time_taken (min)']
corr_matrix = data[numerical_cols].corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f',linewidths=0.5)
plt.title('Correlation Matrix of Delivery Features',fontsize=15,fontweight='bold')
plt.tight_layout()
plt.show()