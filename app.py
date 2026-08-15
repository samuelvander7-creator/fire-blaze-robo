import streamlit as st
from collections import Counter

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="FIRE BLAZE",
    page_icon="🎰",
    layout="centered"
)

st.title("🎰 FIRE BLAZE")
st.subheader("22 CANDIDATOS")

# Ordem da roleta europeia
RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

# Histórico da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# ==========================================================
# ENTRADA
# ==========================================================

ultimo = st.number_input(
    "🎰 ÚLTIMO NÚMERO QUE SAIU",
    min_value=0,
    max_value=36,
    value=0,
    step=1
)

# ==========================================================
# ANALISAR
# ==========================================================

if st.button("🎯 ANALISAR", use_container_width=True):

    # Salva o resultado
    st.session_state.historico.append(ultimo)

    historico = st.session_state.historico

    # Precisa de histórico mínimo
    if len(historico) < 20:

        st.warning(
            f"⚠️ Precisamos de pelo menos 20 resultados. "
            f"Atualmente: {len(historico)}"
        )

    else:

        # Usa os últimos 240 resultados
        dados = historico[-240:]

        frequencia = Counter(dados)

        # Últimos 20 têm peso maior
        recentes = Counter(dados[-20:])

        pos_ultimo = RODA.index(ultimo)

        scores = {}

        # ==================================================
        # SCORE DOS 37 NÚMEROS
        # ==================================================

        for numero in RODA:

            # Não colocar o próprio último resultado
            if numero == ultimo:
                continue

            score = 0

            # Frequência geral
            score += frequencia[numero] * 2

            # Frequência recente
            score += recentes[numero] * 4

            # Distância na roda
            pos_numero = RODA.index(numero)

            distancia = min(
                (pos_numero - pos_ultimo) % len(RODA),
                (pos_ultimo - pos_numero) % len(RODA)
            )

            # Quanto mais próximo na roda,
            # maior o peso do modelo
            if distancia == 1:
                score += 8

            elif distancia == 2:
                score += 6

            elif distancia == 3:
                score += 4

            elif distancia == 4:
                score += 2

            scores[numero] = score

        # ==================================================
        # RANKING
        # ==================================================

        ranking = sorted(
            scores.keys(),
            key=lambda numero: scores[numero],
            reverse=True
        )

        # ==================================================
        # 22 CANDIDATOS
        # ==================================================

        candidatos = ranking[:22]

        # 8 + 7 + 7
        probabilidade = candidatos[:8]
        marcacoes = candidatos[8:15]
        possiveis = candidatos[15:22]

        # ==================================================
        # RESULTADO
        # ==================================================

        st.success(f"Último resultado: {ultimo}")

        st.markdown("## 🔥 PROBABILIDADE")
        st.caption("8 números com maior score do modelo")

        colunas = st.columns(4)

        for i, numero in enumerate(probabilidade):

            with colunas[i % 4]:
                st.metric(
                    label=f"#{i + 1}",
                    value=numero
                )

        st.markdown("---")

        st.markdown("## 🎯 MARCAÇÕES")
        st.caption("7 candidatos seguintes no ranking")

        colunas = st.columns(4)

        for i, numero in enumerate(marcacoes):

            with colunas[i % 4]:
                st.metric(
                    label=f"#{i + 9}",
                    value=numero
                )

        st.markdown("---")

        st.markdown("## 🟢 POSSÍVEIS")
        st.caption("7 candidatos seguintes no ranking")

        colunas = st.columns(4)

        for i, numero in enumerate(possiveis):

            with colunas[i % 4]:
                st.metric(
                    label=f"#{i + 16}",
                    value=numero
                )

        st.markdown("---")

        st.write("🎯 **TOTAL: 22 CANDIDATOS**")

        st.caption(
            "⚠️ As categorias representam a pontuação do modelo "
            "com base nos dados disponíveis. Em uma roleta justa, "
            "isso não garante que um número específico será o próximo."
        )
