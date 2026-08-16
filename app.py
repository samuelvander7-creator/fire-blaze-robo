import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev

st.set_page_config(
    page_title="ROBÔ RICO",
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#061018 0%,#07131d 55%,#0b0916 100%);
    color: #e8eef5;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.card {
    background: rgba(9,23,34,.88);
    border: 1px solid rgba(130,170,200,.22);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

.small {
    color: #9eacba;
    font-size: 13px;
}

.big {
    font-size: 32px;
    font-weight: 800;
    line-height: 1.1;
}

.green { color: #20d85a; }
.blue { color: #2196f3; }
.purple { color: #a855f7; }
.orange { color: #ff9d00; }
.cyan { color: #16c7df; }
.red { color: #ef4444; }

.choice {
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 14px;
    padding: 16px;
    min-height: 190px;
}

.choice h3 {
    margin: 0 0 14px 0;
    font-size: 17px;
}

.choice.high {
    border-color: rgba(32,216,90,.5);
}

.choice.possible {
    border-color: rgba(33,150,243,.5);
}

.choice.mark {
    border-color: rgba(255,157,0,.5);
}

.chip {
    display: inline-block;
    min-width: 36px;
    text-align: center;
    padding: 8px 7px;
    margin: 4px;
    border-radius: 50%;
    background: #05090d;
    border: 1px solid #52606d;
    font-weight: 700;
}

.chip.red {
    background: #d92735;
    border-color: #f34a55;
}

.chip.green {
    background: #159447;
    border-color: #31c96a;
}

.note {
    margin-top: 14px;
    padding: 9px 10px;
    border-top: 1px solid rgba(255,255,255,.08);
    font-size: 12px;
    color: #aebbc7;
}

div[data-testid="stMetric"] {
    background: rgba(9,23,34,.88);
    border: 1px solid rgba(130,170,200,.22);
    padding: 12px;
    border-radius: 14px;
}

button[kind="primary"] {
    background: #18a84a !important;
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
    0, 1, 4, 9, 16,
    25, 36
}

MAX_HISTORICO = 200


# ============================================================
# MEMÓRIA DO STREAMLIT
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []


# ============================================================
# FUNÇÕES
# ============================================================

def extrair_numeros(texto):

    for caractere in [",", ";", "\n", "\t", "|"]:
        texto = texto.replace(caractere, " ")

    numeros = []

    for item in texto.split():

        try:
            numero = int(item)

            if 0 <= numero <= 36:
                numeros.append(numero)

        except ValueError:
            pass

    return numeros


def cor(numero):

    if numero == 0:
        return "Verde"

    if numero in VERMELHOS:
        return "Vermelho"

    return "Preto"


def paridade(numero):

    if numero == 0:
        return "Zero"

    if numero % 2 == 0:
        return "Par"

    return "Ímpar"


def duzia(numero):

    if numero == 0:
        return "Zero"

    if numero <= 12:
        return "1ª"

    if numero <= 24:
        return "2ª"

    return "3ª"


def coluna(numero):

    if numero == 0:
        return "Zero"

    resto = numero % 3

    if resto == 1:
        return "1ª"

    if resto == 2:
        return "2ª"

    return "3ª"


def distancia_roda(a, b):

    distancia = abs(POS[a] - POS[b])

    return min(distancia, 37 - distancia)


def espelho_roda(numero):

    return RODA[(POS[numero] + 18) % 37]


def espelho_numerico(numero):

    if numero == 0:
        return 0

    return 37 - numero


def atraso(numero, dados):

    for i, valor in enumerate(reversed(dados)):

        if valor == numero:
            return i

    return len(dados)


def criar_transicoes(dados):

    matriz = defaultdict(Counter)

    for atual, proximo in zip(dados[:-1], dados[1:]):
        matriz[atual][proximo] += 1

    return matriz


def forca_transicao(numero, ultimo, matriz):

    total = sum(matriz[ultimo].values())

    if total == 0:
        return 0

    return matriz[ultimo][numero] / total


def zscore(numero, dados):

    if not dados:
        return 0.0

    contador = Counter(dados)

    valores = [
        contador[n]
        for n in range(37)
    ]

    desvio = pstdev(valores)

    if desvio == 0:
        return 0.0

    return (
        contador[numero] - mean(valores)
    ) / desvio


# ============================================================
# FREQUÊNCIA
# ============================================================

def score_frequencia(numero, dados):

    pesos = [
        (10, 2.5),
        (20, 2.0),
        (37, 1.6),
        (50, 1.2),
        (100, 0.9),
        (150, 0.6),
        (200, 0.4)
    ]

    score = 0.0

    for janela, peso in pesos:

        parte = dados[-janela:]

        if not parte:
            continue

        frequencia = parte.count(numero) / len(parte)

        score += frequencia * 100 * peso

    return score


# ============================================================
# SCORE PRINCIPAL
# ============================================================

def calcular_score(numero, dados, matriz):

    if not dados:
        return 0.0

    ultimo = dados[-1]

    score = 0.0

    # Frequência
    score += score_frequencia(numero, dados)

    # Atraso
    score += min(
        atraso(numero, dados) * 0.06,
        3.0
    )

    # Z-score
    score += zscore(numero, dados) * 0.7

    # Transição / puxa
    score += (
        forca_transicao(
            numero,
            ultimo,
            matriz
        ) * 10
    )

    # Distância na roda
    ultimos = dados[-10:]

    if ultimos:

        media_distancia = mean(
            distancia_roda(numero, x)
            for x in ultimos
        )

        score += max(
            0,
            3 - media_distancia * 0.18
        )

    # Vizinhança da roda
    for resultado in dados[-30:]:

        distancia = distancia_roda(
            numero,
            resultado
        )

        if distancia == 1:
            score += 0.55

        elif distancia == 2:
            score += 0.25

        elif distancia == 3:
            score += 0.08

    # Primos
    if numero in PRIMOS:
        score += 0.35

    # Fibonacci
    if numero in FIBONACCI:
        score += 0.25

    # Quadrados
    if numero in QUADRADOS:
        score += 0.15

    # Espelho da roda
    score += (
        dados.count(
            espelho_roda(numero)
        ) * 0.10
    )

    # Espelho numérico
    score += (
        dados.count(
            espelho_numerico(numero)
        ) * 0.06
    )

    # Cor
    if cor(numero) != "Verde":

        score += sum(
            1
            for x in dados[-30:]
            if cor(x) == cor(numero)
        ) * 0.025

    # Dúzia
    score += sum(
        1
        for x in dados[-30:]
        if duzia(x) == duzia(numero)
    ) * 0.02

    # Coluna
    score += sum(
        1
        for x in dados[-30:]
        if coluna(x) == coluna(numero)
    ) * 0.02

    return score


# ============================================================
# RANKING
# ============================================================

def criar_ranking(dados):

    matriz = criar_transicoes(dados)

    ranking = []

    for numero in range(37):

        ranking.append({
            "numero": numero,
            "score": calcular_score(
                numero,
                dados,
                matriz
            )
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking


# ============================================================
# CHIPS
# ============================================================

def mostrar_chips(numeros):

    html = ""

    for numero in numeros:

        classe = ""

        if numero == 0:
            classe = "green"

        elif numero in VERMELHOS:
            classe = "red"

        html += (
            '<span class="chip '
            + classe
            + '">'
            + str(numero)
            + "</span>"
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# BACKTEST
# ============================================================

def executar_backtest(dados):

    if len(dados) < 30:
        return None

    inicio = max(
        20,
        len(dados) - 100
    )

    acertos = 0
    testes = 0

    for i in range(inicio, len(dados)):

        historico = dados[:i]

        ranking = criar_ranking(
            historico
        )

        escolhas = {
            item["numero"]
            for item in ranking[:22]
        }

        resultado = dados[i]

        if resultado in escolhas:
            acertos += 1

        testes += 1

    if testes == 0:
        return None

    percentual = (
        acertos / testes
    ) * 100

    return acertos, testes, percentual


# ============================================================
# CABEÇALHO
# ============================================================

col_logo, col_sentido, col_menu = st.columns(
    [5, 2, 1]
)

with col_logo:

    st.markdown(
        """
        ## 🎯 **ROBÔ <span style="color:#20d85a">RICO</span> 🤑**
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Estatística • Matemática • Roda • Mesa • "
        "Transições • Espelhos"
    )


with col_sentido:

    sentido = st.selectbox(
        "Sentido atual",
        ["Direita", "Esquerda"]
    )


with col_menu:

    st.markdown("### ☰")


# ============================================================
# HISTÓRICO
# ============================================================

st.markdown("### 📦 Histórico da roleta")

texto_historico = st.text_area(
    "Resultados",
    placeholder=(
        "Cole os resultados aqui...\n"
        "Exemplo: 32 23 13 35 4 20 4 14 12 4"
    ),
    height=100,
    label_visibility="collapsed"
)


botao1, botao2, botao3 = st.columns(
    [1.4, 1, 1]
)


with botao1:

    analisar = st.button(
        "📊 ANALISAR HISTÓRICO",
        use_container_width=True,
        type="primary"
    )


with botao2:

    limpar = st.button(
        "🗑️ LIMPAR",
        use_container_width=True
    )


with botao3:

    usar_dados = st.button(
        "📋 USAR DADOS COLADOS",
        use_container_width=True
    )


if limpar:

    st.session_state.historico = []

    st.rerun()


if analisar or usar_dados:

    numeros = extrair_numeros(
        texto_historico
    )

    if numeros:

        st.session_state.historico = (
            numeros[-MAX_HISTORICO:]
        )

    else:

        st.warning(
            "Nenhum número válido foi encontrado."
        )


dados = st.session_state.historico


# ============================================================
# SEM DADOS
# ============================================================

if not dados:

    st.info(
        "Cole os resultados da roleta acima "
        "para iniciar a análise estatística."
    )

    st.stop()


# ============================================================
# ANÁLISE
# ============================================================

ranking = criar_ranking(dados)

top22 = [
    item["numero"]
    for item in ranking[:22]
]

tendencia_alta = top22[:8]

possiveis = top22[8:15]

marcacao = top22[15:22]

backtest = executar_backtest(
    dados
)

ultimo = dados[-1]


# ============================================================
# CARDS SUPERIORES
# ============================================================

m1, m2, m3, m4, m5 = st.columns(5)


with m1:

    st.metric(
        "ÚLTIMO RESULTADO",
        ultimo
    )

    st.caption(
        f"{cor(ultimo)} • "
        f"{paridade(ultimo)} • "
        f"{duzia(ultimo)} Dúzia"
    )


with m2:

    st.metric(
        "BASE ANALISADA",
        len(dados)
    )

    st.caption(
        "últimos resultados"
    )


with m3:

    if backtest:

        st.metric(
            "DESEMPENHO (22)",
            f"{backtest[2]:.1f}%"
        )

    else:

        st.metric(
            "DESEMPENHO (22)",
            "—"
        )

    st.caption(
        "cobertura no backtest"
    )


with m4:

    st.metric(
        "ESCOLHAS DO ROBÔ",
        22
    )

    st.caption(
        "números selecionados"
    )


with m5:

    st.metric(
        "TRANSIÇÕES",
        max(0, len(dados) - 1)
    )

    st.caption(
        "transições observadas"
    )


# ============================================================
# ESCOLHAS
# ============================================================

st.markdown("### 🔥 ESCOLHAS DO ROBÔ")


c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        '<div class="choice high">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📈 8 NÚMEROS — TENDÊNCIA ALTA"
    )

    mostrar_chips(
        tendencia_alta
    )

    st.markdown(
        '<div class="note">'
        'Maior força estatística no momento'
        '</div></div>',
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        '<div class="choice possible">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### ❓ 7 NÚMEROS — POSSÍVEIS"
    )

    mostrar_chips(
        possiveis
    )

    st.markdown(
        '<div class="note">'
        'Números com chance secundária'
        '</div></div>',
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        '<div class="choice mark">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🎯 7 NÚMEROS — MARCAÇÃO"
    )

    mostrar_chips(
        marcacao
    )

    st.markdown(
        '<div class="note">'
        'Cobertura e proteção'
        '</div></div>',
        unsafe_allow_html=True
    )


# ============================================================
# ESTATÍSTICAS
# ============================================================

contador = Counter(dados)

frequencias = [
    contador[n]
    for n in range(37)
]

atrasos = [
    atraso(n, dados)
    for n in range(37)
]

zscores = [
    zscore(n, dados)
    for n in range(37)
]


transicoes_fortes = 0

for atual, proximo in zip(
    dados[:-1],
    dados[1:]
):

    if distancia_roda(
        atual,
        proximo
    ) <= 3:

        transicoes_fortes += 1


s1, s2, s3, s4, s5 = st.columns(5)


with s1:

    st.metric(
        "FREQUÊNCIA MÉDIA",
        f"{mean(frequencias):.2f}"
    )


with s2:

    st.metric(
        "ATRASO MÉDIO",
        f"{mean(atrasos):.1f}"
    )


with s3:

    st.metric(
        "Z-SCORE MÉDIO",
        f"{mean(zscores):.2f}"
    )


with s4:

    st.metric(
        "MAIOR ATRASO",
        max(atrasos)
    )


with s5:

    st.metric(
        "PUXAS FORTES",
        transicoes_fortes
    )


# ============================================================
# PAINÉIS INFERIORES
# ============================================================

p1, p2, p3 = st.columns(3)


with p1:

    st.markdown("### 🎨 RESUMO DE CORES")

    total = len(dados)

    vermelhos = contador.copy()

    vermelho_pct = (
        sum(
            1
            for n in dados
            if n in VERMELHOS
        )
        / total
        * 100
    )

    preto_pct = (
        sum(
            1
            for n in dados
            if n != 0 and n not in VERMELHOS
        )
        / total
        * 100
    )

    verde_pct = (
        dados.count(0)
        / total
        * 100
    )

    st.write(
        f"🔴 Vermelhos: **{vermelho_pct:.1f}%**"
    )

    st.write(
        f"⚫ Pretos: **{preto_pct:.1f}%**"
    )

    st.write(
        f"🟢 Verdes: **{verde_pct:.1f}%**"
    )


with p2:

    st.markdown("### 🧮 PADRÕES NUMÉRICOS")

    st.write(
        "Primos:",
        sum(contador[n] for n in PRIMOS)
    )

    st.write(
        "Fibonacci:",
        sum(contador[n] for n in FIBONACCI)
    )

    st.write(
        "Quadrados:",
        sum(contador[n] for n in QUADRADOS)
    )

    st.write(
        "Múltiplos de 3:",
        sum(
            contador[n]
            for n in range(37)
            if n != 0 and n % 3 == 0
        )
    )

    st.write(
        "Múltiplos de 2:",
        sum(
            contador[n]
            for n in range(37)
            if n != 0 and n % 2 == 0
        )
    )


with p3:

    st.markdown("### 🕒 ÚLTIMAS JANELAS")

    for janela in [
        10, 20, 37, 50,
        100, 150, 200
    ]:

        if dados:

            valor = dados[
                -min(janela, len(dados))
            ]

            st.write(
                f"Últimos {janela}: **{valor}**"
            )


# ============================================================
# HISTÓRICO E BACKTEST
# ============================================================

r1, r2 = st.columns([1.5, 1])


with r1:

    st.markdown(
        "### 📜 HISTÓRICO RECENTE "
        "(últimos 20)"
    )

    mostrar_chips(
        dados[-20:]
    )


with r2:

    st.markdown(
        "### 🧪 TESTE DE COBERTURA "
        "(BACKTEST)"
    )

    if backtest:

        acertos, testes, cobertura = (
            backtest
        )

        b1, b2, b3 = st.columns(3)

        b1.metric(
            "Acertos",
            acertos
        )

        b2.metric(
            "Testes",
            testes
        )

        b3.metric(
            "Cobertura",
            f"{cobertura:.1f}%"
        )

    else:

        st.info(
            "São necessários pelo menos "
            "30 resultados."
        )


# ============================================================
# RANKING COMPLETO
# ============================================================

with st.expander(
    "🏆 VER RANKING COMPLETO DOS 37 NÚMEROS"
):

    tabela = []

    for posicao, item in enumerate(
        ranking,
        start=1
    ):

        numero = item["numero"]

        tabela.append({
            "Posição": posicao,
            "Número": numero,
            "Score": round(
                item["score"],
                2
            ),
            "Frequência": contador[numero],
            "Atraso": atraso(
                numero,
                dados
            ),
            "Cor": cor(numero),
            "Dúzia": duzia(numero),
            "Coluna": coluna(numero),
            "Espelho roda": espelho_roda(
                numero
            ),
            "Espelho número": espelho_numerico(
                numero
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

st.markdown("### ➕ ADICIONAR NOVO RESULTADO")

n1, n2 = st.columns([1, 2])


with n1:

    novo_resultado = st.number_input(
        "Número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )


with n2:

    if st.button(
        "ADICIONAR & ATUALIZAR",
        type="primary",
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


# ============================================================
# RODAPÉ
# ============================================================

st.caption(
    "⚠️ Jogue com responsabilidade. "
    "Este sistema é apenas para análise estatística. "
    "A roleta é aleatória e o histórico não garante "
    "o próximo resultado."
)
