
import streamlit as st

st.set_page_config(
    page_title="FIRE BLAZE",
    page_icon="🎰",
    layout="centered"
)

st.title("🎰 FIRE BLAZE")
st.subheader("ANALISADOR DE 22 CANDIDATOS")

ultimo = st.number_input(
    "ÚLTIMO RESULTADO",
    min_value=0,
    max_value=36,
    value=0,
    step=1
)

if st.button("🎯 ANALISAR", use_container_width=True):
    st.success(f"Último resultado informado: {ultimo}")

    st.write("🔥 7 MAIS FORTES")
    st.write("🟡 7 MARCADORES")
    st.write("🟢 8 POSSÍVEIS")
