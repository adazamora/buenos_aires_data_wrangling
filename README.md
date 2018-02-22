# Buenos Aires Data Wrangling

I used data munging techniques to clean OpenStreetMap data from Buenos Aires, then exported it to a database and explored it running queries.


## Files information

This project was part of the Udacity "Data Wrangling" course. 

Each .py file starts with a letter that indicates the order that the files should be run, as variables and data from some files is later used in other files.

The order of the files is as follows: 

a_write_samples.py

b_top_level_tags.py 

c_audit_streets.py 

d_audit_coordinates.py 

e_audit_postal_codes.py 

f_clean_osm_data.py

g_write_csv.py 

h_create_db.py

i_db_queries.py 

There’s also a schema.py file that contains the schema used to create the tables for the database. 

Rubic questions file refers to some questions I had to answer to submit the project and contains the results of the queries I executed on the dataset and some analysis.

## Prerequisites

To install the requirements on a Pyhon 3.6.1 conda environment:

```
conda install --file requirements.txt
conda install -c conda-forge cerberus 
```

To create a new environment that uses the requirements:

```
conda create --name <env> --file requirements.txt
conda install -c conda-forge cerberus 
```

## Data

The Buenos Aires osm data can be downloaded in osm format from this link: https://mapzen.com/data/metro-extracts/metro/buenos-aires_argentina/

The dataset used to verify the accuracy and consistency of the postal codes in the osm file, can be downloaded here: https://yadi.sk/d/WIc5FNVEtk9U8 
