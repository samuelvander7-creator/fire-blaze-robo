import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="ROBÔ RICO",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MAX_ANALISE = 200
TOTAL_ESCOLHAS = 22

NUMEROS = list(range(37))

RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

POS = {n: i for i, n in enumerate(RODA)}

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

VERMELHOS = {
    1, 3, 5, 7, 9,
    12, 14, 16, 18,
    19, 21, 23, 25,
    27, 30, 32, 34, 36
}

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 0% 0%, #071a26 0%, transparent 35%),
        radial-gradient(circle at 100% 0%, #11071d 0%, transparent 35%),
        #030a10;
    color: #f4f7fb;
}

.block-container {
    max-width: 1400px;
    padding: 20px 14px 30px 14px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.logo-area {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 16px;
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
    line-height: 1;
    letter-spacing: -2px;
}

.logo-title .rico {
    color: #20d64f;
}

.logo-subtitle {
    color: #aab5c2;
    font-size: 17px;
    margin-top: 7px;
}

.direction-box {
    min-width: 235px;
    border: 1px solid #344555;
    border-radius: 10px;
    padding: 12px 20px;
    text-align: center;
    background: rgba(5,14,22,.75);
}

.direction-label {
    color: #d8dee5;
    font-size: 13px;
}

.direction-value {
    color: #16d84b;
    font-size: 28px;
    font-weight: 800;
}

.menu-box {
    border: 1px solid #344555;
    border-radius: 10px;
    padding: 15px 20px;
    font-size: 28px;
    background: rgba(5,14,22,.75);
}

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(8,24,35,.95),
        rgba(3,12,19,.96)
    );
    border: 1px solid #263b4b;
    border-radius: 9px;
    padding: 15px 12px;
    min-height: 125px;
    text-align: center;
}

.metric-title {
    color: #d5dce4;
    font-size: 13px;
    text-transform: uppercase;
}

.metric-value {
    font-size: 40px;
    font-weight: 900;
    margin: 5px 0;
}

.metric-sub {
    color: #d5dce4;
    font-size: 14px;
}

.blue {
    color: #168cff;
}

.green {
    color: #16d84b;
}

.purple {
    color: #a84cff;
}

.cyan {
    color: #08d9ee;
}

.white {
    color: white;
}

.section-title {
    font-size: 23px;
    font-weight: 800;
    margin: 20px 0 12px 5px;
}

.choice-card {
    min-height: 300px;
    border-radius: 8px;
    padding: 16px;
    background: #06131c;
}

.choice-high {
    border: 1px solid #0e9e43;
    box-shadow: inset 0 0 25px rgba(0,190,70,.04);
}

.choice-possible {
    border: 1px solid #0878d1;
    box-shadow: inset 0 0 25px rgba(0,120,220,.04);
}

.choice-mark {
    border: 1px solid #d68a00;
    box-shadow: inset 0 0 25px rgba(220,140,0,.04);
}

.choice-title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 20px;
}

.high-title {
    color: #13df59;
}

.possible-title {
    color: #168cff;
}

.mark-title {
    color: #ffb000;
}

.ball {
    display: inline-flex;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    margin: 5px;
    font-size: 17px;
    font-weight: 900;
    border: 2px solid #77818b;
}

.ball-red {
    background: #dc2630;
    border-color: #f14b53;
}

.ball-black {
    background: #050505;
    border-color: #7d8791;
}

.ball-green {
    background: #079b43;
    border-color: #26d96a;
}

.choice-footer {
    margin-top: 20px;
    padding: 10px;
    border-radius: 5px;
    font-size: 12px;
    text-align: center;
}

.footer-high {
    color: #14d953;
    border: 1px solid #116f36;
}

.footer-possible {
    color: #1597ff;
    border: 1px solid #075b9e;
}

.footer-mark {
    color: #ffb000;
    border: 1px solid #9b6500;
}

.panel {
    background: #06131c;
    border: 1px solid #263b4b;
    border-radius: 9px;
    padding: 16px;
    min-height: 170px;
}

.panel-title {
    color: #d9e0e7;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 14px;
}

.panel-line {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,.07);
    color: #c6d0d9;
}

.panel-value {
    font-weight: 800;
    color: white;
}

.recent-ball {
    display: inline-flex;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    margin: 3px;
    font-weight: 800;
    font-size: 13px;
    border: 1px solid #65717c;
}

.rank-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 4px;
    border-bottom: 1px solid rgba(255,255,255,.08);
}

.rank-score {
    color: #14d953;
    font-weight: 800;
}

.footer-note {
    text-align: center;
    color: #7d8b97;
    font-size: 11px;
    margin-top: 20px;
}

div[data-testid="stButton"] button {
    border-radius: 7px;
    min-height: 42px;
    font-weight: 800;
    background: #071721;
    border: 1px solid #294152;
    color: white;
}

div[data-testid="stButton"] button:hover {
    border-color: #16d84b;
    color: #16d84b;
}

textarea {
    background: #07131c !important;
    color: white !important;
    border: 1px solid #2c4251 !important;
}

input {
    background: #07131c !important;
    color: white !important;
}

@media (max-width: 900px) {

    .logo-title {
        font-size: 34px;
    }

    .logo-icon {
        font-size: 42px;
    }

    .logo-subtitle {
        font-size: 13px;
    }

    .direction-box {
        display: none;
    }

    .metric-card {
        min-height: 105px;
    }

    .metric-value {
        font-size: 30px;
    }

    .ball {
        width: 42px;
        height: 42px;
        margin: 3px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION
# =========================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "resultado_anterior" not in st.session_state:
    st.session_state.resultado_anterior = None

if "previsao" not in st.session_state:
    st.session_state.previsao = []

if "acertos" not in st.session_state:
    st.session_state.acertos = 0

if "testes" not in st.session_state:
    st.session_state.testes = 0

# =========================================================
# FUNÇÕES
# =========================================================

def extrair_numeros(texto):
    texto = texto.replace(",", " ")
    texto = texto.replace(";", " ")
    texto = texto.replace("\n", " ")
    texto = texto.replace("\t", " ")

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
        return "Verde"

    if n in VERMELHOS:
        return "Vermelho"

    return "Preto"


def cor_classe(n):
    if n == 0:
        return "ball-green"

    if n in VERMELHOS:
        return "ball-red"

    return "ball-black"


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


def atraso(n, dados):
    for i, valor in enumerate(reversed(dados)):
        if valor == n:
            return i

    return len(dados)


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


def criar_transicoes(dados):
    matriz = defaultdict(Counter)

    for i in range(len(dados) - 1):
        atual = dados[i]
        proximo = dados[i + 1]

        matriz[atual][proximo] += 1

    return matriz


def score_transicao(n, ultimo, matriz):
    if ultimo not in matriz:
        return 0

    total = sum(matriz[ultimo].values())

    if total == 0:
        return 0

    quantidade = matriz[ultimo][n]

    return (quantidade / total) * 100


def score_frequencia(n, dados):

    janelas = [10, 20, 37, 50, 100, 150, 200]

    pesos = [3.0, 2.6, 2.2, 1.8, 1.4, 1.0, .7]

    score = 0

    for janela, peso in zip(janelas, pesos):

        parte = dados[-janela:]

        if not parte:
            continue

        freq = parte.count(n)

        score += freq * peso

    return score


def score_vizinhos(n, dados):

    score = 0

    for x in dados[-40:]:

        d = distancia_roda(x, n)

        if d == 1:
            score += 1.8

        elif d == 2:
            score += 1.0

        elif d == 3:
            score += .4

    return score


def score_espelhos(n, dados):

    er = espelho_roda(n)
    en = espelho_numerico(n)

    return (
        dados.count(er) * .5
        + dados.count(en) * .3
    )


def score_atraso(n, dados):

    a = atraso(n, dados)

    if a <= 2:
        return 0

    return min(a * .08, 4)


def score_matematica(n, dados):

    score = 0

    if n in PRIMOS:
        score += .5

    if n in FIBONACCI:
        score += .5

    if n in QUADRADOS:
        score += .25

    if n != 0:

        if n % 2 == 0:
            score += .10

        if n % 3 == 0:
            score += .15

        if n % 4 == 0:
            score += .10

        if n % 5 == 0:
            score += .10

        if n % 7 == 0:
            score += .10

    return score


def score_classificacao(n, dados):

    if not dados:
        return 0

    recentes = dados[-30:]

    score = 0

    mesma_cor = sum(
        cor(x) == cor(n)
        for x in recentes
    )

    score += mesma_cor * .02

    mesma_paridade = sum(
        paridade(x) == paridade(n)
        for x in recentes
    )

    score += mesma_paridade * .02

    mesma_duzia = sum(
        duzia(x) == duzia(n)
        for x in recentes
    )

    score += mesma_duzia * .02

    mesma_coluna = sum(
        coluna(x) == coluna(n)
        for x in recentes
    )

    score += mesma_coluna * .02

    return score


def calcular_score(n, dados, matriz):

    if not dados:
        return 0

    ultimo = dados[-1]

    score = 0

    score += score_frequencia(n, dados)
    score += score_vizinhos(n, dados)
    score += score_espelhos(n, dados)
    score += score_atraso(n, dados)
    score += score_matematica(n, dados)
    score += score_classificacao(n, dados)
    score += score_transicao(n, ultimo, matriz)

    # proximidade na roda
    distancia = distancia_roda(ultimo, n)

    if distancia == 1:
        score += 4

    elif distancia == 2:
        score += 2

    elif distancia == 3:
        score += 1

    return score


def analisar(dados):

    dados = dados[-MAX_ANALISE:]

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
            "frequencia": dados.count(n),
            "atraso": atraso(n, dados),
            "espelho_roda": espelho_roda(n),
            "espelho_numero": espelho_numerico(n),
            "cor": cor(n)
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # 22 escolhas divididas exatamente
    # 8 tendência alta
    # 7 possíveis
    # 7 marcação

    altas = ranking[:8]

    possiveis = ranking[8:15]

    marcacao = ranking[15:22]

    return ranking, altas, possiveis, marcacao


def formatar_bolas(lista):

    html = ""

    for item in lista:

        n = item["numero"]

        classe = cor_classe(n)

        html += f"""
        <span class="ball {classe}">
            {n}
        </span>
        """

    return html


def analisar_backtest(dados):

    if len(dados) < 30:
        return 0, 0

    acertos = 0
    testes = 0

    inicio = max(20, len(dados) - 100)

    for i in range(inicio, len(dados)):

        historico = dados[:i]

        ranking, altas, possiveis, marcacao = analisar(
            historico
        )

        escolhas = (
            altas +
            possiveis +
            marcacao
        )

        numeros = {
            x["numero"]
            for x in escolhas
        }

        resultado = dados[i]

        if resultado in numeros:
            acertos += 1

        testes += 1

    return acertos, testes

# =========================================================
# CABEÇALHO
# =========================================================

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

    <div class="direction-box">

        <div class="direction-label">
            Sentido atual
        </div>

        <div class="direction-value">
            ➜ Direita
        </div>

        <div class="direction-label">
            Automático
        </div>

    </div>

    <div class="menu-box">
        ☰
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# CONTROLE DE SENTIDO
# =========================================================

col1, col2 = st.columns([3, 1])

with col1:

    sentido = st.selectbox(
        "Sentido",
        ["Direita", "Esquerda", "Automático"],
        index=0,
        label_visibility="collapsed"
    )

with col2:

    st.write("")

# =========================================================
# HISTÓRICO
# =========================================================

st.markdown(
    '<div class="section-title">🔥 ESCOLHAS DO ROBÔ</div>',
    unsafe_allow_html=True
)

texto = st.text_area(
    "Histórico",
    placeholder=(
        "Cole aqui os últimos resultados...\n"
        "Exemplo: 32 23 13 35 4 20 4 14 12 4"
    ),
    height=100,
    label_visibility="collapsed"
)

col_a, col_b, col_c = st.columns([1, 1, 2])

with col_a:

    analisar_btn = st.button(
        "📊 ANALISAR HISTÓRICO",
        use_container_width=True
    )

with col_b:

    limpar_btn = st.button(
        "🗑️ LIMPAR",
        use_container_width=True
    )

with col_c:

    usar_btn = st.button(
        "📋 USAR DADOS COLADOS",
        use_container_width=True
    )

# =========================================================
# BOTÕES
# =========================================================

if limpar_btn:

    st.session_state.historico = []
    st.session_state.previsao = []
    st.session_state.acertos = 0
    st.session_state.testes = 0

    st.rerun()

if analisar_btn or usar_btn:

    novos = extrair_numeros(texto)

    if novos:

        st.session_state.historico = novos[-MAX_ANALISE:]

        st.rerun()

# =========================================================
# DADOS
# =========================================================

dados = st.session_state.historico

if dados:

    ranking, altas, possiveis, marcacao = analisar(dados)

    escolhas = altas + possiveis + marcacao

    # -----------------------------------------------------
    # BACKTEST
    # -----------------------------------------------------

    acertos_bt, testes_bt = analisar_backtest(dados)

    cobertura = (
        acertos_bt / testes_bt * 100
        if testes_bt
        else 0
    )

    # -----------------------------------------------------
    # MÉTRICAS
    # -----------------------------------------------------

    ultimo = dados[-1]

    frequencias = Counter(dados)

    media_freq = mean(
        frequencias.get(n, 0)
        for n in NUMEROS
    )

    atrasos = [
        atraso(n, dados)
        for n in NUMEROS
    ]

    atraso_medio = mean(atrasos)

    maior_atraso = max(atrasos)

    freq_valores = [
        frequencias.get(n, 0)
        for n in NUMEROS
    ]

    zmedio = 0

    if len(freq_valores) > 1:

        media = mean(freq_valores)
        desvio = pstdev(freq_valores)

        if desvio:
            zmedio = mean(
                (x - media) / desvio
                for x in freq_valores
            )

    transicoes = len(dados) - 1

    # -----------------------------------------------------
    # MÉTRICAS TOPO
    # -----------------------------------------------------

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Último resultado</div>
            <div class="metric-value white">{ultimo}</div>
            <div class="metric-sub">{cor(ultimo)}</div>
            <div class="metric-sub">
                {paridade(ultimo)} • {duzia(ultimo)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Base analisada</div>
            <div class="metric-value blue">{len(dados)}</div>
            <div class="metric-sub">últimos resultados</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Desempenho (22)</div>
            <div class="metric-value green">{cobertura:.1f}%</div>
            <div class="metric-sub">
                Cobertura do backtest
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m4:

        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Escolhas do robô</div>
            <div class="metric-value purple">22</div>
            <div class="metric-sub">
                8 + 7 + 7
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m5:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Transições</div>
            <div class="metric-value cyan">{transicoes:,}</div>
            <div class="metric-sub">Puxas analisadas</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # ESCOLHAS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🔥 ESCOLHAS DO ROBÔ</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns([1.25, 1.25, 1.25, .7])

    with c1:

        bolas = formatar_bolas(altas)

        st.markdown(f"""
        <div class="choice-card choice-high">

            <div class="choice-title high-title">
                📈 8 NÚMEROS COM TENDÊNCIA ALTA
            </div>

            <div>
                {bolas}
            </div>

            <div class="choice-footer footer-high">
     
