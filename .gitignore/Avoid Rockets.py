from tkinter import *
from random import *
import SysRand

# ----- Variables Globales ------
# --- Map Generator ---
global bScreenX, bScreenY
# Résolution écran par défaut.
bScreenX = int(600)
bScreenY = int(400)

global cScreenX, cScreenY
# Résolution écran actuel.
cScreenX = int(600)
cScreenY = int(400)

global extension
# Extension des images.
extension = str(".gif")

global mapSize, tileSize
# Taille des tiles (en pixels).
# Attention, il faut faire correspondre la taille des tiles avec la taille des textures.
tileSize = int(32)

# Taille de la map (en tiles).
mapSize = int(15)

global mapTiles
# Liste de toutes les tiles.
mapTiles = []

# Liste des tiles Obstacles (murs)
global obstacles
obstacles = []

# Liste des tiles Pieges (Trous)
global pieges
pieges = []

# Liste des tile Sols
global sols
sols = []

global canvas

global tilePics
# Liste de toutes les Icones de tiles.
tilePics = []

global shuffler_seed
# Seed du mélangeur.
shuffler_seed = int(0)

global obstaclePercent
# Pourcentage d'obstacles sur la map.
# Entre 0 et 1.
obstaclePercent = float(0)

global obstacleMultiplier
# Multiplayer du nombre d'obstacle.
obstacleMultiplier = float(0.01)

global obstacleMax
# Taux maximum d'obstacles.
obstacleMax = float(.05)

global currentNbObstacle
# Nombre actuel d'obstacles sur la map.
currentNbObstacle = int(0)

global obstacleMap
# Grille de boolean pour les obstacles de la map.
obstacleMap = []

global openTiles
# Tiles ouvertes.
openTiles = []

global allTiles
# Toutes les Tiles.
allTiles = []

global shuffledTiles
# Tiles mélangées.
suffledTiles = []

global mapCenter
# Tile centrale de la map.

# --- Player ---

global player
# Référence au script du joueur.

global playerSize
# Taille du joueur.
playerSize = int(16)

global playerImg
# Référence image du joueur.

global playerSpeed
# Vitesse joueur.
# En pixel/50ms.
playerSpeed = int(6)

# --- Missiles ---
global missiles
# Liste de tout les  missiles.
missiles = []

global mSpeed
# Vitesse des missiles.
mSpeed = int(2)

global mRad
# Radius des missiles.
mRad = int(4)

global mSpawnRate
# Spawn rate des missiles.
mSpawnRate = int(1)

global maxSpeed
# Vitesse des missiles max.
maxSpeed = int(6)

global incSpeed
# Taux d'accroissement de la vitesse des missiles.
incSpeed = int(1)

# --- Menus ---
global e_mapSize
# Taille de la map choisie par le joueur.

global e_missilesSize
# Taille des missiles choisie par le joueur.

global e_seed
# Seed de la map.

global e_lunchGame
# Lancer la partie.

# ----- Classes et définitions -----

# ----- SECTION : Tile Properties
class Tile():
    # ----- VARIABLES -----

    # Indexes
    allTiles_index = int(0)
    tilePics_index = int(0)

    # Coordonnées
    x = int(0)
    y = int(0)

    # Type de tile
    # - peut être : Mur_pierre, Mur_bois, Sol ou Trou
    tType = str("")

    # Bool qui check si la tile a une Pic
    hasPic = False


    # ----- DEFINITIONS -----

    # Définition qui setup les coordonnées de la tile.
    def SetupCoords(self,_x,_y):
        self.x = _x
        self.y = _y

    # Définition qui setup le type de tile  
    def SetupType(self, _type):
        global sols, pieges, obstacles

        if self.tType != str(""):
            if _type == "Sol":
                self.RemoveTileFromList(sols)
                sols.append(self)
            elif _type == "Trou":
                self.RemoveTileFromList(pieges)
                pieges.append(self)
            elif _type == "Mur_pierre" or _type == "Mur_bois":
                self.RemoveTileFromList(obstacles)
                obstacles.append(self)
        else:
            if _type == "Sol":
                sols.append(self)
            elif _type == "Trou":
                pieges.append(self)
            elif _type == "Mur_pierre" or _type == "Mur_bois":
                obstacles.append(self)

        self.tType = _type

    def RemoveTileFromList(self, tList):
        newList = []

        for i in tList:
            if i != self:
                newList.append(i)

    def SetupCanvas(self):
        global canvas
        global tileSize

        global img_sol
        global img_murPierre
        global img_murBois
        global img_trou
        
        if self.tType == "Sol":
            tIMG = img_sol
        elif self.tType == "Trou":
            tIMG = img_trou
        elif self.tType == "Mur_pierre":
            tIMG = img_murPierre
        elif self.tType == "Mur_bois":
            tIMG = img_murBois

        # On calcule la position X et Y de l'image.
        imgX = self.x * tileSize + (tileSize/2)
        imgY = self.y * tileSize + (tileSize/2)
        
        pic = canvas.create_image(imgX, imgY, image = tIMG)

        global tilePics

        if self.hasPic == True:
            canvas.delete(self.tilePics_index)
            tilePics[self.tilePics_index] = pic
        else:
            self.hasPic = True
            tilePics.append(pic)
        


# ----- SECTION : Map Generation
class MapGenerator():
    # ----- VARIABLES -----

    # ----- DEFINITIONS -----

    # Définition qui initialise les tiles de la map.
    def Initialisation(self):
        
        global mapSize, tileSize
        global mapTiles
        global openTiles
        global allTiles
        
        mapTiles = []
        openTiles = []
        
        # On commence par creer les tiles
        for x in range (mapSize):
            mapTiles.append([])
            for y in range (mapSize): 
                # On creer et ajoute une tile à la liste de tile XY
                tile = Tile()
                tile.tType = str("")
                tile.allTiles_index = (x * mapSize) + y
                tile.tilePix_index = tile.allTiles_index
                mapTiles[x].append(tile)
                openTiles.append(tile)
                allTiles.append(tile)
                
                
                #print("Tile X",x,y,"Initialized")
            

        for x in range (mapSize):
            for y in range (mapSize):
                mapTiles[x][y].SetupCoords(_x = x, _y = y)
                mapTiles[x][y].SetupType(_type = "Sol")
                #print("Tile",x,y,"Setup")

        # On assigne la map d'obstacles
        global obstacleMap
        for x in range (mapSize):
            obstacleMap.append([])
            for y in range (mapSize):
                isObstacle = False
                obstacleMap[x].append(isObstacle)

        # On définit le centre de la map.
        global mapCenter
        mapCenter = mapTiles[int(mapSize/2)][int(mapSize/2)]

        print("MapGenerator : Tile count =",len(allTiles))
        print("MapGenerator : Open tile count =",len(openTiles))
        print("MapGenerator : Initialisation ended.")

    # Définition qui affiche la map de base.
    def DrawMap(self):
        self.AssignTextures()

        # Référence au canvas de la map.
        global canvas

        # On définit la taille du canvas en fonction du nombre de tiles et de leur taille.
        global mapSize, tileSize
        cSize = int(mapSize * tileSize)
        print("MapGenerator : DrawMap - canvas Size",cSize)

        # On définit les placements du canvas.
        global cScreenX, cScreenY

        # On veut que la canvas soit centré.
        global canvaspX, canvaspY
        canvaspX = int((cScreenX - cSize)/2)
        canvaspY = int((cScreenY - cSize)/2)

        print("MapGenerator : DrawMap - canvas pX",canvaspX)
        print("MapGenerator : DrawMap - canvas pY",canvaspY)
        
        canvas = Canvas(root, width = cSize, height = cSize, bg = "black",highlightthickness=0, bd = 0)
        canvas.place(x = canvaspX, y = canvaspY)

        global mapTiles
        for x in range(mapSize):
            for y in range(mapSize):
                mapTiles[x][y].SetupCanvas()
        
        print("MapGenerator : DrawMap ended.")
        self.SpawnObstacles()

    # Définition qui assigne les textures de la map.
    def AssignTextures(self):
        global img_sol
        global img_murPierre
        global img_murBois
        global img_trou
        global extension
        global tileSize

        img_sol = PhotoImage(file = "Textures/Map/Sol" + str(tileSize) + extension)
        img_murPierre = PhotoImage(file = "Textures/Map/Mur_pierre" + str(tileSize) + extension)
        img_murBois = PhotoImage(file = "Textures/Map/Mur_bois" + str(tileSize) + extension)
        img_trou = PhotoImage(file = "Textures/Map/Trou" + str(tileSize) + extension)

        print("MapGenerator : AssignTexture ended.")

    # Définition qui définit les obstacles.
    def SpawnObstacles(self):
        global mapSize, obstaclePercent, currentNbObstacle, obstacleMap, mapTiles
        global openTiles, shuffledTiles
        
        # Nombre total d'obstacles sur la map.
        print("MapGenerator : SpawnObstacles, obstaclePercent =",obstaclePercent)
        nbObstacles = int(mapSize * mapSize * obstaclePercent)
        print("MapGenerator : SpawnObstacles, NbObstacle =", nbObstacles)
        
        global shuffler
        global mapCenter
        global shuffledTiles
        global obstacles

        # On mélange les Tiles.
        shuffledTiles = shuffler.Shuffle(openTiles)

        for i in range(nbObstacles):
            tile = shuffledTiles[0]
            shuffledTiles.remove(tile)
            shuffledTiles.append(tile)

            obstacleMap[tile.x][tile.y] = True
            currentNbObstacle = currentNbObstacle + 1

            value = self.MapFullyAccessible(obstacleMap, currentNbObstacle)
            #print("MapFullyAccessible",value)
            
            if tile != mapCenter and value == True:
                tile.SetupType(_type = "Mur_bois")
                tile.SetupCanvas()
                openTiles.remove(tile)
                obstacles.append(tile)
            else:
                obstacleMap[tile.x][tile.y] = False
                currentNbObstacle = currentNbObstacle - 1
                
                

        print("MapGenerator : SpawnObstacles, Obstacle Count", currentNbObstacle)
        print("MapGenerator : SpawnObstacles ended.")

    def MapFullyAccessible(self, obMap, currObCount):
        mapFlags = []

        global mapCenter
        global shuffler

        for x in range(len(obMap)):
            mapFlags.append([])
            for y in range(len(obMap)):
                value = False
                mapFlags[x].append(value)

        queue = []
        queue.append(mapCenter)
        mapFlags[mapCenter.x][mapCenter.y] = True

        nbTilesAccessible = int(1)

        global mapSize
        global mapTiles

        _x = int(0)
        _y = int(0)
            
        while len(queue) > 0:
            tile = queue[0]
            queue.remove(tile)

            for x in range(3):
                _x = x - 1
                for y in range(3):                    
                    _y = y - 1

                    nX = int(tile.x + _x)
                    nY = int(tile.y + _y)

                    if _x == 0 or _y == 0:                        
                        if nX >= 0 and nX < mapSize:
                            if nY >= 0 and nY < mapSize:
                                if mapFlags[nX][nY] == False and obMap[nX][nY] == False:
                                    mapFlags[nX][nY] = True
                                    _tile = mapTiles[nX][nY]
                                    queue.append(_tile)                              
                                    nbTilesAccessible = nbTilesAccessible + 1                            

        target = int(mapSize * mapSize - currObCount)
        #print(target, " -- ", nbTilesAccessible)
        return nbTilesAccessible == target
    

    # Définition qui augmente le nombre d'obstacles
    def AddObstacles(self):
        print("MapGenerator : Adding obstacles.")
        
        global obstacleMultiplier
        global obstacleMax
        global obstaclePercent
        
        if obstaclePercent < obstacleMax:
            obstaclePercent = obstaclePercent + obstacleMultiplier
            self.SpawnObstacles()
            


# ----- SECTION : Shuffle

class Shuffler():

    # Le shuffler utilisé est le suivant : "The Fisher-Yate Shuffle".
    

    # Définition qui mélange une List.
    def Shuffle(self, l):
        global shuffler_seed
        prng = SysRand.Random(shuffler_seed)

        #print("prng =", prng)

        for i in range(len(l)):
            # On prend un nombre aléatoire avec un seed grace au prng.
            randomIndex = prng.Next(i, len(l))            
            #print("randomIndex =", randomIndex)

            # On enregistre l'item au rang "randomIndex" de l'array.
            tempItem = l[randomIndex]

            # Puis on intervertis
            l[randomIndex] = l[i]
            l[i] = tempItem

        return l

# ----- SECTION : Joueur
class Joueur():    
    # ----- VARIABLES -----

    # Vie joueur.
    vie = int(1)

    speed = int(2)

    # Sens du mouvement.
    sens = "HORIZONTAL"

    # Inversion.
    inv = 1

    # Est en train de bouger.
    isMoving = False

    # Icone joueur.
    pic = None

    # Position joueur.
    x = int(0)
    y = int(0)

    # ----- DEFINITIONS -----
    def SetupPlayer(self):
        print("Player : Setting up player.")

        global playerSpeed
        
        self.vie = int(1)
        self.speed = playerSpeed
        self.sens = "HORIZONTAL"
        self.inv = int(1)
        self.isMoving = False

        global mapCenter
        self.x = mapCenter.x
        self.y = mapCenter.y

        print("Player : player X " + str(self.x))
        print("Player : player Y " + str(self.y))

        self.DisplayPlayer()

        global timer
        timer.StartTimer()

        global mm
        mm.StartMissileSpawn()
        

    def DisplayPlayer(self):
        global canvas
        global playerSize
        global tileSize
        global extension
        global playerImg

        playerImg = PhotoImage(file = "Textures/Player/Player" + str(playerSize) + extension)
        print("Player : player pic " + "Textures/Player/Player" + str(playerSize) + extension)
        
        _x = int(self.x * tileSize + tileSize/2)
        _y = int(self.y * tileSize + tileSize/2)

        self.x = _x
        self.y = _y

        print("Player : player start X " + str(_x))
        print("Player : player start Y " + str(_y))

        self.pic = canvas.create_image(_x, _y, image = playerImg)
        print("Player : Display player ended.")

        self.StartMoving()

    def StartMoving(self):
        self.MovePlayer()

    def MovePlayer(self):
        global canvas
        global root

        xMove = 0
        yMove = 0
        
        if self.isMoving == True:       

            global playerSize
            global tileSize
            global playerImg

            if self.sens == "HORIZONTAL":
                xMove = self.speed * self.inv

            if self.sens == "VERTICAL":
                yMove = self.speed * self.inv

        _newPosX = self.x + xMove
        _newPosY = self.y + yMove
        
        notExitingMap = self.CheckExitingMap(newPosX = _newPosX, newPosY = _newPosY)
        
        if notExitingMap == True:
            
            noObstacle = self.CheckWallCollision(newPosX = _newPosX, newPosY = _newPosY)

            if noObstacle == True:
                self.x = self.x + xMove
                self.y = self.y + yMove
                canvas.move(self.pic, xMove, yMove)
            
        root.after(50, self.MovePlayer)

    def CheckExitingMap(self, newPosX, newPosY):
        canMove = True

        global mapSize
        global tileSize
        _mp = mapSize * tileSize

        if newPosX < 0:
            canMove = False
        if newPosY < 0:
            canMove = False

        if newPosX > _mp:
            canMove = False
        if newPosY > _mp:
            canMove = False
            

        return canMove

    def CheckWallCollision(self, newPosX, newPosY):
        canMove = True

        global obstacles
        global tileSize
        global playerSize

##        print("NewPos X ", newPosX)
##        print("NewPos Y ", newPosY)

        # Pour chaque tile dans la liste "Obstacles".
        for index in range(len(obstacles)):
            # On prend la distance entre l'obstacle et le joueur via les coordonnées.
            obx = obstacles[index].x * tileSize + (tileSize/2)
            oby = obstacles[index].y * tileSize + (tileSize/2)

##            print("Obstacle",index,"X ",obstacles[index].x)
##            print("Obstacle",index,"Y ",obstacles[index].y)
##            
##            print("Obstacle",index,"X obx ",obx)
##            print("Obstacle",index,"X oby ",oby)
            
            xDiff = pow(newPosX - obx, 2)
            yDiff = pow(newPosY - oby, 2)
            vector = xDiff + yDiff
            #print ("Vector",vector)

            # On retire les taille du joueur et des Tiles au vector.
            finalDist = (vector  ** 0.5) - tileSize/2 - playerSize/2
            #print ("FinalDist",finalDist)
            
            # Si la finalDist est inférieure à 0, alors on ne bouge pas.
            if finalDist < 0:
                canMove = False
        return canMove

    def Die(self):
        global timer
        timer.StopTimer()

        global mm
        mm.StopMissileSpawn()

        global canvas
        canvas.delete(self.pic)

        global missiles
        for i in missiles:
            i.DestroyMissile()

        del self
        
# ----- SECTION : Timer
class Timer():
    # ----- VARIABLES -----

    # Temps écoulé en secondes.
    timeElapsed = int(0)

    # Score à ajouter toutes les secondes.
    scoreFactor = int(5)

    # Score.
    score = int(0)

    # Est-ce que le temps s'écoule.
    isRunning = False

    # ----- DEFINITIONS -----
    def StartTimer(self):
        print("Timer : Creation.")
        
        global root
        global scoreText

        global cScreenX, cScreenY
        global mapSize, tileSize

        self.timeElapsed = int(0)

        self.scoreFactor = int(5)
        
        score = int(0)
        
        cSize = int(mapSize * tileSize)
        
        scoreText = Label(root, text = "0", fg = "white", bg = "black", width = 10, justify = CENTER)
        scoreText.configure(font = (20))
        scoreText.place(x = 0, y = 0)

        scoreText.update()
        wx = scoreText.winfo_width()
        wy = scoreText.winfo_height()

        print("Timer : wx",wx)
        print("Timer : wy",wy)

        _x = int((cScreenX)/2 - wx/3)
        _y = int((cScreenY - cSize)/4 - wy/2)

        scoreText.place(x = _x, y = _y)        
        
        self.isRunning = True
        print("Timer : Created.")
        self.Timer()

    def StopTimer(self):
        print("Timer : stopping timer.")
        self.isRunning = False
        del self

    def Timer(self):
        global root
        global scoreText

        if self.isRunning == True:
            self.score = self.score + self.scoreFactor
            self.timeElapsed = self.timeElapsed + 1
            scoreText.configure(text = str(self.score))

            if self.score%100 == 0:
                self.NewWave()
        
            root.after(1000, self.Timer)

    def NewWave(self):
        print("New Wave ---")
        
        global mSpeed
        global mSpawnRate
        global mg

        global maxSpeed
        global incSpeed

        mg.AddObstacles()

        if mSpeed < maxSpeed:
            mSpeed = mSpeed+incSpeed

        if mSpawnRate > 0.5:
            mSpawnRate = mSpawnRate - 0.1

# ----- SECTION : Missile
class Missile():
    # ----- VARIABLES -----

    # Propriétés missiles
    speed = int(0)
    dirX = int(0)
    dirY = int(0)
    x = int(0)
    y = int(0)
    magX = int(0)
    magY = int(0)

    lAxe = str("")
    l = int(0)

    radius = int(0)

    # Icone missile.
    pic = None    

    # ----- DEFINITIONS -----
    def StartMissile(self):
        global mSpeed
        self.speed = mSpeed

        global mRad
        self.radius = mRad

        global cScreenX, cScreenY
        global mapSize, tileSize
        global canvas
        
        cSize = int(mapSize * tileSize)

        randX = randint(0, (mapSize * tileSize))
        randY = randint(0, (mapSize * tileSize))

        spawnZone = randint(0,3)

        spX = int(0)
        spY = int(0)

        _lAxe = str("")
        _l = int(0)

        if spawnZone == 0:
            # Si le spawnZone vaut 0, alors le missile apparait dans la partie Nord.
            spY = int(0)
            spX = randX
            _lAxe = "VERTICAL"
            _l = int(mapSize * tileSize)

        elif spawnZone == 1:
            # Si le spawnZone vaut 0, alors le missile apparait dans la partie Est.
            spY = randY
            spX = int(0)
            _lAxe = "HORIZONTAL"
            _l = int(0)
            
        elif spawnZone == 2:
            # Si le spawnZone vaut 0, alors le missile apparait dans la partie Sud.
            spY = int(0)
            spX = randX
            _lAxe = "VERTICAL"
            _l = int(0)
            
        elif spawnZone == 3:
            # Si le spawnZone vaut 0, alors le missile apparait dans la partie Ouest.
            spY = randY
            spX = int(0)
            _lAxe = "HORIZONTAL"
            _l = int(mapSize * tileSize)

        self.x = spX
        self.y = spY

        self.lAxe = _lAxe
        self.l = _l

        self.pic = canvas.create_oval(spX - self.radius,
                                      spY - self.radius,
                                      spX + self.radius,
                                      spY + self.radius,
                                      fill = "red")

        global missiles
        missiles.append(self)

        global player
        self.magX = int(pow((self.x - player.x), 2))
        self.magY = int(pow((self.y - player.y), 2))
        mag = self.magX + self.magY

        self.dirX = -(int(self.x - player.x))/(mag) *100
        self.dirY = -(int(self.y - player.y))/(mag) *100

##        print("Missile x",self.x)
##        print("Missile y",self.y)
##
##        print("Missile magX",self.magX)
##        print("Missile magY",self.magY)
##        print("Missile mag",mag)
##
##        print("Missile dirX",self.dirX)
##        print("Missile dirY",self.dirY)
        
        self.Move()

    def Move(self):
        global root
        global player

        global mRad
        global playerSize        

        self.x = self.x + self.dirX * self.speed
        self.y = self.y + self.dirY * self.speed

        xDiff = pow(self.x - player.x, 2)
        yDiff = pow(self.y - player.y, 2)
        vector = xDiff + yDiff
        #print ("Vector",vector)        

        # On retire les taille du joueur et des Tiles au vector.
        dist = (vector ** 0.5) - mRad - playerSize/2

        _continue = True

        if dist <= 0:
            _continue = False
            player.Die()
            
        else:
            if self.lAxe == "VERTICAL":
                if self.l == int(0):
                    if self.y <= self.l:
                        _continue = False
                else:
                    if self.y >= self.l:
                        _continue = False

            if self.lAxe == "HORIZONTAL":
                if self.l == int(0):
                    if self.x <= self.l:
                        _continue = False
                else:
                    if self.x >= self.l:
                        _continue = False

        global canvas
        canvas.coords(self.pic,
                      self.x - mRad,
                      self.y - mRad,
                      self.x + mRad,
                      self.y + mRad)

        if _continue == True:
            root.after(10, self.Move)
        else:
            self.DestroyMissile()

    def DestroyMissile(self):
        global canvas
        canvas.delete(self.pic)
        del self
        
# ----- SECTION : Missiles Manager
class MissileManager():
    # ----- VARIABLES -----

    isRunning = True

    # ----- DEFINITIONS -----
    def StartMissileSpawn(self):
        isRunning = True
        self.Spawn()

    def StopMissileSpawn(self):
        self.isRunning = False
        del self

    def Spawn(self):
        global root
        global mSpawnRate

        if self.isRunning == True:

            m = Missile()
            m.StartMissile()

            root.after(int(mSpawnRate * 1000), self.Spawn)

# ----- SECTION : Missiles Manager
class GameManager():
    # ----- DEFINITIONS -----
    def StartGame(self):
        # Fenetre de jeu
        global root
        root = Tk()
        
        global tileSize
        global mapSize

        global cScreenX,cScreenY
        global bScreenX,bScreenY

        # On calcule la taille de l'écran.
        # On calcule le tout à partir de la taille en Y.
        cScreenY = int(1.25 * (tileSize * mapSize))
        print("Window : size Y",cScreenY)
        cScreenX = int((cScreenY * bScreenX)/ bScreenY)
        print("Window : size X",cScreenX)

        root.configure(width = cScreenX, height = cScreenY, bg = "black")
        root.title("MapGenerator")
        
        # Référence au mélangeur.
        global shuffler
        shuffler = Shuffler()

        # Référence MapGenerator.
        global mg
        mg = MapGenerator()

        mg.Initialisation()
        mg.DrawMap()

        # Référence au MissileManager
        global mm
        mm = MissileManager()

        # Référence au Timer.
        global timer
        timer = Timer()

        # On créer le joueur.
        global player
        player = Joueur()

        root.bind("<KeyPress>", Input_down)
        root.bind("<KeyRelease>", Input_up)

        root.mainloop()       
    
        
# ----- Gestion des Inputs -----
def Input_down(event):
    key = event.char
    key = str(key).lower()
    keysym = event.keysym

    global player
    global mg

    if key == "k":
        mg.AddObstacles()

    if key == "a":
        player.SetupPlayer()

    if key == "m":
        m = Missile()
        m.StartMissile()

    if keysym == "Up":
        player.sens = "VERTICAL"
        player.inv = int(-1)
        player.isMoving = True

    if keysym == "Down":
        player.sens = "VERTICAL"
        player.inv = int(1)
        player.isMoving = True

    if keysym == "Right":
        player.sens = "HORIZONTAL"
        player.inv = int(1)
        player.isMoving = True

    if keysym == "Left":
        player.sens = "HORIZONTAL"
        player.inv = int(-1)
        player.isMoving = True
        
    
def Input_up(event):
    key = str(event.char)
    keysym = event.keysym

    global player

    if keysym == "Up":
        if player.sens == "VERTICAL":
            player.isMoving = False

    if keysym == "Down":
        if player.sens == "VERTICAL":
            player.isMoving = False

    if keysym == "Right":
        if player.sens == "HORIZONTAL":
            player.isMoving = False

    if keysym == "Left":
        if player.sens == "HORIZONTAL":
            player.isMoving = False

    
# ----- Initialisation Map et Fenetre -----
global gm
gm = GameManager()
gm.StartGame()
