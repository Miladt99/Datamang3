import streamlit as st
import pandas as pd
from pymongo import MongoClient
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Verbindung zu MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["supplychain"]
collection = db["logistikdaten"]

data = list(collection.find())
if not data:
    st.warning("Keine Logistikdaten in MongoDB gefunden!")
    st.stop()

df = pd.DataFrame(data)
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)
if "zeitstempel" in df.columns:
    df["zeitstempel"] = pd.to_datetime(df["zeitstempel"])
    df["datum"] = df["zeitstempel"].dt.floor('D')

st.title("Supply Chain Logistik-Dashboard (MongoDB)")

# Filter
sorte = st.selectbox("Bananensorte wählen", ["Alle"] + sorted(df["bananensorte"].unique()))
if sorte != "Alle":
    df = df[df["bananensorte"] == sorte]

# 1. Gesamtmenge pro Bananensorte
st.header("1. Gesamtmenge pro Bananensorte")
menge_pro_sorte = df.groupby("bananensorte")["menge"].sum()
if not isinstance(menge_pro_sorte, pd.Series):
    menge_pro_sorte = pd.Series(menge_pro_sorte)
menge_pro_sorte = menge_pro_sorte.sort_values(ascending=False)
st.bar_chart(menge_pro_sorte)

# 2. Zeitreihe: Menge pro Tag
st.header("2. Zeitreihe: Menge pro Tag")
if "datum" in df.columns:
    menge_pro_tag = df.groupby("datum")["menge"].sum()
    st.write(menge_pro_tag)  # Debug: Zeige die Zeitreihe an
    menge_pro_tag = menge_pro_tag.asfreq('D').fillna(0)
    st.line_chart(menge_pro_tag)

# 3. Top-Lager nach Gesamtmenge
st.header("3. Top-Lager nach Gesamtmenge")
menge_pro_lager = df.groupby("lager")["menge"].sum()
if not isinstance(menge_pro_lager, pd.Series):
    menge_pro_lager = pd.Series(menge_pro_lager)
menge_pro_lager = menge_pro_lager.sort_values(ascending=False)
st.bar_chart(menge_pro_lager)

# 4. Lieferantenvergleich
st.header("4. Lieferantenvergleich")
menge_pro_lieferant = df.groupby("lieferant")["menge"].sum()
if not isinstance(menge_pro_lieferant, pd.Series):
    menge_pro_lieferant = pd.Series(menge_pro_lieferant)
menge_pro_lieferant = menge_pro_lieferant.sort_values(ascending=False)
st.bar_chart(menge_pro_lieferant)

# 5. Ausreißererkennung (Z-Score)
st.header("5. Ausreißererkennung bei Mengen")
df["zscore"] = (df["menge"] - df["menge"].mean()) / df["menge"].std()
ausreisser = df[np.abs(df["zscore"]) > 2]
st.write("Ausreißer (Z-Score > 2):")
st.dataframe(ausreisser[["zeitstempel", "lager", "bananensorte", "menge", "lieferant", "zscore"]])

# 6. ARIMA-Prognose
st.header("6. Vorhersage der täglichen Gesamtmenge (ARIMA)")
if "datum" in df.columns:
    menge_pro_tag = df.groupby("datum")["menge"].sum()
    menge_pro_tag = menge_pro_tag.asfreq('D').fillna(0)
    st.write(menge_pro_tag)  # Debug: Zeige die Zeitreihe an
    try:
        model = sm.tsa.ARIMA(menge_pro_tag, order=(2,1,2))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=7)
        # Ensure menge_pro_tag.index is a DatetimeIndex
        if not isinstance(menge_pro_tag.index, pd.DatetimeIndex):
            forecast_start = pd.to_datetime(menge_pro_tag.index[-1]) + pd.Timedelta(days=1)
        else:
            forecast_start = menge_pro_tag.index[-1] + pd.Timedelta(days=1)
        forecast_index = pd.date_range(forecast_start, periods=7, freq='D')
        forecast_series = pd.Series(forecast, index=forecast_index)

        # Plot: Ist-Werte + Prognose
        fig, ax = plt.subplots()
        menge_pro_tag.plot(ax=ax, label="Ist-Werte")
        forecast_series.plot(ax=ax, label="Vorhersage (nächste 7 Tage)", color="orange")
        ax.set_title("ARIMA-Vorhersage der täglichen Gesamtmenge")
        ax.set_ylabel("Menge")
        ax.legend()
        st.pyplot(fig)

        # Prognosewerte als Tabelle
        st.write("Vorhersage für die nächsten 7 Tage:")
        st.dataframe(forecast_series.rename("Vorhersage").to_frame())
    except Exception as e:
        st.warning(f"ARIMA-Vorhersage nicht möglich: {e}")

# Optional: Rohdaten
with st.expander("Rohdaten anzeigen"):
    st.dataframe(df) 