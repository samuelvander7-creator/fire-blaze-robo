import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev
import math

# ============================================================
# ROBÔ RICO 🤑
# Dashboard estatístico para análise de histórico de roleta
# ============================================================

st.set_page_config(
    page_title="ROBÔ RICO 🤑",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CONFIGURAÇÕES
# ============================================================

MAX_ANALISE = 200
TOTAL_NUMEROS = 37
TOTAL_ESCOLHAS = 22

RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

POS = {n: i for i, n in enumerate(RODA)}

VERMELHOS = {
    1, 3, 5, 7, 9,
    12, 14, 16, 18,
    19, 21, 23, 25,
    27, 30, 32, 34, 36
}

PRIMOS = {
    2, 3, 5, 7, 11,
    13, 17, 19, 23,
    29, 31
}

FIBONACCI = {
    0, 1, 2, 3, 5, 8,
    13, 21, 34
}

QUADRADOS = {
    0, 1, 4, 9, 16, 25, 36
}


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

:root {
    --bg: #02070c;
    --panel: #07131d;
    --panel2: #091923;
    --border: #203442;
    --text: #edf4f8;
    --muted: #91a2ae;
    --blue: #1689ff;
    --green: #19d35a;
    --purple: #9d4cff;
    --cyan: #00cfe8;
    --orange: #ffae22;
    --red: #ff2638;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 0%,
            rgba(0, 110, 170, .13),
            transparent 32%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(75, 0, 150, .12),
            transparent 30%
        ),
        #02070c;
    color: var(--text);
}

.block-container {
    max-width: 1400px;
    padding: 18px 14px 30px 14px;
}

/* Remove excesso visual do Streamlit */
[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* =========================================================
   CABEÇALHO
   ========================================================= */

.logo-area {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}

.logo-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.logo-icon {
    font-size: 55px;
    line-height: 1;
}

.logo-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1;
    color: #f3f7fa;
}

.logo-title .rico {
    color: #18d75a;
}

.logo-subtitle {
    margin-top: 7px;
    color: #a3b0b8;
    font-size: 16px;
}

.direction-box {
    min-width: 285px;
    border: 1px solid #263a48;
    border-radius: 12px;
    padding: 10px 18px;
    text-align: center;
    background: rgba(5, 14, 21, .85);
}

.direction-label {
    font-size: 13px;
    color: #d4dce1;
}

.direction-value {
    color: #18d75a;
    font-size: 28px;
    font-weight: 900;
}

.direction-auto {
    font-size: 12px;
    color: #b2bec6;
}

/* =========================================================
   CARDS
   ========================================================= */

.cards-5 {
    display: grid;
    grid-template-columns:
        repeat(5, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}

.card {
    background:
        linear-gradient(
            145deg,
            rgba(10, 25, 36, .98),
            rgba(3, 12, 18, .98)
        );
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 14px;
    min-height: 115px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.025),
        0 8px 25px rgba(0,0,0,.12);
}

.card-title {
    color: #d3dce1;
    font-size: 13px;
    text-align: center;
    text-transform: uppercase;
}

.card-number {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    line-height: 1.05;
    margin-top: 8px;
}

.card-description {
    text-align: center;
    color: #d4dce1;
    font-size: 14px;
    margin-top: 4px;
}

.blue {
    color: #168cff;
}

.green {
    color: #16d85a;
}

.purple {
    color: #a64dff;
}

.cyan {
    color: #00d5ea;
}

.white {
    color: #ffffff;
}

.progress {
    height: 9px;
    background: #142630;
    border-radius: 20px;
    margin-top: 10px;
    overflow: hidden;
}

.progress-blue {
    height: 100%;
    background: #168cff;
    border-radius: 20px;
}

.progress-green {
    height: 100%;
    background: #18d75a;
    border-radius: 20px;
}

.progress-purple {
    height: 100%;
    background: #9d4cff;
    border-radius: 20px;
}

/* =========================================================
   ESCOLHAS
   ========================================================= */

.main-selection {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 195px;
    gap: 12px;
    margin-bottom: 16px;
}

.selection-container {
    background: #051019;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 13px;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 12px;
    color: #e9f0f4;
}

.selection-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
}

.selection-box {
    border-radius: 8px;
    padding: 12px;
    min-height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.high-box {
    border: 1px solid rgba(20, 220, 85, .55);
    background: rgba(0, 90, 45, .08);
}

.possible-box {
    border: 1px solid rgba(0, 130, 255, .55);
    background: rgba(0, 80, 150, .08);
}

.mark-box {
    border: 1px solid rgba(255, 170, 20, .55);
    background: rgba(130, 80, 0, .08);
}

.selection-title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 15px;
}

.high-title {
    color: #16d85a;
}

.possible-title {
    color: #168cff;
}

.mark-title {
    color: #ffae22;
}

.ball-grid {
    display: grid;
    grid-template-columns:
        repeat(4, minmax(35px, 1fr));
    gap: 14px 10px;
    align-items: center;
    justify-items: center;
    flex: 1;
}

.ball {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 900;
    border: 1px solid #6f7c84;
    color: white;
    background: #050607;
}

.ball.red {
    background: #e51d2a;
    border-color: #ff6670;
}

.ball.black {
    background: #030405;
}

.ball.green {
    background: #16a849;
    border-color: #35ed7b;
}

.selection-footer {
    margin-top: 15px;
    padding: 9px;
    border-radius: 6px;
    font-size: 12px;
    text-align: center;
}

.high-footer {
    color: #17d85b;
    border: 1px solid rgba(20,220,85,.35);
}

.possible-footer {
    color: #168cff;
    border: 1px solid rgba(0,130,255,.35);
}

.mark-footer {
    color: #ffae22;
    border: 1px solid rgba(255,170,20,.35);
}

/* =========================================================
   TOP 5
   ========================================================= */

.top5 {
    background: #051019;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 14px;
}

.top5-title {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 10px;
}

.top-row {
    display: grid;
    grid-template-columns: 28px 1fr 55px;
    gap: 4px;
    align-items: center;
    padding: 11px 2px;
    border-bottom: 1px solid rgba(255,255,255,.08);
}

.top-rank {
    color: #b9c4ca;
}

.top-number {
    font-weight: 900;
}

.top-score {
    text-align: right;
    color: #18d75a;
    font-weight: 800;
}

.top-button {
    margin-top: 12px;
    padding: 10px;
    text-align: center;
    background: #101d26;
    border-radius: 5px;
    font-size: 12px;
}

/* =========================================================
   CARDS DE ESTATÍSTICAS
   ========================================================= */

.stats-5 {
    display: grid;
    grid-template-columns:
        repeat(5, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}

.stat-big {
    font-size: 23px;
    font-weight: 800;
    margin-top: 9px;
}

.stat-line {
    color: #d0d9de;
    margin-top: 6px;
    font-size: 14px;
}

/* =========================================================
   PAINÉIS INFERIORES
   ========================================================= */

.lower-3 {
    display: grid;
    grid-template-columns:
        1fr 1fr 1.25fr;
    gap: 12px;
    margin-bottom: 16px;
}

.panel {
    background: #051019;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 15px;
}

.panel-title {
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.pattern-row,
.window-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 2px;
    border-bottom: 1px solid rgba(255,255,255,.07);
}

.pattern-value {
    font-weight: 900;
    color: #13d65a;
}

.window-number {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    font-weight: 900;
}

/* =========================================================
   HISTÓRICO
   ========================================================= */

.bottom-3 {
    display: grid;
    grid-template-columns:
        1.2fr 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}

.history-balls {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.small-ball {
    width: 31px;
    height: 31px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 900;
    border: 1px solid #6c777d;
}

/* =========================================================
   INPUTS
   ========================================================= */

.input-panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 8px;
}

.input-box {
    background: #051019;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 15px;
}

.input-title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 8px;
}

.footer-note {
    text-align: center;
    color: #85949e;
    font-size: 12px;
    padding: 15px;
}

/* =========================================================
   STREAMLIT INPUTS
   ========================================================= */

textarea {
    background: #07131d !important;
    color: white !important;
    border: 1px solid #284252 !important;
    border-radius: 8px !important;
}

input {
    background: #07131d !important;
    color: white !important;
    border: 1px solid #284252 !important;
    border-radius: 8px !important;
}

.stButton button {
    background: #0a1720 !important;
    color: #e9f0f4 !important;
    border: 1px solid #284252 !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
}

.stButton button:hover {
    border-color: #18d75a !important;
    color: #18d75a !important;
}

[data-testid="stSelectbox"] div {
    color: white !important;
}

/* =========================================================
   RESPONSIVO
   ========================================================= */

@media (max-width: 900px) {

    .logo-area {
        flex-direction: column;
        align-items: stretch;
    }

    .direction-box {
        width: 100%;
    }

    .cards-5 {
        grid-template-columns: repeat(2, 1fr);
    }

    .main-selection {
        grid-template-columns: 1fr;
    }

    .selection-grid {
        grid-template-columns: 1fr;
    }

    .stats-5 {
        grid-template-columns: repeat(2, 1fr);
    }

    .lower-3,
    .bottom-3 {
        grid-template-columns: 1fr;
    }

    .input-panel {
        grid-template-columns: 1fr;
    }

    .logo-title {
        font-size: 32px;
    }
}

@media (max-width: 520px) {

    .block-container {
        padding: 10px 8px 25px 8px;
    }

    .cards-5,
    .stats-5 {
        grid-template-columns: 1fr 1fr;
        gap: 7px;
    }

    .card {
        min-height: 100px;
        padding: 9px 5px;
    }

    .card-title {
        font-size: 10px;
    }

    .card-number {
        font-size: 29px;
    }

    .card-description {
        font-size: 10px;
    }

    .logo-icon {
        font-size: 42px;
    }

    .logo-title {
        font-size: 28px;
    }

    .logo-subtitle {
        font-size: 12px;
    }

    .selection-container {
        padding: 8px;
    }

    .selection-box {
        min-height: 230px;
    }

    .ball {
        width: 42px;
        height: 42px;
        font-size: 14px;
    }

    .ball-grid {
        gap: 10px 4px;
    }

    .section-title {
        font-size: 17px;
    }

    .stat-big {
        font-size: 19px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES
# ============================================================

def extrair_numeros(texto):
    texto = (
        texto.replace(",", " ")
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


def cor_numero(n):
    if n == 0:
        return "green"

    if n in VERMELHOS:
        return "red"

    return "black"


def nome_cor(n):
    if n == 0:
        return "Verde"

    if n in VERMELHOS:
        return "Vermelho"

    return "Preto"


def paridade(n):
    if n == 0:
        return "Zero"

    return "Par" if n % 2 == 0 else "Ímpar"


def faixa(n):
    if n == 0:
        return "Zero"

    return "1–18" if n <= 18 else "19–36"


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
        return 0

    return RODA[(POS[n] + 18) % 37]


def espelho_numerico(n):
    if n == 0:
        return 0

    return 37 - n


def setor_roda(n):
    if n not in POS:
        return 0

    return POS[n] // 5


def atraso(n, dados):
    for i, x in enumerate(reversed(dados)):
        if x == n:
            return i

    return len(dados)


def criar_transicoes(dados):
    matriz = defaultdict(Counter)

    for i in range(len(dados) - 1):
        origem = dados[i]
        destino = dados[i + 1]
        matriz[origem][destino] += 1

    return matriz


def transicao_score(n, ultimo, matriz):
    total = sum(matriz[ultimo].values())

    if total == 0:
        return 0

    ocorrencias = matriz[ultimo][n]

    return (ocorrencias / total) * 12


def frequencia_score(n, dados):

    pesos = {
        10: 2.8,
        20: 2.3,
        37: 1.8,
        50: 1.4,
        100: 1.0,
        150: .7,
        200: .5
    }

    score = 0

    for janela, peso in pesos.items():

        parte = dados[-janela:]

        if not parte:
            continue

        frequencia = parte.count(n)

        media = len(parte) / 37

        if media > 0:
            score += (
                frequencia / media
            ) * peso

    return score


def atraso_score(n, dados):

    a = atraso(n, dados)

    if a <= 2:
        return 0

    return min(a / 15, 4)


def vizinhanca_score(n, dados):

    score = 0

    for x in dados[-40:]:

        d = distancia_roda(n, x)

        if d == 1:
            score += .65

        elif d == 2:
            score += .35

        elif d == 3:
            score += .12

    return score


def espelho_score(n, dados):

    er = espelho_roda(n)
    en = espelho_numerico(n)

    return (
        dados.count(er) * .15
        + dados.count(en) * .08
    )


def matematica_score(n, dados):

    score = 0

    if n in PRIMOS:
        score += .35

    if n in FIBONACCI:
        score += .30

    if n in QUADRADOS:
        score += .20

    if n != 0:

        if n % 2 == 0:
            score += .05

        if n % 3 == 0:
            score += .05

        if n % 4 == 0:
            score += .05

        if n % 5 == 0:
            score += .05

    return score


def classificacao_score(n, dados):

    if not dados:
        return 0

    recentes = dados[-30:]

    score = 0

    # Cor
    cor_n = nome_cor(n)

    mesma_cor = sum(
        nome_cor(x) == cor_n
        for x in recentes
        if x != 0
    )

    score += mesma_cor / 100

    # Paridade
    par_n = paridade(n)

    mesma_paridade = sum(
        paridade(x) == par_n
        for x in recentes
        if x != 0
    )

    score += mesma_paridade / 120

    # Dúzia
    duz_n = duzia(n)

    mesma_duzia = sum(
        duzia(x) == duz_n
        for x in recentes
    )

    score += mesma_duzia / 120

    # Coluna
    col_n = coluna(n)

    mesma_coluna = sum(
        coluna(x) == col_n
        for x in recentes
    )

    score += mesma_coluna / 120

    return score


def zscore(n, dados):

    if not dados:
        return 0

    freq = Counter(dados)

    valores = [
        freq[x]
        for x in range(37)
    ]

    media = mean(valores)

    desvio = pstdev(valores)

    if desvio == 0:
        return 0

    return (
        freq[n] - media
    ) / desvio


def geometria_score(n, dados):

    if not dados:
        return 0

    ultimo = dados[-1]

    d = distancia_roda(
        n,
        ultimo
    )

    if d == 1:
        return 2.0

    if d == 2:
        return 1.1

    if d == 3:
        return .5

    if d <= 5:
        return .15

    return 0


def aritmetica_score(n, dados):

    if not dados:
        return 0

    ultimo = dados[-1]

    diferenca = abs(n - ultimo)

    score = 0

    if diferenca in {1, 2, 3}:
        score += .5

    soma = n + ultimo

    if soma % 3 == 0:
        score += .08

    if soma % 5 == 0:
        score += .08

    if soma % 7 == 0:
        score += .08

    return score


# ============================================================
# ANALISADOR PRINCIPAL
# ============================================================

def analisar(dados, sentido):

    dados = dados[-MAX_ANALISE:]

    matriz = criar_transicoes(dados)

    resultados = []

    ultimo = dados[-1]

    for n in range(37):

        f = frequencia_score(
            n,
            dados
        )

        a = atraso_score(
            n,
            dados
        )

        v = vizinhanca_score(
            n,
            dados
        )

        e = espelho_score(
            n,
            dados
        )

        m = matematica_score(
            n,
            dados
        )

        c = classificacao_score(
            n,
            dados
        )

        z = zscore(
            n,
            dados
        )

        g = geometria_score(
            n,
            dados
        )

        t = transicao_score(
            n,
            ultimo,
            matriz
        )

        ar = aritmetica_score(
            n,
            dados
        )

        # Direção da roda
        direcao = 0

        if n != ultimo:

            if sentido == "Direita":

                delta = (
                    POS[n] - POS[ultimo]
                ) % 37

            else:

                delta = (
                    POS[ultimo] - POS[n]
                ) % 37

            if delta == 1:
                direcao = 1.7

            elif delta == 2:
                direcao = 1.1

            elif delta == 3:
                direcao = .5

        score = (
            f
            + a
            + v
            + e
            + m
            + c
            + (z * .65)
            + g
            + t
            + ar
            + direcao
        )

        resultados.append({
            "numero": n,
            "score": score,
            "frequencia": dados.count(n),
            "atraso": atraso(n, dados),
            "zscore": z,
            "cor": nome_cor(n),
            "espelho_roda": espelho_roda(n),
            "espelho_numero": espelho_numerico(n),
            "setor": setor_roda(n)
        })

    resultados.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultados


# ============================================================
# PERCENTUAIS DO MODELO
# ============================================================

def calcular_percentuais(ranking):

    total_score = sum(
        max(x["score"], .01)
        for x in ranking
    )

    for x in ranking:

        x["percentual"] = (
            max(x["score"], .01)
            / total_score
            * 100
        )

    return ranking


# ============================================================
# CLASSIFICAÇÃO
# ============================================================

def separar_escolhas(ranking):

    ranking = ranking[:22]

    alta = ranking[:8]
    possiveis = ranking[8:15]
    marcacao = ranking[15:22]

    return alta, possiveis, marcacao


# ============================================================
# BACKTEST
# ============================================================

def executar_backtest(dados, sentido):

    if len(dados) < 50:
        return {
            "acertos": 0,
            "testes": 0,
            "cobertura": 0
        }

    inicio = max(
        30,
        len(dados) - 100
    )

    acertos = 0
    testes = 0

    for i in range(
        inicio,
        len(dados)
    ):

        historico = dados[:i]

        ranking = analisar(
            historico,
            sentido
        )

        ranking = calcular_percentuais(
            ranking
        )

        escolhas = {
            x["numero"]
            for x in ranking[:22]
        }

        resultado = dados[i]

        if resultado in escolhas:
            acertos += 1

        testes += 1

    cobertura = (
        acertos / testes * 100
        if testes
        else 0
    )

    return {
        "acertos": acertos,
        "testes": testes,
        "cobertura": cobertura
    }


# ============================================================
# HTML DOS NÚMEROS
# ============================================================

def bola(n, pequena=False):

    classe = (
        "small-ball"
        if pequena
        else "ball"
    )

    return (
        f'<span class="{classe} '
        f'{cor_numero(n)}">{n}</span>'
    )


def bolas(numeros, pequena=False):

    return "".join(
        bola(n, pequena)
        for n in numeros
    )


# ============================================================
# ESTADO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "sentido" not in st.session_state:
    st.session_state.sentido = "Direita"

if "resultado_anterior" not in st.session_state:
    st.session_state.resultado_anterior = None


# ============================================================
# CABEÇALHO
# ============================================================

sentido = st.selectbox(
    "Sentido",
    ["Direita", "Esquerda"],
    index=0 if st.session_state.sentido == "Direita" else 1
)

st.session_state.sentido = sentido

st.markdown(
    f"""
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

        <div class="direction-box">

            <div class="direction-label">
                Sentido atual
            </div>

            <div class="direction-value">
                → {sentido}
            </div>

            <div class="direction-auto">
                Automático　↻
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# ÁREA DE IMPORTAÇÃO
# ============================================================

with st.expander("📥 IMPORTAR / ATUALIZAR HISTÓRICO", expanded=not st.session_state.historico):

    texto = st.text_area(
        "Cole os resultados da roleta",
        placeholder="Exemplo: 32 23 13 35 4 20 4 14 12 4",
        height=100
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        analisar_btn = st.button(
            "📊 ANALISAR HISTÓRICO",
            use_container_width=True
        )

    with c2:
        limpar_btn = st.button(
            "🗑️ LIMPAR",
            use_container_width=True
        )

    if limpar_btn:
        st.session_state.historico = []
        st.rerun()

    if analisar_btn:

        novos = extrair_numeros(texto)

        if novos:

            st.session_state.historico = (
                novos[-MAX_ANALISE:]
            )

            st.session_state.resultado_anterior = (
                st.session_state.historico[-1]
            )

            st.rerun()

        else:

            st.error(
                "Nenhum número válido encontrado. "
                "Use números de 0 a 36."
            )


# ============================================================
# SEM HISTÓRICO
# ============================================================

dados = st.session_state.historico

if not dados:

    st.info(
        "Cole os resultados da roleta acima para iniciar a análise estatística."
    )

    st.stop()


# ============================================================
# ANÁLISE
# ============================================================

ranking = analisar(
    dados,
    sentido
)

ranking = calcular_percentuais(
    ranking
)

alta, possiveis, marcacao = separar_escolhas(
    ranking
)

escolhas = alta + possiveis + marcacao

backtest = executar_backtest(
    dados,
    sentido
)

ultimo = dados[-1]


# ============================================================
# DADOS DO DASHBOARD
# ============================================================

freq = Counter(dados)

frequencia_media = (
    len(dados) / 37
)

frequencias = [
    freq[x]
    for x in range(37)
]

frequencia_max = max(
    frequencias
)

atrasos = [
    atraso(x, dados)
    for x in range(37)
]

atraso_medio = mean(
    atrasos
)

maior_atraso = max(
    atrasos
)

zscores = [
    zscore(x, dados)
    for x in range(37)
]

zscore_medio = mean(
    zscores
)

zscore_max = max(
    zscores
)

total_transicoes = max(
    0,
    len(dados) - 1
) * 36

# ============================================================
# CARDS SUPERIORES
# ============================================================

percentual_cobertura = (
    backtest["cobertura"]
)

st.markdown(
    f"""
    <div class="cards-5">

        <div class="card">
            <div class="card-title">
                ÚLTIMO RESULTADO
            </div>

            <div class="card-number white">
                {ultimo}
            </div>

            <div class="card-description">
                {nome_cor(ultimo).upper()}
            </div>

            <div class="card-description">
                {paridade(ultimo)} • {faixa(ultimo)} • {duzia(ultimo)}
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                BASE ANALISADA
            </div>

            <div class="card-number blue">
                {len(dados)}
            </div>

            <div class="card-description">
                últimos resultados
            </div>

            <div class="progress">
                <div
                    class="progress-blue"
                    style="width:{min(len(dados),200)/2}%">
                </div>
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                DESEMPENHO (22)
            </div>

            <div class="card-number green">
                {percentual_cobertura:.1f}%
            </div>

            <div class="card-description">
                cobertura no backtest
            </div>

            <div class="progress">
                <div
                    class="progress-green"
                    style="width:{min(percentual_cobertura,100)}%">
                </div>
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                ESCOLHAS DO ROBÔ
            </div>

            <div class="card-number purple">
                22
            </div>

            <div class="card-description">
                números selecionados
            </div>

            <div class="progress">
                <div
                    class="progress-purple"
                    style="width:59.45%">
                </div>
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                TRANSIÇÕES
            </div>

            <div class="card-number cyan">
                {total_transicoes:,}
            </div>

            <div class="card-description">
                Puxas analisadas
            </div>

            <div class="card-description"
                 style="color:#18d75a">
                Padrões de transição
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ESCOLHAS + TOP 5
# ============================================================

def selection_box(titulo, numeros, classe, footer):

    html = f"""
    <div class="selection-box {classe}">

        <div class="selection-title">
            {titulo}
        </div>

        <div class="ball-grid">
            {bolas([x["numero"] for x in numeros])}
        </div>

        <div class="selection-footer
            {'high-footer' if classe == 'high-box'
             else 'possible-footer' if classe == 'possible-box'
             else 'mark-footer'}">
            {footer}
        </div>

    </div>
    """

    return html


top5_html = ""

for i, item in enumerate(ranking[:5], 1):

    top5_html += f"""
    <div class="top-row">

        <div class="top-rank">
            {i}
        </div>

        <div class="top-number">
            {item["numero"]}
        </div>

        <div class="top-score">
            {item["percentual"]:.1f}
        </div>

    </div>
    """


st.markdown(
    f"""
    <div class="main-selection">

        <div class="selection-container">

            <div class="section-title">
                🔥 ESCOLHAS DO ROBÔ
            </div>

            <div class="selection-grid">

                {selection_box(
                    "📈 8 NÚMEROS COM TENDÊNCIA ALTA",
                    alta,
                    "high-box",
                    "↗ Maior força estatística no momento"
                )}

                {selection_box(
                    "❓ 7 NÚMEROS COMO POSSÍVEL",
                    possiveis,
                    "possible-box",
                    "ⓘ Números com força secundária"
                )}

                {selection_box(
                    "🎯 7 NÚMEROS COMO MARCAÇÃO",
                    marcacao,
                    "mark-box",
                    "🛡 Cobertura e proteção estatística"
                )}

            </div>

        </div>


        <div class="top5">

            <div class="top5-title">
                👑 TOP 5 GERAL
            </div>

            {top5_html}

            <div class="top-button">
                VER RANKING COMPLETO
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SEGUNDA LINHA
# ============================================================

st.markdown(
    f"""
    <div class="stats-5">

        <div class="card">
            <div class="card-title">
                📊 FREQUÊNCIA (200)
            </div>

            <div class="stat-big">
                Média: {frequencia_media:.2f}
            </div>

            <div class="stat-line">
                Máx: {frequencia_max}
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                🕒 ATRASO MÉDIO
            </div>

            <div class="stat-big">
                Média: {atraso_medio:.1f}
            </div>

            <div class="stat-line">
                Máx: {maior_atraso}
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                Σ Z-SCORE MÉDIO
            </div>

            <div class="stat-big">
                Média: {zscore_medio:.2f}
            </div>

            <div class="stat-line">
                Máx: {zscore_max:.2f}
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                🧳 MAIOR ATRASO
            </div>

            <div class="stat-big">
                {maior_atraso}
            </div>

            <div class="stat-line">
                giros
            </div>
        </div>


        <div class="card">
            <div class="card-title">
                🔄 TRANSIÇÕES
            </div>

            <div class="stat-big">
                {total_transicoes:,}
            </div>

            <div class="stat-line"
                 style="color:#18d75a">
                Puxas analisadas
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RESUMO DE CORES
# ============================================================

vermelhos = sum(
    x in VERMELHOS
    for x in dados
)

verdes = dados.count(0)

pretos = (
    len(dados)
    - vermelhos
    - verdes
)

pct_vermelho = (
    vermelhos / len(dados) * 100
)

pct_preto = (
    pretos / len(dados) * 100
)

pct_verde = (
    verdes / len(dados) * 100
)

# ============================================================
# PADRÕES MATEMÁTICOS
# ============================================================

q_primos = sum(
    x in PRIMOS
    for x in dados
)

q_fibo = sum(
    x in FIBONACCI
    for x in dados
)

q_quadrados = sum(
    x in QUADRADOS
    for x in dados
)

q_mult3 = sum(
    x != 0 and x % 3 == 0
    for x in dados
)

q_mult2 = sum(
    x != 0 and x % 2 == 0
    for x in dados
)

# ============================================================
# JANELAS
# ============================================================

janelas = [
    10,
    20,
    37,
    50,
    100,
    150,
    200
]

janela_html = ""

for janela in janelas:

    if len(dados) >= janela:

        numero = dados[-janela]

    else:

        numero = dados[0]

    janela_html += f"""
    <div class="window-row">

        <span>
            Últimos {janela}
        </span>

        {bola(numero, pequena=True)}

    </div>
    """


# ============================================================
# PAINÉIS
# ============================================================

st.markdown(
    f"""
    <div class="lower-3">

        <div class="panel">

            <div class="panel-title">
                RESUMO DE CORES
            </div>

            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                gap:20px;
                margin:15px 0;
            ">

                <div style="
                    width:130px;
                    height:130px;
                    border-radius:50%;
                    background:
                    conic-gradient(
                        #ef2635 0 {pct_vermelho}%,
                        #050505 {pct_vermelho}% {pct_vermelho + pct_preto}%,
                        #13a74a {pct_vermelho + pct_preto}% 100%
                    );
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">

                    <div style="
                        width:75px;
                        height:75px;
                        border-radius:50%;
                        background:#041019;
                    "></div>

                </div>

                <div>
                    <div>🔴 Vermelhos {pct_vermelho:.1f}%</div>
                    <div>⚫ Pretos {pct_preto:.1f}%</div>
                    <div>🟢 Verdes {pct_verde:.1f}%</div>
                </div>

            </div>

        </div>


        <div class="panel">

            <div class="panel-title">
                PADRÕES NUMÉRICOS
            </div>

            <div class="pattern-row">
                <span>Primos</span>
                <span class="pattern-value">{q_primos}</span>
            </div>

            <div class="pattern-row">
                <span>Fibonacci</span>
                <span class="pattern-value">{q_fibo}</span>
            </div>

            <div class="pattern-row">
                <span>Quadrados</span>
                <span class="pattern-value">{q_quadrados}</span>
            </div>

            <div class="pattern-row">
                <span>Múltiplos de 3</span>
                <span class="pattern-value">{q_mult3}</span>
            </div>

            <div class="pattern-row">
                <span>Múltiplos de 2</span>
                <span class="pattern-value">{q_mult2}</span>
            </div>

        </div>


        <div class="panel">

            <div class="panel-title">
                ÚLTIMAS JANELAS
            </div>

            {janela_html}

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HISTÓRICO RECENTE
# ============================================================

historico_recente = dados[-20:]

historico_html = bolas(
    historico_recente,
    pequena=True
)

st.markdown(
    f"""
    <div class="bottom-3">

        <div class="panel">

            <div class="panel-title">
                HISTÓRICO RECENTE
                <span style="color:#81919b">
                    (últimos 20)
                </span>
            </div>

            <div class="history-balls">
                {historico_html}
            </div>

        </div>


        <div class="panel">

            <div class="panel-title">
                TESTE DE COBERTURA (BACKTEST)
            </div>

            <div style="
                display:grid;
                grid-template-columns:
                repeat(3,1fr);
                text-align:center;
                gap:10px;
            ">

                <div>
                    <div>Acertos</div>
                    <strong style="
                        color:#18d75a;
                        font-size:27px;">
                        {backtest["acertos"]}
                    </strong>
                </div>

                <div>
                    <div>Testes</div>
                    <strong style="
                        color:#168cff;
                        font-size:27px;">
                        {backtest["testes"]}
                    </strong>
                </div>

                <div>
                    <div>Cobertura</div>
                    <strong style="
                        color:#ffae22;
                        font-size:27px;">
                        {backtest["cobertura"]:.1f}%
                    </strong>
                </div>

            </div>

            <div class="progress">
                <div
                    class="progress-green"
                    style="width:{min(backtest["cobertura"],100)}%">
                </div>
            </div>

        </div>


        <div class="panel">

            <div class="panel-title">
                DETALHES DESEMPENHO (22)
            </div>

            <div style="
                display:grid;
                grid-template-columns:
                repeat(3,1fr);
                text-align:center;
                gap:10px;
            ">

                <div>
                    <div>Acertos</div>
                    <strong style="
                        color:#18d75a;
                        font-size:27px;">
                        {backtest["acertos"]}
                    </strong>
                </div>

                <div>
                    <div>Erros</div>
                    <strong style="
                        color:#ef2635;
                        font-size:27px;">
                        {max(
                            0,
                            backtest["testes"]
                            - backtest["acertos"]
                        )}
                    </strong>
                </div>

                <div>
                    <div>Total</div>
                    <strong style="
                        font-size:27px;">
                        {backtest["testes"]}
                    </strong>
                </div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NOVO RESULTADO
# ============================================================

st.markdown(
    '<div class="input-panel">',
    unsafe_allow_html=True
)

with st.container():

    st.markdown(
        """
        <div class="input-box">

            <div class="input-title">
                NOVO RESULTADO
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    novo = st.number_input(
        "Digite o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1,
        key="novo_resultado"
    )

    adicionar = st.button(
        "➕ ADICIONAR & ATUALIZAR",
        use_container_width=True
    )

    if adicionar:

        st.session_state.historico.append(
            int(novo)
        )

        st.session_state.historico = (
            st.session_state.historico[-MAX_ANALISE:]
        )

        st.rerun()


with st.container():

    st.markdown(
        """
        <div class="input-box">

            <div class="input-title">
                📋 IMPORTAR HISTÓRICO
            </div>

            Cole os últimos resultados
            novamente na área de importação
            acima.

        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# RANKING DETALHADO
# ============================================================

with st.expander("📋 VER RANKING COMPLETO DOS 37 NÚMEROS"):

    ranking_data = []

    for posicao, item in enumerate(ranking, 1):

        ranking_data.append({
            "#": posicao,
            "Número": item["numero"],
            "Score": round(item["score"], 2),
            "Modelo %": round(item["percentual"], 2),
            "Frequência": item["frequencia"],
            "Atraso": item["atraso"],
            "Z-score": round(item["zscore"], 2),
            "Cor": item["cor"],
            "Espelho roda": item["espelho_roda"],
            "Espelho numérico": item["espelho_numero"]
        })

    st.dataframe(
        ranking_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        🛡️ Jogue com responsabilidade.
        Este sistema é apenas para análise estatística.
        As estimativas do modelo não garantem o próximo resultado.
    </div>
    """,
    unsafe_allow_html=True
)
