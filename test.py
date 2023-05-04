"""
Python module to test all the function in every module of the project
"""


import unittest
import pandas as pd
import createdb

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

    def test_dataframe_to_sql(self):
        """
        Test the content of the output of the function dataframe_to_sql
        Not yet implemented
        """

if __name__ == '__main__':
    unittest.main()
