[media pointer="file-service://file-7MXMrpijuNW3e8fyDujqSh"]
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

if town:
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

        # === Simulated Extra Inputs ===
        st.markdown("### 🧮 Additional Info (Simulated)")
        past_outages = st.slider("📊 Number of past outages (last 30 days)", 0, 10, 2)
        population_density = st.slider("👥 Population Density (people per sq km)", 100, 2000, 800)

        # === Prepare input for model ===
        input_data = pd.DataFrame([[temperature, humidity, rainfall, wind_speed, past_outages, population_density]],
                                  columns=["Temperature", "Humidity", "Rainfall", "Wind Speed", "Past Outages", "Population Density"])

        # === Predict outage ===
        prediction = model.predict(input_data)[0]
        confidence = max(model.predict_proba(input_data)[0]) * 100

        st.markdown("### 🔍 Prediction Result")
        if prediction == 1:
            st.error("⚠️ Power Outage Expected")
        else:
            st.success("✅ No Power Outage Expected")

        st.info(f"🧠 Model Confidence: **{confidence:.2f}%**") 
