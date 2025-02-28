import pygame
import ast

pygame.init();
display = pygame.display.set_mode((1280, 720));
pygame.display.set_caption("Fast Text");
clock = pygame.time.Clock();
dt = 0;
tte = None;
run = False;

with open("config.txt", "r") as config:
    wps = ast.literal_eval(config.read());
with open("text.txt", "r") as file:
    w = file.read().split();
index_w = 0;
len_w = len(w);

font = pygame.font.Font(None, 74);
text = font.render("Welcome to the FastText. Press SPACE for begin", True, "red");

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit();
        if (event.type == pygame.KEYUP) and (event.key == pygame.K_SPACE):
            if run != True: run = True;

    
    if run == True:
        if pygame.time.get_ticks() % (1000 // wps) < dt:
            text = font.render(w[index_w], True, "blue");
            index_w += 1;
            if index_w >= len_w:
                index_w = 0;
                tte = 5;
                run = False;
    elif (pygame.time.get_ticks() % (1000 // 1) < dt) and (tte is not None):
        tte -= 1;
        text = text = font.render(f"Bye, exit the aplication in {tte}", True, "red");
        if tte <= 0: quit();
    
    display.fill("black");

    text_vec = pygame.Vector2(display.get_width()/2-text.get_width()/2, display.get_height()/2-text.get_height()/2);
    
    display.blit(text, text_vec);

    pygame.display.flip();
    dt = clock.tick(60);