import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev
import math

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Fire Blaze Robo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MAX_ANALISE = 200
NUMEROS = list(range(37))

# ============================================================
# CSS - INTERFACE
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(0,90,140,.14), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(100,0,150,.12), transparent 30%),
        #050a10;
    color: #f1f5f9;
}

.block-container {
    max-width: 1250px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1 {
    font-size: 30px !important;
    margin-bottom: 0 !important;
}

h2 {
    font-size: 20px !important;
}

h3 {
    font-size: 15px !important;
}

p, label, span {
    font-size: 12px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(10,25,40,.95),
        rgba(5,13,22,.95)
    );
    border: 1px solid rgba(100,160,210,.20);
    border-radius: 12px;
    padding: 12px;
}

div[data-testid="stMetricValue"] {
    font-size: 27px;
}

.stButton > button {
    border-radius: 9px;
    min-height: 40px;
    font-weight: 800;
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.05);
}

.stButton > button:hover {
    border-color: rgba(0,220,170,.5);
    background: rgba(0,220,170,.10);
}

textarea,
input {
    border-radius: 9px !important;
}

.card {
    background: linear-gradient(
        145deg,
        rgba(10,27,43,.96),
        rgba(4,13,22,.96)
    );
    border: 1px solid rgba(90,150,200,.18);
    border-radius: 13px;
    padding: 14px;
    margin-bottom: 10px;
}

.card-title {
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .8px;
}

.big-number {
    font-size: 34px;
    font-weight: 900;
}

.small {
    color: #94a3b8;
    font-size: 10px;
}

.choice-box {
    background: linear-gradient(
        145deg,
        rgba(8,25,39,.98),
        rgba(3,13,22,.98)
    );
    border-radius: 12px;
    padding: 14px;
    min-height: 225px;
}

.choice-high {
    border: 1px solid rgba(0,230,120,.35);
}

.choice-possible {
    border: 1px solid rgba(0,160,255,.35);
}

.choice-mark {
    border: 1px solid rgba(255,170,0,.40);
}

.choice-title {
    font-size: 14px;
    font-weight: 900;
    margin-bottom: 12px;
}

.green {
    color: #22c55e;
}

.blue {
    color: #22a7ff;
}

.orange {
    color: #ffb000;
}

.chip {
    display: inline-block;
    min-width: 39px;
    text-align: center;
    padding: 7px 6px;
    margin: 3px;
    border-radius: 50%;
    font-size: 13px;
    font-weight: 900;
    border: 1px solid rgba(255,255,255,.18);
}

.red {
    background: #d71920;
    color: white;
}

.black {
    background: #07090c;
    color: white;
}

.zero {
    background: #159447;
    color: white;
}

.prob {
    font-weight: 800;
    color: #cbd5e1;
}

.reason {
    color: #94a3b8;
    font-size: 10px;
    margin-top: 10px;
}

.section-title {
    font-size: 18px;
    font-weight: 900;
    margin-top: 18px;
    margin-bottom: 8px;
}

.history-chip {
    display: inline-block;
    min-width: 30px;
    padding: 5px;
    margin: 2px;
    text-align: center;
    border-radius: 50%;
    font-weight: 800;
    font-size: 11px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 10px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# RODA EUROPEIA
# ============================================================

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
        except:
            pass

    return resultado


def cor(n):
    if n == 0:
        return "Zero"

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
        return "1ª"

    if n <= 24:
        return "2ª"

    return "3ª"


def coluna(n):
    if n == 0:
        return "Zero"

    resto = n % 3

    if resto == 1:
        return "1ª"

    if resto == 2:
        return "2ª"

    return "3ª"


def atraso(n, dados):
    for i, x in enumerate(reversed(dados)):
        if x == n:
            return i

    return len(dados)


def distancia_roda(a, b):
    d = abs(POS[a] - POS[b])
    return min(d, 37 - d)


# ============================================================
# ESPELHOS
# ============================================================

def espelho_roda(n):
    return RODA[(POS[n] + 18) % 37]


def espelho_numerico(n):
    if n == 0:
        return 0

    return 37 - n


# ============================================================
# VIZINHOS
# ============================================================

def vizinhos(n, quantidade=2):
    p = POS[n]

    resultado = []

    for i in range(-quantidade, quantidade + 1):
        resultado.append(
            RODA[(p + i) % 37]
        )

    return resultado


# ============================================================
# SETORES
# ============================================================

def setor(n):
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


def score_transicao(n, ultimo, matriz):

    total = sum(
        matriz[ultimo].values()
    )

    if total == 0:
        return 0

    quantidade = matriz[ultimo][n]

    return (
        quantidade / total
    ) * 10


# ============================================================
# FREQUÊNCIA
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

        frequencia = (
            parte.count(n) /
            len(parte)
        )

        score += (
            frequencia * 100 * peso
        )

    return score


# ============================================================
# Z-SCORE
# ============================================================

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

    return (
        freq[n] - media
    ) / desvio


# ============================================================
# ATRASO
# ============================================================

def score_atraso(n, dados):

    a = atraso(n, dados)

    if a <= 3:
        return 0

    return min(a * .08, 3)


# ============================================================
# VIZINHANÇA
# ============================================================

def score_vizinhança(n, dados):

    score = 0

    for resultado in dados[-30:]:

        d = distancia_roda(
            resultado,
            n
        )

        if d == 1:
            score += .8

        elif d == 2:
            score += .45

        elif d == 3:
            score += .15

    return score


# ============================================================
# SETOR
# ============================================================

def score_setor(n, dados):

    if not dados:
        return 0

    s = setor(n)

    recentes = dados[-50:]

    quantidade = sum(
        setor(x) == s
        for x in recentes
    )

    return quantidade / 20


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
    ) / 100

    score += sum(
        paridade(x) == paridade(n)
        for x in recentes
        if x != 0
    ) / 100

    score += sum(
        faixa(x) == faixa(n)
        for x in recentes
    ) / 100

    score += sum(
        duzia(x) == duzia(n)
        for x in recentes
    ) / 100

    score += sum(
        coluna(x) == coluna(n)
        for x in recentes
    ) / 100

    return score


# ============================================================
# ESPELHOS
# ============================================================

def score_espelhos(n, dados):

    er = espelho_roda(n)
    en = espelho_numerico(n)

    return (
        dados.count(er) * .12
        + dados.count(en) * .08
    )


# ============================================================
# MATEMÁTICA
# ============================================================

def score_matematica(n):

    score = 0
    motivos = []

    if n in PRIMOS:
        score += .35
        motivos.append("Primo")

    if n in FIBONACCI:
        score += .35
        motivos.append("Fibonacci")

    if n in QUADRADOS:
        score += .20
        motivos.append("Quadrado")

    if n != 0:

        if n % 2 == 0:
            score += .04

        if n % 3 == 0:
            score += .04

        if n % 4 == 0:
            score += .04

        if n % 5 == 0:
            score += .04

        if n % 7 == 0:
            score += .04

        if n % 9 == 0:
            score += .04

    return score, motivos


# ============================================================
# DIREÇÃO
# ============================================================

def score_direcao(n, dados, sentido):

    if not dados:
        return 0

    ultimo = dados[-1]

    if sentido == "Direita":

        delta = (
            POS[n] -
            POS[ultimo]
        ) % 37

    else:

        delta = (
            POS[ultimo] -
            POS[n]
        ) % 37

    if delta == 1:
        return 2.5

    if delta == 2:
        return 2.0

    if delta == 3:
        return 1.2

    if distancia_roda(
        ultimo,
        n
    ) <= 5:
        return .4

    return 0


# ============================================================
# ARITMÉTICA
# ============================================================

def score_aritmetico(n, ultimo):

    if n == ultimo:
        return .3

    diferenca = abs(
        n - ultimo
    )

    score = 0

    if diferenca in {
        1, 2, 3, 4, 5
    }:
        score += .5

    soma = n + ultimo

    if soma % 3 == 0:
        score += .15

    if soma % 5 == 0:
        score += .15

    if soma % 7 == 0:
        score += .10

    return score


# ============================================================
# DISTÂNCIA
# ============================================================

def score_distancia(n, dados):

    recentes = dados[-10:]

    if not recentes:
        return 0

    distancias = [
        distancia_roda(n, x)
        for x in recentes
    ]

    media = mean(distancias)

    return max(
        0,
        3 - media * .18
    )


# ============================================================
# SCORE GEOMÉTRICO DA MESA
# ============================================================

def coordenada_mesa(n):

    if n == 0:
        return None

    coluna_mesa = (n - 1) // 3
    linha_mesa = (n - 1) % 3

    return (
        coluna_mesa,
        linha_mesa
    )


def score_mesa(n, dados):

    if not dados or n == 0:
        return 0

    ultimo = dados[-1]

    a = coordenada_mesa(
        ultimo
    )

    b = coordenada_mesa(
        n
    )

    if a is None or b is None:
        return 0

    distancia = (
        abs(a[0] - b[0])
        +
        abs(a[1] - b[1])
    )

    if distancia == 1:
        return 1.8

    if distancia == 2:
        return .9

    return 0


# ============================================================
# CÁLCULO FINAL
# ============================================================

def calcular_numero(
    n,
    dados,
    matriz,
    sentido
):

    ultimo = dados[-1]

    score = 0
    motivos = []

    # Frequência
    s = score_frequencia(
        n,
        dados
    )

    score += s

    if s > 3:
        motivos.append("Frequência")

    # Atraso
    s = score_atraso(
        n,
        dados
    )

    score += s

    if s > .5:
        motivos.append("Atraso")

    # Z-score
    z = zscore(
        n,
        dados
    )

    score += z * .7

    if z > 1:
        motivos.append("Z-score")

    # Vizinhança
    s = score_vizinhança(
        n,
        dados
    )

    score += s

    if s > 1:
        motivos.append("Vizinhança")

    # Setor
    score += score_setor(
        n,
        dados
    )

    # Direção
    s = score_direcao(
        n,
        dados,
        sentido
    )

    score += s

    if s > 1:
        motivos.append("Direção")

    # Espelhos
    s = score_espelhos(
        n,
        dados
    )

    score += s

    if s > .5:
        motivos.append("Espelho")

    # Transição
    s = score_transicao(
        n,
        ultimo,
        matriz
    )

    score += s

    if s > .5:
        motivos.append("Transição")

    # Matemática
    s, mm = score_matematica(n)

    score += s

    motivos.extend(mm)

    # Aritmética
    score += score_aritmetico(
        n,
        ultimo
    )

    # Mesa
    s = score_mesa(
        n,
        dados
    )

    score += s

    if s > 1:
        motivos.append("Mesa")

    # Distância
    score += score_distancia(
        n,
        dados
    )

    return {
        "numero": n,
        "score": score,
        "frequencia": dados.count(n),
        "atraso": atraso(n, dados),
        "zscore": z,
        "cor": cor(n),
        "paridade": paridade(n),
        "duzia": duzia(n),
        "coluna": coluna(n),
        "setor": setor(n),
        "espelho_roda": espelho_roda(n),
        "espelho_numero": espelho_numerico(n),
        "motivos": motivos
    }


# ============================================================
# ANALISAR
# ============================================================

def analisar(dados, sentido):

    dados = dados[-MAX_ANALISE:]

    matriz = criar_transicoes(
        dados
    )

    ranking = []

    for n in NUMEROS:

        ranking.append(
            calcular_numero(
                n,
                dados,
                matriz,
                sentido
            )
        )

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # --------------------------------------------------------
    # TRANSFORMAR SCORE EM ESTIMATIVA NORMALIZADA
    # --------------------------------------------------------

    scores = [
        max(x["score"], 0)
        for x in ranking
    ]

    total = sum(scores)

    if total <= 0:
        total = 1

    for item in ranking:

        item["probabilidade"] = (
            max(item["score"], 0)
            / total
        ) * 100

    return ranking


# ============================================================
# HISTÓRICO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "sentido" not in st.session_state:
    st.session_state.sentido = "Direita"


# ============================================================
# CABEÇALHO
# ============================================================

col_logo, col_sentido, col_menu = st.columns(
    [6, 3, 1]
)

with col_logo:

    st.markdown(
        """
        <div style="
            font-size:30px;
            font-weight:900;
            padding-top:8px;
        ">
        🎯 FIRE BLAZE <span style="color:#ef2222">
        ROBO
        </span>
        </div>

        <div style="
            color:#94a3b8;
            font-size:12px;
        ">
        Estatística • Matemática • Roda • Mesa •
        Transições • Espelhos
        </div>
        """,
        unsafe_allow_html=True
    )


with col_sentido:

    sentido = st.selectbox(
        "Sentido",
        ["Direita", "Esquerda"],
        index=0 if
        st.session_state.sentido == "Direita"
        else 1
    )

    st.session_state.sentido = sentido


with col_menu:

    st.markdown(
        "<div style='font-size:32px;text-align:center'>☰</div>",
        unsafe_allow_html=True
    )


# ============================================================
# ENTRADA DE HISTÓRICO
# ============================================================

st.markdown(
    '<div class="section-title">📥 HISTÓRICO DA ROLETA</div>',
    unsafe_allow_html=True
)

texto = st.text_area(
    "",
    placeholder=(
        "Cole aqui os últimos resultados...\n"
        "Exemplo: 32 23 13 35 4 20 4 14 12 4"
    ),
    height=90
)

col1, col2 = st.columns([1, 1])

with col1:

    if st.button(
        "📊 ANALISAR HISTÓRICO",
        use_container_width=True
    ):

        numeros = extrair_numeros(
            texto
        )

        if numeros:

            st.session_state.historico = (
                numeros[-MAX_ANALISE:]
            )

            st.success(
                f"{len(st.session_state.historico)} "
                "resultados carregados."
            )

        else:

            st.warning(
                "Nenhum número válido encontrado."
            )


with col2:

    if st.button(
        "🗑️ LIMPAR",
        use_container_width=True
    ):

        st.session_state.historico = []

        st.rerun()


# ============================================================
# DADOS
# ============================================================

dados = st.session_state.historico


if len(dados) == 0:

    st.info(
        "Cole os resultados da roleta acima para iniciar a análise."
    )

    st.stop()


# ============================================================
# ANÁLISE
# ============================================================

ranking = analisar(
    dados,
    sentido
)

top22 = ranking[:22]

tendencia_alta = ranking[:8]

possiveis = ranking[8:15]

marcacao = ranking[15:22]


# ============================================================
# CABEÇALHO DE MÉTRICAS
# ============================================================

ultimo = dados[-1]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "ÚLTIMO RESULTADO",
        ultimo,
        cor(ultimo)
    )

with col2:

    st.metric(
        "BASE ANALISADA",
        len(dados),
        "máx. 200"
    )

with col3:

    cobertura = (
        len(top22) / 37
    ) * 100

    st.metric(
        "ESCOLHAS DO ROBÔ",
        "22",
        f"{cobertura:.1f}% dos números"
    )

with col4:

    media_freq = mean(
        [
            x["frequencia"]
            for x in ranking
        ]
    )

    st.metric(
        "FREQUÊNCIA MÉDIA",
        f"{media_freq:.2f}"
    )

with col5:

    transicoes = max(
        len(dados) - 1,
        0
    )

    st.metric(
        "TRANSIÇÕES",
        f"{transicoes:,}".replace(",", ".")
    )


# ============================================================
# ESCOLHAS
# ============================================================

st.markdown(
    '<div class="section-title">🔥 ESCOLHAS DO ROBÔ</div>',
    unsafe_allow_html=True
)


def chip_html(item):

    n = item["numero"]

    if n == 0:
        classe = "zero"
    elif n in VERMELHOS:
        classe = "red"
    else:
        classe = "black"

    return (
        f'<span class="chip {classe}">'
        f'{n}'
        f'</span>'
    )


def render_grupo(titulo, grupo, classe, cor_classe):

    html = f"""
    <div class="choice-box {classe}">

        <div class="choice-title {cor_classe}">
            {titulo}
        </div>
    """

    for item in grupo:

        html += f"""
        <div style="
            display:flex;
            align-items:center;
            margin-bottom:7px;
        ">

            {chip_html(item)}

            <div style="margin-left:8px">

                <span class="prob">
                    {item["probabilidade"]:.2f}%
                </span>

                <div class="small">
                    Freq: {item["frequencia"]}
                    • Atraso: {item["atraso"]}
                </div>

            </div>

        </div>
        """

    html += """
        <div class="reason">
            Estimativa baseada no conjunto de
            indicadores estatísticos.
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


c1, c2, c3 = st.columns(3)

with c1:

    render_grupo(
        "🟢 8 NÚMEROS COM TENDÊNCIA ALTA",
        tendencia_alta,
        "choice-high",
        "green"
    )

with c2:

    render_grupo(
        "🔵 7 NÚMEROS COMO POSSÍVEL",
        possiveis,
        "choice-possible",
        "blue"
    )

with c3:

    render_grupo(
        "🟠 7 NÚMEROS COMO MARCAÇÃO",
        marcacao,
        "choice-mark",
        "orange"
    )


# ============================================================
# TOP 5
# ============================================================

st.markdown(
    '<div class="section-title">🏆 TOP 5 DO MODELO</div>',
    unsafe_allow_html=True
)

cols = st.columns(5)

for i, item in enumerate(ranking[:5]):

    with cols[i]:

        st.markdown(
            f"""
            <div class="card"
                 style="text-align:center">

                <div class="card-title">
                    #{i + 1}
                </div>

                <div class="big-number">
                    {item["numero"]}
                </div>

                <div style="color:#22c55e;font-weight:800">
                    {item["probabilidade"]:.2f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ESTATÍSTICAS
# ============================================================

st.markdown(
    '<div class="section-title">📊 ESTATÍSTICAS</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    maior_freq = max(
        ranking,
        key=lambda x: x["frequencia"]
    )

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        MAIOR FREQUÊNCIA
        </div>

        <div class="big-number">
        {maior_freq["numero"]}
        </div>

        <div>
        {maior_freq["frequencia"]} vezes
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    maior_atraso = max(
        ranking,
        key=lambda x: x["atraso"]
    )

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        MAIOR ATRASO
        </div>

        <div class="big-number">
        {maior_atraso["numero"]}
        </div>

        <div>
        {maior_atraso["atraso"]} giros
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    media_atraso = mean(
        [
            x["atraso"]
            for x in ranking
        ]
    )

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        ATRASO MÉDIO
        </div>

        <div class="big-number">
        {media_atraso:.1f}
        </div>

        <div>
        giros
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    media_z = mean(
        [
            x["zscore"]
            for x in ranking
        ]
    )

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        Z-SCORE MÉDIO
        </div>

        <div class="big-number">
        {media_z:.2f}
        </div>

        <div>
        distribuição
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PADRÕES MATEMÁTICOS
# ============================================================

st.markdown(
    '<div class="section-title">🧮 PADRÕES MATEMÁTICOS</div>',
    unsafe_allow_html=True
)

primos_count = sum(
    n in PRIMOS
    for n in dados
)

fib_count = sum(
    n in FIBONACCI
    for n in dados
)

quadrados_count = sum(
    n in QUADRADOS
    for n in dados
)

mult3 = sum(
    n != 0 and n % 3 == 0
    for n in dados
)

mult2 = sum(
    n != 0 and n % 2 == 0
    for n in dados
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("PRIMOS", primos_count)

with c2:
    st.metric("FIBONACCI", fib_count)

with c3:
    st.metric("QUADRADOS", quadrados_count)

with c4:
    st.metric("MÚLTIPLOS DE 3", mult3)

with c5:
    st.metric("MÚLTIPLOS DE 2", mult2)


# ============================================================
# ÚLTIMAS JANELAS
# ============================================================

st.markdown(
    '<div class="section-title">🕐 ÚLTIMAS JANELAS</div>',
    unsafe_allow_html=True
)

janelas = [
    10,
    20,
    37,
    50,
    100,
    150,
    200
]

cols = st.columns(7)

for i, janela in enumerate(janelas):

    parte = dados[-janela:]

    if parte:

        freq = Counter(
            parte
        )

        numero = freq.most_common(1)[0][0]

        with cols[i]:

            st.markdown(
                f"""
                <div class="card"
                     style="text-align:center">

                    <div class="card-title">
                    Últimos {janela}
                    </div>

                    <div class="big-number">
                    {numero}
                    </div>

                    <div>
                    {freq[numero]}x
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# HISTÓRICO RECENTE
# ============================================================

st.markdown(
    '<div class="section-title">📜 HISTÓRICO RECENTE</div>',
    unsafe_allow_html=True
)

html = ""

for n in dados[-30:]:

    if n == 0:
        classe = "zero"
    elif n in VERMELHOS:
        classe = "red"
    else:
        classe = "black"

    html += (
        f'<span class="history-chip {classe}">'
        f'{n}'
        f'</span>'
    )

st.markdown(
    f"""
    <div class="card">
    {html}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RANKING COMPLETO
# ============================================================

with st.expander(
    "📋 VER RANKING COMPLETO DOS 37 NÚMEROS"
):

    tabela = []

    for posicao, item in enumerate(ranking):

        tabela.append({
            "#": posicao + 1,
            "Número": item["numero"],
            "Estimativa %": round(
                item["probabilidade"],
                2
            ),
            "Frequência": item["frequencia"],
            "Atraso": item["atraso"],
            "Z-score": round(
                item["zscore"],
                2
            ),
            "Cor": item["cor"],
            "Dúzia": item["duzia"],
            "Coluna": item["coluna"],
            "Espelho roda": item["espelho_roda"],
            "Espelho número": item["espelho_numero"],
            "Motivos": ", ".join(
                item["motivos"]
            )
        })

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# NOVO RESULTADO
# ============================================================

st.markdown(
    '<div class="section-title">➕ NOVO RESULTADO</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(
    [1, 3]
)

with c1:

    novo = st.number_input(
        "Digite o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )

with c2:

    if st.button(
        "ADICIONAR & ATUALIZAR",
        use_container_width=True
    ):

        st.session_state.historico.append(
            int(novo)
        )

        st.session_state.historico = (
            st.session_state.historico[
                -MAX_ANALISE:
            ]
        )

        st.rerun()


# ============================================================
# ATUALIZAR HISTÓRICO RAPIDAMENTE
# ============================================================

with st.expander(
    "📥 IMPORTAR / SUBSTITUIR HISTÓRICO"
):

    novo_historico = st.text_area(
        "Cole os resultados",
        placeholder="32 23 13 35 4 20 4 14..."
    )

    if st.button(
        "CARREGAR HISTÓRICO"
    ):

        numeros = extrair_numeros(
            novo_historico
        )

        if numeros:

            st.session_state.historico = (
                numeros[-MAX_ANALISE:]
            )

            st.rerun()


# ============================================================
# AVISO
# ============================================================

st.markdown(
    """
    <div class="footer">
    🛡️ Jogue com responsabilidade.
    Este sistema realiza análise estatística dos dados
    fornecidos e não garante resultados futuros.
    </div>
    """,
    unsafe_allow_html=True
)
