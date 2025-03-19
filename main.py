import pygame
import locale
import sys
import os
import ast

def search_data(_path):
    '''Leitura dos arquivos data presentes nos aquivos temporáreos _MEIPASS'''
    try:
        # sys._MEIPASS é uma variavel atribuida pelo pyinstaller para arquivos temporários
        base_path = os.path.join(sys._MEIPASS, "data");
    except:
        base_path = os.path.abspath("./data");
    return os.path.join(base_path, _path);
def _quit():
    '''Fecha a aplicação'''
    pygame.quit();
    sys.exit();
def set_display_config(name:str|None="FastText"):
    '''*name* é o nome da janela.'''
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
display = pygame.display.set_mode((1280, 720)); # Cria o display com proporção 720p
icon = pygame.image.load(search_data("images/icon.png"));
pygame.display.set_icon(icon);
set_display_config();
lang = locale.getlocale()[0]; # Pega a linguagem do dispositivo
clock = pygame.time.Clock();
dt = 0;
tte = None;
run = False;

# filetext_selected = True;
# user_input_textbox = "";
# textbox_spr = pygame.image.load(search_data("images/icon.png"));
# textbox_selected = False;
# font_textbox = pygame.font.Font(None, 64);
# while filetext_selected:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: _quit();
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = event.pos;
#             textbox_rect = textbox_spr.get_rect(center=(display.get_width()/2, display.get_height()/2));
#             if textbox_rect.collidepoint(mouse_pos):
#                 textbox_selected = True;
#         if event.type == pygame.KEYDOWN:
#             if textbox_selected == True:
#                 if event.key == pygame.K_BACKSPACE:
#                     user_input_textbox[:-1];
#                 else:
#                     user_input_textbox += event.unicode;

#     display.fill("black");
    
#     display.blit(textbox_spr, pygame.Vector2(display.get_width()/2, display.get_height()/2));
#     display.blit(font_textbox.render(user_input_textbox, True, "white"), pygame.Vector2(display.get_width()/2, display.get_height()/2));

#     pygame.display.flip();
#     dt = clock.tick(60);

with open("config.txt", "r") as config:
    for c in config.readlines():
        # 'c.split("=")[1].split(",")[0]' pega o valor da configuração
        # 'ast.literal_eval()' transforma a string em um boleano ou um número racional
        def get_split(mode:str|None=None):
            '''***mode***: "literal" or "int"'''
            if mode is None:
                var = c.split("=")[1].split(",")[0];
            match mode:
                case "literal":
                    var = ast.literal_eval(c.split("=")[1].split(",")[0]);
                case "int":
                    var = int(c.split("=")[1].split(",")[0]);
            return var;
    
        match c.split("=")[0]:
            case "WPS":
                wps = get_split("literal");
            case "WORD_COLOR":
                color_text = get_split();
            case "BUTTON_COLOR":
                button_color = get_split();
            case "BG_COLOR":
                color_bg = get_split();
            case "EDITION":
                edition = get_split();
            case "HIDE_BUTTONS":
                h_buttons = get_split("literal");
with open("text.txt", "r", encoding="utf-8") as file:
    w = file.read().split(); # 'split()' serve para quebrar uma string em várias, o padrão do sep são espaços
index_w = 0;
len_w = len(w); # Tamanho da lista

font = pygame.font.Font(None, 74); # Fonte
match lang:
    case "pt_BR":
        text = font.render("Bem Vindo ao FastText", True, "red");
    case _:
        text = font.render("Welcome to the FastText", True, "red");
button_plus_spr = pygame.image.load(search_data("images/button_plus.png"));
button_minus_spr = pygame.image.load(search_data("images/button_minus.png"));

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: _quit();
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
        if tte <= 0: _quit();
    
    display.fill(color_bg);

    text_vec = pygame.Vector2(display.get_width()/2-text.get_width()/2, display.get_height()/2-text.get_height()/2);
    button_vec = pygame.Vector2(display.get_width()/2-button_spr.get_width()/2, display.get_height()/4+display.get_height()/2-button_spr.get_height()/2);
    
    display.blit(text, text_vec);
    if h_buttons == True:
        display.blit(button_spr, button_vec);

    pygame.display.flip();
    dt = clock.tick(60);