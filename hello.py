# Maria Júlia Testoni
# Nicolas Feltrin Mendes
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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
    
#df = pd.read_excel('teste.xlsx', sheet_name='planilha')
df = pd.read_excel('coadm-05-2024.xlsx', sheet_name='planilha')

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
#print(teste)

siglaSemRepeticao = []
for companhia in siglas:
    if siglas.count(companhia) > 1 and companhia not in siglaSemRepeticao:
        siglaSemRepeticao.append(companhia)
#Adicionar membros que se repetem ao dicionario
membrosInfluentes = {}
for membro in conselheiros:
    if conselheiros.count(membro) > 1:
        membrosInfluentes.update({membro:conselheiros.count(membro)})

indicacoes ={}
conselhos = {}
for membro in membrosInfluentes:
    indicante = list()  # lista de orgãos que fazem indicacoes
    empresas = list()  # lista de empresas que os indicados estão
    distancias = caminhoMinimo(grafo, membro)
    distancias = distancias.items()
    for item, pulos in distancias:
        #print(f'item: {item}, pulos:{pulos}')
        if pulos == 1 and item in siglaSemRepeticao: #1 pulo é a empresa em que está
            empresas.append(item)
        if pulos == 2 and item in orgao: #2 pulos são os órgãos indicantes ligados à empresa
            indicante.append(item)
    conselhos.update({membro: empresas}) #Relação membro:Empresa (conselho)
    indicacoes.update({membro:indicante}) #relação Membro:Órgaos indicantes (que indicaram para os conselhos em que o membro se encontra)

#Tabela de influencias
tabelaInfluencias = {'Membro':list(conselhos.keys()),
                        'Empresa':list(conselhos.values()),
                     'Órgão Indicante':list(indicacoes.values())}
influencias_df = pd.DataFrame.from_dict(tabelaInfluencias)
influencias_fig, inf = plt.subplots(figsize=(85,6))
inf.axis('tight')
inf.axis('off')
influencias_tabela = inf.table(cellText=influencias_df.values,colLabels=influencias_df.columns,loc='center')
influencias_tabela.auto_set_font_size(False)
influencias_tabela.set_fontsize(5)

tabelaMembrosInfluentes = {'Membro':list(membrosInfluentes.keys()),
                            'Qnt Indicações recebidas':list(membrosInfluentes.values())}
membrosInfluentes_df = pd.DataFrame.from_dict(tabelaMembrosInfluentes)

membrosInfluentes_fig, mi =plt.subplots(figsize=(12,4))
mi.axis('tight')
mi.axis('off')
membrosInfluentes_tabela =mi.table(cellText=membrosInfluentes_df.values,colLabels=membrosInfluentes_df.columns,loc='center')


#Adicionar órgãos (vértices) e seus graus
graus = {}
for vertice in orgao:
    if vertice not in graus:
        graus.update({vertice:grafo.degree[vertice]}) #tratados para não repetir
tabelaOrgaos = {'Órgão Indicante':list(graus.keys()),
                'Qnt Indicações feitas':list(graus.values())}
influenciaOrgaos_df = pd.DataFrame.from_dict(tabelaOrgaos)
#Tabelas para os Órgãos
orgao_fig, org =plt.subplots(figsize=(20,6))
org.axis('tight')
org.axis('off')
orgaos_tabela =org.table(cellText=influenciaOrgaos_df.values,colLabels=influenciaOrgaos_df.columns,loc='center')

influencias = {}
for organizacao in graus:
    o = caminhoMinimo(grafo, organizacao) # percorrendo distâncias
    for pessoa in o:
        conexao = []

        influencias.update({organizacao: conexao})

#Gera da saída em PDF
pdf = PdfPages("Tabelas.pdf")
pdf.savefig(membrosInfluentes_fig, bbox_inches='tight') #acrescenta uma tabela
pdf.savefig(orgao_fig, bbox_inches='tight') #acrescenta outra tabela
pdf.savefig(influencias_fig, bbox_inches='tight')
pdf.close()

print(type(grafo.degree['Representante dos Empregados']))
plt.figure(figsize=(20, 10))
nx.draw_networkx(grafo, with_labels=True, node_color=[cores[node] for node in grafo.nodes()], node_size=500, font_size=12)
plt.show()