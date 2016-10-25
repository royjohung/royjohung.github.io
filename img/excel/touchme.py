'''''''''''''''''''''''''''''
Roy Johung and Roger
Pittman Period 4
'''''''''''''''''''''''''''''

import random, sys, time, pygame
from pygame.locals import *

pygame.init()

fps = 30
windowwidth = 640
windowheight = 480
#this is in ms 
flashdelay = 200 
buttonsize = 200
gapsize = 20
timeout = 3 #time given before terminates

#colors listed and provided 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155,   0)
DARKGRAY = (40, 40, 40)
TURQUOISE = (64, 224, 208)
CREAM = (245, 255, 255)
bgColor = BLACK

xmargin = int((windowwidth - (2 * buttonsize) - gapsize) / 2)
ymargin = int((windowheight - (2 * buttonsize) - gapsize) / 2)

# Rect objects for each of the four buttons
YELLOWRECT = pygame.Rect(xmargin, ymargin, buttonsize, buttonsize)
BLUERECT   = pygame.Rect(xmargin + buttonsize + gapsize, ymargin, buttonsize, buttonsize)
REDRECT    = pygame.Rect(xmargin, ymargin + buttonsize + gapsize, buttonsize, buttonsize)
GREENRECT  = pygame.Rect(xmargin + buttonsize + gapsize, ymargin + buttonsize + gapsize, buttonsize, buttonsize)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Simon')

smallfont = pygame.font.SysFont("Impact", 15)
medfont = pygame.font.SysFont("Impact", 50)
largefont = pygame.font.SysFont("Impact", 80)

clock = pygame.time.Clock()#

#def scoreboard():
    
#start up menu
def game_intro():
    
    intro = True
    while intro:
        
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            
        gameDisplay.fill(TURQUOISE)
        message_to_screen("ATARI'S 1978 TOUCH ME",
                         CREAM,
                         -100,
                         size="medium")
        message_to_screen("The objective is memorize the light-up order of the squares. Good Luck!",
                         BLACK,
                         -30,
                         "small")
        message_to_screen("Remember as you progress to each level, the difficulty increases",
                         BLACK,
                         10,
                         "small")
        message_to_screen("If you submit the wrong pattern, then you will lose",
                         BLACK,
                         50,
                         "small")
        message_to_screen("Created by Roy Johung and Roger ",
                         BLACK,
                         250,
                         "small")
                    
        button("Play",250,450,100,50, GREEN, BRIGHTGREEN, action="Play")                                         
        button("Quit", 450,450,100,50, RED, BRIGHTRED, action="Quit")
                         
        pygame.display.update()
        clock.tick(15)

#the size that refers to the object of size
def text_objects(text,color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    
    return textSurface, textSurface.get_rect()
    
    #find button x and y and cut that by half to find the center
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)
    
    #display the start up text
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)
    
    #size of text
def button(text, x, y, width, height, inactive_color, active_color, action=()):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action !=None:
            if action == "Quit":
                pygame.quit()
                quit()
            if action == "Scoreboard":
                pass
            if action == "Play":
                main()
                
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,BLACK,x,y,width,height)                     
        
#entire program that dictates the functionallity 
def main():
    global fpsclock, displaysurf, basicfont, sound1, sound2, sound3, sound4

    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowwidth, windowheight))
    pygame.display.set_caption('')

    basicfont = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = basicfont.render('**', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, windowheight - 25)

    # load the sound files
    sound1 = pygame.mixer.Sound('beep1.ogg')
    sound2 = pygame.mixer.Sound('beep2.ogg')
    sound3 = pygame.mixer.Sound('beep3.ogg')
    sound4 = pygame.mixer.Sound('beep4.ogg')

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of colors
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True: # main game loop
        clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        displaysurf.fill(bgColor)
        drawButtons()
        
        #increases by one point when the clickedButtons agree
        scoreSurf = basicfont.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (windowwidth - 350, 10)
        displaysurf.blit(scoreSurf, scoreRect)
        

        displaysurf.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
        



        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(flashdelay)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - timeout > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                
        
        pygame.display.update()
        fpsclock.tick(fps)

#provides user to terminate the program
def terminate():
    pygame.quit()
    sys.exit()

#checks for quit previously inputted above
def checkForQuit():
    for event in pygame.event.get(QUIT): #gets the quit commands
        terminate() # terminates when quit is enabled
    for event in pygame.event.get(KEYUP): #get the keyup event
        if event.key == K_ESCAPE:
            terminate() #terminates when ESC key is pressed
        pygame.event.post(event) 

#direct and links to the color light up sequence
def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = sound1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = sound2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = sound3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = sound4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
        
#set up given for functions needed below
    origSurf = displaysurf.copy()
    flashSurf = pygame.Surface((buttonsize, buttonsize))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    #animation is endless
    for start, end, step in ((0, 255, 1), (255, 0, -1)): 
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            displaysurf.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            displaysurf.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            fpsclock.tick(fps)
    displaysurf.blit(origSurf, (0, 0))

#button drawn to display 
def drawButtons():
    pygame.draw.rect(displaysurf, YELLOW, YELLOWRECT)
    pygame.draw.rect(displaysurf, BLUE,   BLUERECT)
    pygame.draw.rect(displaysurf, RED,    REDRECT)
    pygame.draw.rect(displaysurf, GREEN,  GREENRECT)

        

# the overall animation when the user inputs the wrong pattern
def gameOverAnimation(color=RED, animationSpeed=100):
    # plays beep, then flashes
    origSurf = displaysurf.copy()
    flashSurf = pygame.Surface(displaysurf.get_size())
    flashSurf = flashSurf.convert_alpha()
    sound1.play() 
    sound2.play()
    sound3.play()
    sound4.play()
    r, g, b = color
    for i in range(3): # does the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # seconds from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                displaysurf.blit(origSurf, (0, 0))
                displaysurf.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                fpsclock.tick(fps)


#the notation of actual buttons to agree with one another
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE
    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    return None

game_intro()
if __name__ == '__main__':
    main()

    
