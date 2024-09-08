from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime

# Create a SparkSession
spark = SparkSession.builder.appName("Process Plant Data").getOrCreate()

print('Starting spark Session')

site_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("gs://gas-turbine-data/turbine-data/site_metadata.csv")

print('Loaded site metadata')

df = spark.read.format("csv").option("header", "true").option(
    "inferSchema", "true").load("gs://gas-turbine-data/turbine-data/plant_data/ABORIGINAL-PICULET.csv")

print('Loaded plant data')

# Fill null values with 0
df = df.fillna(0)

print('Filled null values')

# Rename column "Unnamed: 0" to "ID"
df = df.withColumnRenamed("Unnamed: 0", "ID")

print('Renamed column')

# Convert "DATE_TIME" column to timestamp and split into "DATE" and "TIME" columns
# df = df.withColumn("DATE_TIME", from_unixtime(col("DATE_TIME"))).withColumn("DATE", col(
#     "DATE_TIME").cast("date")).withColumn("TIME", col("DATE_TIME").cast("time")).drop("DATE_TIME")

# Calculate thermal efficiency for each plant using the fuel LHV value from site_df
for i in range(1, int((len(df.columns) - 3) / 4) + 1):
    for j in range(45):
        df = df.withColumn("THERMAL_EFF", col(
            f"POWER_{i}") / (col(f"FUEL_FLOW_{i}") * 21503.417436) * 100)

print('Calculated thermal efficiency')

# Write the processed DataFrame to CSV
df.write.format("csv").option("header", "true").mode(
    "overwrite").option("delimiter", ",").save("gs://gas-turbine-data/analysed-data/ABORIGINAL-PICULET.csv")

print('Finished processing files')

# Stop the SparkSession
spark.stop()
