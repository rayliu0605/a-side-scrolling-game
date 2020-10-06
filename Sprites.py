import pygame
pygame.init()

class Ball(pygame.sprite.Sprite):
    '''The Ball class creates the Ball controlled by the player. It has the bility to move in 8 directions, dash, and bounce back when collide with wall and obstacle. It explodes when touching cannonball or thorns. It inherits from the built-in Sprite module'''
    
    def __init__(self):
        '''The __init__ method loads image, creates the ball and gives the ball starting position. It takes and returns nothing.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('ball1.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
        #change image of the ball so the ball looks like moving
        self.__ball=1
        #gives it the starting position
        self.rect.center=(50,250)
        #controls the explosion effect
        self.__explosion=0
        
    def explosion(self):
        '''The explosion method implements the effect by changing an amount of images in a short period of time. It takes and returns nothing'''
        
        self.__explosion+=1
        self.image=pygame.image.load('explosion-'+repr(self.__explosion)+'.gif')
        self.image=self.image.convert()
        
    def resurrect(self):
        '''The resurrect method is used to recreate the ball after it explodes. It takes and returns nothing'''
        
        self.image=pygame.image.load('ball1.gif')
        self.image=self.image.convert()
        self.__explosion=0
        
    def change_picture(self):
        '''The change_picture method implements the effect of ball moving by changing pictures. It takes and returns nothing'''
        
        self.__ball=1-self.__ball
        self.image=pygame.image.load('ball'+repr(self.__ball)+'.gif')
        self.image=self.image.convert()
        
    def ballnumber(self):
        '''The ballnumber method indicates the image of ballshadow. It takes no parameter but returns the variable __ball'''
        
        return self.__ball
            
class BallShadow(pygame.sprite.Sprite):
    '''The BallShadow class creates ball shadows that appear when the ball reachs a certain speed and disappear when the ball's speed is low. Ball shadows follow the path of the ball. It inherits from the built-in Sprite module'''
    
    def __init__(self,number,pic):
        '''The __init__ method loads image, creates ballshadow. number is parameter indicates the opacity of ballshadow. pic is parameter indicates the image the class should load. The method returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        #Next two variables indicate which image the class should load
        self.__ballshadow=1-pic
        self.__number=number
        
        self.image=pygame.image.load('ballshadow'+repr(self.__number)+'-'+repr(self.__ballshadow)+'.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
            
    def change_picture(self,pic):
        '''The change_picture method is used to change ball shadows' images so ball shadows have effect of moving like the ball. It takes parameter to indicate the image number but returns nothing'''
        
        if pic>1:
            self.__ballshadow=pic-2
        elif pic==self.__ballshadow:
            self.__ballshadow=1-pic
        self.image=pygame.image.load('ballshadow'+repr(self.__number)+'-'+repr(self.__ballshadow)+'.gif')
        
    def ballnumber(self):
        '''The ballnumber method indicates the ball shadow image of next ball shadow. It returns variable __ballshadow'''
        
        return self.__ballshadow
            
class Wall(pygame.sprite.Sprite):
    '''The Wall class creates the map, the whole stage 1, obstacles in stage 2 and stage 4. It inherits from the built-in Sprite module'''
    
    def __init__(self,wallnumber):
        '''The __init__ method loads the image of walls. parameter wallnumber indicates the image number. It returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('wall-'+wallnumber+'.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
    def left_top(self,location):
        '''The left_top method assigns the location of top left corner of wall sprite. It takes parameter location and returns nothing'''
        
        self.rect.left=location[0]
        self.rect.top=location[1]
        
        #indicate the default location of wall
        self.__center=self.rect.center
        
    def right_top(self,location):
        '''The right_top method assigns the location of right left corner of wall sprite. It takes parameter location and returns nothing'''
        
        self.rect.right=location[0]
        self.rect.top=location[1]
        
        #indicate the default location of wall
        self.__center=self.rect.center
    
    def left_bottom(self,location):
        '''The left_bottom method assigns the location of bottom left corner of wall sprite. It takes parameter location and returns nothing'''
        
        self.rect.left=location[0]
        self.rect.bottom=location[1]
        
        #indicate the default location of wall
        self.__center=self.rect.center
        
    def right_bottom(self,location):
        '''The right_bottom method assigns the location of bottom right corner of wall sprite. It takes parameter location and returns nothing'''
        
        self.rect.right=location[0]
        self.rect.bottom=location[1]
        
        #indicate the default location of wall
        self.__center=self.rect.center
        
    def update(self,location):
        '''The update method dictates where the wall sprite should display according to default location. parameter location is change in location. It returns nothing'''
        
        self.rect.center=(self.__center[0]-location[0],self.__center[1]-location[1])
        
class Surface(pygame.sprite.Sprite):
    '''The Surface class creates surface sprites which indicate which side of obstcles or walls the ball is colliding with. It inherits from the built-in Sprite module'''
    
    def __init__(self,location,start,end,extra,width,types):
        '''The __init__ method create surface and assign locations. Parameter location is the default location of surface, start end extra are length of surface, width is width of surface, types dictates whether surface is vertical or horizontal. It returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        if types==0:
            self.image=pygame.Surface((end-start-extra,width))
        else:
            self.image=pygame.Surface((width,end-start-extra))
        self.image=self.image.convert()
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        
        self.rect=self.image.get_rect()
        self.rect.center=location
        
        #records the default location
        self.__center=location
        
    def update(self,location):
        '''The update method dictates where the surface sprite should display according to default location. parameter location is change in location. It returns nothing'''
        
        self.rect.center=(self.__center[0]-location[0],self.__center[1]-location[1])
        
class Thorn(pygame.sprite.Sprite):
    '''The Thorn class creates thorns on obstacles which will cause the ball to explode. It inherits from the built-in Sprite module'''
    
    def __init__(self,thornnumber,location):
        '''The __init__ method loads image and creates thorn sprites. parameter thornnumber indicates the image of thorn, location is the default of thorn'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('thorn-'+thornnumber+'.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
        self.__center=location
        
    def change_location(self,location):
        '''The change_location method changes the location recorded by __center. It takes the value added or subtracted by the location. It returns nothing'''
        
        self.__center=(self.__center[0]-location[0],self.__center[1]+location[1])
        
    def update(self,location):
        '''The update method dictates where the thorn sprite should display according to default location. parameter location is change in location. It returns nothing'''
        
        self.rect.center=(self.__center[0]-location[0],self.__center[1]-location[1])
        
class Cannonball(pygame.sprite.Sprite):
    '''The Cannonball class creates cannonballs in stage 3. It assigns the location of cannonball. It gives some cannonball the ability to move and turn around when touching wall. It inherits from the built-in Sprite module'''
    
    def __init__(self,location):
        '''The __init__ method loads image of cannonballs and creates cannonballs. It takes parameter starting location of cannonball and returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('cannonball-0.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
        #record the default location
        self.__center=location
        #record the image of cannonball
        self.__cannonballnumber=0
        
    def change_picture(self):
        '''The change_picture changes the image of some cannonballs when touching walls. It takes and returns nothing'''
        
        self.__cannonballnumber=1-self.__cannonballnumber
        self.image=pygame.image.load('cannonball-'+repr(self.__cannonballnumber)+'.gif')
        
    def change_location(self,value):
        '''The change_location method changes the location recorded by __center. It takes the value added or subtracted by the location. It returns nothing'''
        
        self.__center=(self.__center[0],self.__center[1]+value)
        
    def update(self,location):
        '''The update method indicates where the cannonball should display on the map. It takes the change of location but returns nothing'''
        
        self.rect.center=(self.__center[0]-location[0],self.__center[1]-location[1])
        
class UFO(pygame.sprite.Sprite):
    '''The UFO clas creates UFO in stage 5. It gives UFO the ability to move, attack as well as explode. It assigns the location of UFO. It inherits from the built-in Sprite module'''
    
    def __init__(self):
        '''The __init__ loads image of UFO and assigns sprite the starting position. It takes no parameter and returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('UFO.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
        self.rect.center=(3350,2230)
        
        #records the default location
        self.__center=self.rect.center
        #used to create explosion effect
        self.__explosion=0
        
    def change_location(self,location):
        '''The change_location method changes the location recorded by __center. It takes the value added or subtracted by the location and returns nothing'''
        
        self.__center=(self.__center[0]-location[0],self.__center[1]+location[1])
        
    def explosion(self):
        '''The explosion method implements the effect by changing an amount of images in a short period of time. It takes and returns nothing'''
        
        self.image=pygame.image.load('UFOexplosion-'+repr(self.__explosion)+'.gif')
        self.__explosion+=1
        
    def update(self,location):
        '''The update method indicates where the UFO should display on the map. It takes the change of location but returns nothing'''
        
        self.rect.center=(self.__center[0]-location[0],self.__center[1]-location[1])
        
class Fire(pygame.sprite.Sprite):
    '''The Fire class creates fire sprite using a variety of images so fire sprites have effect of moving. It inherits from the built-in sprite module'''
    
    def __init__(self,direction,location):
        '''The __init__ method loads image of fire and assigns them the starting position. It takes parameter direction(which way the fire moves), location(the starting position) and returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('fire-'+repr(direction)+'-0.gif')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
        #__fire records the number of image
        self.__fire=0
        #__direction indicates where the fire should move
        self.__direction=direction
        self.rect.centerx=location[0]
        self.rect.bottom=location[1]
        
        #records the default position
        self.__center=(self.rect.center[0]+2820,self.rect.center[1])
        
    def change_picture(self):
        '''change_picture method changes the picture of fire to implement the effect of moving. It takes and returns nothing'''
        
        self.__fire+=1
        if self.__fire<=11:
            self.image=pygame.image.load('fire-'+repr(self.__direction)+'-'+repr(self.__fire)+'.gif')
        elif self.__fire<=75:
            self.image=pygame.image.load('fire-'+repr(self.__direction)+'-'+repr((self.__fire-4)%8+4)+'.gif')
        else:
            self.image=pygame.image.load('fire-'+repr(self.__direction)+'-'+repr((self.__fire-12)%8+12)+'.gif')
            
    def disappear(self):
        '''disappear method gives fire sprite the abillity of disappearing. It takes nothing and returns nothing'''
        
        if self.__fire>78:
            return True
            
    def update(self,location):
        '''The update method indicates where fire sprites should display on the map. It takes the change of location but returns nothing'''
        
        self.rect.center=(self.__center[0]-location[0],self.__center[1]-location[1])
        
class Health(pygame.sprite.Sprite):
    '''Health class creates two columns (of the ball and UFO) of health in stage 5. health sprites have ability to increase and decrease its size representing the increase or decrese of health of ball or UFO. The class inherits from the built-in sprite module'''
    
    def __init__(self,location,types):
        '''The __init__ method creates surface as the visual representation of health then fill the surface with color red. the method also assigns the starting position of sprite and amount of health ball or UFO has. parameter 'location' is starting position, 'types' indicate whether it's health of ball or UFO. It returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.Surface((0,0))
        self.image=self.image.convert()
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect()
        
        #use one variable to record location and which sprite does this health sprite belong to
        self.__location=[types,location[0],location[1]]
        #use the other variable to record the amount of health
        self.__amount=0
        
    def change(self,amount):
        '''change method directly controls the change in amount of health. It takes parameter amount to determine the amount of health increased or decreased then recreates health sprite with new length. It returns nothing'''
        
        self.__amount+=amount
        if self.__amount<0:
            self.__amount=0
        self.image=pygame.Surface((self.__amount,10))
        self.image=self.image.convert()
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect()
        if self.__location[0]:
            self.rect.right=self.__location[1]
        else:
            self.rect.left=self.__location[1]
        self.rect.centery=self.__location[2]
        
    def die(self):
        '''die method tells whether a sprite's health is zero or below. It takes nothing but returns True when amound of health is 0 or below'''
        
        if self.__amount==0:
            return True
        
    def remaining(self):
        '''remaining method tells how much health is left. It takes nothing but returns the value of __amount'''
        
        return self.__amount
        
class Background(pygame.sprite.Sprite):
    '''Background class creates the background that moves when the ball is moving. it gives the background the ability of moving. The class inherits from the built-in sprite module'''
    
    def __init__(self):
        '''__init__method only loads image of background. It does not assign the starting position of background. The method takes and returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('Background.png')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
    def update(self,location):
        '''update method gives background the ability of moving. but background can only move in a ratio to the value of location. the method takes location as parameter and returns nothing'''
        
        self.rect.left=-location[0]/2820.0*(1920-640)
        self.rect.top=-location[1]/2120.0*(1080-420)
        
class Label(pygame.sprite.Sprite): 
    ''' Label class creates labels that show important information on the screen or give the user choices. label sprites don't have the ability of moving.The class inherits from the builty-in sprite module''' 
    
    def __init__(self, message, x_y_center, font_size,color):
        '''__init__ method creates labels and assigns some variables. It uses user's font. parameter 'message' is the information on labels, 'x_y_center' is the starting position, 'font_size' is how big the font is as well as the color of font. The method returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        #records the user font
        self.__font =  pygame.font.Font("User.ttf", font_size)
        #records information
        self.__text = message 
        #records color of font
        self.__color=color
        
        self.image = self.__font.render(self.__text, 2, self.__color)
        self.rect = self.image.get_rect()
        self.rect.center=x_y_center
        
        #records default location
        self.__center=x_y_center
          
    def set_text(self, message):
        '''set_text method changes the information showing on the label. It accepts parameter message as new information. It returns nothing'''
        
        self.__text = message
    
    def colorchange(self,color):
        '''colorchange method changes color of the font. It accepts new color for the font and returns nothing'''
        
        self.__color=color
        
    def locationchange(self,location):
        '''locationchange method changes the position label sprites display on the screen. It accepts new location and returns nothing'''
        
        self.__center=location
        
    def left_top(self,location):
        '''left_top method sets top left corner (position) of label sprites. It accepts the location and returns nothing'''
        
        self.rect.left=location[0]
        self.rect.top=location[1]
        self.__center=self.rect.center
        
    def update(self): 
        '''update method recreates the labels with new values. the location of labels are still the same. this method takes nothing and returns nothing'''
        
        self.image = self.__font.render(self.__text, 1, self.__color)
        self.rect=self.image.get_rect()
        self.rect.center=self.__center
        
class Menu(pygame.sprite.Sprite):
    '''Menu class creates the menu and some other screens such as instruction and the one after ball explodes. It inherits from the built-in sprite module'''
    
    def __init__(self):
        '''__init__ method loads the menu picture for menu sprite. It also assigns the starting position. This method takes and returns nothing'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load('Menu.png')
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        
        self.rect.center=(320,240)
        
    def instruction(self):
        '''instruction method changes screen of menu sprite to instruction by changing picture. This mathod takes and returns nothing'''
        
        self.image=pygame.image.load('Instruction.png')
        self.image=self.image.convert()
        
    def menu(self):
        '''menu method changes screen of menu sprite to instruction by changing picture. This mathod takes and returns nothing'''
        
        self.image=pygame.image.load('Menu.png')
        self.image=self.image.convert()
        
    def continues(self):
        '''continues method changes screen of menu sprite to instruction by changing picture. This mathod takes and returns nothing'''
        
        self.image=pygame.image.load('Continue.png')
        self.image=self.image.convert()