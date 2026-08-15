import streamlit as st
from collections import Counter

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

# ============================================================
# INTERFACE COMPACTA
# ============================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 12px !important;
}

p, label, span {
    font-size: 12px !important;
}

h1 {
    font-size: 22px !important;
    margin: 2px 0 6px 0 !important;
}

h2 {
    font-size: 16px !important;
    margin: 5px 0 !important;
}

h3 {
    font-size: 14px !important;
    margin: 4px 0 !important;
}

.stButton button {
    font-size: 12px !important;
    min-height: 34px !important;
}

textarea,
input {
    font-size: 12px !important;
}

.resultado {
    display: inline-block;
    padding: 4px 7px;
    margin: 2px;
    border: 1px solid #777;
    border-radius: 5px;
    font-weight: bold;
}

.central {
    display: inline-block;
    padding: 5px 8px;
    margin: 2px;
    border: 2px solid #777;
    border-radius: 5px;
    font-weight: bold;
}

.caixa {
    padding: 7px;
    border: 1px solid #777;
    border-radius: 7px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# ORDEM FÍSICA DA ROLETA
# ============================================================

RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

POSICAO = {
    numero: i
    for i, numero in enumerate(RODA)
}


# ============================================================
# MEMÓRIA
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "iniciado" not in st.session_state:
    st.session_state.iniciado = False

if "ultimo" not in st.session_state:
    st.session_state.ultimo = None


# ============================================================
# LEITURA DOS RESULTADOS
# ============================================================

def extrair_numeros(texto):

    texto = (
        texto
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
        .replace("\t", " ")
    )

    numeros = []

    for item in texto.split():

        try:
            n = int(item)

            if 0 <= n <= 36:
                numeros.append(n)

        except ValueError:
            pass

    return numeros


# ============================================================
# DISTÂNCIA NA RODA
# ============================================================

def distancia_roda(a, b):

    a = POSICAO[a]
    b = POSICAO[b]

    d = abs(a - b)

    return min(d, 37 - d)


# ============================================================
# MARCAÇÃO AUTOMÁTICA
#
# 2 de um lado + centro + 2 do outro
#
# 0 -> 3 26 0 32 15
# 3 -> 12 35 3 26 0
# ============================================================

def marcacao_5(numero):

    pos = POSICAO[numero]

    return [
        RODA[(pos - 2) % 37],
        RODA[(pos - 1) % 37],
        numero,
        RODA[(pos + 1) % 37],
        RODA[(pos + 2) % 37]
    ]


# ============================================================
# 22 POSIÇÕES
#
# 11 de cada lado do número central.
# O centro não entra nos 22.
# ============================================================

def candidatos_22(numero):

    pos = POSICAO[numero]

    esquerda = [
        RODA[(pos - i) % 37]
        for i in range(1, 12)
    ]

    direita = [
        RODA[(pos + i) % 37]
        for i in range(1, 12)
    ]

    return esquerda + direita


# ============================================================
# ATRASO
# ============================================================

def calcular_atraso(numero, historico):

    for distancia, valor in enumerate(
        reversed(historico)
    ):

        if valor == numero:
            return distancia

    return len(historico)


# ============================================================
# ANÁLISE MATEMÁTICA
# ============================================================

def analisar_22(historico, centro):

    janela = historico[-500:]

    candidatos = candidatos_22(centro)

    freq_total = Counter(janela)
    freq_110 = Counter(janela[-110:])
    freq_50 = Counter(janela[-50:])
    freq_30 = Counter(janela[-30:])
    freq_10 = Counter(janela[-10:])

    resultado = []

    for numero in candidatos:

        score = 0.0
        motivos = []

        # ----------------------------------------------------
        # FREQUÊNCIA
        # ----------------------------------------------------

        score += freq_total[numero] * 0.7
        score += freq_110[numero] * 1.0
        score += freq_50[numero] * 1.3
        score += freq_30[numero] * 1.7
        score += freq_10[numero] * 2.0

        if freq_30[numero] > 0:
            motivos.append("frequência recente")

        # ----------------------------------------------------
        # ATRASO
        # ----------------------------------------------------

        atraso = calcular_atraso(
            numero,
            janela
        )

        if atraso >= 8:

            score += min(
                atraso * 0.15,
                5
            )

            motivos.append("atraso")

        # ----------------------------------------------------
        # DISTÂNCIA DO CENTRO
        # ----------------------------------------------------

        distancia = distancia_roda(
            numero,
            centro
        )

        score += max(
            0,
            11 - distancia
        ) * 0.35

        if distancia <= 2:
            motivos.append("vizinho próximo")

        # ----------------------------------------------------
        # PROXIMIDADE NOS ÚLTIMOS 20
        # ----------------------------------------------------

        proximidade = 0

        for r in janela[-20:]:

            d = distancia_roda(
                numero,
                r
            )

            if d == 1:
                proximidade += 2

            elif d == 2:
                proximidade += 1

        if proximidade:

            score += proximidade * 0.5
            motivos.append("proximidade recente")

        # ----------------------------------------------------
        # REPETIÇÃO
        # ----------------------------------------------------

        if freq_110[numero] >= 3:

            score += 1.5
            motivos.append("repetição")

        # ----------------------------------------------------
        # PRIMO
        # ----------------------------------------------------

        primos = {
            2, 3, 5, 7, 11, 13,
            17, 19, 23, 29, 31
        }

        if numero in primos:
            score += 0.5

        # ----------------------------------------------------
        # FIBONACCI
        # ----------------------------------------------------

        fibonacci = {
            0, 1, 2, 3, 5,
            8, 13, 21, 34
        }

        if numero in fibonacci:
            score += 0.5

        # ----------------------------------------------------
        # PARIDADE
        # ----------------------------------------------------

        if numero != 0:

            pares = sum(
                n != 0 and n % 2 == 0
                for n in janela[-30:]
            )

            impares = sum(
                n != 0 and n % 2 != 0
                for n in janela[-30:]
            )

            if pares > impares and numero % 2 == 0:
                score += 0.5

            elif impares > pares and numero % 2 != 0:
                score += 0.5

        # ----------------------------------------------------
        # MÚLTIPLOS
        # ----------------------------------------------------

        if numero != 0:

            quantidade = sum(
                numero % d == 0
                for d in [2, 3, 4, 5, 6, 9]
            )

            score += quantidade * 0.15

        resultado.append({
            "numero": numero,
            "score": round(score, 2),
            "frequencia": freq_110[numero],
            "atraso": atraso,
            "distancia": distancia,
            "motivos": motivos
        })

    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    resultado.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultado


# ============================================================
# TÍTULO
# ============================================================

st.title("🎯 ROBÔ SGU")

st.caption(
    "Análise física da roda + histórico estatístico"
)


# ============================================================
# BASE INICIAL — ATÉ 500
# ============================================================

st.subheader("📥 Histórico inicial")

texto = st.text_area(
    "Cole os resultados da roleta",
    height=120,
    placeholder=(
        "Cole até 500 resultados aqui..."
    )
)

if st.button(
    "📊 CARREGAR HISTÓRICO",
    use_container_width=True
):

    numeros = extrair_numeros(texto)

    if len(numeros) < 1:

        st.error(
            "Nenhum resultado válido encontrado."
        )

    elif len(numeros) > 500:

        st.error(
            "O máximo inicial é 500 resultados."
        )

    else:

        st.session_state.historico = (
            numeros.copy()
        )

        st.session_state.ultimo = (
            numeros[-1]
        )

        st.session_state.iniciado = True

        st.rerun()


# ============================================================
# SISTEMA ATIVO
# ============================================================

if st.session_state.iniciado:

    historico = st.session_state.historico
    ultimo = historico[-1]

    st.divider()

    # ========================================================
    # RESULTADO ATUAL
    # ========================================================

    st.subheader(
        f"🎯 RESULTADO ATUAL: {ultimo}"
    )

    # ========================================================
    # MARCAÇÃO AUTOMÁTICA DOS 5
    # ========================================================

    marcacao = marcacao_5(
        ultimo
    )

    st.markdown(
        "### 🔥 Marcação automática"
    )

    html = ""

    for n in marcacao:

        if n == ultimo:

            html += (
                f'<span class="central">'
                f'🎯 {n}'
                f'</span>'
            )

        else:

            html += (
                f'<span class="resultado">'
                f'{n}'
                f'</span>'
            )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    st.caption(
        "2 vizinhos de cada lado + número central"
    )

    # ========================================================
    # 22 CANDIDATOS
    # ========================================================

    analise = analisar_22(
        historico,
        ultimo
    )

    st.markdown(
        "### 🧮 22 candidatos"
    )

    html = ""

    for item in analise:

        html += (
            f'<span class="resultado">'
            f'{item["numero"]:02d}'
            f'</span>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    # ========================================================
    # GRUPOS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 🔥 8 principais"
        )

        st.write(
            " • ".join(
                str(x["numero"])
                for x in analise[:8]
            )
        )

    with col2:

        st.markdown(
            "### 🎯 7 marcações"
        )

        st.write(
            " • ".join(
                str(x["numero"])
                for x in analise[8:15]
            )
        )

    st.markdown(
        "### 🔎 7 possíveis"
    )

    st.write(
        " • ".join(
            str(x["numero"])
            for x in analise[15:22]
        )
    )

    # ========================================================
    # NOVO GIRO
    # ========================================================

    st.divider()

    st.subheader(
        "🎰 Próximo resultado"
    )

    novo = st.number_input(
        "Digite somente o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )

    if st.button(
        "➕ REGISTRAR RESULTADO",
        use_container_width=True
    ):

        st.session_state.historico.append(
            int(novo)
        )

        st.session_state.ultimo = int(novo)

        st.rerun()

    # ========================================================
    # ANÁLISE DETALHADA
    # ========================================================

    with st.expander(
        "🧠 Ver análise matemática"
    ):

        for i, item in enumerate(
            analise,
            1
        ):

            motivos = ", ".join(
                item["motivos"]
            )

            st.write(
                f"**{i:02d}. {item['numero']:02d}** "
                f"| força {item['score']} "
                f"| freq. {item['frequencia']} "
                f"| atraso {item['atraso']} "
                f"| distância {item['distancia']}"
            )

            if motivos:
                st.caption(motivos)

    # ========================================================
    # HISTÓRICO CONTÍNUO
    # ========================================================

    st.divider()

    st.subheader(
        f"📜 Histórico: {len(historico)} resultados"
    )

    # Mostra os 500 mais recentes
    janela = historico[-500:]

    for i in range(
        0,
        len(janela),
        15
    ):

        linha = janela[i:i + 15]

        st.code(
            " ".join(
                f"{n:02d}"
                for n in linha
            ),
            language=None
        )

    st.caption(
        "O histórico continua crescendo automaticamente. "
        "Para a análise, são consideradas as 500 rodadas mais recentes."
    )

else:

    st.info(
        "Cole os resultados iniciais para começar."
    )


# ============================================================
# AVISO
# ============================================================

st.divider()

st.caption(
    "⚠️ Estatística e padrões da roda não garantem o próximo "
    "resultado em uma roleta aleatória."
            )
