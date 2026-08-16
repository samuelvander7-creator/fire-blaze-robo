import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev

st.set_page_config(
    page_title="ROBÔ RICO 🤑",
    page_icon="🎯",
    layout="wide"
)

MAX_HIST = 200
NUMEROS = list(range(37))

RODA = [
    0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,
    5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26
]

POS = {n:i for i,n in enumerate(RODA)}

VERMELHOS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}

PRIMOS = {
    2,3,5,7,11,13,17,19,23,29,31
}

FIB = {
    0,1,2,3,5,8,13,21,34
}

QUADRADOS = {
    0,1,4,9,16,25,36
}

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp{
    background:
      radial-gradient(
        circle at 0% 0%,
        rgba(0,120,190,.10),
        transparent 28%
      ),
      radial-gradient(
        circle at 100% 0%,
        rgba(100,0,180,.12),
        transparent 30%
      ),
      #02080e;
    color:#edf4f8;
}

.block-container{
    max-width:1500px;
    padding:18px 18px 35px;
}

header[data-testid="stHeader"]{
    background:transparent;
}

/* LOGO */

.brand{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:16px;
    margin-bottom:15px;
}

.brand-left{
    display:flex;
    align-items:center;
    gap:12px;
}

.logo{
    font-size:54px;
    line-height:1;
}

.title{
    font-size:42px;
    font-weight:900;
    letter-spacing:-1.5px;
    line-height:1;
    color:#f4f7fa;
}

.title .rico{
    color:#16d94d;
}

.subtitle{
    color:#aebbc6;
    font-size:15px;
    margin-top:7px;
}

.direction{
    border:1px solid #294050;
    background:#061018;
    border-radius:10px;
    padding:9px 28px;
    text-align:center;
    min-width:225px;
}

.direction small{
    display:block;
    color:#bdc8d1;
}

.direction b{
    display:block;
    color:#19db4f;
    font-size:26px;
}

.direction span{
    font-size:11px;
    color:#9baab5;
}

.menu{
    border:1px solid #294050;
    border-radius:10px;
    background:#061018;
    width:60px;
    height:60px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
}

/* CARDS SUPERIORES */

.metric{
    border:1px solid #263b4b;
    border-radius:9px;
    background:#061018;
    padding:13px 10px;
    text-align:center;
    min-height:112px;
}

.metric .label{
    font-size:12px;
    color:#c2cdd5;
    text-transform:uppercase;
}

.metric .value{
    font-size:37px;
    font-weight:900;
    margin:4px;
}

.metric .sub{
    font-size:12px;
    color:#d0d8de;
}

.blue{color:#1495ff}
.green{color:#16d94d}
.purple{color:#a65cff}
.cyan{color:#11d8ed}
.orange{color:#ffad22}

/* SEÇÃO */

.section{
    font-size:22px;
    font-weight:850;
    color:#dbe4ea;
    margin:18px 0 10px;
}

/* ESCOLHAS */

.pick{
    border-radius:9px;
    background:#040d14;
    padding:14px;
    min-height:285px;
}

.pick.high{
    border:1px solid #0ca64a;
}

.pick.possible{
    border:1px solid #0788e8;
}

.pick.mark{
    border:1px solid #d98b08;
}

.pick h4{
    margin:0 0 15px;
    font-size:14px;
}

.pick.high h4{
    color:#13db54;
}

.pick.possible h4{
    color:#129cff;
}

.pick.mark h4{
    color:#ffad21;
}

/* BOLAS */

.ball{
    display:inline-flex;
    width:45px;
    height:45px;
    border-radius:50%;
    align-items:center;
    justify-content:center;
    margin:5px 3px;
    font-size:17px;
    font-weight:900;
    border:1px solid #6b7780;
}

.red{
    background:#dc2630;
    border-color:#ff6269;
}

.black{
    background:#030609;
}

.zero{
    background:#0a9e43;
    border-color:#24df65;
}

.footer{
    margin-top:14px;
    border:1px solid currentColor;
    border-radius:6px;
    padding:8px;
    text-align:center;
    font-size:11px;
}

/* PAINÉIS */

.panel{
    border:1px solid #263b4b;
    border-radius:9px;
    background:#040d14;
    padding:14px;
    min-height:125px;
}

.panel h4{
    margin:0 0 10px;
    color:#c9d3db;
    font-size:13px;
    text-transform:uppercase;
}

.line{
    display:flex;
    justify-content:space-between;
    padding:7px 0;
    border-bottom:1px solid rgba(150,180,200,.10);
    font-size:13px;
}

.line:last-child{
    border-bottom:0;
}

/* TOP 5 */

.rank{
    display:flex;
    justify-content:space-between;
    padding:8px 0;
    border-bottom:1px solid rgba(150,180,200,.10);
}

.rank b{
    color:#15d94c;
}

/* HISTÓRICO */

.recent{
    display:flex;
    flex-wrap:wrap;
    gap:6px;
}

.smallball{
    width:32px;
    height:32px;
    border-radius:50%;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-size:12px;
    font-weight:900;
    border:1px solid #65727c;
}

div[data-testid="stButton"]>button{
    background:#06131c;
    color:#eaf0f4;
    border:1px solid #2a4656;
    border-radius:8px;
    font-weight:800;
    min-height:42px;
}

div[data-testid="stButton"]>button:hover{
    border-color:#159cff;
    color:white;
}

div[data-testid="stTextArea"] textarea{
    background:#f0f2f6;
    color:#18212a;
    border-radius:10px;
}

div[data-testid="stNumberInput"] input{
    background:#06131c;
    color:white;
}

.footer-note{
    text-align:center;
    color:#788895;
    font-size:11px;
    margin-top:18px;
}

@media(max-width:800px){

    .title{
        font-size:30px;
    }

    .logo{
        font-size:40px;
    }

    .direction,
    .menu{
        display:none;
    }

    .block-container{
        padding:10px;
    }

    .metric .value{
        font-size:29px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES
# ============================================================

def numeros(texto):

    texto = (
        texto
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
        .replace("\t", " ")
    )

    saida = []

    for x in texto.split():

        try:
            n = int(x)

            if 0 <= n <= 36:
                saida.append(n)

        except:
            pass

    return saida


def cor(n):

    if n == 0:
        return "Verde"

    if n in VERMELHOS:
        return "Vermelho"

    return "Preto"


def ball(n, small=False):

    if n == 0:
        cls = "zero"

    elif n in VERMELHOS:
        cls = "red"

    else:
        cls = "black"

    size = "smallball" if small else "ball"

    return (
        f'<span class="{size} {cls}">{n}</span>'
    )


def balls(ns, small=False):

    return "".join(
        ball(n, small)
        for n in ns
    )


def distancia(a, b):

    d = abs(
        POS[a] - POS[b]
    )

    return min(
        d,
        37 - d
    )


def espelho_roda(n):

    return RODA[
        (POS[n] + 18) % 37
    ]


def espelho_num(n):

    if n == 0:
        return 0

    return 37 - n


def atraso(n, data):

    for i, x in enumerate(
        reversed(data)
    ):

        if x == n:
            return i

    return len(data)


def transicoes(data):

    m = defaultdict(Counter)

    for a, b in zip(
        data[:-1],
        data[1:]
    ):

        m[a][b] += 1

    return m


def zscore(n, data):

    if not data:
        return 0

    freq = Counter(data)

    vals = [
        freq[x]
        for x in NUMEROS
    ]

    sd = pstdev(vals)

    if sd == 0:
        return 0

    return (
        freq[n] - mean(vals)
    ) / sd


# ============================================================
# SCORE
# ============================================================

def score(n, data, direcao):

    if not data:
        return 0

    ultimo = data[-1]

    matriz = transicoes(data)

    s = 0

    # --------------------------------------------------------
    # FREQUÊNCIA
    # --------------------------------------------------------

    pesos = {
        10: 2.6,
        20: 2.1,
        37: 1.7,
        50: 1.4,
        100: 1.0,
        150: .7,
        200: .5
    }

    for janela, peso in pesos.items():

        parte = data[-janela:]

        if parte:

            s += (
                parte.count(n)
                / len(parte)
                * 100
                * peso
            )

    # --------------------------------------------------------
    # ATRASO
    # --------------------------------------------------------

    s += min(
        atraso(n, data) * .055,
        2.5
    )

    # --------------------------------------------------------
    # Z-SCORE
    # --------------------------------------------------------

    s += zscore(
        n,
        data
    ) * .55

    # --------------------------------------------------------
    # VIZINHANÇA DA RODA
    # --------------------------------------------------------

    for x in data[-40:]:

        d = distancia(
            n,
            x
        )

        if d == 1:
            s += .65

        elif d == 2:
            s += .32

        elif d == 3:
            s += .10

    # --------------------------------------------------------
    # TRANSIÇÃO / PUXA
    # --------------------------------------------------------

    total = sum(
        matriz[ultimo].values()
    )

    if total:

        s += (
            matriz[ultimo][n]
            / total
            * 12
        )

    # --------------------------------------------------------
    # DIREÇÃO
    # --------------------------------------------------------

    if direcao == "Direita":

        delta = (
            POS[n]
            - POS[ultimo]
        ) % 37

    else:

        delta = (
            POS[ultimo]
            - POS[n]
        ) % 37

    if delta == 1:
        s += 1.7

    elif delta == 2:
        s += 1.1

    elif delta == 3:
        s += .6

    # --------------------------------------------------------
    # ESPELHOS
    # --------------------------------------------------------

    if espelho_roda(n) in data[-50:]:
        s += .6

    if espelho_num(n) in data[-50:]:
        s += .3

    # --------------------------------------------------------
    # SETOR DA RODA
    # --------------------------------------------------------

    setor = POS[n] // 5

    s += sum(
        POS[x] // 5 == setor
        for x in data[-50:]
    ) / 30

    # --------------------------------------------------------
    # MATEMÁTICA
    # --------------------------------------------------------

    if n in PRIMOS:
        s += .30

    if n in FIB:
        s += .25

    if n in QUADRADOS:
        s += .15

    if n and n % 3 == 0:
        s += .05

    if n and n % 2 == 0:
        s += .03

    return s


# ============================================================
# RANKING
# ============================================================

def analisar(data, direcao):

    rows = []

    for n in NUMEROS:

        rows.append({
            "n": n,
            "score": score(
                n,
                data,
                direcao
            )
        })

    rows.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    if not rows:
        return rows

    menor = rows[-1]["score"]
    maior = rows[0]["score"]

    intervalo = max(
        maior - menor,
        1
    )

    for row in rows:

        relativo = (
            row["score"] - menor
        ) / intervalo

        # Estimativa relativa do modelo.
        # Não é probabilidade matemática real.
        row["prob"] = (
            2 + relativo * 8
        )

    return rows


# ============================================================
# BACKTEST
# ============================================================

def backtest(
    data,
    direcao,
    quantidade=22
):

    if len(data) < 40:
        return 0, 0

    inicio = max(
        30,
        len(data) - 100
    )

    acertos = 0
    total = 0

    for i in range(
        inicio,
        len(data)
    ):

        historico = data[:i]

        ranking = analisar(
            historico,
            direcao
        )

        escolhidos = {
            x["n"]
            for x in ranking[:quantidade]
        }

        if data[i] in escolhidos:
            acertos += 1

        total += 1

    return (
        acertos,
        total
    )


# ============================================================
# ESTADO
# ============================================================

if "historico" not in st.session_state:

    st.session_state.historico = []


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown("""
<div class="brand">

    <div class="brand-left">

        <div class="logo">
            🎯💵
        </div>

        <div>

            <div class="title">
                ROBÔ <span class="rico">RICO</span> 🤑
            </div>

            <div class="subtitle">
                Estatística • Matemática • Roda • Mesa • Transições • Espelhos
            </div>

        </div>

    </div>

    <div style="display:flex;gap:9px">

        <div class="direction">

            <small>
                Sentido atual
            </small>

            <b>
                → Direita
            </b>

            <span>
                Automático
            </span>

        </div>

        <div class="menu">
            ☰
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


direcao = st.selectbox(
    "Sentido da análise",
    [
        "Direita",
        "Esquerda"
    ],
    label_visibility="collapsed"
)


# ============================================================
# IMPORTAÇÃO
# ============================================================

with st.expander(
    "📋 IMPORTAR HISTÓRICO",
    expanded=True
):

    texto = st.text_area(
        "Cole os últimos resultados",
        placeholder=(
            "Exemplo: "
            "32 23 13 35 4 20 4 14 12 4"
        ),
        label_visibility="collapsed"
    )

    a, b, c = st.columns(3)

    with a:

        if st.button(
            "📥 USAR DADOS COLADOS",
            use_container_width=True
        ):

            dados_importados = numeros(
                texto
            )

            if dados_importados:

                st.session_state.historico = (
                    dados_importados[-MAX_HIST:]
                )

                st.rerun()

            else:

                st.warning(
                    "Nenhum número válido encontrado."
                )

    with b:

        if st.button(
            "🗑️ LIMPAR",
            use_container_width=True
        ):

            st.session_state.historico = []

            st.rerun()

    with c:

        st.caption(
            "Máximo: 200 resultados"
        )


data = (
    st.session_state
    .historico[-MAX_HIST:]
)


# ============================================================
# ANÁLISE
# ============================================================

if data:

    rows = analisar(
        data,
        direcao
    )

    top22 = rows[:22]

    alta = top22[:8]

    possiveis = top22[8:15]

    marcacao = top22[15:22]

    acertos, testes = backtest(
        data,
        direcao,
        22
    )

    cobertura = (
        acertos / testes * 100
        if testes
        else 0
    )

    freq = Counter(data)

    atrasos = [
        atraso(
            n,
            data
        )
        for n in NUMEROS
    ]

    avgz = mean([
        zscore(n, data)
        for n in NUMEROS
    ])

else:

    rows = []

    alta = []

    possiveis = []

    marcacao = []

    acertos = 0

    testes = 0

    cobertura = 0

    freq = Counter()

    atrasos = [0] * 37

    avgz = 0


# ============================================================
# CARDS SUPERIORES
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

metricas = [

    (
        "ÚLTIMO RESULTADO",
        str(data[-1]) if data else "—",
        "",
        ""
    ),

    (
        "BASE ANALISADA",
        str(len(data)),
        "últimos resultados",
        "blue"
    ),

    (
        "DESEMPENHO (22)",
        f"{cobertura:.1f}%",
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
        str(max(len(data)-1,0)),
        "pares observados",
        "cyan"
    )

]


for col, (
    label,
    value,
    sub,
    classe
) in zip(
    [c1,c2,c3,c4,c5],
    metricas
):

    with col:

        st.markdown(
            f"""
            <div class="metric">

                <div class="label">
                    {label}
                </div>

                <div class="value {classe}">
                    {value}
                </div>

                <div class="sub">
                    {sub}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ESCOLHAS DO ROBÔ
# ============================================================

st.markdown(
    '<div class="section">🔥 ESCOLHAS DO ROBÔ</div>',
    unsafe_allow_html=True
)

p1, p2, p3, rk = st.columns(
    [1.1,1.1,1.1,.72]
)


def card_escolhas(
    titulo,
    lista,
    classe,
    rodape,
    cor_rodape
):

    ns = [
        x["n"]
        for x in lista
    ]

    st.markdown(
        f"""
        <div class="pick {classe}">

            <h4>
                {titulo}
            </h4>

            <div>
                {balls(ns)}
            </div>

            <div
                class="footer"
                style="color:{cor_rodape}"
            >
                {rodape}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with p1:

    card_escolhas(
        "📈 8 NÚMEROS COM TENDÊNCIA ALTA",
        alta,
        "high",
        "↗ Maior força estatística no momento",
        "#15d94e"
    )


with p2:

    card_escolhas(
        "❓ 7 NÚMEROS COMO POSSÍVEL",
        possiveis,
        "possible",
        "ⓘ Números com chance secundária",
        "#129cff"
    )


with p3:

    card_escolhas(
        "🎯 7 NÚMEROS COMO MARCAÇÃO",
        marcacao,
        "mark",
        "♢ Números para cobertura e proteção",
        "#ffad21"
    )


with rk:

    html = (
        '<div class="panel">'
        '<h4>👑 TOP 5 GERAL</h4>'
    )

    for i, x in enumerate(
        rows[:5],
        1
    ):

        html += f"""
        <div class="rank">

            <span>
                {i}
                &nbsp;
                <b style="color:white">
                    {x["n"]}
                </b>
            </span>

            <b>
                {x["prob"]:.1f}
            </b>

        </div>
        """

    if not rows:

        html += (
            '<div class="line">'
            'Aguardando dados'
            '</div>'
        )

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# ESTATÍSTICAS
# ============================================================

s1,s2,s3,s4,s5 = st.columns(5)

stats = [

    (
        "📊",
        "FREQUÊNCIA (200)",
        f"Média: {len(data)/37:.2f}",
        f"Máx: {max(freq.values()) if freq else 0}",
        "blue"
    ),

    (
        "◷",
        "ATRASO MÉDIO",
        f"Média: {mean(atrasos):.1f}",
        f"Máx: {max(atrasos)}",
        "purple"
    ),

    (
        "Σ",
        "Z-SCORE MÉDIO",
        f"Média: {avgz:.2f}",
        "análise normalizada",
        "green"
    ),

    (
        "🧳",
        "MAIOR ATRASO",
        str(max(atrasos)),
        "entre os 37 números",
        "orange"
    ),

    (
        "⇄",
        "TRANSIÇÕES",
        str(max(len(data)-1,0)),
        "pares observados",
        "cyan"
    )

]


for col, (
    ico,
    titulo,
    l1,
    l2,
    classe
) in zip(
    [s1,s2,s3,s4,s5],
    stats
):

    with col:

        st.markdown(
        
