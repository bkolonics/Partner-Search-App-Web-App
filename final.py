"""
This module validates the country acronym.
TODO: Add more here
"""
import sqlite3
import streamlit as st
import pandas as pd
import createdb


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
    conn = sqlite3.connect('ecsel_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Acronym FROM Countries")
    countries = cursor.fetchall()
    countries = [item[0] for item in countries]
    conn.close()
    return countries

def country_anagram_to_full_name(anagram: str) -> str:
    """function maps countries anagram to full name"""
    conn = sqlite3.connect('ecsel_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Country FROM countries WHERE Acronym = ?", (anagram,))
    full_name = cursor.fetchall()
    full_name = [item[0] for item in full_name]
    conn.close()
    return full_name[0]

def generate_dataframe(country: str) -> pd.DataFrame:
    """function generates dataframe"""
    conn = sqlite3.connect('ecsel_database.db')
    query = """SELECT shortName, name, activityType, organizationURL, SUM(ecContribution)
               FROM participants
               WHERE country = ?
               GROUP BY shortName"""
    df_participants = pd.read_sql(query, conn, params=(country,))
    df_participants = df_participants.sort_values(by=['SUM(ecContribution)'], ascending=False)
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
