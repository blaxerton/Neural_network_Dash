import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)

import pgzrun
import csv


TITLE="MA_Dash_Level_Editor"
WIDTH=1200
HEIGHT=700

hintergrund= Actor("kfeld")
player= Actor("player")


scroll = 0
scroll_right= False
scroll_left= False
scrollspeed= 1

player.bottom= 700
player.left= 0

BGs= []
Tiles=[]
Obs=[]

rows=7
collums=12

place_block=False
place_spike=False

current_level=3

for i in range(20):
    bild= Actor("kfeld")
    bild.left= WIDTH*i
    BGs.append(bild)

#create Tilemap
for i in range(rows):
    for p in range(collums*len(BGs)+1):
        Tile= Rect((p*100,i*100),(100,100))
        Tiles.append(Tile)

    




def draw():
    #drawing OG and Obstacles
    hintergrund.draw()
    for i in range(len(BGs)):
        BGs[i].draw()
        BGs[i].x += scroll
    for i in range(len(Obs)):
        Obs[i].draw()
        Obs[i].x += scroll
    
    for i in range(len(Tiles)):
        screen.draw.rect(Tiles[i],"white")
        Tiles[i].left += scroll
        
    player.draw()
    
    
    hintergrund.x += scroll
    
    
#     #vertical lines
#     for i in range((collums*len(BGs)) +1):
#         screen.draw.line(((100*i)+hintergrund.left,0),((100*i)+hintergrund.left,HEIGHT),"white")
#     #horizontal lines
#     for i in range(rows):
#         screen.draw.line((0,100*i),(WIDTH,100*i),"white")
    
    #display Obstacle selection
    if place_block:
        screen.draw.text("Block selected", ((WIDTH/2),(HEIGHT/2)), color="red")
    elif place_spike:
        screen.draw.text("Spike selected", ((WIDTH/2),(HEIGHT/2)), color="red")

    
    
def update():
    global scroll
    global place_block
    global place_spike
    
    
    #Hintergrund and Obstacle scrolling
    if hintergrund.left <= 0:
        
        if keyboard.left:
            scroll= 15
        elif keyboard.right:
            scroll= -15
        else:
            scroll=0
    else:
        scroll=0
        hintergrund.x -= 15
        for i in range(len(BGs)):
            BGs[i].x -= 15
        for i in range(len(Obs)):
            Obs[i].x -=15
        for i in range(len(Tiles)):
            Tiles[i].left -=15
    
    

    
def on_key_down(key):
    global place_block
    global place_spike
    
    #saving
    if key == keys.W:
        save(current_level)
        
    #checking for block placing
    if key == keys.B and place_block==False and place_spike==False:
        place_block=True
    elif key==keys.B and place_block==True and place_spike==False:
        place_block=False
    elif key== keys.B and place_block==False and place_spike==True:
        pass
    
    #checking for spike palcing
    elif key== keys.S and place_spike==False and place_block==False:
        place_spike=True
    elif key==keys.S and place_spike==True and place_block==False:
        place_spike=False
    elif key ==keys.S and place_spike==False and place_block==True:
        pass
    
    
    #loading in already made levels
    if key == keys.L:
        load(current_level)
       


#Editing map   
def on_mouse_down(pos,button):
    #reset to normal condition
    duplicate = False
    
    #placing Obstacles
    if button == mouse.LEFT:
        if place_block:
            Ob=Actor("block")
    #         Ob.x= (100 * round(pos[0]/100)) +50 +(hintergrund.left - (100 *round(hintergrund.left /100)))
    #         Ob.y= (100 * round(pos[1]/100)) +50
            for i in range(len(Tiles)):
                if Tiles[i].collidepoint(pos):
                    Ob.left= Tiles[i].x
                    Ob.top= Tiles[i].y
                    
            #checking for duplicates
            for i in range(len(Obs)):
                if Ob.left == Obs[i].left and Ob.top== Obs[i].top:
                    duplicate =True
            if duplicate == False:
                Obs.append(Ob)
        
        if place_spike:
            Sp=Actor("spike")
    #         Sp.x= (100 * round(pos[0]/100)) +50 +(hintergrund.left - (100 *round(hintergrund.left /100)))
    #         Sp.y= (100 * round(pos[1]/100)) +50
            for i in range(len(Tiles)):
                if Tiles[i].collidepoint(pos):
                    Sp.left= Tiles[i].x
                    Sp.top= Tiles[i].y
                    
            #checking for duplicates
            for i in range(len(Obs)):
                if Sp.left == Obs[i].left and Sp.top== Obs[i].top:
                    duplicate =True
            if duplicate == False:
                Obs.append(Sp)
        
        
            
    
    #removing obstalces
    elif button == mouse.RIGHT:
        for i in range(len(Tiles)):
            if Tiles[i].collidepoint(pos):
                Search_x= Tiles[i].x
                Search_y= Tiles[i].y
        for i in range(len(Obs)):
            if Search_x == Obs[i].left and Search_y == Obs[i].top:
                Obs.remove(Obs[i])
                break

def save(level_id):
    
    level=[]
    
    #checking for obstacle placements and creating list of obstalce and respective coordinates
    
    for ob in Obs:
        data=[ob.image,(ob.left-hintergrund.left), ob.top]
        level.append(data)
    
    #creating or overwriting file with chosen lvl id
    with open(f'level{level_id}data.csv','w', newline='') as csvfile:
        data= csv.writer(csvfile)
        data.writerows(level)
    
    

def load(level_id):
    global Obs
    Obs.clear()
    
    with open(f'level{level_id}data.csv','r',newline='') as csvfile:
        data= csv.reader(csvfile)
        
        for row in data:
            ob=Actor(row[0])
            ob.left = float(row[1]) + hintergrund.left
            ob.top = float(row[2]) 
            
            Obs.append(ob)
    
    
    
    
        
        
        
    
    
    
    


pgzrun.go()