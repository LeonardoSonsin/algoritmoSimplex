print('!! ALGORITMO SIMPLEX !!')
print('Aluno: Leonardo Tozato Sonsin')
print('RA: 591904')


def print_matriz():
    for lin in range(linhas + 1):
        for col in range(colunas + 1):
            print("[{:1}] ".format(matriz[lin][col]), end='')  # Orientação e Organização
        print()  # Pula linha


def recebe_variaveis():
    global num_variaveis, num_restricoes, linhas, colunas
    num_variaveis = int(input('\nNúmero de variáveis: '))
    num_restricoes = int(input('Número de restrições: '))
    linhas = num_restricoes
    colunas = num_variaveis + num_restricoes
    print()


def cria_matriz_inicial():
    global matriz
    matriz = [0] * (linhas + 1)
    for lin in range(linhas + 1):
        matriz[lin] = [0] * (colunas + 1)
        for col in range(colunas + 1):
            matriz[lin][col] = 0

    # Preenche folgas
    posicao = colunas - num_variaveis
    for i in range(linhas):
        matriz[i][colunas - posicao] = 1
        posicao -= 1


def preenche_matriz_inicial():
    for i in range(num_variaveis):
        matriz[linhas][i] = - int(input('X{} da Função: '.format(i + 1)))
    print()
    for i in range(num_restricoes):
        for j in range(num_variaveis):
            matriz[i][j] = int(input('X{} da {}ª restrição: '.format(j + 1, i + 1)))
        matriz[i][colunas] = int(input('Resultado da {}ª restrição: '.format(i + 1)))
        print()
    print('Matriz Inicial:')
    print_matriz()


def encontra_menor_valor_linha_Z():
    global menorValorNegativoZ
    menorValorNegativoZ = 0
    for col in range(colunas):
        if matriz[linhas][col] < menorValorNegativoZ:
            menorValorNegativoZ = matriz[linhas][col]


def encontra_coluna_pivo():
    global colunaPivo
    for lin in range(linhas + 1):
        for col in range(colunas + 1):
            if matriz[lin][col] == menorValorNegativoZ:
                colunaPivo = col


def encontra_linha_e_valor_pivo():
    global linhaPivo, pivo
    menor = 99999
    for i in range(linhas):
        try:
            globals()[f"r{i}"] = matriz[i][colunas] / matriz[i][colunaPivo]
            if globals()[f"r{i}"] < 0:
                globals()[f"r{i}"] = menor
        except ZeroDivisionError:
            globals()[f"r{i}"] = menor

        if globals()[f"r{i}"] < menor:
            menor = globals()[f"r{i}"]
            linhaPivo = i
    pivo = matriz[linhaPivo][colunaPivo]


def atualiza_matriz():
    for col in range(colunas + 1):
        matriz[linhaPivo][col] = matriz[linhaPivo][col] / pivo

    for linha in range(linhas + 1):
        coeficiente = matriz[linha][colunaPivo]
        for lin in range(colunas + 1):
            if linhaPivo != linha:
                matriz[linha][lin] = matriz[linha][lin] - (coeficiente * matriz[linhaPivo][lin])
        linha += 1


def valida_z():
    global validaZ
    print('\nAtualiza Matriz:')
    print_matriz()
    print()
    print('X{} = '.format(colunaPivo + 1), matriz[linhaPivo][colunas])

    for col in range(linhas + 1):
        if matriz[linhas][col] < 0:
            validaZ = True
            break
        else:
            validaZ = False


# MAIN:
recebe_variaveis()
cria_matriz_inicial()
preenche_matriz_inicial()
validaZ = True
while validaZ:
    encontra_menor_valor_linha_Z()
    encontra_coluna_pivo()
    encontra_linha_e_valor_pivo()
    atualiza_matriz()
    valida_z()
print('Max Z = ', matriz[linhas][colunas])
