"""
Python module to test all the function in every module of the project
"""


import unittest
# from unittest import mock
from unittest.mock import patch
import sqlite3 as sq
import pandas as pd
import createdb
import final

FAKE_DATABASE = 'test_assets/fake_database.db'

class TestCreateDB(unittest.TestCase):
    """
    Class to test the function in the createdb module
    """

    def test_type_excel_to_dataframe(self):
        """
        Test the type of the output of the function excel_to_dataframe
        """
        self.assertEqual(type(createdb.excel_to_dataframe('assets/projects.xlsx',
                        sheet_name='Sheet1')), type(pd.DataFrame()))
        self.assertEqual(type(createdb.excel_to_dataframe('assets/participants.xlsx',
                        sheet_name='Sheet1')), type(pd.DataFrame()))
        self.assertEqual(type(createdb.excel_to_dataframe('assets/countries.xlsx',
                        sheet_name='Countries')), type(pd.DataFrame()))

    def test_content_excel_to_dataframe(self):
        """
        Test the content of the output of the function excel_to_dataframe
        """
        test_df = pd.DataFrame({'A': ['D'], 'B': ['E'], 'C': ['F']})
        excel_to_dataframe = createdb.excel_to_dataframe('test_assets/test_excel.xlsx',
                        sheet_name='Feuil1')
        self.assertTrue(excel_to_dataframe.equals(test_df))

    @patch("createdb.DATABASE", FAKE_DATABASE)
    def test_dataframe_to_sql(self):
        """
        Test the content of the output of the function dataframe_to_sql
        """
        test_df = pd.DataFrame({'A': ['D'], 'B': ['E'], 'C': ['F']})
        dataframe_to_sql = createdb.dataframe_to_sql(test_df, 'test_table') # pylint: disable=W0612
        conn = sq.connect(FAKE_DATABASE)
        sql_to_dataframe = pd.read_sql_query("SELECT * FROM test_table", conn)
        sql_to_dataframe = sql_to_dataframe.drop(columns=['index'])
        self.assertTrue(test_df.equals(sql_to_dataframe))
        conn.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()


class TestFinal(unittest.TestCase):
    """
    Class to test the function in the final module
    """

    def test_validate_country_acronym(self):
        """
        Test the content of the output of the function validate_country_acronym
        """
        self.assertEqual(final.validate_country_acronym('FR'), "FR")
        self.assertRaises(ValueError, final.validate_country_acronym, 'fra')
        self.assertRaises(ValueError, final.validate_country_acronym, 'FRANCE')
        self.assertRaises(ValueError, final.validate_country_acronym, 'F')
        self.assertRaises(ValueError, final.validate_country_acronym, 'XY')

    @patch("final.DATABASE", FAKE_DATABASE)
    def test_extract_countries_from_db(self):
        """
        Test the content of the output of the function extract_countries_from_db
        """
        test_list = ['FR', 'DE', 'IT']
        conn = sq.connect(FAKE_DATABASE)
        test_df = pd.DataFrame({'Acronym': test_list})
        test_df.to_sql('countries', conn, if_exists='replace', index=False)
        extract_countries_from_db = final.extract_countries_from_db()
        self.assertEqual(extract_countries_from_db, test_list)
        conn.execute("DROP TABLE countries")
        conn.commit()
        conn.close()

    @patch("final.DATABASE", FAKE_DATABASE)
    def test_country_anagram_to_full_name(self):
        """
        Test the content of the output of the function country_anagram_to_full_name
        """
        test_list = ['FR', 'DE', 'IT']
        conn = sq.connect(FAKE_DATABASE)
        test_df = pd.DataFrame({'Acronym': test_list, 'Country': ['France', 'Germany', 'Italy']})
        test_df.to_sql('countries', conn, if_exists='replace', index=False)
        self.assertEqual(final.country_anagram_to_full_name('FR'), "France")
        self.assertEqual(final.country_anagram_to_full_name('DE'), "Germany")
        self.assertEqual(final.country_anagram_to_full_name('IT'), "Italy")
        conn.execute("DROP TABLE countries")
        conn.commit()
        conn.close()


    @patch("final.DATABASE", FAKE_DATABASE)
    def test_generate_dataframe(self):
        """
        Test the content of the output of the function generate_dataframe
        """
        conn = sq.connect(FAKE_DATABASE)
        input_df = pd.DataFrame({'shortName': ['A'],
                                'Name': ['D'],
                                'activityType': ['G'],
                                'organizationURL': ['J'],
                                'country': ['FR'],
                                'ecContribution': [1]})
        expected_df = pd.DataFrame({'Short Name': ['A'],
                                    'Name': ['D'],
                                    'Activity Type': ['G'],
                                    'Organization URL': ['J'],
                                    'Grants': [1]})

        input_df.to_sql('participants', conn, if_exists='replace', index=False)
        generate_dataframe = final.generate_dataframe('FR')
        print(generate_dataframe)
        print(input_df)
        self.assertTrue(generate_dataframe.equals(expected_df))
        conn.execute("DROP TABLE participants")
        conn.commit()
        conn.close()


if __name__ == '__main__':
    unittest.main()
