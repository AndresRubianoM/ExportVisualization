from extract import *
from transform import *

if __name__ == "__main__":
    download = False
    updateFilter = False
    datasource = dataWits()
    if download:
        datasource.downloadData()
    
    
    
    #data_filtered = filterTop(data, 2018)
    if updateFilter:
        countries = datasource.getCountriesList()    
        data = totalData(countries)
        data_filtered = relevantPartners(data, 2018)
        saveRequestedData(data_filtered)

    data_graphHEB = prepareDataHBE()
    saveRequestedData(data_graphHEB, "dataGraph")