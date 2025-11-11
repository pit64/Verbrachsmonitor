import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 📁 Dateiname für Speicherung
filename = "verbrauchsdaten.csv"

# 📅 Kategorien und Monate
categories = ["Wasser", "Warmwasser", "Heizung"]
months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

st.title("💧🔥 Verbrauchsmonitor")

# 📥 Daten laden oder neu erstellen
if os.path.exists(filename):
    try:
        df = pd.read_csv(filename)
        # Sicherstellen, dass die Monats-Spalte existiert
        if "Monat" not in df.columns:
            df.insert(0, "Monat", months)
        df.set_index("Monat", inplace=True)
        st.success("✅ Verbrauchsdaten geladen.")
    except Exception as e:
        st.error(f"Fehler beim Laden: {e}")
        df = pd.DataFrame({category: [0.0]*12 for category in categories}, index=months)
else:
    df = pd.DataFrame({category: [0.0]*12 for category in categories}, index=months)
    st.info("ℹ️ Keine gespeicherten Daten gefunden. Neue Tabelle erstellt.")

# 🖊️ Eingabeformular
st.subheader("📥 Verbrauchswerte eingeben oder bearbeiten")
for category in categories:
    st.markdown(f"**{category}**")
    for month in months:
        df.loc[month, category] = st.number_input(
            f"{category} ({month})", min_value=0.0, step=0.1,
            value=float(df.loc[month, category]), key=f"{category}_{month}"
        )

# 💾 Speichern
if st.button("💾 Daten speichern"):
    # Monatsnamen als Spalte speichern, nicht nur als Index
    df.reset_index().to_csv(filename, index=False)
    st.success("Daten erfolgreich gespeichert!")

# 📤 CSV-Download
st.download_button(
    label="📥 Verbrauchsdaten als CSV herunterladen",
    data=df.reset_index().to_csv(index=False).encode('utf-8'),
    file_name='verbrauchsdaten.csv',
    mime='text/csv'
)

# 📊 Jahresverbrauch anzeigen
st.subheader("📊 Jahresverbrauch")
for category in categories:
    total = df[category].sum()
    st.write(f"{category}: **{total:.2f}**")

# 📈 Diagramm
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

