# ExportVisualization
A brief ETL that gets the data of  'http://wits.worldbank.org/API/V1/' API. The recopiled data are all the possible values of exportations in each available country in every available year. All the process related with the extraction, cleaning and transformation of the data is handle it in python using native tools and Pandas. 

The first visualization is a Hierarchical Edge Bundling of the year 2018 that shows all the relations between the countries, since the amount of data is enormous at least for this type of graph I decided to reduce irrelevant data, reducing the number of trades between countries just leaving the number of countries that represents the 90% of the total exportations of each country.  
