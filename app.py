import streamlit as st
import requests
import pickle
import pandas as pd

# === Load your trained model ===
model = pickle.load(open('outage_model.pkl', 'rb'))

# === Your OpenWeatherMap API Key ===
API_KEY = "9ec898ed86ffafa9f14138eade261bf0"

# === Streamlit App Config ===
st.set_page_config(page_title="Electricity Outage Predictor", page_icon="⚡")
st.title("⚡ Electricity Outage Prediction in Indian Towns")
st.write("📍 Enter any Indian city, town or village to check power outage prediction based on live weather conditions.")

# === User Input ===
town = st.text_input("🏙️ Enter town / city / village name (India)", "")

# === Predict Button ===
if st.button("🔍 Predict Outage"):
    if not town.strip():
        st.warning("⚠️ Please enter a valid town name.")
    else:
        # === Build API URL ===
        url = f"https://api.openweathermap.org/data/2.5/weather?q={town},IN&appid={API_KEY}&units=metric"

        # === Make API Request ===
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            st.error("❌ Town not found. Please check the spelling and try again.")
        else:
            # === Extract Weather Features ===
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            rainfall = data.get("rain", {}).get("1h", 0)  # Default to 0 mm

            # === Display Weather Info ===
            st.markdown("### 🌦️ Live Weather Info")
            st.write(f"🌡️ Temperature: **{temperature}°C**")
            st.write(f"💧 Humidity: **{humidity}%**")
            st.write(f"🌧️ Rainfall (last 1hr): **{rainfall} mm**")
            st.write(f"🌬️ Wind Speed: **{wind_speed} km/h**")

            # === Prepare input for model ===
            input_data = pd.DataFrame([[temperature, humidity, rainfall, wind_speed]],
                                      columns=["Temperature", "Humidity", "Rainfall", "Wind Speed"])

            # === Predict outage ===
            prediction = model.predict(input_data)[0]
            confidence = max(model.predict_proba(input_data)[0]) * 100

            # === Show Result ===
            st.markdown("### 🔍 Prediction Result")
            if prediction == 1:
                st.error("⚠️ Power Outage Expected")
            else:
                st.success("✅ No Power Outage Expected")

            st.info(f"🧠 Model Confidence: **{confidence:.2f}%**")
