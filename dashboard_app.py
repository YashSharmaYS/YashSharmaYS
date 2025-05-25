
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/sales_data.csv')
df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])
df['High_Discount'] = df['Discount'] > 0.25
df['Month'] = df['Sale_Date'].dt.to_period('M').astype(str)

st.set_page_config(page_title='Discount Abuse Dashboard', layout='wide')

st.title('🧾 Discount Abuse Detection Dashboard')

# Sidebar filters
rep_filter = st.sidebar.multiselect("Select Sales Reps", df['Sales_Rep'].unique(), default=df['Sales_Rep'].unique())
region_filter = st.sidebar.multiselect("Select Regions", df['Region'].unique(), default=df['Region'].unique())

# Filter data
filtered_df = df[df['Sales_Rep'].isin(rep_filter) & df['Region'].isin(region_filter)]

st.subheader('1. Average Discount by Customer Type')
avg_discount = filtered_df.groupby('Customer_Type')['Discount'].mean().reset_index()
st.dataframe(avg_discount)

fig1, ax1 = plt.subplots()
sns.barplot(data=avg_discount, x='Customer_Type', y='Discount', ax=ax1)
st.pyplot(fig1)

st.subheader('2. Monthly High Discount Transactions (>25%)')
monthly_high = filtered_df[filtered_df['High_Discount']].groupby('Month').size().reset_index(name='Count')
fig2, ax2 = plt.subplots()
sns.lineplot(data=monthly_high, x='Month', y='Count', marker='o', ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

st.subheader('3. Discount Distribution by Product Category')
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x='Product_Category', y='Discount', ax=ax3)
plt.xticks(rotation=15)
st.pyplot(fig3)

st.markdown('---')
st.markdown('Built with ❤️ using Streamlit')
