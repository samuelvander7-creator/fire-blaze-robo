import streamlit as st
from collections import Counter
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

MAX_ANALISE = 200
ESCOLHAS = 22

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
        radial-gradient(circle at 15% 0%, #071b28 0%, transparent 35%),
        radial-gradient(circle at 90% 0%, #13091f 0%, transparent 35%),
        #03070b;
    color: #f4f7fb;
}

.block-container {
    max-width: 1500px;
    padding-top: 25px;
    padding-bottom: 30px;
}

/* títulos */

.logo-title {
    font-size: 42px;
    font-weight: 900;
    line-height: 1;
}

.logo-rico {
    color: #19d65a;
}

.subtitle {
    color: #aab5c3;
    font-size: 16px;
    margin-top: 7px;
}

/* cards */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #07131d, #050a10);
    border: 1px solid #263442;
    border-radius: 12px;
    padding: 15px;
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #aab5c3 !important;
}

[data-testid="stMetricValue"] {
    font-weight: 800;
}

/* caixas */

.box {
    background: linear-gradient(145deg, #07131d, #040a10);
    border: 1px solid #263442;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
}

.box-title {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 14px;
}

/* escolhas */

.high-box {
    border: 1px solid #16c75b;
    background: linear-gradient(145deg, #061a13, #04100c);
    border-radius: 12px;
    padding: 18px;
    min-height: 230px;
}

.poss-box {
    border: 1px solid #1686e8;
    background: linear-gradient(145deg, #061522, #040d15);
    border-radius: 12px;
    padding: 18px;
    min-height: 230px;
}

.mark-box {
    border: 1px solid #e49b19;
    background: linear-gradient(145deg, #1b1306, #100c05);
    border-radius: 12px;
    padding: 18px;
    min-height: 230px;
}

.choice-title {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 15px;
}

.high-title {
    color: #16d65d;
}

.poss-title {
    color: #1597ff;
}

.mark-title {
    color: #f0a51c;
}

/* números */

.num {
    display: inline-block;
    width: 42px;
    height: 42px;
    line-height: 42px;
    text-align: center;
    border-radius: 50%;
    margin: 5px;
    font-size: 16px;
    font-weight: 800;
    border: 1px solid #5b6670;
}

.red {
    background: #e5222d;
}

.black {
    background: #050505;
}

.green {
    background: #159447;
}

/* rodapé */

.footer {
    text-align: center;
    color: #65727f;
    margin-top: 25px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ESTADO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []


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


def cor(n):
    if n == 0:
        return "Verde"

    if n in VERMELHOS:
        return "Vermelho"

    return "Preto"


def cor_class(n):
    if n == 0:
        return "green"

    if n in VERMELHOS:
        return "red"

    return "black"


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


def atraso(n, dados):
    for i, x in enumerate(reversed(dados)):
        if x == n:
            return i

    return len(dados)


def vizinhos(n):
    if n not in POS:
        return []

    p = POS[n]

    return [
        RODA[(p - 2) % 37],
        RODA[(p - 1) % 37],
        RODA[(p + 1) % 37],
        RODA[(p + 2) % 37]
    ]


def espelho_roda(n):
    if n not in POS:
        return 0

    return RODA[(POS[n] + 18) % 37]


def espelho_numerico(n):
    if n == 0:
        return 0

    return 37 - n


def transicao_score(n, ultimo, dados):
    if not dados:
        return 0

    ocorrencias = 0
    total = 0

    for i in range(len(dados) - 1):
        if dados[i] == ultimo:
            total += 1

            if dados[i + 1] == n:
                ocorrencias += 1

    if total == 0:
        return 0

    return (ocorrencias / total) * 10


def frequencia_score(n, dados):
    pesos = [
        (10, 3.0),
        (20, 2.5),
        (37, 2.0),
        (50, 1.5),
        (100, 1.0),
        (150, 0.7),
        (200, 0.5)
    ]

    score = 0

    for janela, peso in pesos:

        parte = dados[-janela:]

        if not parte:
            continue

        freq = parte.count(n) / len(parte)

        score += freq * 100 * peso

    return score


def vizinhanca_score(n, dados):
    score = 0

    for x in dados[-40:]:

        d = distancia_roda(n, x)

        if d == 1:
            score += 0.9

        elif d == 2:
            score += 0.55

        elif d == 3:
            score += 0.25

    return score


def atraso_score(n, dados):
    a = atraso(n, dados)

    if a < 3:
        return 0

    return min(a * 0.07, 3.5)


def propriedade_score(n):
    score = 0

    if n in PRIMOS:
        score += 0.35

    if n in FIBONACCI:
        score += 0.35

    if n in QUADRADOS:
        score += 0.20

    if n != 0 and n % 3 == 0:
        score += 0.12

    if n != 0 and n % 2 == 0:
        score += 0.05

    return score


def espelho_score(n, dados):
    er = espelho_roda(n)
    en = espelho_numerico(n)

    return (
        dados.count(er) * 0.12
        + dados.count(en) * 0.08
    )


def classificacao_score(n, dados):
    recentes = dados[-30:]

    if not recentes:
        return 0

    score = 0

    mesma_cor = sum(
        cor(x) == cor(n)
        for x in recentes
    )

    mesma_faixa = sum(
        faixa(x) == faixa(n)
        for x in recentes
    )

    mesma_duzia = sum(
        duzia(x) == duzia(n)
        for x in recentes
    )

    mesma_coluna = sum(
        coluna(x) == coluna(n)
        for x in recentes
    )

    score += mesma_cor * 0.015
    score += mesma_faixa * 0.012
    score += mesma_duzia * 0.012
    score += mesma_coluna * 0.012

    return score


# ============================================================
# ANÁLISE
# ============================================================

def analisar(dados):

    if not dados:
        return []

    ultimo = dados[-1]

    ranking = []

    for n in range(37):

        score = 0

        # frequência
        score += frequencia_score(n, dados)

        # atraso
        score += atraso_score(n, dados)

        # vizinhos
        score += vizinhanca_score(n, dados)

        # transições
        score += transicao_score(
            n,
            ultimo,
            dados
        )

        # espelhos
        score += espelho_score(
            n,
            dados
        )

        # matemática
        score += propriedade_score(n)

        # classificações
        score += classificacao_score(
            n,
            dados
        )

        ranking.append({
            "numero": n,
            "score": score,
            "frequencia": dados.count(n),
            "atraso": atraso(n, dados)
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking


# ============================================================
# BACKTEST
# ============================================================

def backtest(dados):

    if len(dados) < 40:
        return 0, 0

    testes = min(100, len(dados) - 20)

    acertos = 0

    inicio = len(dados) - testes

    for i in range(inicio, len(dados)):

        historico = dados[:i]

        ranking = analisar(historico)

        escolhidos = {
            x["numero"]
            for x in ranking[:22]
        }

        if dados[i] in escolhidos:
            acertos += 1

    return acertos, testes


# ============================================================
# CABEÇALHO
# ============================================================

cab1, cab2 = st.columns([3.8, 1.5])

with cab1:

    st.markdown(
        '<div class="logo-title">'
        '🎯 ROBÔ <span class="logo-rico">RICO 🤑</span>'
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

with cab2:

    st.write("**Sentido atual**")

    sentido = st.selectbox(
        "Sentido",
        ["Direita", "Esquerda", "Automático"],
        label_visibility="collapsed"
    )


st.write("")


# ============================================================
# DADOS
# ============================================================

dados = st.session_state.historico[-MAX_ANALISE:]

ranking = analisar(dados)


# ============================================================
# CARDS SUPERIORES
# ============================================================

if dados:
    ultimo = dados[-1]
else:
    ultimo = 0

if ranking:
    acertos, testes = backtest(dados)

    cobertura = (
        acertos / testes * 100
        if testes else 0
    )

    transicoes = max(
        0,
        len(dados) - 1
    )

else:
    cobertura = 0
    transicoes = 0


c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "ÚLTIMO RESULTADO",
        ultimo
    )
    if dados:
        st.caption(
            f"{cor(ultimo)} • "
            f"{'Par' if ultimo and ultimo % 2 == 0 else 'Ímpar'} • "
            f"{faixa(ultimo)} • {duzia(ultimo)}"
        )

with c2:
    st.metric(
        "BASE ANALISADA",
        len(dados)
    )
    st.caption("máximo de 200 resultados")

with c3:
    st.metric(
        "DESEMPENHO (22)",
        f"{cobertura:.1f}%"
    )
    st.caption("teste histórico experimental")

with c4:
    st.metric(
        "ESCOLHAS DO ROBÔ",
        "22"
    )
    st.caption("8 + 7 + 7")

with c5:
    st.metric(
        "TRANSIÇÕES",
        f"{transicoes:,}".replace(",", ".")
    )
    st.caption("relações observadas")


# ============================================================
# ESCOLHAS
# ============================================================

st.markdown("## 🔥 ESCOLHAS DO ROBÔ")

if ranking:

    alta = ranking[:8]
    possiveis = ranking[8:15]
    marcacao = ranking[15:22]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="high-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="choice-title high-title">'
            '📈 8 NÚMEROS COM TENDÊNCIA ALTA'
            '</div>',
            unsafe_allow_html=True
        )

        for item in alta:

            n = item["numero"]

            st.markdown(
                f'<span class="num {cor_class(n)}">'
                f'{n}'
                f'</span>',
                unsafe_allow_html=True
            )

        st.caption(
            "Maior pontuação estatística no momento."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="poss-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="choice-title poss-title">'
            '❓ 7 NÚMEROS COMO POSSÍVEL'
            '</div>',
            unsafe_allow_html=True
        )

        for item in possiveis:

            n = item["numero"]

            st.markdown(
                f'<span class="num {cor_class(n)}">'
                f'{n}'
                f'</span>',
                unsafe_allow_html=True
            )

        st.caption(
            "Possibilidades secundárias."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col3:

        st.markdown(
            '<div class="mark-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="choice-title mark-title">'
            '🎯 7 NÚMEROS COMO MARCAÇÃO'
            '</div>',
            unsafe_allow_html=True
        )

        for item in marcacao:

            n = item["numero"]

            st.markdown(
                f'<span class="num {cor_class(n)}">'
                f'{n}'
                f'</span>',
                unsafe_allow_html=True
            )

        st.caption(
            "Números para cobertura e proteção."
        )

        st.markdown("</div>", unsafe_allow_html=True)

else:

    st.info(
        "Cole o histórico da roleta para gerar as 22 escolhas."
    )


# ============================================================
# RANKING
# ============================================================

st.markdown("## 🏆 TOP 5 GERAL")

if ranking:

    top5 = ranking[:5]

    for i, item in enumerate(top5, 1):

        n = item["numero"]

        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            st.write(f"**#{i}**")

        with col2:
            st.markdown(
                f'<span class="num {cor_class(n)}">'
                f'{n}'
                f'</span>',
                unsafe_allow_html=True
            )

        with col3:
            st.write(
                f"Pontuação: **{item['score']:.2f}**"
            )


# ============================================================
# ESTATÍSTICAS
# ============================================================

if dados:

    st.markdown("## 📊 ESTATÍSTICAS")

    frequencias = Counter(dados)

    freq_media = len(dados) / 37

    atrasos = [
        atraso(n, dados)
        for n in range(37)
    ]

    maior_atraso = max(atrasos)

    media_atraso = sum(atrasos) / 37

    s1, s2, s3, s4, s5 = st.columns(5)

    with s1:
        st.metric(
            "FREQUÊNCIA",
            f"{freq_media:.2f}"
        )
        st.caption(
            f"Máx: {max(frequencias.values())}"
        )

    with s2:
        st.metric(
            "ATRASO MÉDIO",
            f"{media_atraso:.1f}"
        )
        st.caption(
            f"Máx: {maior_atraso}"
        )

    with s3:

        valores = list(
            frequencias.get(n, 0)
            for n in range(37)
        )

        media = sum(valores) / 37

        variancia = sum(
            (x - media) ** 2
            for x in valores
        ) / 37

        desvio = math.sqrt(variancia)

        st.metric(
            "DESVIO / Z",
            f"{desvio:.2f}"
        )

        st.caption("dispersão das frequências")

    with s4:

        st.metric(
            "MAIOR ATRASO",
            maior_atraso
        )

        st.caption("giros desde a última saída")

    with s5:

        st.metric(
            "TRANSIÇÕES",
            max(0, len(dados) - 1)
        )

        st.caption("pares observados")


# ============================================================
# PADRÕES
# ============================================================

if dados:

    st.markdown("## 🧮 PADRÕES NUMÉRICOS")

    primos = sum(
        n in PRIMOS
        for n in dados
    )

    fibonacci = sum(
        n in FIBONACCI
        for n in dados
    )

    quadrados = sum(
        n in QUADRADOS
        for n in dados
    )

    multiplos3 = sum(
        n != 0 and n % 3 == 0
        for n in dados
    )

    multiplos2 = sum(
        n != 0 and n % 2 == 0
        for n in dados
    )

    p1, p2, p3, p4, p5 = st.columns(5)

    with p1:
        st.metric("PRIMOS", primos)

    with p2:
        st.metric("FIBONACCI", fibonacci)

    with p3:
        st.metric("QUADRADOS", quadrados)

    with p4:
        st.metric("MÚLTIPLOS DE 3", multiplos3)

    with p5:
        st.metric("MÚLTIPLOS DE 2", multiplos2)


# ============================================================
# ÚLTIMAS JANELAS
# ============================================================

if dados:

    st.markdown("## 📌 ÚLTIMAS JANELAS")

    janelas = [10, 20, 37, 50, 100, 150, 200]

    colunas = st.columns(4)

    for i, janela in enumerate(janelas):

        parte = dados[-janela:]

        ultimo_janela = parte[-1] if parte else "-"

        with colunas[i % 4]:

            st.metric(
                f"ÚLTIMOS {janela}",
                ultimo_janela
            )


# ============================================================
# HISTÓRICO RECENTE
# ============================================================

st.markdown("## 🎲 HISTÓRICO RECENTE")

if dados:

    recentes = dados[-20:]

    texto = ""

    for n in recentes:

        emoji = "🟢"

        if n in VERMELHOS:
            emoji = "🔴"

        elif n != 0:
            emoji = "⚫"

        texto += f"{emoji} **{n}**   "

    st.markdown(texto)

else:

    st.info(
        "Nenhum resultado adicionado."
    )


# ============================================================
# BACKTEST
# ============================================================

if dados:

    st.markdown("## 🧪 TESTE DE COBERTURA")

    acertos, testes = backtest(dados)

    if testes:

        taxa = acertos / testes * 100

        b1, b2, b3 = st.columns(3)

        with b1:
            st.metric(
                "ACERTOS",
                acertos
            )

        with b2:
            st.metric(
                "TESTES",
                testes
            )

        with b3:
            st.metric(
                "COBERTURA",
                f"{taxa:.1f}%"
            )

        st.caption(
            "Backtest histórico não representa garantia "
            "de resultados futuros."
        )


# ============================================================
# NOVO RESULTADO
# ============================================================

st.markdown("## ➕ NOVO RESULTADO")

n1, n2, n3 = st.columns([1, 2, 1])

with n1:

    novo = st.number_input(
        "Digite o número que saiu",
        min_value=0,
        max_value=36,
        value=0,
        step=1
    )

with n2:

    adicionar = st.button(
        "🟢 ADICIONAR & ATUALIZAR",
        use_container_width=True
    )

with n3:

    limpar = st.button(
        "🗑️ LIMPAR HISTÓRICO",
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


if limpar:

    st.session_state.historico = []

    st.rerun()


# ============================================================
# IMPORTAR HISTÓRICO
# ============================================================

st.markdown("## 📥 IMPORTAR HISTÓRICO")

texto_importado = st.text_area(
    "Cole aqui os resultados da roleta",
    placeholder=(
        "Exemplo: 32 23 13 35 4 20 4 14 12 4"
    ),
    height=120
)

if st.button(
    "📋 CARREGAR HISTÓRICO",
    use_container_width=True
):

    novos = extrair_numeros(
        texto_importado
    )

    if novos:

        st.session_state.historico = (
            novos[-MAX_ANALISE:]
        )

        st.success(
            f"{len(novos)} resultados carregados."
        )

        st.rerun()

    else:

        st.error(
            "Não encontrei números válidos entre 0 e 36."
        )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    '<div class="footer">'
    '🛡️ Jogue com responsabilidade. '
    'Este sistema é apenas para análise estatística. '
    'As classificações não garantem o próximo resultado.'
    '</div>',
    unsafe_allow_html=True
)
