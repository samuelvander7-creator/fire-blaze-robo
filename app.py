import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev
import math

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="ROBÔ RICO 🤑",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MAX_HISTORICO = 200
TOTAL_ESCOLHAS = 22

# ============================================================
# CSS — ROBÔ RICO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(0,110,180,.12), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(70,0,150,.12), transparent 30%),
        #02070c;
    color: #e8edf5;
}

.block-container {
    max-width: 1450px;
    padding: 18px 18px 35px 18px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1,h2,h3,p {
    margin-top: 0;
}

/* ================= HEADER ================= */

.logo-title {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
}

.logo-title .rico {
    color: #16d65a;
}

.subtitle {
    color: #9ca9b8;
    font-size: 14px;
    margin-top: 8px;
}

/* ================= CARDS ================= */

.card {
    background: linear-gradient(
        145deg,
        rgba(8,22,34,.96),
        rgba(3,11,18,.96)
    );
    border: 1px solid rgba(120,160,190,.22);
    border-radius: 11px;
    padding: 16px;
    min-height: 115px;
    box-shadow: 0 8px 25px rgba(0,0,0,.22);
}

.card-title {
    color: #b7c0cc;
    font-size: 12px;
    text-transform: uppercase;
    text-align: center;
    letter-spacing: .4px;
}

.card-number {
    font-size: 38px;
    font-weight: 900;
    text-align: center;
    margin: 6px 0;
}

.card-sub {
    color: #d7dce4;
    font-size: 13px;
    text-align: center;
}

.blue {
    color: #1495ff;
}

.green {
    color: #16d65a;
}

.purple {
    color: #a34dff;
}

.cyan {
    color: #00cfe8;
}

.orange {
    color: #ffad19;
}

/* ================= SEÇÃO ESCOLHAS ================= */

.main-panel {
    background: linear-gradient(
        145deg,
        rgba(5,18,28,.98),
        rgba(2,9,15,.98)
    );
    border: 1px solid rgba(120,160,190,.22);
    border-radius: 11px;
    padding: 15px;
    margin-top: 15px;
}

.panel-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 13px;
}

/* ================= GRUPOS ================= */

.group {
    border-radius: 9px;
    padding: 14px;
    min-height: 245px;
    background: rgba(0,0,0,.17);
}

.group-green {
    border: 1px solid rgba(0,210,90,.55);
}

.group-blue {
    border: 1px solid rgba(0,130,255,.55);
}

.group-orange {
    border: 1px solid rgba(255,160,0,.55);
}

.group-title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 18px;
}

.green-title {
    color: #16d65a;
}

.blue-title {
    color: #1699ff;
}

.orange-title {
    color: #ffad19;
}

/* ================= BOLAS ================= */

.ball-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 18px;
}

.ball {
    width: 49px;
    height: 49px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 16px;
    color: white;
    border: 2px solid rgba(255,255,255,.28);
    box-shadow: inset 0 0 8px rgba(255,255,255,.08);
}

.red-ball {
    background: #e5242a;
}

.black-ball {
    background: #050505;
}

.green-ball {
    background: #08a94c;
}

.group-footer {
    border: 1px solid currentColor;
    border-radius: 6px;
    padding: 9px;
    text-align: center;
    font-size: 11px;
    margin-top: 10px;
}

/* ================= TOP 5 ================= */

.top5 {
    background: linear-gradient(
        145deg,
        rgba(8,22,34,.98),
        rgba(3,11,18,.98)
    );
    border: 1px solid rgba(120,160,190,.22);
    border-radius: 11px;
    padding: 15px;
}

.top5-title {
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 10px;
}

.top-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 3px;
    border-bottom: 1px solid rgba(255,255,255,.07);
}

.top-number {
    font-size: 17px;
    font-weight: 800;
}

.top-score {
    color: #15d75b;
    font-weight: 800;
}

/* ================= MINI CARDS ================= */

.mini-card {
    background: linear-gradient(
        145deg,
        rgba(8,22,34,.96),
        rgba(3,11,18,.96)
    );
    border: 1px solid rgba(120,160,190,.22);
    border-radius: 10px;
    padding: 14px;
    min-height: 105px;
}

.mini-title {
    color: #c1cad5;
    font-size: 12px;
    text-transform: uppercase;
}

.mini-value {
    font-size: 22px;
    font-weight: 800;
    margin-top: 8px;
}

.mini-sub {
    color: #a7b1bd;
    font-size: 12px;
    margin-top: 4px;
}

/* ================= HISTÓRICO ================= */

.history-box {
    background: #050b11;
    border: 1px solid rgba(120,160,190,.22);
    border-radius: 9px;
    padding: 12px;
}

.history-ball {
    display: inline-flex;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    margin: 3px;
    font-size: 12px;
    font-weight: 800;
    color: white;
    border: 1px solid rgba(255,255,255,.25);
}

/* ================= ALERTA ================= */

.info-box {
    background: rgba(0,75,150,.16);
    border: 1px solid rgba(0,130,255,.25);
    border-radius: 9px;
    padding: 13px;
    color: #7fbfff;
}

/* ================= BOTÕES ================= */

.stButton > button {
    width: 100%;
    border-radius: 8px;
    min-height: 42px;
    font-weight: 800;
    background: #08121b;
    border: 1px solid rgba(130,160,190,.28);
    color: #e9eef5;
}

.stButton > button:hover {
    border-color: #1cd85d;
    color: #1cd85d;
}

/* ================= INPUT ================= */

textarea,
input {
    border-radius: 8px !important;
}

/* ================= MOBILE ================= */

@media (max-width: 800px) {

    .block-container {
        padding: 10px;
    }

    .logo-title {
        font-size: 29px;
    }

    .subtitle {
        font-size: 11px;
    }

    .card {
        min-height: 95px;
        padding: 10px;
    }

    .card-number {
        font-size: 29px;
    }

    .panel-title {
        font-size: 18px;
    }

    .ball {
        width: 42px;
        height: 42px;
        font-size: 14px;
    }
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

POS = {n: i for i, n in enumerate(RODA)}

VERMELHOS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}

PRIMOS = {
    2,3,5,7,11,13,17,19,23,29,31
}

FIBONACCI = {
    0,1,2,3,5,8,13,21,34
}

QUADRADOS = {
    0,1,4,9,16,25,36
}


# ============================================================
# SESSION STATE
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultima_previsao" not in st.session_state:
    st.session_state.ultima_previsao = []

if "validacoes" not in st.session_state:
    st.session_state.validacoes = []

if "sentido" not in st.session_state:
    st.session_state.sentido = "Direita"


# ============================================================
# FUNÇÕES BÁSICAS
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

        except ValueError:
            pass

    return resultado


def cor(n):
    if n == 0:
        return "Verde"

    return "Vermelho" if n in VERMELHOS else "Preto"


def classe_cor(n):
    if n == 0:
        return "green-ball"

    return "red-ball" if n in VERMELHOS else "black-ball"


def paridade(n):
    if n == 0:
        return "Zero"

    return "Par" if n % 2 == 0 else "Ímpar"


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


def faixa(n):
    if n == 0:
        return "Zero"

    return "1-18" if n <= 18 else "19-36"


def distancia_roda(a, b):
    d = abs(POS[a] - POS[b])
    return min(d, 37 - d)


def atraso(n, dados):
    for i, valor in enumerate(reversed(dados)):
        if valor == n:
            return i

    return len(dados)


def espelho_roda(n):
    return RODA[(POS[n] + 18) % 37]


def espelho_numerico(n):
    if n == 0:
        return 0

    return 37 - n


def setor_roda(n):
    return POS[n] // 5


# ============================================================
# TRANSIÇÕES
# ============================================================

def criar_transicoes(dados):
    matriz = defaultdict(Counter)

    for i in range(len(dados) - 1):
        atual = dados[i]
        proximo = dados[i + 1]

        matriz[atual][proximo] += 1

    return matriz


# ============================================================
# SCORE DE FREQUÊNCIA
# ============================================================

def score_frequencia(n, dados):

    pesos = {
        10: 2.8,
        20: 2.3,
        37: 1.9,
        50: 1.5,
        100: 1.1,
        150: .8,
        200: .6
    }

    score = 0

    for janela, peso in pesos.items():

        parte = dados[-janela:]

        if not parte:
            continue

        freq = parte.count(n) / len(parte)

        score += freq * 100 * peso

    return score


# ============================================================
# SCORE DE ATRASO
# ============================================================

def score_atraso(n, dados):

    a = atraso(n, dados)

    if a <= 3:
        return 0

    return min(a * .07, 3.0)


# ============================================================
# SCORE DE VIZINHANÇA
# ============================================================

def score_vizinhos(n, dados):

    score = 0

    for resultado in dados[-40:]:

        d = distancia_roda(
            n,
            resultado
        )

        if d == 1:
            score += .75

        elif d == 2:
            score += .42

        elif d == 3:
            score += .15

    return score


# ============================================================
# SCORE DE ESPELHOS
# ============================================================

def score_espelhos(n, dados):

    espelho_r = espelho_roda(n)
    espelho_n = espelho_numerico(n)

    return (
        dados.count(espelho_r) * .15
        + dados.count(espelho_n) * .08
    )


# ============================================================
# SCORE DE TRANSIÇÃO / "PUXA"
# ============================================================

def score_transicao(n, dados, matriz):

    if not dados:
        return 0

    ultimo = dados[-1]

    total = sum(
        matriz[ultimo].values()
    )

    if total == 0:
        return 0

    ocorrencias = matriz[ultimo][n]

    taxa = ocorrencias / total

    # suavização para não deixar
    # poucas ocorrências dominarem
    confianca = min(total / 10, 1)

    return taxa * 8 * confianca


# ============================================================
# SCORE DE SETOR DA RODA
# ============================================================

def score_setor(n, dados):

    if not dados:
        return 0

    setor = setor_roda(n)

    recentes = dados[-50:]

    quantidade = sum(
        setor_roda(x) == setor
        for x in recentes
    )

    return quantidade / 25


# ============================================================
# SCORE DE MESA
# ============================================================

def coordenada_mesa(n):

    if n == 0:
        return None

    coluna_mesa = (n - 1) // 3
    linha_mesa = (n - 1) % 3

    return coluna_mesa, linha_mesa


def distancia_mesa(a, b):

    ca = coordenada_mesa(a)
    cb = coordenada_mesa(b)

    if ca is None or cb is None:
        return 99

    return (
        abs(ca[0] - cb[0])
        + abs(ca[1] - cb[1])
    )


def score_mesa(n, dados):

    if not dados:
        return 0

    ultimo = dados[-1]

    d = distancia_mesa(
        ultimo,
        n
    )

    if d == 1:
        return 1.4

    if d == 2:
        return .8

    if d == 3:
        return .3

    return 0


# ============================================================
# MATEMÁTICA
# ============================================================

def score_matematica(n):

    score = 0

    if n in PRIMOS:
        score += .35

    if n in FIBONACCI:
        score += .35

    if n in QUADRADOS:
        score += .20

    if n != 0:

        for divisor in [2,3,4,5,6,7,9]:

            if n % divisor == 0:
                score += .035

    return score


# ============================================================
# CLASSIFICAÇÕES
# ============================================================

def score_classificacao(n, dados):

    recentes = dados[-30:]

    if not recentes:
        return 0

    score = 0

    score += sum(
        cor(x) == cor(n)
        for x in recentes
        if x != 0
    ) / 150

    score += sum(
        paridade(x) == paridade(n)
        for x in recentes
        if x != 0
    ) / 150

    score += sum(
        duzia(x) == duzia(n)
        for x in recentes
    ) / 150

    score += sum(
        coluna(x) == coluna(n)
        for x in recentes
    ) / 150

    return score


# ============================================================
# Z-SCORE
# ============================================================

def zscore(n, dados):

    if not dados:
        return 0

    frequencias = Counter(dados)

    valores = [
        frequencias[x]
        for x in range(37)
    ]

    media = mean(valores)

    desvio = pstdev(valores)

    if desvio == 0:
        return 0

    return (
        frequencias[n] - media
    ) / desvio


# ============================================================
# SCORE DE DIREÇÃO
# ============================================================

def score_direcao(n, dados):

    if not dados:
        return 0

    ultimo = dados[-1]

    if st.session_state.sentido == "Direita":

        delta = (
            POS[n] - POS[ultimo]
        ) % 37

    else:

        delta = (
            POS[ultimo] - POS[n]
        ) % 37

    if delta == 1:
        return 1.5

    if delta == 2:
        return 1.0

    if delta == 3:
        return .55

    return 0


# ============================================================
# SCORE TOTAL
# ============================================================

def calcular_score(n, dados, matriz):

    if not dados:
        return 0

    score = 0

    score += score_frequencia(
        n, dados
    )

    score += score_atraso(
        n, dados
    )

    score += score_vizinhos(
        n, dados
    )

    score += score_espelhos(
        n, dados
    )

    score += score_transicao(
        n,
        dados,
        matriz
    )

    score += score_setor(
        n,
        dados
    )

    score += score_mesa(
        n,
        dados
    )

    score += score_matematica(n)

    score += score_classificacao(
        n,
        dados
    )

    score += score_direcao(
        n,
        dados
    )

    # Z-score recebe peso pequeno
    # para evitar distorção
    score += zscore(
        n,
        dados
    ) * .5

    return score


# ============================================================
# ANÁLISE COMPLETA
# ============================================================

def analisar(dados):

    matriz = criar_transicoes(dados)

    ranking = []

    for n in range(37):

        score = calcular_score(
            n,
            dados,
            matriz
        )

        ranking.append({
            "numero": n,
            "score": score,
            "frequencia": dados.count(n),
            "atraso": atraso(n, dados),
            "zscore": zscore(n, dados)
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # 22 números separados:
    alta = ranking[:8]
    possiveis = ranking[8:15]
    marcacao = ranking[15:22]

    # Pontuação relativa para visualização.
    # NÃO representa probabilidade matemática real.
    scores_positivos = [
        max(x["score"], 0)
        for x in ranking
    ]

    total_score = sum(
        scores_positivos
    )

    if total_score <= 0:
        total_score = 1

    for item in ranking:

        item["probabilidade"] = (
            max(item["score"], 0)
            / total_score
            * 100
        )

    return ranking, alta, possiveis, marcacao


# ============================================================
# BACKTEST
# ============================================================

def backtest(dados):

    if len(dados) < 40:
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

    for i in range(inicio, len(dados)):

        historico = dados[:i]

        ranking, alta, possiveis, marcacao = analisar(
            historico
        )

        escolhidos = {
            x["numero"]
            for x in (
                alta
                + possiveis
                + marcacao
            )
        }

        resultado = dados[i]

        if resultado in escolhidos:
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
# COMPONENTES VISUAIS
# ============================================================

def bola_html(n):

    classe = classe_cor(n)

    return (
        f'<span class="ball {classe}">'
        f'{n}'
        f'</span>'
    )


def bolas_html(lista):

    html = '<div class="ball-row">'

    for item in lista:
        html += bola_html(
            item["numero"]
            if isinstance(item, dict)
            else item
        )

    html += "</div>"

    return html


def historico_html(dados):

    html = '<div class="history-box">'

    for n in dados[-20:]:

        html += (
            f'<span class="history-ball '
            f'{classe_cor(n)}">'
            f'{n}'
            f'</span>'
        )

    html += "</div>"

    return html


def media_frequencia(dados):

    if not dados:
        return 0

    freq = Counter(dados)

    valores = [
        freq[x]
        for x in range(37)
    ]

    return mean(valores)


def media_atraso(dados):

    if not dados:
        return 0

    return mean(
        atraso(n, dados)
        for n in range(37)
    )


def maior_atraso(dados):

    if not dados:
        return 0

    return max(
        atraso(n, dados)
        for n in range(37)
    )


def media_zscore(dados):

    if not dados:
        return 0

    return mean(
        zscore(n, dados)
        for n in range(37)
    )


def quantidade_transicoes(dados):

    if len(dados) < 2:
        return 0

    matriz = criar_transicoes(dados)

    total = 0

    for origem in matriz:

        for destino in matriz[origem]:

            if matriz[origem][destino] >= 2:
                total += matriz[origem][destino]

    return total


# ============================================================
# CABEÇALHO
# ============================================================

col_logo, col_sentido, col_menu = st.columns(
    [5.2, 2.2, 0.8]
)

with col_logo:

    st.markdown(
        '<div class="logo-title">'
        '🎯 ROBÔ <span class="rico">RICO</span> 🤑'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Estatística • Matemática • Roda • Mesa • '
        'Transições • Espelhos'
        '</div>',
        unsafe_allow_html=True
    )


with col_sentido:

    sentido = st.selectbox(
        "Sentido atual",
        ["Direita", "Esquerda"],
        index=0 if st.session_state.sentido == "Direita" else 1
    )

    st.session_state.sentido = sentido


with col_menu:

    st.markdown(
        "<div style='font-size:42px;text-align:center;"
        "padding-top:8px;'>☰</div>",
        unsafe_allow_html=True
    )


# ============================================================
# ENTRADA
# ============================================================

st.markdown("### 📥 HISTÓRICO DA ROLETA")

texto = st.text_area(
    "",
    placeholder=(
        "Cole aqui os últimos resultados...\n"
        "Exemplo: 32 23 13 35 4 20 4 14 12 4"
    ),
    height=90,
    key="entrada_historico"
)

c1, c2, c3 = st.columns(3)

with c1:

    analisar_btn = st.button(
        "📊 ANALISAR HISTÓRICO"
    )

with c2:

    limpar_btn = st.button(
        "🗑️ LIMPAR"
    )

with c3:

    importar_btn = st.button(
        "📋 USAR DADOS COLADOS"
    )


if limpar_btn:

    st.session_state.historico = []
    st.session_state.ultima_previsao = []
    st.session_state.validacoes = []

    st.rerun()


if analisar_btn or importar_btn:

    novos = extrair_numeros(texto)

    if novos:

        st.session_state.historico = (
            novos[-MAX_HISTORICO:]
        )

        st.rerun()

    else:

        st.warning(
            "Digite números de 0 a 36 para iniciar."
        )


dados = st.session_state.historico


# ============================================================
# SEM DADOS
# ============================================================

if not dados:

    st.markdown(
        '<div class="info-box">'
        'Cole os resultados da roleta acima para iniciar '
        'a análise estatística.'
        '</div>',
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# ANÁLISE
# ============================================================

ranking, alta, possiveis, marcacao = analisar(
    dados
)

top22 = alta + possiveis + marcacao

st.session_state.ultima_previsao = [
    x["numero"]
    for x in top22
]


# ============================================================
# BACKTEST
# ============================================================

bt = backtest(dados)


# ============================================================
# CARDS SUPERIORES
# ============================================================

ultimo = dados[-1]

frequencia_media = media_frequencia(
    dados
)

atraso_medio = media_atraso(
    dados
)

zmedio = media_zscore(
    dados
)

maior = maior_atraso(
    dados
)

transicoes = quantidade_transicoes(
    dados
)

cards = st.columns(5)

with cards[0]:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Último resultado
            </div>
            <div class="card-number">
                {ultimo}
            </div>
            <div class="card-sub">
                {cor(ultimo)}
            </div>
            <div class="card-sub">
                {paridade(ultimo)} •
                {faixa(ultimo)} •
                {duzia(ultimo)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cards[1]:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Base analisada
            </div>
            <div class="card-number blue">
                {len(dados)}
            </div>
            <div class="card-sub">
                últimos resultados
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cards[2]:

    cobertura = bt["cobertura"]

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Desempenho (22)
            </div>
            <div class="card-number green">
                {cobertura:.1f}%
            </div>
            <div class="card-sub">
                cobertura no backtest
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cards[3]:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Escolhas do robô
            </div>
            <div class="card-number purple">
                22
            </div>
            <div class="card-sub">
                8 + 7 + 7
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cards[4]:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Transições
            </div>
            <div class="card-number cyan">
                {transicoes:,}
            </div>
            <div class="card-sub">
                transições observadas
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ESCOLHAS + TOP 5
# ============================================================

col_escolhas, col_top = st.columns(
    [4.4, 1.1]
)

with col_escolhas:

    st.markdown(
        '<div class="main-panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">'
        '🔥 ESCOLHAS DO ROBÔ'
        '</div>',
        unsafe_allow_html=True
    )

    g1, g2, g3 = st.columns(3)

    # ---------------- TENDÊNCIA ----------------

    with g1:

        st.markdown(
            '<div class="group group-green">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="group-title green-title">'
            '📈 8 NÚMEROS COM TENDÊNCIA ALTA'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            bolas_html(alta),
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="group-footer green-title">'
            'Maior força estatística no momento'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ---------------- POSSÍVEIS ----------------

    with g2:

        st.markdown(
            '<div class="group group-blue">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="group-title blue-title">'
            '❓ 7 NÚMEROS COMO POSSÍVEL'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            bolas_html(possiveis),
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="group-footer blue-title">'
            'Números com chance secundária'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ---------------- MARCAÇÃO ----------------

    with g3:

        st.markdown(
            '<div class="group group-orange">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="group-title orange-title">'
            '🎯 7 NÚMEROS COMO MARCAÇÃO'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            bolas_html(marcacao),
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="group-footer orange-title">'
            'Números para cobertura estatística'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# TOP 5
# ============================================================

with col_top:

    st.markdown(
        '<div class="top5">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="top5-title">'
        '🏆 TOP 5 GERAL'
        '</div>',
        unsafe_allow_html=True
    )

    for i, item in enumerate(
        ranking[:5],
        start=1
    ):

        st.markdown(
            f"""
            <div class="top-item">
                <span>
                    {i} &nbsp;
                    <span class="top-number">
                        {item["numero"]}
                    </span>
                </span>
                <span class="top-score">
                    {item["score"]:.1f}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MINI CARDS
# ============================================================

st.markdown("")

mini = st.columns(5)

with mini[0]:

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                📊 Frequência (200)
            </div>
            <div class="mini-value">
                {frequencia_media:.2f}
            </div>
            <div class="mini-sub">
                Média
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with mini[1]:

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                🕒 Atraso médio
            </div>
            <div class="mini-value">
                {atraso_medio:.1f}
            </div>
            <div class="mini-sub">
                Máx: {maior}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with mini[2]:

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                Σ Z-score médio
            </div>
            <div class="mini-value">
                {zmedio:.2f}
            </div>
            <div class="mini-sub">
                distribuição
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with mini[3]:

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                📦 Maior atraso
            </div>
            <div class="mini-value">
                {maior}
            </div>
            <div class="mini-sub">
                giros
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with mini[4]:

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                🔄 Transições
            </div>
            <div class="mini-value">
                {transicoes:,}
            </div>
            <div class="mini-sub">
                observadas
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RESUMO / PADRÕES / JANELAS
# ============================================================

a, b, c = st.columns(
    [1.2, 1.1, 1.5]
)

# ---------------- CORES ----------------

with a:

    contagem_cores = Counter(
        cor(x)
        for x in dados
    )

    total = len(dados)

    vermelho_pct = (
        contagem_cores["Vermelho"]
        / total
        * 100
    )

    preto_pct = (
        contagem_cores["Preto"]
        / total
        * 100
    )

    verde_pct = (
        contagem_cores["Verde"]
        / total
        * 100
    )

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                RESUMO DE CORES
            </div>
            <br>
            🔴 Vermelhos:
            <b>{vermelho_pct:.1f}%</b>
            <br><br>
            ⚫ Pretos:
            <b>{preto_pct:.1f}%</b>
            <br><br>
            🟢 Verdes:
            <b>{verde_pct:.1f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- PADRÕES ----------------

with b:

    primos = sum(
        x in PRIMOS
        for x in dados
    )

    fibonacci = sum(
        x in FIBONACCI
        for x in dados
    )

    quadrados = sum(
        x in QUADRADOS
        for x in dados
    )

    multiplos3 = sum(
        x != 0 and x % 3 == 0
        for x in dados
    )

    multiplos2 = sum(
        x != 0 and x % 2 == 0
        for x in dados
    )

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                PADRÕES NUMÉRICOS
            </div>
            <br>
            Primos: <b>{primos}</b>
            <br><br>
            Fibonacci: <b>{fibonacci}</b>
            <br><br>
            Quadrados: <b>{quadrados}</b>
            <br><br>
            Múltiplos de 3: <b>{multiplos3}</b>
            <br><br>
            Múltiplos de 2: <b>{multiplos2}</b>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- JANELAS ----------------

with c:

    janelas = [
        10,
        20,
        37,
        50,
        100,
        150,
        200
    ]

    html = """
    <div class="mini-card">
        <div class="mini-title">
            ÚLTIMAS JANELAS
        </div>
        <br>
    """

    for janela in janelas:

        parte = dados[-janela:]

        if parte:

            ultimo_janela = parte[-1]

            html += (
                f"Últimos {janela}: "
                f"<b>{ultimo_janela}</b>"
                "<br><br>"
            )

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# HISTÓRICO / BACKTEST / DESEMPENHO
# ============================================================

h1, h2, h3 = st.columns(
    [1.4, 1.1, 1.1]
)

with h1:

    st.markdown(
        '<div class="mini-card">'
        '<div class="mini-title">'
        'HISTÓRICO RECENTE (últimos 20)'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        historico_html(dados),
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with h2:

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                TESTE DE COBERTURA
            </div>
            <br>
            Acertos:
            <b style="color:#16d65a">
                {bt["acertos"]}
            </b>
            <br><br>
            Testes:
            <b>{bt["testes"]}</b>
            <br><br>
            Cobertura:
            <b style="color:#ffad19">
                {bt["cobertura"]:.1f}%
            </b>
        </div>
        """,
        unsafe_allow_html=True
    )


with h3:

    erros = max(
        bt["testes"] - bt["acertos"],
        0
    )

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">
                DETALHES DESEMPENHO (22)
            </div>
            <br>
            <span style="color:#16d65a">
                Acertos: {bt["acertos"]}
            </span>
            <br><br>
            <span style="color:#ff3b43">
                Erros: {erros}
            </span>
            <br><br>
            Total: {bt["testes"]}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# NOVO RESULTADO
# ============================================================

st.markdown("")

n1, n2 = st.columns(
    [2.3, 1]
)

with n1:

    st.markdown(
        "### 🎯 NOVO RESULTADO"
    )

    novo = st.number_input(
        "Digite o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )


with n2:

    st.markdown("### ")

    atualizar = st.button(
        "🟢 ADICIONAR & ATUALIZAR"
    )


if atualizar:

    st.session_state.historico.append(
        int(novo)
    )

    st.session_state.historico = (
        st.session_state.historico[-MAX_HISTORICO:]
    )

    st.rerun()


# ============================================================
# IMPORTAR NOVAMENTE
# ============================================================

st.markdown("### 📋 IMPORTAR HISTÓRICO")

texto2 = st.text_area(
    "Cole aqui os resultados para substituir a base atual",
    height=80,
    placeholder="Exemplo: 17 34 6 11 27 2 25 13 36..."
)

if st.button("📥 IMPORTAR NOVA BASE"):

    novos = extrair_numeros(
        texto2
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


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7f8b99;
        font-size:11px;
        padding-top:20px;
    ">
        🛡️ Jogue com responsabilidade.
        Este sistema é apenas para análise estatística.
        As pontuações não garantem o resultado de nenhum giro.
    </div>
    """,
    unsafe_allow_html=True
)
