import pygame
import locale
import sys
import os
import ast

def search_data(_path):
    try:
        base_path = os.path.join(sys._MEIPASS, "data");
    except:
        base_path = os.path.abspath("./data");
    return os.path.join(base_path, _path);
def set_display_config(name:str|None="FastText"):
    pygame.display.set_caption(name);
def pause(run):
    match run:
        case True:
            run = False;
            if edition == "jo2x":
                set_display_config("FastText - Stopped Time");
                pygame.mixer.music.load(search_data("sounds/pause_jo2x.mp3"));
                pygame.mixer.music.play();
        case False:
            run = True;
            pygame.mixer.music.unload();
    return run;

pygame.init();
pygame.mixer.init();
display = pygame.display.set_mode((1280, 720));
icon = pygame.image.load(search_data("images/icon.png"));
pygame.display.set_icon(icon);
set_display_config();
lang = locale.getlocale()[0];
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
            case "BUTTON_COLOR":
                button_color = c.split("=")[1].split(",")[0];
            case "BG_COLOR":
                color_bg = c.split("=")[1].split(",")[0];
            case "EDITION":
                edition = c.split("=")[1].split(",")[0];
            case "HIDE_BUTTONS":
                h_buttons = ast.literal_eval(c.split("=")[1].split(",")[0]);
with open("text.txt", "r", encoding="utf-8") as file:
    w = file.read().split();
index_w = 0;
len_w = len(w);

font = pygame.font.Font(None, 74);
match lang:
    case "pt_BR":
        text = font.render("Bem Vindo ao FastText", True, "red");
    case _:
        text = font.render("Welcome to the FastText", True, "red");
button_plus_spr = pygame.image.load(search_data("images/button_plus.png"));
button_minus_spr = pygame.image.load(search_data("images/button_minus.png"));

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit();
        if (event.type == pygame.KEYUP) and (event.key == pygame.K_SPACE):
            if tte is None:
                run = pause(run);
        if h_buttons == True:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos;
                button_rect = button_spr.get_rect(center=(display.get_width()/2, display.get_height()/2 + display.get_height()/4));
                if button_rect.collidepoint(mouse_pos):
                    if tte is None:
                        run = pause(run);
    
    match run:
        case True:
            button_spr = pygame.image.load(search_data("images/button_pause.png"));
        case False:
            button_spr = pygame.image.load(search_data("images/button_play.png"));
    button_spr.fill(button_color, special_flags=pygame.BLEND_RGB_MULT);

    if run == True:
        if pygame.display.get_caption() != ('FastText', 'FastText'):
            set_display_config();
        if pygame.time.get_ticks() % (1000 // wps) < dt:
            text = font.render(w[index_w], True, color_text);
            index_w += 1;
            if index_w >= len_w:
                index_w = 0;
                tte = 8;
                if edition == "jo2x":
                    pygame.mixer.music.load(search_data("sounds/end_jo2x.mp3"));
                    pygame.mixer.music.play();
                run = False;
    elif (pygame.time.get_ticks() % (1000 // 1) < dt) and (tte is not None):
        tte -= 1;
        match lang:
            case "pt_BR":
                text = font.render(f"Tchau, a aplicação fechará em {tte}", True, "red");
            case _:
                text = font.render(f"Bye, exit the aplication in {tte}", True, "red");
        if tte <= 0: exit();
    
    display.fill(color_bg);

    text_vec = pygame.Vector2(display.get_width()/2-text.get_width()/2, display.get_height()/2-text.get_height()/2);
    button_vec = pygame.Vector2(display.get_width()/2-button_spr.get_width()/2, display.get_height()/4+display.get_height()/2-button_spr.get_height()/2);
    
    display.blit(text, text_vec);
    if h_buttons == True:
        display.blit(button_spr, button_vec);

    pygame.display.flip();
    dt = clock.tick(60);