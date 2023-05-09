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

if __name__ == '__main__':
    unittest.main()
