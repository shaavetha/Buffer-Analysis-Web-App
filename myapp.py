import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from io import BytesIO
import zipfile

# CSS to position the logo text at the top right corner
st.markdown("""
    <style>
    .top-right-logo {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 19px;
        font-weight: bold;
        color: #e8e1e1;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    <div class="top-right-logo">
        iSpatial Techno Solutions
    </div>
    """, unsafe_allow_html=True)
# Title
st.title("Buffer Analysis Tool")

# Sidebar for shapefile upload
st.sidebar.header("Upload Data")
shapefile = st.sidebar.file_uploader("Add Shapefile (zip format containing .shp, .shx, .dbf)", type="zip")

# Pick colour for the shapefile border
shapefile_border_color = st.sidebar.color_picker("Border Colour", "#000000")  # Default black

# Sidebar for CSV upload
csv_file = st.sidebar.file_uploader("Add CSV file with coordinates", type="csv")

# Pick the colour and symbol for CSV location points
csv_color = st.sidebar.color_picker("Colour", "#7a0d0d")  # Default red
csv_symbol = st.sidebar.selectbox("Symbol", ["o", "x", "*", "+"])  # circle, cross, asterisk, plus

# Specify column names for latitude and longitude from csv file
st.sidebar.header("Specify Column Names from CSV file")
latitude_column = st.sidebar.text_input("Latitude Column Name", value="Latitude")
longitude_column = st.sidebar.text_input("Longitude Column Name", value="Longitude")

# Input for multiple buffer distances
st.sidebar.header("Define Buffer Distances")
buffer_distances = st.sidebar.text_input("Enter Buffer Distances (comma-separated in km)", "1,2,3")
buffer_distances = [float(dist) for dist in buffer_distances.split(',')]

# Pick colours for each buffer
st.sidebar.header("Customize Buffer Colours")
buffer_colors = []
for i in range(len(buffer_distances)):
    color = st.sidebar.color_picker(f"Colour for Buffer {i+1} (Distance: {buffer_distances[i]} km)", "#FFA500")
    buffer_colors.append(color)

# Allow the user to choose the download format
export_format = st.sidebar.radio("Export Buffer As", ('Shapefile', 'PNG Image'))

# Function to create a zip file for shapefiles
def create_shapefile_zip(geo_df):
    output = BytesIO()
    with zipfile.ZipFile(output, 'w') as zf:
        geo_df.to_file("/tmp/buffer.shp")
        for file_extension in ['shp', 'shx', 'dbf']:
            filename = f"/tmp/buffer.{file_extension}"
            with open(filename, 'rb') as f:
                zf.writestr(f"buffer.{file_extension}", f.read())
    return output.getvalue()

if shapefile and csv_file:
    # Read shapefile
    gdf = gpd.read_file(shapefile)

    # Read CSV file
    csv_df = pd.read_csv(csv_file)

    # Ensure the CSV has the specified latitude and longitude columns
    if latitude_column not in csv_df.columns or longitude_column not in csv_df.columns:
        st.error(f"CSV must contain '{latitude_column}' and '{longitude_column}' columns")
    else:
        # Create GeoDataFrame from CSV
        geometry = [Point(xy) for xy in zip(csv_df[longitude_column], csv_df[latitude_column])]
        geo_df = gpd.GeoDataFrame(csv_df, geometry=geometry, crs="EPSG:4326")

        # Convert shapefile and CSV locations to the same CRS
        gdf = gdf.to_crs(epsg=3395)  # Convert to projection in meters
        geo_df = geo_df.to_crs(epsg=3395)

        # Display the shapefile with CSV locations on top
        st.subheader("Map")
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='lightblue',linewidth=0.7, edgecolor=shapefile_border_color)
        geo_df.plot(ax=ax, color=csv_color, marker=csv_symbol, markersize=100,linewidth=2.5,label='Locations')
        ax.legend()
        st.pyplot(fig)

        # Create and display multiple buffers
        st.subheader("Buffer Visualization")
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='lightblue', edgecolor=shapefile_border_color)
        
        # Plot larger buffers first, then smaller ones to ensure visibility
        for i, buffer_distance in reversed(list(enumerate(buffer_distances))):
            # Create buffer for the current distance
            buffered_geo_df = geo_df.copy()
            buffered_geo_df['geometry'] = buffered_geo_df.buffer(buffer_distance * 1000)  # Convert km to meters
            # Plot buffer with custom color and transparency
            buffered_geo_df.plot(ax=ax, color=buffer_colors[i], alpha=0.7, edgecolor='black', label=f'Buffer {buffer_distance} km')

        # Re-plot locations on top of buffers
        geo_df.plot(ax=ax, color=csv_color, marker=csv_symbol, markersize=40, label='Locations')
        ax.legend()
        st.pyplot(fig)

        # Download Buffer as Shapefile
        if export_format == 'Shapefile':
            buffer_zip = create_shapefile_zip(geo_df)
            st.download_button(
                label="Download Buffer as Shapefile",
                data=buffer_zip,
                file_name="buffer_shapefile.zip",
                mime="application/zip"
            )

        # Download Map as PNG
        elif export_format == 'PNG Image':
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Map as PNG",
                data=buf,
                file_name="buffer_map.png",
                mime="image/png"
            )


