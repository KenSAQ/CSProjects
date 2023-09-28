import pickle 
import sys

class BoardArray: 

    # creates the array 
    # only when you create instances of a class, do you allow parameters
    def __init__(self, boardinfo, boardnum):
        self.col = boardinfo[boardnum][numCol]
        self.row = boardinfo[boardnum][numRow]
        self.boardArray = [ ["" for i in range(self.col)] for i in range(self.row)]
        # self.board_rcoins = [ ["" for i in range(self.col)] for i in range(self.row)]
        # self.board_ycoins = [ ["" for i in range(self.col)] for i in range(self.row)]
        
    
    # prints array info
    def array_info(self):
        return self.boardArray
    
    #modify info on board
    def insert_coin(self, coinrow, coincol, whichPlayer):
        if whichPlayer == True:
            self.boardArray[coinrow][coincol] = "r"
            
        if whichPlayer == False:
            self.boardArray[coinrow][coincol] = "y"
    
    def resetBoard (self):
        for i in range (self.row):
            for j in range(self.col):
                self.boardArray[i][j] = ""
                # self.board_rcoins[i][j] = []
                # self.board_ycoins[i][j] = []


class CheckWinner:
    def __init__(self, boardinfo, boardnum):
        self.row = boardinfo[boardnum][3]
        self.col = boardinfo[boardnum][4]
        self.PIECE_NONE = ""
        self.directions = ((-1, -1), (-1, 0), (-1, 1),( 0, -1), ( 0, 1),( 1, -1), ( 1, 0), ( 1, 1))
    
    def board_info(self):
        return (self.col, self.row)
   
    
    def find_winner(self, board, winlength): #this function returns whether or not the board has a winner
    
        #this for loop checks each piece in the grid
        for row in range(self.row):
            for column in range(self.col):
                # if there is no piece present in that space on the grid, check the next piece
                if board[row][column] == (self.PIECE_NONE):
                    continue
    
                #if there is a piece present, invoke the check piece function to see if a connect 4 has been made              
                if self.check_piece(board, self.directions, row, column, winlength) == True:
                    print ("connect 4")
                    # print(board[row][column])
                    if board[row][column] == "r":
                        # print("r won")      
                        Rwon = True
                        Ywon = False
    
                    if board[row][column] == "y":
                        Rwon = False
                        Ywon = True
                    
                    # return board[row][column]
                    return (Rwon,Ywon)
        return (None, None)
    
    
    #don't say self.directions in the function, but say it when calling the function?
    def check_piece (self, board, directions, row, column, winlength):
        for dr, dc in self.directions:
            found_winner = True
        
            for i in range(1, winlength):
                #checking all the possible places around the coin up to 4 places away and determining which row or column it would be in 
                r = row + dr*i
                c = column + dc*i
    
                # if the place around the coin is not on the grid (e.g. has a row of -1), then now winner
                if r not in range(self.row) or c not in range(self.col):
                    found_winner = False
                    break
                    
                # if the places around the coin is not equal to the coin we're checking (e.g. no 2 red coins in a row), then no winner
                if board[r][c] != board[row][column]:
                    
                    found_winner = False
                    break
        
            if found_winner:
                return True
        
        return False
    
class Menu:
    def __init__(self, mode):
        self.showMenuBar = False
        self.img = 0
        self.sx = 1
        self.sy = 2
        self.sw = 3
        self.sh = 4
        self.dx = 5
        self.dy = 6
        self.dw = 7
        self.dh = 8
        self.modes = mode
    
    def showMenu(self, whichBoundary):
        for i in range (0,5):
            if whichBoundary == i: #click menu
                self.showMenuBar = True
            # print ("show menu")
    
        if 0 < mouseX < (canvasx-menubuttonw):
            self.showMenuBar = False
            # print ("no menu")
    
    def showMenuBar_info(self):
        return self.showMenuBar
    
    def menuButtonClicked (self, whichBoundary, activeBoundaries, gameStarted):
        imageMode(CORNER)
        copy(allImageInfo[1][self.img], allImageInfo[1][self.sx], allImageInfo[1][self.sy], allImageInfo[1][self.sw]+5, allImageInfo[1][self.sh]+822, allImageInfo[1][self.dx]+810, allImageInfo[1][self.dy]+10, allImageInfo[1][self.dw]-90, allImageInfo[1][self.dh]+305)
        # for i in range (1,5):
        #     if whichBoundary == i:
        #         activeBoundaries[i] = True
        for i in range (1,5,1):
            activeBoundaries[i] = True
                
        if whichBoundary == 1:
            print ("help page")
            self.modes = "helpScreen"
            activeBoundaries = [ False for i in range( numBoundaries ) ]
            #copy (allImageInfo[0][self.img], allImageInfo[0][self.sx] + 2000, allImageInfo[0][self.sy], allImageInfo[0][self.sw], allImageInfo[0][self.sh], allImageInfo[0][self.dx], allImageInfo[0][self.dy], allImageInfo[0][self.dw], allImageInfo[0][self.dh])
            
        if whichBoundary == 2:
            print("scores page")
            self.modes = "scoresScreen"

        if whichBoundary == 3 and self.modes != "helpScreen" and self.modes != "startScreen" and self.modes != "scoresScreen":
            print ("reset page")    
            self.modes = "reset"
            #put turn counter back to 0
            
            #reset the board

    
        if whichBoundary == 4 and self.modes != "gameScreen":
            print ("back button")
            print(gameStarted)
            if gameStarted == True:
                self.modes = "gameScreen"
                whichBoundary = -1
            if gameStarted == False:
                self.modes = "startScreen"
                whichBoundary = -1
        return self.modes
                        
def setup_scores():
    global scoresDict
    scoresDict = {}
    try:
        with open('highscores.pkl', 'rb') as file:
            scoresDict = pickle.load(file)
    except:
        score = 0



def save_score(name, score):
    new_score = (name, score)
    
    if new_score[0] in scoresDict:
        if new_score[1] < scoresDict[new_score[0]]:
            scoresDict[new_score[0]] = new_score[1]
    else:
        scoresDict[new_score[0]] = new_score[1]

    with open('highscores.pkl', 'wb') as file:
        pickle.dump(scoresDict, file)



def print_scores(scoresList):
    scores_sorted = sorted(scoresList,key=lambda l:l[1])
    # print(scores_sorted)
    for i in range (5):
        textSize(40)
        fill(0)
        text ("{}".format(scores_sorted[i][0]), 270, 465 + 55 * i)
        text ("{}".format(scores_sorted[i][1]), 640, 465 + 55 * i)

def scroll_scores(scoresList):
    global scrollup, scorestemp, scrolldown
    scores_sorted = sorted(scoresList,key=lambda l:l[1])
    scorestemp = []

    # scroll down
    if scrolldown + 5 <= len(scores_sorted):
        for i in range (scrolldown, scrolldown + 5):
            if i < len(scores_sorted):
                # print (i) 
                scorestemp.append (i)
    
    if scrolldown + 5 > len(scores_sorted):
        for i in range (len(scores_sorted)-5, len(scores_sorted), 1):
            scorestemp.append (i)
            # print (a[i])

    #scroll up
    if (scorestemp[0] - scrollup) <= 0:
        for i in range (5):
            scorestemp.append (i)
    
    if (scorestemp[0] - scrollup) > 0:
        for i in range (scrollup, scrollup + 5):
            scorestemp.append (i)

    # print (scorestemp)

    for i in range(5):
        textSize(40)
        fill(0)
        text ("{}".format(scores_sorted[scorestemp[i]][0]), 270, 465 + 55 * i)
        text ("{}".format(scores_sorted[scorestemp[i]][1]), 640, 465 + 55 * i)
        
    return (scorestemp)
     
    # print ( scrolldown)
    # print (scorestemp)
    
                        
   
def loadFileInfo( fileToRead ):
    file = open( fileToRead )
    fileInfo = []
    text = file.readlines()#turns the whole file into a peice of text

    for line in text:
        line = line.strip()
        line = line.split( "," )
        fileInfo.append( line )
    
    numItems = len( fileInfo )
    file.close()
                  
    return fileInfo, numItems 

def loadImageNames():
    file = open("images.txt")
    fileList = [] #Start with an empty list
    text = file.readlines()
     
    for line in text:
        line = line.strip() #Gets rid of end-of-line markers, etc.
        row = ""
        for c in line:
            row = row + c
        rowList = row.split( ",")
    file.close
    return ( rowList )

def loadImages( allBoardInfo, numImages, numBoards ):

    for i in range( numBoards ):
        for j in range( numImages ):
            allBoardInfo[ i ][ j ] = loadImage( allBoardInfo[ i ][ j ] )
    return( allBoardInfo )


class DropPiece:
    def __init__(self):                
        self.board_redcoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
        self.board_yellowcoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
        
    def board_rcoins_info(self):
        return self.board_redcoins
    
    def board_ycoins_info(self):
        return self.board_yellowcoins 



def drop_piece (column_left, column_num): 
    global board, boardw, boardh, boardx, boardy, row, columns, boardArray, board_rcoins, board_ycoins, boardcoin_size
    global rcoin, ycoin, rcoinx, rcoiny, rcoinw, rcoinh, ycoinx, ycoiny, ycoinw, ycoinh, player_turn, redcoinx, redcoiny, yelcoinx, yelcoiny
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint, gridColumns
    global allBoardInfo, boardImage, rcoinImage, ycoinImage, diceImage, numRow, numCol, boardNum
    global menubuttonx, menubuttony, menubuttonw, menubuttonh, menubar
    global menubar, menubarx, menubary, menubarw, menubarh
    global allImageList, menubar, helpChosen, scoresChosen
    global canvasx, cavnasy, showMenuBar
    global incrBallY, gravity, energyLoss
    global boardArray, PIECE_NONE, Winner, winningLength, DIRECTIONS
    global turnCounter
    global nameIn, nameIn2


    
    activeBoundaries = [ False for i in range( numBoundaries ) ]
    
    # incrBallY = 0
    # gravity = 25
    # energyLoss = 0.95
    
    fill(255)
    rect (0, 0, 1000, 900)
    
    fill(100)
    rect(0, 775, 270, 125)
    
    copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy], allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+810, allImageInfo[1][dy]+10, allImageInfo[1][dw]-90, allImageInfo[1][dh]-40)
    
    #comment?
    imageMode(CENTER)
    image ( allBoardInfo[boardNum][rcoinImage], redcoinx, redcoiny, allBoardInfo[boardNum][rcoinw], allBoardInfo[boardNum][rcoinh] )
    image ( allBoardInfo[boardNum][ycoinImage], yelcoinx, yelcoiny, allBoardInfo[boardNum][ycoinw], allBoardInfo[boardNum][ycoinh] )
    
    for i in range (len(board_rcoins)):
        for j in range (len(board_rcoins[i])):
            if len(board_rcoins[i][j]) != 0:
                imageMode(CENTER)
                image (allBoardInfo[boardNum][rcoinImage], board_rcoins[i][j][0], board_rcoins[i][j][1], allBoardInfo[boardNum][rcoinw], allBoardInfo[boardNum][rcoinh])
                
    for i in range (len(board_ycoins)):
        for j in range (len(board_ycoins[i])):
            if len(board_ycoins[i][j]) != 0:
                imageMode(CENTER)
                image (allBoardInfo[boardNum][ycoinImage], board_ycoins[i][j][0], board_ycoins[i][j][1], allBoardInfo[boardNum][ycoinw], allBoardInfo[boardNum][ycoinh])
                
    #comment?
    imageMode(CORNER)
    image( allBoardInfo[boardNum][boardImage], allBoardInfo[boardNum][boardx], allBoardInfo[boardNum][boardy], allBoardInfo[boardNum][boardw], allBoardInfo[boardNum][boardh])
                

    if player_turn == True:
        redcoinx = column_left + allBoardInfo[boardNum][rcoinw]/2
        incrBallY += gravity
        redcoiny  += incrBallY
        for i in range (len(board_rcoins)):
            if (len(board_rcoins[0][column_num - 1]) != 0 or len(board_ycoins[0][column_num - 1]) != 0): # if top if full, make them go to different column
                whichBoundary = -1
                break
            if (len(board_rcoins[i][column_num - 1])== 0 and len(board_ycoins[i][column_num - 1])== 0):
                if redcoiny > allBoardInfo[boardNum][boardy]+ allBoardInfo[boardNum][boardh] - allBoardInfo[boardNum][rcoinh]/2 :
                    redcoiny = allBoardInfo[boardNum][boardy]+ allBoardInfo[boardNum][boardh] - allBoardInfo[boardNum][rcoinh]/2 # coinY = bottom bound
                    #incrBallY = -incrBallY * energyLoss
                    whichBoundary = -1
                    board_rcoins[len(board_rcoins)-1][column_num - 1].append(redcoinx)
                    board_rcoins[len(board_rcoins)-1][column_num - 1].append(redcoiny)
                    boardArray_OOP.insert_coin(i-1,column_num - 1, player_turn)
                    player_turn = not player_turn
                    #print(boardArray)
                    turnCounter += 1
                    incrBallY = 0
                    break
            elif (len(board_rcoins[i][column_num - 1])!= 0 or len(board_ycoins[i][column_num - 1])!= 0):
                if redcoiny > (i) * boardcoin_size + allBoardInfo[boardNum][boardy] - allBoardInfo[boardNum][rcoinh]/2:
                    redcoiny = (i) * boardcoin_size + allBoardInfo[boardNum][boardy] - allBoardInfo[boardNum][rcoinh]/2
                    #incrBallY = -incrBallY * energyLoss
                    whichBoundary = -1
                    board_rcoins[i-1][column_num - 1].append(redcoinx)
                    board_rcoins[i-1][column_num - 1].append(redcoiny)
                    boardArray_OOP.insert_coin(i-1,column_num - 1, player_turn)
                    turnCounter += 1
                    incrBallY = 0
                    player_turn = not player_turn
                    break

    elif player_turn == False:
        yelcoinx = column_left + allBoardInfo[boardNum][ycoinw]/2 +10
        incrBallY += gravity
        yelcoiny  += incrBallY 
        for i in range (len(board_ycoins)):
            if (len(board_rcoins[0][column_num - 1]) != 0 or len(board_ycoins[0][column_num - 1]) != 0): # if top if full, make them go to different column
                whichBoundary = -1
                break
            if (len(board_rcoins[i][column_num - 1]) == 0 and len(board_ycoins[i][column_num - 1]) == 0): # if there's nothing in the column, go all the way down
                if yelcoiny > allBoardInfo[boardNum][boardy]+ allBoardInfo[boardNum][boardh] - allBoardInfo[boardNum][ycoinh]/2:
                    yelcoiny = allBoardInfo[boardNum][boardy]+ allBoardInfo[boardNum][boardh] - allBoardInfo[boardNum][ycoinh]/2 # coinY = bottom bound
                    #incrBallY = -incrBallY * energyLoss
                    whichBoundary = -1
                    board_ycoins[len(board_ycoins)-1][column_num - 1].append(yelcoinx)
                    board_ycoins[len(board_ycoins)-1][column_num - 1].append(yelcoiny)
                    boardArray_OOP.insert_coin(i-1,column_num - 1, player_turn)
                    player_turn = not player_turn
                    incrBallY = 0
                    break
            elif (len(board_rcoins[i][column_num - 1])!= 0 or len(board_ycoins[i][column_num - 1])!= 0):
                if yelcoiny > (i) * boardcoin_size + allBoardInfo[boardNum][boardy] - allBoardInfo[boardNum][ycoinh]/2:
                    yelcoiny = (i) * boardcoin_size + allBoardInfo[boardNum][boardy] - allBoardInfo[boardNum][ycoinh]/2
                    #incrBallY = -incrBallY * energyLoss
                    whichBoundary = -1
                    board_ycoins[i-1][column_num - 1].append(yelcoinx)
                    board_ycoins[i-1][column_num - 1].append(yelcoiny)
                    boardArray_OOP.insert_coin(i-1,column_num - 1, player_turn)
                    incrBallY = 0
                    player_turn = not player_turn
                    break

                
def setup_game():
    global whichKey, asciList, nameIn, nameIn2, nameLimit, nameCount1, nameCount2, mode, playerName, player2Name
    
    asciList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 01"
    nameIn = ""
    nameIn2 = ""
    whichKey = ""
    nameCount1 = 0
    nameCount2 = 0
    nameLimit = 10

    setup_scores()

    return
            
def setup():
    global board, boardw, boardh, boardx, boardy, row, columns, boardArray, board_rcoins, board_ycoins, boardcoin_size
    global rcoin, ycoin, rcoinx, rcoiny, rcoinw, rcoinh, ycoinx, ycoiny, ycoinw, ycoinh, coinY, player_turn, redcoinx, redcoiny, yelcoinx, yelcoiny
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint, gridColumns
    global game_over
    global allBoardInfo, boardImage, rcoinImage, ycoinImage, diceImage, numRow, numCol, boardNum
    global menubuttonx, menubuttony, menubuttonw, menubuttonh, menubar
    global menubar, menubarx, menubary, menubarw, menubarh
    global allImageList, menubar, helpChosen, scoresChosen
    global canvasx, cavnasy, showMenuBar
    global incrBallY, gravity, energyLoss
    global boardArray, empty_spot, Winner, winningLength, DIRECTIONS
    global turnCounter, gameStarted
    global playernameTurn
    global whichKey, asciList, nameIn, nameIn2, nameLimit, nameCount1, nameCount2, mode, playerName, player2Name
    global mode, allImageInfo, img, sx, sy, sw, sh, dx, dy, dw, dh
    global boardArray_OOP
    global drop_the_coin
    global space, spaceX, spaceY, spaceW, spaceH
    global rocket, rocketX, rocketY, rocketW, rocketH 
    global controlKeys, whichKey
    global leftBound, rightBound, rightside
    global incrCircle1, incrCircle2, incrCircle3, incrCircle4, incrCircle5
    global circle1x, circle1y, circle2x, circle2y, circle3x, circle3y, circle4x, circle4y, circle5x, circle5y, diameter
    global scrollup, scrolldown, scoresDict, scoresList, scrolling

    scrollup = 0
    scrolldown = 0
    scrolling = False
    
    playernameTurn = False
    player_turn = True
    game_over = False

    fill(255)
    size(1000, 900)
    canvasx = 999
    cavnasy = 899
    
    fill(255)
    rect (0, 0, canvasx, cavnasy)
    
    incrBallY = 0
    gravity = 5
    energyLoss = 0.95
    
    ####################################################################################################################make this more universal
    rows = 6
    columns = 7
    # boardArray= [ ["" for i in range(columns)] for i in range(rows)]
    # PIECE_NONE = ''
    Winner = None
    winningLength = 4
    turnCounter = 0
    
    # DIRECTIONS = (
    # (-1, -1), (-1, 0), (-1, 1),
    # ( 0, -1),          ( 0, 1),
    # ( 1, -1), ( 1, 0), ( 1, 1),
    # )
    
    #control variables for allBoardInfo
    numImages1 = 3
    numBoards = 2
    boardNum = 0
    
    #control variables for allImageInfo
    numImg = 2
    numImages2 = 1

    
    #allBoardInfo List Variables
    boardImage = 0
    rcoinImage = 1
    ycoinImage = 2
    numRow = 3
    numCol = 4
    boardx = 5
    boardy = 6
    boardw = 7
    boardh = 8
    rcoinx = 9
    rcoiny = 10
    rcoinw = 11
    rcoinh = 12
    ycoinx = 13
    ycoiny = 14
    ycoinw = 15
    ycoinh = 16
    
    #allImageInfo List Variables
    img = 0
    sx = 1
    sy = 2
    sw = 3
    sh = 4
    dx = 5
    dy = 6
    dw = 7
    dh = 8
    
    fileToRead = "boardinfo.txt"
    allBoardTextInfo, numBoards = loadFileInfo( fileToRead )
    allBoardInfo = loadImages( allBoardTextInfo, numImages1, numBoards )  
    
    
    for i in range( numBoards ):                                      # Changes the numbers in allBoardInfo from text to integer
        for j in range( numImages1, len( allBoardInfo[ i ] ) ):
            allBoardInfo[ i ][ j ] = int( allBoardInfo[ i ][ j ] )
            
    fileToRead = "imageinfo.txt"
    allImageTextInfo, numImg = loadFileInfo( fileToRead )
    allImageInfo = loadImages( allImageTextInfo, numImages2, numImg ) 
    
    for i in range( numImg ):                                      # Changes the numbers in allBoardInfo from text to integer
        for j in range( numImages2, len( allImageInfo[ i ] ) ):
            allImageInfo[ i ][ j ] = int( allImageInfo[ i ][ j ] )
    
    redcoinx = allBoardInfo[boardNum][rcoinx]
    redcoiny = allBoardInfo[boardNum][rcoiny]
    yelcoinx = allBoardInfo[boardNum][ycoiny]
    yelcoiny = allBoardInfo[boardNum][ycoiny]
    # print(allBoardInfo)
    
    player_turn = True
    game_over = False
    
    boardArray = [ ["" for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
    
    #MENU STUFF
    allBoundaries = []
    showMenuBar = False
    allBoundaries = []#boundaries get assigned every time you change the mode 
    menubuttonw = 190
    menubuttonh = 75
    menubuttonx = canvasx - menubuttonw
    menubuttony = 0
    # fill(255)
    # rect(menubuttonx, menubuttony, menubuttonw, menubuttonh)
    # fill(0)
    # textSize(50)  
    # text("MENU", 800, 70)
    
    # drop down menu
    upperLeft = [ menubuttonx, menubuttony ]                                        
    lowerRight = [ menubuttonx + menubuttonw, menubuttony + menubuttonh ]
    clickBoundary = [ upperLeft, lowerRight ]
    allBoundaries.append( clickBoundary )
    
    #menu bar
    menubarx = menubuttonx
    menubary = menubuttony + menubuttonh
    menubarw = menubuttonw
    menubarh = menubuttonh * 5
    numMenuItems = 4
    menuItemWidth = menubarw 
    menuItemHeight = menubarh / numMenuItems 
    
    #menu boundaries
    startLocX = menubarx 
    startLocY = menubary  
                                                                                                                                                                                                                                                                                         
    for i in range ( numMenuItems ): # Adding menu items to click areas
        upperLeft = [ startLocX, startLocY ]                                        
        lowerRight = [ startLocX + menuItemWidth, startLocY + menuItemHeight ]
        clickBoundary = [ upperLeft, lowerRight ]
        allBoundaries.append( clickBoundary )
        startLocY += menuItemHeight                                                                                                                                                                                                             

    playAreaWidth = canvasx - menubarw
    playAreaHeight = menubarh
    
    coinY = 25

    # boardArray = [ ["" for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
    # board_rcoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
    # board_ycoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
    
    #allBoundaries starting from whichBoundary = 5
    boardcoin_size = allBoardInfo[boardNum][boardh]/allBoardInfo[boardNum][numRow]
    allBoundaries.append([[150,700],[420,820]])
    allBoundaries.append([[550,700],[820,820]])
    allBoundaries.append([[85,360],[460,700]])
    allBoundaries.append([[550,360],[920,820]])
    allBoundaries.append([[25,785],[125,885]])
    allBoundaries.append([[146,789],[234,877]])
 
    #Boundary Variables
    numBoundaries = len( allBoundaries )#change according to what boundaries are in place in that mode 
    removeBoundary = False
    whichBoundary = -1
    activeBoundaries = [ False for i in range( numBoundaries ) ]
   
    menubar = loadImage( "menubar.png" )
    game_over = loadImage( "gameover.png" )


    drop_the_coin = DropPiece()
    board_rcoins = drop_the_coin.board_rcoins_info()
    board_ycoins = drop_the_coin.board_ycoins_info()
    
    setup_game()

    mode = "startScreen"
    # print(allBoundaries)
    
    spaceX = 0
    spaceY = 0
    spaceW = canvasx
    spaceH = cavnasy
    space = loadImage ("space.jpeg")
    
    rocketX = 440
    rocketY = 700
    rocketW = 150
    rocketH = 200
    rocket = loadImage ("rocket.png")
    
    controlKeys = [ UP, LEFT, RIGHT ]
    whichKey = -1
    
    leftBound = 0
    rightBound = canvasx - rocketW - 1
    rightside = canvasx
    
    # image (space, spaceX, spaceY, spaceW, spaceH)
    # image (rocket, rocketX, rocketY, rocketW, rocketH)
    
    diameter = 74
    incrCircle1 = 10
    incrCircle2 = 15
    incrCircle3 = 5
    incrCircle4 = 5    
    incrCircle5 = 10

    circle1x = 700
    circle1y = diameter/2
    circle2x = 200
    circle2y = 150
    circle3x = 500
    circle3y = 300
    circle4x = 300
    circle4y = 450
    circle5x = diameter/2
    circle5y = 600
    
    gameStarted = False
    
    scores = [{},{},{}]
    
def draw():
    global board, boardw, boardh, boardx, boardy, row, columns, boardArray, board_rcoins, board_ycoins, boardcoin_size
    global rcoin, ycoin, rcoinx, rcoiny, rcoinw, rcoinh, ycoinx, ycoiny, ycoinw, ycoinh, coinY, player_turn, redcoinx, redcoiny, yelcoinx, yelcoiny
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint, gridColumns
    global game_over
    global allBoardInfo, boardImage, rcoinImage, ycoinImage, diceImage, numRow, numCol, boardNum
    global menubuttonx, menubuttony, menubuttonw, menubuttonh, menubar
    global menubar, menubarx, menubary, menubarw, menubarh
    global allImageList, menubar, helpChosen, scoresChosen
    global canvasx, cavnasy, showMenuBar
    global incrBallY, gravity, energyLoss
    global boardArray, empty_spot, Winner, winningLength, DIRECTIONS
    global turnCounter, gameStarted
    global playernameTurn
    global whichKey, asciList, nameIn, nameIn2, nameLimit, nameCount1, nameCount2, mode, playerName, player2Name
    global mode, allImageInfo, img, sx, sy, sw, sh, dx, dy, dw, dh
    global boardArray_OOP
    global drop_the_coin
    global space, spaceX, spaceY, spaceW, spaceH
    global rocket, rocketX, rocketY, rocketW, rocketH 
    global controlKeys, whichKey
    global leftBound, rightBound, rightside
    global incrCircle1, incrCircle2, incrCircle3, incrCircle4, incrCircle5
    global circle1x, circle1y, circle2x, circle2y, circle3x, circle3y, circle4x, circle4y, circle5x, circle5y, diameter
    global scrollup, scrolldown, scoresDict, scoresList, scrolling
    
    if mode == "startScreen":
        imageMode(CORNER)
        copy(allImageInfo[0][img], allImageInfo[0][sx], allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
        copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(5*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+150, allImageInfo[1][dy]+700, allImageInfo[1][dw], allImageInfo[1][dh])
        copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(1*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+550, allImageInfo[1][dy]+700, allImageInfo[1][dw], allImageInfo[1][dh])
        numBoundaries = len(allBoundaries)
        if whichBoundary == -1:
            activeBoundaries = [ True for i in range( numBoundaries ) ]

        if 150 < mouseX < 420 and 700 < mouseY < 820: 
            copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(5*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+140, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
            
        if 550 < mouseX < 820 and 700 < mouseY < 820:
            copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(1*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+540, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
            
        if whichBoundary == 5:
            mode = "nameScreen"
            setup_game()
            copy(allImageInfo[0][img], allImageInfo[0][sx] + int(1*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
            whichBoundary = -1
            
        elif whichBoundary == 6:
            mode = "helpScreen"
            copy(allImageInfo[0][img], allImageInfo[0][sx] + int(2*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
            whichBoundary = -1
            
    if mode == "nameScreen":
        fill( 10 )
        textSize ( 25 )            
        activeBoundaries = [False for i in range (numBoundaries)]
        if ( whichKey == "0" ) or ( nameCount1 >= nameLimit ):
            playernameTurn = True
            playerName = nameIn    
        elif ( whichKey == "1" ) or ( nameCount2 >= nameLimit ):
            mode = "boardScreen"
            player2Name = nameIn2 
            #set up game function here?  
        else: 
            if whichKey != "" and playernameTurn == False:
                nameIn += whichKey.upper()
                nameCount1 += 1
                text( nameIn, 350, 430 )
                
        if playernameTurn == True and whichKey != "" and whichKey != "0" and whichKey != "1":
            nameIn2 += whichKey.upper()
            nameCount2 += 1
            text( nameIn2, 350, 575 )
            
        text( nameIn, 350, 430 )
        text( nameIn2, 350, 575 )
        whichKey = ""
    if mode == "boardScreen":
        if whichBoundary == -1:
            activeBoundaries = [ False for i in range( numBoundaries ) ]
            activeBoundaries[7] = True
            activeBoundaries[8] = True
            
        copy(allImageInfo[0][img], allImageInfo[0][sx] + int(3*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
        
        if whichBoundary == 7:
            boardNum = 0
            #boardArray = [ ["" for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
            board_rcoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
            board_ycoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
            for i in range (0,allBoardInfo[boardNum][numCol]):
                allBoundaries.append([[allBoardInfo[boardNum][boardx] + allBoardInfo[boardNum][boardw]/allBoardInfo[boardNum][numCol]*i, 0], [allBoardInfo[boardNum][boardx] + allBoardInfo[boardNum][boardw]/allBoardInfo[boardNum][numCol]*(i+1), allBoardInfo[boardNum][boardy]]])
            numBoundaries = len( allBoundaries )
            whichBoundary = -1
            boardArray_OOP = BoardArray(allBoardInfo, boardNum)
            boardArray = boardArray_OOP.array_info()
            mode = "gameScreen"
        if whichBoundary == 8:
            boardNum = 1
            #boardArray = [ ["" for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
            board_rcoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
            board_ycoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
            for i in range (0,allBoardInfo[boardNum][numCol]):
                allBoundaries.append([[allBoardInfo[boardNum][boardx] + allBoardInfo[boardNum][boardw]/allBoardInfo[boardNum][numCol]*i, 0], [allBoardInfo[boardNum][boardx] + allBoardInfo[boardNum][boardw]/allBoardInfo[boardNum][numCol]*(i+1), allBoardInfo[boardNum][boardy]]])
            numBoundaries = len( allBoundaries )
            whichBoundary = -1
            boardArray_OOP = BoardArray(allBoardInfo, boardNum)
            boardArray = boardArray_OOP.array_info()
            mode = "gameScreen"
            
    if mode == "helpScreen" :    
        copy(allImageInfo[0][img], allImageInfo[0][sx] + int(2*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
        
        if whichBoundary == -1:
            activeBoundaries = [ False for i in range( numBoundaries ) ]
            activeBoundaries [0] = True
            
        #load menu button
        copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy], allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+810, allImageInfo[1][dy]+10, allImageInfo[1][dw]-90, allImageInfo[1][dh]-40)
        
        ifshowMenuBar = Menu(mode)
        ifshowMenuBar.showMenu (whichBoundary)
        
        if ifshowMenuBar.showMenuBar_info() == True:
            mode = ifshowMenuBar.menuButtonClicked (whichBoundary, activeBoundaries, gameStarted)
            
    if mode == "gameScreen":
        if whichBoundary == -1:
            activeBoundaries = [ False for i in range( numBoundaries ) ]
        fill(255)
        rect (0, 0, 1000, 900)
        
        gameStarted = True
        
        for i in range (len(board_rcoins)):
            for j in range (len(board_rcoins[i])):
                if len(board_rcoins[i][j]) != 0:
                    imageMode(CENTER)
                    image (allBoardInfo[boardNum][rcoinImage], board_rcoins[i][j][0], board_rcoins[i][j][1],allBoardInfo[boardNum][rcoinw], allBoardInfo[boardNum][rcoinh])
                    
        for i in range (len(board_ycoins)):
            for j in range (len(board_ycoins[i])):
                if len(board_ycoins[i][j]) != 0:
                    imageMode(CENTER)
                    image (allBoardInfo[boardNum][ycoinImage], board_ycoins[i][j][0], board_ycoins[i][j][1],allBoardInfo[boardNum][ycoinw], allBoardInfo[boardNum][ycoinh])
                    
        # print(board_rcoins)
        # print(board_ycoins)
                    
        #load board image
        imageMode(CORNER)
        image( allBoardInfo[boardNum][boardImage], allBoardInfo[boardNum][boardx], allBoardInfo[boardNum][boardy], allBoardInfo[boardNum][boardw], allBoardInfo[boardNum][boardh] )
    
        #load coin rectangle background
        fill(100)
        rect(0, 775, 270, 125)    
        
        #load coin images
        imageMode(CENTER)
        image ( allBoardInfo[boardNum][rcoinImage], redcoinx, redcoiny, allBoardInfo[boardNum][rcoinw], allBoardInfo[boardNum][rcoinh] )
        image ( allBoardInfo[boardNum][ycoinImage], yelcoinx, yelcoiny, allBoardInfo[boardNum][ycoinw], allBoardInfo[boardNum][ycoinh] )
        
        #load menu button
        copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy], allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+810, allImageInfo[1][dy]+10, allImageInfo[1][dw]-90, allImageInfo[1][dh]-40)
        #activeBoundaries = [ False for i in range( numBoundaries ) ]
        #activeBoundaries [0] = True
        
        #create all boundaries for board based on whose turn it is
        if whichBoundary == -1:
            activeBoundaries = [ False for i in range( numBoundaries ) ]
            activeBoundaries[0] = True
            if player_turn == True:
                activeBoundaries[9] = True
            if player_turn == False:
                activeBoundaries[10] = True
            redcoinx = allBoardInfo[boardNum][rcoinx]
            redcoiny = allBoardInfo[boardNum][rcoiny]
            yelcoinx = allBoardInfo[boardNum][ycoinx]
            yelcoiny = allBoardInfo[boardNum][ycoiny]


        ifshowMenuBar = Menu(mode)
        ifshowMenuBar.showMenu (whichBoundary)
        
        if ifshowMenuBar.showMenuBar_info() == True:
            mode = ifshowMenuBar.menuButtonClicked (whichBoundary, activeBoundaries, gameStarted)

            
        if whichBoundary == 9 or whichBoundary == 10:
            #print(whichBoundary)
            for i in range (11,len(activeBoundaries)):
                activeBoundaries[i] = True
        
        for i in range (11, len(allBoundaries)):
            boardcoin_size = allBoardInfo[boardNum][boardh]/allBoardInfo[boardNum][numRow]
            if whichBoundary == i:
                drop_piece(allBoardInfo[boardNum][boardx] + (whichBoundary - 11) * boardcoin_size, whichBoundary - 10)

        whichKey = ""
        checkedBoard = CheckWinner(allBoardInfo, boardNum)
        Winner = checkedBoard.find_winner(boardArray, winningLength) 
        if Winner[0] or Winner [1] == True:
            if Winner [0] == True:
                save_score(playerName, turnCounter)
                scoresList = list(scoresDict.items())
                print_scores(scoresList)
                textSize(50)
                fill (0)
                copy(allImageInfo[0][img], allImageInfo[0][sx] + int(4*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
                text( turnCounter , 350, 575 ) 
                copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(6*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+140, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(7*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+540, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                numBoundaries = len(allBoundaries)
                if whichBoundary == -1:
                    activeBoundaries = [ False for i in range( numBoundaries ) ]
                    activeBoundaries[5] = True
                    activeBoundaries[6] = True
        
                if 150 < mouseX < 420 and 700 < mouseY < 820: 
                    copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(6*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+140, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                    
                if 550 < mouseX < 820 and 700 < mouseY < 820:
                    copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(7*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+540, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                    
                if whichBoundary == 5:
                    mode = "boardScreen"
                    turnCounter = 0
                    player_turn = True
                    setup_game()
                    whichBoundary = -1
                    
                elif whichBoundary == 6:
                    mode = "exitScreen"
                    whichBoundary = -1
            if Winner [1] == True:
                save_score(player2Name, turnCounter)
                scoresList = list(scoresDict.items())
                print_scores(scoresList)
                textSize(50)
                fill (0)
                copy(allImageInfo[0][img], allImageInfo[0][sx] + int(5*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
                text( turnCounter , 350, 575 ) 
                copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(6*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+140, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(7*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+540, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                numBoundaries = len(allBoundaries)
                if whichBoundary == -1:
                    activeBoundaries = [ False for i in range( numBoundaries ) ]
                    activeBoundaries[5] = True
                    activeBoundaries[6] = True
        
                if 150 < mouseX < 420 and 700 < mouseY < 820: 
                    copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(6*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+140, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                    
                if 550 < mouseX < 820 and 700 < mouseY < 820:
                    copy(allImageInfo[1][img], allImageInfo[1][sx], allImageInfo[1][sy] + int(7*205.3), allImageInfo[1][sw]+5, allImageInfo[1][sh], allImageInfo[1][dx]+540, allImageInfo[1][dy]+690, allImageInfo[1][dw]+20, allImageInfo[1][dh]+20)
                    
                if whichBoundary == 5:
                    mode = "boardScreen"
                    turnCounter = 0
                    player_turn = True
                    setup_game()
                    whichBoundary = -1
                    
                elif whichBoundary == 6:
                    mode = "exitScreen"
                    whichBoundary = -1
                    
    if mode == "scoresScreen":
        copy(allImageInfo[0][img], allImageInfo[0][sx] + int(6*1167), allImageInfo[0][sy], allImageInfo[0][sw], allImageInfo[0][sh], allImageInfo[0][dx], allImageInfo[0][dy], allImageInfo[0][dw], allImageInfo[0][dh])  
        if whichBoundary == -1:
            activeBoundaries = [ False for i in range( numBoundaries ) ]
            activeBoundaries [0] = True
        
        ifshowMenuBar = Menu(mode)
        ifshowMenuBar.showMenu (whichBoundary)
        
        if ifshowMenuBar.showMenuBar_info() == True:
            mode = ifshowMenuBar.menuButtonClicked (whichBoundary, activeBoundaries, gameStarted)
        
        scrolling = True
        if scrolldown == 0 and scrollup == 0:
            scoresList = list(scoresDict.items())
            print_scores(scoresList)
        
        if scrolling == True:
            controlKeys = [ UP, DOWN]        
            if ( whichKey == UP ):
                print ( "UP" )
                scrollup += 1
                scrolldown = 0
                scorestemp = []
                scroll_scores(scoresList)
        
            elif ( whichKey == DOWN ):
                print ( "DOWN" )
                scrolldown += 1
                scrollup = 0
                scorestemp = []
                scroll_scores(scoresList)

    if mode == "reset":
        board_rcoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
        board_ycoins = [ [[] for i in range(allBoardInfo[boardNum][numCol])] for i in range(allBoardInfo[boardNum][numRow])]
        player_turn = True
        boardArray_OOP.resetBoard()
        print(boardArray)
        mode = "gameScreen"
    if mode == "exitScreen":
        controlKeys = [ UP, LEFT, DOWN, RIGHT ]      
        image (space, spaceX, spaceY, spaceW*2.3, spaceH*2.3)
        image (rocket, rocketX, rocketY, rocketW, rocketH)
        
        fill (150)
        circle (circle1x, circle1y, diameter)
        circle (circle2x, circle2y, diameter)
        circle (circle3x, circle3y, diameter)
        circle (circle4x, circle4y, diameter)
        circle (circle5x, circle5y, diameter)
        
        fill(255) #shows the number of turns player takes
        rect(0,800,375,100)
        textSize(15)
        fill(0)
        text("Use UP, LEFT, and RIGHT keys to move the rocket", 10, 830)
        text("Don't get hit by the meteors!", 10, 850)
                
        if rocketX > rightBound:
            rocketX = rightBound
        if rocketX < leftBound:
            rocketX = leftBound
        
        if whichKey == UP:
            rocketY -= 40
            whichKey = -1
        if whichKey == LEFT:
            rocketX -= 40
            whichKey = -1        
        if whichKey == RIGHT:
            rocketX += 40
            whichKey = -1
                    
        if rocketY <= 0:
            print ("won the game")
            controlKeys = []
        
        circle1x += incrCircle1
        circle2x += incrCircle2
        circle3x += incrCircle3
        circle4x += incrCircle4
        circle5x += incrCircle5
    
        if circle1x < diameter/2:
            circle1x = diameter/2
            incrCircle1 = -incrCircle1    
        if circle1x > (rightside - diameter/2):
            circle1x = rightside - diameter/2
            incrCircle1 = -incrCircle1        
        if circle2x < diameter/2:
            circle2x = diameter/2
            incrCircle2 = -incrCircle2
        if circle2x > (rightside - diameter/2):
            circle2x = rightside - diameter/2
            incrCircle2 = -incrCircle2        
        if circle3x < diameter/2:
            circle3x = diameter/2
            incrCircle3 = -incrCircle3    
        if circle3x > (rightside - diameter/2):
            circle3x = rightside - diameter/2
            incrCircle3 = -incrCircle3
        if circle4x < diameter/2:
            circle4x = diameter/2
            incrCircle4 = -incrCircle4
        if circle4x > (rightside - diameter/2):
            circle4x = rightside - diameter/2
            incrCircle4 = -incrCircle4     
        if circle5x < diameter/2:
            circle5x = diameter/2
            incrCircle5 = -incrCircle5    
        if circle5x > (rightside - diameter/2):
            circle5x = rightside - diameter/2
            incrCircle5 = -incrCircle5         
        
        if (circle1x - diameter/2) < (rocketX + rocketW/2) < (circle1x + diameter/2) and rocketY < circle1y < (rocketY +rocketH):
            rocketX = 440
            rocketY = 700    
        if (circle2x - diameter/2) < (rocketX + rocketW/2) < (circle2x + diameter/2) and rocketY < circle2y < (rocketY +rocketH):
            rocketX = 440
            rocketY = 700
        if (circle3x - diameter/2) < (rocketX + rocketW/2) < (circle3x + diameter/2) and rocketY < circle3y < (rocketY +rocketH):
            rocketX = 440
            rocketY = 700
        if (circle4x - diameter/2) < (rocketX + rocketW/2) < (circle4x + diameter/2) and rocketY < circle4y < (rocketY +rocketH):
            rocketX = 440
            rocketY = 700
        if (circle5x - diameter/2) < (rocketX + rocketW/2) < (circle5x + diameter/2) and rocketY < circle5y < (rocketY +rocketH):
            rocketX = 440
            rocketY = 700
        
        if rocketY <= 0:
            print("exited game")
            sys.exit()

def keyReleased():
    global whichKey, asciList, controlKeys
    if key == CODED:
       if keyCode in controlKeys:
        whichKey = keyCode
    elif key in asciList:
        whichKey = key
    else:
        whichKey = ''   


def mousePressed():
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint
    
    validLocation = False 

    for i in range( numBoundaries ): 
        if activeBoundaries[ i ]:
            validXRange = allBoundaries[i][0][0] <= mouseX <= allBoundaries[i][1][0]  
            validYRange = allBoundaries[i][0][1]  <= mouseY <= allBoundaries[i][1][1]
            validLocation = validXRange and validYRange

            if validLocation: 
                
                whichBoundary = i
                #whichBoundary points to the boundary that its clicked at. So whichBoundary = 0 would point to the boundary within the x&y values of allBoundaries[i][0]
                break
            
    if validLocation and removeBoundary: 
        activeBoundaries[ whichBoundary ] = False 
        
def mouseDragged():
    global board, boardw, boardh, boardx, boardy
    global rcoin, ycoin, rcoinx, rcoiny, rcoinw, rcoinh, ycoinx, ycoiny, ycoinw, ycoinh, coinY, player_turn, redcoinx, redcoiny, yelcoinx, yelcoiny
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint
    global allBoardInfo, boardImage, rcoinImage, ycoinImage, diceImage, numRow, numCol, boardNum

    if whichBoundary == 9:
        redcoinx = mouseX
        redcoiny = mouseY
            
    if whichBoundary == 10:
        yelcoinx = mouseX
        yelcoiny = mouseY
            
    
def mouseReleased():
    global board, boardw, boardh, boardx, boardy
    global rcoin, ycoin, rcoinx, rcoiny, rcoinw, rcoinh, ycoinx, ycoiny, ycoinw, ycoinh, coinY, player_turn
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint
    global allBoardInfo, boardImage, rcoinImage, ycoinImage, diceImage, numRow, numCol, boardNum
    
    validLocation = False 

    for i in range( numBoundaries ): 
        if activeBoundaries[ i ]:
            validXRange = allBoundaries[i][0][0] <= mouseX <= allBoundaries[i][1][0]  
            validYRange = allBoundaries[i][0][1]  <= mouseY <= allBoundaries[i][1][1]
            validLocation = validXRange and validYRange

            if validLocation: 
                
                whichBoundary = i
                #whichBoundary points to the boundary that its clicked at. So whichBoundary = 0 would point to the boundary within the x&y values of allBoundaries[i][0]
                break
            
    if validLocation and removeBoundary: 
        activeBoundaries[ whichBoundary ] = False
   
    if validLocation == False:
        whichBoundary = -1 
