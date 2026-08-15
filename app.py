import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

# ROULETA EUROPEIA
ROULETA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

st.title("🎯 ROBÔ SGU")
st.subheader("ANALISADOR DE 22 CANDIDATOS")

# =========================
# 110 ÚLTIMOS RESULTADOS
# =========================

st.markdown("### 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS")

texto = st.text_area(
    "Cole os resultados",
    height=150,
    placeholder="Cole os 110 números aqui..."
)

if "resultados" not in st.session_state:
    st.session_state.resultados = []

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
            # Mantém os últimos 110
            st.session_state.resultados = numeros[-110:]

            st.success(
                f"✅ {len(st.session_state.resultados)} resultados carregados."
            )

    except:
        st.error("❌ Existem valores inválidos nos resultados.")

if st.session_state.resultados:
    st.info(
        f"📊 Base estatística: "
        f"{len(st.session_state.resultados)} resultados"
    )

st.divider()

# =========================
# ÚLTIMO NÚMERO
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
# ANALISAR ÚLTIMO NÚMERO
# =========================

if st.button(
    "🎯 ANALISAR ÚLTIMO NÚMERO",
    use_container_width=True
):

    resultados = st.session_state.resultados

    if len(resultados) < 20:
        st.warning(
            "⚠️ Primeiro clique em "
            "'ANALISAR 110 RESULTADOS'."
        )
        st.stop()

    # Frequência dos 110 resultados
    frequencia = Counter(resultados)

    # Posição do último número na roda
    posicao = ROULETA.index(ultimo)

    pontuacao = {}

    for numero in ROULETA:

        freq = frequencia.get(numero, 0)

        # Recência
        recencia = 0

        for distancia, valor in enumerate(
            reversed(resultados)
        ):
            if valor == numero:
                recencia = max(0, 20 - distancia)
                break

        # Proximidade na roda
        pos_numero = ROULETA.index(numero)

        distancia_roda = min(
            abs(pos_numero - posicao),
            len(ROULETA) - abs(pos_numero - posicao)
        )

        proximidade = max(
            0,
            8 - distancia_roda
        )

        pontuacao[numero] = (
            freq * 3
            + recencia * 1.5
            + proximidade * 1.2
        )

    # Ordena todos os números
    ordenados = sorted(
        ROULETA,
        key=lambda n: pontuacao[n],
        reverse=True
    )

    # =========================
    # 22 CANDIDATOS
    # =========================

    candidatos = ordenados[:22]

    # 22 dividido nas 3 formas
    probabilidade = candidatos[:8]
    marcacoes = candidatos[8:15]
    possiveis = candidatos[15:22]

    # =========================
    # PROBABILIDADE
    # =========================

    st.markdown("## 🔥 PROBABILIDADE")

    st.caption("8 maiores candidatos")

    for i, numero in enumerate(
        probabilidade,
        start=1
    ):
        st.write(
            f"**#{i} — {numero}**  "
            f"Score {pontuacao[numero]:.1f}"
        )

    # =========================
    # MARCAÇÕES
    # =========================

    st.markdown("## 🎯 MARCAÇÕES")

    st.write(
        " • ".join(
            str(n)
            for n in marcacoes
        )
    )

    # =========================
    # POSSÍVEIS
    # =========================

    st.markdown("## 🔎 POSSÍVEIS")

    st.write(
        " • ".join(
            str(n)
            for n in possiveis
        )
    )

    # =========================
    # RESUMO
    # =========================

    st.markdown("## 📊 RESUMO DOS 22")

    st.write(
        "🔥 **Probabilidade:** "
        + ", ".join(
            map(str, probabilidade)
        )
    )

    st.write(
        "🎯 **Marcações:** "
        + ", ".join(
            map(str, marcacoes)
        )
    )

    st.write(
        "🔎 **Possíveis:** "
        + ", ".join(
            map(str, possiveis)
        )
    )

    # =========================
    # VIZINHOS DO ÚLTIMO
    # =========================

    st.markdown("## 🎰 VIZINHOS DO ÚLTIMO")

    esquerda = [
        ROULETA[
            (posicao - i) % len(ROULETA)
        ]
        for i in range(1, 4)
    ]

    direita = [
        ROULETA[
            (posicao + i) % len(ROULETA)
        ]
        for i in range(1, 4)
    ]

    st.write(f"Último: **{ultimo}**")

    st.write(
        "⬅️ Esquerda: "
        + " • ".join(
            map(str, esquerda)
        )
    )

    st.write(
        "➡️ Direita: "
        + " • ".join(
            map(str, direita)
        )
    )

    st.divider()

    st.caption(
        "ROBÔ SGU — análise estatística. "
        "Não há garantia de previsão do próximo resultado."
    )
