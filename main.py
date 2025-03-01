import pygame
import ast

pygame.init();
pygame.mixer.init();
display = pygame.display.set_mode((1280, 720));
icon = pygame.image.load("assets/icon.png");
pygame.display.set_icon(icon);
pygame.display.set_caption("FastText");
clock = pygame.time.Clock();
dt = 0;
tte = None;
run = False;

with open("config.txt", "r") as config:
    for c in config.readlines():
        match c.split("=")[0]:
            case "WPS":
                wps = ast.literal_eval(c.split("=")[1].split(",")[0]);
            case "WORD_COLOR":
                color_text = c.split("=")[1].split(",")[0];
            case "BG_COLOR":
                color_bg = c.split("=")[1].split(",")[0];
            case "LANG":
                lang = c.split("=")[1].split(",")[0];
with open("text.txt", "r", encoding="utf-8") as file:
    w = file.read().split();
index_w = 0;
len_w = len(w);

font = pygame.font.Font(None, 74);
match lang:
    case "en":
        text = font.render("Welcome to the FastText", True, "red");
        button_text = font.render("BEGIN/PAUSE", True, color_bg);
    case "pt":
        text = font.render("Bem Vindo ao FastText", True, "red");
        button_text = font.render("COMEÇAR/PAUSAR", True, color_bg);
button_spr = pygame.image.load("assets/button.png");

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit();
        if (event.type == pygame.KEYUP) and (event.key == pygame.K_SPACE):
            if (run == False) and (tte is None):
                run = True;
                pygame.mixer.music.unload();
            elif (tte is None):
                run = False;
                pygame.display.set_caption("FastText - Stopped Time");
                pygame.mixer.music.load("assets/zawarudo.mp3");
                pygame.mixer.music.play();
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos;
            button_rect = button_spr.get_rect(center=(display.get_width()/2, display.get_height()/2 + display.get_height()/4));
            if button_rect.collidepoint(mouse_pos):
                if (run == False) and (tte is None):
                    run = True;
                    pygame.mixer.music.unload();
                elif (tte is None):
                    run = False;
                    pygame.display.set_caption("FastText - Stopped Time");
                    pygame.mixer.music.load("assets/zawarudo.mp3");
                    pygame.mixer.music.play();
    
    if run == True:
        if pygame.display.get_caption() != ('FastText', 'FastText'):
            pygame.display.set_caption("FastText");
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
    
    display.fill(color_bg);

    text_vec = pygame.Vector2(display.get_width()/2-text.get_width()/2, display.get_height()/2-text.get_height()/2);
    button_vec = pygame.Vector2(display.get_width()/2-button_spr.get_width()/2, display.get_height()/4+display.get_height()/2-button_spr.get_height()/2);
    
    display.blit(text, text_vec);
    display.blit(button_spr, button_vec);
    display.blit(button_text, pygame.Vector2(display.get_width()/2-button_text.get_width()/2, display.get_height()/4+display.get_height()/2-button_text.get_height()/2));

    pygame.display.flip();
    dt = clock.tick(60);