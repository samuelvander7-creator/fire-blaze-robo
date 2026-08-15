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

# Ordem da roleta europeia
roleta = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

if st.button("🎯 ANALISAR", use_container_width=True):

    if ultimo in roleta:
        posicao = roleta.index(ultimo)

        # 22 números ao redor do último resultado
        candidatos = []

        for i in range(-11, 12):
            numero = roleta[(posicao + i) % len(roleta)]

            if numero not in candidatos:
                candidatos.append(numero)

        st.success(f"Último resultado: {ultimo}")

        st.markdown("### 🔥 22 CANDIDATOS")

        # Divide em 2 linhas de 11
        colunas = st.columns(11)

        for i, numero in enumerate(candidatos):
            with colunas[i % 11]:
                st.metric("", numero)

        st.markdown("### 📊 Análise")

        vizinhos = []
        for distancia in range(1, 6):
            esquerda = roleta[(posicao - distancia) % len(roleta)]
            direita = roleta[(posicao + distancia) % len(roleta)]
            vizinhos.extend([esquerda, direita])

        st.write("**Vizinhos mais próximos:**")
        st.write(vizinhos)

        st.warning(
            "⚠️ Estes números são candidatos estatísticos baseados "
            "na posição na roda. Isso não garante o próximo resultado."
        )

else:
    st.info("Digite o último número que saiu e toque em ANALISAR.")
