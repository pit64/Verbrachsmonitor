import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

filename = "verbrauchsdaten.csv"
categories = ["Wasser", "Warmwasser", "Heizung"]
months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

st.title("💧🔥 Verbrauchsmonitor")

# 📥 Daten laden
if os.path.exists(filename):
    df = pd.read_csv(filename)
    if "Monat" not in df.columns:
        df.insert(0, "Monat", months)
    df.set_index("Monat", inplace=True)
    st.success("✅ Verbrauchsdaten geladen.")
else:
    df = pd.DataFrame({category: [0.0]*12 for category in categories}, index=months)
    st.info("ℹ️ Neue Tabelle erstellt.")

# 🖊️ Eingabeformular
st.subheader("📥 Verbrauchswerte eingeben oder bearbeiten")

# Neue Werte sammeln, nicht direkt überschreiben
new_values = df.copy()

for category in categories:
    st.markdown(f"**{category}**")
    for month in months:
        new_values.loc[month, category] = st.number_input(
            f"{category} ({month})",
            min_value=0.0,
            step=0.1,
            value=float(df.loc[month, category]),
            key=f"{category}_{month}"
        )

# 💾 Speichern
if st.button("💾 Daten speichern"):
    new_values.reset_index().to_csv(filename, index=False)
    st.success("Daten erfolgreich gespeichert!")
    df = new_values  # Update aktuelle Daten

# 📤 Download
st.download_button(
    label="📥 Verbrauchsdaten als CSV herunterladen",
    data=new_values.reset_index().to_csv(index=False).encode('utf-8'),
    file_name='verbrauchsdaten.csv',
    mime='text/csv'
)

# 📊 Jahresverbrauch
st.subheader("📊 Jahresverbrauch")
for category in categories:
    total = new_values[category].sum()
    st.write(f"{category}: **{total:.2f}**")

# 📈 Diagramm
st.subheader("📈 Verbrauchsdiagramm")
fig, ax = plt.subplots(figsize=(10, 5))
for category in categories:
    ax.plot(months, new_values[category], marker='o', label=category)

ax.set_title("Monatlicher Verbrauch")
ax.set_xlabel("Monat")
ax.set_ylabel("Verbrauch (m³ oder kWh)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

