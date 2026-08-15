import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="FIRE BLAZE",
    page_icon="🎰",
    layout="centered"
)

st.title("🎰 FIRE BLAZE")
st.subheader("ANALISADOR DE 22 CANDIDATOS")

RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

# ==========================================================
# HISTÓRICO DOS 110 RESULTADOS
# ==========================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

# ==========================================================
# ETAPA 1 - COLAR OS 110 RESULTADOS
# ==========================================================

st.markdown("## 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS")

st.caption(
    "Cole os resultados separados por espaço, vírgula ou um por linha."
)

texto_110 = st.text_area(
    "Últimos 110 resultados",
    height=180,
    placeholder="Exemplo: 19 34 2 14 17 22..."
)

if st.button("📥 CARREGAR OS 110 RESULTADOS", use_container_width=True):

    texto = (
        texto_110
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
    )

    numeros = []

    for item in texto.split():
        try:
            numero = int(item)

            if 0 <= numero <= 36:
                numeros.append(numero)

        except:
            pass

    if len(numeros) < 110:

        st.error(
            f"❌ Foram encontrados apenas {len(numeros)} números. "
            "Cole os 110 resultados."
        )

    else:

        # Pega somente os 110 mais recentes
        st.session_state.historico = numeros[-110:]

        st.success(
            f"✅ {len(st.session_state.historico)} resultados carregados!"
        )

# ==========================================================
# MOSTRA A BASE ATUAL
# ==========================================================

if st.session_state.historico:

    st.info(
        f"📊 Base atual: {len(st.session_state.historico)} resultados"
    )

    st.write(
        "Último resultado da base:",
        st.session_state.historico[-1]
    )

# ==========================================================
# ETAPA 2 - NOVO RESULTADO
# ==========================================================

st.markdown("---")
st.markdown("## 🎰 2. NOVO RESULTADO")

st.caption(
    "Saiu um novo número? Digite aqui. "
    "O aplicativo vai analisar esse resultado usando os 110 anteriores."
)

novo_resultado = st.number_input(
    "Novo número que acabou de sair",
    min_value=0,
    max_value=36,
    value=0,
    step=1
)

if st.button("🎯 ANALISAR NOVO RESULTADO", use_container_width=True):

    if len(st.session_state.historico) < 110:

        st.error(
            "❌ Primeiro carregue os 110 resultados."
        )

    else:

        # ==================================================
        # GUARDA OS 110 ANTERIORES
        # ==================================================

        base = st.session_state.historico.copy()

        # O novo resultado entra no histórico
        historico_atualizado = base + [novo_resultado]

        # Mantém somente os 110 mais recentes
        historico_atualizado = historico_atualizado[-110:]

        # Atualiza a memória do aplicativo
        st.session_state.historico = historico_atualizado

        # ==================================================
        # O NOVO RESULTADO É O PONTO DE REFERÊNCIA
        # ==================================================

        ultimo = novo_resultado

        frequencia = Counter(base)

        ultimos_20 = Counter(base[-20:])
        ultimos_40 = Counter(base[-40:])

        pos_ultimo = RODA.index(ultimo)

        scores = {}

        # ==================================================
        # CALCULA O SCORE DOS NÚMEROS
        # ==================================================

        for numero in RODA:

            # Não coloca o próprio número que acabou de sair
            if numero == ultimo:
                continue

            score = 0

            # Frequência nos 110
            score += frequencia[numero] * 2

            # Frequência nos últimos 40
            score += ultimos_40[numero] * 3

            # Frequência nos últimos 20
            score += ultimos_20[numero] * 5

            # ------------------------------------------------
            # POSIÇÃO NA RODA
            # ------------------------------------------------

            pos_numero = RODA.index(numero)

            distancia = min(
                (pos_numero - pos_ultimo) % len(RODA),
                (pos_ultimo - pos_numero) % len(RODA)
            )

            # Peso pela proximidade na roda
            pesos = {
                1: 8,
                2: 7,
                3: 6,
                4: 5,
                5: 4,
                6: 3,
                7: 2,
                8: 1
            }

            score += pesos.get(distancia, 0)

            scores[numero] = score

        # ==================================================
        # RANKING
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

        # 8 + 7 + 7
        probabilidade = candidatos[:8]
        marcacoes = candidatos[8:15]
        possiveis = candidatos[15:22]

        # ==================================================
        # RESULTADO
        # ==================================================

        st.success(
            f"🎰 Último resultado analisado: {ultimo}"
        )

        st.info(
            "📊 Análise baseada nos 110 resultados anteriores."
        )

        # ==================================================
        # 🔥 8 MAIORES PROBABILIDADES
        # ==================================================

        st.markdown("---")
        st.markdown("## 🔥 PROBABILIDADE")
        st.caption("8 maiores scores do modelo")

        colunas = st.columns(4)

        for i, numero in enumerate(probabilidade):

            with colunas[i % 4]:

                st.metric(
                    f"#{i + 1}",
                    numero
                )

                st.caption(
                    f"Score {scores[numero]}"
                )

        # ==================================================
        # 🎯 7 MARCAÇÕES
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
                    f"Score {scores[numero]}"
                )

        # ==================================================
        # 🟢 7 POSSÍVEIS
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
                    f"Score {scores[numero]}"
                )

        # ==================================================
        # RESUMO
        # ==================================================

        st.markdown("---")
        st.markdown("## 📊 RESUMO")

        st.write("🔥 **Probabilidade (8):**", probabilidade)
        st.write("🎯 **Marcações (7):**", marcacoes)
        st.write("🟢 **Possíveis (7):**", possiveis)

        st.success("🎯 TOTAL: 22 CANDIDATOS")

        st.warning(
            "⚠️ O ranking é uma análise estatística baseada "
            "nos dados fornecidos e na posição dos números "
            "na roda. Não garante o próximo resultado."
        )
