#Parse xml
import xml.etree.ElementTree as ET
import json
#Built functions
from .calls import call
from .aux import getDataframes, saveData


class dataWits:

    URL = 'http://wits.worldbank.org/API/V1/'

    def getCountriesList(self):
        countriesListUrl = self.URL + "wits/datasource/tradestats-trade/country/ALL"
        response = call(countriesListUrl, "List of countries").content
        
        countriesList = []
        xmlTree = ET.fromstring(response)
        for country in xmlTree[0]:
            countriesList.append(
            {
                'isoCode': country[0].text,
                'name': country[1].text
            }
            )
            
        return countriesList
    
    def getYearsAvailable(self, country):
        avaibilityUrl = self.URL + 'wits/datasource/tradestats-trade/dataavailability/country/{}/indicator/all'.format(country)
        response = call(avaibilityUrl, "Available years for {}".format(country)).content

        yearsList = []
        xmlTree = ET.fromstring(response)
        for reporter in xmlTree[0]:
            yearsList.append(reporter[1].text)

        return yearsList
    
    def exportValues(self, country, year):
        exportsUrl = self.URL + 'SDMX/V21/datasource/tradestats-trade/reporter/{}/year/{}/partner/all/product/all/indicator/XPRT-TRD-VL?format=JSON'.format(country['isoCode'], year)
        response = call(exportsUrl, "Export values for {} in the year {}".format(country['name'], year)).content
        data = json.loads(response)

        values = data["dataSets"][0]["series"]
        partners = (data["structure"]["dimensions"]["series"][2]["values"])
        products = (data["structure"]["dimensions"]["series"][3]["values"])
        #Format the data into lists
        productsData = getDataframes(products)
        partnersData = getDataframes(partners)
        
        dataValues = []
        for key in values:
            value = values[key]['observations']['0'][0]
            vect = key.split(":")[2:4]
            dataValues.append([vect[0], vect[1], value])
        
        saveData(productsData, '{}/{}/products'.format(country['name'],year))
        saveData(partnersData, '{}/{}/partners'.format(country['name'],year))
        saveData(dataValues, '{}/{}/exportValues'.format(country['name'],year))

        
        
        

    

        


