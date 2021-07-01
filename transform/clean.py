import pandas as pd
from .aux import existingYearDirectories

def readMergeClean(country, year):
    route ='./data/'+ country + '/' + str(year)

    try:
        productsRoute = route + '/products.csv'
        partnersRoute = route + '/partners.csv'
        exportValuesRoute = route + '/exportValues.csv'

        productsDf = pd.read_csv(productsRoute, names=['productId', 'product_code', 'product'])
        partnersDf = pd.read_csv(partnersRoute, names=['partnerId', 'partner_code', 'partner'])
        exportValuesDf = pd.read_csv(exportValuesRoute, names=['partnerId', 'productId', 'value'])
    
        complete = exportValuesDf.merge(partnersDf, how='left', on='partnerId')
        complete = complete.merge(productsDf, how='left', on='productId')
        complete['reporter'] = country
        complete['year'] = year
        complete = complete.drop(columns=['partnerId', 'productId'])
        return complete

    except FileNotFoundError:
        print("ERROR! The directory {} doesn't exists".format(route))


def selectRelevantData(data):
    
    products = ['06-15_Vegetable', '50-63_TextCloth', 
    '01-05_Animal','41-43_HidesSkin',  
    '25-26_Minerals', '68-71_StoneGlas', '16-24_FoodProd', '28-38_Chemicals',
    '44-49_Wood', '27-27_Fuels', 'UNCTAD-SoP4', '39-40_PlastiRub', '64-67_Footwear',
    '72-83_Metals', '84-85_MachElec', '86-89_Transport']
    
    regions = ['East Asia and Pacific', 'Europe and Central Asia', 'Middle East and North Africa',
        'World', 'Latin America and Caribbean', 'Sub-Saharan Africa',
       'British Indian Ocean Ter', 'Us Msc.Pac.I', 'North America', 'South Asia']

    mask_products = data['product_code'].isin(products)
    mask_regions = ~data['partner'].isin(regions)

    reduceData = data[mask_products & mask_regions]

    return reduceData


def totalDataPerCountry(country):
    yearDataFrames = []
    for year in existingYearDirectories(country):
        yearDataFrames.append(readMergeClean(country, year))
    
    return pd.concat(yearDataFrames)


def totalData(countries):
    data = []
    for country in countries:
        data.append(totalDataPerCountry(country['name']))

    dataFrame = pd.concat(data)
     
    return selectRelevantData(dataFrame)




