import os.path
from os import path, makedirs
import csv

def getDataframes(dataList):
    i = 0 
    dataframe = []
    for data in dataList:
        dataframe.append([i, data["id"], data['name']])
        i+=1
    
    return dataframe
    

def saveData(data, name_file):
    
    route = verifyExistence(name_file)
    with open( route, mode='w') as f:
        writer = csv.writer(f, delimiter=",")

        for row in data:
            writer.writerow(row)


def verifyExistence(name_file):
    route ='./data/'+ name_file + '.csv'
    directories = '/'.join(route.split('/')[:-1])

    if not path.exists(directories):
        makedirs(directories)
    
    return route 

         
