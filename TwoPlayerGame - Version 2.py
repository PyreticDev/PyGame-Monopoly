##Initialisation##
#Imports
import pygame
import random

#Initial Variables
displayWidth = 1600
displayHeight = 900
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
brightGreen = (150, 255, 150)

#Pygame Commands
random.seed()
pygame.init()
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Digital Monopoly")
clock = pygame.time.Clock()

##Game Procedures##
#Rolling 2 Six-Sided Die
def rollDice():
    return random.randint(1, 4)

#Keeping Integers Within Limits
def circleLimit(minimum, maximum, variable):
    circleRange = (maximum - minimum) + 1
    toBeReturned = variable
    while minimum > toBeReturned or toBeReturned > maximum:
        if toBeReturned > maximum:
            toBeReturned = toBeReturned - circleRange
        elif toBeReturned < minimum:
            toBeReturned = toBeReturned + circleRange
    return toBeReturned

#Changing the Board
def changeBoard(boardObj):
    global displayWidth
    global displayHeight
    
    currentIndex = boardObj.getIndex
    positions = [[0, 0], [displayWidth - 735, 0], [displayWidth - 735, displayHeight - 732], [0, displayHeight - 732]]

    boardObj.setPosition(positions[currentIndex + 1][0], positions[currentIndex + 1][1])
    boardObj.changeImage(currentIndex + 1)

##Classes##
#Text Class
class Text:
    __position = [0, 0]
    __font = ""
    __text = ""

    def __init__(self, givenText, givenPositionX, givenPositionY, givenFont = "Calibri", givenSize = 50):
        self.__text = givenText
        self.__font = pygame.font.SysFont(givenFont, givenSize)
        self.__position = [givenPositionX, givenPositionY]

    def draw(self):
        textSurf = self.__font.render(self.__text, True, black)
        textRect = textSurf.get_rect()
        textRect.topleft = (self.__position[0], self.__position[1])
        display.blit(textSurf, textRect)

    def changeText(self, newText):
        self.__text = givenText

#Button Class
class Button:
    __inactiveColour = (0, 0, 0)
    __activeColour = (0, 0, 0)
    __position = [0, 0]
    __size = [0, 0]
    __selected = False
    __action = None

    def __init__(self, givenPosX, givenPosY, givenWidth, givenHeight, givenAction, givenActiveColour = (128, 128, 128), givenInactiveColour = black):
        self.__position = [givenPosX, givenPosY]
        self.__size = [givenWidth, givenHeight]
        self.__selected = False
        self.__action = givenAction
        self.__activeColour = givenActiveColour
        self.__inactiveColour = givenInactiveColour
    
    def draw(self):
        if self.__selected == True:
            pygame.draw.rect(display, self.__activeColour, (self.__position[0], self.__position[1], self.__size[0], self.__size[1]))
        else:
            pygame.draw.rect(display, self.__inactiveColour, (self.__position[0], self.__position[1], self.__size[0], self.__size[1]))

    def mouseCheck(self):
        mousePos = pygame.mouse.get_pos()
        if self.__position[0] < mousePos[0] < self.__position[0] + self.__size[0] and self.__position[1] < mousePos[1] < self.__position[1] + self.__size[1]:
            self.__selected = True
        else:
            self.__selected = False

    def isSelected(self):
        return self.__selected

    def performAction(self):
        try:
            return self.__action()
        except(TypeError):
            self.__action()
        except:
            print("Something went wrong.")

#Image Class
class ImageCollection:
    __locations = [""]
    __selectedImage = 0
    __position = [0, 0]
    __rotation = 0

    def __init__(self, givenLocations, givenPositionX, givenPositionY, givenRotation = 0):
        self.__locations = givenLocations
        self.__position = [givenPositionX, givenPositionY]
        self.__rotation = givenRotation
        self.__selectedImage = 0

    def draw(self):
        picture = pygame.image.load(self.__locations[self.__selectedImage])
        display.blit(pygame.transform.rotate(picture, -self.__rotation), (self.__position[0], self.__position[1]))

    def setPosition(self, newPosX, newPosY):
        self.__position = [newPosX, newPosY]

    def getPosition(self):
        return self.__position

    def changeImage(self, index):
        self.__selectedImage = circleLimit(0, len(self.__locations) - 1, index)

    def nextImage(self):
        self.__selectedImage = self.__selectedImage + 1
        if self.__selectedImage >= len(self.__locations):
            self.__selectedImage = 0

    def getIndex(self):
        return self.__selectedImage

#Token Class
class Token(ImageCollection):
    __tokens = ["train.png"]
    
    def __init__(self, givenPositionX, givenPositionY, givenImage, givenRotation = 0):
        super().__init__(self.__tokens, givenPositionX, givenPositionY, givenRotation)
        self.__selectedImage = givenImage

    def moveTo(self, givenSpace):
        super().__position = givenSpace.getPosition()

#Board Space Class
class BoardSpace():
    __name = ""
    __position = [0, 0]
    __board = 0

    def __init__(self, givenName, givenPosX, givenPosY, givenBoard):
        self.__name = givenName
        self.__position = [givenPosX, givenPosY]
        self.__board = givenBoard

    def getPosition(self):
        return self.__position

    def getBoard(self):
        return self.__board

##Main Game Loop##
def gameLoop():
    #Pygame Specific Variables
    closed = False
    
    boardImg = ImageCollection(["board_quarter1.jpg", "board_quarter2.jpg", "board_quarter3.jpg", "board_quarter4.jpg"], 0, 0)
    #helloText = Text("Hello there!", 750, 0)
    movePlayer1 = Button(750, 0, 100, 100, rollDice)

    board = []
    board.append(BoardSpace("GO", boardImg.getPosition()[0] + 557, boardImg.getPosition()[1] + 632, 0))
    board.append(BoardSpace("Old Kent Road", boardImg.getPosition()[0] + 442, boardImg.getPosition()[1] + 632, 0))
    board.append(BoardSpace("Community Chest", boardImg.getPosition()[0] + 327, boardImg.getPosition()[1] + 632, 0))
    board.append(BoardSpace("Whitechapel Road", boardImg.getPosition()[0] + 212, boardImg.getPosition()[1] + 632, 0))
    board.append(BoardSpace("Income Tax", boardImg.getPosition()[0] + 97, boardImg.getPosition()[1] + 632, 0))
    
    player1Pos = 0
    player1 = Token(board[player1Pos].getPosition()[0], board[player1Pos].getPosition()[1], 0)
    
    #While Loop
    while not closed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if movePlayer1.isSelected() == True:
                    player1Pos = circleLimit(0, len(board) - 1, player1Pos + movePlayer1.performAction())
        
        #Drawing to the Screen
        display.fill(white)
        boardImg.draw()
        player1.draw()
        #helloText.draw()
        movePlayer1.draw()
        movePlayer1.mouseCheck()
        player1 = Token(board[player1Pos].getPosition()[0], board[player1Pos].getPosition()[1], 0)
        
        #Updating the Display
        pygame.display.update()
        clock.tick(60)

gameLoop()
pygame.quit()
quit()
