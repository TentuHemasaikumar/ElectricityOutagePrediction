import streamlit as st
import requests
import pickle
import pandas as pd

# === Load the trained model ===
model = pickle.load(open('outage_model.pkl', 'rb'))

# === OpenWeatherMap API Key ===
API_KEY = "9ec898ed86ffafa9f14138eade261bf0"

# === Streamlit Page Settings ===
st.set_page_config(page_title="Electricity Outage Predictor", page_icon="⚡")
st.title("⚡ Electricity Outage Prediction by Town Name")
st.write("Enter Town Name (e.g., Vijayawada, Guntur, etc.)")

# === Input field for town name ===
town = st.text_input("", "Giddalur")  # default can be empty or any town

if st.button("🔍 Predict Outage"):
    if town.strip() == "":
        st.warning("Please enter a town name.")
    else:
        # === Fetch weather data from OpenWeatherMap ===
        url = f"https://api.openweathermap.org/data/2.5/weather?q={town},IN&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            st.error("❌ Town not found. Please check the spelling and try again.")
        else:
            # === Extract weather features ===
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            rainfall = data.get("rain", {}).get("1h", 0)

            # === Show weather info ===
            st.markdown("### 🌤️ Town Weather Info:")
            st.write(f"🌡️ Temperature: {temperature} °C")
            st.write(f"💧 Humidity: {humidity} %")
            st.write(f"🌧️ Rainfall: {rainfall} mm")
            st.write(f"🌬️ Wind Speed: {wind_speed} km/h")

            # === Prepare input for model ===
            input_data = pd.DataFrame([[temperature, humidity, rainfall, wind_speed]],
                                      columns=["Temperature", "Humidity", "Rainfall", "Wind Speed"])

            # === Predict outage ===
            prediction = model.predict(input_data)[0]

            # === Show prediction result ===
            if prediction == 1:
                st.error("⚠️ Power Outage Expected")
            else:
                st.success("✅ No Power Outage Expected")
