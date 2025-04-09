import pandas as pd
import streamlit as st
import plotly.express as px

vehicle_df = pd.read_csv("vehicles_us.csv")
vehicle_df.duplicated().sum()

for model in vehicle_df['model'].unique():
    median_value = vehicle_df[vehicle_df['model'] == model]['cylinders'].median()
    
    vehicle_df.loc[vehicle_df['model']==model, 'cylinders'] = vehicle_df.loc[vehicle_df['model']==model, 'cylinders'].fillna(median_value)


vehicle_df.dropna(subset='model_year', inplace=True)
vehicle_df.fillna({'is_4wd': 0}, inplace=True)
vehicle_df.fillna({'paint_color': 'unknown'}, inplace=True)
vehicle_df.fillna(0, inplace=True)
vehicle_df['model'] = vehicle_df['model'].str.strip().str.replace(" ", "_")
vehicle_df['brand'] = vehicle_df['model'].str.split('_').str[0]

vehicle_df1 = vehicle_df.groupby(['model', 'condition']).agg('max').reset_index()
price_by_condition = vehicle_df1[['model', 'condition', 'price']]
price_by_condition = price_by_condition.copy()
max_prices = price_by_condition.groupby('model')['price'].max()
price_by_condition['max_price'] = price_by_condition['model'].map(max_prices)
price_by_condition['price_percentage'] = (((price_by_condition['price'] / price_by_condition['max_price']) * 100) / 100).round(2)
price_by_condition['avg_price_percentage'] = price_by_condition.groupby('condition')['price_percentage'].transform('mean').round(2)


st.header('Data Viewer')
st.dataframe(price_by_condition)

st.header('Average Percentage of Total Price by Condition')
fig = px.histogram(
price_by_condition,
title="Average Percentage of Total Price by Condition",
x="condition",
y="avg_price_percentage",
color="condition",
barmode="stack",
marginal="box",
nbins=6,
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig)

prices = vehicle_df.pivot_table(index='fuel',columns=['condition'],values='price',aggfunc='mean' ).T.fillna(0).reset_index()
fig = px.histogram(prices,x=['diesel', 'electric', 'gas', 'hybrid', 'other'],y='condition', title="Fuel Type Distribution by Condition", color_discrete_sequence=px.colors.qualitative.Set2)
st.write(fig)

fig = px.scatter(prices, y='condition', x=['diesel', 'electric', 'gas', 'hybrid', 'other'], title="Average Price by Fuel Type by Condition", color_discrete_sequence=px.colors.qualitative.Set2)
st.write(fig)

st.header('By Price')
fig = px.scatter(
vehicle_df,
y="price",
x="model_year",
color='condition',
title='Distribution of Price by Model Year and Condition',
color_discrete_sequence=px.colors.qualitative.Set1
)
st.write(fig)

vehicle_df['year_posted'] = vehicle_df['date_posted'].apply(lambda x: x.split('-')[0]).astype('int')
vehicle_df['age'] = vehicle_df['year_posted'] - vehicle_df['model_year']
vehicle_df['max_price'] = vehicle_df['model'].map(max_prices)
vehicle_df['price_percentage'] = (vehicle_df['price'] / vehicle_df['max_price']) * 100
vehicle_df['price_percentage'] = vehicle_df['price_percentage'].round()
vehicle_df[['age', 'model', 'price', 'price_percentage']]
vehicle_df.groupby(['model', 'age', 'price_percentage']).agg('max').head()
condition_count = vehicle_df[['brand','condition']].value_counts().reset_index()
condition_count['condition_count'] = condition_count['count']

st.dataframe(vehicle_df)

brand_list = sorted(vehicle_df['brand'].unique())

brand_1 = st.selectbox(
    label='Select Brand 1',
    options=brand_list
)

brand_2 = st.selectbox(
    label='Select Brand 2',
    options=brand_list,
)

mask_filter = (vehicle_df['brand'] == brand_1) | (vehicle_df['brand'] == brand_2)
vehicle_df_filtered = vehicle_df[mask_filter]

fig_1 = px.histogram(
vehicle_df_filtered,
x='age',
y='price',
color='model',
histfunc='avg',
title='Average Price Per Model by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)

# Checkbox below to adjust x axis for histogram.
age_range = st.checkbox("Toggle Ages 3 to 10 On or Off", value=True)
if age_range:
	fig_1.update_xaxes(range=[3, 10])

st.write(fig_1)

fig1 = None
fig2 = None
fig3 = None
fig4 = None
fig5 = None
fig6 = None
fig7 = None

if st.checkbox('Distribution of Vehicle Type'):
    fig1 = px.bar(
vehicle_df, 
x="brand", 
color="type", 
barmode="stack", 
title="Distribution of Vehicle Type by Brand", 
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig1)

if st.checkbox('Distribution of Vehicle Prices'):
   fig2 = px.box(
vehicle_df,
x="brand",
y="price",
color='brand',
title='Distribution of Vehicle Prices by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig2)

if st.checkbox('Average Price'):
    fig3 = px.histogram(
vehicle_df,
x="brand",
y="price",
color='brand',
histfunc='avg',
title='Average Vehicle Price by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig3)

if st.checkbox('Average Listed Vehicle Age'):
    fig4 = px.histogram(
vehicle_df,
x="brand",
y="age",
color='brand',
histfunc='avg',
title='Average Listed Vehicle Age by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig4)

if st.checkbox('Average Listed Vehicle Odometer'):
    fig5 = px.histogram(
vehicle_df,
x="brand",
y="odometer",
color='brand',
histfunc='avg',
title='Average Listed Vehicle Odometer by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig5)

if st.checkbox('Average Vehicle Condition'):
    fig6 = px.histogram(
condition_count,
x="brand",
y="condition_count",
color='condition',
histfunc='count',
histnorm='percent',
title='Average Vehicle Condition by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig6)

if st.checkbox('Average Age Per Model'):
    fig7 = px.histogram(
vehicle_df,
x="brand",
y='age',
color='model',
histfunc='avg',
title='Average Age Per Model by Brand',
color_discrete_sequence=px.colors.qualitative.Set2
)
st.write(fig7)
