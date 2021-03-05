##Initialisation##
#Imports
import pygame

#Initial Variables
displayWidth = 1600
displayHeight = 900
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
brightGreen = (150, 255, 150)
clicked = False
boardImages = ["board_quarter1.jpg", "board_quarter2.jpg", "board_quarter3.jpg", "board_quarter4.jpg"]
icon = "train.png"
boardX = 0
boardY = 0
selectedBoard = 0

#Pygame Commands
pygame.init()
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Digital Monopoly")
clock = pygame.time.Clock()


##Classes##
#Image Class
class ImageCollection:
    __locations = [""]
    __selectedImage = 0
    __position = [0, 0]
    __rotation = 0

    def __init__(self, givenLocations, givenPositionX, givenPositionY, givenRotation):
        self.__locations = givenLocations
        self.__selectedImage = 0
        self.__position = [givenPositionX, givenPositionY]
        self.__rotation = givenRotation

    def draw(self):
        picture = pygame.image.load(self.__locations[self.__selectedImage])
        display.blit(pygame.transform.rotate(picture, -self.__rotation), (self.__position[0], self.__position[1]))

    def setPosition(self, newPosX, newPosY):
        self.__position = [newPosX, newPosY]
    
    def changeImage(self, index):
        if index < len(self.__locations) and index > -1:
            self.__selectedImage = index

    def nextImage(self):
        self.__selectedImage = self.__selectedImage + 1
        if self.__selectedImage >= len(self.__locations):
            self.__selectedImage = 0
    
#Drawing Images
def drawImage(image, imageX, imageY, rotation):
    boardImg = pygame.image.load(image)
    display.blit(pygame.transform.rotate(boardImg, -rotation), (imageX, imageY))

#Drawing Text
def drawText(text, size, textStartX, textStartY):
    textFont = pygame.font.SysFont("Calibri", size)
    textSurf = textFont.render(text, True, black)
    textRect = textSurf.get_rect()
    textRect.topleft = (textStartX, textStartY)
    display.blit(textSurf, textRect)

#Drawing Buttons
def drawTextButton(rectStartX, rectStartY, width, height, inactiveColour, activeColour, text, textSize, textStartX, textStartY, action = None):
    global clicked
    
    mousePos = pygame.mouse.get_pos()
    
    if rectStartX < mousePos[0] < rectStartX + width and rectStartY < mousePos[1] < rectStartY + height:
        pygame.draw.rect(display, activeColour, (rectStartX, rectStartY, width, height))
        if clicked == True and action != None:
            action()
            clicked = False
    else:
        pygame.draw.rect(display, inactiveColour, (rectStartX, rectStartY, width, height))
        
    drawText(text, textSize, textStartX, textStartY)

#Main Game Loop
def gameLoop():
    #Pygame Specific Variables
    global clicked
    closed = False
    position1 = [557, 632]

    board = ImageCollection(["board_quarter1.jpg", "board_quarter2.jpg", "board_quarter3.jpg", "board_quarter4.jpg"], 0, 0, 0)
    player1 = ImageCollection(["train.png"], 557, 632, 0)
    
    #While Loop
    while not closed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = True

        #Drawing to the Screen
        display.fill(white)
        #drawImage(boardImages[selectedBoard], boardX, boardY, 0)
        board.draw()
        #drawImage(icon, position1[0], position1[1], 0)
        player1.draw()
        drawTextButton(750, 0, 200, 200, green, brightGreen, "Change", 50, 775, 50, board.nextImage)
        
        #Updating the Display
        pygame.display.update()
        clock.tick(60)

gameLoop()
pygame.quit()
quit()
