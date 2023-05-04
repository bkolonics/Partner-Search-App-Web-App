import unittest
import createdb
import pandas as pd

class TestCreateDB(unittest.TestCase):

    # test excel_to_dataframe
    def test_type_excel_to_dataframe(self):
        self.assertEqual(type(createdb.excel_to_dataframe('assets/projects.xlsx',
                        sheet_name='Sheet1')), type(pd.DataFrame()))
        self.assertEqual(type(createdb.excel_to_dataframe('assets/participants.xlsx',
                        sheet_name='Sheet1')), type(pd.DataFrame()))
        self.assertEqual(type(createdb.excel_to_dataframe('assets/countries.xlsx',
                        sheet_name='Countries')), type(pd.DataFrame()))
        
    def test_content_excel_to_dataframe(self):
        test_df = pd.DataFrame({'A': ['D'], 'B': ['E'], 'C': ['F']})
        excel_to_dataframe = createdb.excel_to_dataframe('test_assets/test_excel.xlsx',
                        sheet_name='Feuil1')
        self.assertTrue(excel_to_dataframe.equals(test_df))

    def test_dataframe_to_sql(self):
        pass
    
if __name__ == '__main__':
    unittest.main()