import openpyxl
import pygame
import time
import random
import sys
import heapq
import time as time_lib  # Para medir o tempo de execução

# Função para ler o arquivo .xlsx e transformar em matriz
def ler_mapa_xlsx(arquivo_xlsx):
    wb = openpyxl.load_workbook(arquivo_xlsx)
    sheet = wb.active
    mapa = []
    for row in sheet.iter_rows(values_only=True):
        mapa.append(list(row))
    return mapa

# Função para desenhar o mapa na tela com bordas
def desenhar_mapa(screen, mapa, tamanho_bloco):
    cores = {
        1: (128, 128, 128),  # Asfalto (Cinza Escuro)
        3: (190, 132, 85),   # Terra (Marrom)
        5: (50, 205, 50),    # Grama (Verde)
        10: (211, 211, 211), # Paralelepípedo (Cinza Claro)
        0: (255, 184, 103)   # Edifícios (Laranja)
    }
    cor_borda = (230, 238, 225)  # Cor da borda
    espessura_borda = 1          # Espessura da borda
    for i, linha in enumerate(mapa):
        for j, terreno in enumerate(linha):
            cor = cores.get(terreno, (255, 255, 255))  # Branco como cor padrão
            pygame.draw.rect(screen, cor, pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco))
            pygame.draw.rect(screen, cor_borda, pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco), espessura_borda)

# Função para desenhar personagens (círculos) em uma posição
def desenhar_personagem(screen, posicao, tamanho_bloco, cor):
    centro_x = posicao[0] * tamanho_bloco + tamanho_bloco // 2
    centro_y = posicao[1] * tamanho_bloco + tamanho_bloco // 2
    raio = tamanho_bloco // 3
    pygame.draw.rect(screen, cor, pygame.Rect(posicao[0] * tamanho_bloco, posicao[1] * tamanho_bloco, tamanho_bloco, tamanho_bloco))

# Função para calcular a heurística (distância de Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Função A* com diferentes custos de terreno
def a_star(mapa, start, goal):
    rows, cols = len(mapa), len(mapa[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristica(start, goal)}

    custo_terreno = {
        1: 1,    # Asfalto
        3: 3,    # Terra
        5: 5,    # Grama
        10: 10   # Paralelepípedo
    }

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, g_score[goal]

        for neighbor in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])
            if 0 <= neighbor_pos[0] < cols and 0 <= neighbor_pos[1] < rows and mapa[neighbor_pos[1]][neighbor_pos[0]] != 0:
                terreno = mapa[neighbor_pos[1]][neighbor_pos[0]]
                tentative_g_score = g_score[current] + custo_terreno.get(terreno, float('inf'))
                if tentative_g_score < g_score.get(neighbor_pos, float('inf')):
                    came_from[neighbor_pos] = current
                    g_score[neighbor_pos] = tentative_g_score
                    f_score[neighbor_pos] = tentative_g_score + heuristica(neighbor_pos, goal)
                    if neighbor_pos not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor_pos], neighbor_pos))
    return [], float('inf')

# Função para mover a Barbie e convencer amigos, exibindo informações no terminal
def mover_barbie(mapa, posicao_barbie, amigos, amigos_sorteados):
    caminho_total = []
    ponto_inicial = posicao_barbie
    amigos_encontrados = set()
    custo_total = 0

    print("Amigos sorteados para convencer:", amigos_sorteados)

    inicio = time_lib.time()  # Início do tempo de execução

    for amigo_nome, amigo_posicao in amigos.items():
        if amigo_nome not in amigos_encontrados:
            caminho, custo = a_star(mapa, ponto_inicial, amigo_posicao)
            for pos in caminho:
                caminho_total.append(pos)
                terreno = mapa[pos[1]][pos[0]]
                custo_terreno = {1: 1, 3: 3, 5: 5, 10: 10}.get(terreno, float('inf'))
                custo_total += custo_terreno
                print(f"Posição: {pos}, Custo acumulado: {custo_total}")

            ponto_inicial = amigo_posicao
            if amigo_nome in amigos_sorteados:
                amigos_encontrados.add(amigo_nome)
                if len(amigos_encontrados) == 3:
                    break

    caminho_retorno, custo_retorno = a_star(mapa, ponto_inicial, posicao_barbie)
    for pos in caminho_retorno:
        caminho_total.append(pos)
        terreno = mapa[pos[1]][pos[0]]
        custo_terreno = {1: 1, 3: 3, 5: 5, 10: 10}.get(terreno, float('inf'))
        custo_total += custo_terreno
        print(f"Posição: {pos}, Custo acumulado: {custo_total}")

    fim = time_lib.time()  # Fim do tempo de execução
    tempo_execucao = fim - inicio

    print(f"Tempo de execução do algoritmo: {tempo_execucao:.4f} segundos")

    return caminho_total, custo_total

# Função principal do jogo
def main():
    arquivo = "matriz.xlsx"
    mapa = ler_mapa_xlsx(arquivo)
    pygame.init()
    tamanho_bloco = 17
    largura = len(mapa[0]) * tamanho_bloco
    altura = len(mapa) * tamanho_bloco
    screen = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mapa do Mundo da Barbie')

    posicao_barbie = (19, 23)
    amigos = {
        "amigo_1": (13, 5),
        "amigo_2": (9, 10),
        "amigo_3": (35, 6),
        "amigo_4": (15, 36),
        "amigo_5": (37, 37),
        "amigo_6": (38, 24),
    }
    amigos_sorteados = random.sample(list(amigos.keys()), 3)
    
    cor_barbie = (255, 0, 123)
    cor_amigo = (48, 45, 100)
    cor_amigo_sorteado = (181, 54, 45)  # Cor do amigo sorteado
    cor_percurso = (255, 0, 123)

    caminho_total, custo_total = mover_barbie(mapa, posicao_barbie, amigos, amigos_sorteados)
    print(f"Custo total da jornada: {custo_total}")

    clock = pygame.time.Clock()
    posicao_atual = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        desenhar_mapa(screen, mapa, tamanho_bloco)
        desenhar_personagem(screen, posicao_barbie, tamanho_bloco, cor_barbie)

        # Desenha amigos com cor diferente se foram sorteados
        for amigo in amigos:
            if amigo in amigos_sorteados:
                desenhar_personagem(screen, amigos[amigo], tamanho_bloco, cor_amigo_sorteado)
            else:
                desenhar_personagem(screen, amigos[amigo], tamanho_bloco, cor_amigo)

        if posicao_atual < len(caminho_total):
            pos = caminho_total[posicao_atual]
            desenhar_personagem(screen, pos, tamanho_bloco, cor_percurso)
            posicao_atual += 1
            pygame.display.flip()
            time.sleep(0.1)
        else:
            posicao_atual = 0

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
