import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = DAO.getAllRetailers()
        self._idMap = {}
        for f in self._nodi:
            self._idMap[f.Retailer_code] = f
        self._volume = {}
        self._bestPath = []
        self._pesoMax = 0

    def buildGraph(self, year, country):
        self._grafo.clear()
        for nod in self._nodi:
            if nod.Country == country:
                self._grafo.add_node(nod)
        self.addEdges(year)

    def addEdges(self, year):
        self._grafo.clear_edges()
        for v1 in self._grafo.nodes:
            for v2 in self._grafo.nodes:
                if v1.Retailer_code != v2.Retailer_code:
                    print(v1)
                    if self._grafo.has_edge(v1, v2) is False:
                        peso = DAO.getPesi(v1, v2, year)
                        print(peso)
                        if peso > 0:
                            self._grafo.add_edge(v1, v2, weight=peso)
        self.getVolumeVendita()

    def getRetailers(self):
        retailers = DAO.getAllRetailers()
        stati = set()
        for ret in retailers:
            stati.add(ret.Country)
        return stati

    def getCamminoOttimo(self, t):
        self._bestPath = []
        for x in self._grafo.nodes:
            parziale = [x]
            self._ricorsione(parziale, t)
        return self._bestPath, self._pesoMax

    def _ricorsione(self, parziale, t):
        if len(parziale) == t :
            if self.getPeso(parziale) > self.getPeso(self._bestPath):
                self._pesoMax = self.getPeso(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return
        if len(parziale) == t - 1:
            vicini = self._grafo.neighbors(parziale[-1])
            if parziale[0] in vicini:
                parziale.append(parziale[0])
                if self.getPeso(parziale) > self.getPeso(self._bestPath):
                    self._pesoMax = self.getPeso(parziale)
                    self._bestPath = copy.deepcopy(parziale)
                parziale.pop()
                return
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, t)
                parziale.pop()

    def getPeso(self, parziale):
        peso = 0
        for i in range(len(parziale)-1):
            peso += self._grafo[parziale[i]][parziale[i+1]]['weight']
        return peso


    def getNumEdges(self):
        return len(self._grafo.edges)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getVolumeVendita(self):
        self._volume = {}
        for v0 in self._grafo.nodes:
            vicini = self._grafo.neighbors(v0)
            sommaPesi = 0
            for v in vicini:
                sommaPesi += self._grafo[v][v0]['weight']
            if sommaPesi != 0:
                self._volume[v0.Retailer_code] = sommaPesi
        return self._volume
