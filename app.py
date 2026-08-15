import streamlit as st
from collections import Counter

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

# ============================================================
# ROLETA EUROPEIA
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
# MEMÓRIA DO APLICATIVO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "base_110" not in st.session_state:
    st.session_state.base_110 = []

if "analisado" not in st.session_state:
    st.session_state.analisado = False

if "ultimo_adicionado" not in st.session_state:
    st.session_state.ultimo_adicionado = None


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
            numero = int(item)

            if 0 <= numero <= 36:
                numeros.append(numero)

        except:
            pass

    return numeros


def distancia_roda(a, b):
    if a not in ROULETA or b not in ROULETA:
        return 0

    pa = ROULETA.index(a)
    pb = ROULETA.index(b)

    distancia = abs(pa - pb)

    return min(distancia, 37 - distancia)


def vizinhos(numero, quantidade=11):
    if numero not in ROULETA:
        return [], []

    posicao = ROULETA.index(numero)

    esquerda = [
        ROULETA[(posicao - i) % 37]
        for i in range(1, quantidade + 1)
    ]

    direita = [
        ROULETA[(posicao + i) % 37]
        for i in range(1, quantidade + 1)
    ]

    return esquerda, direita


def faixa(numero):
    if numero <= 9:
        return "0-9"

    if numero <= 19:
        return "10-19"

    if numero <= 29:
        return "20-29"

    return "30-36"


def soma_digitos(numero):
    return sum(int(x) for x in str(numero))


# ============================================================
# MOTOR DE ANÁLISE
# ============================================================

def analisar(historico):

    if len(historico) < 1:
        return None

    ultimo = historico[-1]

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

    esquerda, direita = vizinhos(ultimo)

    candidatos = esquerda + direita

    # Remove duplicados mantendo a ordem
    candidatos = list(dict.fromkeys(candidatos))

    scores = {}
    detalhes = {}

    # ========================================================
    # ESTATÍSTICAS GERAIS
    # ========================================================

    def proporcao(lista, condicao):

        if not lista:
            return 0

        return sum(
            1 for n in lista
            if condicao(n)
        ) / len(lista)

    pares_total = proporcao(
        [n for n in historico if n != 0],
        lambda n: n % 2 == 0
    )

    pares_30 = proporcao(
        [n for n in ultimos_30 if n != 0],
        lambda n: n % 2 == 0
    )

    primos_total = proporcao(
        historico,
        lambda n: n in PRIMOS
    )

    primos_30 = proporcao(
        ultimos_30,
        lambda n: n in PRIMOS
    )

    fibonacci_total = proporcao(
        historico,
        lambda n: n in FIBONACCI
    )

    fibonacci_30 = proporcao(
        ultimos_30,
        lambda n: n in FIBONACCI
    )

    faixas_total = Counter(
        faixa(n)
        for n in historico
    )

    faixas_30 = Counter(
        faixa(n)
        for n in ultimos_30
    )

    # ========================================================
    # SCORE DE CADA CANDIDATO
    # ========================================================

    for numero in candidatos:

        score = 0
        motivos = []

        # ----------------------------------------------------
        # FREQUÊNCIA
        # ----------------------------------------------------

        score += freq_total[numero] * 0.3
        score += freq_110[numero] * 1.2
        score += freq_50[numero] * 1.8
        score += freq_30[numero] * 2.2
        score += freq_20[numero] * 2.7
        score += freq_10[numero] * 3.0

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

            score += min(atraso, 30) * 0.30

            motivos.append("atraso")

        # ----------------------------------------------------
        # DISTÂNCIA NA RODA
        # ----------------------------------------------------

        distancia = distancia_roda(
            ultimo,
            numero
        )

        if distancia <= 3:

            score += 5

            motivos.append(
                "vizinho próximo"
            )

        elif distancia <= 6:

            score += 3

        elif distancia <= 10:

            score += 1

        # ----------------------------------------------------
        # CONCENTRAÇÃO DOS ÚLTIMOS 30
        # ----------------------------------------------------

        concentracao = sum(
            1
            for resultado in ultimos_30
            if distancia_roda(
                resultado,
                numero
            ) <= 2
        )

        score += concentracao * 1.2

        if concentracao >= 2:

            motivos.append(
                "concentração na roda"
            )

        # ----------------------------------------------------
        # PRIMOS
        # ----------------------------------------------------

        if numero in PRIMOS:

            diferenca = (
                primos_30 -
                primos_total
            )

            score += diferenca * 25

            if diferenca > 0:
                motivos.append(
                    "padrão de primos"
                )

        # ----------------------------------------------------
        # FIBONACCI
        # ----------------------------------------------------

        if numero in FIBONACCI:

            diferenca = (
                fibonacci_30 -
                fibonacci_total
            )

            score += diferenca * 25

            if diferenca > 0:
                motivos.append(
                    "padrão Fibonacci"
                )

        # ----------------------------------------------------
        # PAR / ÍMPAR
        # ----------------------------------------------------

        if numero != 0:

            if numero % 2 == 0:

                diferenca = (
                    pares_30 -
                    pares_total
                )

                score += diferenca * 15

                if diferenca > 0:
                    motivos.append(
                        "tendência par"
                    )

            else:

                diferenca = (
                    (1 - pares_30) -
                    (1 - pares_total)
                )

                score += diferenca * 15

                if diferenca > 0:
                    motivos.append(
                        "tendência ímpar"
                    )

        # ----------------------------------------------------
        # FAIXAS
        # ----------------------------------------------------

        f = faixa(numero)

        total_faixa = (
            faixas_total[f]
            / len(historico)
        )

        recente_faixa = (
            faixas_30[f]
            / len(ultimos_30)
        )

        diferenca_faixa = (
            recente_faixa -
            total_faixa
        )

        score += diferenca_faixa * 30

        if diferenca_faixa > 0:

            motivos.append(
                "faixa em destaque"
            )

        # ----------------------------------------------------
        # SOMA DOS ALGARISMOS
        # ----------------------------------------------------

        soma = soma_digitos(numero)

        soma_total = sum(
            1
            for n in historico
            if soma_digitos(n) == soma
        )

        soma_recente = sum(
            1
            for n in ultimos_30
            if soma_digitos(n) == soma
        )

        if soma_total > 0:

            esperado = (
                soma_total /
                len(historico)
                * len(ultimos_30)
            )

            if soma_recente > esperado:

                score += 2

                motivos.append(
                    "soma dos algarismos"
                )

        # ----------------------------------------------------
        # DISTÂNCIAS ENTRE GIROS
        # ----------------------------------------------------

        if len(historico) >= 2:

            distancias = []

            for i in range(
                1,
                len(historico)
            ):

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

                    score += 2

                    motivos.append(
                        "padrão de distância"
                    )

        # ----------------------------------------------------
        # REPETIÇÕES DE PADRÃO
        # ----------------------------------------------------

        repeticoes = sum(
            1
            for resultado in ultimos_20
            if distancia_roda(
                resultado,
                numero
            ) == distancia
        )

        score += repeticoes * 0.5

        if repeticoes >= 2:

            motivos.append(
                "repetição de padrão"
            )

        scores[numero] = score

        detalhes[numero] = {
            "score": score,
            "frequencia": freq_total[numero],
            "freq_110": freq_110[numero],
            "freq_50": freq_50[numero],
            "freq_30": freq_30[numero],
            "freq_20": freq_20[numero],
            "freq_10": freq_10[numero],
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

    # 22 candidatos
    ranking_22 = ranking[:22]

    # divisão dos grupos
    probabilidade = ranking_22[:8]

    marcacoes = ranking_22[8:15]

    possiveis = ranking_22[15:22]

    return {
        "ultimo": ultimo,
        "ranking": ranking_22,
        "probabilidade": probabilidade,
        "marcacoes": marcacoes,
        "possiveis": possiveis,
        "scores": scores,
        "detalhes": detalhes
    }


# ============================================================
# TÍTULO
# ============================================================

st.title("🎯 ROBÔ SGU")

st.header(
    "MOTOR MATEMÁTICO ADAPTATIVO"
)

st.caption(
    "Análise estatística baseada no histórico informado."
)


# ============================================================
# 1 — OS 110 RESULTADOS
# ============================================================

st.markdown(
    "## 📋 1. COLE OS 110 ÚLTIMOS RESULTADOS"
)

texto_110 = st.text_area(
    "Últimos 110 resultados",
    placeholder="Cole os 110 números aqui...",
    height=180
)

if st.button(
    "📊 ANALISAR 110 RESULTADOS",
    use_container_width=True
):

    resultados = ler_resultados(
        texto_110
    )

    if len(resultados) != 110:

        st.error(
            f"⚠️ Foram encontrados "
            f"{len(resultados)} números. "
            f"É necessário colocar exatamente 110."
        )

    else:

        st.session_state.base_110 = (
            resultados.copy()
        )

        st.session_state.historico = (
            resultados.copy()
        )

        st.session_state.analisado = True

        st.session_state.ultimo_adicionado = (
            resultados[-1]
        )

        st.success(
            "✅ Os 110 resultados foram carregados."
        )

        st.rerun()


# ============================================================
# 2 — ADICIONAR RESULTADO NOVO
# ============================================================
#
# IMPORTANTE:
# Esta parte fica FORA do if analisado.
# Portanto o botão aparece na tela desde o início.
# ============================================================

st.divider()

st.markdown(
    "## 🎰 2. ÚLTIMO RESULTADO"
)

st.caption(
    "Depois da análise inicial, coloque aqui cada novo "
    "resultado da roleta, um por vez."
)

novo_numero = st.number_input(
    "Número que acabou de sair",
    min_value=0,
    max_value=36,
    value=0,
    step=1,
    key="novo_numero"
)

if st.button(
    "➕ ADICIONAR ÚLTIMO RESULTADO",
    use_container_width=True
):

    # Só permite adicionar depois dos 110 iniciais
    if not st.session_state.analisado:

        st.warning(
            "Primeiro carregue e analise os 110 resultados."
        )

    else:

        numero = int(novo_numero)

        st.session_state.historico.append(
            numero
        )

        st.session_state.ultimo_adicionado = (
            numero
        )

        st.success(
            f"✅ Resultado {numero} adicionado ao histórico."
        )

        st.rerun()


# ============================================================
# 3 — HISTÓRICO CONTÍNUO
# ============================================================

if st.session_state.analisado:

    historico = (
        st.session_state.historico
    )

    st.divider()

    st.markdown(
        "## 📜 HISTÓRICO CONTÍNUO"
    )

    st.info(
        f"📈 Total acumulado: "
        f"{len(historico)} resultados"
    )

    # Mostra os últimos resultados primeiro
    st.write(
        " • ".join(
            str(n)
            for n in reversed(historico[-50:])
        )
    )

    # ========================================================
    # ANÁLISE ATUAL
    # ========================================================

    resultado = analisar(
        historico
    )

    if resultado:

        ultimo = resultado["ultimo"]

        st.divider()

        st.markdown(
            f"## 🔥 ANÁLISE ATUAL — ÚLTIMO: {ultimo}"
        )

        # ----------------------------------------------------
        # 22
        # ----------------------------------------------------

        st.markdown(
            "### 📊 22 CANDIDATOS"
        )

        st.write(
            " • ".join(
                str(n)
                for n in resultado["ranking"]
            )
        )

        # ----------------------------------------------------
        # PROBABILIDADE
        # ----------------------------------------------------

        st.markdown(
            "### 🔥 PROBABILIDADE"
        )

        st.write(
            " • ".join(
                str(n)
                for n in resultado[
                    "probabilidade"
                ]
            )
        )

        # ----------------------------------------------------
        # MARCAÇÕES
        # ----------------------------------------------------

        st.markdown(
            "### 🎯 MARCAÇÕES"
        )

        st.write(
            " • ".join(
                str(n)
                for n in resultado[
                    "marcacoes"
                ]
            )
        )

        # ----------------------------------------------------
        # POSSÍVEIS
        # ----------------------------------------------------

        st.markdown(
            "### 🔎 POSSÍVEIS"
        )

        st.write(
            " • ".join(
                str(n)
                for n in resultado[
                    "possiveis"
                ]
            )
        )

        # ----------------------------------------------------
        # VIZINHOS
        # ----------------------------------------------------

        esquerda, direita = vizinhos(
            ultimo
        )

        st.markdown(
            "### 🎰 VIZINHOS DO ÚLTIMO"
        )

        st.write(
            "⬅️ Esquerda: "
            + " • ".join(
                str(n)
                for n in esquerda
            )
        )

        st.write(
            "➡️ Direita: "
            + " • ".join(
                str(n)
                for n in direita
            )
        )

        # ====================================================
        # RESUMO
        # ====================================================

        st.divider()

        st.markdown(
            f"## 📊 RESUMO DO {ultimo}"
        )

        st.write(
            "🔥 Probabilidade: "
            + ", ".join(
                str(n)
                for n in resultado[
                    "probabilidade"
                ]
            )
        )

        st.write(
            "🎯 Marcações: "
            + ", ".join(
                str(n)
                for n in resultado[
                    "marcacoes"
                ]
            )
        )

        st.write(
            "🔎 Possíveis: "
            + ", ".join(
                str(n)
                for n in resultado[
                    "possiveis"
                ]
            )
        )

        # ====================================================
        # DETALHES MATEMÁTICOS
        # ====================================================

        st.divider()

        st.markdown(
            "## 🧠 DETALHES MATEMÁTICOS"
        )

        for numero in resultado["ranking"]:

            dados = resultado[
                "detalhes"
            ][numero]

            with st.expander(
                f"🔢 {numero} — Score {dados['score']:.2f}"
            ):

                if dados["motivos"]:

                    st.write(
                        "**Sinais encontrados:** "
                        + ", ".join(
                            dados["motivos"]
                        )
                    )

                else:

                    st.write(
                        "**Sinais encontrados:** "
                        "nenhum destaque específico."
                    )

                st.write(
                    f"Frequência total: "
                    f"{dados['frequencia']}"
                )

                st.write(
                    f"Frequência nos 110: "
                    f"{dados['freq_110']}"
                )

                st.write(
                    f"Frequência nos 50: "
                    f"{dados['freq_50']}"
                )

                st.write(
                    f"Frequência nos 30: "
                    f"{dados['freq_30']}"
                )

                st.write(
                    f"Frequência nos 20: "
                    f"{dados['freq_20']}"
                )

                st.write(
                    f"Frequência nos 10: "
                    f"{dados['freq_10']}"
                )

                st.write(
                    f"Atraso: "
                    f"{dados['atraso']}"
                )

                st.write(
                    f"Distância na roda: "
                    f"{dados['distancia']}"
                )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "ROBÔ SGU — análise estatística adaptativa. "
    "Os cálculos identificam padrões no histórico, "
    "mas não garantem o próximo resultado."
)
