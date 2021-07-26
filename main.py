from extract import *
from transform import *



if __name__ == "__main__":
    download = False
    datasource = dataWits()
    if download:
        datasource.downloadData()
    
    countries = datasource.getCountriesList()   
    #print(countries)   
    data = totalData(countries)
    
    #data_filtered = filterTop(data, 2018)
    data_filtered = relevantPartners(data, 2018)
    saveRequestedData(data_filtered)