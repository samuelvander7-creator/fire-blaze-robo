import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

# =========================
# CONFIGURAÇÃO
# =========================

ROULETA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

st.title("🎯 ROBÔ SGU")
st.subheader("ANALISADOR DE 22 CANDIDATOS")

st.info(
    "⚠️ O ROBÔ SGU faz análise estatística dos resultados informados. "
    "Isso não garante o próximo resultado."
)

# =========================
# 110 RESULTADOS
# =========================

st.markdown("### 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS")

texto = st.text_area(
    "Cole os resultados",
    height=150,
    placeholder="Exemplo:\n29 20 34 5 30 11 12 13 1 26 ..."
)

resultados = []

if texto.strip():
    try:
        resultados = [
            int(x)
            for x in texto.replace(",", " ").split()
            if x.strip()
        ]

        resultados = [
            n for n in resultados
            if n in ROULETTE
        ]

    except:
        resultados = []

st.caption(f"Resultados carregados: {len(resultados)} / 110")

# =========================
# ÚLTIMO RESULTADO
# =========================

st.markdown("### 🎰 2. ÚLTIMO NÚMERO QUE SAIU")

ultimo = st.number_input(
    "Digite o último número",
    min_value=0,
    max_value=36,
    value=0,
    step=1
)

# =========================
# ANÁLISE
# =========================

if st.button("🎯 ANALISAR", use_container_width=True):

    if len(resultados) < 20:
        st.warning(
            f"⚠️ Precisamos de pelo menos 20 resultados. "
            f"Atualmente: {len(resultados)}"
        )
        st.stop()

    # Frequência
    frequencia = Counter(resultados)

    # Posição do último número na roda
    pos = ROULETTE.index(ultimo)

    # Pontuação estatística
    scores = {}

    for numero in ROULETTE:

        freq = frequencia.get(numero, 0)

        # Recência: quanto mais recente, maior o peso
        recencia = 0

        for i, valor in enumerate(reversed(resultados)):
            if valor == numero:
                recencia = max(1, 20 - i)
                break

        # Proximidade na roda em relação ao último resultado
        p = ROULETTE.index(numero)
        distancia = min(
            abs(p - pos),
            len(ROULETTE) - abs(p - pos)
        )

        proximidade = max(0, 8 - distancia)

        scores[numero] = (
            freq * 3
            + recencia * 1.5
            + proximidade * 1.2
        )

    # Ordenação
    ordenados = sorted(
        ROULETTE,
        key=lambda n: scores[n],
        reverse=True
    )

    # =========================
    # 22 CANDIDATOS
    # =========================

    candidatos = ordenados[:22]

    # Divide 22 em 3 grupos:
    # 8 + 7 + 7 = 22

    probabilidade = candidatos[:8]
    marcacoes = candidatos[8:15]
    possiveis = candidatos[15:22]

    # =========================
    # PROBABILIDADE
    # =========================

    st.markdown("## 🔥 PROBABILIDADE")
    st.caption("8 maiores pontuações estatísticas")

    for i, numero in enumerate(probabilidade, 1):
        st.write(
            f"**#{i} — {numero}**  "
            f"Score: {scores[numero]:.1f}"
        )

    # =========================
    # MARCAÇÕES
    # =========================

    st.markdown("## 🎯 MARCAÇÕES")
    st.caption("7 candidatos seguintes")

    st.write(
        " • ".join(str(n) for n in marcacoes)
    )

    # =========================
    # POSSÍVEIS
    # =========================

    st.markdown("## 🔎 POSSÍVEIS")
    st.caption("7 candidatos complementares")

    st.write(
        " • ".join(str(n) for n in possiveis)
    )

    # =========================
    # RESUMO
    # =========================

    st.markdown("## 📊 RESUMO DOS 22")

    st.write(
        "**Probabilidade:** "
        + ", ".join(map(str, probabilidade))
    )

    st.write(
        "**Marcações:** "
        + ", ".join(map(str, marcacoes))
    )

    st.write(
        "**Possíveis:** "
        + ", ".join(map(str, possiveis))
    )

    # =========================
    # VIZINHOS DO ÚLTIMO
    # =========================

    esquerda = []
    direita = []

    for i in range(1, 4):
        esquerda.append(
            ROULETTE[(pos - i) % len(ROULETTE)]
        )
        direita.append(
            ROULETTE[(pos + i) % len(ROULETTE)]
        )

    st.markdown("## 🎰 VIZINHOS DO ÚLTIMO")

    st.write(
        f"Último: **{ultimo}**"
    )

    st.write(
        "Esquerda: "
        + " • ".join(map(str, esquerda))
    )

    st.write(
        "Direita: "
        + " • ".join(map(str, direita))
    )

    st.divider()

    st.caption(
        "ROBÔ SGU • Análise estatística • "
        "Os resultados da roleta são aleatórios."
    )
