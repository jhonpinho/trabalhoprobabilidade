"""Validacao automatizada. Executar: python -m unittest testes -v"""
import random, unittest
from simulador import premio, lucro, janela, rodada, centros, PAG_BASE, ROLO

class T(unittest.TestCase):
    def test_pagamentos(self):  # cinco triplas pagam; demais pagam zero
        for s, v in PAG_BASE.items():
            self.assertEqual(premio((s, s, s)), v)
        self.assertEqual(premio(("A", "A", "B")), 0)
        self.assertEqual(premio(("B", "D", "A")), 0)
    def test_lucro_desconta_aposta(self):
        self.assertEqual(lucro(0), -1); self.assertEqual(lucro(50), 49)
    def test_esperanca_exata(self):  # enumera as 125 triplas
        tot = sum(premio((a, b, c)) for a in ROLO for b in ROLO for c in ROLO)
        self.assertEqual(tot, 105); self.assertAlmostEqual(tot / 125, 0.84)
    def test_semente(self):
        a = centros(50, random.Random(2026)); b = centros(50, random.Random(2026))
        self.assertEqual(a, b)
    def test_totais(self):
        n = 1000; X = [lucro(premio(c)) for c in centros(n, random.Random(1))]
        self.assertEqual(len(X), n)
    def test_caso_limite_janela(self):  # K=4 -> E, A, B (Figura 3)
        self.assertEqual(janela(4), ("E", "A", "B"))
