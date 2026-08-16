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

JANELAS = [10, 20, 37, 50, 100, 150, 200]

# ============================================================
# CSS - INTERFACE MODERNA
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(80, 70, 180, .18),
            transparent 35%
        ),
        radial-gradient(
            circle at top left,
            rgba(0, 180, 170, .10),
            transparent 30%
        ),
        #090b12;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    letter-spacing: -0.5px;
}

h1 {
    font-size: 30px !important;
}

h2 {
    font-size: 20px !important;
}

h3 {
    font-size: 15px !important;
}

p, label, span, div {
    font-size: 12px;
}

.stButton > button {
    border-radius: 10px;
    min-height: 38px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.06);
}

.stButton > button:hover {
    border-color: rgba(255,255,255,.30);
    background: rgba(255,255,255,.10);
}

textarea, input {
    border-radius: 10px !important;
}

.card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.075),
        rgba(255,255,255,.025)
    );
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 0 8px 30px rgba(0,0,0,.18);
}

.card-title {
    font-size: 11px;
    opacity: .65;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.card-value {
    font-size: 25px;
    font-weight: 800;
    margin-top: 4px;
}

.number-chip {
    display: inline-block;
    padding: 5px 8px;
    margin: 3px;
    border-radius: 8px;
    background: rgba(255,255,255,.075);
    border: 1px solid rgba(255,255,255,.12);
    font-weight: 700;
    font-size: 12px;
}

.number-chip-top {
    display: inline-block;
    padding: 7px 10px;
    margin: 3px;
    border-radius: 9px;
    background: linear-gradient(
        135deg,
        rgba(0,200,170,.30),
        rgba(80,80,220,.25)
    );
    border: 1px solid rgba(100,220,210,.35);
    font-weight: 800;
    font-size: 13px;
}

.result-number {
    font-size: 48px;
    font-weight: 900;
    line-height: 1;
}

.mini {
    font-size: 10px !important;
    opacity: .65;
}

.section {
    margin-top: 18px;
    margin-bottom: 8px;
}

hr {
    border-color: rgba(255,255,255,.08);
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
# ESTADO
# ============================================================

defaults = {
    "historico": [],
    "iniciado": False,
    "ultimo": None,
    "sentido": "Direita",
    "previsoes": [],
    "acertos": 0,
    "total_validacoes": 0,
    "ultima_previsao": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


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

    saida = []

    for item in texto.split():
        try:
            n = int(item)
            if 0 <= n <= 36:
                saida.append(n)
        except ValueError:
            continue

    return saida


def distancia_roda(a, b):
    d = abs(POS[a] - POS[b])
    return min(d, 37 - d)


def cor(n):
    if n == 0:
        return "Zero"
    return "Vermelho" if n in VERMELHOS else "Preto"


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
    r = n % 3
    if r == 1:
        return "1ª"
    if r == 2:
        return "2ª"
    return "3ª"


def atraso(n, dados):
    for i, x in enumerate(reversed(dados)):
        if x == n:
            return i
    return len(dados)


def soma_digitos(n):
    return sum(int(x) for x in str(n))


# ============================================================
# VIZINHOS
# ============================================================

def vizinhos_roda(n, quantidade=2):
    p = POS[n]

    esquerda = [
        RODA[(p - i) % 37]
        for i in range(quantidade, 0, -1)
    ]

    direita = [
        RODA[(p + i) % 37]
        for i in range(1, quantidade + 1)
    ]

    return esquerda + [n] + direita


def vizinhos_ampliados(n):
    p = POS[n]

    return [
        RODA[(p + i) % 37]
        for i in range(-5, 6)
    ]


# ============================================================
# ESPELHOS
# ============================================================

def espelho_roda(n):
    p = POS[n]
    return RODA[(p + 18) % 37]


def espelho_numerico(n):
    if n == 0:
        return 0
    return 37 - n


# ============================================================
# SETOR
# ============================================================

def setor(n):
    return POS[n] // 5


# ============================================================
# TRANSIÇÕES / "PUXA"
# ============================================================

def criar_transicoes(dados):
    matriz = defaultdict(Counter)

    for i in range(len(dados) - 1):
        atual = dados[i]
        proximo = dados[i + 1]
        matriz[atual][proximo] += 1

    return matriz


def forca_transicao(origem, destino, matriz):
    total = sum(matriz[origem].values())

    if total == 0:
        return 0

    return matriz[origem][destino] / total


# ============================================================
# MESA
# ============================================================

def coordenada_mesa(n):
    if n == 0:
        return None

    # representação das três linhas da mesa
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


def movimento_mesa(a, b):
    ca = coordenada_mesa(a)
    cb = coordenada_mesa(b)

    if ca is None or cb is None:
        return None

    return (
        cb[0] - ca[0],
        cb[1] - ca[1]
    )


# ============================================================
# ANÁLISE DE PADRÃO DA MESA
# ============================================================

def score_geometria(n, dados):
    if len(dados) < 2 or n == 0:
        return 0

    ultimo = dados[-1]

    score = 0

    dmesa = distancia_mesa(
        ultimo,
        n
    )

    if dmesa == 1:
        score += 2.0

    elif dmesa == 2:
        score += 1.0

    movimento_anterior = None

    if len(dados) >= 2:
        movimento_anterior = movimento_mesa(
            dados[-2],
            dados[-1]
        )

    movimento_atual = movimento_mesa(
        dados[-1],
        n
    )

    if (
        movimento_anterior is not None
        and movimento_atual is not None
    ):

        dx1, dy1 = movimento_anterior
        dx2, dy2 = movimento_atual

        # continuidade
        if dx1 == dx2 and dy1 == dy2:
            score += 1.5

        # inversão
        if dx1 == -dx2 and dy1 == -dy2:
            score += 1.5

        # alternância
        if dx1 != dx2 or dy1 != dy2:
            score += .3

        # diagonal
        if abs(dx2) == 1 and abs(dy2) == 1:
            score += .7

    return score


# ============================================================
# DIREÇÃO NA RODA
# ============================================================

def score_direcao(n, dados, sentido):
    if not dados:
        return 0

    ultimo = dados[-1]

    d = distancia_roda(
        ultimo,
        n
    )

    if sentido == "Direita":
        delta = (
            POS[n] - POS[ultimo]
        ) % 37
    else:
        delta = (
            POS[ultimo] - POS[n]
        ) % 37

    if delta == 1:
        return 2.5

    if delta == 2:
        return 2.0

    if delta == 3:
        return 1.2

    if d <= 5:
        return .4

    return 0


# ============================================================
# Z-SCORE
# ============================================================

def zscore_numero(n, dados):
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
# PONTUAÇÃO DE PROPRIEDADES MATEMÁTICAS
# ============================================================

def propriedades(n):
    score = 0
    motivos = []

    if n in PRIMOS:
        score += .35
        motivos.append("primo")

    if n in FIBONACCI:
        score += .35
        motivos.append("Fibonacci")

    if n in QUADRADOS:
        score += .20
        motivos.append("quadrado")

    for divisor in [2, 3, 4, 5, 6, 7, 9]:
        if n != 0 and n % divisor == 0:
            score += .04

    return score, motivos


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

        f = parte.count(n) / len(parte)

        score += f * 100 * peso

    return score


# ============================================================
# SCORE DE ATRASO
# ============================================================

def score_atraso(n, dados):
    a = atraso(n, dados)

    if a <= 3:
        return 0

    return min(
        a * .08,
        3
    )


# ============================================================
# SCORE DE VIZINHANÇA
# ============================================================

def score_vizinhança(n, dados):
    score = 0

    for r in dados[-30:]:
        d = distancia_roda(
            r,
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
# SCORE DE SETOR
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
# SCORE DE CLASSIFICAÇÕES
# ============================================================

def score_classificacao(n, dados):

    recentes = dados[-30:]

    if not recentes:
        return 0

    score = 0

    # cor
    mesma_cor = sum(
        cor(x) == cor(n)
        for x in recentes
        if x != 0
    )

    score += mesma_cor / 100

    # paridade
    mesma_paridade = sum(
        paridade(x) == paridade(n)
        for x in recentes
        if x != 0
    )

    score += mesma_paridade / 100

    # faixa
    mesma_faixa = sum(
        faixa(x) == faixa(n)
        for x in recentes
    )

    score += mesma_faixa / 100

    # dúzia
    mesma_duzia = sum(
        duzia(x) == duzia(n)
        for x in recentes
    )

    score += mesma_duzia / 100

    # coluna
    mesma_coluna = sum(
        coluna(x) == coluna(n)
        for x in recentes
    )

    score += mesma_coluna / 100

    return score


# ============================================================
# SCORE DE ESPELHOS
# ============================================================

def score_espelhos(n, dados):

    er = espelho_roda(n)
    en = espelho_numerico(n)

    return (
        dados.count(er) * .12
        + dados.count(en) * .08
    )


# ============================================================
# SCORE ARITMÉTICO
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
# SCORE DE TRANSIÇÃO
# ============================================================

def score_transicao(
    n,
    ultimo,
    matriz
):

    p = forca_transicao(
        ultimo,
        n,
        matriz
    )

    # pequeno peso para evitar
    # que poucas ocorrências dominem
    return p * 10


# ============================================================
# SCORE DE DISTÂNCIA
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
# SCORE FINAL
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

    # frequência
    sf = score_frequencia(
        n,
        dados
    )

    score += sf

    if sf > 3:
        motivos.append("frequência")

    # atraso
    sa = score_atraso(
        n,
        dados
    )

    score += sa

    if sa > .5:
        motivos.append("atraso")

    # z-score
    z = zscore_numero(
        n,
        dados
    )

    score += z * .7

    if z > 1:
        motivos.append("z-score alto")

    # vizinhos
    sv = score_vizinhança(
        n,
        dados
    )

    score += sv

    if sv > 1:
        motivos.append("vizinhança")

    # setor
    ss = score_setor(
        n,
        dados
    )

    score += ss

    # direção
    sd = score_direcao(
        n,
        dados,
        sentido
    )

    score += sd

    if sd > 1:
        motivos.append(
            f"direção {sentido.lower()}"
        )

    # geometria
    sg = score_geometria(
        n,
        dados
    )

    score += sg

    if sg > 1:
        motivos.append("geometria")

    # espelhos
    se = score_espelhos(
        n,
        dados
    )

    score += se

    if se > .5:
        motivos.append("espelho")

    # transição
    stt = score_transicao(
        n,
        ultimo,
        matriz
    )

    score += stt

    if stt > .5:
        motivos.append("puxa")

    # matemática
    sm, mm = propriedades(n)

    score += sm
    motivos.extend(mm)

    # aritmética
    score += score_aritmetico(
        n,
        ultimo
    )

    # classificações
    score += score_classificacao(
        n,
        dados
    )

    # distância
    score += score_distancia(
        n,
        dados
    )

    return {
        "numero": n,
        "score": round(score, 3),
        "frequencia": dados.count(n),
        "atraso": atraso(n, dados),
        "zscore": round(z, 2),
        "cor": cor(n),
        "paridade": paridade(n),
        "duzia": duzia(n),
        "coluna": coluna(n),
        "setor": setor(n),
        "espelho_roda": er := espelho_roda(n),
        "espelho_numero": espelho_numerico(n),
        "motivos": motivos
    }


# ============================================================
# ANALISAR 37
# ============================================================

def analisar_37(dados, sentido):

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

    return ranking


# ============================================================
# BACKTEST
# ============================================================

def executar_backtest(
    dados,
    sentido
):

    if len(dados) < 40:
        return None

    acertos = 0
    total = 0

    # usa os dados anteriores
    # para prever cada próximo resultado
    inicio = max(
        20,
        len(dados) - 100
    )

    for i in range(
        inicio,
        len(dados)
    ):

        historico = dados[:i]

        ranking = analisar_37(
            historico,
            sentido
        )

        top22 = {
            x["numero"]
            for x in ranking[:22]
        }

        resultado = dados[i]

        if resultado in top22:
            acertos += 1

        total += 1

    if total == 0:
        return None

    return {
        "acertos": acertos,
        "total": total,
        "taxa": acertos / total * 100
    }


# ============================================================
# VALIDAR PREVISÃO ANTERIOR
# ============================================================

def validar_previsao(resultado):

    previsao = st.session_state.ultima_previsao

    if not previsao:
        return

    st.session_state.total_validacoes += 1

    if resultado in previsao:
        st.session_state.acertos += 1

    st.session_state.previsoes.append({
        "resultado": resultado,
        "previsao": previsao,
        "acerto": resultado in previsao
    })

    st.session_state.ultima_previsao = []


# ============================================================
# CHIPS
# ============================================================

def chips(numeros, top=False):

    html = ""

    classe = (
        "number-chip-top"
        if top
        else "number-chip"
    )

    for n in numeros:
        html += (
            f'<span class="{classe}">'
            f'{n:02d}'
            f'</span>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    "# 🎯 FIRE BLAZE ROBO"
)

st.caption(
    "Motor estatístico • matemático • roda • mesa • transições"
)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if not st.session_state.iniciado:

    st.markdown(
        '<div class="card">'
        '<div class="card-title">BASE INICIAL</div>'
        '<div style="font-size:25px;font-weight:800;">'
        'Até 200 resultados'
        '</div>'
        '<div class="mini">'
        'Cole o histórico da roleta para iniciar.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    texto = st.text_area(
        "Histórico",
        height=120,
        placeholder=(
            "Cole aqui os resultados...\n"
            "Exemplo: 32 15 19 4 21 2..."
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        sentido = st.selectbox(
            "Sentido da análise",
            ["Direita", "Esquerda"]
        )

    with col2:
        st.metric(
            "Janela principal",
            "200"
        )

    if st.button(
        "🚀 INICIAR ANÁLISE",
        use_container_width=True
    ):

        numeros = extrair_numeros(
            texto
        )

        if len(numeros) < 20:

            st.error(
                "Insira pelo menos 20 resultados."
            )

        elif len(numeros) > 200:

            st.error(
                "A carga inicial aceita no máximo 200 resultados."
            )

        else:

            st.session_state.historico = numeros
            st.session_state.ultimo = numeros[-1]
            st.session_state.sentido = sentido
            st.session_state.iniciado = True

            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

else:

    historico = st.session_state.historico

    # mantém análise limitada aos 200 mais recentes
    dados = historico[-MAX_ANALISE:]

    ultimo = dados[-1]

    sentido = st.session_state.sentido

    ranking = analisar_37(
        dados,
        sentido
    )

    top22 = ranking[:22]
    top5 = ranking[:5]

    numeros22 = [
        x["numero"]
        for x in top22
    ]

    # guarda previsão atual
    if (
        st.session_state.ultima_previsao
        != numeros22
    ):
        st.session_state.ultima_previsao = numeros22

    # ========================================================
    # CARDS PRINCIPAIS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            '<div class="card">'
            '<div class="card-title">'
            'ÚLTIMO RESULTADO'
            '</div>'
            f'<div class="result-number">{ultimo}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="card">'
            '<div class="card-title">'
            'BASE ANALISADA'
            '</div>'
            '<div class="card-value">'
            f'{len(dados)}'
            '</div>'
            '<div class="mini">'
            'últimos resultados'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:
        taxa = 0

        if st.session_state.total_validacoes:
            taxa = (
                st.session_state.acertos
                / st.session_state.total_validacoes
                * 100
            )

        st.markdown(
            '<div class="card">'
            '<div class="card-title">'
            'DESEMPENHO'
            '</div>'
            '<div class="card-value">'
            f'{taxa:.1f}%'
            '</div>'
            '<div class="mini">'
            'cobertura dos 22'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            '<div class="card">'
            '<div class="card-title">'
            'SENTIDO'
            '</div>'
            '<div class="card-value">'
            f'{sentido}'
            '</div>'
            '<div class="mini">'
            'automático'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # ========================================================
    # 22
    # ========================================================

    st.markdown(
        '<div class="section">'
        '<h2>🎯 22 NÚMEROS SELECIONADOS</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card">'
        '<div class="card-title">'
        'RANKING DOS 37 → TOP 22'
        '</div>',
        unsafe_allow_html=True
    )

    chips(numeros22)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # TOP 5
    # ========================================================

    st.markdown(
        '<div class="section">'
        '<h2>🏆 TOP 5</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    chips(
        [x["numero"] for x in top5],
        top=True
    )

    # ========================================================
    # VIZINHOS
    # ========================================================

    viz = vizinhos_roda(
        ultimo,
        2
    )

    st.markdown(
        '<div class="section">'
        '<h2>🎡 VIZINHOS DO ÚLTIMO</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    chips(viz)

    st.caption(
        "Ordem física padrão da roleta europeia."
    )

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Ranking",
        "🧮 Matemática",
        "🔗 Relações",
        "🎡 Roda",
        "📈 Desempenho"
    ])

    # ========================================================
    # TAB RANKING
    # ========================================================

    with tab1:

        st.subheader(
            "Ranking completo"
        )

        for i, item in enumerate(
            ranking,
            1
        ):

            marcador = "🎯" if i <= 22 else ""

            st.write(
                f"{marcador} "
                f"**{i:02d}. {item['numero']:02d}** "
                f"— score **{item['score']:.2f}** "
                f"| freq {item['frequencia']} "
                f"| atraso {item['atraso']} "
                f"| z {item['zscore']}"
            )

            if item["motivos"]:
                st.caption(
                    " • ".join(
                        dict.fromkeys(
                            item["motivos"]
                        )
                    )
                )

    # ========================================================
    # TAB MATEMÁTICA
    # ========================================================

    with tab2:

        st.subheader(
            "🔢 Análise matemática"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Primo",
                "SIM" if ultimo in PRIMOS else "NÃO"
            )

        with c2:
            st.metric(
                "Fibonacci",
                "SIM" if ultimo in FIBONACCI else "NÃO"
            )

        with c3:
            st.metric(
                "Quadrado",
                "SIM" if ultimo in QUADRADOS else "NÃO"
            )

        st.write(
            f"**Soma dos dígitos:** "
            f"{soma_digitos(ultimo)}"
        )

        st.write(
            f"**Cor:** {cor(ultimo)}"
        )

        st.write(
            f"**Paridade:** {paridade(ultimo)}"
        )

        st.write(
            f"**Faixa:** {faixa(ultimo)}"
        )

        st.write(
            f"**Dúzia:** {duzia(ultimo)}"
        )

        st.write(
            f"**Coluna:** {coluna(ultimo)}"
        )

        st.divider()

        st.subheader(
            "Janelas"
        )

        for janela in JANELAS:

            parte = dados[-janela:]

            if not parte:
                continue

            freq = Counter(parte)

            principais = freq.most_common(5)

            texto_freq = " • ".join(
                f"{n} ({q})"
                for n, q in principais
            )

            st.write(
                f"**Últimos {janela}:** "
                f"{texto_freq}"
            )

    # ========================================================
    # TAB RELAÇÕES
    # ========================================================

    with tab3:

        st.subheader(
            "🔗 Relações 'puxa'"
        )

        matriz = criar_transicoes(
            dados
        )

        relacoes = matriz[
            ultimo
        ].most_common()

        if relacoes:

            total = sum(
                matriz[ultimo].values()
            )

            for n, qtd in relacoes[:10]:

                percentual = (
                    qtd / total * 100
                )

                st.write(
                    f"**{ultimo} → {n}** "
                    f"| {qtd} vezes "
                    f"| {percentual:.2f}%"
                )

        else:

            st.info(
                "Ainda não existem transições suficientes."
            )

        st.divider()

        st.subheader(
            "🪞 Espelhos"
        )

        st.write(
            f"Espelho na roda: "
            f"**{espelho_roda(ultimo)}**"
        )

        st.write(
            f"Espelho numérico: "
            f"**{espelho_numerico(ultimo)}**"
        )

    # ========================================================
    # TAB RODA
    # ========================================================

    with tab4:

        st.subheader(
            "🎡 Geometria da roda"
        )

        st.write(
            f"Centro atual: **{ultimo}**"
        )

        st.write(
            f"Sentido: **{sentido}**"
        )

        st.write(
            "11 casas ao redor:"
        )

        chips(
            vizinhos_ampliados(
                ultimo
            )
        )

        st.divider()

        st.subheader(
            "📐 Distância dos Top 5"
        )

        for item in top5:

            n = item["numero"]

            d = distancia_roda(
                ultimo,
                n
            )

            st.write(
                f"{n:02d} → "
                f"{d} casas na roda"
            )

        st.divider()

        st.subheader(
            "🗺️ Mesa"

        )

        for item in top5:

            n = item["numero"]

            dm = distancia_mesa(
                ultimo,
                n
            )

            st.write(
                f"{n:02d} → "
                f"distância de mesa "
                f"{dm}"
            )

    # ========================================================
    # TAB DESEMPENHO
    # ========================================================

    with tab5:

        st.subheader(
            "📈 Validação"
        )

        total = (
            st.session_state.total_validacoes
        )

        acertos = (
            st.session_state.acertos
        )

        if total:

            percentual = (
                acertos / total * 100
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Testes",
                    total
                )

            with c2:
                st.metric(
                    "Acertos",
                    acertos
                )

            with c3:
                st.metric(
                    "Cobertura",
                    f"{percentual:.2f}%"
                )

        else:

            st.info(
                "Registre novos giros para começar a validar o modelo."
            )

        st.divider()

        if len(dados) >= 40:

            if st.button(
                "🧪 EXECUTAR BACKTEST",
                use_container_width=True
            ):

                resultado_bt = executar_backtest(
                    dados,
                    sentido
                )

                if resultado_bt:

                    st.success(
                        f"Backtest: "
                        f"{resultado_bt['acertos']}/"
                        f"{resultado_bt['total']} "
                        f"({resultado_bt['taxa']:.2f}%)"
                    )

    # ========================================================
    # NOVO GIRO
    # ========================================================

    st.markdown(
        '<div class="section">'
        '<h2>🎰 REGISTRAR NOVO GIRO</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        [3, 1]
    )

    with col1:

        novo = st.number_input(
            "Número que acabou de sair",
            min_value=0,
            max_value=36,
            value=0,
            step=1,
            key="novo_resultado"
        )

    with col2:

        st.write("")

        if st.button(
            "➕ REGISTRAR",
            use_container_width=True
        ):

            # valida a previsão anterior
            validar_previsao(
                int(novo)
            )

            # adiciona ao histórico infinito
            st.session_state.historico.append(
                int(novo)
            )

            st.session_state.ultimo = int(novo)

            st.rerun()

    # ========================================================
    # HISTÓRICO
    # ========================================================

    st.markdown(
        '<div class="section">'
        '<h2>📜 HISTÓRICO</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        f"Total acumulado: "
        f"{len(historico)} resultados • "
        f"Análise atual: últimos 200"
    )

    # últimos 200
    dados_hist = historico[-200:]

    for i in range(
        0,
        len(dados_hist),
        20
    ):

        linha = dados_hist[
            i:i + 20
        ]

        chips(linha)


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "⚠️ O ranking é uma pontuação estatística experimental. "
    "Roleta justa permanece aleatória; nenhum desses critérios "
    "garante o próximo resultado."
)
