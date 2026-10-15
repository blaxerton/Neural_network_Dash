import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)

import pgzrun
import csv
import math
import random
import copy




TITLE="MA_Dash"
WIDTH=1200
HEIGHT=700

hintergrund=Actor("kfeld")
player=Actor("player")


BGs=[]
Obs=[]




for i in range(20):
    bild= Actor("kfeld")
    bild.left= WIDTH*i
    BGs.append(bild)
#game specific variables
current_level=3
speed= 19
gravity= 4

#player spcific variables(mostly no longer relevant)
# player.left=0
# player.bottom=HEIGHT
# jump_s= 50
# player.vy=0
# airborne = False
death=False
# player.hurtbar_ground=Rect((0,HEIGHT-1),(100,1))
# player.hurtbar_front=Rect((100,HEIGHT-99),(1,75))
# player.score=0


#NN variables
num_NN= 10
#number of generated NNs
Num_NN=2000

#hidden layer
h_layers= 5
h_layer_size=5

#input layer
i_layer_size=18

sizes=[h_layers,h_layer_size,i_layer_size]

#value to keep track of generation
generation=1

#lists for living and dead Neural networks
living=[]
dead=[]

def gen_NN(NN_count):
    global sizes
    global generation
    
    #list of Neural Networks
    NNs=[]
    
    for i in range(NN_count):
        NN=Actor("player")
        #variables for game interactability
        NN.left=0
        NN.bottom=HEIGHT
        NN.jump=50
        NN.score=0
        NN.vy=0
        NN.airborne=False
        NN.death=False
        NN.action=0
        NN.hurtbar_ground=Rect((0,HEIGHT-1),(99,2))
        NN.hurtbar_front=Rect((100,HEIGHT-99),(1,60))
        NN.sightbar_front=Rect((100,HEIGHT-50),(WIDTH-100,1))
        NN.sightbar_top=Rect((0,HEIGHT-170),(WIDTH-100,1))
        NN.sightbar_top1=Rect((0,HEIGHT-270),(WIDTH-100,1))
        NN.sightbar_top2=Rect((0,HEIGHT-370),(WIDTH-100,1))
        NN.sightbar_top3=Rect((0,HEIGHT-470),(WIDTH-100,1))
        NN.sightbar_bottom=Rect((150,HEIGHT+70),(WIDTH-100,1))
        NN.sightbar_bottom1=Rect((150,HEIGHT+170),(WIDTH-100,1))
        NN.sightbar_bottom2=Rect((150,HEIGHT+270),(WIDTH-100,1))
        NN.sightbar_bottom3=Rect((150,HEIGHT+370),(WIDTH-100,1))
        NN.inputs=[]
        
        #varaibles for the NN functionality
        #biases[neuron]
        NN.biases=[]
        for i in range(sizes[0]*sizes[1]+1):
            NN.biases.append(float(random.uniform(-2,2)))
            
        
        #weights[neurons][Weights]
        NN.weights=[]
        for i in range(sizes[0]*sizes[1]+1):
            values=[]
            if i < sizes[1]:
                for p in range(sizes[2]):
                    values.append(float(random.uniform(-2,2)))
            else:
                for p in range(sizes[1]):
                    values.append(float(random.uniform(-2,2)))
                
                    
                    
            NN.weights.append(values)
        NNs.append(NN)
    
                
    return NNs



#iteration function to compute the output of a Neural network
def iterate(NN,inputs):
    global sizes
    #saving the inputs in a list to be used in the function for the current values of the previus layer
    values=inputs
    
    #input layer
    #putting all inputs through the activation function
    for i in range(len(inputs)):
        values[i]= sigmoid(values[i])
    
    #hidden layers
    previous_values=values
    current_values=[]
    computing_values=[]
    
    for i in range(sizes[0]*sizes[1]+1):
        computing_values=[]
        #applying weights on the values of the previous layer and saving it in a list
        for p in range(len(NN.weights[i])):
            computing_values.append(previous_values[p]*NN.weights[i][p])
            
        
        output=sigmoid(sum(computing_values)+ NN.biases[i])
        current_values.append(output)
        if (i+1) % sizes[1]==0:
            previous_values = current_values
            current_values=[]
    #putting the outpout through a step function to get binary values
    output=sum(previous_values)+ NN.biases[sizes[0]*sizes[1]]
    if output >= 0.5:
        output=1
    else:
        output=0
    return output





#function for generating new child networks based off mutated parent networks
def mutate(parents,num_children):
    
    # variable for the likelyhood of a variable mutating
    mutation_rate=0.1
    
    #varaible for how strong mutations can affect a value
    mutation_strenght=0.5
    
    NNs=[]
    for i in range(num_children-1):
        NN = Actor("player")
        NN.left=0
        NN.bottom=HEIGHT
        NN.jump=50
        NN.score=0
        NN.vy=0
        NN.airborne=False
        NN.death=False
        NN.action=0
        NN.hurtbar_ground=Rect((0,HEIGHT-1),(99,2))
        NN.hurtbar_front=Rect((100,HEIGHT-99),(1,60))
        NN.sightbar_front=Rect((100,HEIGHT-50),(WIDTH-100,1))
        NN.sightbar_top=Rect((0,HEIGHT-170),(WIDTH-100,1))
        NN.sightbar_top1=Rect((0,HEIGHT-270),(WIDTH-100,1))
        NN.sightbar_top2=Rect((0,HEIGHT-370),(WIDTH-100,1))
        NN.sightbar_top3=Rect((0,HEIGHT-470),(WIDTH-100,1))
        NN.sightbar_bottom=Rect((150,HEIGHT+70),(WIDTH-100,1))
        NN.sightbar_bottom1=Rect((150,HEIGHT+170),(WIDTH-100,1))
        NN.sightbar_bottom2=Rect((150,HEIGHT+270),(WIDTH-100,1))
        NN.sightbar_bottom3=Rect((150,HEIGHT+370),(WIDTH-100,1))
        NN.inputs=[]
        
        #chosing a specific parent for the child
        parent_id=random.randrange(len(parents))
        
        #copying and mutating biases of random parent
        NN.biases=parents[parent_id].biases.copy()
        for i in range(len(NN.biases)):
            if random.random() < mutation_rate:
                NN.biases[i] += random.uniform(-1*mutation_strenght,mutation_strenght)
        
        #copying and mutating weights of random parent
        NN.weights=copy.deepcopy(parents[parent_id].weights)
        for i in range(len(NN.weights)):
            for p in range(len(NN.weights[i])):
                if random.random() < mutation_rate:
                    NN.weights[i][p] += random.uniform(-1*mutation_strenght,mutation_strenght)
                    
        NNs.append(NN)
    
    #preserving the best performing NN of the previous generation
    winner=Actor("player")
    winner.left=0
    winner.bottom=HEIGHT
    winner.jump=50
    winner.score=0
    winner.vy=0
    winner.airborne=False
    winner.death=False
    winner.action=0
    winner.hurtbar_ground=Rect((0,HEIGHT-1),(99,2))
    winner.hurtbar_front=Rect((100,HEIGHT-99),(1,60))
    winner.sightbar_front=Rect((100,HEIGHT-50),(WIDTH-100,1))
    winner.sightbar_top=Rect((0,HEIGHT-170),(WIDTH-100,1))
    winner.sightbar_top1=Rect((0,HEIGHT-270),(WIDTH-100,1))
    winner.sightbar_top2=Rect((0,HEIGHT-370),(WIDTH-100,1))
    winner.sightbar_top3=Rect((0,HEIGHT-470),(WIDTH-100,1))
    winner.sightbar_bottom=Rect((150,HEIGHT+70),(WIDTH-100,1))
    winner.sightbar_bottom1=Rect((150,HEIGHT+170),(WIDTH-100,1))
    winner.sightbar_bottom2=Rect((150,HEIGHT+270),(WIDTH-100,1))
    winner.sightbar_bottom3=Rect((150,HEIGHT+370),(WIDTH-100,1))
    winner.inputs=[]
    
    winner.biases=parents[0].biases.copy()
    winner.weights=copy.deepcopy(parents[0].weights)
    
    NNs.append(winner)
    
    return NNs
        
        



#defining activation function
def sigmoid(value):
    return 1/(1+math.exp(value*-1))

#loading function
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


def draw():
    global death
    global living
    #drawing backgrounds
    hintergrund.draw()
    for i in range(len(BGs)):
        BGs[i].draw()
    #drawing first NN in the list of living NNs
    if living !=[]:
        NNs[0].draw()
    
    
    #drawing obstacles
    for i in range(len(Obs)):
        Obs[i].draw()
        
   
    


def update():
    global airborne
    global death
    global speed
    global living
    global dead
    global NNs
    global generation
    
    
    #checking if some NNs are still alive and if a new generation should be started
    if living != []:
        
        for i in range (len(dead)):
            if dead[i] in living:
                living.remove(dead[i])
            else:
                pass
        #raycasting to get distance to nearest object 
        for NN in NNs:
            #defining input variables
            distance_f= WIDTH-100
            distance_t= WIDTH-100
            distance_t1= WIDTH-100
            distance_t2= WIDTH-100
            distance_t3= WIDTH-100
            distance_b= WIDTH-100
            distance_b1=WIDTH-100
            distance_b2=WIDTH-100
            distance_b3=WIDTH-100
            type_f=0
            type_t=0
            type_t1=0
            type_t2=0
            type_t3=0
            type_b=0
            type_b1=0
            type_b2=0
            type_b3=0
            nearest_f=None
            nearest_t=None
            nearest_t1=None
            nearest_t2=None
            nearest_t3=None
            nearest_b=None
            nearest_b1=None
            nearest_b2=None
            nearest_b3=None
            
            #checking for distance and obstacly type then updating input variables
            for ob in Obs:
                if NN.sightbar_front.colliderect(ob._rect):
                    if ob.x - NN.x < distance_f:
                        distance_f=ob.x - NN.x
                        nearest_f= ob
                    else:
                        type_f=0
                        
                if NN.sightbar_top.colliderect(ob._rect):
                    if ob.x - NN.x < distance_t:
                        distance_t=ob.x -NN.x
                        nearest_t=ob
                    else:
                        type_t=0
                if NN.sightbar_top1.colliderect(ob._rect):
                    if ob.x - NN.x < distance_t1:
                        distance_t1=ob.x -NN.x
                        nearest_t1=ob
                    else:
                        type_t1=0
                if NN.sightbar_top2.colliderect(ob._rect):
                    if ob.x - NN.x < distance_t2:
                        distance_t2=ob.x -NN.x
                        nearest_t2=ob
                    else:
                        type_t2=0
                if NN.sightbar_top3.colliderect(ob._rect):
                    if ob.x - NN.x < distance_t3:
                        distance_t3=ob.x -NN.x
                        nearest_t3=ob
                    else:
                        type_t3=0
                        
                if NN.sightbar_bottom.colliderect(ob._rect):
                    if ob.x - NN.x < distance_b:
                        distance_b= ob.x -NN.x
                        nearest_b = ob
                    else:
                        type_b=0
                
                if NN.sightbar_bottom1.colliderect(ob._rect):
                    if ob.x - NN.x < distance_b1:
                        distance_b1=ob.x -NN.x
                        nearest_b1= ob
                    else:
                        type_b1=0
                
                if NN.sightbar_bottom2.colliderect(ob._rect):
                    if ob.x - NN.x < distance_b2:
                        distance_b2=ob.x -NN.x
                        nearest_b2= ob
                    else:
                        type_b2=0
                
                if NN.sightbar_bottom3.colliderect(ob._rect):
                    if ob.x - NN.x < distance_b3:
                        distance_b3=ob.x -NN.x
                        nearest_b3= ob
                    else:
                        type_b3=0
            
            if nearest_f != None:
                if nearest_f.image =="block":
                    type_f=0.5
                elif nearest_f.image=="spike":
                    type_f=1
            if nearest_t !=None:
                if nearest_t.image =="block":
                    type_t=0.5
                elif nearest_t.image =="spike":
                    type_t=1
            if nearest_t1 !=None:
                if nearest_t1.image =="block":
                    type_t1=0.5
                elif nearest_t1.image =="spike":
                    type_t1=1
            if nearest_t2 !=None:
                if nearest_t2.image =="block":
                    type_t2=0.5
                elif nearest_t2.image =="spike":
                    type_t2=1
            if nearest_t3 !=None:
                if nearest_t3.image =="block":
                    type_t3=0.5
                elif nearest_t3.image =="spike":
                    type_t3=1
            if nearest_b !=None:
                if nearest_b.image=="block":
                    type_b=0.5
                elif nearest_b.image=="spike":
                    type_b=1
            if nearest_b1 !=None:
                if nearest_b1.image=="block":
                    type_b1=0.5
                elif nearest_b1.image=="spike":
                    type_b1=1
            if nearest_b2 !=None:
                if nearest_b2.image=="block":
                    type_b2=0.5
                elif nearest_b2.image=="spike":
                    type_b2=1
            if nearest_b3 !=None:
                if nearest_b3.image=="block":
                    type_b3=0.5
                elif nearest_b3.image=="spike":
                    type_b3=1
                        

                
            # scaling down the inputs for the distance
            #putting inputs into a list
            NN.inputs=[distance_f/220, type_f, distance_t/220, type_t, distance_t1/220, type_t1, distance_t2/220, type_t2, distance_t3/220, type_t3, distance_b/220, type_b, distance_b1/220, type_b1, distance_b2/220, type_b2, distance_b3/220, type_b3]


            
        
        #computing output values for each Neural Network
        for NN in NNs:
            NN.action=iterate(NN,NN.inputs)
            
        
        #making the level move towards the player
        hintergrund.x -=speed
        for B in BGs:
            B.x -=speed
        
        for O in Obs:
            O.x -= speed
        #looping thorough the NNs in for the pyhsics simulations
        for NN in NNs:
            if NN.death is not True:
                #increasing NN score if it hasnt died
                NN.score += 1
                #saving NN bottom before moving it for collision calculations
                previous_bottom=NN.bottom
                
                #applying the players speed to its position
                NN.y -= NN.vy
                
                #keeping the player on the ground when he touches the ground
                if NN.bottom >= HEIGHT:
                    NN.airborne=False
                    NN.bottom = HEIGHT
                
                #applying gravity on the player if he is airborne
                if NN.airborne:
                    gravity = 5
                    NN.vy -= gravity
                elif NN.airborne == False:
                    NN.vy = 0
                    gravity = 0
                
                #increasing vertical momentum when jumping putting airborne to true
                if NN.action ==1 and NN.airborne== False:
                    NN.vy += NN.jump
                    NN.airborne=True
                    
                #updating player hurtboxes
                NN.hurtbar_ground.bottom=NN.bottom
                NN.hurtbar_ground.left=NN.left
                
                NN.hurtbar_front.top=NN.top
                NN.hurtbar_front.right=NN.right
                
                #updating player sightbars
                NN.sightbar_front.y = NN.y
                NN.sightbar_top.y = NN.y - 120
                NN.sightbar_bottom.y = NN.y + 120
                NN.sightbar_bottom1.y = NN.y + 220
                NN.sightbar_bottom2.y = NN.y + 320
                NN.sightbar_bottom3.y = NN.y + 420

                #checking for collision with obstacles
                for O in Obs:
                    landed=False
                    if O.image == "spike" and NN.colliderect(O._rect):
                        NN.death =True
                        break
                    if O.image =="block" and NN.hurtbar_front.colliderect(O._rect) and previous_bottom <= O.top:
                        landed=True
                        NN.vy=0
                        NN.bottom=O.top
                        break
                    elif O.image =="block" and NN.hurtbar_front.colliderect(O._rect) and previous_bottom >= O.top:
                        NN.death=True
                        break
                    if O.image =="block" and NN.hurtbar_ground.colliderect(O._rect) and previous_bottom <= O.top:
                        NN.vy=0
                        NN.bottom=O.top
                        landed=True
                        break
                #setting airborne to true if player landed on none of the blocks
                if not landed and NN.bottom!= 0:
                    NN.airborne=True
                else:
                    NN.airborne=False
                        
                    
            else:
                #putting the dead NNs into a list for chosing the longest living NN later
                dead.append(NN)
            
    else:
        #selecting some of the fittest NNs for mutation
        parents=[]
        for i in range (int(Num_NN/10)):
            parents.append(dead[len(dead)-i-1])
            
        #appending average of parents to a csv file
        sum_scores=0
        for i in range(len(parents)):
            sum_scores+=parents[i].score
        
        parent_avg=["Generation "+str(generation),sum_scores/len(parents)]
        
        with open("Test_scores_16.csv","a",newline="") as f:
            writer_obj=csv.writer(f)
            writer_obj.writerow(parent_avg)
            
        #start of next generation   
        NNs=mutate(parents,Num_NN)
        living=NNs
        generation += 1
        
        
        
        
        #reseting level back to startposition
        for bild in BGs:
            bild.x -= hintergrund.left
        for ob in Obs:
            ob.x -= hintergrund.left
        hintergrund.left=0
        
        dead=[]

#loading training level and initiating first generation
load(current_level)
NNs=gen_NN(Num_NN)
living=NNs

pgzrun.go()
    
    
