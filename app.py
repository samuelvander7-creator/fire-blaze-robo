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
# FONTE COMPACTA
# ============================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 12px !important;
}

p, label, span, div {
    font-size: 12px !important;
}

h1 {
    font-size: 23px !important;
    margin: 3px 0 7px 0 !important;
}

h2 {
    font-size: 17px !important;
}

h3 {
    font-size: 14px !important;
}

.stButton button {
    font-size: 12px !important;
    min-height: 34px !important;
    padding: 2px 5px !important;
}

.stNumberInput input,
textarea {
    font-size: 12px !important;
}

.marcado {
    display: inline-block;
    padding: 5px 7px;
    margin: 2px;
    border-radius: 5px;
    border: 1px solid #777;
    font-weight: bold;
}

.centro {
    display: inline-block;
    padding: 6px 9px;
    margin: 2px;
    border-radius: 5px;
    border: 2px solid #fff;
    font-weight: bold;
}

.historico {
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# ORDEM FÍSICA DA ROLETA
#
# Sentido utilizado:
# ... 12 - 35 - 3 - 26 - 0 - 32 - 15 - 19 ...
#
# Portanto:
# 0 -> 3, 26, 0, 32, 15
# 3 -> 12, 35, 3, 26, 0
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

if "analisado" not in st.session_state:
    st.session_state.analisado = False

if "numero_selecionado" not in st.session_state:
    st.session_state.numero_selecionado = None


# ============================================================
# FUNÇÕES
# ============================================================

def ler_numeros(texto):

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
            numero = int(item)

            if 0 <= numero <= 36:
                numeros.append(numero)

        except ValueError:
            pass

    return numeros


def sequencia_5(numero):
    """
    Retorna:
    2 números de um lado
    + número central
    + 2 números do outro lado.

    Exemplo:

    0 -> 3, 26, 0, 32, 15
    3 -> 12, 35, 3, 26, 0
    """

    pos = POSICAO[numero]

    # Na apresentação queremos:
    # posição -2, posição -1, centro,
    # posição +1, posição +2
    #
    # Como a lista começa em 0,32,15...,
    # isso produz:
    #
    # 0 -> 3,26,0,32,15

    esquerda_2 = RODA[
        (pos - 2) % 37
    ]

    esquerda_1 = RODA[
        (pos - 1) % 37
    ]

    direita_1 = RODA[
        (pos + 1) % 37
    ]

    direita_2 = RODA[
        (pos + 2) % 37
    ]

    return [
        esquerda_2,
        esquerda_1,
        numero,
        direita_1,
        direita_2
    ]


def vizinhos_22(numero):
    """
    11 posições de cada lado do número.
    """

    pos = POSICAO[numero]

    resultado = []

    for distancia in range(1, 12):

        resultado.append(
            RODA[
                (pos - distancia) % 37
            ]
        )

    for distancia in range(1, 12):

        resultado.append(
            RODA[
                (pos + distancia) % 37
            ]
        )

    return resultado


def distancia_roda(a, b):

    pa = POSICAO[a]
    pb = POSICAO[b]

    distancia = abs(pa - pb)

    return min(
        distancia,
        37 - distancia
    )


def atraso(numero, historico):

    for i, resultado in enumerate(
        reversed(historico)
    ):

        if resultado == numero:
            return i

    return len(historico)


# ============================================================
# ANÁLISE MATEMÁTICA
# ============================================================

def analisar_22(
    historico,
    numero_central
):

    janela = historico[-110:]

    candidatos = vizinhos_22(
        numero_central
    )

    frequencia = Counter(janela)

    resultados = []

    for numero in candidatos:

        score = 0.0
        motivos = []

        # ----------------------------------------------------
        # FREQUÊNCIA
        # ----------------------------------------------------

        freq = frequencia[numero]

        score += freq * 2

        if freq > 0:
            motivos.append(
                f"freq. {freq}"
            )

        # ----------------------------------------------------
        # ATRASO
        # ----------------------------------------------------

        atraso_numero = atraso(
            numero,
            janela
        )

        if atraso_numero >= 8:

            score += min(
                atraso_numero * 0.3,
                8
            )

            motivos.append(
                f"atraso {atraso_numero}"
            )

        # ----------------------------------------------------
        # DISTÂNCIA DO CENTRAL
        # ----------------------------------------------------

        distancia = distancia_roda(
            numero,
            numero_central
        )

        # Quanto mais perto do central,
        # maior a prioridade.

        score += max(
            0,
            12 - distancia
        ) * 0.5

        # ----------------------------------------------------
        # RECÊNCIA
        # ----------------------------------------------------

        freq30 = Counter(
            janela[-30:]
        )[numero]

        score += freq30 * 2.5

        if freq30:
            motivos.append(
                f"últimos 30: {freq30}"
            )

        # ----------------------------------------------------
        # ÚLTIMOS 10
        # ----------------------------------------------------

        freq10 = Counter(
            janela[-10:]
        )[numero]

        score += freq10 * 3

        # ----------------------------------------------------
        # RELAÇÃO COM O CENTRAL
        # ----------------------------------------------------

        if numero != numero_central:

            d = distancia_roda(
                numero,
                numero_central
            )

            if d <= 2:

                score += 4

                motivos.append(
                    "vizinho direto"
                )

            elif d <= 4:

                score += 2

        # ----------------------------------------------------
        # RELAÇÃO COM RESULTADOS RECENTES
        # ----------------------------------------------------

        proximidade = 0

        for resultado in janela[-20:]:

            d = distancia_roda(
                numero,
                resultado
            )

            if d == 1:
                proximidade += 2

            elif d == 2:
                proximidade += 1

        score += proximidade * 0.8

        if proximidade:

            motivos.append(
                "proximidade recente"
            )

        # ----------------------------------------------------
        # REPETIÇÕES
        # ----------------------------------------------------

        if freq >= 3:

            score += 2

            motivos.append(
                "repetição"
            )

        resultados.append({
            "numero": numero,
            "score": round(
                score,
                2
            ),
            "frequencia": freq,
            "atraso": atraso_numero,
            "motivos": motivos
        })

    # Ordena pela pontuação
    resultados.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultados


# ============================================================
# TÍTULO
# ============================================================

st.title("🎯 ROBÔ SGU")

st.caption(
    "Marcação automática pela posição física da roleta"
)


# ============================================================
# 110 RESULTADOS
# ============================================================

st.subheader(
    "📥 110 RESULTADOS"
)

texto = st.text_area(
    "Cole os 110 resultados",
    height=100,
    placeholder="Ex.: 21 31 19 12 13..."
)

if st.button(
    "📊 ANALISAR 110",
    use_container_width=True
):

    numeros = ler_numeros(
        texto
    )

    if len(numeros) != 110:

        st.error(
            f"Foram encontrados {len(numeros)} números. "
            "Cole exatamente 110."
        )

    else:

        st.session_state.historico = (
            numeros.copy()
        )

        st.session_state.analisado = True

        # O último número é o centro inicial
        st.session_state.numero_selecionado = (
            numeros[-1]
        )

        st.success(
            "✅ 110 resultados carregados."
        )

        st.rerun()


# ============================================================
# SELEÇÃO DO NÚMERO
# ============================================================

if st.session_state.analisado:

    st.divider()

    st.subheader(
        "🎯 CLIQUE NO NÚMERO"
    )

    st.caption(
        "Ao selecionar um número, os 2 vizinhos de cada lado "
        "são marcados automaticamente."
    )

    # --------------------------------------------------------
    # BOTÕES 0–36
    # --------------------------------------------------------

    for inicio in range(
        0,
        37,
        7
    ):

        colunas = st.columns(7)

        for i in range(7):

            numero = inicio + i

            if numero > 36:
                continue

            with colunas[i]:

                if st.button(
                    str(numero),
                    key=f"numero_{numero}",
                    use_container_width=True
                ):

                    st.session_state.numero_selecionado = (
                        numero
                    )

                    st.rerun()


# ============================================================
# MARCAÇÃO AUTOMÁTICA DOS 5
# ============================================================

if (
    st.session_state.analisado
    and
    st.session_state.numero_selecionado is not None
):

    numero = (
        st.session_state.numero_selecionado
    )

    st.divider()

    st.subheader(
        f"🎯 MARCAÇÃO DO {numero}"
    )

    sequencia = sequencia_5(
        numero
    )

    html = ""

    for n in sequencia:

        if n == numero:

            html += (
                f'<span class="centro">'
                f'🎯 {n}'
                f'</span>'
            )

        else:

            html += (
                f'<span class="marcado">'
                f'{n}'
                f'</span>'
            )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    st.write(
        "Sequência: "
        + " • ".join(
            str(n)
            for n in sequencia
        )
    )

    # ========================================================
    # 22 CANDIDATOS
    # ========================================================

    analise = analisar_22(
        st.session_state.historico,
        numero
    )

    st.subheader(
        "🧮 22 CANDIDATOS"
    )

    st.caption(
        "Os 22 são definidos pela posição física na roda "
        "e depois ordenados pela análise do histórico."
    )

    html = ""

    for item in analise:

        html += (
            '<span class="marcado">'
            f'{item["numero"]:02d}'
            '</span>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    # ========================================================
    # GRUPOS
    # ========================================================

    st.markdown(
        "### 🔥 8 PRINCIPAIS"
    )

    st.write(
        " • ".join(
            str(x["numero"])
            for x in analise[:8]
        )
    )

    st.markdown(
        "### 🎯 7 MARCAÇÕES"
    )

    st.write(
        " • ".join(
            str(x["numero"])
            for x in analise[8:15]
        )
    )

    st.markdown(
        "### 🔎 7 POSSÍVEIS"
    )

    st.write(
        " • ".join(
            str(x["numero"])
            for x in analise[15:22]
        )
    )

    # ========================================================
    # DETALHES
    # ========================================================

    with st.expander(
        "🧠 Análise matemática"
    ):

        for pos, item in enumerate(
            analise,
            1
        ):

            motivos = ", ".join(
                item["motivos"]
            )

            st.write(
                f"**{pos:02d}. {item['numero']:02d}** "
                f"• força {item['score']} "
                f"• freq. {item['frequencia']} "
                f"• atraso {item['atraso']}"
            )

            if motivos:

                st.caption(
                    motivos
                )


# ============================================================
# NOVO RESULTADO
# ============================================================

if st.session_state.analisado:

    st.divider()

    st.subheader(
        "🎰 NOVO RESULTADO"
    )

    novo = st.number_input(
        "Número que acabou de sair",
        min_value=0,
        max_value=36,
        value=0,
        step=1,
        key="novo_numero"
    )

    if st.button(
        "➕ ADICIONAR RESULTADO",
        use_container_width=True
    ):

        # Adiciona ao histórico infinito
        st.session_state.historico.append(
            int(novo)
        )

        # Automaticamente o novo resultado
        # vira o centro da próxima análise
        st.session_state.numero_selecionado = (
            int(novo)
        )

        st.rerun()


# ============================================================
# HISTÓRICO
# ============================================================

if st.session_state.analisado:

    st.divider()

    st.subheader(
        f"📜 HISTÓRICO — "
        f"{len(st.session_state.historico)} RESULTADOS"
    )

    historico = (
        st.session_state.historico
    )

    # Últimos 110 usados na análise
    janela = historico[-110:]

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
        "O histórico completo continua acumulado. "
        "A análise matemática usa os 110 resultados mais recentes."
    )


# ============================================================
# AVISO
# ============================================================

st.divider()

st.caption(
    "⚠️ A marcação representa a posição física dos números "
    "na roda. O ranking é estatístico e não garante o próximo giro."
)
