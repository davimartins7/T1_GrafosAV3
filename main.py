"""
Kattis - Treehouses
Link: https://open.kattis.com/problems/treehouses

=== MODELAGEM DO GRAFO ===

Objetivo: conectar TODOS os treehouses (e o espaço aberto) com o menor
comprimento total de cabo novo.

Vértices: os n treehouses (índices 0..n-1).

Arestas e pesos:
  - Os primeiros e treehouses são acessíveis a pé → pré-conectados diretamente
    no DSU antes do Kruskal (custo zero, sem gerar arestas explícitas).
  - Cabos já existentes entre a e b → também pré-conectados no DSU (custo zero).
  - Todo par (i, j) de treehouses → aresta com peso = distância euclidiana
    (cabo novo candidato).

A ideia central: pré-conexões gratuitas são registradas diretamente no DSU
antes do Kruskal rodar. Assim, o algoritmo só precisa decidir quais cabos novos
adicionar para unir os componentes ainda desconexos — minimizando o comprimento total.

=== POR QUE O KRUSKAL FUNCIONA ===

O Kruskal adiciona gulodosamente a aresta mais barata que conecta dois
componentes ainda desconexos. Isso é correto porque:
  1. Queremos o menor comprimento total de cabo novo → minimizar a soma dos pesos.
  2. Precisamos que todos os n treehouses estejam num único componente conectado.
  3. Pré-conexões gratuitas (primeiros e treehouses + cabos existentes) são
     registradas no DSU antes do algoritmo principal, equivalendo a arestas de
     custo zero já incorporadas.

O DSU com compressão de caminho + união por rank verifica conectividade em
O(α(n)) ≈ O(1) amortizado, fazendo o Kruskal rodar em O(E log E) dominado pela
ordenação das arestas.

=== TRATAMENTO DOS TREEHOUSES PRÉ-CONECTADOS ===

Em vez de criar um nó virtual com arestas de peso 0, as pré-conexões são
registradas diretamente no DSU com chamadas a union() antes do Kruskal:

  1. Os primeiros e treehouses formam um único componente inicial:
       for i in range(e - 1): dsu.union(i, i + 1)

  2. Cada cabo existente (a, b) une os componentes de a e b:
       dsu.union(a - 1, b - 1)

Quando o Kruskal itera sobre as arestas ordenadas, qualquer par já no mesmo
componente tem union() retornando False — a aresta é descartada sem custo.

=== COMPLEXIDADE DE TEMPO ===

Seja n o número de treehouses e p o número de cabos existentes.
  - Pré-conexões no DSU:              O(e + p) · O(α(n)) ≈ O(n)
  - Geração das arestas candidatas:   O(n²)
  - Ordenação das arestas:            O(n² log n)   ← dominante
  - Kruskal com DSU:                  O(n² · α(n)) ≈ O(n²)
  Total:                              O(n² log n)

Com n ≤ 1000, temos ~500 000 arestas → execução em milissegundos.

=== CASOS ESPECIAIS ===

  - n = 1: somente um treehouse, e ≥ 1 → já está no seu próprio componente,
           nenhuma aresta é gerada, resposta = 0.
  - e = n: todos os treehouses são pré-conectados no DSU → todos num único
           componente antes do Kruskal; nenhuma aresta será aceita, resposta = 0
           (se p = 0 e n = e).
  - p > 0: cabos existentes reduzem o número de componentes antes do Kruskal,
           diminuindo o cabo novo necessário.
  - Grafo sempre conexo: como geramos todas as arestas possíveis entre treehouses
    (grafo completo), o Kruskal sempre consegue conectar todos os componentes.
"""

import sys
import math

input = sys.stdin.readline


# ─────────────────────────────────────────────
# Union-Find / DSU
# Compressão de caminho (recursiva) + união por rank
# ─────────────────────────────────────────────

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        # Compressão de caminho: faz cada nó apontar diretamente para a raiz
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)

        if rx == ry:
            return False  # já estão no mesmo componente — aresta descartada

        # União por rank: árvore menor fica abaixo da maior
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# ─────────────────────────────────────────────
# Função principal
# ─────────────────────────────────────────────

def solve():
    n, e, p = map(int, input().split())

    # Lê as coordenadas dos treehouses (0-indexado internamente)
    coords = []

    for _ in range(n):
        x, y = map(float, input().split())
        coords.append((x, y))

    dsu = DSU(n)

    # Pré-conexão 1: os primeiros e treehouses são acessíveis a pé
    # → une-os em cadeia num único componente inicial (custo zero)
    for i in range(e - 1):
        dsu.union(i, i + 1)

    # Pré-conexão 2: cabos já existentes entre pares de treehouses (custo zero)
    for _ in range(p):
        a, b = map(int, input().split())
        dsu.union(a - 1, b - 1)  # converte para índice 0-based

    # Gera todas as arestas candidatas: pares (i, j) com peso = distância euclidiana
    edges = []

    for i in range(n):
        xi, yi = coords[i]

        for j in range(i + 1, n):
            xj, yj = coords[j]

            dist = math.hypot(xi - xj, yi - yj)

            edges.append((dist, i, j))

    # Kruskal: processa arestas em ordem crescente de peso
    edges.sort()

    total = 0.0

    for cost, u, v in edges:
        if dsu.union(u, v):  # une apenas se estiverem em componentes distintos
            total += cost

    print(f"{total:.6f}")


solve()
