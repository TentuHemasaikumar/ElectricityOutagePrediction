import streamlit as st
import requests
import pickle
import pandas as pd

# === Load your trained model ===
model = pickle.load(open('outage_model.pkl', 'rb'))

# === OpenWeatherMap API Key ===
API_KEY = "9ec898ed86ffafa9f14138eade261bf0"

st.set_page_config(page_title="Electricity Outage Predictor", page_icon="⚡")
st.title("⚡ Electricity Outage Prediction in Indian Towns")
st.write("📍 Enter any Indian city, town or village to check power outage prediction based on live weather conditions.")

# === User input ===
town = st.text_input("🏙️ Enter Town / City / Village (India)", "Giddalur")

# === Manual number input instead of slider ===
st.markdown("### 📊 Additional Info")
past_outages = st.number_input("Number of past outages (last 30 days)", min_value=0, max_value=30, step=1, value=2)

# === Predict Button ===
if st.button("🔍 Predict Outage"):
    if town.strip() == "":
        st.warning("Please enter a valid town name.")
    else:
        # === Get weather data ===
        url = f"https://api.openweathermap.org/data/2.5/weather?q={town},IN&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            st.error("❌ Town not found. Please check the spelling and try again.")
        else:
            # === Extract weather details ===
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            rainfall = data.get("rain", {}).get("1h", 0)  # default to 0

            # === Show weather data ===
            st.markdown("### 🌤️ Weather Info")
            st.write(f"🌡️ Temperature: **{temperature} °C**")
            st.write(f"💧 Humidity: **{humidity} %**")
            st.write(f"🌧️ Rainfall: **{rainfall} mm**")
            st.write(f"🌬️ Wind Speed: **{wind_speed} km/h**")
            st.write(f"📊 Past Outages: **{past_outages}**")

            # === Prepare input for model ===
            input_data = pd.DataFrame([[temperature, humidity, rainfall, wind_speed, past_outages]],
                                      columns=["Temperature", "Humidity", "Rainfall", "Wind Speed", "Past Outages"])

            # === Predict ===
            prediction = model.predict(input_data)[0]
            confidence = max(model.predict_proba(input_data)[0]) * 100

            # === Show result ===
            st.markdown("### 🔍 Prediction Result")
            if prediction == 1:
                st.error("⚠️ Power Outage Expected")
            else:
                st.success("✅ No Power Outage Expected")

            st.info(f"🧠 Model Confidence: **{confidence:.2f}%**")
