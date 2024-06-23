import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_excel('coadm-05-2024.xlsx', sheet_name='planilha')

sigla = df['Sigla']

grafo = nx.Graph()
grafo.add_node("A")
grafo.add_node("B")
grafo.add_node("C")

grafo.add_edge("A", "B")
grafo.add_edge("A", "B")
grafo.add_edge("C", "C")
grafo.add_edge("A", "C")

nx.draw(grafo, with_labels=True)
plt.show()
