import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

ROULETA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

st.title("🎯 ROBÔ SGU")
st.subheader("ANALISADOR DE 22 CANDIDATOS")

st.markdown("### 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS")

texto = st.text_area(
    "Cole os resultados",
    height=160,
    placeholder="Cole aqui os 110 resultados..."
)

# Guarda os resultados analisados
if "historico" not in st.session_state:
    st.session_state.historico = []

# BOTÃO DOS 110
if st.button(
    "📊 ANALISAR 110 RESULTADOS",
    use_container_width=True
):

    try:
        numeros = [
            int(x)
            for x in texto.replace(",", " ").split()
        ]

        numeros = [
            n for n in numeros
            if 0 <= n <= 36
        ]

        if len(numeros) < 20:
            st.warning(
                f"⚠️ Precisamos de pelo menos 20 resultados. "
                f"Atualmente: {len(numeros)}"
            )

        else:
            st.session_state.historico = numeros[-110:]

            st.success(
                f"✅ {len(st.session_state.historico)} resultados carregados."
            )

    except ValueError:
        st.error("❌ Verifique os números digitados.")

# MOSTRA STATUS
if st.session_state.historico:
    st.info(
        f"📊 Base estatística ativa: "
        f"{len(st.session_state.historico)} resultados"
    )

# SEPARADOR
st.divider()

# ÚLTIMO NÚMERO
st.markdown("### 🎰 2. ÚLTIMO NÚMERO QUE SAIU")

ultimo = st.number_input(
    "Digite o último número",
    min_value=0,
    max_value=36,
    value=0,
    step=1
)

# BOTÃO DA ANÁLISE
if st.button(
    "🎯 ANALISAR ÚLTIMO NÚMERO",
    use_container_width=True
):

    historico = st.session_state.historico

    if len(historico) < 20:
        st.warning(
            "⚠️ Primeiro cole os resultados e toque em "
            "'ANALISAR 110 RESULTADOS'."
        )
        st.stop()

   
