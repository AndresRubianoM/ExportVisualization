import pandas as pd

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
        print(complete.head())
        return complete

    except FileNotFoundError:
        print("ERROR! The directory {} doesn't exists".format(route))


def totalDataPerCountry(country):
    yearDataFrames = []
    for year in existingYearDirectories(country):
        yearDataFrames.append(readAndMerge(country, year))
        print(i, '\n')

