# Analyzing of click stream and training set data
## Description
This program analyse typical e-commerce click stream data and training set in RankLib format.
Data is read line by line so this program can be used for analysis of huge files. Program settings are placed in **config.json**.
### analyse_data.py
There are several available modes:
 * Statistic
 * Queries
 * Histogram
 * Scatter plot
##### Statistic
Apply only for click stream.
Print number of query - product pairs, number of unique queries, max/min/avg products per query, products with zero clicks
##### Queries
Apply only for click stream.
Write in file all unique queries that was filtered by several filters. Filters are defined in settings. Can add to queries number of products.
##### Histogram
Apply for click stream and training set. Source can be changed in settings.
Show histogram of click stream/training set column data. 
##### Scatter plot
Apply only for training set.
Show 2d or 3d scatter plot of training set column data. 
### indexer.py
Index training set and click stream data to Solr. Use separate core for that.
It's expected that core will be create by **bin\solr** script with default configs so Managed schema will be enabled.
For initializing of fields use **add-fields.sh**. Other useful scripts is placed in **solr-scripts** folder.
## Information
This program is written on *Python 3.5*.
It use **matplotlib**, **requests**. 