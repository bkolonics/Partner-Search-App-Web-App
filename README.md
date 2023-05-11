# Partener-search-app-web Project

The project has been carried out on Github, allowing the team members to work in collaboration. 
A streamlit file has been made, allowing us to use automated test after each input.

Github repository: https://github.com/bkolonics/Partner-Search-App-Web-App
Our hosted Streamlit app: https://partner-search.streamlit.app/

This project is composed by three python scripts:

## createdb.py

This module create a SQL database called  « ecsel_database.db », in the same directory that the script.
Three tables are created in this database, with the three excel files in the asset folder.
The excel files are firstly converted to dataframes, and then to SQL tables.
The tables are called projects, participants and countries.
Import two modules:
- sqlite3
- pandas

# final.py

This script contains the main code of the project.
It is a Streamlit app that allows the user to select a country
and displays the participants from that country in a table.
The tables can be downloaded as a CSV files.
Import 5 modules:
- sqlite3
- streamlit
- pandas
- altair

The script, using Streamlit module displays the website.
With an st.selectbox, the user can choose a country.
The program will then verify if the acronym is correct, with the function validate_country_acronym.
Then the program will get the full name of the country with the function country_anagram_to_full_name, by using en SQL request in the Country table.
For the selected country, the program generates and displays  a dataframes for participants, ordered by grants, by using a SQL request, and read_sql from pandas module.
The Program generates and displays:
- a chart for the top 10 participants of the selected country
- a dataframe exposing the main informations of the projects coordinators of the selected country.
- the ten most active countries and their grant in a dataframe, and their grants.
There is a download_button from Sqlite3 allowing to download each dataframes and charts and, covered in csv.

# Test.py
All the tests are happening in the `test.py` file.
In the `test.py` file there are two classes, both of these classes inherit from the `unittest.TestCase` classes. 
The `TestCreateDB` and the `TestFinal` classes defines the tests for the functions inside the `createdb.py` and `final.py` files respectively.

## Testing strategy
Our testing strategy was to test all the functions to ensure that nothing breaks during the development process.
We are satisfied with our results we tested all the functions achieving `86%` of coverage.
Here is our coverage report.
```c
Name          Stmts   Miss  Cover
---------------------------------
createdb.py      12      3    75%
final.py         77     22    71%
test.py          96      1    99%
---------------------------------
TOTAL           185     26    86%
```
We dont have 100% coverage because we did not test every statements in the project.

## Tests approach
Our tests breaks up in three categories
### Simple tests
Our simple tests only gives inputs to the functions and looks to the output of the function like the `test_validate_country_acronym()` function. 
```python
    def test_validate_country_acronym(self):
        self.assertEqual(final.validate_country_acronym('FR'), "FR")
```
We can see that it check thanks to the `assertEqual` function that the function `validate_country_acronym()` outputs `FR` if it was given the input `FR`.

### Excel tests
There is only one test in this category, and it's used to test the `test_content_excel_to_dataframe()` function.
This test uses a mock excel file and converts it to Pandas Dataframe. The mock excel file is located in `test_assets/test_excel.xlsx`. Then we hardcoded the values of the expected Dataframe in the function. At the end we just need to compare the hardcoded Dataframe with the return Dataframe of the `excel_to_dataframe()` function.

### Database interaction tests
The majority of our tests work like this.
In theses tests we use a "fake database" located in `test_assets/fake_database.db` and is created automatically when starting the tests. We declare a global variable on the top of the `test.py` file so we can easily refer to the fake database with the `FAKE_DATABASE` variable.

In these tests we generally use the following decorator
```python
@patch("createdb.DATABASE", FAKE_DATABASE)
```
This decorator helps us so that every time we call a function in a project it will use our fake database and not the production database. 

All the tests follow the same structure, it first puts mock data in the database then  calls the function to execute an action. It the queries the database to check if the data has been correctly processed and compare the output with hardcoded values. At the end the test deletes the tables created in order to execute the tests.






