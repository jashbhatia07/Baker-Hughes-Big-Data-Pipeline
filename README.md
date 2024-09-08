# Big_Data_Engineering_Project

### Description
We have multiple engine data and site data
Each site has multiple engines

Two lookup files
- engine_metadata
- site_metadata

In data directory at end of each day a csv is added that has logs of the engine data for all each plant
This data undegoes the following analysis
- Filling null values
- Renaming column ID
- Dropping redundant columns
- Calculating Thermal effiency
- Creates a new dataframe with new columns

Google Cloud Platform metadata
Region - US
Zone - us-central
