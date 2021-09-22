
# Used example Code http://usingpython.com/adding-an-inventory/
# Player Img https://pixabay.com/vectors/firefighters-axe-emblem-fire-151711/
# https://github.com/opensourcedesign/fonts/blob/master/gnu-freefont_freesans/FreeSansBold.ttf
# https://findicons.com/files/icons/245/xmas/128/tree.png
# https://findicons.com/files/icons/2028/fire_toolbar/48/fire_v2.png
# https://www.pngkey.com/detail/u2q8u2r5u2o0q8t4_vector-illustration-of-alarm-clock-as-pixelated-bitmap/
# https://findicons.com/files/icons/2028/fire_toolbar/48/fire_v2.png
# http://designbeep.com/2012/04/27/50-free-high-resolution-grass-textures-for-designers/
# Pathfinding - Part 4# Dijkstra Search# KidsCanCode 2017


from fireFighterPath import *
import sys

print(sys.version)
#useful game dimensions

#set up the display
pygame.init()
clock = pygame.time.Clock()

MY_PLAYER = pygame.image.load('img/my_player1.png')
PLAYER = pygame.image.load('img/player1.png')
playerPos = [10,10]

# mapGraph = WeightedGrid(MAPWIDTH, MAPHEIGHT)
# goal = vec(14, 8)
# start = vec(20, 0)
# search_type = a_star_search
# path, cost = search_type(mapGraph, goal, start)



# screen = pygame.display.set_mode((MAPWIDTH, MAPHEIGHT))
# for node in path:
#     x, y = node
#     rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
#     pygame.draw.rect(screen, MEDGRAY, rect)

#the player image
player_List = []
#playerPos_list = []
j=0
for i in range(0,NUM_PLAYERS):
    if i >= MAPWIDTH-1:
        xpos= MAPWIDTH-1-i
        j+=1
    else:
        xpos=i
        fire_man = FireMan([xpos+1,j])
    player_List.append( fire_man ) #pygame.image.load('img/player1.png') )
    #the position of the player [x,y]
    #playerPos_list.append( [xpos+1,j])




#add a font for our statInfo
INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)

#loop through each row
for rw in range(MAPHEIGHT):
    #loop through each column in that row
    for cl in range(MAPWIDTH):
        #pick a random number between 0 and 15
        randomNumber = random.randint(0,100)
        # #if a zero, then the tile is coa
        # if randomNumber == 0:
        #     tile = FIRE

        #water if the random number is a 1 or a 2
        if randomNumber >= 0 and randomNumber <= 50:
            tile = TREE
        elif randomNumber >= 61 and randomNumber <= 70:
            tile = GRASS
        else:
            tile = DIRT
        #set the position in the tilemap to the randomly chosen tile
        tilemap[rw][cl] = tile
#3 Staring File locations

#Place the Fire
fire_list =[]
for i in range(0,2):
    y_pos = random.randint(10,MAPHEIGHT-1)
    x_pos = random.randint(10,MAPWIDTH-1)
    fire_list.append([x_pos,y_pos])
    tilemap[y_pos][x_pos]=FIRE
bernOutTime =100
ticks =0
while True:
    # keep loop running at the right speed
    clock.tick(FPS)
    ticks +=1
    if ticks ==10000:
        GameOver(statInfo, resources, ticks, len(player_List), tilemap)
        pygame.quit()

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            GameOver(statInfo,resources,ticks,len(player_List),tilemap)
            pygame.quit()
            
            #sys.exit()
        #if a key is pressed
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                GameOver(statInfo,resources,ticks,len(player_List),tilemap)
                pygame.quit() 
                exit()             
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                playerPos[0] += 1
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's x position
                playerPos[1] -= 1
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                playerPos[1] += 1
            if event.key == K_SPACE:
                #what resource is the player standing on?
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                #player now has 1 more of this resource
                statInfo[currentTile] += 1
                #the player is now standing on dirt
                tilemap[playerPos[1]][playerPos[0]] = DIRT
            #placing dirt
            if (event.key == K_1):
                #get the tile to swap with the dirt
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                tilemap[playerPos[1]][playerPos[0]] = DIRT


    if len(fire_list) == 0:
        GameOver(statInfo,resources,ticks,len(player_List),tilemap)

        break
        #GameOver


    if len(fire_list)>= bernOutTime:
        bernOutTime -= bernOutTime
        oldFlame = fire_list[0]
        fire_list.pop(0)
        tilemap[oldFlame[1]][oldFlame[0]]= BURNT

    #fire Grows
    length = len(fire_list)
    #print("fire_list Per Spread length: ",length)
    for i in range(length):
        #print("i: ",i)

        #Will the this fire spread?
        if random.randint(0,4) != 1 :
            continue

        x_pos = fire_list[i][0]
        y_pos = fire_list[i][1]
        # 0 1 2
        # 3 @ 4
        # 5 6 7
        # @ = cur location of fire
        #randomly Pic the next spot for a fire to go
        spreadFireNext = random.randint(0,7)
        if spreadFireNext == 0 or spreadFireNext == 3 or spreadFireNext == 5 :
            x_pos = x_pos-1
        elif spreadFireNext == 2 or spreadFireNext == 4 or spreadFireNext == 7 :
            x_pos = x_pos+1
        #else keep x the same

        if spreadFireNext == 0 or spreadFireNext == 1 or spreadFireNext == 2 :
            y_pos= y_pos-1
        elif spreadFireNext == 5 or spreadFireNext == 6 or spreadFireNext == 7 :
            y_pos= y_pos+1
        #else keep y the same
        if x_pos  > MAPWIDTH - 1 or y_pos > MAPHEIGHT - 1 or x_pos < 0 or y_pos < 0:
            continue
        if tilemap[y_pos][x_pos] == BURNT:
            continue
        if tilemap[y_pos][x_pos] == FIRE:
            continue
        if tilemap[y_pos][x_pos] == DIRT:
            if random.randint(0,200) != 1 :
                 continue
        #Now add this fire to the list
        fire_list.append([x_pos,y_pos])
        tilemap[y_pos][x_pos] = FIRE
        #print("Adding to the End of List")

    #Clear The statInfo
    statInfo = statInfo.fromkeys(statInfo,0)

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct image
            statInfo[tilemap[row][column]] +=1
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))

    #display the player at the correct position
    sizeOFTeam = len(player_List)
    tempDead_list = []
    for i in range(sizeOFTeam):
        #setFireFighterPath(playerPos_list[i])
        if not player_List[i].pathBasic3():
            #death to the Fire fighter
            tempDead_list.append(i)
            continue
        #player_List[i].pathBasic1(fire_list)

        DISPLAYSURF.blit(player_List[i].img,(player_List[i].cerPos[0]*TILESIZE,player_List[i].cerPos[1]*TILESIZE))
    
    #remove All dead Players this rownd
    for playerIndex in tempDead_list:
        if len(player_List) <=playerIndex:
            continue
        player_List.pop(playerIndex)
        #playerPos_list.pop(playerIndex)
    del tempDead_list[:]
    
    # DISPLAYS my Player
    DISPLAYSURF.blit(MY_PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    statInfo[FIREMEN]=len(player_List)
    statInfo[TURN]= ticks

    #display the statInfo, starting 10 pixels in
    placePosition = 10

    for item in resources:
        #add the image
        DISPLAYSURF.blit(textures[item],(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 30
        #add the text showing the amount in the statInfo
        if item == FIREMEN or item == TURN:
            textObj = INVFONT.render(str(statInfo[item]), True, WHITE, BLACK)
        else:
            textObj = INVFONT.render(str(statInfo[item])+" : "+ str(int((statInfo[item]/TOTAL_MAP_SIZE)*100))+"%     ", True, WHITE, BLACK) 

        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 150#50
    #update the display
    pygame.display.flip()
    pygame.display.update()
   





#The Simulation has End