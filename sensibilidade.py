import numpy as np

print('!! ALGORITMO SIMPLEX FIXO !!')

print('\nEquipe: '
      '\nLeonardo Tozato Sonsin            RA: 591904'
      '\nLucas de Oliveira Baptista        RA: 588180'
      '\nLucas Rinaldi Rodrigues           RA: 591890'
      '\nMatheus Francisco Leite de Sousa  RA: 588458')


def print_matriz():
    global lin, col
    for lin in range(0, 4):
        for col in range(0, 6):
            print("[{:1}] ".format(matriz[lin][col]), end='')  # Orientação e Organização
        print()  # Pula linha


def cria_matriz_inicial():
    global matriz
    matriz = [0] * 4
    for lin in range(0, 4):
        matriz[lin] = [0] * 6
        for col in range(0, 6):
            matriz[lin][col] = 0

    # Identificação das Bases
    for b in range(3):
        globals()[f"B{b}"] = "F{}".format(b)

    # F1
    matriz[0][0] = 2
    matriz[0][1] = 1
    matriz[0][2] = 1
    matriz[0][3] = 0
    matriz[0][4] = 0
    matriz[0][5] = 18

    # F2
    matriz[1][0] = 2
    matriz[1][1] = 3
    matriz[1][2] = 0
    matriz[1][3] = 1
    matriz[1][4] = 0
    matriz[1][5] = 42

    # F3
    matriz[2][0] = 3
    matriz[2][1] = 1
    matriz[2][2] = 0
    matriz[2][3] = 0
    matriz[2][4] = 1
    matriz[2][5] = 24

    # Z
    matriz[3][0] = -3
    matriz[3][1] = -2
    matriz[3][2] = 0
    matriz[3][3] = 0
    matriz[3][4] = 0
    matriz[3][5] = 0


def encontra_menor_valor_linha_Z():
    global menorValorNegativoZ
    menorValorNegativoZ = 0
    for col in range(5):
        if matriz[3][col] < menorValorNegativoZ:
            menorValorNegativoZ = matriz[3][col]


def encontra_coluna_pivo():
    global colunaPivo
    for lin in range(4):
        for col in range(6):
            if matriz[lin][col] == menorValorNegativoZ:
                colunaPivo = col


def encontra_coluna_base():
    global colunaBase
    if colunaPivo == 0:
        colunaBase = 'X1'
    elif colunaPivo == 1:
        colunaBase = 'X2'
    elif colunaPivo == 2:
        colunaBase = 'F1'
    elif colunaPivo == 3:
        colunaBase = 'F2'
    elif colunaPivo == 4:
        colunaBase = 'F3'


def encontra_linha_e_valor_pivo():
    global linhaPivo, pivo
    for i in range(3):
        try:
            globals()[f"r{i}"] = matriz[i][5] / matriz[i][colunaPivo]
            if globals()[f"r{i}"] < 0:
                globals()[f"r{i}"] = 999999
        except ZeroDivisionError:
            globals()[f"r{i}"] = 999999

    if globals()[f"r{0}"] <= globals()[f"r{1}"] and globals()[f"r{0}"] <= globals()[f"r{2}"]:
        linhaPivo = 0
        globals()[f"B{0}"] = colunaBase
    elif globals()[f"r{1}"] <= globals()[f"r{2}"]:
        linhaPivo = 1
        globals()[f"B{1}"] = colunaBase
    else:
        linhaPivo = 2
        globals()[f"B{2}"] = colunaBase
    pivo = matriz[linhaPivo][colunaPivo]


def atualiza_matriz():
    for col in range(6):
        matriz[linhaPivo][col] = matriz[linhaPivo][col] / pivo

    for linha in range(4):
        coeficiente = matriz[linha][colunaPivo]
        for lin in range(6):
            if linhaPivo != linha:
                matriz[linha][lin] = matriz[linha][lin] - (coeficiente * matriz[linhaPivo][lin])
        linha += 1


def valida_z():
    global validaZ
    for col in range(5):
        x = round(matriz[3][col])
        if x < 0:
            validaZ = True
            break
        else:
            validaZ = False

def closestToZero(var1, var2, var3):
    # cria um array com as variáveis
    arr = np.array([var1, var2, var3])

    # calcula a diferença dos itens do array
    difference_array = np.absolute(arr)

    # encontra o index do elemento minimo no array
    index = difference_array.argmin()

    # cria novo array sem o item encontrado anteriormente
    new_arr = np.delete(arr, index)

    # calcula a diferença dos itens do novo array
    difference_array = np.absolute(new_arr)

    # encontra o index do elemento minimo do novo array
    index = difference_array.argmin()

    # retorna os valores encontrados
    return arr[index], new_arr[index]


# MAIN:
cria_matriz_inicial()
validaZ = True
while validaZ:
    encontra_menor_valor_linha_Z()
    encontra_coluna_pivo()
    encontra_coluna_base()
    encontra_linha_e_valor_pivo()
    atualiza_matriz()
    valida_z()

# ANÁLISE DE SENSIBILIDADE

# Criar nova matriz
matrizSensibilidade = [0] * 7
for lin in range(0, 7):
    matrizSensibilidade[lin] = [0] * 5
    for col in range(0, 5):
        matrizSensibilidade[lin][col] = 0

# CALCULA F1
AF1 = round((matriz[0][5] / matriz[0][2]) * -1)
BF1 = round((matriz[1][5] / matriz[1][2]) * -1)
CF1 = round((matriz[2][5] / matriz[2][2]) * -1)
arrF1 = np.array([closestToZero(AF1, BF1, CF1)])

# CALCULA F2
AF2 = round((matriz[0][5] / matriz[0][3]) * -1)
BF2 = round((matriz[1][5] / matriz[1][3]) * -1)
CF2 = round((matriz[2][5] / matriz[2][3]) * -1)
arrF2 = np.array([closestToZero(AF2, BF2, CF2)])

# CALCULA F3
AF3 = 0
BF3 = round((matriz[1][5] / matriz[1][4]) * -1)
CF3 = 0
arrF3 = np.array([closestToZero(AF3, BF3, CF3)])

# INFO
matrizSensibilidade[0][0] = 'VAR'
matrizSensibilidade[0][1] = 'V.F'
matrizSensibilidade[0][2] = 'P.S'
matrizSensibilidade[0][3] = ' + '
matrizSensibilidade[0][4] = ' - '

# X1
matrizSensibilidade[1][0] = 'X1'
matrizSensibilidade[1][1] = round(matriz[1][5])
matrizSensibilidade[1][2] = ' - '
matrizSensibilidade[1][3] = ' - '
matrizSensibilidade[1][4] = ' - '

# X2
matrizSensibilidade[2][0] = 'X2'
matrizSensibilidade[2][1] = round(matriz[0][5])
matrizSensibilidade[2][2] = ' - '
matrizSensibilidade[2][3] = ' - '
matrizSensibilidade[2][4] = ' - '

# F1
matrizSensibilidade[3][0] = 'F1'
matrizSensibilidade[3][1] = 0
matrizSensibilidade[3][2] = matriz[3][2]
matrizSensibilidade[3][3] = arrF1.max()
matrizSensibilidade[3][4] = arrF2.min() * -1

# F2
matrizSensibilidade[4][0] = 'F2'
matrizSensibilidade[4][1] = 0
matrizSensibilidade[4][2] = matriz[3][3]
matrizSensibilidade[4][3] = arrF2.max()
matrizSensibilidade[4][4] = arrF2.min() * -1

# F3
matrizSensibilidade[5][0] = 'F3'
matrizSensibilidade[5][1] = round(matriz[1][5])
matrizSensibilidade[5][2] = 0
matrizSensibilidade[5][3] = arrF3.max()
matrizSensibilidade[5][4] = arrF3.min() * -1

# Z
matrizSensibilidade[6][0] = 'Z'
matrizSensibilidade[6][1] = round(matriz[3][5])
matrizSensibilidade[6][2] = ' - '
matrizSensibilidade[6][3] = ' - '
matrizSensibilidade[6][4] = ' - '

print("\nMatriz Sensibilidade:")
for lin in range(0, 7):
    for col in range(0, 5):
        print("[{:1}]      ".format(matrizSensibilidade[lin][col]), end='')  # Orientação e Organização
    print()  # Pula linha