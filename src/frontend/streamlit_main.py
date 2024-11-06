import streamlit as st
import pandas as pd
from io import BytesIO
import time

from backend.services.explainer import ExplainerCreator


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


st.title("iScope3.1")
st.info("""
        Beispiel UI um iScope3.1 zu nutzen.
        """)
st.subheader("", divider="rainbow")

st.header("👇 Hier den Kontext zum Kunden eintragen:")
with st.form("client_context"):
    client_context = st.text_input(
        "Kontext zum Unternehmen, welches betrachtet werden soll. Wenn möglich Unternehmensnamen nennen.",
        placeholder="Das Unternehmen ist ein international agierender Lebensmittelproduzent aus dem Iran.",
    )
    uploaded_file = st.file_uploader("Hier die Liste der Items hochladen.", type="xlsx")
    submitted = st.form_submit_button("☑️ Submit")

if submitted:
    st.subheader("Dein Input", anchor=False, divider="rainbow")
    workload = pd.read_excel(uploaded_file)
    st.write(workload)

    start_time = time.time()

    creator = ExplainerCreator(workload, "prompt.txt", context=client_context)
    results = creator.get_results()

    end_time = time.time()
    time_taken = end_time - start_time

    st.write(
        f"Verarbeitungszeit: {time_taken:.2f} Sekunden für {len(workload)-1} Einträge"
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        results.to_excel(writer, index=False, sheet_name="Sheet1")

    st.write("### Verarbeitete Daten:")
    st.dataframe(results)

    processed_data = output.getvalue()
    st.download_button(
        label="Ergebnisse als Excel herunterladen",
        data=processed_data,
        file_name="processed_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
