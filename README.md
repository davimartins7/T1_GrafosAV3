# Treehouses — Problema de AGM no Kattis

**Link:** https://open.kattis.com/problems/treehouses  
**Grupo:** C  
**Disciplina:** Resolução de Problemas com Grafos  
**Orientador:** Prof. Me. Ricardo Carubbi

---

## Integrantes

| Nome | Matrícula |
|------|-----------|
| *(Integrante 1)* | *(xxxxxxxx)* |
| *(Integrante 2)* | *(xxxxxxxx)* |
| *(Integrante 3)* | *(xxxxxxxx)* |

---

## Linguagem

Python 3

---

## Como executar

### Pré-requisitos

- Python 3.8 ou superior (sem dependências externas)

### Execução com arquivo de entrada

```bash
python3 src/main.py < dados/entradas_do_problema.txt
```

### Execução com entrada digitada manualmente

```bash
python3 src/main.py
```

Cole a entrada e pressione `Ctrl+D` (Linux/Mac) ou `Ctrl+Z` + Enter (Windows).

### Exemplos rápidos no terminal

```bash
# Exemplo 1 → saída esperada: 4.236067
printf "3 1 0\n0.0 0.0\n2.0 0.0\n1.0 2.0\n" | python3 src/main.py

# Exemplo 2 → saída esperada: 2.000000
printf "3 1 1\n0.0 0.0\n0.5 2.0\n2.5 2.0\n1 2\n" | python3 src/main.py

# Exemplo 3 → saída esperada: 2.236067
printf "3 2 0\n0.0 0.0\n2.0 0.0\n1.0 2.0\n" | python3 src/main.py
```

---

## Modelagem do problema como grafo ponderado

### Vértices

Os **n treehouses**, numerados de 0 a n−1 internamente (1 a n na entrada).

Não há nó virtual. O espaço aberto é representado implicitamente pelo conjunto
dos primeiros `e` treehouses, que são pré-conectados diretamente no DSU antes
do Kruskal ser executado.

### Arestas e pesos

| Tipo | Representação | Peso |
|------|---------------|------|
| Caminhada entre os primeiros `e` treehouses | Pré-conexão no DSU via `union(i, i+1)` | gratuito |
| Cabo já existente entre `a` e `b` | Pré-conexão no DSU via `union(a-1, b-1)` | gratuito |
| Cabo novo possível entre `i` e `j` | Aresta explícita na lista do Kruskal | distância euclidiana |

### Estratégia de modelagem

As conexões gratuitas (caminhada + cabos existentes) são registradas diretamente
no DSU **antes** do Kruskal rodar, em vez de serem representadas como arestas de peso zero.
Isso reduz o número de arestas processadas e torna a implementação mais direta:

```
Passo 1 — pré-conectar os primeiros e treehouses em cadeia:
    for i in range(e - 1): dsu.union(i, i + 1)

Passo 2 — pré-conectar cabos existentes:
    for cada (a, b): dsu.union(a - 1, b - 1)

Passo 3 — gerar arestas candidatas e rodar Kruskal:
    para todo par (i, j): aresta com peso = dist(i, j)
```

O resultado do Kruskal é a soma dos cabos novos necessários para unir os
componentes ainda desconexos após as pré-conexões.

### Por que é uma AGM?

Após as pré-conexões, o problema se reduz a: **conectar os componentes restantes
com o menor comprimento total de cabo novo** — que é exatamente a definição de
Árvore Geradora Mínima aplicada ao grafo de componentes.

---

## Algoritmo utilizado

**Kruskal** com **Union-Find / DSU** (Conjunto Disjunto).

### Passos do algoritmo

1. Ler coordenadas e inicializar o DSU com `n` vértices.
2. Pré-conectar os primeiros `e` treehouses em cadeia no DSU.
3. Pré-conectar os `p` cabos existentes no DSU.
4. Gerar todas as O(n²) arestas candidatas (pares de treehouses + distância euclidiana).
5. Ordenar as arestas por peso crescente.
6. Iterar: se `u` e `v` estão em componentes diferentes → une e soma o custo.
7. Imprimir o total.

### Por que Kruskal e não Prim?

O grafo é **denso** (O(n²) arestas) e as arestas são todas geradas explicitamente.
O Kruskal com ordenação é mais natural nesse cenário, especialmente porque as
pré-conexões são incorporadas diretamente no DSU — sem necessidade de nó virtual
ou arestas artificiais de peso zero na lista.

---

## Papel do Union-Find / DSU

O DSU é usado em duas etapas distintas:

**Antes do Kruskal — pré-conexões gratuitas:**
- `union(i, i+1)` para i em `[0, e-1)`: une os primeiros `e` treehouses num único componente.
- `union(a-1, b-1)` para cada cabo existente: une os componentes de `a` e `b`.

**Durante o Kruskal — controle de ciclos:**
- `find(x)`: retorna o representante do componente de `x`.
  Usa **compressão de caminho recursiva**: cada nó visitado passa a apontar
  diretamente para a raiz, garantindo O(α(n)) amortizado nas próximas consultas.
- `union(x, y)`: une os componentes de `x` e `y`.
  Usa **união por rank**: a raiz com rank menor é anexada abaixo da raiz com rank maior,
  evitando que a árvore interna do DSU degenere em lista encadeada.
- Se `find(u) == find(v)`: `u` e `v` já estão conectados → aresta descartada (formaria ciclo).

Complexidade por operação: **O(α(n)) ≈ O(1)** amortizado (α = inversa de Ackermann).

---

## Variação de AGM utilizada

**AGM com componentes pré-conectados.**

Os primeiros `e` treehouses e os pares com cabos existentes formam componentes
iniciais no DSU antes do Kruskal. O algoritmo então trata esses componentes como
"super-vértices" e determina quais cabos novos são necessários para uni-los todos,
minimizando o comprimento total adicionado.

---

## Análise de complexidade

| Etapa | Complexidade |
|-------|-------------|
| Pré-conexões no DSU | O((e + p) · α(n)) ≈ O(n) |
| Leitura das coordenadas | O(n) |
| Geração das arestas candidatas | O(n²) |
| Ordenação das arestas | **O(n² log n)** ← dominante |
| Kruskal com DSU | O(n² · α(n)) ≈ O(n²) |
| **Total** | **O(n² log n)** |

**Memória dominante:** lista de arestas com O(n²) entradas ≈ 500 000 entradas para n=1000.

---

## Casos especiais relevantes

| Caso | Comportamento |
|------|---------------|
| `n = 1` | Nenhuma aresta gerada, resposta = 0. |
| `e = n` | Todos os treehouses pré-conectados em cadeia → um único componente antes do Kruskal. Se `p = 0`, resposta = 0. |
| `p > 0` | Cabos existentes reduzem o número de componentes antes do Kruskal, diminuindo o cabo novo necessário. |
| Todos já conectados | Todas as chamadas `union()` do Kruskal retornam `False`; `total` permanece 0. |
| Grafo sempre conexo | O grafo completo de treehouses garante que a AGM sempre existe. |

---

## Evidência de Accepted

![Accepted](evidencias/accepted.png)

---

## Estrutura do repositório

```
T1/
├── README.md
├── src/
│   └── main.py                   ← solução completa com comentários em português
├── evidencias/
│   └── accepted.png              ← captura de tela do resultado Accepted no Kattis
├── apresentacao/
│   └── apresentacao.pdf          ← slides da apresentação
└── dados/
    └── entradas_do_problema.txt  ← exemplos de entrada para testes locais
```
