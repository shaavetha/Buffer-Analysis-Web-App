# Buffer Analysis Web Application (Streamlit)

This is a fully interactive GIS buffer analysis web app built using Streamlit. It allows users to upload shapefiles and CSV files with Latitude and Longitude coordinates, perform multi-distance buffer analysis, and download the results as shapefiles or PNG images.


## Features

✅ Upload shapefile (.zip) and CSV file  
✅ Set custom latitude/longitude columns  
✅ Choose symbols and colors for location markers  
✅ Create multiple buffer zones with unique colors  
✅ Download as shapefile or image  
✅ Built-in visualization with Matplotlib


## Project Structure
- myapp.py #Streamlit application
- citydata.csv #Sample CSV data with UAE city coordinates
- gadm41_ARE_1.zip #Sample shapefile of UAE boundary
- README.md #Project Overview


## Tools & Libraries Used

- Streamlit
- Pandas
- GeoPandas
- Shapely
- Matplotlib
- Geopy


## How to Run

# Step 1: Install dependencies
pip install streamlit pandas geopandas matplotlib geopy shapely

# Step 2: Run the Streamlit app
streamlit run myapp.py


## Sample Use

Upload:
 - gadm41_ARE_1.zip – a zipped shapefile for UAE boundaries
 - citydata.csv – city coordinates with Latitude and Longitude columns

Customize:
 - Marker color and shape
 - Buffer distances (in km)
 - Export format (Shapefile or PNG)

