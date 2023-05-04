"""
This module validates the country acronym.
TODO: Add more here
"""
import sqlite3
import streamlit as st
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


if __name__ == '__main__':
    st.title("Partner Search App")
    st.write("Antoine Colinet & Bence Kolonics")
    st.selectbox("Choose a country :", map(country_anagram_to_full_name, 
                                           extract_countries_from_db()))
