import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
import pydeck as pdk
import leafmap.foliumap as leafmap
import os

st.set_page_config(
    page_title="BDE Mini Project",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

site_df = pd.read_csv(
    './bde_data/site_metadata.csv')

st.sidebar.title('BDE Mini Project')
rad1 = st.sidebar.radio("Navigation", ["Plant Locations", "Customer Plants",
                        "Elevation", "Thermal Efficiency", "N2 Emmission", "Operational Hours"])

if rad1 == "Plant Locations":
    st.title('BDE Mini Project')

    st.subheader('Locate Plants')

    m = folium.Map(location=[site_df['LATITUDE'].mean(
    ), site_df['LONGITUDE'].mean()], zoom_start=4, control_scale=True)
    for index, location_info in site_df.iterrows():
        folium.Marker([location_info["LATITUDE"], location_info["LONGITUDE"]],
                      popup=location_info["PLANT_NAME"]).add_to(m)

    folium_static(m)

if rad1 == "Customer Plants":
    st.title('BDE Mini Project')

    st.subheader('Customer Plants Numbers')

    values = site_df['CUSTOMER_NAME'].value_counts().to_dict()

    chart_data = pd.DataFrame(list(values.values()), list(values.keys()))

    st.bar_chart(chart_data)

if rad1 == "Elevation":
    st.title('BDE Mini Project')

    st.subheader('Plant Elevations')

    ele_df = pd.DataFrame(
        np.random.randn(40, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=ele_df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=ele_df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

if rad1 == "Thermal Efficiency":
    st.title('BDE Mini Project')

    st.subheader('Thermal Efficiency')

    df = pd.read_csv('./analysed_data/ABORIGINAL-PICULET.csv')

    st.write(df)

if rad1 == "N2 Emmission":
    m = leafmap.Map(tiles="stamentoner")
    st.title('BDE Mini Project')

    st.subheader('N2 Emmission')

    heat_map_df = site_df[['LATITUDE', 'LONGITUDE', 'FUEL_N2_MOL_PCT']]

    m.add_heatmap(
        heat_map_df,
        latitude="LATITUDE",
        longitude="LONGITUDE",
        value="FUEL_N2_MOL_PCT",
        name="Heat map",
        radius=20,
    )
    m.to_streamlit(width=700, height=500)

if rad1 == "Operational Hours":

    st.title('BDE Mini Project')

    st.subheader('Operational Hours')

    st.write("ABORIGINAL-PICULET - 3243 hours")

    st.write("SPIRITUAL-POLECAT - 2846 hours")

    st.write("PREHISTORIC-PETREL - 4395 hours")

    st.write("BIPEDAL-UAKARI - 4536hours")

    st.write("TOURMALINE-MOUSE - 3452 hours")

    st.write("LUSH-CHIPMUNK - 2468 hours")
