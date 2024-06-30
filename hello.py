import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys

def caminhoMinimo(grafo, origem):
    # Inicialização das distâncias com infinito, exceto a origem que é zero
    distancias = {v: sys.maxsize for v in grafo}
    distancias[origem] = 0

    # Conjunto de vértices visitados
    visitados = set()

    while visitados != set(distancias):
        # Encontra o vértice não visitado com menor distância atual
        vertice_atual = None
        menor_distancia = sys.maxsize
        for v in grafo:
            if v not in visitados and distancias[v] < menor_distancia:
                vertice_atual = v
                menor_distancia = distancias[v]

        # Marca o vértice atual como visitado
        visitados.add(vertice_atual)

        # Atualiza as distâncias dos vértices vizinhos
        for vizinho, peso in grafo[vertice_atual].items():
            if distancias[vertice_atual] + peso['weight'] < distancias[vizinho]:
                distancias[vizinho] = distancias[vertice_atual] + peso['weight']

    # Retorna as distâncias mais curtas a partir da origem
    return distancias
    
df = pd.read_excel('teste.xlsx', sheet_name='planilha')

siglas = df['Sigla'].tolist()
conselheiros = df['Conselheiro(a)'].tolist()
orgao = df['Órgão Indicante'].tolist()

grafo = nx.Graph()

# Criando um dicionário para mapear cada valor único para uma cor
cores = {}
cores.update({node: 'blue' for node in siglas})
cores.update({node: 'red' for node in conselheiros})
cores.update({node: 'green' for node in orgao})

arestasCE = list(zip(conselheiros, siglas))
arestasOE = list(zip(orgao, siglas))

grafo.add_edges_from(arestasCE, weight=1)
grafo.add_edges_from(arestasOE, weight=1)

teste = caminhoMinimo(grafo, 'Márcio Antônio Chiumento')
print(teste)

plt.figure(figsize=(10, 8))
nx.draw_networkx(grafo, with_labels=True, node_color=[cores[node] for node in grafo.nodes()], node_size=500, font_size=12)
plt.show()
