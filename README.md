Master: Master in statistics for Data Science 
Course: Data Tidying and Reporting
Year: 2020
Name: David Enrique Merchán Cano
Url: https://github.com/davidmerchan04/mydashpython.git

# Public transport of Alcobendas - Dash Python App

This app contains information about transport of Alcobendas, this information was collect by Ayuntamiento de Alcobendas. In this app we will different statistical plots that let you to infer how was the behavior of the public transport in Alcobendas between 2015 and 2017. 


## Data description 

The data contains 84 variables about 28 bus lines for 3 years in Alcobendas. The variables that are described in this dataset are:

* Line: Is the number of the linebus

* Year: Corresponds to the year in which it was collected

* Tipo de transporte: Refers to the type of the line, it can be urban bus and interurban bus

* Número anual de pasajeros: Refers to the annual number of passengers in a certain line

* Expediciones por día: Refers to the number of times that the bus was in services

* Viajeros por día:Refers to the daily number of passengers in a certain line

* Viajeros por expedición: Refers to the number passengers in each time in which the bus was in services

* Kilometros anuales recorridos: Refers to the number of kilometers that the bus toured in a year.

In the next section you can find the functionalities of the app: 

### Data:

In this first tab, we can observe the data of the public transport of Alcobendas in 2015,2016 and 2017. The table shows all the variable that contains the dataset,
if you want you can select only the information of the line that you prefer. 

### Variable distribution:

The variable distribution is shown with a histogram plot, this is use to understand the behavior of tha variable that are studied. In this panel
you can select the variable that you want to analyze. 

### Relations between variables: 

In this panel we can observe a plot that is called correlation plot, this is used to understand the behavior between then. For example, if we see a cloud of points that draw a diagonal that increase
from the down left side to the up rigth side the relation is positive. On the other hand, if that point cloud draws  a diagonal that decrease from the up left corner to  the down rigth corner we can say
that those two variable have a negative relation. Otherwise, we can say that the variables have not relation. 

### Differences between two types:

In the final tab we can see a box plot that let us to understand some differences between the two types of autobuses in the public transport of Alcobendas (Interurban and Urban)
