import streamlit as st
from collections import Counter
import math

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

# ============================================================
# ROleta europeia - ordem física da roda
# ============================================================

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

# ============================================================
# MEMÓRIA
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "base_110" not in st.session_state:
    st.session_state.base_110 = []

if "analisado" not in st.session_state:
    st.session_state.analisado = False

if "ultimo" not in st.session_state:
    st.session_state.ultimo = None


# ============================================================
# FUNÇÕES
# ============================================================

def ler_resultados(texto):
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

        except ValueError:
            pass

    return numeros


def distancia_roda(a, b):
    pa = ROULETA.index(a)
    pb = ROULETA.index(b)

    d = abs(pa - pb)

    return min(d, 37 - d)


def vizinhos_do_numero(numero):
    pos = ROULETA.index(numero)

    esquerda = [
        ROULETA[(pos - i) % 37]
        for i in range(1, 12)
    ]

    direita = [
        ROULETA[(pos + i) % 37]
        for i in range(1, 12)
    ]

    return esquerda, direita


def soma_digitos(numero):
    return sum(int(x) for x in str(numero))


def faixa(numero):
    if numero <= 9:
        return "0-9"
    if numero <= 19:
        return "10-19"
    if numero <= 29:
        return "20-29"
    return "30-36"


def analisar(historico, ultimo):

    if len(historico) == 0:
        return None

    # Os 22 candidatos são definidos pela posição
    # do último número na roda.
    esquerda, direita = vizinhos_do_numero(ultimo)

    candidatos = esquerda + direita

    # Janelas estatísticas
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

    # --------------------------------------------------------
    # Propriedades matemáticas observadas no histórico
    # --------------------------------------------------------

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

    fib_total = proporcao(
        historico,
        lambda n: n in FIBONACCI
    )

    fib_recente = proporcao(
        ultimos_30,
        lambda n: n in FIBONACCI
    )

    pares_total = proporcao(
        [n for n in historico if n != 0],
        lambda n: n % 2 == 0
    )

    pares_recente = proporcao(
        [n for n in ultimos_30 if n != 0],
        lambda n: n % 2 == 0
    )

    faixas_total = Counter(
        faixa(n) for n in historico
    )

    faixas_recente = Counter(
        faixa(n) for n in ultimos_30
    )

    scores = {}
    detalhes = {}

    # ========================================================
    # SCORE DOS 22
    # ========================================================

    for numero in candidatos:

        score = 0.0
        motivos = []

        # ----------------------------------------------------
        # FREQUÊNCIA
        # ----------------------------------------------------

        score += freq_total[numero] * 0.4
        score += freq_110[numero] * 1.5
        score += freq_50[numero] * 2.0
        score += freq_30[numero] * 2.5
        score += freq_20[numero] * 3.0
        score += freq_10[numero] * 3.5

        if freq_30[numero] > 0:
            motivos.append("frequência recente")

        # ----------------------------------------------------
        # ATRASO
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # DISTÂNCIA NA RODA
        # ----------------------------------------------------

        distancia = distancia_roda(
            ultimo,
            numero
        )

        score += max(
            0,
            12 - distancia
        ) * 1.2

        if distancia <= 3:
            motivos.append("vizinho próximo")

        # ----------------------------------------------------
        # CONCENTRAÇÃO DE VIZINHOS
        # ----------------------------------------------------

        concentracao = 0

        for resultado in ultimos_30:

            if distancia_roda(
                resultado,
                numero
            ) <= 2:

                concentracao += 1

        score += concentracao * 1.3

        if concentracao >= 2:
            motivos.append("concentração na roda")

        # ----------------------------------------------------
        # PRIMOS
        # ----------------------------------------------------

        if numero in PRIMOS:

            diferenca = (
                primo_recente - primo_total
            )

            score += diferenca * 30

            if diferenca > 0:
                motivos.append("padrão primo")

        # ----------------------------------------------------
        # FIBONACCI
        # ----------------------------------------------------

        if numero in FIBONACCI:

            diferenca = (
                fib_recente - fib_total
            )

            score += diferenca * 30

            if diferenca > 0:
                motivos.append("padrão Fibonacci")

        # ----------------------------------------------------
        # PAR / ÍMPAR
        # ----------------------------------------------------

        if numero != 0:

            if numero % 2 == 0:

                diferenca = (
                    pares_recente - pares_total
                )

                score += diferenca * 20

                if diferenca > 0:
                    motivos.append("padrão par")

            else:

                diferenca = (
                    (1 - pares_recente)
                    - (1 - pares_total)
                )

                score += diferenca * 20

                if diferenca > 0:
                    motivos.append("padrão ímpar")

        # ----------------------------------------------------
        # FAIXA
        # ----------------------------------------------------

        f = faixa(numero)

        total_faixa = (
            faixas_total[f]
            / len(historico)
        )

        recente_faixa = (
            faixas_recente[f]
            / len(ultimos_30)
        )

        diferenca_faixa = (
            recente_faixa - total_faixa
        )

        score += diferenca_faixa * 30

        if diferenca_faixa > 0:
            motivos.append("faixa em destaque")

        # ----------------------------------------------------
        # SOMA DOS ALGARISMOS
        # ----------------------------------------------------

        soma = soma_digitos(numero)

        total_soma = sum(
            1 for n in historico
            if soma_digitos(n) == soma
        )

        recente_soma = sum(
            1 for n in ultimos_30
            if soma_digitos(n) == soma
        )

        esperado = (
            total_soma / len(historico) * 30
        )

        if recente_soma > esperado:
            score += 2
            motivos.append("soma dos algarismos")

        # ----------------------------------------------------
        # PADRÃO DE DISTÂNCIA ENTRE RESULTADOS
        # ----------------------------------------------------

        if len(historico) >= 2:

            distancias = []

            for i in range(1, len(historico)):

                distancias.append(
                    distancia_roda(
                        historico[i - 1],
                        historico[i]
                    )
                )

            janela = distancias[-20:]

            if janela:

                media = (
                    sum(janela)
                    / len(janela)
                )

                if abs(
                    distancia - media
                ) <= 2:

                    score += 3
                    motivos.append(
                        "padrão de distância"
                    )

        # ----------------------------------------------------
        # REPETIÇÃO DE PADRÕES
        # ----------------------------------------------------

        repeticoes = 0

        for resultado in ultimos_20:

            if distancia_roda(
                resultado,
                numero
            ) == distancia:

                repeticoes += 1

        score += repeticoes * 0.6

        if repeticoes >= 2:
            motivos.append(
                "repetição de padrão"
            )

        scores[numero] = score

        detalhes[numero] = {
            "score": score,
            "frequencia": freq_total[numero],
            "ultimos_110": freq_110[numero],
            "ultimos_50": freq_50[numero],
            "ultimos_30": freq_30[numero],
            "ultimos_20": freq_20[numero],
            "ultimos_10": freq_10[numero],
            "atraso": atraso,
            "distancia": distancia,
            "motivos": motivos
        }

    # ========================================================
    # RANKING
    # ========================================================

    ranking = sorted(
        candidatos,
        key=lambda n: scores[n],
        reverse=True
    )

    return {
        "ranking": ranking,
        "probabilidade": ranking[:8],
        "marcacoes": ranking[8:15],
        "possiveis": ranking[15:22],
        "scores": scores,
        "detalhes": detalhes
    }


# ============================================================
# INTERFACE
# ============================================================

st.title("🎯 ROBÔ SGU")
st.subheader("MOTOR MATEMÁTICO ADAPTATIVO")

st.caption(
    "Análise estatística baseada no histórico da roleta."
)

# ============================================================
# 1. COLE OS 110
# ============================================================

st.markdown(
    "## 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS"
)

texto_110 = st.text_area(
    "Cole os resultados",
    height=150,
    placeholder="Cole os 110 resultados aqui..."
)

if st.button(
    "📊 ANALISAR 110 RESULTADOS",
    use_container_width=True
):

    resultados = ler_resultados(texto_110)

    if len(resultados) != 110:

        st.error(
            f"Foram encontrados {len(resultados)} resultados. "
            "É necessário exatamente 110."
        )

    else:

        st.session_state.base_110 = resultados.copy()

        st.session_state.historico = resultados.copy()

        st.session_state.analisado = True

        st.session_state.ultimo = resultados[-1]

        st.success(
            "✅ 110 resultados carregados para a análise inicial."
        )


# ============================================================
# 2. ÚLTIMO NÚMERO
# ============================================================

if st.session_state.analisado:

    st.divider()

    st.markdown(
        "## 🎰 2. ÚLTIMO NÚMERO QUE SAIU"
    )

    st.number_input(
        "Digite o último número",
        min_value=0,
        max_value=36,
        value=0,
        step=1,
        key="entrada_ultimo"
    )

    # ========================================================
    # BOTÃO QUE VOCÊ PEDIU PARA MANTER
    # ========================================================

    if st.button(
        "🎯 ANALISAR ÚLTIMO NÚMERO",
        use_container_width=True
    ):

        numero = int(
            st.session_state.entrada_ultimo
        )

        # Evita registrar o mesmo número duas vezes
        # caso o usuário aperte novamente sem novo giro.
        if (
            not st.session_state.historico
            or numero != st.session_state.historico[-1]
        ):

            st.session_state.historico.append(
                numero
            )

        st.session_state.ultimo = numero

        st.rerun()

    # ========================================================
    # ANÁLISE
    # ========================================================

    historico = st.session_state.historico
    ultimo = st.session_state.ultimo

    analise = analisar(
        historico,
        ultimo
    )

    if analise:

        st.info(
            f"📈 Histórico acumulado: "
            f"{len(historico)} resultados"
        )

        st.markdown(
            f"### 🎯 Último: **{ultimo}**"
        )

        # ====================================================
        # 22
        # ====================================================

        st.markdown(
            "## 📊 22 CANDIDATOS"
        )

        st.write(
            " • ".join(
                map(
                    str,
                    analise["ranking"]
                )
            )
        )

        # ====================================================
        # 8
        # ====================================================

        st.markdown(
            "## 🔥 PROBABILIDADE — 8"
        )

        st.write(
            " • ".join(
                map(
                    str,
                    analise["probabilidade"]
                )
            )
        )

        # ====================================================
        # 7
        # ====================================================

        st.markdown(
            "## 🎯 MARCAÇÕES — 7"
        )

        st.write(
            " • ".join(
                map(
                    str,
                    analise["marcacoes"]
                )
            )
        )

        # ====================================================
        # 7
        # ====================================================

        st.markdown(
            "## 🔎 POSSÍVEIS — 7"
        )

        st.write(
            " • ".join(
                map(
                    str,
                    analise["possiveis"]
                )
            )
        )

        # ====================================================
        # VIZINHOS
        # ====================================================

        st.markdown(
            "## 🎰 VIZINHOS DO ÚLTIMO"
        )

        esquerda, direita = vizinhos_do_numero(
            ultimo
        )

        st.write(
            "⬅️ Esquerda: "
            + " • ".join(
                map(str, esquerda)
            )
        )

        st.write(
            "➡️ Direita: "
            + " • ".join(
                map(str, direita)
            )
        )

        # ====================================================
        # RESUMO
        # ====================================================

        st.markdown(
            f"## 📊 RESUMO DO {ultimo}"
        )

        st.write(
            "🔥 Probabilidade: "
            + ", ".join(
                map(
                    str,
                    analise["probabilidade"]
                )
            )
        )

        st.write(
            "🎯 Marcações: "
            + ", ".join(
                map(
                    str,
                    analise["marcacoes"]
                )
            )
        )

        st.write(
            "🔎 Possíveis: "
            + ", ".join(
                map(
                    str,
                    analise["possiveis"]
                )
            )
        )

        # ====================================================
        # DETALHES MATEMÁTICOS
        # ====================================================

        st.markdown(
            "## 🧠 DETALHES DA ANÁLISE"
        )

        for numero in analise["ranking"]:

            dados = analise["detalhes"][numero]

            with st.expander(
                f"{numero} — Score {dados['score']:.2f}"
            ):

                if dados["motivos"]:

                    st.write(
                        "**Sinais:** "
                        + ", ".join(
                            dados["motivos"]
                        )
                    )

                else:

                    st.write(
                        "**Sinais:** pontuação estatística"
                    )

                st.write(
                    f"Frequência total: "
                    f"{dados['frequencia']}"
                )

                st.write(
                    f"Últimos 110: "
                    f"{dados['ultimos_110']}"
                )

                st.write(
                    f"Últimos 50: "
                    f"{dados['ultimos_50']}"
                )

                st.write(
                    f"Últimos 30: "
                    f"{dados['ultimos_30']}"
                )

                st.write(
                    f"Últimos 20: "
                    f"{dados['ultimos_20']}"
                )

                st.write(
                    f"Últimos 10: "
                    f"{dados['ultimos_10']}"
                )

                st.write(
                    f"Atraso: "
                    f"{dados['atraso']}"
                )

                st.write(
                    f"Distância na roda: "
                    f"{dados['distancia']}"
                )

        # ====================================================
        # HISTÓRICO CONTÍNUO
        # ====================================================

        st.markdown(
            "## 📜 HISTÓRICO CONTÍNUO"
        )

        st.caption(
            f"{len(historico)} resultados acumulados"
        )

        st.write(
            " • ".join(
                map(str, historico)
            )
        )

st.divider()

st.caption(
    "ROBÔ SGU — análise estatística. "
    "Nenhuma regra matemática garante o próximo resultado."
        )
