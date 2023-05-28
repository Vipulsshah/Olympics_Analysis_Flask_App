import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import preprocessor, helper

df = pd.read_csv('F:/Data Science/Data Sets/All About Olympics/Olympics_Analysis_Web_App/athlete_events.csv')
region_df = pd.read_csv('F:/Data Science/Data Sets/All About Olympics/Olympics_Analysis_Web_App/noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title("Overall Tally for " + str(selected_country))
    if selected_year != "Overall" and selected_country != "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympics for " + str(selected_country) )
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Athletes")
        st.title(athletes)
    with col6:
        st.header("Nations")
        st.title(nations)

    st.title("Participating Nations Over the Years")
    nations_over_time = helper.data_over_time(df,"region")
    fig = px.line(nations_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    st.title("Events Over the Years")
    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    st.title("Athletes Over the Years")
    athletes_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athletes_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    st.title("Sports Over the Years")
    sports_over_time = helper.data_over_time(df, "Sport")
    fig = px.line(sports_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    sport = helper.sports_list(df)
    st.title("Top 10 Most Successful Athletes")
    selected_sport = st.selectbox("Select Sport", sport)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == "Country-wise Analysis":
    countries = helper.country_list(df)
    st.sidebar.title("Country-wise Analysis")
    selected_country = st.sidebar.selectbox("Select Country", countries)
    tally = helper.country_year_tally(df,selected_country)
    st.title(str(selected_country) + " Performance Over the Years")
    fig = px.line(tally, x="Year", y="Medal")
    st.plotly_chart(fig)

    st.title(str(selected_country) + " Performance In Different Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    countries = helper.country_list(df)
    st.title("Country-wise Sex Ratio Analysis")
    temp_df = df[df['region'] == selected_country]
    temp_df['Sex'] = temp_df['Sex'].dropna()
    temp = temp_df.groupby(by=["Sex"]).size().reset_index(name="counts")
    fig = px.bar(data_frame=temp, x="Sex", y="counts", color="Sex")
    st.plotly_chart(fig)

    st.title("Top 10 Athletes from " + str(selected_country))
    temp = helper.country_wise_most_successful(df,selected_country)
    st.table(temp)

if user_menu == "Athlete-wise Analysis":
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == "Gold"]['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == "Silver"]['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == "Bronze"]['Age'].dropna()
    st.title("Athletes Age Distribution Graph")
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    st.title("Athletes Height vs weight Analysis")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna("No Medal", inplace=True)
    Sport = helper.sports_list(df)
    Sport.pop(0)
    selected_sport = st.selectbox("Select Sport", Sport)
    plt.figure(figsize=(15, 10))
    temp_df = athlete_df[athlete_df['Sport'] == selected_sport]
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=50)
    st.pyplot(fig)

    st.title("Male vs Female Participation over the years")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    male = athlete_df[athlete_df['Sex'] == "M"].groupby("Year").count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == "F"].groupby("Year").count()['Name'].reset_index()
    final_df = male.merge(female, on="Year", how="left")
    final_df.rename(columns={'Name_x': "Male", 'Name_y': "Female"}, inplace=True)
    final_df.fillna(0, inplace=True)
    fig = px.line(final_df, x="Year", y=['Male', 'Female'])
    st.plotly_chart(fig)