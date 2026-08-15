import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="FIRE BLAZE",
    page_icon="🎰",
    layout="centered"
)

st.title("🎰 FIRE BLAZE")
st.subheader("ANALISADOR DE 22 CANDIDATOS")

# ROLETА EUROPEIA
roleta = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

# ==================================================
# 1. COLOCAR OS 110 RESULTADOS
# ==================================================

st.markdown("### 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS")

texto = st.text_area(
    "Últimos 110 resultados",
    height=150,
    placeholder="Cole aqui os 110 números..."
)

# Transformar texto em números
try:
    resultados = [
        int(x)
        for x in texto.replace(",", " ").split()
        if x.strip().isdigit()
    ]
except:
    resultados = []

if resultados:
    st.success(f"✅ {len(resultados)} resultados carregados.")

# ==================================================
# 2. NÚMERO QUE ACABOU DE SAIR
# ==================================================

st.markdown("### 🎰 2. ÚLTIMO NÚMERO")

ultimo = st.number_input(
    "Número que acabou de sair",
    min_value=0,
    max_value=36,
    value=0,
    step=1
)

# ==================================================
# ANÁLISE
# ==================================================

if st.button("🎯 ANALISAR", use_container_width=True):

    if len(resultados) < 110:
        st.warning(
            f"⚠️ Precisamos de 110 resultados. "
            f"Atualmente: {len(resultados)}"
        )

    elif ultimo not in roleta:
        st.error("Número inválido.")

    else:

        # Posição do último número na roda
        posicao = roleta.index(ultimo)

        # ==========================================
        # PEGAR 22 NÚMEROS AO REDOR
        # ==========================================

        candidatos = []

        for i in range(-11, 12):

            if i == 0:
                continue

            numero = roleta[(posicao + i) % len(roleta)]

            if numero not in candidatos:
                candidatos.append(numero)

        # ==========================================
        # FREQUÊNCIA NOS 110 RESULTADOS
        # ==========================================

        frequencia = Counter(resultados)

        # ==========================================
        # PONTUAÇÃO DOS 22 CANDIDATOS
        # ==========================================

        ranking = []

        for numero in candidatos:

            freq = frequencia[numero]

            # frequência simples nos 110 resultados
            score = freq

            ranking.append((numero, score, freq))

        # Ordenar pela pontuação
        ranking.sort(
            key=lambda x: (-x[1], x[0])
        )

        # ==========================================
        # DIVIDIR 22 EM 8 + 7 + 7
        # ==========================================

        probabilidade = ranking[:8]
        marcacoes = ranking[8:15]
        possiveis = ranking[15:22]

        # ==========================================
        # RESULTADO COMPACTO
        # ==========================================

        st.success(f"Último resultado: {ultimo}")

        st.markdown("### 🔥 PROBABILIDADE")
        st.caption("8 maiores frequências nos 110 resultados")

        nums = [str(x[0]) for x in probabilidade]
        st.markdown(
            "**" + "  •  ".join(nums) + "**"
        )

        st.markdown("### 🎯 MARCAÇÕES")
        nums = [str(x[0]) for x in marcacoes]
        st.markdown(
            "**" + "  •  ".join(nums) + "**"
        )

        st.markdown("### 🟢 POSSÍVEIS")
        nums = [str(x[0]) for x in possiveis]
        st.markdown(
            "**" + "  •  ".join(nums) + "**"
        )

        # ==========================================
        # DETALHAMENTO
        # ==========================================

        with st.expander("📊 Ver frequência dos 22 candidatos"):

            for numero, score, freq in ranking:

                st.write(
                    f"**{numero}** — {freq} vezes"
                )

        st.caption(
            "⚠️ Os grupos são um ranking estatístico "
            "dos 110 resultados. Não garantem o próximo giro."
        )
