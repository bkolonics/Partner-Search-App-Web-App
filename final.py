"""
This module contains the main code of the Partner Search App.
It is a Streamlit app that allows the user to select a country
and displays the participants from that country in a table.
The tables can be downloaded as a CSV files.
"""
import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
import createdb

DATABASE = 'ecsel_database.db'

@st.cache_resource
def validate_country_acronym(aconym: str) -> str:
    """function valideates country acronym"""
    if len(aconym) != 2:
        raise ValueError("Country acronym must be 2 characters long")

    if aconym not in createdb.excel_to_dataframe('assets/countries.xlsx',
                                        sheet_name='Countries')["Acronym"].values:
        raise ValueError("Country acronym not in list of countries")

    return aconym

def extract_countries_from_db() -> list:
    """function extracts countries from db"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT Acronym FROM Countries")
    countries = cursor.fetchall()
    countries = [item[0] for item in countries]
    conn.close()
    return countries

@st.cache_resource
def country_anagram_to_full_name(anagram: str) -> str:
    """function maps countries anagram to full name"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT Country FROM countries WHERE Acronym = ?", (anagram,))
    full_name = cursor.fetchall()
    full_name = [item[0] for item in full_name]
    conn.close()
    return full_name[0]

@st.cache_data
def generate_dataframe(country: str) -> pd.DataFrame:
    """function generates dataframe for participants and orders by grants"""
    conn = sqlite3.connect(DATABASE)
    query = """SELECT shortName, name, activityType, organizationURL, SUM(ecContribution)
               FROM participants
               WHERE country = ?
               GROUP BY shortName"""
    df_participants = pd.read_sql(query, conn, params=(country,))
    df_participants = df_participants.sort_values(by=['SUM(ecContribution)'], ascending=False)
    df_participants = df_participants.rename(columns={'shortName': 'Short Name',
                                                        'name': 'Name',
                                                        'activityType': 'Activity Type',
                                                        'organizationURL': 'Organization URL',
                                                        'SUM(ecContribution)': 'Grants'})
    conn.close()
    return df_participants

def generate_dataframe_project_coordinators(country: str) -> pd.DataFrame:
    """function generates dataframe for project coordinators"""
    conn = sqlite3.connect(DATABASE)
    query = """SELECT shortName, name, activityType, projectAcronym
               FROM participants
               WHERE country = ? AND role = 'coordinator'"""
    df_participants = pd.read_sql(query, conn, params=(country,))
    df_participants = df_participants.sort_values(by=['shortName'], ascending=True)
    df_participants = df_participants.rename(columns={'shortName': 'Short Name',
                                                        'name': 'Name',
                                                        'activityType': 'Activity Type',
                                                        'projectAcronym': 'Project Acronym'})
    conn.close()
    return df_participants

def generate_dataframe_10_most_active_countries() -> pd.DataFrame:
    """function generates dataframe for 10 most active countries"""
    conn = sqlite3.connect(DATABASE)
    query = """SELECT country, SUM(ecContribution)
               FROM participants
               GROUP BY country
               ORDER BY SUM(ecContribution) DESC
               LIMIT 10"""
    df_participants = pd.read_sql(query, conn)
    df_participants = df_participants.rename(columns={'country': 'Country',
                                                        'SUM(ecContribution)': 'Grants'})
    conn.close()
    return df_participants

if __name__ == '__main__':
    st.set_page_config(page_title="Partner Search App", page_icon="assets/logo-ecsel.png")
    st.image("assets/kdtju.png")
    st.title("Partner Search App")
    st.write("Antoine Colinet & Bence Kolonics")
    selected_country = st.selectbox("Choose a country :", extract_countries_from_db(),
                                    format_func=country_anagram_to_full_name)

    st.subheader(f"Participants in {country_anagram_to_full_name(selected_country)}")
    st.dataframe(generate_dataframe(selected_country), use_container_width=True)

    st.subheader(f"Top 10 Participants in {country_anagram_to_full_name(selected_country)}")
    chart = alt.Chart(generate_dataframe(selected_country).head(10)).mark_bar().encode(
        x='Short Name',
        y='Grants',
        color='Activity Type',
        tooltip=['Short Name', 'Grants', 'Activity Type', 'Organization URL']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

    st.download_button(label="Download Participants as CSV",
                          data=generate_dataframe(selected_country).to_csv(),
                            file_name=f"{country_anagram_to_full_name(selected_country)}.csv",
                            mime="text/csv")

    st.divider()

    st.subheader(f"Project Coordinators in {country_anagram_to_full_name(selected_country)}")
    st.dataframe(generate_dataframe_project_coordinators(selected_country),
                 use_container_width=True)
    st.download_button(label="Download Project Coordinators as CSV",
                            data=generate_dataframe_project_coordinators(selected_country).to_csv(),
                            file_name=f"{country_anagram_to_full_name(selected_country)}_coordinators.csv", # pylint: disable=line-too-long
                            mime="text/csv")

    st.divider()

    st.subheader("Top 10 Countries")
    st.dataframe(generate_dataframe_10_most_active_countries(), use_container_width=True)
    chart = alt.Chart(generate_dataframe_10_most_active_countries()).mark_bar().encode(
        x='Country',
        y='Grants',
        tooltip=['Country', 'Grants']
    ).interactive()

    st.subheader("Top 10 Countries Graph")
    st.altair_chart(chart, use_container_width=True)

    st.download_button(label="Download Top 10 Countries as CSV",
                            data=generate_dataframe_10_most_active_countries().to_csv(),
                            file_name="top_10_countries.csv",
                            mime="text/csv")
