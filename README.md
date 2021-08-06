# ExportVisualization
A brief ETL that gets the data of  'http://wits.worldbank.org/API/V1/' API. The recopiled data are all the possible values of exportations in each available country in every available year. All the process related with the extraction, cleaning and transformation of the data is handle it in python using native tools and Pandas. 

The first visualization is a Hierarchical Edge Bundling of the year 2018 that shows all the relations between the countries, since the amount of data is enormous at least for this type of graph I decided to reduce irrelevant data, reducing the number of trades between countries just leaving the number of countries that represents the 90% of the total exportations of each country. 

![heb](https://github.com/AndresRubianoM/exportVisualization/blob/master/images/HEB1.png)

Each group of countries are determined by the official regions provided in 'https://unstats.un.org/unsd/methodology/m49/overview/'.
Is important to take into account that the relations presented in the graph are the relevant trades based on exportations data of each country and not an all the available data, neither data related to importations. 

the visualization was programed to show per country the importations and exportations marking the paths with red and blue respectively.

To run the present code only is necesary to change the bool values to True in the file **main.py**, this way the code will start to do all the requests to tha API and organize, clean and transform all the data (The data related to the countries must by download previously because it comes from another source).

