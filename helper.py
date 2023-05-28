import pandas as pd
import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby(['region']).sum()[['Bronze', 'Gold', 'Silver']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Bronze'] + medal_tally['Gold'] + medal_tally['Silver']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country

def sports_list(df):
    sport = np.unique(df['Sport'].dropna().values).tolist()
    sport.sort()
    sport.insert(0, "Overall")
    return sport

def country_list(df):
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    return country

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == year]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]
    if flag == 1:
        x = temp_df.groupby(['Year']).sum()[['Bronze','Gold','Silver']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby(['NOC']).sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Bronze'] + x['Gold'] + x['Silver']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values("Year",axis=0)
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != "Overall":
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(10)
    x = x.merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'Name':"Name",'count':"Medals",'Sport':"Sport",'region':"Nation"},inplace = True)
    return x

def country_year_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp = temp_df[temp_df['region'] == country]
    x = temp.groupby('Year').count()['Medal'].reset_index()
    return x


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def country_wise_most_successful(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10)
    x = x.merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'Name':"Name",'count':"Medals",'Sport':"Sport",'region':"Nation"},inplace = True)
    return x