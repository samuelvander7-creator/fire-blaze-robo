import streamlit as st
from collections import Counter
import math

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
    margin: 4px 0 8px 0 !important;
}

h2 {
    font-size: 17px !important;
    margin: 6px 0 !important;
}

h3 {
    font-size: 14px !important;
    margin: 5px 0 !important;
}

.stButton button {
    font-size: 12px !important;
    min-height: 34px !important;
    padding: 2px 6px !important;
}

.stTextInput input,
.stNumberInput input,
textarea {
    font-size: 12px !important;
}

[data-testid="stMetricValue"] {
    font-size: 16px !important;
}

.candidato {
    display: inline-block;
    padding: 3px 6px;
    margin: 2px;
    border: 1px solid #777;
    border-radius: 5px;
    font-size: 12px !important;
    font-weight: bold;
}

.caixa {
    padding: 6px;
    border: 1px solid #555;
    border-radius: 7px;
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# ROLETA EUROPEIA
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

PRIMOS = {
    2, 3, 5, 7, 11, 13, 17,
    19, 23, 29, 31
}

FIBONACCI = {
    0, 1, 2, 3, 5, 8, 13, 21, 34
}

VERMELHOS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}


# ============================================================
# MEMÓRIA
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "direcao" not in st.session_state:
    st.session_state.direcao = None

if "analisado" not in st.session_state:
    st.session_state.analisado = False


# ============================================================
# FUNÇÕES
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
            numero = int(item)

            if 0 <= numero <= 36:
                numeros.append(numero)

        except ValueError:
            pass

    return numeros


def distancia_roda(a, b):

    pa = POSICAO[a]
    pb = POSICAO[b]

    distancia = abs(pa - pb)

    return min(
        distancia,
        37 - distancia
    )


def sequencia_direcional(
    numero,
    direcao,
    quantidade=22
):
    """
    Retorna os 22 números seguindo
    somente a direção selecionada.
    """

    pos = POSICAO[numero]

    if direcao == "ESQUERDA":
        passo = -1
    else:
        passo = 1

    resultado = []

    for i in range(
        1,
        quantidade + 1
    ):

        resultado.append(
            RODA[
                (pos + passo * i) % 37
            ]
        )

    return resultado


def atraso(
    numero,
    historico
):

    for i, resultado in enumerate(
        reversed(historico)
    ):

        if resultado == numero:
            return i

    return len(historico)


def faixa(numero):

    if numero <= 9:
        return "0-9"

    if numero <= 19:
        return "10-19"

    if numero <= 29:
        return "20-29"

    return "30-36"


def setor(numero):

    voisins = {
        0, 2, 3, 4, 7, 12,
        15, 18, 19, 21, 22,
        25, 26, 28, 29, 32,
        35
    }

    tiers = {
        5, 8, 10, 11, 13,
        16, 23, 24, 27,
        30, 33, 34, 36
    }

    orphelins = {
        1, 6, 9, 14,
        17, 20, 31
    }

    if numero in voisins:
        return "VOISINS"

    if numero in tiers:
        return "TIERS"

    if numero in orphelins:
        return "ORPHELINS"

    return "OUTRO"


def cor(numero):

    if numero == 0:
        return "ZERO"

    if numero in VERMELHOS:
        return "VERMELHO"

    return "PRETO"


def score_numero(
    numero,
    historico,
    ultimo,
    direcao
):

    """
    Calcula uma pontuação estatística.
    Não representa probabilidade matemática real.
    """

    if not historico:
        return 0.0, []

    janela110 = historico[-110:]
    janela50 = historico[-50:]
    janela30 = historico[-30:]
    janela20 = historico[-20:]
    janela10 = historico[-10:]

    f110 = Counter(janela110)
    f50 = Counter(janela50)
    f30 = Counter(janela30)
    f20 = Counter(janela20)
    f10 = Counter(janela10)

    score = 0.0
    motivos = []

    # --------------------------------------------------------
    # FREQUÊNCIA
    # --------------------------------------------------------

    score += f110[numero] * 1.0
    score += f50[numero] * 1.5
    score += f30[numero] * 2.0
    score += f20[numero] * 2.5
    score += f10[numero] * 3.0

    if f30[numero] > 0:
        motivos.append("frequência recente")

    # --------------------------------------------------------
    # ATRASO
    # --------------------------------------------------------

    atraso_numero = atraso(
        numero,
        janela110
    )

    if atraso_numero >= 8:

        score += min(
            atraso_numero * 0.20,
            7
        )

        motivos.append("atraso")

    # --------------------------------------------------------
    # DISTÂNCIA DO ÚLTIMO
    # --------------------------------------------------------

    distancia = distancia_roda(
        ultimo,
        numero
    )

    score += max(
        0,
        10 - distancia
    ) * 0.6

    if distancia <= 3:
        motivos.append("proximidade na roda")

    # --------------------------------------------------------
    # DIREÇÃO
    # --------------------------------------------------------

    direcional = sequencia_direcional(
        ultimo,
        direcao,
        22
    )

    if numero in direcional:

        posicao_direcional = (
            direcional.index(numero) + 1
        )

        # Quanto mais próximo do último,
        # maior a influência direcional.
        score += max(
            0,
            12 - posicao_direcional
        ) * 0.8

        motivos.append(
            f"posição {posicao_direcional} na direção"
        )

    # --------------------------------------------------------
    # SEQUÊNCIA DIRECIONAL NO HISTÓRICO
    # --------------------------------------------------------

    if len(janela110) >= 2:

        acertos_direcionais = 0

        for i in range(
            1,
            len(janela110)
        ):

            anterior = janela110[i - 1]
            atual = janela110[i]

            seq = sequencia_direcional(
                anterior,
                direcao,
                22
            )

            if atual in seq:

                distancia_seq = (
                    seq.index(atual) + 1
                )

                acertos_direcionais += max(
                    0,
                    12 - distancia_seq
                )

        # Normalização
        score += (
            acertos_direcionais / 110
        ) * 5

        if acertos_direcionais > 0:
            motivos.append(
                "histórico direcional"
            )

    # --------------------------------------------------------
    # SETOR
    # --------------------------------------------------------

    setor_ultimo = setor(ultimo)
    setor_numero = setor(numero)

    if setor_numero == setor_ultimo:

        score += 1.5

        motivos.append(
            "mesmo setor"
        )

    # --------------------------------------------------------
    # PRIMOS
    # --------------------------------------------------------

    if numero in PRIMOS:

        proporcao = (
            sum(
                n in PRIMOS
                for n in janela30
            )
            / len(janela30)
        )

        score += proporcao * 2

    # --------------------------------------------------------
    # FIBONACCI
    # --------------------------------------------------------

    if numero in FIBONACCI:

        score += 1.5

    # --------------------------------------------------------
    # MÚLTIPLOS
    # --------------------------------------------------------

    quantidade_multiplos = sum(
        numero != 0 and numero % divisor == 0
        for divisor in (
            2, 3, 4, 5, 6, 9
        )
    )

    score += (
        quantidade_multiplos * 0.4
    )

    # --------------------------------------------------------
    # PAR / ÍMPAR
    # --------------------------------------------------------

    if numero != 0:

        pares = sum(
            n != 0 and n % 2 == 0
            for n in janela30
        )

        impares = sum(
            n != 0 and n % 2 != 0
            for n in janela30
        )

        if pares > impares:

            if numero % 2 == 0:
                score += 1
            else:
                score -= 0.5

        elif impares > pares:

            if numero % 2 != 0:
                score += 1
            else:
                score -= 0.5

    # --------------------------------------------------------
    # COR
    # --------------------------------------------------------

    if numero != 0:

        vermelhos = sum(
            n in VERMELHOS
            for n in janela30
        )

        pretos = sum(
            n != 0 and n not in VERMELHOS
            for n in janela30
        )

        if vermelhos > pretos:
            if numero not in VERMELHOS:
                score += 0.5

        elif pretos > vermelhos:
            if numero in VERMELHOS:
                score += 0.5

    # --------------------------------------------------------
    # FAIXA
    # --------------------------------------------------------

    faixa_numero = faixa(numero)

    freq_faixa_total = sum(
        faixa(n) == faixa_numero
        for n in janela110
    )

    freq_faixa_recente = sum(
        faixa(n) == faixa_numero
        for n in janela30
    )

    esperado = (
        freq_faixa_total
        / len(janela110)
        * len(janela30)
    )

    if freq_faixa_recente > esperado:

        score += 1.5

        motivos.append(
            "faixa recente"
        )

    # --------------------------------------------------------
    # RELAÇÃO NUMÉRICA COM O ÚLTIMO
    # --------------------------------------------------------

    diferenca = abs(
        numero - ultimo
    )

    if diferenca in {
        1, 2, 3, 4, 5,
        7, 8, 9, 10,
        12, 13, 17, 18
    }:

        score += 1

        motivos.append(
            "relação numérica"
        )

    # --------------------------------------------------------
    # DISTÂNCIAS DOS ÚLTIMOS RESULTADOS
    # --------------------------------------------------------

    distancias = [
        distancia_roda(
            numero,
            n
        )
        for n in janela10
    ]

    if distancias:

        media = (
            sum(distancias)
            / len(distancias)
        )

        if media <= 8:

            score += 1

            motivos.append(
                "concentração recente"
            )

    return round(
        score,
        3
    ), motivos


def analisar_22(
    historico,
    direcao
):

    if not historico:
        return []

    ultimo = historico[-1]

    # ========================================================
    # AQUI ESTÁ O CRITÉRIO PRINCIPAL:
    # EXATAMENTE 22 POSIÇÕES A PARTIR DA DIREÇÃO ESCOLHIDA
    # ========================================================

    candidatos = sequencia_direcional(
        ultimo,
        direcao,
        22
    )

    resultado = []

    for posicao, numero in enumerate(
        candidatos,
        start=1
    ):

        score, motivos = score_numero(
            numero,
            historico,
            ultimo,
            direcao
        )

        resultado.append({
            "numero": numero,
            "posicao": posicao,
            "score": score,
            "motivos": motivos,
            "frequencia": Counter(
                historico[-110:]
            )[numero],
            "atraso": atraso(
                numero,
                historico[-110:]
            ),
            "setor": setor(numero)
        })

    # ========================================================
    # RANKING
    # ========================================================

    resultado.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultado


# ============================================================
# TÍTULO
# ============================================================

st.title("🤖 ROBÔ SGU")

st.caption(
    "Análise matemática + sequência direcional da roda"
)

# ============================================================
# DIREÇÃO — ESCOLHE UMA VEZ
# ============================================================

st.subheader("🧭 Direção da operação")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "⬅️ ESQUERDA",
        use_container_width=True
    ):

        st.session_state.direcao = "ESQUERDA"

with col2:

    if st.button(
        "➡️ DIREITA",
        use_container_width=True
    ):

        st.session_state.direcao = "DIREITA"


if st.session_state.direcao:

    st.success(
        f"Direção selecionada: "
        f"**{st.session_state.direcao}**"
    )

    st.caption(
        "A direção permanece automática até você escolher a outra."
    )

else:

    st.warning(
        "Selecione ESQUERDA ou DIREITA para começar."
    )


# ============================================================
# 110 RESULTADOS
# ============================================================

st.subheader("📥 110 resultados iniciais")

texto = st.text_area(
    "Cole os 110 resultados",
    height=110,
    placeholder="Ex.: 10 16 36 4 35..."
)

if st.button(
    "📊 ANALISAR 110 RESULTADOS",
    use_container_width=True
):

    numeros = extrair_numeros(
        texto
    )

    if len(numeros) != 110:

        st.error(
            f"Foram encontrados {len(numeros)} resultados. "
            "É necessário exatamente 110."
        )

    elif not st.session_state.direcao:

        st.warning(
            "Escolha primeiro ESQUERDA ou DIREITA."
        )

    else:

        st.session_state.historico = (
            numeros.copy()
        )

        st.session_state.analisado = True

        st.success(
            "✅ Base de 110 resultados carregada."
        )

        st.rerun()


# ============================================================
# NOVO RESULTADO
# ============================================================

if st.session_state.analisado:

    st.divider()

    st.subheader("🎰 Novo resultado")

    col1, col2 = st.columns([2, 1])

    with col1:

        novo = st.number_input(
            "Número que acabou de sair",
            min_value=0,
            max_value=36,
            value=0,
            step=1
        )

    with col2:

        adicionar = st.button(
            "➕ ADICIONAR",
            use_container_width=True
        )

    if adicionar:

        st.session_state.historico.append(
            int(novo)
        )

        st.rerun()


# ============================================================
# ANÁLISE ATUAL
# ============================================================

if (
    st.session_state.analisado
    and st.session_state.historico
    and st.session_state.direcao
):

    historico = (
        st.session_state.historico
    )

    ultimo = historico[-1]

    analise = analisar_22(
        historico,
        st.session_state.direcao
    )

    st.divider()

    st.subheader(
        f"🧮 Análise — último: {ultimo}"
    )

    # ========================================================
    # STATUS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Último",
            ultimo
        )

    with col2:
        st.metric(
            "Histórico",
            len(historico)
        )

    with col3:
        st.metric(
            "Direção",
            st.session_state.direcao
        )

    # ========================================================
    # 22 CANDIDATOS
    # ========================================================

    st.markdown(
        "### 🎯 22 candidatos"
    )

    html = ""

    for item in analise:

        html += (
            '<span class="candidato">'
            f'{item["numero"]:02d}'
            '</span>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    # ========================================================
    # 8 + 7 + 7
    # ========================================================

    st.markdown(
        "### 🔥 Probabilidade — 8"
    )

    st.write(
        " • ".join(
            f'{x["numero"]:02d}'
            for x in analise[:8]
        )
    )

    st.markdown(
        "### 🎯 Marcações — 7"
    )

    st.write(
        " • ".join(
            f'{x["numero"]:02d}'
            for x in analise[8:15]
        )
    )

    st.markdown(
        "### 🔎 Possíveis — 7"
    )

    st.write(
        " • ".join(
            f'{x["numero"]:02d}'
            for x in analise[15:22]
        )
    )

    # ========================================================
    # ORDEM DIRECIONAL
    # ========================================================

    with st.expander(
        f"🧭 Ver sequência na direção {st.session_state.direcao}"
    ):

        st.write(
            " → ".join(
                f'{x:02d}'
                for x in sequencia_direcional(
                    ultimo,
                    st.session_state.direcao,
                    22
                )
            )
        )

    # ========================================================
    # DETALHES
    # ========================================================

    with st.expander(
        "🧠 Ver análise matemática dos 22"
    ):

        for i, item in enumerate(
            analise,
            start=1
        ):

            motivos = item["motivos"]

            if motivos:
                texto_motivos = ", ".join(
                    motivos
                )
            else:
                texto_motivos = "sem sinal específico"

            st.write(
                f"**{i:02d}. {item['numero']:02d}** "
                f"• força {item['score']:.2f} "
                f"• posição direcional {item['posicao']} "
                f"• frequência {item['frequencia']} "
                f"• atraso {item['atraso']}"
            )

            st.caption(
                texto_motivos
            )

    # ========================================================
    # HISTÓRICO
    # ========================================================

    st.divider()

    st.subheader(
        f"📜 Histórico ({len(historico)})"
    )

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
        "A análise utiliza os 110 resultados mais recentes. "
        "O histórico total continua acumulado."
    )

else:

    st.info(
        "Selecione a direção e carregue os 110 resultados."
    )


# ============================================================
# AVISO
# ============================================================

st.divider()

st.caption(
    "⚠️ A direção e os padrões matemáticos são usados "
    "como critérios estatísticos. Eles não garantem "
    "o resultado de uma roleta justa."
)
