##Initialisation##
#Imports
import pygame
import random

#Initial Variables
displayWidth = 1600
displayHeight = 900

diceWidth = 150
diceHeight = diceWidth

boardWidth = 735
boardHeight = 732

infoWidth = 500
infoHeight = 200

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
brightGreen = (150, 255, 150)

dicePositions = [[boardWidth + 50, 0], [0, 0], [0, 0], [0, 0]]
boardPositions = [[0, 0], [displayWidth - boardWidth, 0], [displayWidth - boardWidth, displayHeight - boardHeight], [0, displayHeight - boardHeight]]
infoPositions = [[displayWidth - infoWidth, displayHeight - infoHeight], [0, displayHeight - infoHeight], [0, 0], [displayWidth - infoWidth, 0]]

diceX = dicePositions[0][0]
diceY = dicePositions[0][1]

#Pygame Commands
random.seed()
pygame.init()
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Digital Monopoly")
clock = pygame.time.Clock()

##Game Procedures##
#Rolling 2 Six-Sided Die
def rollDice(givenDice, givenDice2):
    print(random.randint(1, 12))

#Checking Info About Board Spaces
def checkInfo(boardSpace, infoPosition):
    infoX = infoPosition[0]
    infoY = infoPosition[1]
    outline = 5
    titleSize = 50
    textSize = 25

    pygame.draw.rect(display, black, (infoX - outline, infoY - outline, infoWidth + (outline) * 2, infoHeight + (outline) * 2))
    pygame.draw.rect(display, white, (infoX, infoY, infoWidth, infoHeight))

    nameText = Text(boardSpace.getName(), infoX + outline, infoY + outline, titleSize)
    nameText.draw()
    groupText = Text(boardSpace.getGroup(), infoX + outline, infoY + (titleSize), textSize)
    groupText.draw()
    if boardSpace.getGroup() != "Special":
        priceText = Text("$" + str(boardSpace.getPrice()), infoX + outline, infoY + titleSize + (textSize), textSize)
        priceText.draw()

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
def changeBoard(boardObj, boardIndex):
    global boardPositions

    boardObj.setPosition(boardPositions[boardIndex][0], boardPositions[boardIndex][1])
    boardObj.changeImage(boardIndex)
    
##Classes##
#Text Class
class Text:
    _position = [0, 0]
    _font = ""
    _text = ""

    def __init__(self, givenText, givenPositionX, givenPositionY, givenSize = 50, givenFont = "Calibri"):
        self._text = givenText
        self._font = pygame.font.SysFont(givenFont, givenSize)
        self._position = [givenPositionX, givenPositionY]

    def draw(self):
        textSurf = self._font.render(self._text, True, black)
        textRect = textSurf.get_rect()
        textRect.topleft = (self._position[0], self._position[1])
        display.blit(textSurf, textRect)

    def changeText(self, newText):
        self._text = givenText

#Button Class
class Button:
    _inactiveColour = (0, 0, 0)
    _activeColour = (0, 0, 0)
    _position = [0, 0]
    _size = [0, 0]
    _selected = False

    def __init__(self, givenPosX, givenPosY, givenWidth, givenHeight, givenActiveColour = (128, 128, 128), givenInactiveColour = black):
        self._position = [givenPosX, givenPosY]
        self._size = [givenWidth, givenHeight]
        self._selected = False
        self._activeColour = givenActiveColour
        self._inactiveColour = givenInactiveColour
    
    def draw(self):
        mousePos = pygame.mouse.get_pos()
        if self._position[0] < mousePos[0] < self._position[0] + self._size[0] and self._position[1] < mousePos[1] < self._position[1] + self._size[1]:
            pygame.draw.rect(display, self._activeColour, (self._position[0], self._position[1], self._size[0], self._size[1]))
            self._selected = True
        else:
            pygame.draw.rect(display, self._inactiveColour, (self._position[0], self._position[1], self._size[0], self._size[1]))
            self._selected = False

    def setPosition(self, newPosX, newPosY):
        self._position = [newPosX, newPosY]

    def isSelected(self):
        return self._selected

#Text Button Class
class ImageButton(Button):
    _normalImage = ""
    _hoverImage = ""

    def __init__(self, givenNormalImage, givenHoverImage, givenPosX, givenPosY, givenWidth, givenHeight):
        super().__init__(givenPosX, givenPosY, givenWidth, givenHeight)
        self._normalImage = givenNormalImage
        self._hoverImage = givenHoverImage

    def draw(self):
        normalButton = pygame.image.load(self._normalImage)
        hoverButton = pygame.image.load(self._hoverImage)
        mousePos = pygame.mouse.get_pos()
        if self._position[0] < mousePos[0] < self._position[0] + self._size[0] and self._position[1] < mousePos[1] < self._position[1] + self._size[1]:
            display.blit(pygame.transform.rotate(hoverButton, 0), (self._position[0], self._position[1]))
            self._selected = True
        else:
            display.blit(pygame.transform.rotate(normalButton, 0), (self._position[0], self._position[1]))
            self._selected = False

#Image Class
class ImageCollection:
    __locations = [""]
    __selectedImage = 0
    __position = [0, 0]
    __rotation = 0

    def __init__(self, givenLocations, givenPositionX, givenPositionY, givenRotation = 0):
        self.__locations = givenLocations
        self.__position = [givenPositionX, givenPositionY]
        self.__rotation = -givenRotation
        self.__selectedImage = 0

    def draw(self):
        picture = pygame.image.load(self.__locations[self.__selectedImage])
        display.blit(pygame.transform.rotate(picture, self.__rotation), (self.__position[0], self.__position[1]))

    def setPosition(self, newPosX, newPosY):
        self.__position = [newPosX, newPosY]

    def getPosition(self):
        return self.__position

    def setRotation(self, newRotation):
        self.__rotation = -newRotation

    def changeImage(self, index):
        self.__selectedImage = circleLimit(0, len(self.__locations) - 1, index)

    def nextImage(self):
        self.__selectedImage = self.__selectedImage + 1
        if self.__selectedImage >= len(self.__locations):
            self.__selectedImage = 0

    def getIndex(self):
        return self.__selectedImage

    def getLength(self):
        return len(self.__locations)

#Token Class
class Token(ImageCollection):
    __tokens = ["train.png"]
    __currentSpace = None
    __currentIndex = 0
    __player = 0
    __cash = 0
    
    def __init__(self, givenPlayer, givenBoardSpace, givenImage, givenRotation = 0):
        super().__init__(self.__tokens, givenBoardSpace.getPosition(givenPlayer)[0], givenBoardSpace.getPosition(givenPlayer)[1], -givenRotation)
        self.__currentSpace = givenBoardSpace
        self.__player = givenPlayer
        self.__selectedImage = givenImage

    def getCurrentSpace(self):
        return self.__currentSpace

    def getCash(self):
        return self.__cash

    def addCash(self, newCash):
        self.__cash = self.__cash + newCash
        print("Player", self.__player, "has gained", newCash, "dollars.")
        
    def move(self, givenSpaces, givenBoardObj, givenBoardCollection):
        
        if self.__currentIndex == 0:
            self.addCash(200)
        self.__currentIndex = circleLimit(0, len(givenBoardObj) - 1, self.__currentIndex + givenSpaces)
        newSpace = givenBoardObj[self.__currentIndex]
        super().setPosition(newSpace.getPosition(self.__player)[0], newSpace.getPosition(self.__player)[1])
        if givenBoardCollection.getIndex() != newSpace.getBoard():
            global diceX
            global diceY
            diceX = dicePositions[newSpace.getBoard()][0]
            diceY = dicePositions[newSpace.getBoard()][1]
            
            changeBoard(givenBoardCollection, newSpace.getBoard())
        self.__currentSpace = newSpace
        super().setRotation(-newSpace.getRotation())
        if self.__currentIndex == 10 and self.__player == 2:
            super().setRotation(0)

#Board Space Class
class BoardSpace():
    __name = ""
    __position1 = [0, 0]
    __rotation = 0
    __board = 0
    __group = "Special"

    def __init__(self, givenName, givenPosX1, givenPosY1, givenPosX2, givenPosY2, givenRotation, givenBoard):
        self.__name = givenName
        self.__position1 = [boardPositions[givenBoard][0] + givenPosX1, boardPositions[givenBoard][1] + givenPosY1]
        self.__position2 = [boardPositions[givenBoard][0] + givenPosX2, boardPositions[givenBoard][1] + givenPosY2]
        self.__rotation = -givenRotation
        self.__board = givenBoard

    def getName(self):
        return self.__name

    def getPosition(self, givenPlayer):
        if givenPlayer == 1:
            return self.__position1
        else:
            return self.__position2

    def getRotation(self):
        return self.__rotation

    def getBoard(self):
        return self.__board

    def getGroup(self):
        return self.__group

    def setGroup(self, newGroup):
        self.__group = newGroup
    
#Property Class
class Property(BoardSpace):
    __price = 0
    
    def __init__(self, givenName, givenPrice, givenPosX1, givenPosY1, givenPosX2, givenPosY2, givenRotation, givenBoard):
        super().__init__(givenName, givenPosX1, givenPosY1, givenPosX2, givenPosY2, givenRotation, givenBoard)
        self.__price = givenPrice

    def getPrice(self):
        return self.__price

#Colour Grouped Property Class
class ColourGroupProperty(Property):
    __groups = ["Brown", "Light Blue", "Pink", "Orange", "Red", "Yellow", "Green", "Dark Blue"]

    def __init__(self, givenName, givenGroup, givenPrice, givenPosX1, givenPosY1, givenPosX2, givenPosY2, givenRotation, givenBoard):
        super().__init__(givenName, givenPrice, givenPosX1, givenPosY1, givenPosX2, givenPosY2, givenRotation, givenBoard)
        super().setGroup(self.__groups[givenGroup] + " Property")

##Main Game Loop##
if __name__ == "__main__":
    #Pygame Specific Variables
    closed = False
   
    boardImg = ImageCollection(["board_quarter1.jpg", "board_quarter2.jpg", "board_quarter3.jpg", "board_quarter4.jpg"], 0, 0)
    diceImg = ImageCollection(["dice_1.png", "dice_2.png", "dice_3.png", "dice_4.png", "dice_5.png", "dice_6.png"], diceX, diceY)
    diceImg2 = ImageCollection(["dice_1.png", "dice_2.png", "dice_3.png", "dice_4.png", "dice_5.png", "dice_6.png"], diceX + 175, diceY)
    
    #helloText = Text("Hello there!", 750, 0)
    movePlayer1 = Button(750, 300, 100, 100)
    movePlayer2 = Button(950, 300, 100, 100)
    roll2Dice = ImageButton("roll2Dice.png", "roll2DiceInverted.png", diceX + diceWidth + diceWidth + 100, diceY, 200, 100)
    checkSpace = Button(750, 500, 100, 100)

    #Board Spaces
    board = []
    board.append(BoardSpace("GO", 592, 632, 592, 662, 0, 0))
    
    board.append(ColourGroupProperty("Old Kent Road", 0, 60, 442, 632, 442, 662, 0, 0))
    
    board.append(BoardSpace("Community Chest", 322, 632, 322, 662, 0, 0))
    
    board.append(ColourGroupProperty("Whitechapel Road", 0, 60, 202, 632, 202, 662, 0, 0))
    
    board.append(BoardSpace("Income Tax", 82, 632, 82, 662, 0, 0))
    
    board.append(BoardSpace("Kings Cross Station", 698, 632, 698, 662, 0, 1))
    
    board.append(ColourGroupProperty("The Angel, Islington", 1, 100, 578, 632, 578, 662, 0, 1))
    
    board.append(BoardSpace("Chance", 458, 632, 458, 662, 0, 1))
    
    board.append(ColourGroupProperty("Euston Road", 1, 100, 338, 632, 338, 662, 0, 1))
    board.append(ColourGroupProperty("Pentonville Road", 1, 120, 218, 632, 218, 662, 0, 1))
    
    board.append(BoardSpace("Jail Visiting Area", 18, 562, 88, 692, 90, 1))
    
    board.append(ColourGroupProperty("Pall Mall", 2, 140, 78, 442, 48, 442, 90, 1))
    
    board.append(BoardSpace("Electric Company", 78, 322, 48, 322, 90, 1))
    
    board.append(ColourGroupProperty("Whitehall", 2, 140, 78, 202, 48, 202, 90, 1))
    board.append(ColourGroupProperty("Northumberland Avenue", 2, 160, 78, 82, 48, 82, 90, 1))
    
    board.append(BoardSpace("Marylbone Station", 78, 694, 48, 694, 90, 2))
    
    board.append(ColourGroupProperty("Bow Street", 3, 180, 78, 574, 48, 574, 90, 2))
    
    board.append(BoardSpace("Community Chest", 78, 454, 48, 454, 90, 2))
    
    board.append(ColourGroupProperty("Marlborough Street", 3, 180, 78, 334, 48, 334, 90, 2))
    board.append(ColourGroupProperty("Vine Street", 3, 200, 78, 214, 48, 214, 90, 2))
    
    board.append(BoardSpace("Free Parking", 68, 74, 68, 44, 180, 2))
    
    board.append(ColourGroupProperty("Strand", 4, 220, 218, 74, 218, 44, 180, 2))
    
    board.append(BoardSpace("Chance", 338, 74, 338, 44, 180, 2))
    
    board.append(ColourGroupProperty("Fleet Street", 4, 220, 458, 74, 458, 44, 180, 2))
    board.append(ColourGroupProperty("Trafalgar Square", 4, 240, 578, 74, 578, 44, 180, 2))
    
    board.append(BoardSpace("Fenchurch Street Station", -37, 74, -37, 44, 180, 3))
    
    board.append(ColourGroupProperty("Leicester Square", 5, 260, 83, 74, 83, 44, 180, 3))
    board.append(ColourGroupProperty("Coventry Street", 5, 260, 203, 74, 203, 44, 180, 3))
    
    board.append(BoardSpace("Water Works", 323, 74, 323, 44, 180, 3))
    
    board.append(ColourGroupProperty("Picadilly", 5, 280, 443, 74, 443, 44, 180, 3))
    
    board.append(BoardSpace("Go to Jail", 563, 74, 563, 44, 180, 3))
    
    board.append(ColourGroupProperty("Regent Street", 6, 300, 633, 214, 663, 214, 270, 3))
    board.append(ColourGroupProperty("Oxford Street", 6, 300, 633, 334, 663, 334, 270, 3))
    
    board.append(BoardSpace("Community Chest", 633, 454, 663, 454, 270, 3))
    
    board.append(ColourGroupProperty("Bond Street", 6, 320, 633, 574, 663, 574, 270, 3))
    
    board.append(BoardSpace("Liverpool Street Station", 633, 694, 663, 694, 270, 3))
    board.append(BoardSpace("Chance", 633, 82, 663, 82, 270, 0))
    
    board.append(ColourGroupProperty("Park Lane", 7, 350, 633, 202, 663, 202, 270, 0))
    
    board.append(BoardSpace("Super Tax", 633, 322, 663, 322, 270, 0))
    
    board.append(ColourGroupProperty("Mayfair", 7, 350, 633, 452, 663, 452, 270, 0))

    #Players
    player1 = Token(1, board[0], 0)
    player2 = Token(2, board[0], 0)

    infoBoard = False
    
    #While Loop
    while not closed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if roll2Dice.isSelected() == True:
                    rollDice(diceImg, diceImg2)
                elif movePlayer1.isSelected() == True:
                    player1.move(1, board, boardImg)
                elif movePlayer2.isSelected() == True:
                    player2.move(1, board, boardImg)
                elif checkSpace.isSelected() == True:
                    if infoBoard == True:
                        infoBoard = False
                    else:
                        infoBoard = True

        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_ESCAPE]:
            closed = True
    
        #Drawing to the Screen
        display.fill(white)
        diceImg.draw()
        diceImg2.draw()
        boardImg.draw()
        if boardImg.getIndex() == player1.getCurrentSpace().getBoard():
            player1.draw()
        if boardImg.getIndex() == player2.getCurrentSpace().getBoard():
            player2.draw()
        #helloText.draw()
        movePlayer1.draw()
        movePlayer2.draw()
        roll2Dice.draw()
        checkSpace.draw()

        if infoBoard == True:
            checkInfo(player1.getCurrentSpace(), infoPositions[player1.getCurrentSpace().getBoard()])
        
        #Updating the Display
        diceImg.setPosition(diceX, diceY)
        roll2Dice.setPosition(diceX + diceWidth + diceWidth + 50, diceY)
        pygame.display.update()
        clock.tick(60)

pygame.quit()
quit()
