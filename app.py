import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev

st.set_page_config(
    page_title="ROBÔ RICO",
    page_icon="🎯",
    layout="wide"
)

MAX_HISTORY = 200
NUMBERS = list(range(37))

WHEEL = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

POS = {n: i for i, n in enumerate(WHEEL)}

RED = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

PRIMES = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31
}

FIB = {
    0, 1, 2, 3, 5, 8, 13, 21, 34
}

SQUARES = {
    0, 1, 4, 9, 16, 25, 36
}


if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# INTERFACE
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #071018;
    color: #edf3f7;
}

.block-container {
    max-width: 1200px;
    padding: 24px 18px 40px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
}

.brand-icon {
    font-size: 42px;
}

.brand-title {
    font-size: 32px;
    font-weight: 800;
    line-height: 1;
}

.brand-title span {
    color: #19d95b;
}

.subtitle {
    color: #91a3af;
    font-size: 13px;
    margin: 4px 0 18px 55px;
}

.card {
    background: #0b1721;
    border: 1px solid #203544;
    border-radius: 14px;
    padding: 16px;
    min-height: 105px;
}

.card-title {
    color: #9aaab5;
    font-size: 11px;
    text-transform: uppercase;
}

.card-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 6px;
}

.blue {
    color: #159cff;
}

.green {
    color: #19d95b;
}

.purple {
    color: #a86cff;
}

.cyan {
    color: #19d7e8;
}

.orange {
    color: #ffb52e;
}

.section {
    font-size: 19px;
    font-weight: 800;
    margin: 22px 0 10px;
}

.pick {
    background: #0b1721;
    border-radius: 14px;
    padding: 15px;
    min-height: 190px;
}

.pick-high {
    border: 1px solid #158f4b;
}

.pick-possible {
    border: 1px solid #087dce;
}

.pick-mark {
    border: 1px solid #c98213;
}

.pick-title {
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 12px;
}

.high-text {
    color: #19d95b;
}

.possible-text {
    color: #159cff;
}

.mark-text {
    color: #ffb52e;
}

.ball {
    display: inline-flex;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    margin: 4px 3px;
    font-weight: 800;
    border: 1px solid #60707c;
}

.red-ball {
    background: #d92532;
}

.black-ball {
    background: #05080b;
}

.zero-ball {
    background: #0cae49;
}

.note {
    margin-top: 14px;
    padding: 8px;
    border-radius: 8px;
    background: #071018;
    color: #93a5b1;
    font-size: 11px;
}

.panel {
    background: #0b1721;
    border: 1px solid #203544;
    border-radius: 14px;
    padding: 15px;
}

.panel-title {
    color: #cbd5dc;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 10px;
}

.row {
    display: flex;
    justify-content: space-between;
    padding: 7px 0;
    border-bottom: 1px solid #162a37;
    font-size: 13px;
}

.row:last-child {
    border-bottom: 0;
}

.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 700;
}

div[data-testid="stTextArea"] textarea {
    border-radius: 12px;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #6f818e;
    font-size: 11px;
    margin-top: 22px;
}

@media (max-width: 700px) {

    .brand-title {
        font-size: 27px;
    }

    .brand-icon {
        font-size: 35px;
    }

    .subtitle {
        margin-left: 48px;
    }

    .card-value {
        font-size: 25px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES
# ============================================================

def parse_numbers(text):
    text = (
        text
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
        .replace("\t", " ")
    )

    result = []

    for part in text.split():

        try:
            n = int(part)

            if 0 <= n <= 36:
                result.append(n)

        except ValueError:
            continue

    return result[-MAX_HISTORY:]


def color_name(n):

    if n == 0:
        return "Verde"

    if n in RED:
        return "Vermelho"

    return "Preto"


def wheel_distance(a, b):

    d = abs(POS[a] - POS[b])

    return min(d, 37 - d)


def wheel_mirror(n):

    return WHEEL[(POS[n] + 18) % 37]


def numeric_mirror(n):

    if n == 0:
        return 0

    return 37 - n


def delay(n, data):

    for i, value in enumerate(reversed(data)):

        if value == n:
            return i

    return len(data)


def z_score(n, data):

    if not data:
        return 0.0

    counts = Counter(data)

    values = [
        counts[x]
        for x in NUMBERS
    ]

    sd = pstdev(values)

    if sd == 0:
        return 0.0

    return (
        counts[n] - mean(values)
    ) / sd


def transition_matrix(data):

    matrix = defaultdict(Counter)

    for a, b in zip(
        data[:-1],
        data[1:]
    ):

        matrix[a][b] += 1

    return matrix


# ============================================================
# SCORE
# ============================================================

def number_score(n, data, direction):

    if not data:
        return 0.0

    last = data[-1]

    score = 0.0

    matrix = transition_matrix(data)

    windows = {
        10: 2.4,
        20: 1.9,
        37: 1.5,
        50: 1.2,
        100: 0.9,
        150: 0.6,
        200: 0.45
    }

    # Frequência
    for size, weight in windows.items():

        part = data[-size:]

        if part:

            score += (
                part.count(n)
                / len(part)
                * 100
                * weight
            )

    # Atraso
    score += min(
        delay(n, data) * 0.055,
        2.5
    )

    # Z-score
    score += (
        z_score(n, data)
        * 0.55
    )

    # Vizinhança na roda
    for previous in data[-35:]:

        d = wheel_distance(
            n,
            previous
        )

        if d == 1:
            score += 0.55

        elif d == 2:
            score += 0.28

        elif d == 3:
            score += 0.08

    # Transições / "puxa"
    total = sum(
        matrix[last].values()
    )

    if total:

        score += (
            matrix[last][n]
            / total
            * 12
        )

    # Direção
    if direction == "Direita":

        delta = (
            POS[n]
            - POS[last]
        ) % 37

    else:

        delta = (
            POS[last]
            - POS[n]
        ) % 37

    if delta == 1:
        score += 1.6

    elif delta == 2:
        score += 1.0

    elif delta == 3:
        score += 0.5

    # Espelhos
    if wheel_mirror(n) in data[-50:]:
        score += 0.55

    if numeric_mirror(n) in data[-50:]:
        score += 0.25

    # Setor da roda
    sector = POS[n] // 5

    score += (
        sum(
            POS[x] // 5 == sector
            for x in data[-50:]
        )
        / 35
    )

    # Matemática
    if n in PRIMES:
        score += 0.25

    if n in FIB:
        score += 0.20

    if n in SQUARES:
        score += 0.12

    return score


# ============================================================
# RANKING
# ============================================================

def ranking(data, direction):

    values = []

    for n in NUMBERS:

        values.append({
            "number": n,
            "score": number_score(
                n,
                data,
                direction
            )
        })

    values.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    if values:

        low = values[-1]["score"]

        high = values[0]["score"]

        span = max(
            high - low,
            1.0
        )

        for item in values:

            relative = (
                item["score"] - low
            ) / span

            item["probability"] = (
                2.0 + relative * 8.0
            )

    return values


# ============================================================
# BACKTEST
# ============================================================

def backtest(data, direction):

    if len(data) < 40:
        return 0, 0

    start = max(
        30,
        len(data) - 100
    )

    hits = 0
    tests = 0

    for i in range(
        start,
        len(data)
    ):

        previous = data[:i]

        ranked = ranking(
            previous,
            direction
        )

        selected = {
            x["number"]
            for x in ranked[:22]
        }

        if data[i] in selected:
            hits += 1

        tests += 1

    return hits, tests


# ============================================================
# BOLAS
# ============================================================

def ball_html(n):

    if n == 0:
        cls = "zero-ball"

    elif n in RED:
        cls = "red-ball"

    else:
        cls = "black-ball"

    return (
        '<span class="ball {}">{}</span>'
        .format(cls, n)
    )


def balls_html(items):

    return "".join(
        ball_html(x["number"])
        for x in items
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown("""
<div class="brand">

    <div class="brand-icon">
        🎯💵
    </div>

    <div class="brand-title">
        ROBÔ <span>RICO</span> 🤑
    </div>

</div>

<div class="subtitle">
    Estatística • Matemática • Roda • Mesa • Transições • Espelhos
</div>
""", unsafe_allow_html=True)


# ============================================================
# SENTIDO
# ============================================================

left, right = st.columns([3, 1])

with left:

    direction = st.selectbox(
        "Sentido da análise",
        [
            "Direita",
            "Esquerda"
        ]
    )

with right:

    st.markdown(
        """
        <div class="card"
             style="text-align:center;min-height:72px;">

            <div class="card-title">
                SENTIDO ATUAL
            </div>

            <div class="card-value green">
                → {}
            </div>

        </div>
        """.format(direction),
        unsafe_allow_html=True
    )


# ============================================================
# HISTÓRICO
# ============================================================

st.markdown(
    '<div class="section">📦 Histórico da roleta</div>',
    unsafe_allow_html=True
)


text = st.text_area(
    "Cole os últimos resultados",
    placeholder=(
        "Exemplo: "
        "32 23 13 35 4 20 4 14 12 4"
    ),
    height=110
)


b1, b2, b3 = st.columns(3)


with b1:

    if st.button(
        "📊 ANALISAR HISTÓRICO",
        use_container_width=True
    ):

        parsed = parse_numbers(text)

        if parsed:

            st.session_state.history = parsed

            st.rerun()

        else:

            st.warning(
                "Cole números de 0 a 36."
            )


with b2:

    if st.button(
        "📋 USAR DADOS COLADOS",
        use_container_width=True
    ):

        parsed = parse_numbers(text)

        if parsed:

            st.session_state.history = parsed

            st.rerun()

        else:

            st.warning(
                "Nenhum número válido encontrado."
            )


with b3:

    if st.button(
        "🗑️ LIMPAR",
        use_container_width=True
    ):

        st.session_state.history = []

        st.rerun()


# ============================================================
# DADOS
# ============================================================

data = (
    st.session_state.history[
        -MAX_HISTORY:
    ]
)


if data:

    ranked = ranking(
        data,
        direction
    )

else:

    ranked = []


top22 = ranked[:22]

high = top22[:8]

possible = top22[8:15]

marked = top22[15:22]


hits, tests = backtest(
    data,
    direction
)


coverage = (
    hits / tests * 100
    if tests
    else 0.0
)


counts = Counter(data)


if data:

    delays = [
        delay(n, data)
        for n in NUMBERS
    ]

else:

    delays = [0] * 37


last = (
    data[-1]
    if data
    else "—"
)


# ============================================================
# CARDS
# ============================================================

m1, m2, m3, m4, m5 = st.columns(5)


metrics = [

    (
        "ÚLTIMO RESULTADO",
        last,
        color_name(last)
        if data
        else "",
        ""
    ),

    (
        "BASE ANALISADA",
        len(data),
        "últimos resultados",
        "blue"
    ),

    (
        "DESEMPENHO (22)",
        "{:.1f}%".format(coverage),
        "backtest",
        "green"
    ),

    (
        "ESCOLHAS DO ROBÔ",
        22,
        "8 + 7 + 7",
        "purple"
    ),

    (
        "TRANSIÇÕES",
        max(len(data) - 1, 0),
        "pares observados",
        "cyan"
    )

]


for col, item in zip(
    [m1, m2, m3, m4, m5],
    metrics
):

    title, value, sub, color = item

    with col:

        st.markdown(
            """
            <div class="card">

                <div class="card-title">
                    {}
                </div>

                <div class="card-value {}">
                    {}
                </div>

                <div style="
                    color:#91a3af;
                    font-size:11px;
                ">
                    {}
                </div>

            </div>
            """.format(
                title,
                color,
                value,
                sub
            ),
            unsafe_allow_html=True
        )


# ============================================================
# ESCOLHAS
# ============================================================

st.markdown(
    '<div class="section">🔥 Escolhas do robô</div>',
    unsafe_allow_html=True
)


p1, p2, p3 = st.columns(3)


with p1:

    st.markdown(
        """
        <div class="pick pick-high">

            <div class="pick-title high-text">
                📈 8 NÚMEROS COM TENDÊNCIA ALTA
            </div>

            <div>
                {}
            </div>

            <div class="note">
                Maior força estatística no momento
            </div>

        </div>
        """.format(
            balls_html(high)
        ),
        unsafe_allow_html=True
    )


with p2:

    st.markdown(
        """
        <div class="pick pick-possible">

            <div class="pick-title possible-text">
                ❓ 7 NÚMEROS COMO POSSÍVEL
            </div>

            <div>
                {}
            </div>

            <div class="note">
                Chance secundária dentro do modelo
            </div>

        </div>
        """.format(
            balls_html(possible)
        ),
        unsafe_allow_html=True
    )


with p3:

    st.markdown(
        """
        <div class="pick pick-mark">

            <div class="pick-title mark-text">
                🎯 7 NÚMEROS COMO MARCAÇÃO
            </div>

            <div>
                {}
            </div>

            <div class="note">
                Cobertura e proteção estatística
            </div>

        </div>
        """.format(
            balls_html(marked)
        ),
        unsafe_allow_html=True
    )


# ============================================================
# RESUMO
# ============================================================

st.markdown(
    '<div class="section">📊 Resumo da análise</div>',
    unsafe_allow_html=True
)


s1, s2, s3, s4 = st.columns(4)


avg_frequency = (
    len(data) / 37
    if data
    else 0
)


max_frequency = (
    max(counts.values())
    if counts
    else 0
)


avg_delay = (
    mean(delays)
    if data
    else 0
)


max_delay = (
    max(delays)
    if data
    else 0
)


avg_z = (
    mean(
        [
            z_score(n, data)
            for n in NUMBERS
        ]
    )
    if data
    else 0
)


summary = [

    (
        "FREQUÊNCIA",
        "Média: {:.2f}".format(
            avg_frequency
        ),
        "Máxima: {}".format(
            max_frequency
        ),
        "blue"
    ),

    (
        "ATRASO",
        "Média: {:.1f}".format(
            avg_delay
        ),
        "Máximo: {}".format(
            max_delay
        ),
        "purple"
    ),

    (
        "Z-SCORE",
        "Média: {:.2f}".format(
            avg_z
        ),
        "37 números analisados",
        "green"
    ),

    (
        "BACKTEST",
        "Acertos: {}".format(
            hits
        ),
        "Testes: {} • {:.1f}%".format(
            tests,
            coverage
        ),
        "orange"
    )

]


for col, item in zip(
    [s1, s2, s3, s4],
    summary
):

    title, line1, line2, color = item

    with col:

        st.markdown(
            """
            <div class="panel">

                <div class="panel-title">
                    {}
                </div>

                <div class="{}"
                     style="
                     font-size:19px;
                     font-weight:800;
                     ">
                    {}
                </div>

                <div style="
                    color:#91a3af;
                    font-size:12px;
                    margin-top:7px;
                ">
                    {}
                </div>

            </div>
            """.format(
                title,
                color,
                line1,
                line2
            ),
            unsafe_allow_html=True
        )


# ============================================================
# MATEMÁTICA
# ============================================================

st.markdown(
    '<div class="section">🧮 Padrões matemáticos</div>',
    unsafe_allow_html=True
)


q1, q2, q3 = st.columns(3)


with q1:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-title">
                PADRÕES
            </div>

            <div class="row">
                <span>Primos</span>
                <b>{}</b>
            </div>

            <div class="row">
                <span>Fibonacci</span>
                <b>{}</b>
            </div>

            <div class="row">
                <span>Quadrados</span>
                <b>{}</b>
            </div>

        </div>
        """.format(
            sum(x in PRIMES for x in data),
            sum(x in FIB for x in data),
            sum(x in SQUARES for x in data)
        ),
        unsafe_allow_html=True
    )


with q2:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-title">
                CLASSIFICAÇÕES
            </div>

            <div class="row">
                <span>🔴 Vermelhos</span>
                <b>{}</b>
            </div>

            <div class="row">
                <span>⚫ Pretos</span>
                <b>{}</b>
            </div>

            <div class="row">
                <span>🟢 Zeros</span>
                <b>{}</b>
            </div>

        </div>
        """.format(
            sum(x in RED for x in data),
            sum(
                x != 0 and x not in RED
                for x in data
            ),
            data.count(0)
        ),
        unsafe_allow_html=True
    )


with q3:

    html = (
        '<div class="panel">'
        '<div class="panel-title">'
        'ÚLTIMAS JANELAS'
        '</div>'
    )

    for size in [
        10,
        20,
        37,
        50,
        100,
        150,
        200
    ]:

        part = data[-size:]

        va
