import openpyxl
import pygame
import time
import random
import sys  # Importar sys para encerrar o programa
import heapq  # Para implementar o algoritmo A*

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
    pygame.draw.circle(screen, cor, (centro_x, centro_y), raio)

# Função para exibir mensagem de erro
def exibir_mensagem(screen, mensagem, largura, altura):
    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render(mensagem, True, (255, 255, 255))  # Branco para a mensagem de erro
    
    retangulo_x = largura // 2 - texto.get_width() // 2 - 10
    retangulo_y = altura // 2 - texto.get_height() // 2 - 10
    retangulo_largura = texto.get_width() + 20
    retangulo_altura = texto.get_height() + 20

    pygame.draw.rect(screen, (0, 0, 0), (retangulo_x, retangulo_y, retangulo_largura, retangulo_altura))
    screen.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))

# Função para verificar se a posição é válida (não é um edifício)
def verificar_posicao_valida(mapa, posicao, nome_personagem):
    if mapa[posicao[1]][posicao[0]] == 0:  # Edifícios são representados por 0
        print(f"Erro: {nome_personagem} foi colocado em um edifício. Posição: {posicao}")
        sys.exit(1)  # Encerrar o programa com erro

# Função para sortear aleatoriamente 3 amigos
def sortear_amigos(amigos):
    amigos_sorteados = random.sample(list(amigos.keys()), 3)
    print(f"Amigos sorteados: {amigos_sorteados}")
    return amigos_sorteados

# Função para calcular a heurística (distância de Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Função A* para encontrar o caminho mais curto
def a_star(mapa, start, goal):
    rows, cols = len(mapa), len(mapa[0])
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f_score, posição)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristica(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Inverter o caminho
            return path

        for neighbor in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Cima, Direita, Baixo, Esquerda
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])
            if 0 <= neighbor_pos[0] < cols and 0 <= neighbor_pos[1] < rows and mapa[neighbor_pos[1]][neighbor_pos[0]] != 0:
                tentative_g_score = g_score[current] + 1  # Custo constante de 1
                if tentative_g_score < g_score.get(neighbor_pos, float('inf')):
                    came_from[neighbor_pos] = current
                    g_score[neighbor_pos] = tentative_g_score
                    f_score[neighbor_pos] = tentative_g_score + heuristica(neighbor_pos, goal)
                    if neighbor_pos not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor_pos], neighbor_pos))

    return []  # Retornar lista vazia se não encontrar caminho

# Função para mover a Barbie e encontrar amigos sorteados
def mover_barbie_encontrar_amigos(mapa, posicao_barbie, amigos, amigos_sorteados):
    caminho_total = []
    ponto_inicial = posicao_barbie
    amigos_encontrados = set()

    for amigo_nome, amigo_posicao in amigos.items():
        if amigo_nome not in amigos_encontrados:  # Evitar visitar o mesmo amigo duas vezes
            caminho = a_star(mapa, ponto_inicial, amigo_posicao)
            caminho_total.extend(caminho)
            ponto_inicial = amigo_posicao  # Atualiza a posição da Barbie

            # Verifica se o amigo encontrado está entre os sorteados
            if amigo_nome in amigos_sorteados:
                amigos_encontrados.add(amigo_nome)
                if len(amigos_encontrados) == 3:
                    break

    return caminho_total

# Função principal do jogo
def main():
    # Ler o mapa do arquivo .xlsx
    arquivo = "matriz.xlsx"
    mapa = ler_mapa_xlsx(arquivo)

    # Inicializar o Pygame
    pygame.init()

    # Definir tamanho da tela (largura e altura)
    tamanho_bloco = 17  # Tamanho de cada célula no mapa
    largura = len(mapa[0]) * tamanho_bloco
    altura = len(mapa) * tamanho_bloco
    screen = pygame.display.set_mode((largura, altura))

    pygame.display.set_caption('Mapa do Mundo da Barbie')

    # Definir a posição inicial fixa da Barbie e dos amigos
    posicao_barbie = (19, 23)
    
    amigos = {
        "amigo_1": (13, 5),
        "amigo_2": (9, 10),
        "amigo_3": (35, 6),
        "amigo_4": (15, 36),
        "amigo_5": (37, 37),
        "amigo_6": (38, 24),
    }

    # Verificar se a posição da Barbie é válida
    verificar_posicao_valida(mapa, posicao_barbie, "Barbie")

    # Sortear 3 amigos
    amigos_sorteados = sortear_amigos(amigos)

    # Verificar se a posição dos amigos sorteados é válida
    for amigo in amigos.values():  # Verificar todos os amigos
        verificar_posicao_valida(mapa, amigo, amigo)

    # Cores para a Barbie e os amigos
    cor_barbie = (255, 0, 123)  # Rosa
    cor_amigo = (48, 45, 100)    # Azul Claro
    cor_percurso = (255, 0, 123)  # Amarelo para o percurso

    # Calcular o caminho para encontrar os amigos sorteados
    caminho_total = mover_barbie_encontrar_amigos(mapa, posicao_barbie, amigos, amigos_sorteados)

    # Loop do jogo
    clock = pygame.time.Clock()
    posicao_atual = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Desenhar o mapa
        screen.fill((0, 0, 0))
        desenhar_mapa(screen, mapa, tamanho_bloco)

        # Desenhar a Barbie
        desenhar_personagem(screen, posicao_barbie, tamanho_bloco, cor_barbie)

        # Desenhar todos os amigos no mapa
        for amigo in amigos:
            desenhar_personagem(screen, amigos[amigo], tamanho_bloco, cor_amigo)

        # Desenhar o percurso
        if posicao_atual < len(caminho_total):
            pos = caminho_total[posicao_atual]
            desenhar_personagem(screen, pos, tamanho_bloco, cor_percurso)
            posicao_atual += 1
            pygame.display.flip()
            time.sleep(0.1)  # Atraso para visualização do percurso
        else:
            posicao_atual = 0  # Reiniciar o percurso quando concluído

        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 quadros por segundo

# Iniciar o programa
if __name__ == "__main__":
    main()
