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
st.subheader("ANALISADOR DE 22 CANDIDATOS")

# Ordem da roleta europeia
RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

# ==========================================================
# CAMPO DOS 110 RESULTADOS
# ==========================================================

st.markdown("### 📋 COLE OS 110 ÚLTIMOS RESULTADOS")

st.caption(
    "Cole os números separados por espaço, vírgula ou um por linha."
)

texto_resultados = st.text_area(
    "Resultados",
    height=180,
    placeholder="Exemplo:\n25 12 10 35 17 3 21 8 30..."
)

# ==========================================================
# ANALISAR
# ==========================================================

if st.button("🎯 ANALISAR 110 RESULTADOS", use_container_width=True):

    # ------------------------------------------------------
    # TRANSFORMA O TEXTO EM NÚMEROS
    # ------------------------------------------------------

    texto = texto_resultados.replace(",", " ")
    texto = texto.replace(";", " ")
    texto = texto.replace("\n", " ")

    partes = texto.split()

    resultados = []

    for parte in partes:
        try:
            numero = int(parte)

            if 0 <= numero <= 36:
                resultados.append(numero)

        except:
            pass

    # ------------------------------------------------------
    # VERIFICAÇÃO
    # ------------------------------------------------------

    if len(resultados) == 0:

        st.error("❌ Nenhum resultado válido foi encontrado.")

    elif len(resultados) < 110:

        st.warning(
            f"⚠️ Você colocou {len(resultados)} resultados. "
            f"O ideal é colocar os 110 últimos resultados."
        )

    else:

        # Usa exatamente os 110 mais recentes
        resultados = resultados[-110:]

        ultimo = resultados[-1]

        st.success(
            f"✅ {len(resultados)} resultados carregados."
        )

        st.info(
            f"🎰 Último resultado identificado: **{ultimo}**"
        )

        # ==================================================
        # FREQUÊNCIA
        # ==================================================

        frequencia = Counter(resultados)

        # Últimos 20 resultados recebem peso maior
        recentes = Counter(resultados[-20:])

        # Últimos 40 resultados
        medio_prazo = Counter(resultados[-40:])

        pos_ultimo = RODA.index(ultimo)

        scores = {}

        # ==================================================
        # CALCULA SCORE DOS 36 NÚMEROS RESTANTES
        # ==================================================

        for numero in RODA:

            if numero == ultimo:
                continue

            score = 0

            # ------------------------------------------------
            # FREQUÊNCIA DOS 110
            # ------------------------------------------------

            score += frequencia[numero] * 2

            # ------------------------------------------------
            # FREQUÊNCIA DOS ÚLTIMOS 40
            # ------------------------------------------------

            score += medio_prazo[numero] * 3

            # ------------------------------------------------
            # FREQUÊNCIA DOS ÚLTIMOS 20
            # ------------------------------------------------

            score += recentes[numero] * 5

            # ------------------------------------------------
            # POSIÇÃO NA RODA
            # ------------------------------------------------

            pos_numero = RODA.index(numero)

            distancia = min(
                (pos_numero - pos_ultimo) % len(RODA),
                (pos_ultimo - pos_numero) % len(RODA)
            )

            # Quanto mais próximo do último número,
            # maior a pontuação do modelo.

            if distancia == 1:
                score += 8

            elif distancia == 2:
                score += 7

            elif distancia == 3:
                score += 6

            elif distancia == 4:
                score += 5

            elif distancia == 5:
                score += 4

            elif distancia == 6:
                score += 3

            elif distancia == 7:
                score += 2

            elif distancia == 8:
                score += 1

            scores[numero] = score

        # ==================================================
        # ORDENA PELO MAIOR SCORE
        # ==================================================

        ranking = sorted(
            scores,
            key=lambda numero: scores[numero],
            reverse=True
        )

        # ==================================================
        # 22 CANDIDATOS
        # ==================================================

        candidatos = ranking[:22]

        # 8 + 7 + 7 = 22

        probabilidade = candidatos[:8]
        marcacoes = candidatos[8:15]
        possiveis = candidatos[15:22]

        # ==================================================
        # 🔥 PROBABILIDADE
        # ==================================================

        st.markdown("---")
        st.markdown("## 🔥 PROBABILIDADE")
        st.caption("8 números com maior pontuação do modelo")

        colunas = st.columns(4)

        for i, numero in enumerate(probabilidade):

            with colunas[i % 4]:

                st.metric(
                    f"#{i + 1}",
                    numero
                )

                st.caption(
                    f"Score: {scores[numero]}"
                )

        # ==================================================
        # 🎯 MARCAÇÕES
        # ==================================================

        st.markdown("---")
        st.markdown("## 🎯 MARCAÇÕES")
        st.caption("7 candidatos seguintes")

        colunas = st.columns(4)

        for i, numero in enumerate(marcacoes):

            with colunas[i % 4]:

                st.metric(
                    f"#{i + 9}",
                    numero
                )

                st.caption(
                    f"Score: {scores[numero]}"
                )

        # ==================================================
        # 🟢 POSSÍVEIS
        # ==================================================

        st.markdown("---")
        st.markdown("## 🟢 POSSÍVEIS")
        st.caption("7 candidatos seguintes")

        colunas = st.columns(4)

        for i, numero in enumerate(possiveis):

            with colunas[i % 4]:

                st.metric(
                    f"#{i + 16}",
                    numero
                )

                st.caption(
                    f"Score: {scores[numero]}"
                )

        # ==================================================
        # RESUMO
        # ==================================================

        st.markdown("---")

        st.markdown("## 🎯 RESUMO DOS 22")

        st.write(
            "**Probabilidade:**",
            probabilidade
        )

        st.write(
            "**Marcações:**",
            marcacoes
        )

        st.write(
            "**Possíveis:**",
            possiveis
        )

        st.success(
            "🔥 8 + 7 + 7 = 22 candidatos"
        )

        st.warning(
            "⚠️ A pontuação é uma classificação estatística "
            "do modelo. Em uma roleta justa, nenhum algoritmo "
            "pode garantir qual será o próximo número."
        )
