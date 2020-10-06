'''Ray Liu
   June 8th 2011
   This game, MEGA BALL!, is playing using joystick. In the game, user controls a ball to go through 5 stages (those stages are full of thorns, obstacle, cannonball, traps etc.). There's also a hidden path in the game. The user would eventually encounter the boss at stage 5. After defeating the boss, user would be evaluated according to how long do they finish the game and the amount of remaining health'''

#Import and Initialize
import pygame,random,Sprites
pygame.init()
pygame.mixer.init()

#set the resolution to 640*480
screen=pygame.display.set_mode((640,480))

#Create a list of Joystick objects
joysticks = []
for joystick_no in range(pygame.joystick.get_count()):
    stick = pygame.joystick.Joystick(joystick_no)
    stick.init()
    joysticks.append(stick)

#body part of the program
def main():
    
    #Display
    #title the game 'MEGA BALL!'
    pygame.display.set_caption('MEGA BALL!')
    
    #Entities
    #create background and blit it
    background=pygame.Surface(screen.get_size())
    background=background.convert()
    screen.blit(background,(0,0))
    
    #create a dynamic background
    pic=Sprites.Background()
    picSprite=pygame.sprite.Group(pic)
    
    #create basic map that contains only walls (wall sprite)
    wall=[]
    for set_wall in range(9):
        if set_wall==0:
            wall+=[],
            for _ in range(4):
                wall[set_wall]+=[Sprites.Wall('0')]
        elif set_wall==4:
            wall+=[],
            for bottomwall in range(10):
                wall[set_wall]+=[Sprites.Wall('4-'+repr(bottomwall))]
        elif set_wall==6:
            wall+=[],
            wall[set_wall]+=[Sprites.Wall('6-0')]
            wall[set_wall]+=[Sprites.Wall('6-1')]
        else:
            wall+=[Sprites.Wall(repr(set_wall))]
    
    wall[1].left_bottom((0,80))
    wall[0][0].left_top((0,400))
    wall[2].left_top((wall[0][0].rect.right,wall[0][0].rect.top))
    wall[3].right_top((wall[1].rect.right,wall[2].rect.bottom+300))
    wall[0][1].left_bottom((wall[3].rect.right,wall[3].rect.bottom))
    wall[4][0].left_top((wall[3].rect.left,wall[3].rect.bottom+300))
    wall_4_space=[[Sprites.Surface((wall[4][0].rect.centerx,wall[4][0].rect.centery-1),wall[4][0].rect.left,wall[4][0].rect.right,76,wall[4][0].rect.bottom-wall[4][0].rect.top,0)],False]
    for set_wall in range(1,9):
        wall[4][set_wall].left_top((wall[4][set_wall-1].rect.right+1,wall[4][set_wall-1].rect.top))
        wall_4_space[0]+=[Sprites.Surface((wall[4][set_wall].rect.centerx,wall[4][set_wall].rect.centery-1),wall[4][set_wall].rect.left,wall[4][set_wall].rect.right,80,wall[4][set_wall].rect.bottom-wall[4][set_wall].rect.top,0)]
    wall_4=pygame.sprite.Group(wall[4])    
        
    wall[0][2].left_top((wall[4][8].rect.right,wall[4][8].rect.top-480))
    wall[6][0].left_top((wall[0][2].rect.right,wall[0][2].rect.top))
    wall[6][1].left_bottom((wall[6][0].rect.right+100,wall[6][0].rect.bottom))
    wall[5].right_bottom((wall[6][1].rect.right,wall[6][1].rect.top+17))
    wall[4][9].left_top((wall[0][2].rect.right,wall[4][8].rect.top))
    wall[0][3].left_bottom((wall[4][9].rect.right,wall[4][9].rect.bottom))
    wall[8].left_bottom((wall[5].rect.left,wall[5].rect.top-70))
    wall[7].left_bottom((wall[0][1].rect.right,wall[8].rect.top+81))
    
    #scene_change(surface sprite) contains a line of an area that determine the shift between scenes (like endzone)
    scene_change=[None,Sprites.Surface(((2200+wall[2].rect.right+40)/2,wall[2].rect.top-1),wall[2].rect.right+40,2200,0,1,0)]
    scene_change+=[[Sprites.Surface((wall[2].rect.right,(1300+1365)/2),1300,1365,0,1,1),Sprites.Surface(((wall[0][0].rect.right+415)/2,1550),wall[0][0].rect.right,415,50,1,0)],0]
    scene_change+=[[Sprites.Surface((wall[0][1].rect.centerx,wall[0][1].rect.bottom+1),wall[0][1].rect.left,wall[0][1].rect.right,24,1,0),Sprites.Surface(((wall[5].rect.left+wall[0][1].rect.right)/2,wall[5].rect.bottom),wall[0][1].rect.right,wall[5].rect.left,0,1,0),Sprites.Surface((2779,(wall[5].rect.bottom+wall[0][2].rect.top)/2),wall[5].rect.bottom,wall[0][2].rect.top,0,1,1),Sprites.Surface((2437,(wall[5].rect.top+wall[8].rect.bottom)/2),wall[8].rect.bottom,wall[5].rect.top,0,1,1),Sprites.Surface(((wall[5].rect.right+wall[0][3].rect.left+20)/2,wall[5].rect.top-1),wall[5].rect.right,wall[0][3].rect.left+10,76,1,0),Sprites.Surface(((wall[6][1].rect.right+wall[0][3].rect.left+20)/2,wall[6][1].rect.bottom+38),wall[6][1].rect.right,wall[0][3].rect.left+10,0,1,0),Sprites.Surface(((2437+wall[5].rect.right)/2,wall[5].rect.bottom),2437,wall[5].rect.right,0,1,0)]]
    scene_change+=[[Sprites.Surface(((wall[6][0].rect.right+wall[6][1].rect.left)/2,wall[6][0].rect.top-1),wall[6][0].rect.right,wall[6][1].rect.left,76,1,0),Sprites.Surface(((wall[6][0].rect.right+wall[6][1].rect.left)/2,wall[6][0].rect.bottom+38),wall[6][0].rect.right,wall[6][1].rect.left,0,1,0)]]
        
    #group wall and scene_chang together
    wallSprite=pygame.sprite.OrderedUpdates(wall[0],wall[1],wall[2],wall[3],wall[4],wall[5],wall[6],wall[7],wall[8],scene_change[1],scene_change[2],scene_change[4],scene_change[5],wall_4_space[0])
    
    #create obstacle (wall sprite) in stage 1 and surfaces (surface sprite) that determine which side does the obstacle collide with the ball
    obstacle=[[],[]]
    surface=[[],[]]
    
    obstacle_value=[['10-0',658],['10-1',713],['11-0',956],['10-1',1066],['11-4',1207],['10-3',1317],['10-2',1372],['10-1',1427],['10-0',1482]]
    for set_obstacle in range(len(obstacle_value)):
        obstacle[0]+=[Sprites.Wall(obstacle_value[set_obstacle][0])]
        obstacle[0][set_obstacle].left_bottom((obstacle_value[set_obstacle][1],wall[2].rect.top))
        surface[0]+=[[Sprites.Surface((obstacle[0][set_obstacle].rect.centerx,obstacle[0][set_obstacle].rect.top-1),obstacle[0][set_obstacle].rect.left,obstacle[0][set_obstacle].rect.right,24,1,0),Sprites.Surface((obstacle[0][set_obstacle].rect.left-50,obstacle[0][set_obstacle].rect.centery),obstacle[0][set_obstacle].rect.top,obstacle[0][set_obstacle].rect.bottom,0,50,1)]]
        
    obstacle_value=[['10-1',803],['10-2',858],['10-1',913],['10-0',968],['10-0',1462],['10-1',1517],['10-2',1572],['10-3',1627]]
    for set_obstacle in range(len(obstacle_value)):
        obstacle[1]+=[Sprites.Wall(obstacle_value[set_obstacle][0])]
        obstacle[1][set_obstacle].left_top((obstacle_value[set_obstacle][1],wall[1].rect.bottom))
        surface[1]+=[[Sprites.Surface((obstacle[1][set_obstacle].rect.centerx,obstacle[1][set_obstacle].rect.bottom+1),obstacle[1][set_obstacle].rect.left,obstacle[1][set_obstacle].rect.right,24,1,0),Sprites.Surface((obstacle[1][set_obstacle].rect.left-50,obstacle[1][set_obstacle].rect.centery),obstacle[1][set_obstacle].rect.top,obstacle[1][set_obstacle].rect.bottom,0,50,1)]]
        
    #group obstacle and surface together
    obstacleSprite=pygame.sprite.OrderedUpdates(obstacle[0],surface[0],obstacle[1],surface[1])
    
    #create the ball(ball sprite) controlled by the user and 5 other ball (ballshadows sprite) that appear when the ball reaches a certain speed
    #In ball list, first index is sprite, second index controls whether ballshadows appear, third index determines whether the ball is moving on the ground, fourth index controls explosion of the ball, fifth index determines the period of time the ball becomes invincible after it's attacked
    for set_ball in range(6):
        if set_ball==0:
            ball=[[Sprites.Ball(),False,0,False,0]]
        else:
            #first index of ball shadows is sprite, second index works as the second index of the ball
            ball+=[[Sprites.BallShadow(set_ball,ball[set_ball-1][0].ballnumber()),ball[set_ball-1][1]]]
    
    #group only the ball controlled by user
    ballSprite=pygame.sprite.Group(ball[0][0])
    
    #create the boss, which is a UFO
    UFO=[Sprites.UFO(),-1,0,0]
    #group only the boss
    UFOSprite=pygame.sprite.Group(UFO[0])
    
    #create a menu sprite
    menu=Sprites.Menu()
    
    #create a list of label sprites that appear in menu and evaluation
    label=[Sprites.Label('Play',(410,220),40,(255,255,255)),Sprites.Label('Instruction',(410,270),40,(255,255,255)),Sprites.Label('Back to Menu',(320,440),25,(255,255,255)),Sprites.Label('Press Space to continue/any other key to exit',(320,200),25,(255,153,0))]
    #group menu sprite and corresponding label sprite
    menuSprite=pygame.sprite.OrderedUpdates(menu,label[0],label[1])
    
    #location dictates where most sprites in this game display, first index controls x-axis, second index controls y-axis, the third index works similarly to stage
    location=[0,0,0]
    #stage indicates how much the user has passed
    stage=1
    #time is used to count the time of dash (index one), and a certain period that the ball cannot dash (index two), and the time that has passed(index three)
    time=[0,0,0]
    #timelabel shows the time that has passed on the top right corner of the screen
    timelabel=Sprites.Label('',(600,30),30,(255,255,0))
    #group time label
    timeSprite=pygame.sprite.Group(timelabel)
    #move dictates the change in variable 'location' and the ball sprite, first index controls x-axis, second index control y-axis
    move=[0,0]
    #it represents the direction controlled by joystick, first index controls the horizontaol move, second index controls the vertical move, third index only works when the ball touches the ground
    direction=[0,0,0]
    #a list that groups all ballshadows when the ball reaches a certain amount of speed
    ballshadow=pygame.sprite.Group()
    #a technique that fix the bug that screen shakes when the ball bounces too frequently
    bound=[[260,240],[380,400],0,[280,260],[360,380],[200,0],[280,480]]
    #shake list is used to implement the effect of shake in stage 5
    shake=[0,-55,0]
    #one attack is a thorn sprite that kills the boss when touches it, but it can only be found in hidden path
    oneattack=None
    #the first index in position determines where the mouse locates, second dindex ends the menu when becomes True
    position=[(0,0),False]
    
    #create sound effects
    click=pygame.mixer.Sound('click.wav')
    click.set_volume(0.5)
    dash=pygame.mixer.Sound('dash.wav')
    dash.set_volume(0.5)
    hit=pygame.mixer.Sound('hit.wav')
    hit.set_volume(0.5)
    shakes=pygame.mixer.Sound('shakes.wav')
    shakes.set_volume(0.5)
    fires=pygame.mixer.Sound('fires.wav')
    fires.set_volume(0.5)
    shoot=pygame.mixer.Sound('shoot.wav')
    shoot.set_volume(0.5)
    explosions=pygame.mixer.Sound('explosions.wav')
    explosions.set_volume(0.5)
    UFOexplosions=pygame.mixer.Sound('UFOexplosions.wav')
    UFOexplosions.set_volume(0.5)
    
    #play the first background music
    pygame.mixer.music.load('menu.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
    #sets a variable for frame rate
    x=30
    
    #Assign
    #Action
    clock=pygame.time.Clock()
    keepGoing=True
    
    #Loop 1 (menu)
    while keepGoing:
        
        #Time
        clock.tick(30)
        
        #Event Handling for choices on the menu
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                keepGoing = False    
            elif event.type == pygame.MOUSEMOTION:
                position = [pygame.mouse.get_pos(),False]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                #change menu sprite if the user chooses one of the options
                for set_label in range(len(label)):
                    if position[0][0]<=label[set_label].rect.right and position[0][0]>=label[set_label].rect.left and position[0][1]>=label[set_label].rect.top and position[0][1]<=label[set_label].rect.bottom:
                        click.play()
                        if set_label==0:
                            position[1]=True
                        elif set_label==1:
                            menu.instruction()
                            menuSprite=pygame.sprite.OrderedUpdates(menu,label[2])
                        elif set_label==2:
                            menu.menu()
                            menuSprite=pygame.sprite.OrderedUpdates(menu,label[0],label[1])
        
        #Exit when user chooses to start the game
        #start to play background music for stage 1
        if position[1]:
            pygame.mixer.music.load('stage1.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            break
        
        #change the color of font when mouse stays on the label
        for set_label in range(len(label)):
            if position[0][0]<=label[set_label].rect.right and position[0][0]>=label[set_label].rect.left and position[0][1]>=label[set_label].rect.top and position[0][1]<=label[set_label].rect.bottom:
                label[set_label].colorchange((0,102,102))
            else:
                label[set_label].colorchange((255,255,255))
        
        #Refresh Screen
        menuSprite.update()
        menuSprite.draw(screen)
        pygame.display.flip()
        menuSprite.clear(screen,background)
    
    #Loop 2 (body of the game)
    while keepGoing:
        
        #Time, with a variable frame rate
        clock.tick(x)
        
        #ballshadows inherit the value of location from the ball so they follow the ball
        for set_ball in range(5,0,-1):
            ball[set_ball][0].rect.center=ball[set_ball-1][0].rect.center
            ball[set_ball][1]=ball[set_ball-1][1]
        
        #change the location of the ball
        ball[0][0].rect.centerx+=move[0]
        ball[0][0].rect.centery-=move[1]
        if ball[0][0].rect.left<0:
            ball[0][0].rect.left=0
        
        #determine if there should be ballshadows according to the speed of the ball
        if move[0]**2+move[1]**2>350:
            ball[0][1]=True
        else:
            ball[0][1]=False
        
        #coutnt the time that has passed
        time[2]+=1.0/x
        
        #Event Handling for the ball
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.JOYHATMOTION:
                direction=[event.value[0],event.value[1],direction[2]]
            elif event.type == pygame.JOYBUTTONDOWN: 
                if not time[1] and event.button==1:
                    time[0]=5
                    dash.play()
            elif event.type == pygame.JOYBUTTONUP:
                if time[0] and event.button==1:
                    direction[2]=0
                    time[0]=0
                    time[1]=5
        
        #increse the frame rate as well as the speed of the ball as it is dashing
        #the ball can move in 8 different directions
        if time[0]:
            x=45
            if direction[2]:
                if move[0]:
                    move[0]+=direction[0]*2
                    move[1]+=2.1
                else:
                    move[1]+=2.3
            elif direction[0]<>0 and direction[1]<>0:
                move[0]+=direction[0]*7
                if direction[1]<0 and not ball[0][2]:
                    move[1]+=direction[1]*10
                elif direction[1]<0 and ball[0][2]:
                    move[1]+=15
                    direction[2]=1
                elif move[1]<0:
                    move[1]/=2
            elif direction[0]<>0:
                move[0]+=10*direction[0]
                if move[1]<-2:
                    move[1]+=2
            elif direction[1]<>0:
                if direction[1]<0 and not ball[0][2]:
                    move[1]+=direction[1]*15
                elif direction[1]<0 and ball[0][2]:
                    move[1]+=15
                    direction[2]=1
                elif move[1]<0:
                    move[1]/=2
            time[0]-=1
            if move[0]>30:
                move[0]=50
            elif move[0]<-30:
                move[0]=-50
            if time[0]==0:
                time[1]=5

        #set the speed and frame rate back to normal when the ball is not dashing
        #ball can move in 5 directions (west to south to east)
        else:
            x=30
            direction[2]=0
            if direction[1]<>0:
                move[0]+=direction[0]*1
                if direction[1]<0 and not ball[0][2]:
                    move[1]+=direction[1]*1
                elif direction[1]>1 and not ball[0][2]:
                    if move[1]<0:
                        move[1]=move[1]*9/10
            if move[0]>0:
                move[0]=move[0]*9/10
            elif move[0]<0:
                move[0]=move[0]*9/10+0.05
            if direction[0]<>0:
                move[0]+=direction[0]*1.005
            if time[1]>0:
                time[1]-=1
        
        #limit the falling speed of the ball
        if move[1]<-50:
            move[1]=-50
            
        #determine if the ball is moving on the ground
        if move[1]<>0:
            ball[0][2]=0
        
        #if the horziontal speed of the ball is greater than one, chanage the image of the ball so it looks like rolling
        if move[0]<-1 or move[0]>1:
            ball[0][0].change_picture()
            for set_ball in range(1,6):
                ball[set_ball][0].change_picture(ball[set_ball-1][0].ballnumber())
        
        #stage 1
        if stage==1:
            #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball and walls
            if not ball[0][2]:
                move[1]-=1.2
                
                if ball[0][0].rect.colliderect(wall[2].rect) or ball[0][0].rect.colliderect(wall[0][0].rect):
                    hit.play()
                    if move[1]>=-8 and move[1]<0:
                        ball[0][2]=1
                        move[1]=0
                    else:
                        move[1]=-move[1]*5/9
                        direction[2]=True
                    ball[0][0].rect.bottom=wall[2].rect.top
                elif ball[0][0].rect.colliderect(wall[1].rect):
                    hit.play()
                    ball[0][0].rect.top=wall[1].rect.bottom+1
                    move[1]=-move[1]
                elif ball[0][0].rect.colliderect(wall[0][1].rect):
                    hit.play()
                    ball[0][0].rect.right=wall[0][1].rect.left
                    move[0]=-move[0]*5/9
            
            #determine if ball stays on the top of obstacles
            if ball[0][2]==2:
                for types in range(len(surface[0])):
                    if ball[0][0].rect.colliderect(surface[0][types][0].rect):
                        ball[0][2]=2
                        break
                    ball[0][2]=0
                    
            #determien the collision between ball and obstacles    
            bound[2]=0
            for types in range(len(obstacle)):
                for collision in range(len(obstacle[types])):
                    if ball[0][0].rect.colliderect(obstacle[types][collision].rect):
                        hit.play()
                        if types==0 and ball[0][0].rect.colliderect(surface[types][collision][0].rect) and ball[2][0].rect.bottom<=obstacle[types][collision].rect.top:
                            if move[1]>=-8 and move[1]<0:
                                ball[0][2]=2
                                move[1]=0
                            elif move[1]<0:
                                move[1]=-move[1]*5/9
                                direction[2]=True
                            ball[0][0].rect.bottom=obstacle[types][collision].rect.top
                        
                        elif types==1 and ball[0][0].rect.colliderect(surface[types][collision][0].rect) and ball[2][0].rect.top>=obstacle[types][collision].rect.bottom:
                            ball[0][0].rect.top=obstacle[types][collision].rect.bottom+1
                            if move[1]>0:
                                move[1]=-move[1]
                        else:
                            bound[2]=1
                            
                            if ball[0][0].rect.colliderect(surface[types][collision][1].rect) or ball[1][0].rect.colliderect(surface[types][collision][1].rect) or ball[2][0].rect.colliderect(surface[types][collision][1].rect):
                                ball[0][0].rect.right=obstacle[types][collision].rect.left
                                if move[0]>0:
                                    move[0]=-move[0]
                            else:
                                ball[0][0].rect.left=obstacle[types][collision].rect.right
                                if move[0]<0:
                                    move[0]=-move[0]
                            move[0]=move[0]*5/9
            
            #shift the scene to 1.5
            if ball[0][0].rect.colliderect(scene_change[1].rect):
                stage=1.5
                ball[0][2]=0
        
        #stage 1.5
        if stage==1.5:
            move[1]-=1.2
            
            #determine the collision between ball and side walls
            if ball[0][0].rect.colliderect(wall[2].rect):
                hit.play()
                ball[0][0].rect.left=wall[2].rect.right
                if move[0]<0:
                    move[0]=-move[0]
                move[0]=move[0]*5/9
            if ball[0][0].rect.colliderect(wall[0][1].rect):
                hit.play()
                ball[0][0].rect.right=wall[0][1].rect.left
                move[0]=-move[0]*5/9
                
            #shift stage to 2 and create obstacles (wall sprite), surfaces (surface sprite), thorn(thorn sprite) in stage 2
            if location[1]>1300-240:
                stage=2
                
                obstacle=[[],[]]
                surface=[[],[]]
                
                obstacle_value=[['11-4',1788],['11-1',1550],['11-3',1312],['12-0',1050],['10-4',995],['12-0',580],['12-3',415]]
                for set_obstacle in range(len(obstacle_value)):
                    obstacle[0]+=[Sprites.Wall(obstacle_value[set_obstacle][0])]
                    obstacle[0][set_obstacle].left_bottom((obstacle_value[set_obstacle][1],wall[3].rect.top+location[1]+1))
                    surface[0]+=[[Sprites.Surface((obstacle[0][set_obstacle].rect.centerx,obstacle[0][set_obstacle].rect.top-1),obstacle[0][set_obstacle].rect.left,obstacle[0][set_obstacle].rect.right,24,1,0),Sprites.Surface((obstacle[0][set_obstacle].rect.left-50,obstacle[0][set_obstacle].rect.centery),obstacle[0][set_obstacle].rect.top,obstacle[0][set_obstacle].rect.bottom,0,50,1)]]
                    
                obstacle_value=[['10-4',1160],['10-3',782],['12-0',415]]
                for set_obstacle in range(len(obstacle_value)):
                    obstacle[1]+=[Sprites.Wall(obstacle_value[set_obstacle][0])]
                    obstacle[1][set_obstacle].left_top((obstacle_value[set_obstacle][1],wall[2].rect.bottom+location[1]-47))
                    surface[1]+=[[Sprites.Surface((obstacle[1][set_obstacle].rect.centerx,obstacle[1][set_obstacle].rect.bottom+1),obstacle[1][set_obstacle].rect.left,obstacle[1][set_obstacle].rect.right,24,1,0),Sprites.Surface((obstacle[1][set_obstacle].rect.left-50,obstacle[1][set_obstacle].rect.centery),obstacle[1][set_obstacle].rect.top,obstacle[1][set_obstacle].rect.bottom,0,50,1)]]
                    
                thorn_value=[['1-1',((obstacle[0][0].rect.left-obstacle[0][1].rect.right)/3+obstacle[0][1].rect.right,wall[3].rect.top-13+location[1]+1)]]
                for set_thorn_value in range(1,3):
                    thorn_value+=[['1-1',((obstacle[0][1].rect.left-obstacle[0][2].rect.right)/3*set_thorn_value+obstacle[0][2].rect.right,wall[3].rect.top-13+location[1]+1)]]
                thorn_value+=[['1-1',((obstacle[0][2].rect.left-obstacle[0][3].rect.right)/2+obstacle[0][3].rect.right,wall[3].rect.top-13+location[1]+1)]]
                for set_thorn_value in range(7):
                    thorn_value+=[['1-0',(obstacle[0][4].rect.left-13,(obstacle[0][4].rect.top-obstacle[0][4].rect.bottom+20)/7*set_thorn_value+obstacle[0][4].rect.bottom-30)]]
                for set_thorn_value in range(5):
                    thorn_value+=[['1-2',(obstacle[1][1].rect.right+13,(wall[2].rect.bottom+location[1]+1-obstacle[1][1].rect.bottom)/5*set_thorn_value+obstacle[1][1].rect.bottom-9)]]
                for set_thorn_value in range(1,4,2):
                    thorn_value+=[['1-3',((obstacle[1][1].rect.right-obstacle[1][1].rect.left)/4*set_thorn_value+obstacle[1][1].rect.left,obstacle[1][1].rect.bottom+13)]]
                for set_thorn_value in range(1,6):
                    thorn_value+=[['1-1',((obstacle[0][4].rect.left-obstacle[0][5].rect.right)/6*set_thorn_value+obstacle[0][5].rect.right,wall[3].rect.top-13+location[1]+1)]]
                for set_thorn_value in range(3,5):
                    thorn_value+=[['1-2',(obstacle[0][6].rect.right+13,(obstacle[0][6].rect.top-obstacle[0][5].rect.top)/5*set_thorn_value+obstacle[0][5].rect.top-8)]]
                for set_thorn_value in range(6):
                    thorn_value+=[['1-3',((obstacle[1][2].rect.right-obstacle[1][2].rect.left+10)/6*set_thorn_value+obstacle[1][2].rect.left+10,obstacle[1][2].rect.bottom+13)]]
                    thorn_value+=[['1-1',((obstacle[0][6].rect.right-obstacle[0][6].rect.left+10)/6*set_thorn_value+obstacle[0][6].rect.left+10,obstacle[0][6].rect.top-13)]]
        
                thorn=[]
                for set_thorn in range(len(thorn_value)):
                    thorn+=[Sprites.Thorn(thorn_value[set_thorn][0],thorn_value[set_thorn][1])]
                thornSprite=pygame.sprite.Group(thorn)
                
                #group those sprites in obstalceSprite
                obstacleSprite=pygame.sprite.Group(obstacle[0],surface[0],obstacle[1],surface[1],thorn)
                
        #stage 2
        if stage==2:
            #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball and walls
            if not ball[0][2]:
                move[1]-=1.2
                
                if ball[0][0].rect.colliderect(wall[3].rect):
                    hit.play()
                    if move[1]>=-8 and move[1]<0:
                        ball[0][2]=1
                        move[1]=0
                    else:
                        move[1]=-move[1]*5/9
                        direction[2]=True
                    ball[0][0].rect.bottom=wall[3].rect.top
            
                elif ball[0][0].rect.colliderect(wall[2].rect):
                    if ball[0][0].rect.colliderect(scene_change[2][0].rect) and ball[2][0].rect.left>scene_change[2][0].rect.right:
                        hit.play()
                        location[0]-=ball[0][0].rect.left-wall[2].rect.right
                        ball[0][0].rect.left=wall[2].rect.right
                        if move[0]<0:
                            move[0]=-move[0]
                        move[0]=move[0]*5/9
                    else:
                        #if ball touches thorns hanging on the bottom of wall[2], it explodes
                        ball[0][3]=True
            if ball[0][0].rect.colliderect(wall[0][0].rect):
                hit.play()
                ball[0][0].rect.left=wall[0][0].rect.right
                move[0]=-move[0]*5/9        
            if ball[0][0].rect.colliderect(wall[0][1].rect):
                hit.play()
                move[0]=-move[0]*5/9
                ball[0][0].rect.right=wall[0][1].rect.left
        
            #determine if ball stays on the top of obstacles
            if ball[0][2]==2:
                for types in range(len(surface[0])):
                    if ball[0][0].rect.colliderect(surface[0][types][0].rect):
                        ball[0][2]=2
                        break
                    ball[0][2]=0
            
            #determien the collision between ball and obstacles
            bound[2]=0
            for types in range(len(obstacle)):
                for collision in range(len(obstacle[types])):
                    if ball[0][0].rect.colliderect(obstacle[types][collision].rect):
                        hit.play()
                        if types==0 and ball[0][0].rect.colliderect(surface[types][collision][0].rect) and ball[2][0].rect.bottom<=obstacle[types][collision].rect.top:
                            if move[1]>=-8 and move[1]<0:
                                ball[0][2]=2
                                move[1]=0
                            elif move[1]<0:
                                move[1]=-move[1]*5/9
                                direction[2]=True
                            ball[0][0].rect.bottom=obstacle[types][collision].rect.top
                        
                        elif types==1 and ball[0][0].rect.colliderect(surface[types][collision][0].rect) and ball[2][0].rect.top>=obstacle[types][collision].rect.bottom:
                            ball[0][0].rect.top=obstacle[types][collision].rect.bottom+1
                            if move[1]>0:
                                move[1]=-move[1]
                        else:
                            bound[2]=1
                            
                            if ball[0][0].rect.colliderect(surface[types][collision][1].rect) or ball[1][0].rect.colliderect(surface[types][collision][1].rect) or ball[2][0].rect.colliderect(surface[types][collision][1].rect):
                                ball[0][0].rect.right=obstacle[types][collision].rect.left
                                if move[0]>0:
                                    move[0]=-move[0]
                            else:
                                ball[0][0].rect.left=obstacle[types][collision].rect.right
                                if move[0]<0:
                                    move[0]=-move[0]
                            move[0]=move[0]*5/9
                          
            #if ball touches thorns, it explodes
            if pygame.sprite.spritecollide(ball[0][0],thornSprite,False):
                ball[0][3]=True
            
            #shift stage to 2.5
            if ball[0][0].rect.colliderect(scene_change[2][1]):
                stage=2.5
                
                #create cannonballs(cannonball sprite) in stage 3
                cannonball=[]
                cbSprite=pygame.sprite.Group()
                cannonball_value=[[543,1],[650,1],[759,1],[950,2],[1002,2],[1191,3],[1245,3],[1459,2],[1569,1],[1676,2],[1893,3],[2055,2],[2107,2],[2163,2]]
                for set_cannonball in range(len(cannonball_value)):
                    cannonball+=[[Sprites.Cannonball((cannonball_value[set_cannonball][0]+2,wall[3].rect.bottom+location[1]+40)),cannonball_value[set_cannonball][1],random.randint(8,14)]]
                    cbSprite.add(cannonball[set_cannonball][0])
        
        #stage 2.5
        if stage==2.5:
            #increase falling speed of the ball by 1.2
            move[1]-=1.2
            
            #determine collision between ball and all sides
            #the ball explodes when it touches thorns or drop out of the map
            if ball[0][0].rect.colliderect(wall[0][0].rect):
                hit.play()
                ball[0][0].rect.left=wall[0][0].rect.right
                move[0]=-move[0]*5/9
            if ball[0][0].rect.colliderect(wall[3].rect):
                ball[0][3]=True
            if ball[0][0].rect.colliderect(obstacle[0][6].rect):
                hit.play()
                ball[0][0].rect.right=obstacle[0][6].rect.left
                move[0]=-move[0]*5/9    
            if ball[0][0].rect.colliderect(wall[4][0].rect):
                ball[0][3]=True
            if ball[0][0].rect.centery>=480:
                ball[0][3]=True
            
            #set the movement of cannonball
            #3 kinds of cannonball (1. touch the bottom wall and disappear, 2. drop into holes, 3. bounce up when touch the bottom wall and bounce down when touch the top wall
            for set_cannonball in range(len(cannonball)):
                if cannonball[set_cannonball][1]==1:
                    if pygame.sprite.spritecollide(cannonball[set_cannonball][0],wall_4,False):
                        cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.bottom)
                        cannonball[set_cannonball][1]+=240
                    else:
                        cannonball[set_cannonball][0].change_location(cannonball[set_cannonball][2]*30/x)
                    
                elif cannonball[set_cannonball][1]==2:
                    if cannonball[set_cannonball][0].rect.centery>=520:
                        cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.bottom)
                        cannonball[set_cannonball][1]+=240
                    else:
                        cannonball[set_cannonball][0].change_location(cannonball[set_cannonball][2]*30/x)
                            
                elif cannonball[set_cannonball][1]==3:
                    if pygame.sprite.spritecollide(cannonball[set_cannonball][0],wall_4,False):
                        cannonball[set_cannonball][0].change_picture()
                        cannonball[set_cannonball][0].change_location(wall[4][0].rect.top-cannonball[set_cannonball][0].rect.bottom)
                        cannonball[set_cannonball][2]=-cannonball[set_cannonball][2]
                    elif cannonball[set_cannonball][0].rect.colliderect(wall[3].rect):
                        cannonball[set_cannonball][0].change_picture()
                        cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.top)
                        cannonball[set_cannonball][2]=-cannonball[set_cannonball][2]
                    else:
                        cannonball[set_cannonball][0].change_location(cannonball[set_cannonball][2]*30/x)

                else:
                    cannonball[set_cannonball][1]-=4    
            
            #shift scene to 3
            #load background music for stage 3
            if ball[0][0].rect.centerx+location[0]>415 and ball[0][0].rect.top>wall[3].rect.bottom:
                stage=3
                
                pygame.mixer.music.load('stage3.mp3')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                
                #set obstacles (wall sprite) and surface(surface sprite) in stage 3
                obstacle=[[],[]]
                surface=[[],[]]
                
                for set_obstacle in range(4):
                    obstacle[0]+=[Sprites.Wall('11-'+repr(3-set_obstacle))]
                    obstacle[0][set_obstacle].right_bottom((2779-110*set_obstacle,2506))
                    surface[0]+=[[Sprites.Surface((obstacle[0][set_obstacle].rect.centerx,obstacle[0][set_obstacle].rect.top-1),obstacle[0][set_obstacle].rect.left,obstacle[0][set_obstacle].rect.right,24,1,0),Sprites.Surface((obstacle[0][set_obstacle].rect.left-50,obstacle[0][set_obstacle].rect.centery),obstacle[0][set_obstacle].rect.top,obstacle[0][set_obstacle].rect.bottom,0,50,1)]]
                    
                obstacle[1]+=[Sprites.Wall('15-0'),Sprites.Wall('12-0'),Sprites.Wall('15-1'),Sprites.Wall('10-0'),Sprites.Wall('11-0'),Sprites.Wall('10-0'),Sprites.Wall('11-0')]
                obstacle[1][0].left_bottom((2261,2206))
                obstacle[1][1].left_top((2261,2025))
                obstacle[1][2].right_top((2779,2025))
                obstacle[1][3].left_bottom((2261,1907))
                obstacle[1][4].right_bottom((2437,1730))
                obstacle[1][5].left_bottom((2261,1561))
                obstacle[1][6].right_bottom((2437,1265))
                
                for set_surface in range(len(obstacle[1])):
                    surface[1]+=[[Sprites.Surface((obstacle[1][set_surface].rect.centerx,obstacle[1][set_surface].rect.top-1),obstacle[1][set_surface].rect.left,obstacle[1][set_surface].rect.right,24,1,0),Sprites.Surface((obstacle[1][set_surface].rect.centerx,obstacle[1][set_surface].rect.bottom+1),obstacle[1][set_surface].rect.left,obstacle[1][set_surface].rect.right,24,1,0)]]
                
                obstacleSprite=pygame.sprite.Group(obstacle[0],surface[0],obstacle[1],surface[1])
        
        #stage 3
        if stage==3:
            #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball and walls
            if location[2]>=2:
                if wall_4_space[1]:
                    move[1]-=1.2
                    if ball[0][0].rect.centery>=480:
                        ball[0][3]=True
                    
                elif not ball[0][2]:
                    move[1]-=1.2
                    
                    for collision in range(0,9,2):
                        if ball[0][0].rect.colliderect(wall[4][collision].rect):
                            hit.play()
                            if move[1]>=-8 and move[1]<0:
                                ball[0][2]=1
                                move[1]=0
                            else:
                                move[1]=-move[1]*5/9
                                direction[2]=True
                            ball[0][0].rect.bottom=wall[4][collision].rect.top
                            break
                    if ball[0][0].rect.colliderect(wall[3].rect) or ball[0][0].rect.colliderect(wall[0][1].rect):
                        hit.play()
                        ball[0][0].rect.top=wall[3].rect.bottom+1
                        move[1]=-move[1]
                
                #determine the collision between ball and obstacles
                bound[2]=0
                for set_drop in range(1,8,2):
                    if ball[0][0].rect.colliderect(wall_4_space[0][set_drop].rect) or ball[1][0].rect.colliderect(wall_4_space[0][set_drop].rect) or ball[2][0].rect.colliderect(wall_4_space[0][set_drop].rect):
                        wall_4_space[1]=True
                        bound[2]=1
                        
                        if ball[0][0].rect.colliderect(wall[4][set_drop-1].rect):
                            hit.play()
                            ball[0][0].rect.left=wall[4][set_drop-1].rect.right
                            if move[0]<0:
                                move[0]=-move[0]
                            move[0]=move[0]*5/9
                        elif ball[0][0].rect.colliderect(wall[4][set_drop+1].rect):
                            hit.play()
                            ball[0][0].rect.right=wall[4][set_drop+1].rect.left
                            if move[0]>0:
                                move[0]=-move[0]
                            move[0]=move[0]*5/9
                        break
                
                #Also determine the collision between ball and obstacles
                if ball[0][2]==2:
                    for types in range(len(surface[0])):
                        if ball[0][0].rect.colliderect(surface[0][types][0].rect):
                            ball[0][2]=2
                            break
                        ball[0][2]=0
                
                for collision in range(len(obstacle[0])):
                    if ball[0][0].rect.colliderect(obstacle[0][collision].rect):
                        hit.play()
                        if ball[0][0].rect.colliderect(surface[0][collision][0].rect) and ball[2][0].rect.bottom<=obstacle[0][collision].rect.top:
                            if move[1]>=-8 and move[1]<0:
                                ball[0][2]=2
                                move[1]=0
                            elif move[1]<0:
                                move[1]=-move[1]*5/9
                                direction[2]=True
                            ball[0][0].rect.bottom=obstacle[0][collision].rect.top
                        else:
                            bound[2]=1
                            ball[0][0].rect.right=obstacle[0][collision].rect.left
                            if move[0]>0:
                                move[0]=-move[0]
                if ball[0][0].rect.colliderect(obstacle[1][0]):
                    hit.play()
                    ball[0][0].rect.top=obstacle[1][0].rect.bottom+1
                    move[1]=-move[1]
                    
                #shift stage to 4
                if location[0]>=2200:
                    stage=4
                    
                    pygame.mixer.music.load('stage4.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)

            else:
                #there is an animation of stage shift between stage 3 and stage 2.5, speed of the ball is set to zero
                move=[0,0]
                if ball[0][0].rect.colliderect(wall[4][0].rect):
                    ball[0][0].rect.bottom=wall[4][0].rect.top
            
            #set the movement of cannonball
            for set_cannonball in range(len(cannonball)):
                if ball[0][0].rect.colliderect(cannonball[set_cannonball][0]):
                    ball[0][3]=True
                    cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.bottom)
                    cannonball[set_cannonball][1]+=240
                    break
                    
                if cannonball[set_cannonball][1]==1:
                    if pygame.sprite.spritecollide(cannonball[set_cannonball][0],wall_4,False):
                        cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.bottom)
                        cannonball[set_cannonball][1]+=240
                    else:
                        cannonball[set_cannonball][0].change_location(cannonball[set_cannonball][2]*30/x)
                    
                elif cannonball[set_cannonball][1]==2:
                    if cannonball[set_cannonball][0].rect.centery>=520:
                        cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.bottom)
                        cannonball[set_cannonball][1]+=240
                    else:
                        cannonball[set_cannonball][0].change_location(cannonball[set_cannonball][2]*30/x)
                            
                elif cannonball[set_cannonball][1]==3:
                    if pygame.sprite.spritecollide(cannonball[set_cannonball][0],wall_4,False):
                        cannonball[set_cannonball][0].change_picture()
                        cannonball[set_cannonball][0].change_location(wall[4][0].rect.top-cannonball[set_cannonball][0].rect.bottom)
                        cannonball[set_cannonball][2]=-cannonball[set_cannonball][2]
                    elif cannonball[set_cannonball][0].rect.colliderect(wall[3].rect):
                        cannonball[set_cannonball][0].change_picture()
                        cannonball[set_cannonball][0].change_location(wall[3].rect.bottom-cannonball[set_cannonball][0].rect.top)
                        cannonball[set_cannonball][2]=-cannonball[set_cannonball][2]
                    else:
                        cannonball[set_cannonball][0].change_location(cannonball[set_cannonball][2]*30/x)

                else:
                    cannonball[set_cannonball][1]-=4
                
                #if canonball can be seen in the screen, it will make sounds
                if cannonball[set_cannonball][0].rect.bottom>wall[3].rect.bottom and cannonball[set_cannonball][0].rect.top<wall[4][0].rect.top and cannonball[set_cannonball][0].rect.left>0 and cannonball[set_cannonball][0].rect.right<640:
                    shoot.play()
        
        #stage 4
        if stage==4:
            #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
            if not ball[0][2] or ball[0][2]==2:
                move[1]-=1.2
                
                if ball[0][0].rect.colliderect(wall[4][8].rect):
                    hit.play()
                    if move[1]>=-8 and move[1]<0:
                        ball[0][2]=1
                        move[1]=0
                    else:
                        move[1]=-move[1]*5/9
                        direction[2]=True
                    ball[0][0].rect.bottom=wall[4][8].rect.top
                if ball[0][0].rect.colliderect(wall[0][1].rect):
                    hit.play()
                    if ball[0][0].rect.colliderect(scene_change[4][0].rect):
                        ball[0][0].rect.top=wall[3].rect.bottom+1
                        move[1]=-move[1]
                    else:
                        ball[0][0].rect.left=wall[0][1].rect.right
                        if move[0]<0:
                            move[0]=-move[0]
                        move[0]=move[0]*5/9
                if ball[0][0].rect.colliderect(wall[0][2].rect):
                    hit.play()
                    if ball[0][0].rect.centerx<obstacle[1][2].rect.top:
                        if move[1]>=-8 and move[1]<0:
                            ball[0][2]=1
                            move[1]=0
                        else:
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=wall[0][2].rect.top
                    else:
                        ball[0][0].rect.right=wall[0][2].rect.left
                        if move[0]>0:
                            move[0]=-move[0]
                        move[0]=move[0]*5/9
            
            #determine the collision between ball and obstacles
            if ball[0][2]==2:
                for types in range(len(surface[0])):
                    if ball[0][0].rect.colliderect(surface[0][types][0].rect):
                        ball[0][2]=2
                        break
                    ball[0][2]=0
                for types in range(len(surface[1])):
                    if ball[0][2]:
                        break
                    if ball[0][0].rect.colliderect(surface[1][types][0].rect):
                        ball[0][2]=2
                        break
                    ball[0][2]=0
                
            for collision in range(len(obstacle[0])):
                if ball[0][0].rect.colliderect(obstacle[0][collision].rect):
                    hit.play()
                    if ball[0][0].rect.colliderect(surface[0][collision][0].rect) and ball[2][0].rect.bottom<=obstacle[0][collision].rect.top:
                        if move[1]>=-8 and move[1]<0:
                            ball[0][2]=2
                            move[1]=0
                        elif move[1]<0:
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=obstacle[0][collision].rect.top
                    else:
                        bound[2]=1
                        ball[0][0].rect.right=obstacle[0][collision].rect.left
                        if move[0]>0:
                            move[0]=-move[0]
                            
            #determine the collision between ball and obstacles
            for collision in range(3):
                if ball[0][0].rect.colliderect(obstacle[1][collision].rect):
                    hit.play()
                    if ball[0][0].rect.colliderect(surface[1][collision][0].rect) and ball[2][0].rect.bottom<=obstacle[1][collision].rect.top:
                        if move[1]>=-8 and move[1]<0:
                            ball[0][2]=2
                            move[1]=0
                        elif move[1]<0:
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=obstacle[1][collision].rect.top
                        
                    elif ball[0][0].rect.colliderect(surface[1][collision][1].rect) and ball[2][0].rect.top>=obstacle[1][collision].rect.bottom:
                        ball[0][0].rect.top=obstacle[1][collision].rect.bottom+1
                        move[1]=-move[1]*5/9
                            
                    else:
                        if collision<2:
                            ball[0][0].rect.left=obstacle[1][collision].rect.right
                            if move[0]<0:
                                move[0]=-move[0]
                        else:
                            ball[0][0].rect.right=obstacle[1][collision].rect.left    
                            if move[0]>0:
                                move[0]=-move[0]
                        move[0]=move[0]*5/9
            
            #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
            if ball[0][0].rect.colliderect(wall[5].rect):
                hit.play()
                ball[0][0].rect.top=wall[5].rect.bottom+1
                move[1]=-move[1]*5/9
            #shift stage to 4.2 (hidden path)
            if ball[0][0].rect.colliderect(scene_change[4][1]):
                stage=4.2
            #shift stage to 5 (boss stage)
            if ball[0][0].rect.colliderect(scene_change[4][2]):
                ball[0][2]=0
                stage=5
        
        #stage 4.2
        if stage==4.2:
            #location[2] now acts as little stage in each stage
            if location[2]==3:
                if ball[0][2]==2:
                    for types in range(len(surface[0])):
                        if ball[0][0].rect.colliderect(surface[0][types][0].rect):
                            ball[0][2]=2
                            break
                        ball[0][2]=0
                #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
                if not ball[0][2]:
                    move[1]-=1.2
                
                    if ball[0][0].rect.colliderect(obstacle[1][1].rect) or ball[0][0].rect.colliderect(obstacle[1][2].rect):
                        hit.play()
                        if move[1]>=-8 and move[1]<0:
                            ball[0][2]=2
                            move[1]=0
                        else:
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=obstacle[1][1].rect.top
                    
                if ball[0][0].rect.colliderect(wall[0][1].rect):
                    hit.play()
                    ball[0][0].rect.left=wall[0][1].rect.right
                    move[0]=-move[0]*5/9
                
                #determine the collision between ball and obstacles
                bound[2]=0
                for collision in range(3,7):
                    if ball[0][0].rect.colliderect(obstacle[1][collision].rect):
                        hit.play()
                        if ball[0][0].rect.colliderect(surface[1][collision][0].rect) and ball[2][0].rect.bottom<=obstacle[1][collision].rect.top:
                            bound[2]=1
                            if move[1]>=-8 and move[1]<0:
                                ball[0][2]=2
                                move[1]=0
                            elif move[1]<0:
                                move[1]=-move[1]*5/9
                                direction[2]=True
                            ball[0][0].rect.bottom=obstacle[1][collision].rect.top
                        
                        elif ball[0][0].rect.colliderect(surface[1][collision][1].rect) and ball[2][0].rect.top>=obstacle[1][collision].rect.bottom:
                            bound[2]=1
                            ball[0][0].rect.top=obstacle[1][collision].rect.bottom+1
                            move[1]=-move[1]*5/9
                            
                        else:
                            if collision%2==1:
                                ball[0][0].rect.left=obstacle[1][collision].rect.right
                                if move[0]<0:
                                    move[0]=-move[0]
                            else:
                                ball[0][0].rect.right=obstacle[1][collision].rect.left    
                                if move[0]>0:
                                    move[0]=-move[0]
                            move[0]=move[0]*5/9
                
                #determine which side of wall[5] the ball collides with, one side of wall[5] has thorns on it so the ball will explode if it thouches that side
                if ball[0][0].rect.colliderect(wall[5].rect):
                    if ball[0][0].rect.colliderect(scene_change[4][6]) and ball[2][0].rect.top>=scene_change[4][6].rect.bottom:
                        hit.play()
                        move[1]=-move[1]*5/9
                        ball[0][0].rect.top=wall[5].rect.bottom
                    else:
                        ball[0][3]=True
                        
                #if ball collides with wall[8] or wall[9], it explodes
                if ball[0][0].rect.centery>=480 or ball[0][0].rect.colliderect(wall[7].rect) or ball[0][0].rect.colliderect(wall[8].rect):
                    ball[0][3]=True
                    
                #shift stage to 4.8
                if ball[0][0].rect.colliderect(scene_change[4][3]):
                    stage=4.8
                    oneattack=Sprites.Thorn('0-0',(3400,1600))
                    wallSprite.add(oneattack)
                
                #shift stage to 5
                if ball[0][0].rect.colliderect(scene_change[4][2]):
                    ball[0][2]=0
                    stage=5
                    
            else:
                #another animation between stages (stage 4 and stage 4.2)
                move=[0,0]
                
        #stage 4.8
        if stage==4.8:
            #cut stage 4.8 into small stages according to location[2]
            if location[2]==4:
                #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls
                if not ball[0][2]:
                    move[1]-=1.2
                
                    if ball[0][0].rect.colliderect(wall[5].rect):
                        hit.play()
                        if move[1]>=-8 and move[1]<0:
                            ball[0][2]=1
                            move[1]=0
                        else:
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=wall[5].rect.top
                    if ball[0][0].rect.colliderect(wall[8].rect):
                        hit.play()
                        ball[0][0].rect.top=wall[8].rect.bottom+1
                        move[1]=-move[1]*5/9
                    if ball[0][0].rect.colliderect(wall[0][3].rect):
                        hit.play()
                        ball[0][0].rect.right=wall[0][3].rect.left
                        move[0]=-move[0]*5/9
                
                #little stage shift to 4.5
                if ball[0][0].rect.colliderect(scene_change[4][4].rect):
                    ball[0][2]=0
                    location[2]=4.5
                    
            #second little stage
            #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
            elif location[2]==4.5:
                move[1]-=1.2
                
                if ball[0][0].rect.colliderect(wall[0][3].rect):
                    hit.play()
                    ball[0][0].rect.right=wall[0][3].rect.left
                    move[0]=-move[0]*5/9
                if ball[0][0].rect.colliderect(wall[5].rect):
                    hit.play()
                    ball[0][0].rect.left=wall[5].rect.right
                    if move[0]<0:
                        move[0]=-move[0]
                    move[0]=move[0]*5/9
                #push a thorn down to defeat the boss with only one attack
                if ball[0][0].rect.colliderect(oneattack.rect):
                    oneattack.change_location((0,ball[0][0].rect.bottom+1-oneattack.rect.top))
                    
                #stage shift to 5
                #little stage shift to 5.1
                if ball[0][0].rect.colliderect(scene_change[4][5].rect):
                    stage=5
                    location[2]=5.1
                
            else:
                #an animation between stage 4.2 and 4.8, speed of ball is set to zero
                move=[0,0]
                if ball[0][0].rect.colliderect(wall[8].rect):
                    ball[0][0].rect.top=wall[8].rect.bottom+1
                elif ball[0][0].rect.colliderect(wall[5].rect):
                    ball[0][0].rect.bottom=wall[5].rect.top
        
        #stage 5
        if stage==5:
            if location[2]==4:
                #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
                if not ball[0][2]:
                    move[1]-=1.2
                
                    if ball[0][0].rect.colliderect(wall[6][0].rect) or ball[0][0].rect.colliderect(wall[0][2].rect):
                        hit.play()
                        if move[1]>=-8 and move[1]<0:
                            ball[0][2]=1
                            move[1]=0
                        else:
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=wall[6][0].rect.top
                    if ball[0][0].rect.colliderect(wall[5].rect):
                        hit.play()
                        ball[0][0].rect.top=wall[5].rect.bottom+1
                        move[1]=-move[1]*5/9
                    if ball[0][0].rect.colliderect(wall[6][1].rect):
                        hit.play()
                        ball[0][0].rect.right=wall[6][1].rect.left
                        move[0]=-move[0]*5/9
                
                #little stage shift to 4.5
                if ball[0][0].rect.colliderect(scene_change[5][0].rect):
                    ball[0][2]=0
                    location[2]=4.5
                    
            elif location[2]==4.5:
                #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
                move[1]-=1.2
                
                if ball[0][0].rect.colliderect(wall[6][1].rect):
                    hit.play()
                    ball[0][0].rect.right=wall[6][1].rect.left
                    move[0]=-move[0]*5/9
                if ball[0][0].rect.colliderect(wall[6][0].rect):
                    hit.play()
                    ball[0][0].rect.left=wall[6][0].rect.right
                    if move[0]<0:
                        move[0]=-move[0]
                    move[0]=move[0]*5/9
                
                #little stage shift to 5
                if ball[0][0].rect.colliderect(scene_change[5][1].rect):
                    location[2]=5
                    
            elif location[2]>=5:
                #creates a little animation when meets the boss
                if location[2]<5.5:
                    move[0]=0
                
                #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
                if not ball[0][2]:
                    move[1]-=1.2
                    
                    if ball[0][0].rect.colliderect(wall[4][9].rect):
                        if move[1]>=-8 and move[1]<0:
                            hit.play()
                            ball[0][2]=1
                            move[1]=0
                        else:
                            if location[2]==5.5 and move[1]<-50:
                                shakes.play()
                                shake[0]=30
                                if not shake[1] and thorn:
                                    if thorn[0].rect.centery<77:
                                        for set_thorn in range(len(thorn)):
                                            thorn[set_thorn].change_location((0,11))
                                    else:
                                        shake[2]=40
                            else:
                                hit.play()
                            move[1]=-move[1]*5/9
                            direction[2]=True
                        ball[0][0].rect.bottom=wall[4][9].rect.top
                    elif ball[0][0].rect.colliderect(wall[6][0].rect) or ball[0][0].rect.colliderect(wall[6][1].rect):
                        ball[0][0].rect.top=wall[6][0].rect.bottom-1
                        move[1]=-move[1]*5/9
                        
                #determine if the ball is on the ground, if not, the falling speed of the ball increases by 1.2, it also checks the collision between ball, walls and obstacles
                if ball[0][0].rect.colliderect(wall[0][2].rect):
                    hit.play()
                    ball[0][0].rect.left=wall[0][2].rect.right
                    move[0]=-move[0]
                elif ball[0][0].rect.colliderect(wall[0][3].rect):
                    hit.play()
                    ball[0][0].rect.right=wall[0][3].rect.left
                    move[0]=-move[0]
                    
                #stage 5, little stage 5.5, the boss stage, last stage of the game
                if location[2]==5.5:
                    
                    #adds the shake effect of walls
                    if shake[1]<0:
                        if shake[1]==-55:
                            thorn=[]
                            for set_thorn in range(3):
                                thorn+=[Sprites.Thorn('0-0',(45+54*set_thorn+2820,2081))]
                            for set_thorn in range(5):
                                thorn+=[Sprites.Thorn('0-0',(308+54*set_thorn+2820,2081))]
                            thornSprite=pygame.sprite.Group(thorn)
                            shake[1]+=1
                        else:
                            for set_thorn in range(len(thorn)):
                                thorn[set_thorn].change_location((0,1))
                            shake[1]+=1
                    
                    #adds the dropping effect of thorns
                    if shake[2]:
                        if not pygame.sprite.spritecollide(wall[4][9],thornSprite,False):
                            for set_thorn in range(len(thorn)-1,-1,-1):
                                if not thorn[set_thorn].rect.colliderect(UFO[0].rect):
                                    thorn[set_thorn].change_location((0,40-shake[2]))
                                else:
                                    health[1].change(-40)
                                    del thorn[set_thorn]
                                    #health of UFO decreases when thorns hit it
                                    thornSprite=pygame.sprite.Group(thorn)
                                    UFO[1]=2
                                    UFO[2]=0
                        #health of ball decreases when thorns hit it
                        if thorn and pygame.sprite.spritecollide(ball[0][0],thornSprite,True):
                            if not ball[0][4]:
                                health[0].change(-20)
                                ball[0][4]=15
                            
                        shake[2]-=1
                        if not shake[2]:
                            thorn=[]
                            thornSprite=pygame.sprite.Group()
                            if len(thorn)==8:
                                shake[1]=-55
                    else:
                        if thorn and not ball[0][4] and pygame.sprite.spritecollide(ball[0][0],thornSprite,False):
                            health[0].change(-20)
                            ball[0][4]=15
                    
                    if UFO[1]==-1:
                        cannonball=[]
                        cbSprite=pygame.sprite.Group()
                        UFO[1]=0
                    
                    #UFO shoots cannonballs when it stays near the same x-axis value as the ball, UFO shoots 3 cannonballs at a time and stop for while and then keeps doing this until it is hit by thorns
                    elif UFO[1]==0:
                        if UFO[2]:
                            if UFO[2]%5==0:
                                shoot.play()
                                cannonball+=[Sprites.Cannonball((UFO[0].rect.centerx+location[0],UFO[0].rect.centery+location[1]+40))]
                                cbSprite=pygame.sprite.Group(cannonball)
                            
                            if UFO[0].rect.centerx-ball[0][0].rect.centerx<10 and UFO[0].rect.centerx-ball[0][0].rect.centerx>-10:
                                UFO[0].change_location((UFO[0].rect.centerx-ball[0][0].rect.centerx,0))
                            elif UFO[0].rect.centerx>ball[0][0].rect.centerx:
                                UFO[0].change_location((10,0))
                            else:
                                UFO[0].change_location((-10,0))
                            
                            UFO[2]+=1
                            if UFO[2]>=15:
                                UFO[1]+=60
                                UFO[2]=0
                                
                        elif (UFO[0].rect.centerx-ball[0][0].rect.centerx)**2<=2048:
                            if not cannonball:
                                shoot.play()
                                cannonball+=[Sprites.Cannonball((UFO[0].rect.centerx+location[0],UFO[0].rect.centery+location[1]+40))]
                                cbSprite=pygame.sprite.Group(cannonball)
                                UFO[2]=1
                        else:
                            if (UFO[0].rect.centerx-ball[0][0].rect.centerx)*8/10/x>5 or (UFO[0].rect.centerx-ball[0][0].rect.centerx)*8/10/x<-5:
                                UFO[0].change_location(((UFO[0].rect.centerx-ball[0][0].rect.centerx)*8/10/x,0))
                            elif UFO[0].rect.centerx-ball[0][0].rect.centerx<5 and UFO[0].rect.centerx-ball[0][0].rect.centerx>-5:
                                UFO[0].change_location((UFO[0].rect.centerx-ball[0][0].rect.centerx,0))
                            elif (UFO[0].rect.centerx-ball[0][0].rect.centerx)*8/10/x>0:
                                UFO[0].change_location((5,0))
                            else:
                                UFO[0].change_location((-5,0))
                    
                    #when UFO is hit by thorns, it uses the second attack mode, it would go to the closest side wall, then go down. set fire on the ground. if the ball touches fire, its health dcreses. after a period of time, UFO would go up again and resume its first attack mode
                    
                    elif UFO[1]==2:
                        if UFO[2]==-1:
                            thornSprite=pygame.sprite.Group()
                            UFO[0].change_location((0,-5))
                            if UFO[0].rect.centery<=150:
                                UFO[1]=0
                                UFO[2]=0
                                shake[1]=-55
                        
                        elif UFO[2]:
                            if UFO[2]>70:
                                fires.play()
                            if (UFO[2]+1)%2==0:
                                if UFO[2]==199:
                                    fire+=[Sprites.Fire(UFO[3],(UFO[0].rect.centerx,2506))]
                                elif fire:
                                    if not UFO[3]:
                                        if fire[len(fire)-1].rect.centerx+30<640:
                                            fire+=[Sprites.Fire(UFO[3],(fire[len(fire)-1].rect.centerx+30,2506))]
                                    elif fire[len(fire)-1].rect.centerx-30>0:
                                        fire+=[Sprites.Fire(UFO[3],(fire[len(fire)-1].rect.centerx-30,2506))]
                                    if fire[0].disappear():
                                        del fire[0]
                                for set_fire in range(len(fire)):
                                    fire[set_fire].change_picture()
                                    
                                thornSprite=pygame.sprite.Group(fire)
                                
                            if pygame.sprite.spritecollide(ball[0][0],thornSprite,False):
                                if not ball[0][4]:
                                    health[0].change(-1)
                                    ball[0][4]=3
                                    
                            UFO[2]-=2
                                        
                        elif UFO[0].rect.colliderect(wall[4][9].rect):
                            UFO[2]=199
                            UFO[0].change_location((0,-10))
                            fire=[]
                            
                        elif UFO[0].rect.colliderect(wall[0][2].rect) or UFO[0].rect.colliderect(wall[0][3].rect):
                            UFO[0].change_location((0,5))
                            
                        elif UFO[0].rect.centerx<=320:
                            UFO[3]=0
                            if (UFO[0].rect.centerx-320)*8/10/x<-5:
                                UFO[0].change_location((-(UFO[0].rect.centerx-320)*8/10/x,0))
                            else:
                                UFO[0].change_location((5,0))
                        else:
                            UFO[3]=1
                            if (UFO[0].rect.centerx-320)*8/10/x>5:
                                UFO[0].change_location((-(UFO[0].rect.centerx-320)*8/10/x,0))
                            else:
                                UFO[0].change_location((-5,0))
                    
                    #a technique that lets UFO pause for a second
                    else:
                        UFO[1]-=4
                            
                    #both ball and UFO's healths would decrease when they touch each other
                    if ball[0][0].rect.colliderect(UFO[0].rect):
                        if not ball[0][4]:
                            health[0].change(-2)
                            ball[0][4]=5
                        if move[0]**2+move[1]**2>900:
                            health[1].change(-5)
                    
                    #ball's health decreases when it touches cannonball, and the cannonball will disappear
                    if cannonball:
                        for set_cannonball in range(len(cannonball)-1,-1,-1):
                            if ball[0][0].rect.colliderect(cannonball[set_cannonball].rect):
                                del cannonball[set_cannonball]
                                if not ball[0][4]:
                                    ball[0][4]=10
                                    health[0].change(-10)
                                cbSprite=pygame.sprite.Group(cannonball)
                            elif cannonball[set_cannonball].rect.centery>640:
                                del cannonball[set_cannonball]
                                cbSprite=pygame.sprite.Group(cannonball)
                            else:
                                cannonball[set_cannonball].change_location(20*30/x)
                    
                    if ball[0][4]:
                        ball[0][4]-=1
                        
                    #Next few lines are responsible for the one attack that defeat UFO
                    if oneattack and oneattack.rect.colliderect(UFO[0].rect):
                        health[1].change(-1000)
                        oneattack.kill()
                    #move oneattack sprite
                    elif stage==5.1:
                        oneattack.change_location((0,ball[0][0].rect.bottom+1-oneattack.rect.top))
                    
                    #when UFO health is zero or below
                    if health[1].die():
                        
                        #Effect of explosion
                        UFOexplosions.play()
                        for explosion in range(336):
                            picSprite.update(location)
                            ballSprite.update()
                            if location[2]==5.5:
                                if shake[2]:
                                    thornSprite.update((2820,2560-480))
                                else:
                                    thornSprite.update(location)
                            wallSprite.update(location)
                            if location[2]<5.5:
                                obstacleSprite.update(location)
                            else:
                                healthSprite.update()
                            if shake[0]:
                                UFOSprite.update((2820,2560-480))
                            else:
                                UFOSprite.update(location)
                            
                            picSprite.draw(screen)
                            ballSprite.draw(screen)
                            if location[2]==5.5:
                                thornSprite.draw(screen)
                            wallSprite.draw(screen)
                            if location[2]<5.5:
                                obstacleSprite.draw(screen)
                            else:
                                healthSprite.draw(screen)
                            UFOSprite.draw(screen)
        
                            pygame.display.flip()
                            
                            picSprite.clear(screen,background)
                            ballSprite.clear(screen,background)
                            if ballshadow:
                                ballshadow.clear(screen,background)
                            if location[2]==5.5:
                                thornSprite.clear(screen,background)
                            wallSprite.clear(screen,background)
                            if location[2]<5.5:
                                obstacleSprite.clear(screen,background)
                            else:
                                healthSprite.clear(screen,background)
                            UFOSprite.clear(screen,background)
                                
                            if explosion%24==0:
                                UFO[0].explosion()
                        
                        #a screen shows the evaluation of player
                        #Play the background music of victory
                        pygame.mixer.music.load('win.wav')
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(0)
                        
                        #An animation of couting marks
                        menu.continues()
                        label+=[Sprites.Label('YOU WIN!',(320,50),50,(0,0,153))]
                        label+=[Sprites.Label('Time:',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((100,100))
                        label+=[Sprites.Label('Remaining Health:',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((100,150))
                        label+=[Sprites.Label('---------------------------------------------',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((100,180))
                        label+=[Sprites.Label('Total:',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((100,210))
                        
                        menuSprite=pygame.sprite.OrderedUpdates(menu,label[len(label)-1],label[len(label)-2],label[len(label)-3],label[len(label)-4],label[len(label)-5])
                        
                        label+=[Sprites.Label('',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((500,100))
                        menuSprite.add(label[len(label)-1])
                        for set_label in range(1,(int(time[2])+1)*10):
                            if set_label%10==0:
                                label[len(label)-1].set_text(repr(set_label/10))
                                menuSprite.update()
                                menuSprite.draw(screen)
                                pygame.display.flip()
                                menuSprite.clear(screen,background)
                                            
                        label+=[Sprites.Label('',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((500,150))
                        menuSprite.add(label[len(label)-1])
                        for set_label in range(1,(health[0].remaining()+1)*10):
                            if set_label%10==0:
                                label[len(label)-1].set_text(repr(set_label/10))
                                menuSprite.update()
                                menuSprite.draw(screen)
                                pygame.display.flip()
                                menuSprite.clear(screen,background)
                                
                        for _ in range(180):
                            menuSprite.update()
                            menuSprite.draw(screen)
                            pygame.display.flip()
                            menuSprite.clear(screen,background)
                            
                        label+=[Sprites.Label('',(0,0),25,(255,255,0))]
                        label[len(label)-1].left_top((500,210))
                        total=0
                        menuSprite.add(label[len(label)-1])
                        for set_label in range((int(time[2])+1)*5-1,-1,-1):
                            if set_label%5==0:
                                label[len(label)-3].set_text(repr(set_label/5))
                                total+=1
                                label[len(label)-1].set_text(repr(total))
                                menuSprite.update()
                                menuSprite.draw(screen)
                                pygame.display.flip()
                                menuSprite.clear(screen,background)
                        for set_label in range((health[0].remaining()+1)*5-1,-1,-1):
                            if set_label%5==0:
                                label[len(label)-2].set_text(repr(set_label/5))
                                total+=1
                                label[len(label)-1].set_text(repr(total))
                                menuSprite.update()
                                menuSprite.draw(screen)
                                pygame.display.flip()
                                menuSprite.clear(screen,background)
                        for set_label in range(total*5+1,(600-int(time[2]))*health[0].remaining()*5):
                            if set_label%5==0:
                                total+=1
                                label[len(label)-1].set_text(repr(total))
                                menuSprite.update()
                                menuSprite.draw(screen)
                                pygame.display.flip()
                                menuSprite.clear(screen,background)
                        
                        #a label shows to indicate Press any key to exit
                        menuSprite.add(label[3])
                        label[3].set_text('Press any key to exit')
                        label[3].locationchange((320,420))
                        label[3].colorchange((255,153,0))
                        
                        #a while loop to exit the game when any key is pressed
                        while keepGoing:
                            for event in pygame.event.get():
                                if event.type==pygame.QUIT:
                                    keepGoing = False
                                elif event.type==pygame.KEYDOWN:
                                    keepGoing = False
                                    
                            menuSprite.update()
                            menuSprite.draw(screen)
                            pygame.display.flip()
                            menuSprite.clear(screen,background)
                            
                        break
                    
                    #when ball's health is 0 or below
                    elif health[0].die():
                        ball[0][3]=True
                
            #an animation between stage 4 and 5
            else:
                move=[0,0]
                if ball[0][0].rect.colliderect(wall[5].rect):
                    ball[0][0].rect.top=wall[5].rect.bottom+1
                elif ball[0][0].rect.colliderect(wall[6][0].rect):
                    ball[0][0].rect.bottom=wall[6][0].rect.top
                
        #effect of ball's explosion
        if ball[0][3]:
            
            #change pictures to implement the effect
            explosions.play()
            ball[0][0].explosion()
            for explosion in range(120):
                picSprite.update(location)
                if stage>2:
                    cbSprite.update(location)
                if location[2]==5.5:
                    if shake[2]:
                        thornSprite.update((2820,2560-480))
                    else:
                        thornSprite.update(location)
                if shake[0]:
                    UFOSprite.update((2820,2560-480))
                else:
                    UFOSprite.update(location)
                wallSprite.update(location)
                if location[2]<5.5:
                    obstacleSprite.update(location)
                else:
                    healthSprite.update()
                ballSprite.update()
                
                picSprite.draw(screen)
                if stage>2:
                    cbSprite.draw(screen)
                if location[2]==5.5:
                    thornSprite.draw(screen)
                UFOSprite.draw(screen)
                wallSprite.draw(screen)
                if location[2]<5.5:
                    obstacleSprite.draw(screen)
                else:
                    healthSprite.draw(screen)
                ballSprite.draw(screen)
        
                pygame.display.flip()
                
                picSprite.clear(screen,background)
                if ballshadow:
                    ballshadow.clear(screen,background)
                if stage>2:
                    cbSprite.clear(screen,background)
                if location[2]==5.5:
                    thornSprite.clear(screen,background)
                UFOSprite.clear(screen,background)
                wallSprite.clear(screen,background)
                if location[2]<5.5:
                    obstacleSprite.clear(screen,background)
                else:
                    healthSprite.clear(screen,background)
                ballSprite.clear(screen,background)
                if explosion%12==0:
                    ball[0][0].explosion()
            
            #a screen shows up to ask whether player wants to continue
            #if continuing, the player starts at the very beginning of that stage (except for stage 5)
            menu.continues()
            label[3].locationchange((320,200))
            label[1].locationchange((500,350))
            menuSprite=pygame.sprite.OrderedUpdates(menu,label[1],label[3])
            keepGoing=False
                
            #wait for choice from player
            while not keepGoing:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        keepGoing = -1
                    elif event.type==pygame.KEYDOWN:
                        click.play()
                        if event.key==pygame.K_SPACE:
                            keepGoing=True
                        else:
                            keepGoing=-1
                    elif event.type == pygame.MOUSEMOTION:
                        position = [pygame.mouse.get_pos(),False]
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if position[0][0]<=label[1].rect.right and position[0][0]>=label[1].rect.left and position[0][1]>=label[1].rect.top and position[0][1]<=label[1].rect.bottom:
                            click.play()
                            menu.instruction()
                            label[3].locationchange((320,440))
                            menuSprite=pygame.sprite.OrderedUpdates(menu,label[3])
                
                for set_label in range(len(label)):
                    if position[0][0]<=label[set_label].rect.right and position[0][0]>=label[set_label].rect.left and position[0][1]>=label[set_label].rect.top and position[0][1]<=label[set_label].rect.bottom:
                        label[set_label].colorchange((0,102,102))
                    else:
                        if set_label==3:
                            label[set_label].colorchange((255,153,0))
                        else:
                            label[set_label].colorchange((204,204,51))
                                
                menuSprite.update()
                menuSprite.draw(screen)
                pygame.display.flip()
                menuSprite.clear(screen,background)
                            
            if keepGoing==-1:
                break
            
            #recreate the ball and ballshadows
            #reassign the value of variables that are related to the ball
            else:
                for set_ball in range(6):
                    if set_ball==0:
                        ball=[[Sprites.Ball(),False,0,False,0]]
                    else:
                        ball+=[[Sprites.BallShadow(set_ball,ball[set_ball-1][0].ballnumber()),ball[set_ball-1][1]]]
                ballSprite=pygame.sprite.Group(ball[0][0])
                move=[0,0]
                direction=[0,0,0]
                if stage<3:
                    stage=2
                    location=[2260-640,1300,1]
                    ball[0][0].rect.center=(480,240)
                elif stage<4:
                    stage=3
                    location=[420,2120,2.5]
                    ball[0][0].rect.center=(50,240)
                    wall_4_space[1]=False
                elif stage<5:
                    stage=4
                    location=[2200,2120,2.5]
                    ball[0][0].rect.center=(50,240)
                else:
                    stage=4
                    location=[2200,1940,2.5]
                    ball[0][0].rect.center=(350,25)
                    UFO=[Sprites.UFO(),-1,0,0]
                    UFOSprite=pygame.sprite.Group(UFO[0])
                    shake=[0,-55,0]
                    fire=[]
                    thorn=[]
                    cannonball=[]
                    cbSprite=pygame.sprite.Group()
                    thornSprite=pygame.sprite.Group()
                    pygame.mixer.music.load('stage4.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
            
        #a Group that is responsible for ball shadows
        ballshadow=pygame.sprite.OrderedUpdates()
        for set_ball in range(5,0,-1):
            if ball[set_ball][1]:
                ballshadow.add(ball[set_ball][0])
        
        #a set of code that is responsible for the change in 'location' variable
        #it controls the movement of walls
        #change in 'location' is related to the move of the ball
        #there are some bounds that 'location' cannot cross
        if stage>=1 and stage<3:
            if stage==1:
                location[1]=0
            
            elif stage==1.5:
                if move[1]<0:
                    location[1]-=move[1]
                for set_ball in range(5,-1,-1):
                    ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-400

            elif stage==2:
                if location[2]:
                    location[1]=1300
                elif location[1]>1300 or move[1]>0:
                    ball[0][0].rect.centery+=location[1]-1300
                    location[1]=1300
                    location[2]=1
                else:
                    location[1]-=move[1]
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-400
                if ball[0][0].rect.top<0:
                    ball[0][0].rect.top=0
            
            elif stage==2.5:
                if ball[0][0].rect.centery>400:
                    if move[1]<0:
                        location[1]-=move[1]
                    if location[1]<2600-480:
                        for set_ball in range(5,-1,-1):
                            ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-400
                
            if location[0]>0 and ball[0][0].rect.centerx<bound[0][bound[2]]:
                location[0]+=move[0]
                for set_ball in range(5,-1,-1):
                    ball[set_ball][0].rect.centerx-=ball[0][0].rect.centerx-bound[0][bound[2]]
            elif location[0]<2260-640 and ball[0][0].rect.centerx>bound[1][bound[2]]:
                location[0]+=move[0]
                for set_ball in range(5,-1,-1):
                    ball[set_ball][0].rect.centerx-=ball[0][0].rect.centerx-bound[1][bound[2]]
            elif location[0]>0 and ball[0][0].rect.centerx<bound[3][bound[2]]:
                location[0]-=3
                for set_ball in range(5,-1,-1):
                    ball[set_ball][0].rect.centerx+=3
            elif location[0]<2260-640 and ball[0][0].rect.centerx>bound[4][bound[2]]:
                location[0]+=3
                for set_ball in range(5,-1,-1):
                    ball[set_ball][0].rect.centerx-=3
            if location[0]>2260-640:
                location[0]=2260-640
                
        elif stage==3:
            if location[2]==2.5:
                location[1]=2120
            elif move[1]>0:
                ball[0][0].rect.centery+=location[1]-(2600-480)
                location[2]=2.5
            else:
                location[1]-=move[1]
                if ball[0][0]>400:
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-400
            
            if location[2]<2:
                if ball[0][0].rect.centerx+location[0]>440:
                    ball[0][0].rect.centerx-=4*30/x
                    
                location[0]+=4*30/x
                if location[0]>=417:
                    location[2]=2
                    location[0]=420
            else:
                if location[0]>420 and ball[0][0].rect.centerx<bound[0][bound[2]]:
                    location[0]+=move[0]
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx-=ball[0][0].rect.centerx-bound[0][bound[2]]
                elif ball[0][0].rect.centerx>bound[1][bound[2]]:
                    location[0]+=move[0]
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx-=ball[0][0].rect.centerx-bound[1][bound[2]]
                elif location[0]>420 and ball[0][0].rect.centerx<bound[3][bound[2]]:
                    location[0]-=3
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx+=3
                elif ball[0][0].rect.centerx>bound[4][bound[2]]:
                    location[0]+=3
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx-=3
                        
                if location[0]<420:
                    location[0]=420
                    
        elif stage==4 or stage==4.2:
            location[0]=2200
            
            if stage==4:
                if ball[0][0].rect.centery<100 and location[1]>1940:
                    location[1]-=10
                    for set_ball in range(6):
                        ball[set_ball][0].rect.centery+=10
                elif ball[0][0].rect.centery>380 and location[1]<2600-480:
                    location[1]+=10
                    for set_ball in range(6):
                        ball[set_ball][0].rect.centery-=10
                if location[1]<1940:
                    location[1]=1940
            else:
                if location[2]==3:
                    location[1]-=2
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centery+=2

                else:
                    location[1]-=10*30/x
                    ball[0][0].rect.centery+=10*30/x
                    
                    if location[1]<2080-480:
                        location[1]=2080-480
                        location[2]=3
        
        elif stage==4.8:
            if location[2]==4:
                if location[0]>2440 and ball[0][0].rect.centerx<bound[0][bound[2]]:
                    location[0]+=move[0]
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx-=ball[0][0].rect.centerx-bound[0][bound[2]]
                elif location[0]<3460-640 and ball[0][0].rect.centerx>bound[1][bound[2]]:
                    location[0]+=move[0]
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx-=ball[0][0].rect.centerx-bound[1][bound[2]]
                elif location[0]>2440 and ball[0][0].rect.centerx<bound[3][bound[2]]:
                    location[0]-=3
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx+=3
                elif location[0]<3460-640 and ball[0][0].rect.centerx>bound[4][bound[2]]:
                    location[0]+=3
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centerx-=3
                        
                if location[0]>3460-640:
                    location[0]=3460-640
                if location[0]<2440:
                    location[0]=2440
                
            elif location[2]==4.5:
                if move[1]<0:
                    location[1]-=move[1]
                if ball[0][0].rect.centery>440:
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-440
                    
            else:
                if location[0]<2440:
                    location[0]+=4*30/x
                    if location[0]+ball[0][0].rect.centerx>2465:
                        ball[0][0].rect.centerx-=4*30/x
                else:
                    location[0]=2440
                    location[2]=4
                    
        elif stage==5:
            if location[2]==4:
                location[0]=2820
            elif location[2]==4.5:
                location[1]-=move[1]
                if ball[0][0].rect.centery>440:
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-440
            elif location[2]==5 or location[2]==5.1:
                if move[1]<0:
                    location[1]-=move[1]
                if ball[0][0].rect.centery>440:
                    for set_ball in range(5,-1,-1):
                        ball[set_ball][0].rect.centery-=ball[0][0].rect.centery-440
                    
            elif location[2]==5.5:
                location[0]=2820
                if shake[0]:
                    if location[1]>2560-480:
                        location[1]=2560-480-5
                    else:
                        location[1]=2560-480+5
                    shake[0]-=2
                else:
                    location[1]=2560-480
            else:
                if location[0]<2820:
                    location[0]+=4*30/x
                    if location[0]+ball[0][0].rect.centerx>2845:
                        ball[0][0].rect.centerx-=4*30/x
                else:
                    location[0]=2820
                    location[2]=4
                    
            if location[2]<>5.5 and location[1]+ball[0][0].rect.centery>2560-240:
                location[2]=5.5
                for set_ball in range(5,-1,-1):
                    ball[set_ball][0].rect.centery+=location[1]-2080
                location[1]=2560-480
                
                thornSprite=pygame.sprite.Group()
                
                pygame.mixer.music.load('stage5.mp3')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                
                #create health sprites just before ball fights the UFO
                health=[Sprites.Health((30,30),0),Sprites.Health((610,450),1)]
                healthSprite=pygame.sprite.Group(health)
                for set_health in range(120):
                    health[0].change(1)
                    health[1].change(4)
                    
                    picSprite.update(location)
                    ballSprite.update()
                    UFOSprite.update(location)
                    wallSprite.update(location)
                    healthSprite.update()
                    
                    picSprite.draw(screen)
                    ballSprite.draw(screen)
                    UFOSprite.draw(screen)
                    wallSprite.draw(screen)
                    healthSprite.draw(screen)
                    
                    pygame.display.flip()
                    
                    picSprite.clear(screen,background)
                    ballSprite.clear(screen,background)
                    UFOSprite.clear(screen,background)
                    wallSprite.clear(screen,background)
                    healthSprite.clear(screen,background)
                
        if location[0]<0:
            location[0]=0
        if location[1]>2600-480:
            ball[0][0].rect.centery+=location[1]-(2600-480)
            location[1]=2600-480
            if location[2]<2.5:
                location[2]=2.5
        
        #change the time showing on the top right corner
        timelabel.set_text(repr(int(time[2])))
        
        #update sprites
        picSprite.update(location)
        ballSprite.update()
        if stage>2:
            cbSprite.update(location)
        if location[2]==5.5:
            if shake[2]:
                thornSprite.update((2820,2560-480))
            else:
                thornSprite.update(location)
        if shake[0]:
            UFOSprite.update((2820,2560-480))
        else:
            UFOSprite.update(location)
        wallSprite.update(location)
        if location[2]<5.5:
            obstacleSprite.update(location)
        else:
            healthSprite.update()
        timeSprite.update()
        
        #draw sprites
        picSprite.draw(screen)
        if ballshadow:
            ballshadow.draw(screen)
        ballSprite.draw(screen)
        if stage>2:
            cbSprite.draw(screen)
        if location[2]==5.5:
            thornSprite.draw(screen)
        UFOSprite.draw(screen)
        wallSprite.draw(screen)
        if location[2]<5.5:
            obstacleSprite.draw(screen)
        else:
            healthSprite.draw(screen)
        timeSprite.draw(screen)
        
        #flip
        pygame.display.flip()
        
        #clear sprites
        picSprite.clear(screen,background)
        if ballshadow:
            ballshadow.clear(screen,background)
        ballSprite.clear(screen,background)
        if stage>2:
            cbSprite.clear(screen,background)
        if location[2]==5.5:
            thornSprite.clear(screen,background)
        UFOSprite.clear(screen,background)
        wallSprite.clear(screen,background)
        if location[2]<5.5:
            obstacleSprite.clear(screen,background)
        else:
            healthSprite.clear(screen,background)
        timeSprite.clear(screen,background)
        
    #exit when keepGoing=False
    pygame.quit()

#call the main function
main()