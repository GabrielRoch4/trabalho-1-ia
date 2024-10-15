import openpyxl
import pygame

# Função para ler o arquivo .xlsx e transformar em matriz
def ler_mapa_xlsx(arquivo_xlsx):
    wb = openpyxl.load_workbook(arquivo_xlsx)
    sheet = wb.active

    mapa = []
    for row in sheet.iter_rows(values_only=True):
        mapa.append(list(row))

    return mapa

# Função para desenhar o mapa na tela
def desenhar_mapa(screen, mapa, tamanho_bloco):
    # Cores para cada tipo de terreno
    cores = {
        1: (128, 128, 128),  # Asfalto (Cinza Escuro)
        3: (139, 69, 19),    # Terra (Marrom)
        5: (50, 205, 50),      # Grama (Verde)
        10: (211, 211, 211),  # Paralelepípedo (Cinza Claro)
        0: (210, 105, 30)     # Edifícios (Laranja)
    }

    for i, linha in enumerate(mapa):
        for j, terreno in enumerate(linha):
            # Definir a cor de acordo com o tipo de terreno
            cor = cores.get(terreno, (255, 255, 255))  # Branco como cor padrão
            # Desenhar o retângulo correspondente ao terreno
            pygame.draw.rect(screen, cor, pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco))

# Função principal do jogo
def main():
    # Ler o mapa do arquivo .xlsx
    arquivo = "matriz.xlsx"
    mapa = ler_mapa_xlsx(arquivo)

    # Inicializar o Pygame
    pygame.init()

    # Definir tamanho da tela (largura e altura)
    tamanho_bloco = 18  # Tamanho de cada célula no mapa
    largura = len(mapa[0]) * tamanho_bloco
    altura = len(mapa) * tamanho_bloco
    screen = pygame.display.set_mode((largura, altura))

    pygame.display.set_caption('Mapa do Mundo da Barbie')

    # Loop principal do jogo
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        # Preencher a tela com branco
        screen.fill((255, 255, 255))

        # Desenhar o mapa na tela
        desenhar_mapa(screen, mapa, tamanho_bloco)

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()

# Executar o programa
if __name__ == "__main__":
    main()
