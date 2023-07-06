from .helpers import *

def eliminarEpsilonTransicoes(afnd):
    epsilon = []

    for chave in afnd.keys():
        if '&' in afnd[chave]:
            epsilon.append(chave)

    def copiarRegras(regras, nRegra):
        if nRegra not in epsilon:
            return

        epsilon.remove(nRegra)

        for regra in regras['&']:
            chaves = afnd[regra].keys()

            if '&' in chaves:
                copiarRegras(afnd[regra], regra)
                regras['&'] = unirListas(regras['&'], afnd[regra]['&'])

            for simbolo in chaves:
                if simbolo != '&':
                    transicoes = afnd[regra][simbolo]
                    for estado in transicoes:
                        if simbolo not in regras.keys():
                            regras[simbolo] = []
                        if estado not in regras[simbolo]:
                            regras[simbolo].append(estado)

        afnd[nRegra] = regras

    epAux = epsilon.copy()

    for ep in epAux:
        copiarRegras(afnd[ep], ep)

    for ep in epAux:
        del afnd[ep]['&']


def determinizar(afnd):
    mpRgs = {}
    visitados = set()

    def determiniza(regra, nReg):
        if nReg in visitados:
            return
        visitados.add(nReg)
        chaves = list(regra.keys())

        for chave in chaves:
            if len(regra[chave]) > 1:
                regra[chave].sort()
                nRg = str(regra[chave])
                if nRg not in mpRgs.keys():
                    nEst = len(mpRgs)
                    mpRgs[nRg] = nEst
                    afnd[nEst] = {}
                    determiniza(unirEstados(afnd, regra[chave]), nEst)
                regra[chave] = [mpRgs[nRg]]

    determiniza(afnd[0], 0)
