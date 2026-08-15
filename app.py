import streamlit as st

st.set_page_config(
    page_title="🔥 FIRE BLAZE",
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

# Ordem da roleta europeia
roleta = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

if st.button("🎯 ANALISAR", use_container_width=True):

    posicao = roleta.index(ultimo)

    # ==================================================
    # 1️⃣ POSSIBILIDADE — 22 números ao redor
    # ==================================================

    possibilidade = []

    for i in range(-11, 12):
        numero = roleta[(posicao + i) % len(roleta)]

        if numero not in possibilidade:
            possibilidade.append(numero)

    st.success(f"Último resultado: {ultimo}")

    st.markdown("## 🔥 POSSIBILIDADE")
    st.write("22 candidatos ao redor do último resultado:")

    colunas = st.columns(11)

    for i, numero in enumerate(possibilidade):
        with colunas[i % 11]:
            st.metric("", numero)

    # ==================================================
    # 2️⃣ MARCAÇÕES — 10 vizinhos mais próximos
    # ==================================================

    marcacoes = []

    for distancia in range(1, 6):
        esquerda = roleta[(posicao - distancia) % len(roleta)]
        direita = roleta[(posicao + distancia) % len(roleta)]

        if esquerda not in marcacoes:
            marcacoes.append(esquerda)

        if direita not in marcacoes:
            marcacoes.append(direita)

    st.markdown("## 🎯 MARCAÇÕES")
    st.write("10 vizinhos mais próximos:")

    colunas = st.columns(5)

    for i, numero in enumerate(marcacoes):
        with colunas[i % 5]:
            st.metric("", numero)

    # ==================================================
    # 3️⃣ POSSÍVEIS — 6 mais próximos
    # ==================================================

    possiveis = []

    for distancia in range(1, 4):
        esquerda = roleta[(posicao - distancia) % len(roleta)]
        direita = roleta[(posicao + distancia) % len(roleta)]

        if esquerda not in possiveis:
            possiveis.append(esquerda)

        if direita not in possiveis:
            possiveis.append(direita)

    st.markdown("## 🔥 POSSÍVEIS")
    st.write("Os 6 números imediatamente vizinhos:")

    colunas = st.columns(6)

    for i, numero in enumerate(possiveis):
        with colunas[i]:
            st.metric("", numero)

    # ==================================================
    # AVISO
    # ==================================================

    st.warning(
        "⚠️ As marcações são baseadas exclusivamente na posição "
        "dos números na roda. Elas não garantem o próximo resultado."
    )
