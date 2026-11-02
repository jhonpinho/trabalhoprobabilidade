import json, os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
_d="/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed"
for n,suf in (("DS",""),("DS-B","-Bold"),("DS-I","-Italic"),("DS-BI","-BoldItalic")):
    pdfmetrics.registerFont(TTFont(n,_d+suf+".ttf"))
for b,i,n in ((0,0,"DS"),(1,0,"DS-B"),(0,1,"DS-I"),(1,1,"DS-BI")): addMapping("DS",b,i,n)
pdfmetrics.registerFont(TTFont("DM","/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
d = json.load(open(os.path.join(R, "resultados.json")))
def f(x, n=2): return f"{x:.{n}f}".replace(".", ",")
def pc(x, n=2): return f(100 * x, n) + "%"

B = ParagraphStyle("b", fontName="DS", fontSize=10.5, leading=13.5, alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="DS-B", fontSize=13, leading=16, spaceBefore=9, spaceAfter=5, textColor=colors.HexColor("#1f6f4a"))
H2 = ParagraphStyle("h2", fontName="DS-B", fontSize=11, leading=14, spaceBefore=5, spaceAfter=3)
CAP = ParagraphStyle("cap", fontName="DS", fontSize=9, leading=11, spaceAfter=7, alignment=TA_JUSTIFY)
TT = ParagraphStyle("tt", fontName="DS-B", fontSize=15, leading=18, alignment=1, spaceAfter=3)
ST = ParagraphStyle("st", fontName="DS", fontSize=10, leading=12, alignment=1, spaceAfter=2)
SM = ParagraphStyle("sm", fontName="DS", fontSize=9, leading=11, spaceAfter=3)
P = lambda t, s=B: Paragraph(t, s)
story = []
nfig = [0]
def figura(arq, larg, legenda):
    nfig[0] += 1
    im = Image(os.path.join(R, arq)); r = im.imageHeight / im.imageWidth
    im.drawWidth, im.drawHeight = larg * cm, larg * cm * r
    story.append(KeepTogether([im, P(f"<b>Figura {nfig[0]}.</b> {legenda}", CAP)]))
ntab = [0]
def tabela(dados, larguras, legenda):
    ntab[0] += 1
    HS = ParagraphStyle('hs', fontName='DS-B', fontSize=8.5, leading=10, alignment=1)
    dados = [[Paragraph(str(x), HS) for x in dados[0]]] + dados[1:]
    t = Table(dados, colWidths=[w * cm for w in larguras], repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "DS-B", 9), ("FONT", (0, 1), (-1, -1), "DS", 9),
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black), ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story.append(KeepTogether([P(f"<b>Tabela {ntab[0]}.</b> {legenda}", CAP), t, Spacer(1, 7)]))

r1, r3, r4, r5, ic, mm, ex, se = d["r1"], d["r3"], d["r4"], d["r5"], d["ic"], d["mm"], d["ex"], d["se"]
c = r1["contagens"]

# ---------------- cabeçalho (sem capa)
story += [P("Máquina Estatística: probabilidade, apostas e pensamento crítico", TT),
          P("Probabilidade e Estatística I – Trabalho I – IFES Campus Serra – 2026/2", ST),
          P("Jhon Pinho e Marlon Silva – Bacharelado em Sistemas de Informação – 29 de outubro de 2026", ST), Spacer(1, 8)]

story += [P("1. Contexto e objetivos", H1),
 P("As máquinas de rolos digitais, popularizadas no Brasil como “jogo do tigrinho”, apresentam o resultado de cada rodada por meio de símbolos e animações, mas a animação não informa a chance de prêmio nem o resultado financeiro de apostar repetidamente. Este trabalho constrói uma <b>máquina didática com regras públicas</b> (cinco símbolos, três rolos, aposta de 1 crédito fictício, apenas a linha central paga) para responder à pergunta do enunciado: <i>como ganhos ocasionais podem coexistir com uma perda esperada para o jogador, e o que isso ajuda a compreender sobre as apostas na sociedade?</i> Não se faz engenharia reversa de nenhum produto comercial, e os resultados simulados não medem prevalência de transtornos nem impacto nacional."),
 P("O tema tem relevância de saúde pública. A Organização Mundial da Saúde associa os danos das apostas a sofrimento financeiro, comprometimento de despesas essenciais, problemas de saúde mental e conflitos familiares, inclusive para quem não aposta, e classifica máquinas eletrônicas e jogos de cassino entre os produtos de maior risco [1]. A Comissão da <i>The Lancet Public Health</i> estimou 15,8% (IC 95%: 10,7% a 21,6%) de jogo problemático ou transtorno do jogo entre adultos que usaram cassino ou rolos on-line [2]; o denominador é quem usou o produto, e não a população brasileira. No Brasil, o LENAD III (2025) aplicou o módulo de apostas a uma subamostra de 4.914 pessoas com a escala PGSI [3], que rastreia problemas e não equivale a diagnóstico clínico."),
 P("As fontes sobre a política pública estão datadas de <b>29/10/2026</b> e o cenário muda rápido (ver seção 5)."),

 P("2. Modelo e conceitos", H1),
 P("Cada rolo é a sequência circular R = (A, B, C, D, E). Sorteia-se uma parada K uniforme em {0,…,4} (probabilidade 1/5); a coluna mostra R<sub>K</sub>, R<sub>(K+1) mod 5</sub> e R<sub>(K+2) mod 5</sub>. Os três rolos são sorteados de forma independente em cada rodada, de modo que as três células centrais são independentes e a probabilidade de uma tripla específica é (1/5)³ = 1/125. O espaço amostral central tem 5³ = 125 resultados equiprováveis; as células de uma mesma coluna <i>não</i> são independentes, pois são vizinhas no rolo. O evento “sem prêmio” tem 120 triplas (96%)."),
 P("Seja <i>P</i> o prêmio bruto e <i>X = P − 1</i> o lucro líquido. A distribuição é: A–A–A (P=5, X=4), B–B–B (10, 9), C–C–C (15, 14), D–D–D (25, 24), E–E–E (50, 49), cada uma com probabilidade 1/125, e qualquer outra tripla (P=0, X=−1) com 120/125. A chance de prêmio é 5/125 = 4%. Pela definição de esperança, E[P] = (5+10+15+25+50)/125 = 105/125 = 0,84 e, pela linearidade, <b>E[X] = 0,84 − 1 = −0,16</b>. O <b>RTP</b> é E[P]/aposta = 84%, e a vantagem esperada do operador é 16%. O desvio-padrão teórico do lucro é σ = " + f(5.2052, 3) + " crédito (σ² = E[X²] − E[X]²). Três ideias distintas não devem ser confundidas: <i>chance de prêmio</i> (4%), <i>RTP</i> (84%) e <i>lucro esperado</i> (−0,16 por crédito apostado). A desvantagem é uma propriedade da distribuição, e não de cada rodada: ganhos ocasionais são perfeitamente compatíveis com E[X] < 0."),
 P("<b>Implementação.</b> O código (simulador.py, Python, <font name='DM'>random.Random(semente).randrange(5)</font>) inicia o gerador uma única vez por execução, separa as funções de rodada, pagamento e lucro e tem seis testes automatizados (testes.py). O programa exibe “Simulador acadêmico - somente créditos fictícios”. Ambiente: " + d["amb"] + ". O enunciado indica Python 3.14 para a equipe; o código usa apenas a biblioteca padrão e deve ser reexecutado e conferido nessa versão."),

 P("3. Os cinco experimentos", H1)]

# E1
story += [P("Experimento 1 – As frequências acompanham as probabilidades?", H2),
 P("Procedimento: 10.000 rodadas, semente 2026, sem saldo. A soma das contagens é 10.000 (conferido no código).")]
rows = [["Lucro X", "Prob. teórica", "Contagem", "Freq. relativa"]]
for v, pt in zip(["-1", "4", "9", "14", "24", "49"], [0.96] + [0.008] * 5):
    rows.append([v.replace("-", "−"), pc(pt, 1), str(c[v]), pc(c[v] / 10000)])
tabela(rows, [3, 3.5, 3, 3.5], "Distribuição teórica e observada do lucro (E1, semente 2026, N = 10.000). Fonte: resultados/e1_distribuicao.csv.")
figura("fig_e1.png", 9.5, "Proporções teóricas e observadas do lucro por rodada. Fonte: simulação própria (semente 2026).")
story += [P(f"Lucro médio X̄ = {f(r1['media_X'],4)} crédito; RTP observado = {pc(r1['rtp'])}; proporção de rodadas premiadas = {pc(r1['prop_premio'])}; desvio-padrão amostral s = {f(r1['s'],3)} crédito (divisor N−1); mediana = −1. <b>Interpretação.</b> A perda média por rodada observada (≈{f(-r1['media_X'],3)} crédito) é menor que a teórica (0,16), e o RTP observado está acima de 84%. Isso não exige correção nos dados: o erro padrão da média é s/√N ≈ {f(r1['s']/100,3)}, e a diferença de {f(r1['media_X']+0.16,4)} corresponde a cerca de {f((r1['media_X']+0.16)/(r1['s']/100),2)} erro padrão, compatível com a variação amostral. As frequências ficam próximas, mas não iguais, às probabilidades (por exemplo, 0,77% a 0,88% contra 0,8%). A proporção de prêmios ({pc(r1['prop_premio'])}) responde “com que frequência recebo algo?”, enquanto o RTP responde “quanto volta, em média, por crédito apostado?”; um jogo pode premiar com frequência e ainda assim devolver menos do que recebe. O desvio-padrão (≈5,3 créditos) é muito maior que o módulo da média (0,13 a 0,16), isto é, o resultado de curto prazo é dominado pela dispersão, o que sustenta a percepção de que “dá para ganhar”.")]

# E2
story += [P("Experimento 2 – O que muda quando aumentamos a amostra?", H2),
 P("Três sequências de 10.000 rodadas (sementes 10, 2026 e 123456); a de 2026 é a mesma do E1 (conferido por igualdade das listas).")]
rows = [["Semente", "n = 100", "n = 1.000", "n = 10.000"]] + [[str(int(t[0]))] + [f(x, 4).replace("-", "−") for x in t[1:]] for t in d["tab2"]]
tabela(rows, [3, 3, 3, 3], "Médias acumuladas do lucro (créditos). Referência teórica: −0,16. Fonte: resultados/e2_medias_acumuladas.csv.")
figura("fig_e2.png", 9.5, "Trajetórias da média acumulada do lucro (escala logarítmica em n) e referência E[X] = −0,16. Fonte: simulação própria.")
story += [P(f"Reexecutando a semente 2026 no mesmo ambiente, os dez primeiros resultados foram {'<b>reproduzidos</b>' if d['repro'] else 'diferentes'} ({', '.join(str(x) for x in d['dez'])}). <b>Interpretação.</b> Com n = 100, as médias variam de {f(min(t[1] for t in d['tab2']),1)} a {f(max(t[1] for t in d['tab2']),1)}, e a sequência de 2026 chegou a ficar positiva; com n = 10.000, as três ficam entre −0,22 e −0,10. Isso ilustra a Lei dos Grandes Números: a média tende à esperança, sem ser monotônica e sem garantia de erro máximo em 10.000 rodadas. Um início favorável não altera a distribuição das próximas rodadas, e a sequência não “compensa” perdas: a esperança negativa não vira renda ao aumentar a amostra.")]

# E3
story += [P("Experimento 3 – O que acontece com um saldo limitado?", H2),
 P("100 participantes virtuais, saldo inicial 100, aposta 1, fim em 500 rodadas ou saldo &lt; 1, sem reposição, com B<sub>t+1</sub> = B<sub>t</sub> + X<sub>t+1</sub> e semente 42 iniciada uma vez. Resultados (fonte: e3_participantes.csv):")]
rows = [["Ganho (B<sub>f</sub> &gt; 100)", "Empate", "Perda", "Esgotamento*", "Média", "Mediana", "Máx."],
        [f"{r3['ganho']}%", f"{r3['empate']}%", f"{r3['perda']}%", f"{r3['esgotou']}%", f(r3['media'], 1), f(r3['mediana'], 1), str(r3['max'])]]
rows[0][0] = "Ganho (Bf > 100)"
tabela(rows, [3.2, 2, 2, 2.6, 2, 2, 1.8], f"Resultados finais de 100 participantes virtuais (saldo em créditos; *esgotamento é subconjunto das perdas; ganho + empate + perda = 100%). Duração média das sessões: {f(r3['rod_media'],1)} rodadas.")
figura("fig_e3.png", 9.5, "Trajetórias de saldo dos cinco primeiros participantes (saldo mantido constante após a parada), sem seleção por resultado. Fonte: simulação própria (semente 42).")
story += [P(f"<b>Interpretação.</b> Mesmo com esperança negativa, {r3['ganho']} de 100 participantes terminaram acima de 100 (máximo {r3['max']}) e {r3['empate']} empataram: ganhos individuais são esperados quando a dispersão é grande. Contudo, {r3['perda']}% perderam e {r3['esgotou']}% esgotaram o saldo antes de 500 rodadas. A média final ({f(r3['media'],1)}) é bem maior que a mediana ({f(r3['mediana'],1)}) porque poucos saldos altos puxam a média: o participante “típico” zerou o saldo. Um relato isolado de sucesso omite os demais 75 casos; ele é visível, mas não é representativo. Como as sessões têm duração variável (esgotamento), a referência 100 − 500(0,16) = 20 não se aplica automaticamente. Estas taxas descrevem este modelo, saldo e horizonte, e não a situação de famílias brasileiras.")]

# E4
story += [P("Experimento 4 – Depois de perder, aumenta a chance de ganhar?", H2)]
rows = [["Resultado anterior", "Total de pares", "Prêmios na seguinte", "Proporção"]] + [[l[0].replace("apos", "Após").replace("premio", "prêmio").replace("sem prêmio", "sem prêmio"), str(l[1]), str(l[2]), pc(float(l[3]))] for l in r4]
tabela(rows, [4, 3, 3.5, 3], "Probabilidade condicional empírica de prêmio na rodada seguinte (9.999 pares consecutivos do E1). Referência: 4%. Fonte: resultados/e4_condicional.csv.")
figura("fig_e4.png", 8, "Proporção de rodadas seguintes premiadas, por resultado da rodada anterior. Fonte: simulação própria (E1).")
story += [P(f"<b>Interpretação.</b> As duas proporções ({pc(float(r4[0][3]))} após prêmio e {pc(float(r4[1][3]))} após rodada sem prêmio) são praticamente iguais e próximas de 4%, como prevê Pr(G<sub>i+1</sub> | G<sub>i</sub>) = Pr(G<sub>i+1</sub> | G<sub>i</sub><super>c</super>) = Pr(G<sub>i+1</sub>) = 4%. O grupo “após prêmio” é bem menor (412 pares contra 9.587), então sua proporção é menos precisa. A máquina não “deve” um prêmio depois de perder: crer no contrário é a falácia do jogador, a espera por compensação entre resultados independentes.")]

# E5
story += [P("Experimento 5 – Prêmios maiores tornam o jogo favorável?", H2)]
b, p10 = r5
rows = [["Tabela", "P(prêmio) teór.", "Freq. prêmio obs.", "Prêmio médio obs.", "Lucro médio obs.", "RTP teór.", "RTP obs.", "E[X] teór."],
        ["Base", "4%", pc(b[2]), f(b[3], 4), f(b[4], 4).replace("-", "−"), "84%", pc(b[6]), "−0,16"],
        ["+10%", "4%", pc(p10[2]), f(p10[3], 4), f(p10[4], 4).replace("-", "−"), "92,4%", pc(p10[6]), "−0,076"]]
tabela(rows, [1.5, 2.2, 2.2, 2.2, 2.2, 1.8, 1.9, 1.9], "Duas tabelas de pagamento aplicadas aos mesmos 10.000 resultados do E1. Fonte: resultados/e5_comparacao.csv.")
figura("fig_e5.png", 7.5, "RTP teórico e observado das duas tabelas de pagamento. Fonte: simulação própria (E1).")
story += [P(f"<b>Interpretação.</b> A chance de prêmio permanece 4% nas duas tabelas, já que símbolos e probabilidades são os mesmos. Pela linearidade, E[P] escala por 1,10 e o RTP vai de 84% para 1,10 × 84% = 92,4% (E[X] = −0,076): o jogo melhora para o jogador, mas segue desfavorável. No dado observado, o RTP da tabela +10% foi {pc(p10[6])}, abaixo de 100%, porém acima do teórico (92,4%) pela mesma flutuação amostral do E1. Portanto, <i>pagar mais</i>, <i>pagar com maior frequência</i> e <i>ter lucro esperado positivo</i> são afirmações diferentes. O ponto de equilíbrio exigiria multiplicar os prêmios por 1/0,84 ≈ 1,19 (extra de sensibilidade).")]

# ---------------- extras
story += [P("4. Extras realizados", H1),
 P("<b>4.1 Intervalos de confiança.</b> Com os dados do E1 (normal, n = 10.000): X̄ = " + f(ic['m'],4) + ", IC 95% = [" + f(ic['ic1'][0],4) + "; " + f(ic['ic1'][1],4) + "], que contém −0,16. Com 30 execuções independentes de 10.000 rodadas (sementes 1000–1029; t com 29 g.l. = 2,045): média das médias = " + f(ic['mm'],4) + ", IC 95% = [" + f(ic['ic2'][0],4) + "; " + f(ic['ic2'][1],4) + "], também contendo −0,16, e bem mais estreito, pois cada execução é uma observação independente de uma média de 10.000 rodadas (desvio-padrão entre execuções " + f(ic['ss'],3) + "). Hipóteses: observações independentes e média aproximadamente normal (razoável pelo Teorema Central do Limite com n grande, apesar de a distribuição de X ser muito assimétrica). Um IC mede a incerteza da estimativa a partir do modelo, e não a probabilidade de uma sessão individual ser lucrativa."),
 P("<b>4.2 Mesma média, riscos diferentes.</b> Mantendo RTP = 84%, construímos a tabela “Concentrada” (apenas E–E–E paga 105) e a “Uniforme” (todas as triplas iguais pagam 21), comparadas à Base nas mesmas 100 sessões de 500 rodadas (semente 43). A conferência E[P] = 0,84 vale nas três (assert no código)."),]
rows = [["Tabela", "E[P]", "P(prêmio)", "σ teórico de X", "Saldo médio", "Saldo mediano", "Perdas", "Esgotados", "Saldo máx."]]
for r in mm: rows.append([r[0], f(r[1]), f(r[3], 1) + "%", f(r[4], 2), f(r[5], 1), f(r[6], 1), str(r[7]), str(r[8]), str(r[9])])
tabela(rows, [2.3, 1.3, 1.8, 2.2, 1.8, 1.9, 1.4, 1.8, 1.7], "Mesma esperança, dispersões diferentes (100 sessões, saldo inicial 100, 500 rodadas). Fonte: resultados/extra_mesma_media.csv.")
story += [P("A esperança é idêntica, mas a dispersão não: a tabela Concentrada tem σ ≈ 9,35 contra 5,21 (Base) e 4,12 (Uniforme), paga prêmio em apenas 0,8% das rodadas e produz o maior saldo máximo, ao passo que a Uniforme limita ganhos extremos. Duas máquinas com o mesmo RTP podem “parecer” muito diferentes ao jogador; o RTP sozinho não descreve o risco. As diferenças entre médias dessas 100 sessões também refletem variação amostral."),
 P("<b>4.3 Limites de exposição.</b> Com 1.000 sessões (semente 77) sobre as mesmas sequências, comparamos regras de parada definidas antes da simulação:")]
rows = [["Regra", "Saldo final médio", "Ganho", "Perda", "Rodadas médias", "Perda por crédito apostado"]]
for r in ex: rows.append([r[0].replace("R0: sem limite (500 rod. ou esgotar)", "R0 sem limite"), f(r[1], 1), f(r[2], 1) + "%", f(r[3], 1) + "%", f(r[4], 1), f(r[5], 3)])
rows = [[x.replace("R1: parar com perda de 20 (saldo<=80)", "R1 parar após perder 20").replace("R2: parar com ganho de 20 (saldo>=120)", "R2 parar após ganhar 20").replace("R3: R1 e R2 combinadas", "R3 R1 + R2") for x in row] for row in rows]
tabela(rows, [3.7, 2.5, 1.7, 1.7, 2.5, 3.4], "Regras de parada (saldo inicial 100, máximo 500 rodadas, 1.000 sessões). Fonte: resultados/extra_exposicao.csv.")
story += [P("Parar após ganhar 20 (R2) aumenta muito a proporção de sessões vencedoras (≈59%), mas isso é consequência de truncar as sessões vencedoras cedo: o saldo médio continua abaixo de 100 e a perda por crédito apostado permanece da ordem de 0,13 a 0,17 (a esperança por rodada, 0,16, não muda com a regra). Limites reduzem a <i>exposição</i> (menos rodadas e, portanto, menos crédito em jogo), mas não tornam o jogo favorável. As diferenças de 0,13 a 0,17 devem-se à seleção de sessões e ao tamanho amostral, e não a uma mudança na esperança por rodada."),
 P("<b>4.4 Análise de sensibilidade.</b> Multiplicamos os pagamentos por oito fatores (0,5 a 2,0), inclusive o fator de equilíbrio 1/0,84 ≈ 1,19 (RTP = 100%).")]
rows = [["Fator", "RTP teórico", "E[X] teórico", "RTP obs. (E1)", "Lucro médio obs."]]
for r in se: rows.append([f(r[0], 3), f(r[1], 1) + "%", f(r[2], 3).replace("-", "−"), f(r[3], 1) + "%", f(r[4], 3).replace("-", "−")])
tabela(rows, [2.2, 3, 3, 3.2, 3.2], "Sensibilidade do RTP ao fator de pagamentos, com probabilidades fixas. Fonte: resultados/extra_sensibilidade.csv.")
story += [P("O RTP é linear no fator de pagamentos: RTP = 84% × fator. Só acima de ≈1,19 o jogo seria favorável ao jogador, o que um operador não adotaria. Note que com fator 1,19 o RTP observado em E1 foi 103%, embora o teórico seja 100%: mesmo no ponto de equilíbrio, uma amostra pode parecer favorável. Esse é o mecanismo da percepção de “estar ganhando” em sessões curtas."),
 P("<b>4.5 Validação automatizada.</b> testes.py contém seis verificações (pagamentos, lucro descontando a aposta, enumeração exata das 125 triplas com soma 105, reprodução por semente, totais e caso-limite da janela K = 4), executadas com <font name='DM'>python -m unittest testes -v</font>; todas passaram.")]

# ---------------- discussão
story += [P("5. Discussão crítica e conclusão", H1),
 P("<b>Mecanismo e percepção.</b> A conta E[X] = 0,84 − 1 = −0,16 coexiste com resultados favoráveis visíveis: no E1, 4,12% das rodadas pagaram prêmio; no E3, 23 de 100 participantes terminaram acima de 100 créditos, e um chegou a 390. Os vencedores são fáceis de ver e divulgar; os 75 que perderam e os 67 que zeraram o saldo são menos visíveis. A dispersão (s ≈ 5,3 contra |E[X]| = 0,16) faz com que curtos períodos sejam dominados pelo acaso, e só o longo prazo aproxima a média da esperança (E2). Por isso, “aleatoriedade” não implica “igualdade”: os sorteios são independentes e honestos, e ainda assim o prêmio médio é inferior à aposta."),
 P("<b>Renda e saúde.</b> A simulação mostra apenas o que o modelo faz: perda média de 0,16 crédito por crédito apostado e esgotamento frequente de um saldo fixo. Os danos reais a famílias vêm de estudos sobre pessoas: a OMS aponta sofrimento financeiro e problemas de saúde mental [1]; Baker et al. encontraram, nos EUA, redução de poupança e maior pressão sobre o crédito entre famílias com restrições financeiras após a expansão das apostas esportivas [4], com a ressalva de que modalidade e país diferem. No Brasil, o Banco Central estimou R$ 18–21 bilhões mensais em transferências brutas via Pix em 2024, valor que não é perda líquida [11]; o TCU cita receita bruta de jogos de R$ 17,4 bilhões no 1º semestre de 2025 (apostado menos prêmios) [12]; e o IEPS estimou custos sociais de R$ 38,8 bilhões anuais (R$ 30,6 bilhões associados à saúde), com componentes estimados e limites metodológicos nas páginas 33–35 [13]. São medidas de natureza distinta, e por isso não foram somadas. Uma rodada perdida não é diagnóstico, e os 15,8% da Lancet [2] se referem a usuários de cassino/rolos, não à população."),
 P("<b>Políticas e interesses: nossa posição é favorável à restrição.</b> O fato central do modelo é que o produto tem desvantagem esperada para o jogador e é desenhado para ser percebido de outro modo: velocidade, visualização e relatos de ganho distorcem a avaliação de risco. Newall et al. mostram que a forma de expressar a mesma informação (retorno ao jogador ou vantagem da casa) altera a compreensão e a percepção [5]; isto indica que a informação por si só, ao menos como hoje apresentada, é insuficiente, e sustenta limitar publicidade e oferta, e não apenas exigir avisos. A Comissão da Lancet associa disponibilidade contínua, velocidade e promoção comercial à maior exposição [2]. A MP 1.394/2026, de 25/09/2026, proíbe exploração, oferta, intermediação e publicidade de apostas de quota fixa [7, 8], e o governo cobra judicialmente despesas do SUS de 17 plataformas [9]. Em 6/10, a AGU defendeu a MP no STF e sugeriu audiência pública [14]."),
 P("<b>Argumentos contrários, que levamos a sério.</b> ANJL e IBJR pedem a suspensão da MP no STF, alegando insegurança jurídica, ausência de urgência e prejuízo a investimentos [10]; segundo a petição, o Ministério da Fazenda respondeu em 24/09 que não havia estudos específicos sobre os impactos da proibição [15]. Clubes e a Abert alegam efeitos sobre o financiamento do futebol e da mídia [16]. Há ainda o risco de migração para sites clandestinos, que não é trivial: o TCU já havia identificado, em maio de 2026, falhas de coordenação e limites no monitoramento de operadores ilegais [12]. Estas são alegações de partes, e não decisões judiciais. Até as fontes consultadas em 27–29/10/2026, noticiou-se que nenhuma das ações das empresas tinha liminar em vigor na Justiça Federal e que o ministro Fux sinalizara decidir após o 2º turno [17, 16]; é necessário verificar atualizações."),
 P("<b>Força das evidências.</b> O mecanismo (esperança negativa) é matemático e robusto; os danos à saúde e às finanças têm apoio em fontes institucionais e de pesquisa, mas as estimativas monetárias do IEPS e as da Lancet têm limites de transferência (denominador, método, contexto) e associação não é causalidade. Já a eficácia da <i>proibição total</i> versus regulação mais rígida é menos sustentada: depende de fiscalização, de que o mercado clandestino não absorva a demanda e de transição jurídica adequada. Portanto, defendemos restrição como proteção de pessoas vulneráveis, mas reconhecemos que a escolha do instrumento (proibição, limite de publicidade, de depósito, de tempo, ou melhor fiscalização) exige avaliação de impacto, e o próprio debate no STF pede essa evidência."),
 P("<b>Responsabilidade profissional.</b> Como futuros profissionais de sistemas de informação, escolhas de interface (animações, quase-acertos, ausência do RTP ou da vantagem da casa) e de divulgação podem moldar a compreensão do usuário. Uma interface honesta mostraria a distribuição e a esperança, e o simulador deste trabalho o faz. Uma conclusão educativa, sem promessa de ganho e sem culpabilizar pessoas afetadas: <b>resultados aleatórios podem premiar alguns, mas, em média, o jogador perde; entender a distribuição ajuda a avaliar relatos, promessas e políticas.</b>"),
 P("<b>Limites do estudo.</b> O modelo é didático (RTP de 84% não representa produto comercial); as sementes foram fixadas previamente e nenhum dado foi descartado; os resultados do E1 divergem um pouco da teoria, o que foi mantido e explicado; os resultados de saúde e política dependem de fontes externas.")]

# ---------------- referências e transparência (fora da contagem)
story += [PageBreak(), P("Referências e transparência", H1),
 P("<b>Uso de IA.</b> Utilizamos o assistente Claude (Anthropic) para estruturar o simulador, gerar os experimentos, as tabelas, os gráficos e o rascunho deste relatório, e para buscar notícias recentes. A dupla deve conferir: as contas teóricas (E[X] = −0,16, RTP 84% e 92,4%), a execução do código em Python 3.14 e a coerência entre relatório e arquivos, assim como as fontes citadas. Ambos os integrantes devem compreender e subscrever o conteúdo.", SM)]
refs = ["WORLD HEALTH ORGANIZATION. Gambling. 2 dez. 2024.",
 "WARDLE, H. et al. The Lancet Public Health Commission on gambling. The Lancet Public Health, v. 9, p. e950–e994, 2024. DOI: 10.1016/S2468-2667(24)00167-1.",
 "UNIFESP; UNIAD. Caderno Temático LENAD III: jogos de aposta na população brasileira. 2025.",
 "BAKER, S. R. et al. Gambling Away Stability: Sports Betting’s Impact on Vulnerable Households. NBER Working Paper 33108, 2024.",
 "NEWALL, P. W. S.; WALASEK, L.; LUDVIG, E. A. Equivalent gambling warning labels are perceived differently. Addiction, v. 115, n. 9, p. 1762–1767, 2020.",
 "BRASIL. Lei 14.790, de 29 de dezembro de 2023.",
 "BRASIL. Congresso Nacional. Medida Provisória 1.394/2026. Publicada em 25 set. 2026.",
 "BRASIL. Ministério da Saúde. Presidente Lula assina Medida Provisória que proíbe as bets no Brasil. 25 set. 2026.",
 "RICHTER, A. Agência Brasil. Governo cobra na Justiça gastos do SUS com tratamento de apostadores. 28 set. 2026.",
 "PONTES, F. Agência Brasil. Associações de jogos acionam STF contra MP que proibiu apostas online. 28 set. 2026.",
 "BANCO CENTRAL DO BRASIL. Estudo Especial 119/2024; Nota Técnica 513/2024. Set. 2024.",
 "TRIBUNAL DE CONTAS DA UNIÃO. Tribunal analisa enfrentamento a casas de apostas ilegais. 19 maio 2026 (Acórdão 1296/2026).",
 "ROSA, D. et al. IEPS; FPSM; Umane. A saúde dos brasileiros em jogo. Dez. 2025, p. 33–35.",

 "CONGRESSO EM FOCO. AGU pede que STF mantenha proibição de bets determinada por Lula. 6 out. 2026 (notícia).",
 "O ESTADO DE S. PAULO (via DGABC). Bets recorrem ao STF contra MP de Lula que proibiu apostas no País. 28 set. 2026 (notícia; alegações das entidades).",
 "PODER360. Passado o 2º turno, Fux deve decidir se MP das Bets vale ou não. Out. 2026 (notícia).",
 "BNL DATA. Nenhuma das 19 ações das bets contra a MP tem liminar em vigor na Justiça Federal. 27 out. 2026 (notícia)."]
for i, t in enumerate(refs, 1):
    if t: story.append(P(f"[{i}] {t}", SM))
story.append(P("Gêneros: [1,2,3,4,5,13] pesquisa/relatório institucional; [6,7] norma; [8,11,12] comunicação/documento oficial; [9,10,14-17] notícias (registram alegações de partes). Data de consulta das notícias: 29/10/2026; o cenário pode ter mudado.", SM))

def rodape(cv, doc):
    cv.setFont("DS", 8.5); cv.drawCentredString(A4[0] / 2, 1.2 * cm, f"Jhon Pinho e Marlon Silva – Trabalho I – página {doc.page}")
doc = SimpleDocTemplate("/mnt/user-data/outputs/Relatorio_Trabalho1_Probabilidade.pdf", pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                        topMargin=2 * cm, bottomMargin=2 * cm, title="Máquina Estatística", author="Jhon Pinho; Marlon Silva")
doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
