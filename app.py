import streamlit as st
from collections import Counter
import math

# =========================================================
# ROBÔ SGU
# =========================================================

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

ROULETA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

PRIMOS = {
    2, 3, 5, 7, 11, 13, 17,
    19, 23, 29, 31
}

FIBONACCI = {
    0, 1, 2, 3, 5, 8, 13, 21, 34
}

# =========================================================
# MEMÓRIA DO APP
# =========================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "base_carregada" not in st.session_state:
    st.session_state.base_carregada = False

if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = None


# =========================================================
# FUNÇÕES
# =========================================================

def ler_numeros(texto):

    texto = (
        texto
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
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


def distancia_roda(a, b):

    pa = ROULETA.index(a)
    pb = ROULETA.index(b)

    distancia = abs(pa - pb)

    return min(
        distancia,
        len(ROULETA) - distancia
    )


def vizinhos(numero):

    pos = ROULETA.index(numero)

    esquerda = [
        ROULETA[(pos - i) % 37]
        for i in range(1, 12)
    ]

    direita = [
        ROULETA[(pos + i) % 37]
        for i in range(1, 12)
    ]

    return esquerda + direita


def soma_digitos(numero):

    return sum(
        int(x)
        for x in str(numero)
    )


def faixa(numero):

    if numero <= 9:
        return "0-9"

    if numero <= 19:
        return "10-19"

    if numero <= 29:
        return "20-29"

    return "30-36"


def analisar(historico, ultimo):

    if not historico:
        return None

    # =====================================================
    # 22 CANDIDATOS
    # 11 DE CADA LADO DO ÚLTIMO NÚMERO
    # =====================================================

    candidatos = vizinhos(ultimo)

    # =====================================================
    # JANELAS
    # =====================================================

    ultimos_110 = historico[-110:]
    ultimos_50 = historico[-50:]
    ultimos_30 = historico[-30:]
    ultimos_20 = historico[-20:]
    ultimos_10 = historico[-10:]

    freq_total = Counter(historico)
    freq_110 = Counter(ultimos_110)
    freq_50 = Counter(ultimos_50)
    freq_30 = Counter(ultimos_30)
    freq_20 = Counter(ultimos_20)
    freq_10 = Counter(ultimos_10)

    # =====================================================
    # DISTRIBUIÇÕES
    # =====================================================

    def proporcao(lista, funcao):

        if not lista:
            return 0

        return sum(
            1 for n in lista
            if funcao(n)
        ) / len(lista)

    primo_total = proporcao(
        historico,
        lambda n: n in PRIMOS
    )

    primo_recente = proporcao(
        ultimos_30,
        lambda n: n in PRIMOS
    )

    fibonacci_total = proporcao(
        historico,
        lambda n: n in FIBONACCI
    )

    fibonacci_recente = proporcao(
        ultimos_30,
        lambda n: n in FIBONACCI
    )

    par_total = proporcao(
        [n for n in historico if n != 0],
        lambda n: n % 2 == 0
    )

    par_recente = proporcao(
        [n for n in ultimos_30 if n != 0],
        lambda n: n % 2 == 0
    )

    faixas_total = Counter(
        faixa(n)
        for n in historico
    )

    faixas_recente = Counter(
        faixa(n)
        for n in ultimos_30
    )

    # =====================================================
    # PONTUAÇÃO
    # =====================================================

    scores = {}
    detalhes = {}

    for numero in candidatos:

        score = 0
        motivos = []

        # -------------------------------------------------
        # FREQUÊNCIA
        # -------------------------------------------------

        score += freq_total[numero] * 0.5
        score += freq_110[numero] * 1.5
        score += freq_50[numero] * 2
        score += freq_30[numero] * 2.5
        score += freq_20[numero] * 3
        score += freq_10[numero] * 3.5

        if freq_30[numero] > 0:
            motivos.append("frequência recente")

        # -------------------------------------------------
        # ATRASO
        # -------------------------------------------------

        atraso = len(historico)

        for i, resultado in enumerate(
            reversed(historico)
        ):

            if resultado == numero:

                atraso = i
                break

        if atraso >= 10:
            score += min(atraso, 30) * 0.25
            motivos.append("atraso")

        # -------------------------------------------------
        # DISTÂNCIA NA RODA
        # -------------------------------------------------

        distancia = distancia_roda(
            ultimo,
            numero
        )

        score += max(
            0,
            12 - distancia
        ) * 1.2

        if distancia <= 3:
            motivos.append("proximidade na roda")

        # -------------------------------------------------
        # VIZINHOS DOS ÚLTIMOS RESULTADOS
        # -------------------------------------------------

        concentracao = 0

        for resultado in ultimos_30:

            if distancia_roda(
                resultado,
                numero
            ) <= 2:

                concentracao += 1

        score += concentracao * 1.3

        if concentracao >= 2:
            motivos.append("concentração de vizinhos")

        # -------------------------------------------------
        # PRIMOS
        # -------------------------------------------------

        if numero in PRIMOS:

            diferenca = (
                primo_recente
                - primo_total
            )

            score += diferenca * 30

            if diferenca > 0:
                motivos.append("padrão primo")

        # -------------------------------------------------
        # FIBONACCI
        # -------------------------------------------------

        if numero in FIBONACCI:

            diferenca = (
                fibonacci_recente
                - fibonacci_total
            )

            score += diferenca * 30

            if diferenca > 0:
                motivos.append("padrão Fibonacci")

        # -------------------------------------------------
        # PAR / ÍMPAR
        # -------------------------------------------------

        if numero != 0:

            if numero % 2 == 0:

                diferenca = (
                    par
