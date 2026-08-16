import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev

# ============================================================
# FIRE BLAZE ROBO
# ============================================================

st.set_page_config(
    page_title="Fire Blaze Robo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MAX_ANALISE = 200
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

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 90% 0%,
            rgba(70,80,190,.20),
            transparent 32%
        ),
        radial-gradient(
            circle at 0% 10%,
            rgba(0,190,170,.10),
            transparent 28%
        ),
        #080b12;
}

.block-container {
    max-width: 1250px;
    padding-top: 1rem;
}

.card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.08),
        rgba(255,255,255,.025)
    );
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 16px;
    padding: 15px;
    margin: 6px 0;
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
}

.chip {
    display: inline-block;
    padding: 6px 9px;
    margin: 3px;
    border-radius: 9px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.12);
    font-weight: 700;
}

.topchip {
    display: inline-block;
    padding: 8px 11px;
    margin: 3px;
    border-radius: 10px;
    background: linear-gradient(
        135deg,
        rgba(0,190,170,.30),
        rgba(80,80,220,.25)
    );
    border: 1px solid rgba(100,220,210,.35);
    font-weight: 800;
}

.small {
    font-size: 11px;
    opacity: .65;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# ESTADO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultima_previsao" not in st.session_state:
    st.session_state.ultima_previsao = []

if "acertos" not in st.session_state:
    st.session_state.acertos = 0

if "validacoes" not in st.session_state:
    st.session_state.validacoes = 0

# ============================================================
# FUNÇÕES BÁSICAS
# ============================================================

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

        except ValueError:
            pass

    return resultado


def distancia_roda(a, b):

    d = abs(POS[a] - POS[b])

    return min(d, 37 - d)


def cor(n):

    if n == 0:
        return "Zero"

    if n in VERMELHOS:
        return "Vermelho"

    return "Preto"


def paridade(n):

    if n == 0:
        return "Zero"

    if n % 2 == 0:
        return "Par"

    return "Ímpar"


def faixa(n):

    if n == 0:
        return "Zero"

    if n <= 18:
        return "1–18"

    return "19–36"


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


def soma_digitos(n):

    return sum(int(x) for x in str(n))


def setor_roda(n):

    return POS[n] // 5


# ============================================================
# VIZINHOS E ESPELHOS
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


def vizinhos_ampliados(n, raio=5):

    p = POS[n]

    return [
        RODA[(p + i) % 37]
        for i in range(-raio, raio + 1)
    ]


def espelho_roda(n):

    return RODA[(POS[n] + 18) % 37]


def espelho_numerico(n):

    if n == 0:
        return 0

    return 37 - n


# ============================================================
# MESA
# ============================================================

def coordenada_mesa(n):

    if n == 0:
        return None

    return (
        (n - 1) // 3,
        (n - 1) % 3
    )


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

    total = sum(
        matriz[origem].values()
    )

    if total == 0:
        return 0.0

    return (
        matriz[origem][destino]
        / total
    )


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
        150: 0.8,
        200: 0.6
    }

    score = 0.0

    for janela, peso in pesos.items():

        parte = dados[-janela:]

        if not parte:
            continue

        frequencia = (
            parte.count(n)
            / len(parte)
        )

        score += (
            frequencia
            * 100
            * peso
        )

    return score


# ============================================================
# Z-SCORE
# ============================================================

def zscore_numero(n, dados):

    if not dados:
        return 0.0

    freq = Counter(dados)

    valores = [
        freq[x]
        for x in NUMEROS
    ]

    media = mean(valores)

    desvio = pstdev(valores)

    if desvio == 0:
        return 0.0

    return (
        freq[n] - media
    ) / desvio


# ============================================================
# ATRASO
# ============================================================

def score_atraso(n, dados):

    a = atraso(n, dados)

    if a <= 3:
        return 0.0

    return min(
        a * 0.08,
        3.0
    )


# ============================================================
# VIZINHANÇA
# ============================================================

def score_vizinhanca(n, dados):

    score = 0.0

    for resultado in dados[-30:]:

        d = distancia_roda(
            resultado,
            n
        )

        if d == 1:
            score += 0.8

        elif d == 2:
            score += 0.45

        elif d == 3:
            score += 0.15

    return score


# ============================================================
# SETOR
# ============================================================

def score_setor(n, dados):

    if not dados:
        return 0.0

    setor = setor_roda(n)

    quantidade = sum(
        setor_roda(x) == setor
        for x in dados[-50:]
    )

    return quantidade / 20


# ============================================================
# DIREÇÃO
# ============================================================

def score_direcao(n, dados, sentido):

    if not dados:
        return 0.0

    ultimo = dados[-1]

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

    if distancia_roda(ultimo, n) <= 5:
        return 0.4

    return 0.0


# ============================================================
# GEOMETRIA DA MESA
# ============================================================

def score_geometria(n, dados):

    if len(dados) < 2 or n == 0:
        return 0.0

    ultimo = dados[-1]

    score = 0.0

    dm = distancia_mesa(
        ultimo,
        n
    )

    if dm == 1:
        score += 2.0

    elif dm == 2:
        score += 1.0

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

        if movimento_anterior == movimento_atual:
            score += 1.5

        if movimento_anterior == (
            -movimento_atual[0],
            -movimento_atual[1]
        ):
            score += 1.5

        if (
            abs(movimento_atual[0]) == 1
            and
            abs(movimento_atual[1]) == 1
        ):
            score += 0.7

    return score


# ============================================================
# ESPELHOS
# ============================================================

def score_espelhos(n, dados):

    espelho1 = espelho_roda(n)

    espelho2 = espelho_numerico(n)

    return (
        dados.count(espelho1) * 0.12
        +
        dados.count(espelho2) * 0.08
    )


# ============================================================
# ARITMÉTICA
# ============================================================

def score_aritmetico(n, ultimo):

    if n == ultimo:
        return 0.3

    diferenca = abs(
        n - ultimo
    )

    score = 0.0

    if diferenca in {
        1, 2, 3, 4, 5
    }:
        score += 0.5

    soma = n + ultimo

    if soma % 3 == 0:
        score += 0.15

    if soma % 5 == 0:
        score += 0.15

    if soma % 7 == 0:
        score += 0.10

    return score


# ============================================================
# TRANSIÇÃO
# ============================================================

def score_transicao(
    n,
    ultimo,
    matriz
):

    return (
        forca_transicao(
            ultimo,
            n,
            matriz
        )
        * 10
    )


# ============================================================
# DISTÂNCIA
# ============================================================

def score_distancia(n, dados):

    recentes = dados[-10:]

    if not recentes:
        return 0.0

    media_distancia = mean(
        distancia_roda(n, x)
        for x in recentes
    )

    return max(
        0.0,
        3.0 - media_distancia * 0.18
    )


# ============================================================
# CLASSIFICAÇÕES
# ============================================================

def score_classificacao(n, dados):

    recentes = [
        x
        for x in dados[-30:]
        if x != 0
    ]

    if not recentes:
        return 0.0

    score = 0.0

    score += (
        sum(
            cor(x) == cor(n)
            for x in recentes
        )
        / 100
    )

    score += (
        sum(
            paridade(x) == paridade(n)
            for x in recentes
        )
        / 100
    )

    score += (
        sum(
            faixa(x) == faixa(n)
            for x in recentes
        )
        / 100
    )

    score += (
        sum(
            duzia(x) == duzia(n)
            for x in recentes
        )
        / 100
    )

    score += (
        sum(
            coluna(x) == coluna(n)
            for x in recentes
        )
        / 100
    )

    return score


# ============================================================
# MATEMÁTICA
# ============================================================

def score_matematica(n):

    score = 0.0

    motivos = []

    if n in PRIMOS:

        score += 0.35

        motivos.append(
            "primo"
        )

    if n in FIBONACCI:

        score += 0.35

        motivos.append(
            "Fibonacci"
        )

    if n in QUADRADOS:

        score += 0.20

        motivos.append(
            "quadrado"
        )

    for divisor in [
        2, 3, 4, 5, 6, 7, 9
    ]:

        if (
            n != 0
            and n % divisor == 0
        ):
            score += 0.04

    if (
        n != 0
        and soma_digitos(n) in PRIMOS
    ):

        score += 0.12

        motivos.append(
            "soma-prima"
        )

    return score, motivos


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

    score = 0.0

    motivos = []

    sf = score_frequencia(
        n,
        dados
    )

    score += sf

    if sf > 3:
        motivos.append(
            "frequência"
        )

    sa = score_atraso(
        n,
        dados
    )

    score += sa

    if sa > 0.5:
        motivos.append(
            "atraso"
        )

    z = zscore_numero(
        n,
        dados
    )

    score += z * 0.7

    if z > 1:
        motivos.append(
            "z-score alto"
        )

    if z < -1:
        motivos.append(
            "z-score baixo"
        )

    sv = score_vizinhanca(
        n,
        dados
    )

    score += sv

    if sv > 1:
        motivos.append(
            "vizinhança"
        )

    score += score_setor(
        n,
        dados
    )

    sd = score_direcao(
        n,
        dados,
        sentido
    )

    score += sd

    if sd > 1:
        motivos.append(
            "direção"
        )

    sg = score_geometria(
        n,
        dados
    )

    score += sg

    if sg > 1:
        motivos.append(
            "geometria"
        )

    se = score_espelhos(
        n,
        dados
    )

    score += se

    if se > 0.5:
        motivos.append(
            "espelho"
        )

    st = score_transicao(
        n,
        ultimo,
        matriz
    )

    score += st

    if st > 0.5:
        motivos.append(
            "puxa"
        )

    sm, mm = score_matematica(n)

    score += sm

    motivos.extend(mm)

    score += score_aritmetico(
        n,
        ultimo
    )

    score += score_classificacao(
        n,
        dados
    )

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
        "faixa": faixa(n),
        "duzia": duzia(n),
        "coluna": coluna(n),
        "setor": setor_roda(n),
        "espelho_roda": espelho_roda(n),
        "espelho_numero": espelho_numerico(n),
        "motivos": motivos
    }


# ============================================================
# RANKING
# ============================================================

def analisar(
    dados,
    sentido
):

    dados = dados[-MAX_ANALISE:]

    matriz = criar_transicoes(
        dados
    )

    ranking = []

    for n in NUMEROS:

        item = calcular_numero(
            n,
            dados,
            matriz,
            sentido
        )

        ranking.append(item)

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking


# ============================================================
# BACKTEST
# ============================================================

def backtest(
    dados,
    sentido,
    quantidade=22
):

    if len(dados) < 40:
        return None

    acertos = 0
    total = 0

    inicio = max(
        30,
        len(dados) - 100
    )

    for i in range(
        inicio,
        len(dados)
    ):

        historico = dados[:i]

        ranking = analisar(
            historico,
            sentido
        )

        escolhas = {
            x["numero"]
            for x in ranking[:quantidade]
        }

        if dados[i] in escolhas:
            acertos += 1

        total += 1

    if total == 0:
        return None

    return {
        "acertos": acertos,
        "total": total,
        "taxa": (
            acertos
            / total
            * 100
        )
    }


# ============================================================
# CHIPS
# ============================================================

def mostrar_chips(
    numeros,
    destaque=False
):

    classe = (
        "topchip"
        if destaque
        else "chip"
    )

    html = ""

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
# INTERFACE
# ============================================================

st.title(
    "🎯 FIRE BLAZE ROBO"
)

st.caption(
    "Estatística • matemática • roda • mesa • espelhos • transições"
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        """
        <div class="card">
        <div class="card-title">
        HISTÓRICO MÁXIMO
        </div>
        <div class="card-value">
        200
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        """
        <div class="card">
        <div class="card-title">
        ESCOLHAS
        </div>
        <div class="card-value">
        22
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        """
        <div class="card">
        <div class="card-title">
        NÚMEROS ANALISADOS
        </div>
        <div class="card-value">
        37
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.subheader(
    "📥 Histórico da roleta"
)

texto = st.text_area(
    "Cole aqui os últimos resultados",
    height=140,
    placeholder=(
        "Exemplo:\n"
        "32 23 13 35 4 20 4 14 12 4"
    )
)

col1, col2 = st.columns(2)

with col1:

    sentido = st.selectbox(
        "Sentido analisado",
        [
            "Direita",
            "Esquerda"
        ]
    )

with col2:

    quantidade = st.number_input(
        "Quantidade de escolhas",
        min_value=1,
        max_value=37,
        value=22,
        step=1
    )


if texto.strip():

    novos = extrair_numeros(
        texto
    )

    if novos:

        st.session_state.historico = (
            novos[-MAX_ANALISE:]
        )


if st.button(
    "🗑️ Limpar histórico",
    use_container_width=True
):

    st.session_state.historico = []

    st.session_state.ultima_previsao = []

    st.session_state.acertos = 0

    st.session_state.validacoes = 0

    st.rerun()


dados = st.session_state.historico


if len(dados) < 5:

    st.info(
        "Cole pelo menos 5 resultados. "
        "Para uma análise mais completa, use até 200."
    )

else:

    ranking = analisar(
        dados,
        sentido
    )

    escolhas = ranking[
        :int(quantidade)
    ]

    numeros_escolhidos = [
        x["numero"]
        for x in escolhas
    ]

    st.session_state.ultima_previsao = (
        numeros_escolhidos
    )


    st.subheader(
        "🔥 ESCOLHAS DO ROBÔ"
    )

    mostrar_chips(
        numeros_escolhidos,
        True
    )


    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        SITUAÇÃO ATUAL
        </div>

        <div class="card-value">
        Último: {dados[-1]}
        </div>

        <div class="small">
        {len(dados)} resultados analisados
        • Sentido: {sentido}
        • Janela máxima: 200
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.subheader(
        "🏆 TOP 5"
    )

    mostrar_chips(
        [
            x["numero"]
            for x in ranking[:5]
        ],
        True
    )


    st.subheader(
        "📊 Ranking dos 37 números"
    )

    tabela = []

    for posicao, item in enumerate(
        ranking,
        start=1
    ):

        tabela.append(
            {
                "Posição": posicao,
                "Número": item["numero"],
                "Score": item["score"],
                "Frequência": item["frequencia"],
                "Atraso": item["atraso"],
                "Z-score": item["zscore"],
                "Cor": item["cor"],
                "Paridade": item["paridade"],
                "Dúzia": item["duzia"],
                "Coluna": item["coluna"],
                "Espelho": item["espelho_roda"],
                "Motivos": ", ".join(
                    dict.fromkeys(
                        item["motivos"]
                    )
                )
            }
        )


    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )


    st.subheader(
        "🔍 Detalhamento das escolhas"
    )


    for item in escolhas:

        motivos = ", ".join(
            dict.fromkeys(
                item["motivos"]
            )
        )

        st.markdown(
            f"""
            <div class="card">

            <b>#{item["numero"]}</b>

            — Score:
            <b>{item["score"]}</b>

            • Frequência:
            {item["frequencia"]}

            • Atraso:
            {item["atraso"]}

            • Espelho roda:
            {item["espelho_roda"]}

            • Espelho numérico:
            {item["espelho_numero"]}

            <br>

            <span class="small">
            Motivos:
            {motivos if motivos else "combinação estatística"}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.subheader(
        "🎡 Vizinhança do último resultado"
    )

    mostrar_chips(
        vizinhos_ampliados(
            dados[-1],
            5
        )
    )


    st.subheader(
        "📜 Últimos 30 resultados"
    )

    mostrar_chips(
        list(
            reversed(
                dados[-30:]
            )
        )
    )


    st.subheader(
        "🧪 Backtest"
    )

    resultado = backtest(
        dados,
        sentido,
        int(quantidade)
    )


    if resultado:

        b1, b2, b3 = st.columns(3)

        with b1:
            st.metric(
                "Acertos",
                resultado["acertos"]
            )

        with b2:
            st.metric(
                "Testes",
                resultado["total"]
            )

        with b3:
            st.metric(
                "Cobertura",
                f'{resultado["taxa"]:.1f}%'
            )

        st.caption(
            "Backtest é uma avaliação histórica. "
            "Ele não garante o próximo resultado."
        )

    else:

        st.info(
            "Use pelo menos 40 resultados "
            "para executar o backtest."
        )


    st.subheader(
        "🎯 Validar próxima rodada"
    )

    resultado_atual = st.number_input(
        "Digite o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )


    if st.button(
        "✅ VALIDAR RESULTADO",
        use_container_width=True
    ):

        st.session_state.validacoes += 1

        if (
            resultado_atual
            in st.session_state.ultima_previsao
        ):

            st.session_state.acertos += 1

            st.success(
                "O resultado estava entre as escolhas."
            )

        else:

            st.error(
                "O resultado não estava entre as escolhas."
            )

        st.session_state.ultima_previsao = []


    if st.session_state.validacoes > 0:

        taxa_validacao = (
            st.session_state.acertos
            /
            st.session_state.validacoes
            * 100
        )

        st.metric(
            "Taxa das validações",
            f"{taxa_validacao:.1f}%"
        )


st.divider()

st.caption(
    "Fire Blaze Robo • análise experimental. "
    "Roleta é aleatória; padrões históricos não garantem o próximo resultado."
)
