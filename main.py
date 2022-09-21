print('!! ALGORITMO SIMPLEX !!')
print('Aluno: Leonardo Tozato Sonsin')
print('RA: 591904')


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

    # F1
    matriz[0][0] = 1
    matriz[0][1] = 0
    matriz[0][2] = 1
    matriz[0][3] = 0
    matriz[0][4] = 0
    matriz[0][5] = 6

    # F2
    matriz[1][0] = 0
    matriz[1][1] = 2
    matriz[1][2] = 0
    matriz[1][3] = 1
    matriz[1][4] = 0
    matriz[1][5] = 12

    # F3
    matriz[2][0] = 3
    matriz[2][1] = 2
    matriz[2][2] = 0
    matriz[2][3] = 0
    matriz[2][4] = 1
    matriz[2][5] = 18

    # Z
    matriz[3][0] = -5
    matriz[3][1] = -6
    matriz[3][2] = 0
    matriz[3][3] = 0
    matriz[3][4] = 0
    matriz[3][5] = 0

    print("\nMatriz Inicial:")
    print_matriz()


def encontra_menor_valor_linha_Z():
    global menorValorNegativoZ
    menorValorNegativoZ = 0
    for col in range(4):
        if matriz[3][col] < menorValorNegativoZ:
            menorValorNegativoZ = matriz[3][col]


def encontra_coluna_pivo():
    global colunaPivo
    for lin in range(4):
        for col in range(6):
            if matriz[lin][col] == menorValorNegativoZ:
                colunaPivo = col


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
    elif globals()[f"r{1}"] <= globals()[f"r{2}"]:
        linhaPivo = 1
    else:
        linhaPivo = 2

    pivo = matriz[linhaPivo][colunaPivo]
    print("Pivo = ", pivo)


def atualiza_matriz():
    for col in range(6):
        matriz[linhaPivo][col] = matriz[linhaPivo][col] / pivo

    for linha in range(4):
        coeficiente = matriz[linha][colunaPivo]
        for lin in range(6):
            if linhaPivo != linha:
                matriz[linha][lin] = matriz[linha][lin] - (coeficiente * matriz[linhaPivo][lin])
        linha += 1
        print()
        print('Atualiza Matriz:')
        print_matriz()


def valida_z():
    global validaZ
    for col in range(4):
        if matriz[3][col] < 0:
            validaZ = True
            break
        else:
            validaZ = False


def mostra_resultado():
    print('\nResposta Final:')
    print('Max Z = ', matriz[3][5])
    print('X1 = ', matriz[2][5])
    print('X2 = ', matriz[1][5])


# MAIN:
cria_matriz_inicial()
validaZ = True
while validaZ:
    encontra_menor_valor_linha_Z()
    encontra_coluna_pivo()
    encontra_linha_e_valor_pivo()
    atualiza_matriz()
    valida_z()
mostra_resultado()
