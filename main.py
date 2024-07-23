import streamlit as st
import plotly.express as px
from backend import get_data

# add title, text input, slider, select box, subheader
st.title("Weather Forecast for the Next Days")

place = st.text_input("Place: ").capitalize()

days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of days of forecast days")

option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        # get the temperature/sky data
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            # create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature"})
            st.plotly_chart(figure)

        if option == "Sky":
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            images = {"Clear": "images_weather/clear.png", "Clouds": "images_weather/cloud.png",
                      "Snow": "images_weather/snow.png", "Rain": "images_weather/rain.png"}
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115)
    except KeyError:
        st.write("That place does not exist.")