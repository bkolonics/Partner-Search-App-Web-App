import createdb

def validate_country_acronym(aconym: str) -> str:
    """function valideates country acronym"""
    if len(aconym) != 2:
        raise ValueError("Country acronym must be 2 characters long")

    if aconym not in createdb.excel_to_dataframe('assets/countries.xlsx',
                                        sheet_name='Countries')["Acronym"].values:
        raise ValueError("Country acronym not in list of countries")

    return aconym

if __name__ == '__main__':
    print(validate_country_acronym('FR'))