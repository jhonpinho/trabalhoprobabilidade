"""Simulador academico - somente creditos ficticios.
Trabalho I - Probabilidade e Estatistica I (IFES Serra, 2026/2).
Uso: python simulador.py   (gera tudo em ./resultados)
"""
import csv, json, math, os, platform, random, statistics as st, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BANNER = "Simulador academico - somente creditos ficticios"
ROLO = ("A", "B", "C", "D", "E")
PAG_BASE = {"A": 5, "B": 10, "C": 15, "D": 25, "E": 50}
PAG_10 = {s: 1.10 * v for s, v in PAG_BASE.items()}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")


# ---------------------------------------------------------------- modelo
def janela(k):
    """Coluna (topo, centro, base) para a parada k."""
    return ROLO[k % 5], ROLO[(k + 1) % 5], ROLO[(k + 2) % 5]


def rodada(rng):
    """Sorteia uma parada por rolo; devolve (paradas, tabuleiro 3x3, linha central)."""
    ks = [rng.randrange(5) for _ in range(3)]
    colunas = [janela(k) for k in ks]
    centro = tuple(c[1] for c in colunas)
    return ks, colunas, centro


def premio(centro, tabela=PAG_BASE):
    """Premio bruto P: so paga se os tres simbolos centrais forem iguais."""
    return tabela[centro[0]] if centro[0] == centro[1] == centro[2] else 0


def lucro(p, aposta=1):
    return p - aposta


def centros(n, rng):
    return [rodada(rng)[2] for _ in range(n)]


def mostrar_rodada(rng):
    ks, cols, centro = rodada(rng)
    print(BANNER)
    print("Paradas K:", ks)
    for i in range(3):
        print("  ".join(c[i] for c in cols), "  <- linha central" if i == 1 else "")
    p = premio(centro)
    print(f"Premio P = {p} | Lucro X = {lucro(p)}")


# ---------------------------------------------------------------- utilidades
def salvar_csv(nome, cab, linhas):
    with open(os.path.join(OUT, nome), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows(linhas)


def media(v):
    return sum(v) / len(v)


def desvio(v):
    return st.stdev(v)


def fig(nome):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, nome), dpi=150)
    plt.close()


# ---------------------------------------------------------------- experimentos
def exp1():
    rng = random.Random(2026)
    cs = centros(10000, rng)
    P = [premio(c) for c in cs]
    X = [lucro(p) for p in P]
    valores = [-1, 4, 9, 14, 24, 49]
    cont = {v: X.count(v) for v in valores}
    assert sum(cont.values()) == 10000
    prob = {-1: 120 / 125, 4: 1 / 125, 9: 1 / 125, 14: 1 / 125, 24: 1 / 125, 49: 1 / 125}
    linhas = [[v, round(prob[v], 6), cont[v], cont[v] / 10000] for v in valores]
    salvar_csv("e1_distribuicao.csv", ["lucro_X", "prob_teorica", "contagem", "freq_relativa"], linhas)
    salvar_csv("e1_rodadas.csv", ["rodada", "t1", "t2", "t3", "P", "X"],
               [[i + 1, *c, P[i], X[i]] for i, c in enumerate(cs)])
    res = dict(media_X=media(X), rtp=media(P), prop_premio=sum(p > 0 for p in P) / 10000,
               s=desvio(X), mediana=st.median(X), contagens=cont)
    # grafico
    pos = range(6)
    plt.bar([i - 0.2 for i in pos], [prob[v] for v in valores], 0.4, label="Teoria", color="#7a7a7a")
    plt.bar([i + 0.2 for i in pos], [cont[v] / 10000 for v in valores], 0.4, label="Observado", color="#1f6f4a")
    plt.xticks(list(pos), [str(v) for v in valores])
    plt.xlabel("Lucro X por rodada (creditos)"); plt.ylabel("Proporcao de rodadas")
    plt.legend(); fig("fig_e1.png")
    return cs, P, X, res


def exp2(P2026):
    seeds = [10, 2026, 123456]
    marcos = [100, 1000, 10000]
    tab, traj = [], {}
    for s in seeds:
        rng = random.Random(s)
        X = [lucro(premio(c)) for c in centros(10000, rng)]
        if s == 2026:
            assert X == [p - 1 for p in P2026]
        acc, run = [], 0
        for i, x in enumerate(X, 1):
            run += x
            acc.append(run / i)
        traj[s] = acc
        tab.append([s] + [acc[m - 1] for m in marcos])
    salvar_csv("e2_medias_acumuladas.csv", ["semente", "n=100", "n=1000", "n=10000"], tab)
    for s in seeds:
        plt.plot(range(1, 10001), traj[s], label=f"semente {s}", lw=1)
    plt.axhline(-0.16, color="k", ls="--", label="E[X] = -0,16")
    plt.xscale("log"); plt.xlabel("Numero de rodadas"); plt.ylabel("Lucro medio acumulado (creditos)")
    plt.legend(); fig("fig_e2.png")
    a = [lucro(premio(c)) for c in centros(10, random.Random(2026))]
    repro = a == [p - 1 for p in P2026[:10]]
    return tab, repro, a


def sessao(cs_part, saldo0=100, max_rod=500, parar=None):
    """cs_part: lista de linhas centrais ja sorteadas. parar(b)->bool opcional."""
    b, traj = saldo0, [saldo0]
    for c in cs_part[:max_rod]:
        if b < 1 or (parar and parar(b)):
            break
        b += lucro(premio(c))
        traj.append(b)
    return b, len(traj) - 1, traj


def exp3():
    rng = random.Random(42)
    linhas, finais, trajs = [], [], []
    for i in range(100):
        # sorteia rodada a rodada ate o fim da sessao (sequencia continua)
        b, n, traj = 100, 0, [100]
        while n < 500 and b >= 1:
            b += lucro(premio(rodada(rng)[2])); n += 1; traj.append(b)
        finais.append(b); trajs.append(traj)
        linhas.append([i + 1, b, n, int(b < 1)])
    salvar_csv("e3_participantes.csv", ["participante", "saldo_final", "rodadas", "esgotou"], linhas)
    g = sum(b > 100 for b in finais); e = sum(b == 100 for b in finais); p = sum(b < 100 for b in finais)
    esg = sum(b < 1 for b in finais)
    assert g + e + p == 100
    res = dict(ganho=g, empate=e, perda=p, esgotou=esg, media=media(finais), mediana=st.median(finais),
               min=min(finais), max=max(finais), rod_media=media([l[2] for l in linhas]))
    salvar_csv("e3_resumo.csv", list(res.keys()), [list(res.values())])
    for i in range(5):
        t = trajs[i] + [trajs[i][-1]] * (501 - len(trajs[i]))
        plt.plot(range(501), t, lw=1, label=f"Participante {i+1}")
    plt.axhline(100, color="k", ls=":", lw=0.8)
    plt.xlabel("Rodada"); plt.ylabel("Saldo (creditos)"); plt.legend(fontsize=7); fig("fig_e3.png")
    return res


def exp4(P):
    G = [p > 0 for p in P]
    grupos = {"apos premio": [], "apos sem premio": []}
    for i in range(len(P) - 1):
        grupos["apos premio" if G[i] else "apos sem premio"].append(G[i + 1])
    assert sum(len(v) for v in grupos.values()) == 9999
    linhas = []
    for k, v in grupos.items():
        linhas.append([k, len(v), sum(v), (sum(v) / len(v)) if v else "nao estimavel"])
    salvar_csv("e4_condicional.csv", ["resultado_anterior", "total_pares", "premios_seguinte", "proporcao"], linhas)
    props = [l[3] for l in linhas]
    plt.bar(["Apos premio", "Apos sem premio"], [x * 100 for x in props], color=["#1f6f4a", "#7a7a7a"])
    plt.axhline(4, color="k", ls="--", label="Referencia: 4%")
    plt.ylabel("Rodadas seguintes premiadas (%)"); plt.legend(); fig("fig_e4.png")
    return linhas


def exp5(cs):
    out, rows = {}, []
    for nome, tab in (("Base", PAG_BASE), ("+10%", PAG_10)):
        P = [premio(c, tab) for c in cs]
        teo = sum(tab.values()) / 125
        rows.append([nome, 0.04, sum(p > 0 for p in P) / len(P), media(P), media(P) - 1,
                     teo, media(P), teo - 1])
        out[nome] = rows[-1]
    salvar_csv("e5_comparacao.csv", ["tabela", "prob_premio_teorica", "freq_premio_obs", "premio_medio_obs",
                                     "lucro_medio_obs", "RTP_teorico", "RTP_observado", "E[X]_teorico"], rows)
    plt.bar(["Base", "+10%"], [rows[0][6] * 100, rows[1][6] * 100], 0.4, color="#1f6f4a", label="Observado")
    plt.scatter(["Base", "+10%"], [rows[0][5] * 100, rows[1][5] * 100], color="k", zorder=3, label="Teorico")
    plt.axhline(100, color="r", ls="--", label="RTP = 100%")
    plt.ylabel("RTP (%)"); plt.ylim(0, 110); plt.legend(); fig("fig_e5.png")
    return rows


# ---------------------------------------------------------------- extras
def extra_ic(P):
    n = len(P); X = [p - 1 for p in P]
    m, s = media(X), desvio(X); hw = 1.96 * s / math.sqrt(n)
    ic1 = (m - hw, m + hw)
    medias = []
    for sd in range(1000, 1030):  # 30 execucoes independentes
        r = random.Random(sd)
        medias.append(media([lucro(premio(c)) for c in centros(10000, r)]))
    mm, ss = media(medias), desvio(medias); hw2 = 2.045 * ss / math.sqrt(30)
    ic2 = (mm - hw2, mm + hw2)
    cobre = sum(1 for x in medias if abs(x + 0.16) <= 1.96 * s / math.sqrt(n))
    salvar_csv("extra_ic.csv", ["metodo", "media", "limite_inf", "limite_sup"],
               [["E1 (normal, n=10000)", m, *ic1], ["30 execucoes (t, gl=29)", mm, *ic2]])
    return dict(m=m, s=s, ic1=ic1, mm=mm, ss=ss, ic2=ic2, cobre=cobre)


def extra_mesma_media():
    tabs = {"Base": PAG_BASE, "Concentrada": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 105},
            "Uniforme": {s: 21 for s in ROLO}}
    rng = random.Random(43)
    sess = [[rodada(rng)[2] for _ in range(500)] for _ in range(100)]
    rows = []
    for nome, t in tabs.items():
        ep = sum(t.values()) / 125
        ep2 = sum(v * v for v in t.values()) / 125
        dp = math.sqrt(ep2 - ep * ep)
        assert abs(ep - 0.84) < 1e-12
        fin = []
        for cs in sess:
            b = 100
            for c in cs:
                if b < 1: break
                b += premio(c, t) - 1
            fin.append(b)
        rows.append([nome, ep, 100 * sum(t.values()) / 125 / 100 * 100 / 100, 100 * sum(v > 0 for v in t.values()) / 125, dp,
                     media(fin), st.median(fin), sum(b < 100 for b in fin), sum(b < 1 for b in fin), max(fin)])
    for r in rows: r[2] = r[1] * 100
    salvar_csv("extra_mesma_media.csv", ["tabela", "E[P]", "RTP_%", "prob_premio_%", "dp_teorico_X",
                                         "saldo_medio", "saldo_mediano", "n_perdas", "n_esgotados", "saldo_max"], rows)
    return rows


def extra_exposicao():
    rng = random.Random(77)
    N = 1000
    sess = [[rodada(rng)[2] for _ in range(500)] for _ in range(N)]
    regras = {"R0: sem limite (500 rod. ou esgotar)": None,
              "R1: parar com perda de 20 (saldo<=80)": lambda b: b <= 80,
              "R2: parar com ganho de 20 (saldo>=120)": lambda b: b >= 120,
              "R3: R1 e R2 combinadas": lambda b: b <= 80 or b >= 120}
    rows = []
    for nome, f in regras.items():
        fin, rod = [], []
        for cs in sess:
            b, n, _ = sessao(cs, parar=f)
            fin.append(b); rod.append(n)
        vol = sum(rod)
        rows.append([nome, media(fin), sum(b > 100 for b in fin) / N * 100, sum(b < 100 for b in fin) / N * 100,
                     media(rod), (100 * N - sum(fin)) / vol])
    salvar_csv("extra_exposicao.csv", ["regra", "saldo_final_medio", "ganho_%", "perda_%", "rodadas_medias",
                                       "perda_por_credito_apostado"], rows)
    return rows


def extra_sensibilidade(cs):
    esc = [0.5, 0.8, 1.0, 1.1, 1 / 0.84, 1.3, 1.5, 2.0]
    rows = []
    for k in esc:
        t = {s: k * v for s, v in PAG_BASE.items()}
        teo = k * 0.84
        obs = media([premio(c, t) for c in cs])
        rows.append([round(k, 4), teo * 100, (teo - 1), obs * 100, obs - 1])
    salvar_csv("extra_sensibilidade.csv", ["fator_pagamentos", "RTP_teorico_%", "E[X]_teorico",
                                           "RTP_obs_%", "lucro_medio_obs"], rows)
    plt.plot([r[0] for r in rows], [r[1] for r in rows], "k-", label="Teorico")
    plt.scatter([r[0] for r in rows], [r[3] for r in rows], color="#1f6f4a", zorder=3, label="Observado (E1)")
    plt.axhline(100, color="r", ls="--"); plt.xlabel("Fator multiplicador dos pagamentos")
    plt.ylabel("RTP (%)"); plt.legend(); fig("fig_sens.png")
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    mostrar_rodada(random.Random(1))
    cs, P, X, r1 = exp1()
    tab2, repro, dez = exp2(P)
    r3 = exp3()
    r4 = exp4(P)
    r5 = exp5(cs)
    ic = extra_ic(P)
    mm = extra_mesma_media()
    ex = extra_exposicao()
    se = extra_sensibilidade(cs)
    amb = f"Python {sys.version.split()[0]} | {platform.platform()} | gerador: random.Random (Mersenne Twister), randrange(5)"
    open(os.path.join(OUT, "ambiente.txt"), "w").write(amb + "\n")
    json.dump(dict(r1=r1, tab2=tab2, repro=repro, dez=dez, r3=r3, r4=r4, r5=r5, ic=ic, mm=mm, ex=ex, se=se, amb=amb),
              open(os.path.join(OUT, "resultados.json"), "w"), indent=1, default=str)
    print("Concluido. Ambiente:", amb)


if __name__ == "__main__":
    main()
