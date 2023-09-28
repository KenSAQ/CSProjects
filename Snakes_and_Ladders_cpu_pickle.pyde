#Ken and Caitlyns Snakes and Ladders game
#=========================================================================================================================================================================
import random
import pickle
#===========================================================================================================================================================================
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
#=========================================================================================================================================================================
def loadImages( allBoardInfo, numImages, numBoards ):

    for i in range( numBoards ):
        for j in range( numImages ):
            allBoardInfo[ i ][ j ] = loadImage( allBoardInfo[ i ][ j ] )
    return( allBoardInfo )
#==================================================================================================================================================================
def setup():
    global allBoardInfo, boardImage, player2Image, player1Image, diceImage, bannerImage, numCol, numRow, factorX, factorY, boardWidth, boardHeight, mode, boardNum, startScreen, time, goCPU, click, topPlayer, leaderboardList
    global allPlayerInfo, playerPosX, playerPosY, playerWidth, playerHeight, playerCount, player1,chooseBoard,playerScore, gameState,help,helpButton, scores, leaderBoard
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, whereList,nameCount1,nameIn1,nameLimit,leaderBoardButton, controlKeys
    global whichKey, asciList, menu,exitScreen
    
    size(800, 700)
    numImages = 5
    boardWidth = 600
    boardHeight = 600
    boardNum = 0
    
    #Vaiables for getting names
    asciList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0"
    controlKeys = []
    whichKey = ''
    nameCount1 = 0
    nameIn1 = ''
    nameLimit = 15
    
    #allBoardInfo List Variables
    boardImage = 0
    player2Image = 1
    player1Image = 2
    diceImage = 3
    bannerImage = 4
    numCol = 5
    numRow = 6
    factorX = 7
    factorY = 8
    
    fileToRead = "boardinfo.txt" # Gets content of file and number of boards puts in allBoardTextInfo
    allBoardTextInfo, numBoards = loadFileInfo( fileToRead )
    allBoardInfo = loadImages( allBoardTextInfo, numImages, numBoards )   # Loads the images into list called allBoardInfo using allBoardTextInfo
    
    for i in range( numBoards ):                                      # Changes the numbers in allBoardInfo from text to integer
        for j in range( numImages, len( allBoardInfo[ i ] ) ):
            allBoardInfo[ i ][ j ] = int( allBoardInfo[ i ][ j ] )
            numSpaces = allBoardInfo[i][numCol] * allBoardInfo[i][numRow] #generate number of spaces on board 

    #Modes/States
    gameState = "Beginning"#for help button to direct to the correct part of the game
    mode = "startScreen"
    
    #allPlayerInfo List Variables
    playerPosX = 0
    playerPosY = 1
    playerWidth = 2
    playerHeight = 3
    playerCount = 4
    
    player1 = False
    
    #CPU Variables 
    time = 0 #collect time to delay CPU  
    goCPU = False #boolean variable that controls when CPU should go 
    
    #intialize wherelist for each board
    whereList = []
    whereList.append([i for i in range(30)])
    whereList.append([i for i in range(100)])
    whereList.append([i for i in range(64)])    
    
    #edit whereList values based on snakes and ladders 
    for i in range( numBoards ): 
        for w in range( 9, len(allBoardInfo[ i ]),2):
            if allBoardInfo[ i ][ w ] in whereList [ i ]:
                whereList[ i ][allBoardInfo[ i ][ w ]] = allBoardInfo[ i ][ w+1 ]
    
    #Image variables
    startScreen = loadImage("snakes and ladders start.png")
    chooseBoard = loadImage("getboard.png")
    help = loadImage("helpScreen.png")
    menu = loadImage("menu.png")
    leaderBoard = loadImage("leaderboard.png")
    exitScreen = loadImage("Exit screen.png")
    
    #Boundary Variables
    allBoundaries = []#boundaries get assigned every time you change the mode 
    numBoundaries = 0#change according to what boundaries are in place in that mode 
    removeBoundary = False
    whichBoundary = -1
    activeBoundaries = [ True for i in range( numBoundaries ) ]
    
    click = 0
    scores = [{},{},{}]
#============================================================================================================================================        
def do_pickle():
    global used,click,nameIn1,scores, leaderboardList
    try:
        with open('scores.pkl','rb') as file: #rb stands for read bytes
            l = pickle.load(file)
            file.close()
            
        with open('scores.pkl', 'wb') as file: #wb stands for write bytes
            if click in l[boardNum]:
                l[boardNum][click].append(nameIn1)
            else:
                l[boardNum][click] = [nameIn1]
            pickle.dump(l,file)
            file.close()
        
    except:
        with open('scores.pkl', 'wb') as file:
            pickle.dump(scores, file)
            file.close()
    
        with open('scores.pkl','rb') as file:
            l = pickle.load(file)
            file.close()
            
        with open('scores.pkl', 'wb') as file:
            l[boardNum][click] = [nameIn1]
            pickle.dump(l,file)
            file.close()

#========================================================================================================================================================    
def findHighScores(filename):
    global boardNum,new_scores,valueList, Sorted, topPlayer, leaderboardList,scoresList
    
    file = open('scores.pkl','rb')
    new_scores = pickle.load(file)
    file.close()
    print(new_scores)
    
    keyList = list(new_scores[boardNum].keys())
    def bubbleSort( listToSort ):
        limit = len( listToSort )
        for i in range( 1, limit ):
            isSorted = True
            for j in range( limit - i ): 
                if listToSort[ j ] > listToSort[ j + 1 ]:
                    listToSort[ j ], listToSort[ j + 1 ] = listToSort[ j + 1 ], listToSort[ j ]
                    isSorted = False
            if isSorted:
                break 
        return( listToSort )
    
    Sorted = bubbleSort(keyList)
    leaderboardList = []
    scoresList = []
    
    #put player names in a sorted list and their respective scores in another sorted list for each board
    for i in range (len(Sorted)): 
        for k in range (len(new_scores[boardNum][Sorted[i]])):
            leaderboardList.append(new_scores[boardNum].get(Sorted[i])[k])
            scoresList.append(Sorted[i])
    print(leaderboardList)
    print(scoresList)

#============================================================================================================================================
def diceNum (playerCount,player1,allBoardInfo):
    global click
    
    dice = random.randint(1,6)
    allPlayerInfo[player1][playerCount] += dice
    if player1 == True: #count the number of times the player clicked/went 
        click +=1
    image(allBoardInfo[ boardNum ][4],600,0,200,600)
    copy (allBoardInfo[ boardNum ][3],(dice-1)*100,0,100,97,660,500,80,77)     # image , section of image, length and height of image, image spot on board, size of image
    return dice
#=============================================================================================================================================
def movePlayer (allPLayerInfo, allBoardInfo):
    global boardImage, player2Image, player1Image, diceImage, bannerImage, numCol, numRow, factorX, factorY, boardNum
    global playerPosX, playerPosY, playerWidth, playerHeight, playerCount, player1, whereList
    
    allPlayerInfo[player1][playerPosX] = allPlayerInfo[player1][playerCount] % allBoardInfo[ boardNum ][numCol] * allBoardInfo[ boardNum ][factorX] + allBoardInfo[ boardNum ][factorX] // 2
    allPlayerInfo[player1][playerPosY] = (boardHeight - 55) - allPlayerInfo[player1][playerCount] // allBoardInfo[ boardNum ][numCol] * allBoardInfo[ boardNum ][factorY]
    
    #find the column the do MOD 2 to find if its and odd number
    if (boardNum == 0 or boardNum == 2) and (allPlayerInfo[player1][playerCount] // allBoardInfo[ boardNum ][numCol]) % 2 == 1: #if using board1 or board 3 and poitner in odd row, make it move backwards
        allPlayerInfo[player1][playerPosX] = (boardWidth - allBoardInfo[ boardNum ][factorX] // 2) - (allPlayerInfo[player1][playerCount] % allBoardInfo[ boardNum ][numCol] * allBoardInfo[ boardNum ][factorX])
    drawPlayers()
#========================================================================================================================================================================
def mouseReleased():
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, breakPoint
    
    validLocation = False 

    for i in range( numBoundaries ): 
        if activeBoundaries[ i ]:
            validXRange = allBoundaries[i][0][0] <= mouseX <= allBoundaries[i][1][0]  
            validYRange = allBoundaries[i][0][1]  <= mouseY <= allBoundaries[i][1][1]
            validLocation = validXRange and validYRange

            if validLocation: 
                
                whichBoundary = i
                break
            
    if validLocation and removeBoundary: 
        activeBoundaries[ whichBoundary ] = False 
#=======================================================================================================================================================================================
def StartGame():   
    fill(176, 215, 245)
    rect(0,0,800,700)
    fill(255,255,255,150)
    rect(100,50,600,400)
    fill( 0 )
    textSize ( 20 )    
#=====================================================================================================================================================================
def drawPlayers():
    image (allBoardInfo[ boardNum ][boardImage], 0, 0, boardWidth, boardHeight)
    if player1:
        image (allBoardInfo[ boardNum ][player2Image], allPlayerInfo[player1][playerPosX], allPlayerInfo[player1][playerPosY], allPlayerInfo[player1][playerWidth], allPlayerInfo[player1][playerHeight])
        image (allBoardInfo[ boardNum ][player1Image], allPlayerInfo[not player1][playerPosX], allPlayerInfo[not player1][playerPosY], allPlayerInfo[not player1][playerWidth], allPlayerInfo[not player1][playerHeight])
    else:
        image (allBoardInfo[ boardNum ][player1Image], allPlayerInfo[player1][playerPosX], allPlayerInfo[player1][playerPosY], allPlayerInfo[player1][playerWidth], allPlayerInfo[player1][playerHeight])
        image (allBoardInfo[ boardNum ][player2Image], allPlayerInfo[not player1][playerPosX], allPlayerInfo[not player1][playerPosY], allPlayerInfo[not player1][playerWidth], allPlayerInfo[not player1][playerHeight])    
#==========================================================================================================================================================================
def helpButtonandTurns():
    global click,menu
    
    fill(0)
    textSize(30)
    image(menu,0,600,800,100)
    text(click,40,675)
    #do we need this part

#==========================================================================================================================================================================
def showLeaderboard():
    global leaderBoard, leaderboardList, new_scores, boardNum, Sorted,scoresList
    
    image(leaderBoard, 0, 0, 600, 600)
    fill(255)
    textSize(25)
    text("Leaderboard #" + str(boardNum+1), 205, 105)
    
    y = 185
    if len(leaderboardList) < 5:
        for i in range (len(leaderboardList)): 
            fill(0)
            textSize(20)
            text(leaderboardList[i], 220, y)
            text(scoresList[i],400,y)
            y += 68
    else:
        for i in range (5):
            fill(0)
            textSize(20)
            text(leaderboardList[i], 220, y)
            text(scoresList[i],400,y)
            y += 68
#===================================================================================================================================================================================
def draw():
    global allBoardInfo, boardImage, player2Image, player1Image, diceImage, bannerImage, numCol, numRow, factorX, factorY, boardWidth, boardHeight, mode, boardNum, startScreen, time, goCPU, click, Sorted, topPlayer
    global allPlayerInfo, playerPosX, playerPosY, playerWidth, playerHeight, playerCount, player1,chooseBoard,gameState,help,helpButton, leaderboardList,leaderBoardButton
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, whereList,nameIn1Done,nameCount1,nameIn1,nameIn2,nameCount2, name, nameLimit, controlKeys
    global whichKey, asciList,new_scores,Key,exitScreen
    
    if mode == "startScreen":
        image(startScreen,0,0,800,700)   
        allBoundaries = [[[85,515],[300,600]],[[500,515],[720,600]]]
        numBoundaries = len(allBoundaries)
        if whichBoundary == -1:
            activeBoundaries = [ True for i in range( numBoundaries ) ]

        if whichBoundary == 0:
            mode = "Names"
            StartGame()
            whichBoundary = -1
            text( "Enter your name > ", 150, 100 )
            
        elif whichBoundary == 1:
            mode = "help"
            whichBoundary = -1

    if mode == "Names":
        if whichKey != '':
            StartGame()
            text( "Enter your name > ", 150, 100 )
            nameIn1 += whichKey.upper()
            nameCount1 += 1
            text( nameIn1, 350, 100 )
            text("press space when done",250,400)
            if ( whichKey == ' ') or ( nameCount1 >= nameLimit ):
                mode = "Start" 

    if mode == "help":
        allBoundaries = [[[0,600],[200,700]]]
        numBoundaries = len(allBoundaries)
        image(help,0,0,800,700)
        
        if whichBoundary == -1:
            activeBoundaries = [ True for i in range( numBoundaries ) ]

        if whichBoundary == 0:
            if gameState == "Start":
                mode = "Play"
                fill(188,126,242)
                rect(0,0,800,700)
                helpButtonandTurns()
                image (allBoardInfo[ boardNum ][boardImage], 0, 0, boardWidth, boardHeight)
                image(allBoardInfo[ boardNum ][4],600,0,200,600)   
                drawPlayers()

            else:
                mode = "startScreen"
            whichBoundary = -1
                                                                               
    if mode == "Start":
        gameState = "Start"
        allBoundaries =  [[[65,455],[240,600]],[[320,445],[480,600]],[[565,445],[720,600]]]
        numBoundaries = len(allBoundaries)
        image(chooseBoard, 0, 0, 800, 700)
        
        if whichBoundary == -1:
            activeBoundaries = [ True for i in range( numBoundaries ) ]
            
        if whichBoundary == 0:
            boardNum = 0

        elif whichBoundary == 1:
            boardNum = 1

        elif whichBoundary == 2:
            boardNum = 2

        if whichBoundary == 0 or whichBoundary == 1 or whichBoundary == 2:         
            player1 = False
            goCPU = False
            allPlayerInfo = [ [allBoardInfo[boardNum][factorX]//2, boardHeight - 55, 25, 40, 0], [allBoardInfo[boardNum][factorX]//2, boardHeight - 55, 25, 40, 0] ]
            fill(188,126,242)
            rect(0,0,800,700)
            helpButtonandTurns()
            image (allBoardInfo[ boardNum ][boardImage], 0, 0, boardWidth, boardHeight)
            image(allBoardInfo[ boardNum ][4],600,0,200,600)            
            image (allBoardInfo[ boardNum ][player2Image], allPlayerInfo[player1][playerPosX], allPlayerInfo[player1][playerPosY], allPlayerInfo[player1][playerWidth], allPlayerInfo[player1][playerHeight])
            image (allBoardInfo[ boardNum ][player1Image], allPlayerInfo[not player1][playerPosX], allPlayerInfo[not player1][playerPosY], allPlayerInfo[not player1][playerWidth], allPlayerInfo[not player1][playerHeight])

            mode = "Play"
            whichBoundary = -1
                  
    if mode == "Play":
        allBoundaries = [[[600,470],[800,600]],[[625,600],[800,700]],[[450,600],[625,700]],[[275,600],[450,700]],[[100,600],[275,700]]]
        numBoundaries = len(allBoundaries)   
        
        if goCPU == False:
            activeBoundaries = [ True for i in range( numBoundaries ) ]
        #print(numBoundaries)       
        if whichBoundary == 1:
            mode = "help"
            whichBoundary = -1
        
        if whichBoundary == 2:
            print ("restart")
            player1 = False
            goCPU = False
            allPlayerInfo = [ [allBoardInfo[boardNum][factorX]//2, boardHeight - 55, 25, 40, 0], [allBoardInfo[boardNum][factorX]//2, boardHeight - 55, 25, 40, 0] ]
            fill(188,126,242)
            rect(0,0,800,700)
            click = 0
            helpButtonandTurns()
            image (allBoardInfo[ boardNum ][boardImage], 0, 0, boardWidth, boardHeight)
            image(allBoardInfo[ boardNum ][4],600,0,200,600)            
            image (allBoardInfo[ boardNum ][player2Image], allPlayerInfo[player1][playerPosX], allPlayerInfo[player1][playerPosY], allPlayerInfo[player1][playerWidth], allPlayerInfo[player1][playerHeight])
            image (allBoardInfo[ boardNum ][player1Image], allPlayerInfo[not player1][playerPosX], allPlayerInfo[not player1][playerPosY], allPlayerInfo[not player1][playerWidth], allPlayerInfo[not player1][playerHeight])
            
            whichBoundary = -1
        
        if whichBoundary == 3:
            print("finish")
            mode = "Finish"
            whichBoundary = -1
        
        if whichBoundary == 4:
            print("leaderboard")
            mode = "leaderboard"
            whichBoundary = -1       
        
        if whichBoundary == 0:
            player1 = not player1
            time = millis()
            diceNum (playerCount,player1,allBoardInfo)
            
            if allPlayerInfo[player1][playerCount] < len (whereList[boardNum]):
                allPlayerInfo[player1][playerCount] = whereList[boardNum][allPlayerInfo[player1][playerCount]]
            
            helpButtonandTurns()  
            
            movePlayer (allPlayerInfo, allBoardInfo)
            
            goCPU = True
            whichBoundary = -1
            activeBoundaries = [ False for i in range( numBoundaries ) ] 

    
        if time + 1000 < millis() and goCPU == True :#delays move between player and CPU - once 2 seconds have passed after player made a move, then CPU goes 
            player1 = not player1
            diceNum (playerCount,player1,allBoardInfo)
            if allPlayerInfo[player1][playerCount] < len (whereList[boardNum]):
                allPlayerInfo[player1][playerCount] = whereList[boardNum][allPlayerInfo[player1][playerCount]]
            movePlayer (allPlayerInfo, allBoardInfo)
            activeBoundaries = [ True for i in range( numBoundaries ) ]
            goCPU = False
 
        
        if allPlayerInfo[True][playerCount] > len(whereList[boardNum]) - 1: #if green wins
            activeBoundaries = [ False for i in range( numBoundaries ) ] 
            do_pickle()
            findHighScores('scores.txt')
            mode = "End"
            click = 0
        elif allPlayerInfo[False][playerCount] > len(whereList[boardNum]) - 1: #if purple wins
            activeBoundaries = [ False for i in range( numBoundaries ) ]
            findHighScores('scores.txt')
            mode = "End"
            click = 0
            
    if mode == "End":
        allBoundaries = [[[250,480],[350,530]],[[275,600],[450,700]]]
        numBoundaries = len(allBoundaries)
        activeBoundaries = [ True for i in range( numBoundaries ) ]
        showLeaderboard()
        
        if whichBoundary == 0:
            mode = "Start"
            whichBoundary = -1
            
        if whichBoundary == 1:
            mode = "Finish"
            print("finish")
            
        if allPlayerInfo[True][playerCount] > len(whereList[boardNum]) - 1: #if green wins
            fill(0)
            textSize(30)
            textAlign(CENTER, BOTTOM)
            text(nameIn1 + "wins", 300, 580 )
            textAlign(LEFT, BOTTOM)
            
        elif allPlayerInfo[False][playerCount] > len(whereList[boardNum]) - 1: #if purple wins
            fill(0)
            textSize(30)
            textAlign(CENTER, BOTTOM)
            text("Computer wins", 300, 580 )
            textAlign(LEFT, BOTTOM)
            

        whichBoundary = -1    
        
    if mode == "leaderboard":
        allBoundaries = [[[250,480],[350,530]]]
        numBoundaries = len(allBoundaries)
        activeBoundaries = [ True for i in range( numBoundaries ) ]
        findHighScores('scores.txt')
        showLeaderboard()
        if whichBoundary == 0:
            mode = "Play"
            fill(188,126,242)
            rect(0,0,800,700)
            helpButtonandTurns()
            image (allBoardInfo[ boardNum ][boardImage], 0, 0, boardWidth, boardHeight)
            image(allBoardInfo[ boardNum ][4],600,0,200,600)   
            drawPlayers()
        whichBoundary = -1        
    
     
       #this is the exit screen after person clicks exit button. Boundaries should be boundaries of play again button
    if mode == "Finish":
        image(exitScreen,0,0,800,700)
        allBoundaries = [[[230,520],[530,620]]]
        numBoundaries = len(allBoundaries)
        
        
        if whichBoundary == -1:
            activeBoundaries = [ True for i in range( numBoundaries ) ]
            
        if whichBoundary == 0:
            mode = "startScreen"
            whichBoundary = -1
            gameState = "Beginning"
            nameCount1 = 0
            nameIn1 = ''
            click = 0
    whichKey = ''
    
#====================================================================================================================================================================
def keyReleased():
    global whichKey, asciList, controlKeys, asciicontrolList
    if key == CODED:
       if keyCode in controlKeys:
        whichKey = keyCode
    elif key in asciList:
        whichKey = key
    else:
        whichKey = ''    
        
