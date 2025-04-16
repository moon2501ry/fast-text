import pygame
import locale
import sys
import os
from config import ConfigTXT

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
            if config.get("edition") == "jo2x":
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

config = ConfigTXT({"wps":"literal,0.6","word_color":"str,blue","button_color":"str,white","bg_color":"str,black","edition":"str,none","hide_buttons":"literal,True"});
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
button_minus_spr = pygame.image.load(search_data("images/button_minus.png"));
button_plus_spr = pygame.image.load(search_data("images/button_plus.png"));
button_minus_spr.fill(config.get("button_color"), special_flags=pygame.BLEND_RGB_MULT);
button_plus_spr.fill(config.get("button_color"), special_flags=pygame.BLEND_RGB_MULT);

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: _quit();
        if (event.type == pygame.KEYUP) and (event.key == pygame.K_SPACE):
            if tte is None:
                run = pause(run);
        if config.get("hide_buttons") == True:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos;
                button_rect = button_spr.get_rect(center=(display.get_width()/2, display.get_height()/2 + display.get_height()/4));
                button_minus_rect = button_minus_spr.get_rect(center=((display.get_width()/2)-75, display.get_height()/4+display.get_height()/2));
                button_plus_rect = button_plus_spr.get_rect(center=((display.get_width()/2)+75, display.get_height()/4+display.get_height()/2));
                if run == True:
                    if button_minus_rect.collidepoint(mouse_pos):
                        index_w -= 1;
                    if button_plus_rect.collidepoint(mouse_pos):
                        index_w += 1;
                if (button_rect.collidepoint(mouse_pos)) and (tte is None):
                        run = pause(run);
    
    match run:
        case True:
            button_spr = pygame.image.load(search_data("images/button_pause.png"));
        case False:
            button_spr = pygame.image.load(search_data("images/button_play.png"));
    button_spr.fill(config.get("button_color"), special_flags=pygame.BLEND_RGB_MULT);

    if run == True:
        if pygame.display.get_caption() != ('FastText', 'FastText'):
            set_display_config();
        text = font.render(w[index_w], True, config.get("word_color"));
        if pygame.time.get_ticks() % (1000 // config.get("wps")) < dt:
            index_w += 1;
            if index_w >= len_w:
                index_w = 0;
                tte = 8;
                if config.get("edition") == "jo2x":
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
    
    display.fill(config.get("bg_color"));

    background = pygame.image.load(search_data("images/background_time.png"));
    background.fill(config.get("bg_color"), special_flags=pygame.BLEND_RGB_MULT);
    text_vec = pygame.Vector2(display.get_width()/2-text.get_width()/2, display.get_height()/2-text.get_height()/2);
    button_vec = pygame.Vector2(display.get_width()/2-button_spr.get_width()/2, display.get_height()/4+display.get_height()/2-button_spr.get_height()/2);
    button_minus_vec = pygame.Vector2(((display.get_width()/2)-button_spr.get_width())-button_minus_spr.get_width()/2, display.get_height()/4+display.get_height()/2-button_minus_spr.get_height()/2);
    button_plus_vec = pygame.Vector2(((display.get_width()/2)+button_spr.get_width())-button_plus_spr.get_width()/2, display.get_height()/4+display.get_height()/2-button_plus_spr.get_height()/2);
    
    display.blit(background, (0,0));
    display.blit(text, text_vec);
    if config.get("hide_buttons") == True:
        display.blit(button_spr, button_vec);
        display.blit(button_minus_spr, button_minus_vec);
        display.blit(button_plus_spr, button_plus_vec);

    pygame.display.flip();
    dt = clock.tick(60);