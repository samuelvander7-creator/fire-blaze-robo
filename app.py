import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="ROBÔ RICO",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, #061824 0%, #02070d 45%, #080511 100%);
    color: #eef3f8;
}

.block-container {
    max-width: 1400px;
    padding: 22px 18px 35px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    display: none;
}

/* LOGO */

.logo {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 5px;
}

.logo-icon {
    font-size: 52px;
    line-height: 1;
}

.logo-title {
    font-size: 44px;
    font-weight: 900;
    letter-spacing: -2px;
}

.rico {
    color: #18c85b;
}

.subtitle {
    color: #aab5c3;
    font-size: 17px;
    margin-left: 2px;
}

/* DIREÇÃO */

.dirbox {
    border: 1px solid #263647;
    border-radius: 12px;
    padding: 12px 18px;
    text-align: center;
    background: #07121c;
}

.dirlabel {
    font-size: 13px;
    color: #c8d0d9;
}

.dir {
    font-size: 26px;
    font-weight: 900;
    color: #19c95b;
}

.auto {
    font-size: 12px;
    color: #a8b2bd;
}

/* CARDS */

.card {
    background:
        linear-gradient(
            145deg,
            rgba(5,22,34,.95),
            rgba(3,10,17,.95)
        );

    border: 1px solid #263847;
    border-radius: 12px;
    padding: 17px;

    height: 100%;

    box-shadow:
        0 8px 24px rgba(0,0,0,.16);
}

.kicker {
    font-size: 13px;
    color: #b9c3cd;
    text-transform: uppercase;
}

.big {
    font-size: 40px;
    font-weight: 900;
    line-height: 1.1;
    margin: 8px 0;
}

.blue {
    color: #168cff;
}

.green {
    color: #18c95b;
}

.purple {
    color: #a64cff;
}

.cyan {
    color: #11c5e8;
}

.muted {
    color: #aab5c3;
}

.bar {
    height: 8px;
    background: #14222d;
    border-radius: 10px;
    overflow: hidden;
}

.bar span {
    display: block;
    height: 100%;
    border-radius: 10px;
    background: #168cff;
}

/* SEÇÕES */

.section {
    font-size: 24px;
    font-weight: 800;
    margin: 20px 0 12px;
}

/* ESCOLHAS */

.choice {
    border-radius: 11px;
    padding: 18px;
    min-height: 210px;
    background: #06131d;
}

.choice.high {
    border: 1px solid #08b958;
}

.choice.poss {
    border: 1px solid #168cff;
}

.choice.mark {
    border: 1px solid #ffae00;
}

.choice-title {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 18px;
}

.high .choice-title {
    color: #12d965;
}

.poss .choice-title {
    color: #168cff;
}

.mark .choice-title {
    color: #ffae00;
}

/* NÚMEROS */

.chips {
    display: flex;
    flex-wrap: wrap;
    gap: 13px;
}

.chip {
    width: 50px;
    height: 50px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 1px solid #76808a;
    background: #05080b;

    font-size: 17px;
    font-weight: 800;
}

.red {
    background: #df2631;
    border-color: #ff4b54;
}

.greenchip {
    background: #16a94d;
    border-color: #28db6c;
}

.choice-foot {
    margin-top: 22px;
    padding-top: 12px;

    border-top: 1px solid rgba(255,255,255,.12);

    font-size: 12px;
    color: #8da2b2;
}

/* RANKING */

.rank-row {
    display: grid;

    grid-template-columns:
        30px
        1fr
        70px;

    gap: 8px;

    padding: 9px 0;

    border-bottom:
        1px solid rgba(255,255,255,.08);
}

.rank-score {
    color: #18c95b;
    font-weight: 800;
    text-align: right;
}

/* MÉTRICAS */

.mini-line {
    display: flex;
    justify-content: space-between;

    padding: 8px 0;

    border-bottom:
        1px solid rgba(255,255,255,.07);
}

/* FOOTER */

.footer {
    text-align: center;
    color: #8b98a6;
    font-size: 12px;
    margin-top: 20px;
}

/* MOBILE */

@media(max-width:900px) {

    .logo-title {
        font-size: 31px;
    }

    .subtitle {
        font-size: 13px;
    }

    .big {
        font-size: 31px;
    }

    .section {
        font-size: 20px;
    }

    .chip {
        width: 43px;
        height: 43px;
    }

    .block-container {
        padding: 14px 10px 30px;
    }

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

POS = {
    n: i
    for i, n in enumerate(RODA)
}

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
    0, 1, 2, 3, 5,
    8, 13, 21, 34
}

QUADRADOS = {
    0, 1, 4, 9,
    16, 25, 36
}


# ============================================================
# MEMÓRIA
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []


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

    return numeros[-200:]


def cor(numero):

    if numero == 0:
        return "verde"

    if numero in VERMELHOS:
        return "vermelho"

    return "preto"


def classe_chip(numero):

    if numero == 0:
        return "greenchip"

    if numero in VERMELHOS:
        return "red"

    return ""


def distancia_roda(a, b):

    distancia = abs(
        POS[a] - POS[b]
    )

    return min(
        distancia,
        37 - distancia
    )


def criar_transicoes(dados):

    matriz = defaultdict(Counter)

    for atual, proximo in zip(
        dados,
        dados[1:]
    ):

        matriz[atual][proximo] += 1

    return matriz


# ============================================================
# SCORE
# ============================================================

def calcular_score(
    numero,
    dados,
    matriz
):

    if not dados:
        return 0

    ultimo = dados[-1]

    score = 0

    # ----------------------------
    # FREQUÊNCIA
    # ----------------------------

    janelas = [
        (10, 3.0),
        (20, 2.4),
        (37, 1.8),
        (50, 1.3),
        (100, .8),
        (150, .55),
        (200, .35)
    ]

    for tamanho, peso in janelas:

        janela = dados[-tamanho:]

        if janela:

            frequencia = (
                janela.count(numero)
                / len(janela)
            )

            score += (
                frequencia
                * 100
                * peso
            )

    # ----------------------------
    # ATRASO
    # ----------------------------

    if numero in dados:

        ultimo_indice = (
            len(dados)
            - 1
            - dados[::-1].index(numero)
        )

        atraso = (
            len(dados)
            - 1
            - ultimo_indice
        )

    else:

        atraso = len(dados)

    score += min(
        atraso * .055,
        2.5
    )

    # ----------------------------
    # VIZINHANÇA DA RODA
    # ----------------------------

    for resultado in dados[-25:]:

        distancia = distancia_roda(
            numero,
            resultado
        )

        if distancia == 1:
            score += .25

        elif distancia == 2:
            score += .12

    # ----------------------------
    # TRANSIÇÃO
    # ----------------------------

    total = sum(
        matriz[ultimo].values()
    )

    if total > 0:

        probabilidade_transicao = (
            matriz[ultimo][numero]
            / total
        )

        score += (
            probabilidade_transicao
            * 12
        )

    # ----------------------------
    # ESPELHO NA RODA
    # ----------------------------

    espelho = RODA[
        (POS[numero] + 18) % 37
    ]

    score += (
        dados.count(espelho)
        * .12
    )

    # ----------------------------
    # MATEMÁTICA
    # ----------------------------

    if numero in PRIMOS:
        score += .30

    if numero in FIBONACCI:
        score += .25

    if numero in QUADRADOS:
        score += .15

    if numero != 0 and numero % 3 == 0:
        score += .08

    if numero != 0 and numero % 2 == 0:
        score += .05

    return score


# ============================================================
# RANKING
# ============================================================

def gerar_ranking(dados):

    matriz = criar_transicoes(
        dados
    )

    ranking = []

    for numero in range(37):

        score = calcular_score(
            numero,
            dados,
            matriz
        )

        ranking.append(
            (
                numero,
                score
            )
        )

    ranking.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranking


# ============================================================
# 22 ESCOLHAS
# ============================================================

def gerar_escolhas(ranking):

    tendencia_alta = [
        numero
        for numero, score
        in ranking[:8]
    ]

    possiveis = [
        numero
        for numero, score
        in ranking[8:15]
    ]

    marcacao = [
        numero
        for numero, score
        in ranking[15:22]
    ]

    return (
        tendencia_alta,
        possiveis,
        marcacao
    )


# ============================================================
# BACKTEST
# ============================================================

def executar_backtest(dados):

    if len(dados) < 45:

        return {
            "acertos": 0,
            "testes": 0,
            "taxa": 0
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

        ranking = gerar_ranking(
            historico
        )

        escolhas = {
            numero
            for numero, score
            in ranking[:22]
        }

        resultado = dados[i]

        if resultado in escolhas:
            acertos += 1

        testes += 1

    taxa = (
        acertos / testes * 100
        if testes
        else 0
    )

    return {
        "acertos": acertos,
        "testes": testes,
        "taxa": taxa
    }


# ============================================================
# CHIPS
# ============================================================

def mostrar_chips(numeros):

    html = '<div class="chips">'

    for numero in numeros:

        classe = classe_chip(
            numero
        )

        html += (
            f'<span class="chip {classe}">'
            f'{numero}'
            f'</span>'
        )

    html += '</div>'

    return html


# ============================================================
# CABEÇALHO
# ============================================================

cab1, cab2 = st.columns(
    [3.8, 1.2]
)

with cab1:

    st.markdown(
        """
        <div class="logo">

            <div class="logo-icon">
                🎯💵
            </div>

            <div>

                <div class="logo-title">
                    ROBÔ
                    <span class="rico">
                        RICO
                    </span>
                    🤑
                </div>

                <div class="subtitle">
                    Estatística • Matemática • Roda • Mesa • Transições • Espelhos
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with cab2:

    sentido = st.selectbox(
        "Sentido atual",
        [
            "Direita",
            "Esquerda"
        ]
    )

    st.markdown(
        f"""
        <div class="dirbox">

            <div class="dirlabel">
                Sentido atual
            </div>

            <div class="dir">
                → {sentido}
            </div>

            <div class="auto">
                Automático
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DADOS
# ============================================================

historico = st.session_state.historico

ultimo = (
    historico[-1]
    if historico
    else None
)

ranking = gerar_ranking(
    historico
)

tendencia, possiveis, marcacao = (
    gerar_escolhas(ranking)
)

backtest = executar_backtest(
    historico
)


# ============================================================
# CARDS SUPERIORES
# ============================================================

colunas = st.columns(5)

dados_cards = [

    (
        "ÚLTIMO RESULTADO",
        str(ultimo)
        if ultimo is not None
        else "—",
        "",
        "green"
    ),

    (
        "BASE ANALISADA",
        str(len(historico)),
        "últimos resultados",
        "blue"
    ),

    (
        "DESEMPENHO (22)",
        f'{backtest["taxa"]:.1f}%',
        "cobertura histórica",
        "green"
    ),

    (
        "ESCOLHAS DO ROBÔ",
        "22",
        "números selecionados",
        "purple"
    ),

    (
        "TRANSIÇÕES",
        f'{max(0,len(historico)-1):,}'.replace(",", "."),
        "puxas observadas",
        "cyan"
    )

]

for coluna, dados in zip(
    colunas,
    dados_cards
):

    titulo, valor, descricao, classe = dados

    with coluna:

        st.markdown(
            f"""
            <div class="card">

                <div class="kicker">
                    {titulo}
                </div>

                <div class="big {classe}">
                    {valor}
                </div>

                <div class="muted">
                    {descricao}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ESCOLHAS
# ============================================================

st.markdown(
    '<div class="section">🔥 ESCOLHAS DO ROBÔ</div>',
    unsafe_allow_html=True
)

a, b, c, ranking_col = st.columns(
    [1, 1, 1, .72]
)


# TENDÊNCIA ALTA

with a:

    st.markdown(
        f"""
        <div class="choice high">

            <div class="choice-title">
                📈 8 NÚMEROS COM TENDÊNCIA ALTA
            </div>

            {mostrar_chips(tendencia)}

            <div class="choice-foot">
                📈 Maior força estatística no momento
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# POSSÍVEIS

with b:

    st.markdown(
        f"""
        <div class="choice poss">

            <div class="choice-title">
                ❓ 7 NÚMEROS COMO POSSÍVEL
            </div>

            {mostrar_chips(possiveis)}

            <div class="choice-foot">
                ℹ️ Números com boa chance secundária
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# MARCAÇÃO

with c:

    st.markdown(
        f"""
        <div class="choice mark">

            <div class="choice-title">
                🎯 7 NÚMEROS COMO MARCAÇÃO
            </div>

            {mostrar_chips(marcacao)}

            <div class="choice-foot">
                🛡️ Números para cobertura e proteção
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TOP 5
# ============================================================

with ranking_col:

    html = """
    <div class="card">

        <div class="section"
             style="font-size:16px;margin-top:0">

            👑 TOP 5 GERAL

        </div>
    """

    for posicao, (
        numero,
        score
    ) in enumerate(
        ranking[:5],
        1
    ):

        html += f"""
        <div class="rank-row">

            <span>
                {posicao}
            </span>

            <strong>
                {numero}
            </strong>

            <span class="rank-score">
                {score:.1f}
            </span>

        </div>
        """

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# RESUMO
# ============================================================

st.markdown(
    '<div class="section">📊 RESUMO DA ANÁLISE</div>',
    unsafe_allow_html=True
)

frequencias = [
    historico.count(n)
    for n in range(37)
]

media_frequencia = (
    mean(frequencias)
    if historico
    else 0
)

maior_frequencia = (
    max(frequencias)
    if frequencias
    else 0
)

atrasos = []

for numero in range(37):

    if numero in historico:

        indice = (
            len(historico)
            - 1
            - historico[::-1].index(numero)
        )

        atraso = (
            len(historico)
            - 1
            - indice
        )

        atrasos.append(
            atraso
        )

maior_atraso = (
    max(atrasos)
    if atrasos
    else 0
)

atraso_medio = (
    mean(atrasos)
    if atrasos
    else 0
)

colunas = st.columns(5)

metricas = [

    (
        "FREQUÊNCIA (200)",
        f"{media_frequencia:.2f}",
        f"Máx: {maior_frequencia}",
        "blue"
    ),

    (
        "ATRASO MÉDIO",
        f"{atraso_medio:.1f}",
        f"Máx: {maior_atraso}",
        "purple"
    ),

    (
        "Z-SCORE MÉDIO",
        "0.00",
        "normalização",
        "green"
    ),

    (
        "MAIOR ATRASO",
        str(maior_atraso),
        "entre os 37 números",
        "blue"
    ),

    (
        "TRANSIÇÕES",
        f'{max(0,len(historico)-1):,}'.replace(",", "."),
        "Puxas observadas",
        "cyan"
    )

]

for coluna, dados in zip(
    colunas,
    metricas
):

    titulo, valor, descricao, classe = dados

    with coluna:

        st.markdown(
            f"""
            <div class="card">

                <div class="kicker">
                    {titulo}
                </div>

                <div class="big {classe}">
                    {valor}
                </div>

                <div class="muted">
                    {descricao}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PADRÕES
# ============================================================

a, b, c = st.columns(
    [1, 1, 1.2]
)


# CORES

with a:

    total = max(
        1,
        len(historico)
    )

    vermelhos = sum(
        n in VERMELHOS
        for n in historico
    )

    pretos = sum(
        n != 0 and n not in VERMELHOS
        for n in historico
    )

    verdes = historico.count(0)

    st.markdown(
        f"""
        <div class="card">

            <div class="section"
                 style="font-size:17px;margin-top:0">

                RESUMO DE CORES

            </div>

            🔴 Vermelhos
            <strong>
                {vermelhos / total * 100:.1f}%
            </strong>

            <br><br>

            ⚫ Pretos
            <strong>
                {pretos / total * 100:.1f}%
            </strong>

            <br><br>

            🟢 Verdes
            <strong>
                {verdes / total * 100:.1f}%
            </strong>

        </div>
        """,
        unsafe_allow_html=True
    )


# MATEMÁTICA

with b:

    st.markdown(
        """
        <div class="card">

            <div class="section"
                 style="font-size:17px;margin-top:0">

                PADRÕES NUMÉRICOS

            </div>
        """,
        unsafe_allow_html=True
    )

    padroes = [

        (
            "Primos",
            sum(
                n in PRIMOS
                for n in historico
            )
        ),

        (
            "Fibonacci",
            sum(
                n in FIBONACCI
                for n in historico
            )
        ),

        (
            "Quadrados",
            sum(
                n in QUADRADOS
                for n in historico
            )
        ),

        (
            "Múltiplos de 3",
            sum(
                n != 0 and n % 3 == 0
                for n in historico
            )
        ),

        (
            "Múltiplos de 2",
            sum(
                n != 0 and n % 2 == 0
                for n in historico
            )
        )

    ]

    for nome, valor in padroes:

        st.markdown(
            f"""
            <div class="mini-line">

                <span>
                    {nome}
                </span>

                <strong>
                    {valor}
                </strong>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# JANELAS

with c:

    st.markdown(
        """
        <div class="card">

            <div class="section"
                 style="font-size:17px;margin-top:0">

                ÚLTIMAS JANELAS

            </div>
        """,
        unsafe_allow_html=True
    )

    for tamanho in [
        10,
        20,
        37,
        50,
        100,
        150,
        200
    ]:

        if historico:

            valor = historico[
                -tamanho
            ] if len(historico) >= tamanho else historico[0]

            st.markdown(
                f"""
                <div class="mini-line">

                    <span>
                        Últimos {tamanho}
                    </span>

                    <strong>
                        {valor}
                    </strong>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# HISTÓRICO / BACKTEST
# ============================================================

st.markdown(
    '<div class="section">📋 HISTÓRICO E DESEMPENHO</div>',
    unsafe_allow_html=True
)

a, b, c = st.columns(
    [1.3, 1, 1]
)


with a:

    st.markdown(
        f"""
        <div class="card">

            <div class="kicker">
                HISTÓRICO RECENTE (últimos 20)
            </div>

            {mostrar_chips(historico[-20:])}

        </div>
        """,
        unsafe_allow_html=True
    )


with b:

    taxa = backtest["taxa"]

    st.markdown(
        f"""
        <div class="card">

            <div class="kicker">
                TESTE DE COBERTURA (BACKTEST)
            </div>

            <div class="big green">
                {backtest["acertos"]}
            </div>

            <div class="muted">
                Acertos de {backtest["testes"]}
                testes
            </div>

            <div class="muted">
                Cobertura:
                {taxa:.1f}%
            </div>

            <div class="bar">
                <span style="width:{min(taxa,100):.1f}%"></span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c:

    erros = max(
        0,
        backtest["testes"]
        - backtest["acertos"]
    )

    st.markdown(
        f"""
        <div class="card">

            <div class="kicker">
                DETALHES DESEMPENHO (22)
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-top:20px;
            ">

                <div>
                    Acertos

                    <strong
                        class="green"
                        style="
                        display:block;
                        font-size:28px;
                    ">
                        {backtest["acertos"]}
                    </strong>
                </div>

                <div>
                    Erros

                    <strong
                        style="
                        display:block;
                        font-size:28px;
                        color:#ff3344;
                    ">
                        {erros}
                    </strong>
                </div>

                <div>
                    Total

                    <strong
                        style="
                        display:block;
                        font-size:28px;
                    ">
                        {backtest["testes"]}
                    </strong>
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
    '<div class="section">➕ NOVO RESULTADO / IMPORTAR HISTÓRICO</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(
    [1, 2]
)


with col1:

    novo_numero = st.number_input(
        "Digite o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )

    if st.button(
        "➕ ADICIONAR & ATUALIZAR",
        use_container_width=True
    ):

        st.session_state.historico = (
            st.session_state.historico
            + [int(novo_numero)]
        )[-200:]

        st.rerun()


with col2:

    texto = st.text_area(
        "Cole aqui os últimos resultados",
        height=100,
        placeholder=(
            "Exemplo: "
            "32 23 13 35 4 20 4 14 12 4"
        )
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "📋 CARREGAR DADOS COLADOS",
            use_container_width=True
        ):

            dados = extrair_numeros(
                texto
            )

            if dados:

                st.session_state.historico = dados

                st.rerun()

    with c2:

        if st.button(
            "🗑️ LIMPAR HISTÓRICO",
            use_container_width=True
        ):

            st.session_state.historico = []

            st.rerun()


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">

        🛡️ Jogue com responsabilidade.
        Este sistema é apenas para análise estatística.

    </div>
    """,
    unsafe_allow_html=True
)
