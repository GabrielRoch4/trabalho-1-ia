import openpyxl
import pygame
import time

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
    # Cores para cada tipo de terreno
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
            # Definir a cor de acordo com o tipo de terreno
            cor = cores.get(terreno, (255, 255, 255))  # Branco como cor padrão

            # Desenhar o retângulo correspondente ao terreno
            pygame.draw.rect(screen, cor, pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco))

            # Desenhar a borda ao redor do quadrado
            pygame.draw.rect(screen, cor_borda, pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco), espessura_borda)

# Função para desenhar a Barbie (círculo) em uma posição
def desenhar_barbie(screen, posicao, tamanho_bloco):
    # Cor da Barbie (círculo)
    cor_barbie = (255, 0, 123)  # Rosa

    # Calcular o centro do quadrado onde o círculo será desenhado
    centro_x = posicao[0] * tamanho_bloco + tamanho_bloco // 2
    centro_y = posicao[1] * tamanho_bloco + tamanho_bloco // 2

    # Desenhar um círculo menor que o quadrado (representa a Barbie)
    raio = tamanho_bloco // 3
    pygame.draw.circle(screen, cor_barbie, (centro_x, centro_y), raio)

# Função para exibir mensagem de erro
def exibir_mensagem(screen, mensagem, largura, altura):
    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render(mensagem, True, (255, 255, 255))  # Branco para a mensagem de erro
    
    # Calcular a posição do retângulo em torno do texto
    retangulo_x = largura // 2 - texto.get_width() // 2 - 10  # 10 pixels de margem
    retangulo_y = altura // 2 - texto.get_height() // 2 - 10  # 10 pixels de margem
    retangulo_largura = texto.get_width() + 20  # 20 pixels de largura (10 de margem de cada lado)
    retangulo_altura = texto.get_height() + 20  # 20 pixels de altura (10 de margem em cima e embaixo)

    # Desenhar o retângulo preto
    pygame.draw.rect(screen, (0, 0, 0), (retangulo_x, retangulo_y, retangulo_largura, retangulo_altura))

    # Desenhar o texto no centro do retângulo
    screen.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))


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

    # Definir a posição inicial fixa da Barbie
    posicao_barbie = (19, 23)
    mensagem_erro = None
    tempo_mensagem = 0

    # Loop principal do jogo
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Calcular em qual célula o clique ocorreu
                pos_x = mouse_pos[0] // tamanho_bloco
                pos_y = mouse_pos[1] // tamanho_bloco

                # Mostrar a posição clicada no console
                print(f"Posição clicada: ({pos_x}, {pos_y})")

                # Verificar se o clique está nas bordas ou em um edifício (laranja)
                if pos_x == 0 or pos_y == 0 or pos_x == len(mapa[0]) - 1 or pos_y == len(mapa) - 1:
                    mensagem_erro = "Clique em outro local"
                    tempo_mensagem = time.time()  # Armazenar o tempo atual
                elif mapa[pos_y][pos_x] == 0:  # Verificar se é um edifício
                    mensagem_erro = "Terreno inválido! Edifício selecionado"
                    tempo_mensagem = time.time()  # Armazenar o tempo atual
                else:
                    mensagem_erro = None  # Remover a mensagem de erro

        # Preencher a tela com branco
        screen.fill((255, 255, 255))

        # Desenhar o mapa na tela
        desenhar_mapa(screen, mapa, tamanho_bloco)

        # Desenhar a Barbie na posição fixa
        desenhar_barbie(screen, posicao_barbie, tamanho_bloco)

        # Exibir a mensagem de erro se existir e se tiver passado menos de 2 segundos
        if mensagem_erro and time.time() - tempo_mensagem < 2:
            exibir_mensagem(screen, mensagem_erro, largura, altura)

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()

# Executar o programa
if __name__ == "__main__":
    main()
