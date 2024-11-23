##WebAppCode


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

#############
# Page Title
############

# Correct path to the fil
image = Image.open('images/DEALERLIST.png')

st.image(image, use_column_width= True)


st.markdown("""
#Our Car Dealership 
         a simple sda project on a car dealership
         
         
         """)

##################

df = pd.read_csv('/Users/macos/Downloads/vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Data viewer')
show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

st.dataframe(df)
st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='manufacturer', color='type'))
st.header('Histogram of `condition` vs `model_year`')

# -------------------------------------------------------
# histograms in plotly:
# fig = go.Figure()
# fig.add_trace(go.Histogram(x=df[df['condition']=='good']['model_year'], name='good'))
# fig.add_trace(go.Histogram(x=df[df['condition']=='excellent']['model_year'], name='excellent'))
# fig.update_layout(barmode='stack')
# st.write(fig)
# works, but too many lines of code
# -------------------------------------------------------

# histograms in plotly_express:
st.write(px.histogram(df, x='model_year', color='condition'))
# a lot more concise!
# -------------------------------------------------------

st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))

########
#New Web App Function 
########
data_comp = {
    'model_year': df['model_year'],
    'odometer' : df['odometer']


}

df_comp = pd.DataFrame(data_comp)

# Streamlit App
st.header("Compare Vehicle Year to Mileage")

# Dropdown for selecting vehicle year with default option "Show All"
veh_list = ["Show All"] + sorted(df_comp['model_year'].unique())
selected_year = st.selectbox("Select vehicle year", veh_list)

# Filter the data based on the selected year
if selected_year == "Show All":
    filtered_df_comp = df_comp
else:
    filtered_df_comp = df_comp[df_comp['model_year'] == selected_year]

# Display filtered data
st.subheader(f"Vehicles for Year: {selected_year if selected_year != 'Show All' else 'All Years'}")
st.write(filtered_df_comp)

# Interactive Scatterplot
st.subheader("Interactive Scatterplot")
fig = px.scatter(
    filtered_df_comp,
    x="model_year",
    y="odometer",
    title="Vehicle Year vs Mileage",
    labels={"model_year": "Vehicle Year", "odometer": "Mileage (Odometer Reading)"},
    color="model_year" if selected_year == "Show All" else None,
    hover_data=["odometer"]
)
fig.update_traces(marker=dict(size=10, opacity=0.7))
st.plotly_chart(fig)

# Mileage Categories with Counts
st.subheader("Mileage Categories")
categories = {
    "Under 10k": filtered_df_comp[filtered_df_comp["odometer"] <= 10000],
    "Under 35k": filtered_df_comp[(filtered_df_comp["odometer"] > 10000) & (filtered_df_comp["odometer"] <= 35000)],
    "Under 50k": filtered_df_comp[(filtered_df_comp["odometer"] > 35000) & (filtered_df_comp["odometer"] <= 50000)],
    "Under 75k": filtered_df_comp[(filtered_df_comp["odometer"] > 50000) & (filtered_df_comp["odometer"] <= 75000)],
    "Under 100k": filtered_df_comp[(filtered_df_comp["odometer"] > 75000) & (filtered_df_comp["odometer"] <= 100000)],
    "Above 100k": filtered_df_comp[filtered_df_comp["odometer"] > 100000],
}

for category, data in categories.items():
    st.write(f"There are **{len(data)} vehicles** with mileage {category.lower()}.")



###New Web Function###




# Streamlit App
st.title("Vehicle Database Analysis")

# Dropdown for selecting vehicle type
vehicle_types_ = df['type'].unique()
selected_type_ = st.selectbox("Select Vehicle Type", vehicle_types_, index=0)

# Filter the DataFrame based on the selected type
filtered_df_no = df[df['type'] == selected_type_]

# Display filtered data
st.subheader(f"Vehicles of type '{selected_type_}'")
st.write(filtered_df_no)

# Create a bar chart to display the count of vehicles for each model year
st.subheader("Vehicle Count by Model Year")
if not filtered_df_no.empty:
    vehicle_count = filtered_df_no['model_year'].value_counts().reset_index()
    vehicle_count.columns = ['model_year', 'count']

    # Plot using Plotly
    fig = px.bar(
        vehicle_count,
        x='model_year',
        y='count',
        title=f"Number of {selected_type_}s by Model Year",
        labels={'model_year': 'Model Year', 'count': 'Number of Vehicles'},
    )
    st.plotly_chart(fig)
else:
    st.write(f"No vehicles of type '{selected_type_}' found in the database.")
