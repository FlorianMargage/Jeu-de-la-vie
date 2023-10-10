import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.backend_bases import MouseButton
import json as js

'''
Touches :
Augmenter d'une étape: Z ou flèche du droite
Descendre d'une étape: A ou flèche de gauche
Augmenter la vitesse: + ou flèche du haut
Diminuer la vitesse: - ou flèche du bas
Augmenter les naissances : B
Diminuer les naissances : N

Enregistrer: E
Charger: R

Mettre en pause: P

Fonctionnalités:
Inverser les cellules vivantes et mortes : ESPACE
Ajouter une cellule vivante: Clic Gauche
Ajouter un motif étoile: Clic Droit
'''

def save():
    global grid
    dict = {'grille': grid.tolist()}
    json = js.dumps(dict)

    with open("game_of_life_state.json", "w") as json_file:
        json_file.write(json)
    print("Fichier enregistré")


def load():
    global grid
    global N
    with open('game_of_life_state.json') as json_file:
        state = js.load(json_file)
        if len(np.array(state["grille"])) == N:
            grid = np.array(state["grille"])
            print("Fichier chargé")
        else:
            print("Erreur, taille de grille différente")


def verif(value):
    if value == 1:
        return 1
    else:
        return 0


def reaction(nb, state):
    global b
    if state >= 2:
        return state - 1
    else:
        if nb < 2:
            return 0
        elif nb == 2:
            return state
        elif nb == 3:
            if state == 0:
                return 1 + b
            else:
                return 1
        else:
            return 0


def newgrid(fgrid):
    tmpgrid = np.zeros((len(fgrid), len(fgrid[0])))
    for i in range(len(tmpgrid)):
        for j in range(len(tmpgrid[0])):
            # coins
            # coin haut gauche
            if i == 0 and j == 0:
                nb = verif(fgrid[i][j + 1]) + verif(fgrid[i + 1][j]) + verif(fgrid[i + 1][j + 1])
            # coin haut droit
            elif i == 0 and j == len(fgrid[0]) - 1:
                nb = verif(fgrid[i][j - 1]) + verif(fgrid[i + 1][j - 1]) + verif(fgrid[i + 1][j])
            # coin bas gauche
            elif i == len(fgrid) - 1 and j == 0:
                nb = verif(fgrid[i - 1][j]) + verif(fgrid[i - 1][j + 1]) + verif(fgrid[i][j + 1])
            # coin bas droit
            elif i == len(fgrid) - 1 and j == len(fgrid[0]) - 1:
                nb = verif(fgrid[i - 1][j - 1]) + verif(fgrid[i][j - 1]) + verif(fgrid[i][j - 1])

            # bords
            # bord haut
            elif i == 0:
                nb = verif(fgrid[i][j - 1]) + verif(fgrid[i][j + 1]) + verif(fgrid[i + 1][j - 1]) + verif(
                    fgrid[i + 1][j]) + verif(fgrid[i + 1][j + 1])
            # bord gauche
            elif j == 0:
                nb = verif(fgrid[i - 1][j]) + verif(fgrid[i + 1][j]) + verif(fgrid[i - 1][j + 1]) + verif(
                    fgrid[i][j + 1]) + verif(fgrid[i + 1][j + 1])
            # bord droit
            elif j == len(fgrid[0]) - 1:
                nb = verif(fgrid[i - 1][j - 1]) + verif(fgrid[i - 1][j]) + verif(fgrid[i][j - 1]) + verif(
                    fgrid[i + 1][j - 1]) + verif(fgrid[i + 1][j])
            # bord bas
            elif i == len(fgrid) - 1:
                nb = verif(fgrid[i - 1][j - 1]) + verif(fgrid[i - 1][j]) + verif(fgrid[i - 1][j + 1]) + verif(
                    fgrid[i][j - 1]) + verif(fgrid[i][j + 1])
            # non rattaché à un bord
            else:
                nb = verif(fgrid[i - 1][j - 1]) + verif(fgrid[i - 1][j]) + verif(fgrid[i - 1][j + 1]) + verif(
                    fgrid[i][j - 1]) + verif(fgrid[i][j + 1]) + verif(fgrid[i + 1][j - 1]) + verif(
                    fgrid[i + 1][j]) + verif(fgrid[i + 1][j + 1])
            tmpgrid[i][j] = reaction(nb, fgrid[i][j])
    return tmpgrid


def on_press(event):
    # Quand on modifie une variable globale, il faut ajouter cette ligne
    global last_key_pressed
    global speed
    global stage
    global start
    global b
    global grid

    last_key_pressed = event.key
    if last_key_pressed == "z" or last_key_pressed == "right":
        stage += 1
    elif (last_key_pressed == "a" or last_key_pressed == "left") and stage > 0:
        stage -= 1
    elif (last_key_pressed == "+" or last_key_pressed == "up") and speed > 0:
        speed -= 1
    elif (last_key_pressed == "-" or last_key_pressed == "down") and speed < maxspeed:
        speed += 1
    elif last_key_pressed == "p":
        if start:
            ani.pause()
            start = False
        else:
            ani.resume()
            start = True
    elif last_key_pressed == "b":
        b += 1
    elif last_key_pressed == "n" and b > 0:
        b -= 1
    elif last_key_pressed == "e":
        save()
    elif last_key_pressed == "r":
        load()
    elif last_key_pressed == " ":
        grid = inversion(grid)
    return event


def on_click(event):
    global grid
    button = event
    if button.xdata != None and button.ydata != None:
        if button.button is MouseButton.LEFT:
            # print(round(event.xdata), round(event.ydata))
            grid[round(button.ydata)][round(button.xdata)] = 1
            return grid, event
        elif button.button is MouseButton.RIGHT:
            x, y = round(button.xdata), round(button.ydata)
            if 1 < y < len(grid)-2 and 1 < x < len(grid[0])-2:
                grid[y][x] = 1
                grid[y][x - 2] = 1
                grid[y][x + 2] = 1
                grid[y - 2][x] = 1
                grid[y + 2][x] = 1
                grid[y + 1][x + 1] = 1
                grid[y + 1][x - 1] = 1
                grid[y - 1][x - 1] = 1
                grid[y - 1][x + 1] = 1
                return grid, event
    return event


def nbcell(fgrid):
    alive = 0
    dead = 0
    for i in range(len(fgrid)):
        for j in range(len(fgrid[0])):
            if fgrid[i][j] == 0:
                dead += 1
            elif fgrid[i][j] == 1:
                alive += 1

    return [alive, dead]


def diffgrid(oldgrid, newgrid):
    born = 0
    dead = 0
    for i in range(len(oldgrid)):
        for j in range(len(oldgrid[0])):
            if oldgrid[i][j] == 1 and newgrid[i][j] == 0:
                dead += 1
            elif oldgrid[i][j] == 0 and (newgrid[i][j] == 1 or newgrid[i][j] == 2):
                born += 1
    return [born, dead]


def inversion(fgrid):
    tmpgrid = np.zeros((len(fgrid), len(fgrid[0])))
    for i in range(len(tmpgrid)):
        for j in range(len(tmpgrid[0])):
            if fgrid[i][j] == 0:
                tmpgrid[i][j] = 1
            elif fgrid[i][j] == 1:
                tmpgrid[i][j] = 0
            else:
                tmpgrid[i][j] = fgrid[i][j]
    return tmpgrid


def update(frame):
    global grid
    global oldgrid
    global last_key_pressed
    global b
    global countframe

    if countframe < speed:
        countframe += 1
        return
    countframe = 0

    for i in range(stage):
        oldgrid = grid
        grid = newgrid(list(grid))

    borndead = diffgrid(oldgrid, grid)
    cell = nbcell(grid)
    figtext.set_text(f"frame: {frame}. Étapes: {stage}. Vitesse: {maxspeed-speed}.\n Nb Naissance: {b}. Nb vivant/mort: {cell[0]}/{cell[1]}.  Nvnés: {borndead[0]}. Nvmorts: {borndead[1]}")
    mat.set_data(grid)
    return [mat]


N = 40
p = 0.5
speed = 10


start = True
vals = [0, 1, 2]
stage = 0
maxspeed = speed
countframe = 0
b = 0
last_key_pressed = None
grid = np.zeros((N, N))

# initialisation d'une grille pour les couleurs
grid[0][1], grid[1][0] = 1, 2
fig, ax = plt.subplots()
# Couleur 0 = 'black', 1 = 'yellow' 2 >= 'green'
mat = ax.matshow(grid, cmap=ListedColormap(['black', 'yellow', 'green']))
grid = np.random.choice(vals, N * N, p=[1 - p, p, 0]).reshape(N, N)

oldgrid = grid

figtext = plt.figtext(0.5, 0.01, "", wrap=True, horizontalalignment='center', fontsize=12)

ani = animation.FuncAnimation(fig, update, interval=50, save_count=50)

fig.canvas.mpl_connect('key_press_event', on_press)
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
