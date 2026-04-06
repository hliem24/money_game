import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

try:
    pygame.mixer.init()
    ok = True
except:
    ok = False

def play_music():
    if not ok: return
    try:
        pygame.mixer.music.load("assets/bg_music.mp3")
        pygame.mixer.music.play(-1)
    except: pass

def play_catch():
    if not ok: return
    try:
        pygame.mixer.Sound("assets/catch.wav").play()
    except: pass

def play_lose():
    if not ok: return
    try:
        pygame.mixer.Sound("assets/lose.wav").play()
    except: pass