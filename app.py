import streamlit as st
import requests
import pickle
import pandas as pd

# === Load your trained model ===
model = pickle.load(open('outage_model.pkl', 'rb'))

# === Your OpenWeatherMap API Key ===
API_KEY = "9ec898ed86ffafa9f14138eade261bf0"

st.set_page_config(page_title="Electricity Outage Predictor", page_icon="⚡")
st.title("⚡ Electricity Outage Prediction in Indian Towns")
st.write("📍 Enter any Indian city, town or village to check power outage prediction based on live weather conditions.")

# === User Input for Town ===
town = st.text_input("🏙️ Enter town / city / village name (India)", "")

# === Input for past outages (not a slider) ===
past_outages = st.number_input("📊 Enter number of past outages in last 30 days", min_value=0, max_value=30, step=1)

# === Predict Button ===
if st.button("🔍 Predict Outage"):
    if town.strip() == "":
        st.warning("⚠️ Please enter a town or city name.")
    else:
        # === Build OpenWeatherMap API URL ===
        url = f"https://api.openweathermap.org/data/2.5/weather?q={town},IN&appid={API_KEY}&units=metric"

        # === Fetch weather data ===
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            st.error("❌ Town not found. Please check the spelling and try again.")
        else:
            # === Extract weather data ===
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            rainfall = data.get("rain", {}).get("1h", 0)  # default to 0 if missing

            # === Display weather data ===
            st.markdown("### 🌦️ Live Weather Info")
            st.write(f"🌡️ Temperature: **{temperature}°C**")
            st.write(f"💧 Humidity: **{humidity}%**")
            st.write(f"🌧️ Rainfall (last 1hr): **{rainfall} mm**")
            st.write(f"🌬️ Wind Speed: **{wind_speed} km/h**")

            # === Prepare input for model ===
            input_data = pd.DataFrame([[temperature, humidity, rainfall, wind_speed, past_outages]],
                                      columns=["Temperature", "Humidity", "Rainfall", "Wind Speed", "Past Outages"])

            # === Predict outage ===
            prediction = model.predict(input_data)[0]
            confidence = max(model.predict_proba(input_data)[0]) * 100

            # === Display prediction ===
            st.markdown("### 🔍 Prediction Result")
            if prediction == 1:
                st.error("⚠️ Power Outage Expected")
            else:
                st.success("✅ No Power Outage Expected")

            st.info(f"🧠 Model Confidence: **{confidence:.2f}%**")

            # === Show Additional Info at Bottom ===
            st.markdown("### 🧮 Additional Info (Simulated)")
            st.write(f"📊 Number of past outages (last 30 days): **{past_outages}**")
