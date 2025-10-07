import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Kategorien und Monate
categories = ["Wasser", "Warmwasser", "Heizung"]
months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
filename = "verbrauchsdaten.csv"

st.title("💧🔥 Verbrauchsmonitor mit Speicherfunktion")

# Daten laden, wenn vorhanden
if os.path.exists(filename):
    df = pd.read_csv(filename, index_col=0)
    st.success("Vorhandene Daten geladen.")
else:
    df = pd.DataFrame({category: [0.0]*12 for category in categories}, index=months)

# Eingabeformular
st.subheader("📥 Verbrauchswerte eingeben oder bearbeiten")
for category in categories:
    st.markdown(f"**{category}**")
    for month in months:
        df.loc[month, category] = st.number_input(
            f"{category} ({month})", min_value=0.0, step=0.1, value=float(df.loc[month, category]), key=f"{category}_{month}"
        )

# Speichern
if st.button("💾 Daten speichern"):
    df.to_csv(filename)
    st.success("Daten erfolgreich gespeichert!")

# Jahresverbrauch anzeigen
st.subheader("📊 Jahresverbrauch")
for category in categories:
    total = df[category].sum()
    st.write(f"{category}: **{total:.2f}**")

# Diagramm
st.subheader("📈 Verbrauchsdiagramm")
fig, ax = plt.subplots(figsize=(10, 5))
for category in categories:
    ax.plot(months, df[category], marker='o', label=category)

ax.set_title("Monatlicher Verbrauch")
ax.set_xlabel("Monat")
ax.set_ylabel("Verbrauch (m³ oder kWh)")
ax.legend()
ax.grid(True)
st.pyplot(fig)
