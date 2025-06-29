import streamlit as st
import numpy as np
import pickle
import requests

# Load the model
model = pickle.load(open('outage_model.pkl', 'rb'))

# Get weather data from OpenWeatherMap
def get_weather(town, api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={town}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return None

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        rainfall = data.get("rain", {}).get("1h", 0)  # Rain in last hour

        return temperature, humidity, rainfall, wind_speed
    except:
        return None

# Streamlit UI
st.set_page_config(page_title="Electricity Outage Predictor")
st.title("⚡ Electricity Outage Prediction by Town Name")

town = st.text_input("Enter Town Name (e.g., Vijayawada, Guntur, etc.)")

if st.button("Predict Outage"):
    API_KEY = "7e3b3a1fb759df9356859b79fb919d9c"  # Replace with your actual OpenWeatherMap API key
    weather = get_weather(town, API_KEY)

    if weather:
        temperature, humidity, rainfall, wind_speed = weather

        # Use fixed or estimated values for remaining features
        past_outages = 2  # You can use logic or keep it fixed for now
        population_density = 1000  # Just an assumption

        features = np.array([[temperature, humidity, rainfall, wind_speed, past_outages, population_density]])
        result = model.predict(features)

        st.subheader("Town Weather Info:")
        st.write(f"🌡️ Temperature: {temperature} °C")
        st.write(f"💧 Humidity: {humidity} %")
        st.write(f"🌧️ Rainfall: {rainfall} mm")
        st.write(f"💨 Wind Speed: {wind_speed} km/h")

        if result[0] == 1:
            st.error("⚠️ Power Outage Expected!")
        else:
            st.success("✅ No Power Outage Expected")

    else:
        st.error("❌ Unable to fetch weather data. Check town name or API key.")
