from extract import *
from transform import *

import xml.etree.ElementTree as ET


if __name__ == "__main__":

    datasource = dataWits()
    countries = datasource.getCountriesList()
    #for country in countries:
    #    years = datasource.getYearsAvailable(country['isoCode'])
    #    print( country['name'], years)
    #    for year in years:
    #        datasource.exportValues(country,year)
    #    break 
    #datasource.exportValues('AFG', 2008)
    #readAndMerge('AFG', 2008)

    for i in existingDirectories('AFG'):
        readAndMerge('AFG', i)
        print(i, '\n')
    