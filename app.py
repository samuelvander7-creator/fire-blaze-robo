import streamlit as st
from collections import Counter, defaultdict
from statistics import mean, pstdev
import math

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

JANELA_PRINCIPAL = 200

JANELAS = [10, 20, 37, 50, 100, 150, 200]

# ============================================================
# INTERFACE COMPACTA
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-size: 10px !important;
}

p, label, span {
    font-size: 10px !important;
}

h1 {
    font-size: 20px !important;
    margin: 2px 0 5px 0 !important;
}

h2 {
    font-size: 15px !important;
    margin: 4px 0 !important;
}

h3 {
    font-size: 12px !important;
    margin: 3px 0 !important;
}

.stButton button {
    font-size: 10px !important;
    min-height: 31px !important;
    padding: 2px 5px !important;
}

textarea,
input {
    font-size: 10px !important;
}

.numero {
    display: inline-block;
    padding: 3px 5px;
    margin: 1px;
    border: 1px solid #777;
    border-radius: 4px;
    font-weight: bold;
}

.destaque {
    display: inline-block;
    padding: 4px 6px;
    margin: 1px;
    border: 2px solid #777;
    border-radius: 4px;
    font-weight: bold;
}

.caixa {
    padding: 5px;
    border: 1px solid #777;
    border-radius: 6px;
    margin: 4px 0;
}

.small {
    font-size: 9px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ORDEM FÍSICA DA ROLETA EUROPEIA
# ============================================================

RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

POSICAO = {
    n: i for i, n in enumerate(RODA)
}

NUMEROS = list(range(37))


# ============================================================
# CARACTERÍSTICAS DA ROLETA
# ============================================================

PRIMOS = {
    2, 3, 5, 7, 11, 13,
    17, 19, 23, 29, 31
}

FIBONACCI = {
    0, 1, 2, 3, 5,
    8, 13, 21, 34
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

PRETOS = set(NUMEROS) - VERMELHOS - {0}


# ============================================================
# MEMÓRIA
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "iniciado" not in st.session_state:
    st.session_state.iniciado = False

if "ultimo" not in st.session_state:
    st.session_state.ultimo = None

if "previsoes" not in st.session_state:
    st.session_state.previsoes = []

if "acertos" not in st.session_state:
    st.session_state.acertos = 0

if "total_previsoes" not in st.session_state:
    st.session_state.total_previsoes = 0


# ============================================================
# FUNÇÕES BÁSICAS
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
            n = int(item)

            if 0 <= n <= 36:
                numeros.append(n)

        except:
            pass

    return numeros


def posicao_roda(numero):
    return POSICAO[numero]


def distancia_roda(a, b):

    d = abs(
        POSICAO[a] - POSICAO[b]
    )

    return min(d, 37 - d)


def cor(numero):

    if numero == 0:
        return "zero"

    if numero in VERMELHOS:
        return "vermelho"

    return "preto"


def paridade(numero):

    if numero == 0:
        return "zero"

    return "par" if numero % 2 == 0 else "impar"


def faixa(numero):

    if numero == 0:
        return "zero"

    return "baixo" if numero <= 18 else "alto"


def duzia(numero):

    if numero == 0:
        return "zero"

    if numero <= 12:
        return "D1"

    if numero <= 24:
        return "D2"

    return "D3"


def coluna(numero):

    if numero == 0:
        return "zero"

    resto = numero % 3

    if resto == 1:
        return "C1"

    if resto == 2:
        return "C2"

    return "C3"


# ============================================================
# VIZINHOS DA RODA
# ============================================================

def vizinhos(numero, quantidade=5):

    pos = POSICAO[numero]

    esquerda = [
        RODA[(pos - i) % 37]
        for i in range(1, quantidade + 1)
    ]

    direita = [
        RODA[(pos + i) % 37]
        for i in range(1, quantidade + 1)
    ]

    return esquerda, direita


def marcacao_5(numero):

    esquerda, direita = vizinhos(
        numero,
        2
    )

    return [
        esquerda[1],
        esquerda[0],
        numero,
        direita[0],
        direita[1]
    ]


# ============================================================
# SETORES
# ============================================================

def setor_roda(numero):

    pos = POSICAO[numero]

    setor = int(
        pos / 9.25
    )

    return min(
        setor,
        3
    )


# ============================================================
# ESPELHOS NA RODA
# ============================================================

def espelho_roda(numero):

    pos = POSICAO[numero]

    espelho_pos = (
        pos + 18
    ) % 37

    return RODA[espelho_pos]


def espelho_numerico(numero):

    if numero == 0:
        return 0

    return 37 - numero


# ============================================================
# ATRASO
# ============================================================

def atraso(numero, historico):

    for i, valor in enumerate(
        reversed(historico)
    ):

        if valor == numero:
            return i

    return len(historico)


# ============================================================
# FREQUÊNCIA
# ============================================================

def frequencia(numero, historico):

    if not historico:
        return 0

    return (
        historico.count(numero)
        / len(historico)
    )


# ============================================================
# Z-SCORE
# ============================================================

def zscore(numero, historico):

    if not historico:
        return 0

    freq = Counter(
        historico
    )

    valores = [
        freq[n]
        for n in NUMEROS
    ]

    media = mean(valores)

    desvio = pstdev(valores)

    if desvio == 0:
        return 0

    return (
        freq[numero] - media
    ) / desvio


# ============================================================
# TRANSIÇÕES
#
# O QUE APARECE DEPOIS DE CADA NÚMERO
# ============================================================

def matriz_transicoes(historico):

    transicoes = defaultdict(Counter)

    for i in range(
        len(historico) - 1
    ):

        atual = historico[i]
        proximo = historico[i + 1]

        transicoes[atual][proximo] += 1

    return transicoes


def probabilidade_transicao(
    origem,
    destino,
    transicoes
):

    total = sum(
        transicoes[origem].values()
    )

    if total == 0:
        return 0

    return (
        transicoes[origem][destino]
        / total
    )


# ============================================================
# TRANSIÇÃO POR DISTÂNCIA
# ============================================================

def transicoes_por_distancia(
    centro,
    historico
):

    resultado = Counter()

    for i in range(
        len(historico) - 1
    ):

        if historico[i] == centro:

            seguinte = historico[i + 1]

            d = distancia_roda(
                centro,
                seguinte
            )

            resultado[d] += 1

    return resultado


# ============================================================
# PADRÕES DE MESA
#
# Representação aproximada da mesa:
#
# 1  4  7  10 13 16 19 22 25 28 31 34
# 2  5  8  11 14 17 20 23 26 29 32 35
# 3  6  9  12 15 18 21 24 27 30 33 36
#
# O 0 fica fora.
# ============================================================

def coordenada_mesa(numero):

    if numero == 0:
        return None

    coluna_mesa = (
        (numero - 1) // 3
    )

    linha_mesa = (
        (numero - 1) % 3
    )

    return (
        coluna_mesa,
        linha_mesa
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
        return "zero"

    dx = cb[0] - ca[0]
    dy = cb[1] - ca[1]

    return (
        dx,
        dy
    )


# ============================================================
# PADRÕES DE MOVIMENTO
# ============================================================

def assinatura_movimentos(
    historico,
    tamanho=5
):

    if len(historico) < tamanho + 1:
        return []

    movimentos = []

    inicio = max(
        1,
        len(historico) - tamanho
    )

    for i in range(
        inicio,
        len(historico)
    ):

        a = historico[i - 1]
        b = historico[i]

        movimentos.append(
            movimento_mesa(a, b)
        )

    return movimentos


# ============================================================
# ANÁLISE DE PADRÕES GEOMÉTRICOS
# ============================================================

def pontuacao_geometrica(
    numero,
    historico
):

    if len(historico) < 3:
        return 0

    ultimo = historico[-1]

    if numero == 0:
        return 0

    score = 0

    movimento_anterior = movimento_mesa(
        historico[-2],
        ultimo
    )

    movimento_candidato = movimento_mesa(
        ultimo,
        numero
    )

    if (
        movimento_anterior != "zero"
        and movimento_candidato != "zero"
    ):

        dx1, dy1 = movimento_anterior
        dx2, dy2 = movimento_candidato

        # Continuidade
        if dx1 == dx2 and dy1 == dy2:
            score += 2

        # Inversão
        if dx1 == -dx2 and dy1 == -dy2:
            score += 2

        # Zig-zag
        if (
            dx1 == -dx2
            or dy1 == -dy2
        ):
            score += 1

        # Diagonal
        if (
            abs(dx2) == 1
            and abs(dy2) == 1
        ):
            score += 1

    # Proximidade da mesa
    d = distancia_mesa(
        ultimo,
        numero
    )

    if d == 1:
        score += 2

    elif d == 2:
        score += 1

    return score


# ============================================================
# FIBONACCI / PRIMOS / QUADRADOS
# ============================================================

def propriedades_matematicas(numero):

    pontos = 0
    motivos = []

    if numero in PRIMOS:

        pontos += 1
        motivos.append("primo")

    if numero in FIBONACCI:

        pontos += 1
        motivos.append("Fibonacci")

    if numero in QUADRADOS:

        pontos += 1
        motivos.append("quadrado")

    if numero != 0:

        for divisor in [
            2, 3, 4, 5, 6, 7, 9
        ]:

            if numero % divisor == 0:

                pontos += 0.15

    return pontos, motivos


# ============================================================
# SOMA DOS ALGARISMOS
# ============================================================

def soma_digitos(numero):

    return sum(
        int(d)
        for d in str(numero)
    )


# ============================================================
# RELAÇÕES ARITMÉTICAS
# ============================================================

def relacao_aritmetica(
    numero,
    centro
):

    score = 0

    diferenca = abs(
        numero - centro
    )

    if diferenca in {
        1, 2, 3, 4, 5
    }:
        score += 1

    if (
        numero != 0
        and centro != 0
    ):

        if (
            numero % centro == 0
            or centro % numero == 0
        ):
            score += 1

    soma = numero + centro

    if soma % 3 == 0:
        score += 0.5

    if soma % 5 == 0:
        score += 0.5

    return score


# ============================================================
# CARACTERÍSTICAS RECENTES
# ============================================================

def tendencia_caracteristica(
    numero,
    historico,
    atributo
):

    janela = historico[-30:]

    if not janela:
        return 0

    valor_numero = atributo(
        numero
    )

    quantidade = sum(
        atributo(n) == valor_numero
        for n in janela
    )

    return (
        quantidade
        / len(janela)
    )


# ============================================================
# RELAÇÕES DE ESPELHO
# ============================================================

def pontuacao_espelho(
    numero,
    historico
):

    if not historico:
        return 0

    espelho_roda_numero = espelho_roda(
        numero
    )

    espelho_numerico_numero = espelho_numerico(
        numero
    )

    janela = historico[-200:]

    score = 0

    score += (
        janela.count(
            espelho_roda_numero
        ) * 0.15
    )

    score += (
        janela.count(
            espelho_numerico_numero
        ) * 0.10
    )

    return score


# ============================================================
# RELAÇÃO "PUXA"
# ============================================================

def pontuacao_puxa(
    numero,
    ultimo,
    transicoes
):

    p = probabilidade_transicao(
        ultimo,
        numero,
        transicoes
    )

    if p <= 0:
        return 0

    return p * 15


# ============================================================
# VIZINHOS HISTÓRICOS
# ============================================================

def pontuacao_vizinhos(
    numero,
    historico
):

    if not historico:
        return 0

    score = 0

    for resultado in historico[-30:]:

        d = distancia_roda(
            resultado,
            numero
        )

        if d == 1:
            score += 1

        elif d == 2:
            score += 0.5

        elif d == 3:
            score += 0.2

    return score


# ============================================================
# SETORES
# ============================================================

def pontuacao_setor(
    numero,
    historico
):

    if not historico:
        return 0

    setor = setor_roda(
        numero
    )

    recentes = historico[-50:]

    quantidade = sum(
        setor_roda(n) == setor
        for n in recentes
    )

    return (
        quantidade / 10
    )


# ============================================================
# SEQUÊNCIA DE COR
# ============================================================

def pontuacao_cor(
    numero,
    historico
):

    if not historico:
        return 0

    ultimo = historico[-1]

    if (
        cor(numero)
        == cor(ultimo)
    ):

        return 0.5

    return 0


# ============================================================
# PARIDADE
# ============================================================

def pontuacao_paridade(
    numero,
    historico
):

    recentes = [
        n
        for n in historico[-30:]
        if n != 0
    ]

    if not recentes:
        return 0

    pares = sum(
        n % 2 == 0
        for n in recentes
    )

    impares = len(
        recentes
    ) - pares

    score = 0

    if pares > impares:

        if numero != 0 and numero % 2 == 0:
            score += 1

    elif impares > pares:

        if numero != 0 and numero % 2 != 0:
            score += 1

    return score


# ============================================================
# DÚZIA / COLUNA / FAIXA
# ============================================================

def pontuacao_classificacao(
    numero,
    historico
):

    score = 0

    janela = historico[-30:]

    # Dúzia
    d = duzia(numero)

    quantidade_d = sum(
        duzia(n) == d
        for n in janela
    )

    score += (
        quantidade_d / 30
    )

    # Coluna
    c = coluna(numero)

    quantidade_c = sum(
        coluna(n) == c
        for n in janela
    )

    score += (
        quantidade_c / 30
    )

    # Baixo / alto
    f = faixa(numero)

    quantidade_f = sum(
        faixa(n) == f
        for n in janela
    )

    score += (
        quantidade_f / 30
    )

    return score


# ============================================================
# DISTÂNCIA MÉDIA DOS ÚLTIMOS RESULTADOS
# ============================================================

def pontuacao_distancia(
    numero,
    historico
):

    recentes = historico[-10:]

    if not recentes:
        return 0

    distancias = [
        distancia_roda(
            numero,
            r
        )
        for r in recentes
    ]

    media_distancia = mean(
        distancias
    )

    return max(
        0,
        5 - media_distancia * 0.4
    )


# ============================================================
# SCORE DE CADA NÚMERO
# ============================================================

def calcular_score(
    numero,
    historico,
    transicoes
):

    if not historico:
        return 0, []

    ultimo = historico[-1]

    score = 0
    motivos = []

    # ========================================================
    # 1. FREQUÊNCIA MULTIJANELA
    # ========================================================

    pesos = {
        10: 2.5,
        20: 2.0,
        37: 1.7,
        50: 1.4,
        100: 1.0,
        150: 0.8,
        200: 0.6
    }

    for janela, peso in pesos.items():

        dados = historico[-janela:]

        if dados:

            freq = (
                dados.count(numero)
                / len(dados)
            )

            score += (
                freq * peso * 100
            )

    # ========================================================
    # 2. Z-SCORE
    # ========================================================

    z = zscore(
        numero,
        historico[-200:]
    )

    score += z * 1.5

    if z > 1:
        motivos.append("frequência acima da média")

    elif z < -1:
        motivos.append("frequência abaixo da média")

    # ========================================================
    # 3. ATRASO
    # ========================================================

    atraso_numero = atraso(
        numero,
        historico[-200:]
    )

    if atraso_numero >= 5:

        score += min(
            atraso_numero * 0.08,
            3
        )

        motivos.append(
            f"atraso {atraso_numero}"
        )

    # ========================================================
    # 4. VIZINHOS
    # ========================================================

    viz = pontuacao_vizinhos(
        numero,
        historico
    )

    score += viz * 0.3

    if viz > 2:
        motivos.append("relação com vizinhos")

    # ========================================================
    # 5. DISTÂNCIA DA RODA
    # ========================================================

    dist = distancia_roda(
        numero,
        ultimo
    )

    score += max(
        0,
        6 - dist * 0.5
    )

    if dist <= 2:
        motivos.append("proximidade na roda")

    # ========================================================
    # 6. SETOR
    # ========================================================

    setor_score = pontuacao_setor(
        numero,
        historico
    )

    score += setor_score

    # ========================================================
    # 7. TRANSIÇÕES / PUXA
    # ========================================================

    puxa = pontuacao_puxa(
        numero,
        ultimo,
        transicoes
    )
