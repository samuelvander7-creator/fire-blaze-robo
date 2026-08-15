import streamlit as st
from collections import Counter
import math

st.set_page_config(
    page_title="ROBÔ SGU",
    page_icon="🎯",
    layout="centered"
)

# ============================================================
# ROLETA EUROPEIA
# ============================================================

RODA = [
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

VERMELHOS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}


# ============================================================
# MEMÓRIA
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "analisado" not in st.session_state:
    st.session_state.analisado = False

if "analise_atual" not in st.session_state:
    st.session_state.analise_atual = None


# ============================================================
# FUNÇÕES
# ============================================================

def ler_numeros(texto):
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


def vizinhos_22(numero):
    """
    Retorna exatamente 22 números:
    11 de cada lado do último número na roda.
    O próprio número nunca entra.
    """

    pos = RODA.index(numero)

    esquerda = [
        RODA[(pos - i) % len(RODA)]
        for i in range(1, 12)
    ]

    direita = [
        RODA[(pos + i) % len(RODA)]
        for i in range(1, 12)
    ]

    return esquerda, direita


def distancia_roda(a, b):
    pa = RODA.index(a)
    pb = RODA.index(b)

    d = abs(pa - pb)

    return min(d, 37 - d)


def atraso(historico, numero):
    for i, n in enumerate(reversed(historico)):
        if n == numero:
            return i

    return len(historico)


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


def cor(numero):

    if numero == 0:
        return "zero"

    if numero in VERMELHOS:
        return "vermelho"

    return "preto"


# ============================================================
# ANÁLISE DOS 22
# ============================================================

def analisar_22(historico, ultimo):

    janela = historico[-110:]

    esquerda, direita = vizinhos_22(ultimo)

    candidatos = esquerda + direita

    freq = Counter(janela)

    freq_50 = Counter(janela[-50:])

    freq_30 = Counter(janela[-30:])

    freq_20 = Counter(janela[-20:])

    freq_10 = Counter(janela[-10:])

    scores = {}

    detalhes = {}

    # --------------------------------------------------------
    # PADRÕES GERAIS
    # --------------------------------------------------------

    total = len(janela)

    taxa_primos = (
        sum(n in PRIMOS for n in janela)
        / total
    )

    taxa_fibonacci = (
        sum(n in FIBONACCI for n in janela)
        / total
    )

    pares = [
        n for n in janela
        if n != 0
    ]

    taxa_pares = (
        sum(n % 2 == 0 for n in pares)
        / len(pares)
        if pares else 0
    )

    faixas = Counter(
        faixa(n)
        for n in janela
    )

    # ========================================================
    # CADA UM DOS 22
    # ========================================================

    for numero in candidatos:

        score = 0.0
        motivos = []

        # ----------------------------------------------------
        # 1. FREQUÊNCIA
        # ----------------------------------------------------

        score += freq[numero] * 1.5
        score += freq_50[numero] * 2
        score += freq_30[numero] * 2.5
        score += freq_20[numero] * 3
        score += freq_10[numero] * 3.5

        if freq_30[numero]:
            motivos.append("frequência recente")

        # ----------------------------------------------------
        # 2. ATRASO
        # ----------------------------------------------------

        atraso_numero = atraso(
            janela,
            numero
        )

        if atraso_numero >= 5:

            score += min(
                atraso_numero * 0.35,
                12
            )

            motivos.append("atraso")

        # ----------------------------------------------------
        # 3. DISTÂNCIA DO ÚLTIMO
        # ----------------------------------------------------

        distancia = distancia_roda(
            ultimo,
            numero
        )

        # Quanto mais próximo na roda,
        # maior o peso de vizinhança.
        score += max(
            0,
            12 - distancia
        ) * 1.3

        if distancia <= 3:
            motivos.append("vizinho próximo")

        # ----------------------------------------------------
        # 4. VIZINHOS DOS RESULTADOS RECENTES
        # ----------------------------------------------------

        proximidade = 0

        for resultado in janela[-30:]:

            d = distancia_roda(
                resultado,
                numero
            )

            if d == 1:
                proximidade += 2

            elif d == 2:
                proximidade += 1

        score += proximidade * 1.2

        if proximidade:
            motivos.append("concentração na roda")

        # ----------------------------------------------------
        # 5. PRIMOS
        # ----------------------------------------------------

        if numero in PRIMOS:

            freq_primos = sum(
                n in PRIMOS
                for n in janela[-30:]
            ) / min(
                30,
                len(janela)
            )

            diferenca = (
                freq_primos - taxa_primos
            )

            score += diferenca * 25

            if diferenca > 0:
                motivos.append("padrão primo")

        # ----------------------------------------------------
        # 6. FIBONACCI
        # ----------------------------------------------------

        if numero in FIBONACCI:

            freq_fib = sum(
                n in FIBONACCI
                for n in janela[-30:]
            ) / min(
                30,
                len(janela)
            )

            diferenca = (
                freq_fib - taxa_fibonacci
            )

            score += diferenca * 25

            if diferenca > 0:
                motivos.append("padrão Fibonacci")

        # ----------------------------------------------------
        # 7. PAR / ÍMPAR
        # ----------------------------------------------------

        if numero != 0:

            if numero % 2 == 0:

                recente = sum(
                    n != 0 and n % 2 == 0
                    for n in janela[-30:]
                ) / max(
                    1,
                    sum(
                        n != 0
                        for n in janela[-30:]
                    )
                )

                score += (
                    recente - taxa_pares
                ) * 20

                if recente > taxa_pares:
                    motivos.append("tendência par")

            else:

                recente = sum(
                    n != 0 and n % 2 != 0
                    for n in janela[-30:]
                ) / max(
                    1,
                    sum(
                        n != 0
                        for n in janela[-30:]
                    )
                )

                tendencia_impar = 1 - taxa_pares

                score += (
                    recente - tendencia_impar
                ) * 20

                if recente > tendencia_impar:
                    motivos.append("tendência ímpar")

        # ----------------------------------------------------
        # 8. MÚLTIPLOS
        # ----------------------------------------------------

        multiplos = 0

        for divisor in [2, 3, 4, 5, 6, 9]:

            if numero != 0 and numero % divisor == 0:

                multiplos += 1

        score += multiplos * 0.8

        if multiplos >= 2:
            motivos.append("divisibilidade")

        # ----------------------------------------------------
        # 9. SOMA DOS ALGARISMOS
        # ----------------------------------------------------

        soma = soma_digitos(numero)

        ocorrencias_soma = sum(
            soma_digitos(n) == soma
            for n in janela[-30:]
        )

        if ocorrencias_soma >= 3:

            score += 2

            motivos.append(
                "padrão de soma"
            )

        # ----------------------------------------------------
        # 10. FAIXA
        # ----------------------------------------------------

        f = faixa(numero)

        proporcao_total = (
            faixas[f] / total
        )

        proporcao_recente = (
            sum(
                faixa(n) == f
                for n in janela[-30:]
            )
            / min(30, len(janela))
        )

        if proporcao_recente > proporcao_total:

            score += (
                proporcao_recente
                - proporcao_total
            ) * 30

            motivos.append(
                "faixa recente"
            )

        # ----------------------------------------------------
        # 11. RELAÇÃO COM O ÚLTIMO
        # ----------------------------------------------------

        diferenca = abs(
            numero - ultimo
        )

        if diferenca in {
            1, 2, 3, 4, 5,
            7, 8, 9, 10,
            12, 13, 17, 18
        }:

            score += 2

            motivos.append(
                "diferença numérica"
            )

        soma_com_ultimo = (
            numero + ultimo
        )

        if soma_com_ultimo % 3 == 0:
            score += 1

        if soma_com_ultimo % 4 == 0:
            score += 1

        if soma_com_ultimo % 5 == 0:
            score += 1

        # ----------------------------------------------------
        # 12. COR
        # ----------------------------------------------------

        cor_numero = cor(numero)

        ultimas_10_cores = [
            cor(n)
            for n in janela[-10:]
        ]

        if ultimas_10_cores.count(
            cor_numero
        ) >= 6:

            score += 1.5

            motivos.append(
                "padrão de cor"
            )

        # ----------------------------------------------------
        # 13. REPETIÇÃO DE DISTÂNCIAS
        # ----------------------------------------------------

        distancias = []

        for i in range(
            1,
            len(janela)
        ):

            distancias.append(
                distancia_roda(
                    janela[i - 1],
                    janela[i]
                )
            )

        if distancias:

            recentes = distancias[-20:]

            distancia_atual = distancia

            quantidade = sum(
                abs(
                    d - distancia_atual
                ) <= 1
                for d in recentes
            )

            score += quantidade * 0.35

            if quantidade >= 3:

                motivos.append(
                    "padrão de distância"
                )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        scores[numero] = round(
            score,
            2
        )

        detalhes[numero] = {
            "score": round(score, 2),
            "frequencia": freq[numero],
            "freq_50": freq_50[numero],
            "freq_30": freq_30[numero],
            "freq_20": freq_20[numero],
            "freq_10": freq_10[numero],
            "atraso": atraso_numero,
            "distancia": distancia,
            "motivos": motivos
        }

    # ========================================================
    # RANKING DOS 22
    # ========================================================

    ranking = sorted(
        candidatos,
        key=lambda n: scores[n],
        reverse=True
    )

    return {
        "ultimo": ultimo,
        "esquerda": esquerda,
        "direita": direita,
        "ranking": ranking,
        "scores": scores,
        "detalhes": detalhes
    }


# ============================================================
# INTERFACE
# ============================================================

st.title("🤖 ROBÔ SGU")

st.caption(
    "Análise matemática adaptativa da roleta"
)

# ============================================================
# 110 INICIAIS
# ============================================================

st.subheader(
    "📥 110 RESULTADOS INICIAIS"
)

texto = st.text_area(
    "Cole os últimos 110 resultados",
    height=140,
    placeholder="Exemplo: 10 16 36 4 35..."
)

if st.button(
    "📊 ANALISAR 110 RESULTADOS",
    use_container_width=True
):

    numeros = ler_numeros(texto)

    if len(numeros) != 110:

        st.error(
            f"Foram encontrados {len(numeros)} números. "
            "Digite exatamente 110 resultados."
        )

    else:

        st.session_state.historico = (
            numeros.copy()
        )

        st.session_state.analisado = True

        ultimo = numeros[-1]

        st.session_state.analise_atual = (
            analisar_22(
                st.session_state.historico,
                ultimo
            )
        )

        st.success(
            "✅ Análise inicial concluída."
        )

        st.rerun()


# ============================================================
# NOVO RESULTADO
# ============================================================

st.divider()

st.subheader(
    "🎰 NOVO RESULTADO"
)

novo_numero = st.number_input(
    "Número que acabou de sair",
    min_value=0,
    max_value=36,
    value=0,
    step=1,
    key="novo_resultado"
)

if st.button(
    "➕ ADICIONAR RESULTADO",
    use_container_width=True
):

    if not st.session_state.analisado:

        st.warning(
            "Primeiro faça a análise dos 110 resultados."
        )

    else:

        numero = int(novo_numero)

        st.session_state.historico.append(
            numero
        )

        st.session_state.analise_atual = (
            analisar_22(
                st.session_state.historico,
                numero
            )
        )

        st.rerun()


# ============================================================
# RESULTADO DA ANÁLISE
# ============================================================

if st.session_state.analise_atual:

    analise = st.session_state.analise_atual

    st.divider()

    st.subheader(
        f"🧮 ANÁLISE MATEMÁTICA — ÚLTIMO: {analise['ultimo']}"
    )

    # ========================================================
    # 22 POSSIBILIDADES REAIS DA RODA
    # ========================================================

    st.markdown(
        "### 🎯 22 POSSIBILIDADES"
    )

    st.info(
        " • ".join(
            f"{n:02d}"
            for n in analise["ranking"]
        )
    )

    # ========================================================
    # GRUPOS
    # ========================================================

    ranking = analise["ranking"]

    st.markdown(
        "### 🔥 PROBABILIDADE — 8"
    )

    st.write(
        " • ".join(
            f"{n:02d}"
            for n in ranking[:8]
        )
    )

    st.markdown(
        "### 🎯 MARCAÇÕES — 7"
    )

    st.write(
        " • ".join(
            f"{n:02d}"
            for n in ranking[8:15]
        )
    )

    st.markdown(
        "### 🔎 POSSÍVEIS — 7"
    )

    st.write(
        " • ".join(
            f"{n:02d}"
            for n in ranking[15:22]
        )
    )

    # ========================================================
    # POSIÇÃO NA RODA
    # ========================================================

    with st.expander(
        "🎰 Ver os 11 números de cada lado"
    ):

        st.write(
            "⬅️ "
            + " • ".join(
                f"{n:02d}"
                for n in analise["esquerda"]
            )
        )

        st.write(
            "➡️ "
            + " • ".join(
                f"{n:02d}"
                for n in analise["direita"]
            )
        )

    # ========================================================
    # DETALHES
    # ========================================================

    with st.expander(
        "🧠 Ver análise matemática dos 22"
    ):

        for pos, numero in enumerate(
            ranking,
            start=1
        ):

            d = analise["detalhes"][numero]

            motivos = d["motivos"]

            if motivos:
                texto_motivos = ", ".join(
                    motivos
                )
            else:
                texto_motivos = (
                    "sem sinal específico"
                )

            st.write(
                f"**{pos:02d}. {numero:02d}** "
                f"— força {d['score']:.2f} "
                f"— {texto_motivos}"
            )

            st.caption(
                f"Frequência 110: {d['frequencia']} | "
                f"50: {d['freq_50']} | "
                f"30: {d['freq_30']} | "
                f"20: {d['freq_20']} | "
                f"10: {d['freq_10']} | "
                f"Atraso: {d['atraso']} | "
                f"Distância: {d['distancia']}"
            )

    # ========================================================
    # HISTÓRICO
    # ========================================================

    st.divider()

    st.subheader(
        "📜 HISTÓRICO"
    )

    historico = st.session_state.historico

    st.caption(
        f"Histórico acumulado: "
        f"{len(historico)} resultados"
    )

    # Últimos 110 usados na análise
    janela = historico[-110:]

    st.caption(
        f"Janela matemática atual: "
        f"{len(janela)} resultados"
    )

    for i in range(
        0,
        len(janela),
        10
    ):

        linha = janela[i:i + 10]

        st.code(
            " ".join(
                f"{n:02d}"
                for n in linha
            )
        )

st.divider()

st.caption(
    "O ranking é estatístico. "
    "Em uma roleta justa, cada número individual "
    "continua tendo a mesma probabilidade matemática."
)
