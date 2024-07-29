import plotly.express as px
import pandas as pd
import os
import streamlit as st
from plotly.subplots import make_subplots  # for creating subplots in plotly
import plotly.graph_objects as go




world_data = pd.read_csv("worldometer_data.csv")
group_data = pd.read_csv("country_wise_latest.csv")
day_wise = pd.read_csv("day_wise.csv")

# Streamlit title
st.title("Corona Analysis")

# Example data
columns = ['TotalCases', 'TotalDeaths', 'TotalRecovered', 'ActiveCases']
pop_test_ratio = world_data.iloc[0:20]['Population'] / world_data.iloc[0:20]['TotalTests']

# Create figures
figs = []
for i in columns:
    figs.append(px.treemap(world_data[0:20], values=i, path=['Country/Region'], template="plotly_dark",
                           title=f"<b>TreeMap representation of different Countries w.r.t. their {i}</b>"))

fig1 = px.line(day_wise, x="Date", y=["Confirmed", "Deaths", "Recovered", "Active"], title="COVID-19 Cases w.r.t. Date",
               template="plotly_dark")
fig2 = px.bar(world_data.iloc[0:20], color='Country/Region', y=pop_test_ratio, x='Country/Region',
              template="plotly_dark", title="<b>Population to Tests Done Ratio</b>")
fig3 = px.bar(world_data.iloc[0:20], x='Country/Region',
              y=['Serious,Critical', 'TotalDeaths', 'TotalRecovered', 'ActiveCases', 'TotalCases'],
              template="plotly_dark")
fig3.update_layout(title="Coronavirus Cases w.r.t. Time")
fig4 = px.bar(world_data.iloc[0:20], y='Country/Region', x='TotalCases', color='TotalCases', text="TotalCases")
fig4.update_layout(template="plotly_dark", title="<b>Top 20 Countries by Total Confirmed Cases</b>")
fig5 = px.bar(world_data.sort_values(by='TotalDeaths', ascending=False)[0:20], y='Country/Region', x='TotalDeaths',
              color='TotalDeaths', text="TotalDeaths")
fig5.update_layout(template="plotly_dark", title="<b>Top 20 Countries by Total Deaths</b>")
fig6 = px.bar(world_data.sort_values(by='ActiveCases', ascending=False)[0:20], y='Country/Region', x='ActiveCases',
              color='ActiveCases', text='ActiveCases')
fig6.update_layout(template="plotly_dark", title="<b>Top 20 Countries by Active Cases</b>")
fig7 = px.bar(world_data.sort_values(by='TotalRecovered', ascending=False)[:20], y='Country/Region', x='TotalRecovered',
              color='TotalRecovered', text='TotalRecovered')
fig7.update_layout(template="plotly_dark", title="<b>Top 20 Countries by Total Recovered</b>")
labels = world_data[0:15]['Country/Region'].values
fig8 = []
for i in columns:
    fig8.append(px.pie(world_data[0:15], values=i, names=labels, template="plotly_dark", hole=0.3,
                       title=f"{i} Recorded w.r.t. WHO Region of 15 Worst Affected Countries"))

deaths_to_confirmed = (world_data['TotalDeaths'] / world_data['TotalCases'])
fig9 = px.bar(world_data, x='Country/Region', y=deaths_to_confirmed)
fig9.update_layout(title="Death to Confirmed Ratio of Worst Affected Countries", template="plotly_dark")

deaths_to_recovered = (world_data['TotalDeaths'] / world_data['TotalRecovered'])
fig10 = px.bar(world_data, x='Country/Region', y=deaths_to_recovered)
fig10.update_layout(title="Death to Recovered Ratio of Worst Affected Countries", template="plotly_dark")

tests_to_confirmed = (world_data['TotalTests'] / world_data['TotalCases'])
fig11 = px.bar(world_data, x='Country/Region', y=tests_to_confirmed)
fig11.update_layout(title="Tests to Confirmed Ratio of Worst Affected Countries", template="plotly_dark")

serious_to_death = (world_data['Serious,Critical'] / world_data['TotalDeaths'])
fig12 = px.bar(world_data, x='Country/Region', y=serious_to_death)
fig12.update_layout(title="Serious to Death Ratio of Worst Affected Countries", template="plotly_dark")


# Function to create country visualization
def country_visualization(group_data, country):
    data = group_data[group_data['Country/Region'] == country]
    df = data.loc[:, ['Date', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    fig = make_subplots(rows=1, cols=4, subplot_titles=("Confirmed", "Active", "Recovered", 'Deaths'))

    fig.add_trace(go.Scatter(name="Confirmed", x=df['Date'], y=df['Confirmed']), row=1, col=1)
    fig.add_trace(go.Scatter(name="Active", x=df['Date'], y=df['Active']), row=1, col=2)
    fig.add_trace(go.Scatter(name="Recovered", x=df['Date'], y=df['Recovered']), row=1, col=3)
    fig.add_trace(go.Scatter(name="Deaths", x=df['Date'], y=df['Deaths']), row=1, col=4)

    fig.update_layout(height=600, width=1000, title=f"Date Vs Recorded Cases of {country}", template="plotly_dark")
    return fig


# Streamlit Sidebar
st.sidebar.title("Covid-19 Analysis")
chart_type = st.sidebar.radio("Select Chart Type:",
                              ['Tree map', 'Data', 'Bar Chart', 'Pie Chart', 'Line Chart', 'Country Visualization'])

# Display charts based on user selection
if chart_type == 'Tree map':
    selected_column = st.sidebar.selectbox("Select Column:", columns)
    fig_index = columns.index(selected_column)
    st.plotly_chart(figs[fig_index], use_container_width=True)

elif chart_type == 'Line Chart':
    st.plotly_chart(fig1, use_container_width=True)

elif chart_type == 'Bar Chart':
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.plotly_chart(fig7, use_container_width=True)

elif chart_type == 'Pie Chart':
    for i in range(len(columns)):
        st.plotly_chart(fig8[i], use_container_width=True)

elif chart_type == 'Data':
    st.dataframe(world_data)

elif chart_type == 'Country Visualization':
    country = st.sidebar.selectbox("Select Country:", group_data['Country/Region'].unique())
    fig = country_visualization(group_data, country)
    st.plotly_chart(fig, use_container_width=True)
