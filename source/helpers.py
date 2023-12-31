def unirEstados(automato, estados):
    final = {}  # Dicionário para armazenar as transições do estado resultante
    def unir(estado):
        # Função interna para unir as transições de um estado no estado resultante
        for e in estado:
            if e in final:
                final[e] = unirListas(final[e], estado[e])  # Combina as transições se já existirem
            else:
                final.update({e: estado[e]})  # Adiciona as transições se não existirem

    for estado in estados:  # Percorre os estados que devem ser unidos
        unir(automato[estado])  # Chama a função de unir para cada estado
    return final  # Retorna o estado resultante unido


def unirListas(l1, l2):
    return l1 + list(set(l2) - set(l1))


def  unirAutomatos(afd, afndTemp):
    mapaNovosEstados = {x: x + len(afd) for x in range(len(afndTemp))} # cria um dicionário, com as novas posições na afnd principal das regras do afnd
    aux = []

    if '&' in afd[0].keys():     # É criado uma nova regra S' que leva a regra S por epsilon transição
        afd[0]['&'].append(mapaNovosEstados[0])
    else:
        afd[0].update({'&': [mapaNovosEstados[0]]})
    
    for chave in afndTemp.keys(): #percorre os estados do afnd temporario
        for ch in afndTemp[chave].keys(): #percorre os simbolos/transições dos estados
            if ch == '*': # se for terminal, continua o loop
                continue
            aux = [] #lista auxiliar com os novos estados da afnd temporario
            for i in afndTemp[chave][ch]: # percorre os estados atingiveis pelo simbolo
                aux.append(mapaNovosEstados[i]) 
            afndTemp[chave][ch] = aux #atualiza os estados atingiveis da afnd temporaria, para os novos estados que serão criados na afnd principal
    
    for chave in afndTemp.keys():
        afd.update({mapaNovosEstados[chave] : afndTemp[chave]}) #cria os novos estados na afnd principal

def exibirAutomatoDeterministico(afnd, alfabeto):
    alfabeto.sort()  # Ordena o alfabeto em ordem alfabética
    # Imprime a linha superior da tabela
    print("  ",'     {}'.format('-----' * len(alfabeto)))
    # Imprime os símbolos do alfabeto na primeira linha da tabela
    print("  ",'     |', end='')
    for i in alfabeto:
        print('  {:2}|'.format(i), end='')
    print("  ",'\n     {}'.format('-----' * len(alfabeto)))
    # Percorre os estados do autômato
    for i in afnd.keys():
        if '*' in afnd[i].keys():
            print('*', end='')
        else:
            print(' ', end='')
        if i == 0:  # Modificação: Verifica se o estado é o estado inicial e imprime 'S'
            print(" ",'S   :|', end='')
        else:
            print('{:^6}:|'.format(chr(64 + i)), end='')  # Imprime as regras em ordem alfabética
        for j in alfabeto:
            if j in afnd[i].keys():
                print(' {:2} |'.format(chr(64 + afnd[i][j][0])), end='')
            else:
                print(' {:2} |'.format('-'), end='')
        print('')
    print("  ",'     {}'.format('-----' * len(alfabeto)))
