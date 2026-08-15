import streamlit as st
from collections import Counter
import math

# ============================================================
# ROBÔ SGU — MOTOR ESTATÍSTICO ADAPTATIVO
# ============================================================

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

# ============================================================
# ESTADO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "analisado" not in st.session_state:
    st.session_state.analisado = False

if "ultimo_analisado" not in st.session_state:
    st.session_state.ultimo_analisado = None

# ============================================================
# FUNÇÕES MATEMÁTICAS
# ============================================================

def eh_primo(n):
    if n < 2:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


def fibonacci():
    return {0, 1, 2, 3, 5, 8, 13, 21, 34}


PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
FIBONACCI = fibonacci()


def soma_digitos(n):
    return sum(int(x) for x in str(n))


def faixa(n):
    if n <= 9:
        return "0-9"
    elif n <= 19:
        return "10-19"
    elif n <= 29:
        return "20-29"
    return "30-36"


def paridade(n):
    if n == 0:
        return "zero"
    return "par" if n % 2 == 0 else "impar"


def posicao_roleta(n):
    return ROULETA.index(n)


def distancia_roleta(a, b):
    pa = posicao_roleta(a)
    pb = posicao_roleta(b)

    d = abs(pa - pb)

    return min(d, len(ROULETA) - d)


def vizinhos(n, quantidade=11):
    pos = posicao_roleta(n)

    esquerda = [
        ROULETA[(pos - i) % len(ROULETA)]
        for i in range(1, quantidade + 1)
    ]

    direita = [
        ROULETA[(pos + i) % len(ROULETA)]
        for i in range(1, quantidade + 1)
    ]

    return esquerda + direita


def parse_resultados(texto):
    texto = (
        texto
        .replace(",", " ")
        .replace(";", " ")
        .replace("\n", " ")
        .replace("\t", " ")
    )

    valores = []

    for item in texto.split():
        try:
            numero = int(item)

            if 0 <= numero <= 36:
                valores.append(numero)

        except ValueError:
            pass

    return valores


# ============================================================
# ANÁLISE
# ============================================================

def analisar(historico, ultimo):
    if len(historico) == 0:
        return None

    # --------------------------------------------------------
    # Os 22 candidatos são SEMPRE os 11 vizinhos de cada lado
    # do último número.
    # --------------------------------------------------------

    candidatos = vizinhos(ultimo, 11)

    # --------------------------------------------------------
    # Bases de análise
    # --------------------------------------------------------

    total = len(historico)

    recente_110 = historico[-110:]
    recente_50 = historico[-50:]
    recente_30 = historico[-30:]
    recente_20 = historico[-20:]
    recente_10 = historico[-10:]

    freq_total = Counter(historico)
    freq_110 = Counter(recente_110)
    freq_50 = Counter(recente_50)
    freq_30 = Counter(recente_30)
    freq_20 = Counter(recente_20)
    freq_10 = Counter(recente_10)

    # --------------------------------------------------------
    # Frequência das propriedades matemáticas
    # --------------------------------------------------------

    def taxa_propriedade(lista, func):
        if not lista:
            return 0

        return sum(
            1 for n in lista if func(n)
        ) / len(lista)

    taxa_primo_total = taxa_propriedade(
        historico,
        lambda n: n in PRIMOS
    )

    taxa_primo_recente = taxa_propriedade(
        recente_30,
        lambda n: n in PRIMOS
    )

    taxa_fib_total = taxa_propriedade(
        historico,
        lambda n: n in FIBONACCI
    )

    taxa_fib_recente = taxa_propriedade(
        recente_30,
        lambda n: n in FIBONACCI
    )

    taxa_par_total = taxa_propriedade(
        [n for n in historico if n != 0],
        lambda n: n % 2 == 0
    )

    taxa_par_recente = taxa_propriedade(
        [n for n in recente_30 if n != 0],
        lambda n: n % 2 == 0
    )

    # --------------------------------------------------------
    # Frequência das faixas
    # --------------------------------------------------------

    faixa_total = Counter(faixa(n) for n in historico)
    faixa_recente = Counter(faixa(n) for n in recente_30)

    # --------------------------------------------------------
    # Score
    # --------------------------------------------------------

    scores = {}

    detalhes = {}

    for numero in candidatos:

        score = 0
        motivos = []

        # ====================================================
        # 1. FREQUÊNCIA GERAL
        # ====================================================

        f_total = freq_total[numero]
        f_110 = freq_110[numero]
        f_50 = freq_50[numero]
        f_30 = freq_30[numero]
        f_20 = freq_20[numero]
        f_10 = freq_10[numero]

        score += f_total * 0.8
        score += f_110 * 1.8
        score += f_50 * 2.2
        score += f_30 * 2.8
        score += f_20 * 3.2
        score += f_10 * 3.8

        if f_30 > 0:
            motivos.append("frequência recente")

        # ====================================================
        # 2. ATRASO
        # ====================================================

        atraso = total

        for i, resultado in enumerate(reversed(historico)):
            if resultado == numero:
                atraso = i
                break

        if atraso > 0:
            score += min(atraso, 30) * 0.25

        if atraso >= 10:
            motivos.append("atraso")

        # ====================================================
        # 3. PROXIMIDADE DO ÚLTIMO NÚMERO
        # ====================================================

        distancia = distancia_roleta(
            ultimo,
            numero
        )

        proximidade = max(
            0,
            12 - distancia
        )

        score += proximidade * 1.5

        if distancia <= 3:
            motivos.append("vizinho próximo")

        # ====================================================
        # 4. VIZINHOS DOS RESULTADOS RECENTES
        # ====================================================

        contador_vizinhos = 0

        for resultado in recente_30:
            if distancia_roleta(
                resultado,
                numero
            ) <= 2:
                contador_vizinhos += 1

        score += contador_vizinhos * 1.4

        if contador_vizinhos >= 2:
            motivos.append("concentração de vizinhos")

        # ====================================================
        # 5. PRIMOS
        # ====================================================

        if numero in PRIMOS:

            diferenca = (
                taxa_primo_recente
                - taxa_primo_total
            )

            score += diferenca * 40

            if diferenca > 0:
                motivos.append("sinal primo")

        # ====================================================
        # 6. FIBONACCI
        # ====================================================

        if numero in FIBONACCI:

            diferenca = (
                taxa_fib_recente
                - taxa_fib_total
            )

            score += diferenca * 40

            if diferenca > 0:
                motivos.append("sinal Fibonacci")

        # ====================================================
        # 7. PAR / ÍMPAR
        # ====================================================

        if numero != 0:

            if numero % 2 == 0:

                diferenca = (
                    taxa_par_recente
                    - taxa_par_total
                )

                score += diferenca * 25

                if diferenca > 0:
                    motivos.append("sinal par")

            else:

                diferenca = (
                    (1 - taxa_par_recente)
                    - (1 - taxa_par_total)
                )

                score += diferenca * 25

                if diferenca > 0:
                    motivos.append("sinal ímpar")

        # ====================================================
        # 8. FAIXAS
        # ====================================================

        f = faixa(numero)

        proporcao_total = (
            faixa_total[f] / total
            if total else 0
        )

        proporcao_recente = (
            faixa_recente[f] / len(recente_30)
            if recente_30 else 0
        )

        diferenca_faixa = (
            proporcao_recente
            - proporcao_total
        )

        score += diferenca_faixa * 35

        if diferenca_faixa > 0:
            motivos.append("faixa em destaque")

        # ====================================================
        # 9. SOMA DOS ALGARISMOS
        # ====================================================

        soma = soma_digitos(numero)

        ocorrencias_soma_total = sum(
            1
            for n in historico
            if soma_digitos(n) == soma
        )

        ocorrencias_soma_recente = sum(
            1
            for n in recente_30
            if soma_digitos(n) == soma
        )

        if ocorrencias_soma_recente > (
            ocorrencias_soma_total / max(1, total / 30)
        ):
            score += 2
            motivos.append("soma de algarismos")

        # ====================================================
        # 10. DIFERENÇA ENTRE RESULTADOS
        # ====================================================

        if len(historico) >= 2:

            diferencas = []

            for i in range(1, len(historico)):
                d = distancia_roleta(
                    historico[i - 1],
                    historico[i]
                )

                diferencas.append(d)

            if diferencas:

                media = (
                    sum(diferencas[-20:])
                    / len(diferencas[-20:])
                )

                distancia_ultimo = distancia_roleta(
                    ultimo,
                    numero
                )

                if abs(
                    distancia_ultimo - media
                ) <= 2:

                    score += 4
                    motivos.append("padrão de distância")

        # ====================================================
        # 11. REPETIÇÃO DO PADRÃO DE VIZINHANÇA
        # ====================================================

        repeticoes = 0

        for resultado in recente_20:

            if distancia_roleta(
                resultado,
                numero
            ) == distancia:

                repeticoes += 1

        score += repeticoes * 0.8

        if repeticoes >= 2:
            motivos.append("padrão de repetição")

        # ====================================================
        # SCORE FINAL
        # ====================================================

        scores[numero] = score

        detalhes[numero] = {
            "score": score,
            "frequencia_total": f_total,
            "ultimos_110": f_110,
            "ultimos_50": f_50,
            "ultimos_30": f_30,
            "ultimos_20": f_20,
            "ultimos_10": f_10,
            "atraso": atraso,
            "distancia_roda": distancia,
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

    probabilidade = ranking[:8]
    marcacoes = ranking[8:15]
    possiveis = ranking[15:22]

    return {
        "ranking": ranking,
        "probabilidade": probabilidade,
        "marcacoes": marcacoes,
        "possiveis": possiveis,
        "scores": scores,
        "detalhes": detalhes
    }


# ============================================================
# INTERFACE
# ============================================================

st.title("🎯 ROBÔ SGU")
st.subheader("MOTOR MATEMÁTICO ADAPTATIVO")

st.caption(
    "A análise é estatística. Ela não garante o próximo resultado."
)

# ============================================================
# HISTÓRICO INICIAL
# ============================================================

st.markdown("### 📋 1. HISTÓRICO INICIAL")

texto = st.text_area(
    "Cole os 110 resultados iniciais",
    height=150,
    placeholder="Cole aqui os 110 resultados..."
)

if st.button(
    "📊 ANALISAR 110 RESULTADOS",
    use_container_width=True
):

    resultados = parse_resultados(texto)

    if len(resultados) < 110:

        st.error(
            f"Você colocou {len(resultados)} resultados. "
            f"Precisamos dos 110 iniciais."
        )

    else:

        st.session_state.historico = resultados[:110]

        st.session_state.analisado = True

        st.success(
            "✅ 110 resultados carregados."
        )


# ============================================================
# OPERAÇÃO CONTÍNUA
# ============================================================

if st.session_state.analisado:

    historico = st.session_state.historico

    st.divider()

    st.markdown("### 🎰 OPERAÇÃO CONTÍNUA")

    st.info(
        f"Histórico atual: **{len(historico)} resultados**"
    )

    ultimo = st.number_input(
        "Número que acabou de sair",
        min_value=0,
        max_value=36,
        value=0,
        step=1,
        key="numero_novo"
    )

    if st.button(
        "➕ REGISTRAR NOVO RESULTADO",
        use_container_width=True
    ):

        st.session_state.historico.append(
            int(ultimo)
        )

        st.success(
            f"Resultado {ultimo} registrado."
        )

        st.rerun()

    # ========================================================
    # ÚLTIMO RESULTADO
    # ========================================================

    ultimo_real = historico[-1]

    st.markdown(
        f"### 🎯 Último resultado: **{ultimo_real}**"
    )

    # ========================================================
    # ANÁLISE ATUAL
    # ========================================================

    analise = analisar(
        historico,
        ultimo_real
    )

    if analise:

        probabilidade = analise["probabilidade"]
        marcacoes = analise["marcacoes"]
        possiveis = analise["possiveis"]

        # ----------------------------------------------------
        # PROBABILIDADE
        # ----------------------------------------------------

        st.markdown("## 🔥 PROBABILIDADE — 8")

        st.write(
            " • ".join(
                str(n)
                for n in probabilidade
            )
        )

        # ----------------------------------------------------
        # MARCAÇÕES
        # ----------------------------------------------------

        st.markdown("## 🎯 MARCAÇÕES — 7")

        st.write(
            " • ".join(
                str(n)
                for n in marcacoes
            )
        )

        # ----------------------------------------------------
        # POSSÍVEIS
        # ----------------------------------------------------

        st.markdown("## 🟢 POSSÍVEIS — 7")

        st.write(
            " • ".join(
                str(n)
                for n in possiveis
            )
        )

        # ----------------------------------------------------
        # 22 CANDIDATOS
        # ----------------------------------------------------

        st.markdown("## 📊 22 CANDIDATOS")

        st.write(
            " • ".join(
                str(n)
                for n in analise["ranking"]
            )
        )

        # ----------------------------------------------------
        # VIZINHOS
        # ----------------------------------------------------

        st.markdown("## 🎰 VIZINHOS DO ÚLTIMO")

        viz = vizinhos(
            ultimo_real,
            11
        )

        esquerda = viz[:11]
        direita = viz[11:]

        st.write(
            "⬅️ "
            + " • ".join(
                map(str, esquerda)
            )
        )

        st.write(
            "➡️ "
            + " • ".join(
                map(str, direita)
            )
        )

        # ----------------------------------------------------
        # DETALHAMENTO
        # ----------------------------------------------------

        st.markdown("## 🧠 POR QUE OS NÚMEROS SUBIRAM?")

        for numero in analise["ranking"]:

            d = analise["detalhes"][numero]

            motivos = d["motivos"]

            motivo_texto = (
                ", ".join(motivos)
                if motivos
                else "pontuação estatística"
            )

            with st.expander(
                f"{numero} — Score {d['score']:.2f}"
            ):

                st.write(
                    f"**Motivos:** {motivo_texto}"
                )

                st.write(
                    f"Frequência total: "
                    f"{d['frequencia_total']}"
                )

                st.write(
                    f"Últimos 110: "
                    f"{d['ultimos_110']}"
                )

                st.write(
                    f"Últimos 50: "
                    f"{d['ultimos_50']}"
                )

                st.write(
                    f"Últimos 30: "
                    f"{d['ultimos_30']}"
                )

                st.write(
                    f"Últimos 20: "
                    f"{d['ultimos_20']}"
                )

                st.write(
                    f"Últimos 10: "
                    f"{d['ultimos_10']}"
                )

                st.write(
                    f"Atraso: "
                    f"{d['atraso']}"
                )

                st.write(
                    f"Distância na roda: "
                    f"{d['distancia_roda']}"
                )

        # ----------------------------------------------------
        # HISTÓRICO RECENTE
        # ----------------------------------------------------

        st.markdown("## 📜 HISTÓRICO")

        st.write(
            " • ".join(
                map(
                    str,
                    historico[-50:]
                )
            )
        )

        st.caption(
            f"Histórico acumulado: "
            f"{len(historico)} resultados"
        )

        st.caption(
            "O robô recalcula a análise a cada novo resultado."
        )
