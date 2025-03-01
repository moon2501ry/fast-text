import pygame
import ast

pygame.init();
display = pygame.display.set_mode((1280, 720));
icon = pygame.image.load("data/icon.png");
pygame.display.set_icon(icon);
pygame.display.set_caption("Fast Text");
clock = pygame.time.Clock();
dt = 0;
tte = None;
run = False;

with open("config.txt", "r") as config:
    for c in config.readlines():
        match c.split("=")[0]:
            case "WPS":
                wps = ast.literal_eval(c.split("=")[1].split(",")[0]);
            case "COLOR":
                color_text = c.split("=")[1].split(",")[0];
            case "LANG":
                lang = c.split("=")[1].split(",")[0];
with open("text.txt", "r", encoding="utf-8") as file:
    w = file.read().split();
index_w = 0;
len_w = len(w);

font = pygame.font.Font(None, 74);
match lang:
    case "en":
        text = font.render("Welcome to the FastText. Press SPACE for begin", True, "red");
    case "pt":
        text = font.render("Bem Vindo ao FastText. Pressione ESPAÇO", True, "red");
    case _:
        text = font.render("Welcome to the FastText. Press SPACE for begin", True, "red");

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit();
        if (event.type == pygame.KEYUP) and (event.key == pygame.K_SPACE):
            if (run != True) and (tte is None): run = True;

    
    if run == True:
        if pygame.time.get_ticks() % (1000 // wps) < dt:
            text = font.render(w[index_w], True, color_text);
            index_w += 1;
            if index_w >= len_w:
                index_w = 0;
                tte = 5;
                run = False;
    elif (pygame.time.get_ticks() % (1000 // 1) < dt) and (tte is not None):
        tte -= 1;
        match lang:
            case "en":
                text = font.render(f"Bye, exit the aplication in {tte}", True, "red");
            case "pt":
                text = font.render(f"Tchau, a aplicação fechará em {tte}", True, "red");
        if tte <= 0: exit();
    
    display.fill("black");

    text_vec = pygame.Vector2(display.get_width()/2-text.get_width()/2, display.get_height()/2-text.get_height()/2);
    
    display.blit(text, text_vec);

    pygame.display.flip();
    dt = clock.tick(60);