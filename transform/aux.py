import os 

def existingYearDirectories(country):
    route = './data/' + country
    for root, dirs, files in os.walk(route):
        for directory in dirs:
            yield directory 
    