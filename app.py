import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev
import math

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="ROBÔ RICO",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MAX_HISTORICO = 200
TOTAL_ESCOLHAS = 22

NUMEROS = list(range(37))

# Roleta europeia
RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

POS = {n: i for i, n in enumerate(RODA)}

VERMELHOS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

PRIMOS = {
    2, 3, 5, 7, 11, 13,
    17, 19, 23, 29, 31
}

FIBONACCI = {
    0, 1, 2, 3, 5, 8, 13, 21, 34
}

QUADRADOS = {
    0, 1, 4, 9, 16, 25, 36
}


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(0,90,130,.16), transparent 32%),
        radial-gradient(circle at 90% 10%, rgba(70,0,100,.14), transparent 35%),
        #020810;
    color: #f4f7fb;
}

.block-container {
    max-width: 1500px;
    padding: 18px 18px 35px 18px;
}

/* remove espaços exagerados */
div[data-testid="stVerticalBlock"] {
    gap: .45rem;
}

/* texto */
h1, h2, h3, p {
    color: #f4f7fb;
}

/* =========================================================
   CABEÇALHO
   ========================================================= */

.logo-area {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.logo-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.logo-icon {
    font-size: 54px;
    line-height: 1;
}

.logo-title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1;
}

.logo-title .rico {
    color: #18d85b;
}

.logo-subtitle {
    color: #aab6c7;
    font-size: 17px;
    margin-top: 8px;
}

.direction-card {
    border: 1px solid #26384c;
    background: linear-gradient(145deg,#06131e,#07101a);
    border-radius: 10px;
    padding: 10px 20px;
    min-width: 235px;
    text-align: center;
}

.direction-small {
    color: #d6dce5;
    font-size: 13px;
}

.direction-main {
    color: #16d95a;
    font-size: 25px;
    font-weight: 800;
}

.direction-auto {
    color: #b9c1cc;
    font-size: 12px;
}

/* =========================================================
   CARDS
   ========================================================= */

.metric-card {
    background: linear-gradient(145deg,#071521,#030b13);
    border: 1px solid #26384a;
    border-radius: 10px;
    min-height: 125px;
    padding: 14px;
    text-align: center;
}

.metric-title {
    color: #d4dbe4;
    font-size: 13px;
    text-transform: uppercase;
    margin-bottom: 9px;
}

.metric-value {
    font-size: 38px;
    font-weight: 900;
    line-height: 1.1;
}

.metric-sub {
    color: #d6dce4;
    font-size: 14px;
    margin-top: 6px;
}

.blue {
    color: #168cff;
}

.green {
    color: #19d85b;
}

.purple {
    color: #a24cff;
}

.cyan {
    color: #11c9e8;
}

.orange {
    color: #ffab22;
}

/* =========================================================
   CARD GERAL
   ========================================================= */

.panel {
    background: linear-gradient(145deg,#06131d,#020a11);
    border: 1px solid #26394b;
    border-radius: 10px;
    padding: 15px;
    height: 100%;
}

.panel-title {
    font-size: 17px;
    font-weight: 700;
    color: #dfe7ef;
    margin-bottom: 12px;
}

/* =========================================================
   ESCOLHAS
   ========================================================= */

.choice-panel {
    background: linear-gradient(145deg,#06151f,#031019);
    border: 1px solid #20394a;
    border-radius: 10px;
    padding: 15px;
    min-height: 310px;
}

.choice-panel.high {
    border-color: rgba(20,220,90,.55);
}

.choice-panel.possible {
    border-color: rgba(0,130,255,.55);
}

.choice-panel.mark {
    border-color: rgba(255,170,20,.60);
}

.choice-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 17px;
}

.high-text {
    color: #19df61;
}

.possible-text {
    color: #158cff;
}

.mark-text {
    color: #ffae1b;
}

.choice-number {
    display: inline-flex;
    width: 51px;
    height: 51px;
    margin: 4px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    font-weight: 800;
    color: white;
    background: #020507;
    border: 1px solid #708090;
    box-shadow: inset 0 0 10px rgba(255,255,255,.04);
}

.choice-number.red {
    background: #dc2532;
    border-color: #ff4854;
}

.choice-number.black {
    background: #030506;
    border-color: #8b949e;
}

.choice-number.zero {
    background: #0b9f42;
    border-color: #22d966;
}

.choice-footer {
    margin-top: 17px;
    padding: 9px;
    border-radius: 7px;
    font-size: 12px;
}

.high-footer {
    color: #18d85b;
    border: 1px solid rgba(20,220,90,.35);
}

.possible-footer {
    color: #1996ff;
    border: 1px solid rgba(0,130,255,.35);
}

.mark-footer {
    color: #ffad18;
    border: 1px solid rgba(255,170,20,.35);
}

/* =========================================================
   TOP 5
   ========================================================= */

.top-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #263442;
    padding: 9px 2px;
}

.top-number {
    font-size: 18px;
    font-weight: 800;
}

.top-score {
    color: #17d85b;
    font-weight: 800;
}

/* =========================================================
   BARRAS
   ========================================================= */

.progress-bg {
    height: 10px;
    background: #142330;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 8px;
}

.progress-blue {
    height: 100%;
    background: #168cff;
    border-radius: 20px;
}

.progress-green {
    height: 100%;
    background: #17d85b;
    border-radius: 20px;
}

.progress-purple {
    height: 100%;
    background: #9d43ef;
    border-radius: 20px;
}

/* =========================================================
   NÚMEROS
   ========================================================= */

.ball {
    display: inline-flex;
    width: 30px;
    height: 30px;
    margin: 3px;
    border-radius: 50%;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    font-weight: 800;
}

.ball-red {
    background: #df2733;
}

.ball-black {
    background: #030405;
    border: 1px solid #6b7680;
}

.ball-green {
    background: #0aa447;
}

/* =========================================================
   TABELAS / LISTAS
   ========================================================= */

.stat-line {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #182735;
    padding: 8px 2px;
    color: #d8e0e9;
}

.stat-value {
    font-weight: 800;
}

/* =========================================================
   BOTÕES
   ========================================================= */

.stButton > button {
    background: linear-gradient(145deg,#061723,#07111a);
    color: #eef4fa;
    border: 1px solid #294052;
    border-radius: 8px;
    font-weight: 700;
    min-height: 43px;
}

.stButton > button:hover {
    border-color: #20d95c;
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div {
    background-color: #f0f2f6 !important;
    color: #20242a !important;
    border-radius: 9px !important;
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .block-container {
        padding: 10px;
    }

    .logo-title {
        font-size: 32px;
    }

    .logo-icon {
        font-size: 40px;
    }

    .logo-subtitle {
        font-size: 12px;
    }

    .direction-card {
        min-width: 145px;
        padding: 7px;
    }

    .metric-card {
        min-height: 110px;
    }

    .metric-value {
        font-size: 30px;
    }

    .choice-number {
        width: 44px;
        height: 44px;
        font-size: 16px;
        margin: 3px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ESTADO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "sentido" not in st.session_state:
    st.session_state.sentido = "Direita"

if "resultado_analisado" not in st.session_state:
    st.session_state.resultado_analisado = None


# ============================================================
# FUNÇÕES
# ============================================================

def extrair_numeros(texto):
    texto = (
        str(texto)
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
        .replace("\t", " ")
    )

    resultado = []

    for item in texto.split():
        try:
            n = int(item)

            if 0 <= n <= 36:
                resultado.append(n)

        except:
            pass

    return resultado


def cor(n):
    if n == 0:
        return "verde"

    if n in VERMELHOS:
        return "vermelho"

    return "preto"


def cor_nome(n):
    if n == 0:
        return "VERDE"

    if n in VERMELHOS:
        return "VERMELHO"

    return "PRETO"


def paridade(n):
    if n == 0:
        return "Zero"

    return "Par" if n % 2 == 0 else "Ímpar"


def faixa(n):
    if n == 0:
        return "Zero"

    return "1-18" if n <= 18 else "19-36"


def duzia(n):
    if n == 0:
        return "Zero"

    if n <= 12:
        return "1ª Dúzia"

    if n <= 24:
        return "2ª Dúzia"

    return "3ª Dúzia"


def coluna(n):
    if n == 0:
        return "Zero"

    resto = n % 3

    if resto == 1:
        return "1ª Coluna"

    if resto == 2:
        return "2ª Coluna"

    return "3ª Coluna"


def distancia_roda(a, b):
    if a not in POS or b not in POS:
        return 99

    d = abs(POS[a] - POS[b])

    return min(d, 37 - d)


def espelho_roda(n):
    if n not in POS:
        return n

    return RODA[(POS[n] + 18) % 37]


def espelho_numero(n):
    if n == 0:
        return 0

    return 37 - n


def atraso(n, dados):
    for i, x in enumerate(reversed(dados)):
        if x == n:
            return i

    return len(dados)


def criar_transicoes(dados):
    matriz = defaultdict(Counter)

    for i in range(len(dados) - 1):
        atual = dados[i]
        proximo = dados[i + 1]

        matriz[atual][proximo] += 1

    return matriz


def frequencia(n, dados):
    return dados.count(n)


def zscore(n, dados):
    if not dados:
        return 0

    freq = Counter(dados)

    valores = [
        freq[x]
        for x in NUMEROS
    ]

    media = mean(valores)

    desvio = pstdev(valores)

    if desvio == 0:
        return 0

    return (freq[n] - media) / desvio


# ============================================================
# SCORE
# ============================================================

def calcular_score(n, dados, matriz):

    if not dados:
        return 0

    ultimo = dados[-1]

    score = 0

    # --------------------------------------------------------
    # FREQUÊNCIA
    # --------------------------------------------------------

    pesos = {
        10: 3.0,
        20: 2.5,
        37: 2.0,
        50: 1.6,
        100: 1.2,
        150: .8,
        200: .5
    }

    for janela, peso in pesos.items():

        parte = dados[-janela:]

        if parte:
            freq = parte.count(n) / len(parte)

            score += freq * 100 * peso

    # --------------------------------------------------------
    # ATRASO
    # --------------------------------------------------------

    atr = atraso(n, dados)

    if atr > 3:
        score += min(atr * .08, 3)

    # --------------------------------------------------------
    # Z-SCORE
    # --------------------------------------------------------

    z = zscore(n, dados)

    score += z * .8

    # --------------------------------------------------------
    # VIZINHANÇA NA RODA
    # --------------------------------------------------------

    for r in dados[-30:]:

        d = distancia_roda(n, r)

        if d == 1:
            score += .75

        elif d == 2:
            score += .40

        elif d == 3:
            score += .15

    # --------------------------------------------------------
    # TRANSIÇÕES
    # --------------------------------------------------------

    total_transicoes = sum(
        matriz[ultimo].values()
    )

    if total_transicoes > 0:

        ocorrencias = matriz[ultimo][n]

        score += (
            ocorrencias /
            total_transicoes
        ) * 12

    # --------------------------------------------------------
    # ESPELHOS
    # --------------------------------------------------------

    espelho1 = espelho_roda(n)
    espelho2 = espelho_numero(n)

    score += dados.count(espelho1) * .10
    score += dados.count(espelho2) * .07

    # --------------------------------------------------------
    # DIREÇÃO
    # --------------------------------------------------------

    if len(dados) >= 2:

        anterior = dados[-2]
        atual = dados[-1]

        pos_anterior = POS[anterior]
        pos_atual = POS[atual]
        pos_n = POS[n]

        movimento = (
            pos_atual - pos_anterior
        ) % 37

        proximo = (
            pos_n - pos_atual
        ) % 37

        if st.session_state.sentido == "Direita":

            if proximo == 1:
                score += 2.0

            elif proximo == 2:
                score += 1.2

            elif proximo == 3:
                score += .7

        else:

            if proximo == 36:
                score += 2.0

            elif proximo == 35:
                score += 1.2

            elif proximo == 34:
                score += .7

        # continuidade do movimento
        if movimento == proximo:
            score += 1.3

    # --------------------------------------------------------
    # MATEMÁTICA
    # --------------------------------------------------------

    if n in PRIMOS:
        score += .30

    if n in FIBONACCI:
        score += .25

    if n in QUADRADOS:
        score += .15

    if n != 0:

        if n % 2 == 0:
            score += .05

        if n % 3 == 0:
            score += .06

        if n % 4 == 0:
            score += .04

        if n % 5 == 0:
            score += .04

        if n % 7 == 0:
            score += .04

        if n % 9 == 0:
            score += .04

    # --------------------------------------------------------
    # CLASSIFICAÇÕES RECENTES
    # --------------------------------------------------------

    recentes = dados[-30:]

    if recentes:

        mesma_cor = sum(
            cor(x) == cor(n)
            for x in recentes
        )

        mesma_paridade = sum(
            paridade(x) == paridade(n)
            for x in recentes
            if x != 0
        )

        mesma_duzia = sum(
            duzia(x) == duzia(n)
            for x in recentes
            if x != 0
        )

        mesma_coluna = sum(
            coluna(x) == coluna(n)
            for x in recentes
            if x != 0
        )

        score += mesma_cor * .025
        score += mesma_paridade * .018
        score += mesma_duzia * .018
        score += mesma_coluna * .018

    return score


# ============================================================
# ANALISAR
# ============================================================

def analisar(dados):

    dados = dados[-MAX_HISTORICO:]

    if not dados:
        return []

    matriz = criar_transicoes(dados)

    ranking = []

    for n in NUMEROS:

        score = calcular_score(
            n,
            dados,
            matriz
        )

        ranking.append({
            "numero": n,
            "score": score,
            "frequencia": frequencia(n, dados),
            "atraso": atraso(n, dados),
            "zscore": zscore(n, dados),
            "espelho_roda": espelho_roda(n),
            "espelho_numero": espelho_numero(n)
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking


# ============================================================
# 22 ESCOLHAS
# ============================================================

def selecionar_22(ranking):

    # 8 mais fortes
    altas = [
        x["numero"]
        for x in ranking[:8]
    ]

    # próximos 7
    possiveis = [
        x["numero"]
        for x in ranking[8:15]
    ]

    # próximos 7
    marcacao = [
        x["numero"]
        for x in ranking[15:22]
    ]

    return altas, possiveis, marcacao


# ============================================================
# SCORE NORMALIZADO
# ============================================================

def percentual_score(ranking):

    if not ranking:
        return {}

    maior = ranking[0]["score"]

    menor = ranking[-1]["score"]

    diferenca = maior - menor

    if diferenca <= 0:
        return {
            x["numero"]: 0
            for x in ranking
        }

    resultado = {}

    for x in ranking:

        valor = (
            (x["score"] - menor)
            / diferenca
        ) * 100

        resultado[x["numero"]] = valor

    return resultado


# ============================================================
# BACKTEST
# ============================================================

def backtest(dados):

    if len(dados) < 30:
        return 0, 0, 0

    inicio = max(
        20,
        len(dados) - 100
    )

    acertos = 0
    testes = 0

    for i in range(inicio, len(dados)):

        historico = dados[:i]

        ranking = analisar(historico)

        top22 = {
            x["numero"]
            for x in ranking[:22]
        }

        resultado = dados[i]

        if resultado in top22:
            acertos += 1

        testes += 1

    if testes == 0:
        return 0, 0, 0

    taxa = (
        acertos /
        testes
    ) * 100

    return acertos, testes, taxa


# ============================================================
# HTML DE BOLINHAS
# ============================================================

def bola(n):

    classe = "ball-green"

    if n != 0:

        if n in VERMELHOS:
            classe = "ball-red"

        else:
            classe = "ball-black"

    return (
        f'<span class="ball {classe}">'
        f'{n}'
        f'</span>'
    )


def bolas(lista):

    return "".join(
        bola(n)
        for n in lista
    )


def escolha_bolas(lista):

    html = ""

    for n in lista:

        classe = "zero"

        if n != 0:

            if n in VERMELHOS:
                classe = "red"

            else:
                classe = "black"

        html += (
            f'<span class="choice-number {classe}">'
            f'{n}'
            f'</span>'
        )

    return html


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown("""
<div class="logo-area">

    <div class="logo-left">

        <div class="logo-icon">
            🎯💵
        </div>

        <div>
            <div class="logo-title">
                ROBÔ <span class="rico">RICO</span> 🤑
            </div>

            <div class="logo-subtitle">
                Estatística • Matemática • Roda • Mesa • Transições • Espelhos
            </div>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SENTIDO
# ============================================================

c1, c2 = st.columns([4, 1])

with c1:
    sentido = st.selectbox(
        "Sentido atual",
        ["Direita", "Esquerda", "Automático"],
        index=0
    )

st.session_state.sentido = sentido


# ============================================================
# DADOS
# ============================================================

historico = st.session_state.historico

ranking = analisar(historico)

percentuais = percentual_score(ranking)

if ranking:
    altas, possiveis, marcacao = selecionar_22(ranking)
else:
    altas = []
    possiveis = []
    marcacao = []

ultimo = historico[-1] if historico else 0

acertos, testes, cobertura = backtest(historico)

# total de transições
total_transicoes = max(
    0,
    len(historico) - 1
)


# ============================================================
# INDICADORES SUPERIORES
# ============================================================

m1, m2, m3, m4, m5 = st.columns(5)

with m1:

    if historico:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                Último resultado
            </div>

            <div class="metric-value">
                {ultimo}
            </div>

            <div class="metric-sub">
                {cor_nome(ultimo)}
            </div>

            <div class="metric-sub">
                {paridade(ultimo)} • {faixa(ultimo)} • {duzia(ultimo)}
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Último resultado</div>
            <div class="metric-value">—</div>
            <div class="metric-sub">Aguardando dados</div>
        </div>
        """, unsafe_allow_html=True)


with m2:

    quantidade = len(historico)

    porcentagem_base = (
        quantidade / MAX_HISTORICO
    ) * 100

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            Base analisada
        </div>

        <div class="metric-value blue">
            {quantidade}
        </div>

        <div class="metric-sub">
            últimos resultados
        </div>

        <div class="progress-bg">
            <div class="progress-blue"
                 style="width:{min(porcentagem_base,100)}%">
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)


with m3:

    if testes:
        desempenho = cobertura
    else:
        desempenho = 0

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            Desempenho (22)
        </div>

        <div class="metric-value green">
            {desempenho:.1f}%
        </div>

        <div class="metric-sub">
            Cobertura no backtest
        </div>

        <div class="progress-bg">
            <div class="progress-green"
                 style="width:{min(desempenho,100)}%">
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)


with m4:

    st.markdown("""
    <div class="metric-card">

        <div class="metric-title">
            Escolhas do robô
        </div>

        <div class="metric-value purple">
            22
        </div>

        <div class="metric-sub">
            8 + 7 + 7 números
        </div>

        <div class="progress-bg">
            <div class="progress-purple"
                 style="width:61%">
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)


with m5:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            Transições
        </div>

        <div class="metric-value cyan">
            {total_transicoes:,}
        </div>

        <div class="metric-sub">
            transições analisadas
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ESCOLHAS + TOP 5
# ============================================================

st.markdown("### 🔥 ESCOLHAS DO ROBÔ")

col_escolhas, col_top = st.columns([4, 1])


with col_escolhas:

    a, b, c = st.columns(3)

    with a:

        st.markdown(f"""
        <div class="choice-panel high">

            <div class="choice-title high-text">
                📈 8 NÚMEROS COM TENDÊNCIA ALTA
            </div>

            <div>
                {escolha_bolas(altas)}
            </div>

            <div class="choice-footer high-footer">
                ↗ Maior força estatística no momento
            </div>

        </div>
        """, unsafe_allow_html=True)


    with b:

        st.markdown(f"""
        <div class="choice-panel possible">

            <div class="choice-title possible-text">
                ❓ 7 NÚMEROS COMO POSSÍVEL
            </div>

            <div>
                {escolha_bolas(possiveis)}
            </div>

            <div class="choice-footer possible-footer">
                ⓘ Números com força secundária
            </div>

        </div>
        """, unsafe_allow_html=True)


    with c:

        st.markdown(f"""
        <div class="choice-panel mark">

            <div class="choice-title mark-text">
                🎯 7 NÚMEROS COMO MARCAÇÃO
            </div>

            <div>
                {escolha_bolas(marcacao)}
            </div>

            <div class="choice-footer mark-footer">
                🛡 Números para cobertura e proteção
            </div>

        </div>
        """, unsafe_allow_html=True)


with col_top:

    top5 = ranking[:5]

    html = """
    <div class="panel">

        <div class="panel-title">
            👑 TOP 5 GERAL
        </div>
    """

    for i, item in enumerate(top5, 1):

        n = item["numero"]

        pct = percentuais.get(n, 0)

        html += f"""
        <div class="top-row">

            <span>
                {i}
            </span>

            <span class="top-number">
                {n}
            </span>

            <span class="top-score">
                {pct:.1f}
            </span>

        </div>
        """

    html += """
        <div style="
            margin-top:12px;
            padding:9px;
            border:1px solid #26394b;
            border-radius:7px;
            text-align:center;
            color:#b8c4d0;">
            RANKING CALCULADO PELO ROBÔ
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# ESTATÍSTICAS
# ============================================================

if historico:

    frequencias = [
        historico.count(n)
        for n in NUMEROS
    ]

    atrasos = [
        atraso(n, historico)
        for n in NUMEROS
    ]

    zscores = [
        zscore(n, historico)
        for n in NUMEROS
    ]

    media_freq = mean(frequencias)
    max_freq = max(frequencias)

    media_atraso = mean(atrasos)
    max_atraso = max(atrasos)

    media_z = mean(zscores)

    max_z = max(zscores)

else:

    media_freq = 0
    max_freq = 0
    media_atraso = 0
    max_atraso = 0
    media_z = 0
    max_z = 0


s1, s2, s3, s4, s5 = st.columns(5)


with s1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            📊 Frequência (200)
        </div>

        <div class="metric-sub">
            Média: <b>{media_freq:.2f}</b>
        </div>

        <div class="metric-sub">
            Máx: <b>{max_freq}</b>
        </div>

    </div>
    """, unsafe_allow_html=True)


with s2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            🕘 Atraso médio
        </div>

        <div class="metric-sub">
            Média: <b>{media_atraso:.1f}</b>
        </div>

        <div class="metric-sub">
            Máx: <b>{max_atraso}</b>
        </div>

    </div>
    """, unsafe_allow_html=True)


with s3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            ∑ Z-SCORE MÉDIO
        </div>

        <div class="metric-sub">
            Média: <b>{media_z:.2f}</b>
        </div>

        <div class="metric-sub">
            Máx: <b>{max_z:.2f}</b>
        </div>

    </div>
    """, unsafe_allow_html=True)


with s4:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            🧳 Maior atraso
        </div>

        <div class="metric-value">
            {max_atraso}
        </div>

    </div>
    """, unsafe_allow_html=True)


with s5:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-title">
            🔄 Transições
        </div>

        <div class="metric-value cyan">
            {total_transicoes:,}
        </div>

        <div class="metric-sub">
            transições analisadas
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# RESUMOS
# ============================================================

r1, r2, r3 = st.columns([1, 1, 1])


# ------------------------------------------------------------
# CORES
# ------------------------------------------------------------

with r1:

    if historico:

        vermelhos = sum(
            x in VERMELHOS
            for x in historico
        )

        pretos = sum(
            x != 0 and x not in VERMELHOS
            for x in historico
        )

        verdes = historico.count(0)

        total = len(historico)

        vr = vermelhos / total * 100
        pt = pretos / total * 100
        vd = verdes / total * 100

    else:

        vr = pt = vd = 0

    st.markdown(f"""
    <div class="panel">

        <div class="panel-title">
            RESUMO DE CORES
        </div>

        <div style="font-size:18px; margin-top:20px;">
            🔴 Vermelhos
            <b>{vr:.1f}%</b>
        </div>

        <div style="
            height:14px;
            background:#18222d;
            border-radius:20px;
            margin:8px 0 15px 0;">
            <div style="
                width:{vr}%;
                height:100%;
                background:#e32635;
                border-radius:20px;">
            </div>
        </div>

        <div style="font-size:18px;">
            ⚫ Pretos
            <b>{pt:.1f}%</b>
        </div>

        <div style="
            height:14px;
            background:#18222d;
            border-radius:20px;
            margin:8px 0 15px 0;">
            <div style="
                width:{pt}%;
                height:100%;
                background:#11151a;
                border-radius:20px;">
            </div>
        </div>

        <div style="font-size:18px;">
            🟢 Verdes
            <b>{vd:.1f}%</b>
        </div>

    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# PADRÕES NUMÉRICOS
# ------------------------------------------------------------

with r2:

    if historico:

        qtd_primos = sum(
            x in PRIMOS
            for x in historico
        )

        qtd_fibo = sum(
            x in FIBONACCI
            for x in historico
        )

        qtd_quad = sum(
            x in QUADRADOS
            for x in historico
        )

        qtd_m3 = sum(
            x != 0 and x % 3 == 0
            for x in historico
        )

        qtd_m2 = sum(
            x != 0 and x % 2 == 0
            for x in historico
        )

        soma_digitos_primos = sum(
            sum(
                int(d)
                for d in str(x)
            )
            in PRIMOS
            for x in historico
        )

    else:

        qtd_primos = 0
        qtd_fibo = 0
        qtd_quad = 0
        qtd_m3 = 0
        qtd_m2 = 0
        soma_digitos_primos = 0

    st.markdown(f"""
    <div class="panel">

        <div class="panel-title">
            PADRÕES NUMÉRICOS
        </div>

        <div class="stat-line">
            <span>Primos</span>
            <span class="stat-value green">{qtd_primos}</span>
        </div>

        <div class="stat-line">
            <span>Fibonacci</span>
            <span class="stat-value blue">{qtd_fibo}</span>
        </div>

        <div class="stat-line">
            <span>Quadrados</span>
            <span class="stat-value">{qtd_quad}</span>
        </div>

        <div class="stat-line">
            <span>Múltiplos de 3</span>
            <span class="stat-value orange">{qtd_m3}</span>
        </div>

        <div class="stat-line">
            <span>Múltiplos de 2</span>
            <span class="stat-value orange">{qtd_m2}</span>
        </div>

        <div class="stat-line">
            <span>Soma dos dígitos</span>
            <span class="stat-value cyan">{soma_digitos_primos}</span>
        </div>

    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# ÚLTIMAS JANELAS
# ------------------------------------------------------------

with r3:

    janelas = [10, 20, 37, 50, 100, 150, 200]

    html = """
    <div class="panel">

        <div class="panel-title">
            ÚLTIMAS JANELAS
        </div>
    """

    for janela in janelas:

        if historico:

            parte = historico[-janela:]

            ultimo_janela = (
                parte[-1]
                if parte
                else "—"
            )

        else:

            ultimo_janela = "—"

        html += f"""
        <div class="stat-line">

            <span>
                Últimos {janela}
            </span>

            <span>
                {bola(ultimo_janela)
                if ultimo_janela != "—"
                else "—"}
            </span>

        </div>
        """

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# HISTÓRICO / BACKTEST / DESEMPENHO
# ============================================================

h1, h2, h3 = st.columns([1.25, 1, 1])


with h1:

    st.markdown("""
    <div class="panel">

        <div class="panel-title">
            HISTÓRICO RECENTE
            <span style="font-size:12px;">
                (últimos 20)
            </span>
        </div>

    """, unsafe_allow_html=True)

    if historico:

        st.markdown(
            bolas(historico[-20:]),
            unsafe_allow_html=True
        )

    else:

        st.caption(
            "Nenhum resultado inserido."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with h2:

    st.markdown(f"""
    <div class="panel">

        <div class="panel-title">
            TESTE DE COBERTURA (BACKTEST)
        </div>

        <div style="
            display:flex;
            justify-content:space-around;
            text-align:center;
            margin-top:20px;">

            <div>
                <div>Acertos</div>
                <div style="
                    font-size:27px;
                    color:#18d85b;
                    font-weight:800;">
                    {acertos}
                </div>
            </div>

            <div>
                <div>Testes</div>
                <div style="
                    font-size:27px;
                    color:#168cff;
                    font-weight:800;">
                    {testes}
                </div>
            </div>

            <div>
                <div>Cobertura</div>
                <div style="
                    font-size:27px;
                    color:#ffb21d;
                    font-weight:800;">
                    {cobertura:.1f}%
                </div>
            </div>

        </div>

        <div class="progress-bg">
            <div class="progress-green"
                 style="width:{min(cobertura,100)}%">
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)


with h3:

    erros = max(
        0,
        testes - acertos
    )

    st.markdown(f"""
    <div class="panel">

        <div class="panel-title">
            DETALHES DESEMPENHO (22)
        </div>

        <div style="
            display:flex;
            justify-content:space-around;
            text-align:center;
            margin-top:25px;">

            <div>
                <div>Acertos</div>
                <div style="
                    font-size:28px;
                    color:#18d85b;
                    font-weight:800;">
                    {acertos}
                </div>
            </div>

            <div>
                <div>Erros</div>
                <div style="
                    font-size:28px;
                    color:#ef3542;
                    font-weight:800;">
                    {erros}
                </div>
            </div>

            <div>
                <div>Total</div>
                <div style="
                    font-size:28px;
                    font-weight:800;">
                    {testes}
                </div>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ENTRADA DE NOVO RESULTADO
# ============================================================

st.markdown("---")

novo1, novo2, novo3 = st.columns([1, 1.5, 1.2])


with novo1:

    novo_resultado = st.number_input(
        "NOVO RESULTADO",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )


with novo2:

    if st.button(
        "🟢 ADICIONAR & ATUALIZAR",
        use_container_width=True
    ):

        st.session_state.historico.append(
            int(novo_resultado)
        )

        st.session_state.historico = (
            st.session_state.historico[
                -MAX_HISTORICO:
            ]
        )

        st.rerun()


with novo3:

    if st.button(
        "🗑 LIMPAR HISTÓRICO",
        use_container_width=True
    ):

        st.session_state.historico = []

        st.rerun()


# ============================================================
# IMPORTAR HISTÓRICO
# ============================================================

st.markdown("### 📋 IMPORTAR HISTÓRICO")

dados_colados = st.text_area(
    "Cole aqui os resultados da roleta (0 a 36)",
    placeholder=(
        "Exemplo:\n"
        "32 23 13 35 4 20 4 14 12 4"
    ),
    height=110
)

imp1, imp2 = st.columns([1, 1])


with imp1:

    if st.button(
        "📥 USAR DADOS COLADOS",
        use_container_width=True
    ):

        novos = extrair_numeros(
            dados_colados
        )

        if novos:

            st.session_state.historico = (
                novos[-MAX_HISTORICO:]
            )

            st.rerun()

        else:

            st.warning(
                "Nenhum número válido encontrado."
            )


with imp2:

    if st.button(
        "🔄 ANALISAR HISTÓRICO",
        use_container_width=True
    ):

        if st.session_state.historico:

            st.rerun()

        else:

            st.info(
                "Cole os resultados primeiro."
            )


# ============================================================
# RANKING DETALHADO
# ============================================================

if ranking:

    with st.expander(
        "📊 VER RANKING COMPLETO"
    ):

        linhas = []

        for i, item in enumerate(
            ranking,
            start=1
        ):

            n = item["numero"]

            linhas.append({
                "#": i,
                "Número": n,
                "Score": round(
                    item["score"],
                    3
                ),
                "Score %": round(
                    percentuais.get(n, 0),
                    2
                ),
                "Frequência": item["frequencia"],
                "Atraso": item["atraso"],
                "Z-score": round(
                    item["zscore"],
                    2
                ),
                "Espelho roda": item["espelho_roda"],
                "Espelho numérico": item["espelho_numero"]
            })

        st.dataframe(
            linhas,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("""
<div style="
    text-align:center;
    color:#778595;
    font-size:12px;
    padding:20px 0 5px 0;">

    🛡️ Jogue com responsabilidade.
    Este sistema é apenas para análise estatística.

</div>
""", unsafe_allow_html=True)
