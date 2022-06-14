import pygame, random

WINDOW_WIDTH = 888
WINDOW_HEIGHT = 700

def startGame():
    pygame.init()

def quitGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            else :
                pass

def monster():
    startGame()
    
    displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Monster Hunter")

    FPS = 60
    clock = pygame.time.Clock()

    backgroundImage = pygame.image.load("MonsterHunter/background.png")
    backgroundImageRect = backgroundImage.get_rect()
    backgroundImageRect.x = 0
    backgroundImageRect.y = 100

    titleFont1 = pygame.font.Font("MonsterHunter/Abrushow.ttf", 80)
    titleText1 = titleFont1.render("Monster Hunter", True, (226, 73, 243))
    titleTextRect1 = titleText1.get_rect()
    titleTextRect1.centerx = WINDOW_WIDTH//2
    titleTextRect1.centery = WINDOW_HEIGHT//2 - 50

    titleFont2 = pygame.font.Font("MonsterHunter/Abrushow2.otf", 50)
    titleText2 = titleFont2.render("PRESS  ANY  KEY  TO  START  THE  GAME", True, (0,0,0))
    titleTextRect2 = titleText2.get_rect()
    titleTextRect2.centerx = WINDOW_WIDTH//2
    titleTextRect2.centery = WINDOW_HEIGHT//2 + 20


    class Game():

        def __init__(self, player, monsterGroup):

            self.score = 0
            self.roundNumber = 0
            self.roundTime = 0
            self.frameCount = 0
            self.player = player
            self.monsterGroup = monsterGroup

            self.nextLevelSound = pygame.mixer.Sound("MonsterHunter/next_level.wav")
            self.nextLevelSound.set_volume(0.2)

            self.font = pygame.font.Font("MonsterHunter/Celosia.otf", 28)

            blueImage = pygame.image.load("MonsterHunter/blue_monster.png")
            greenImage = pygame.image.load("MonsterHunter/green_monster.png")
            purpleImage = pygame.image.load("MonsterHunter/purple_monster.png")
            yellowImage = pygame.image.load("MonsterHunter/yellow_monster.png")

            #This list cooresponds to the monster_type attribute int 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
            self.targetMonsterImages = [blueImage, greenImage, purpleImage, yellowImage]
            self.targetMonsterType = random.randint(0,3)
            self.targetMonsterImage = self.targetMonsterImages[self.targetMonsterType]

            self.targetMonsterRect = self.targetMonsterImage.get_rect()
            self.targetMonsterRect.centerx = WINDOW_WIDTH//2
            self.targetMonsterRect.top = 33

        def update(self):
            self.frameCount += 1
            if self.frameCount == FPS:
                self.roundTime += 1
                self.frameCount = 0
            self.checkCollisions()

        def draw(self):

            WHITE = (255, 255, 255)
            BLUE = (20, 176, 235)
            GREEN = (87, 201, 47)
            PURPLE = (226, 73, 243)
            YELLOW = (243, 157, 20)
            BLACK = (0, 0, 0)
            colors = [BLUE, GREEN, PURPLE, YELLOW]

            catchText = self.font.render("Current Target", True, colors[self.targetMonsterType])
            catchRect = catchText.get_rect()
            catchRect.centerx = WINDOW_WIDTH//2
            catchRect.top = 0

            scoreText = self.font.render("Score: " + str(self.score), True, BLACK)
            scoreRect = scoreText.get_rect()
            scoreRect.topleft = (5, 5)

            livesText = self.font.render("Lives: " + str(self.player.lives), True, BLACK)
            livesRect = livesText.get_rect()
            livesRect.topleft = (5, 35)

            roundText = self.font.render("Current Round: " + str(self.roundNumber), True, BLACK)
            roundRect = roundText.get_rect()
            roundRect.topleft = (5, 65)

            timeText = self.font.render("Round Time: " + str(self.roundTime), True, BLACK)
            timeRect = timeText.get_rect()
            timeRect.topright = (WINDOW_WIDTH - 10, 5)

            warpText = self.font.render("Warps: " + str(self.player.warps), True, BLACK)
            warpRect = warpText.get_rect()
            warpRect.topright = (WINDOW_WIDTH - 10, 35)

            displaySurface.blit(catchText, catchRect)
            displaySurface.blit(scoreText, scoreRect)
            displaySurface.blit(roundText, roundRect)
            displaySurface.blit(livesText, livesRect)
            displaySurface.blit(timeText, timeRect)
            displaySurface.blit(warpText, warpRect)
            displaySurface.blit(self.targetMonsterImage, self.targetMonsterRect)

            pygame.draw.rect(displaySurface, colors[self.targetMonsterType], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT-200), 4)

        def checkCollisions(self):
            collidedMonster = pygame.sprite.spritecollideany(self.player, self.monsterGroup)

            #We collided with a monster
            if collidedMonster:
                #Caught the correct monster
                if collidedMonster.type == self.targetMonsterType:
                    self.score += 100*self.roundNumber
                    #Remove caught monster
                    collidedMonster.remove(self.monsterGroup)
                    if (self.monsterGroup):
                        #There are more monsters to catch
                        self.player.catchSound.play()
                        self.chooseNewTarget()
                    else:
                        #The round is complete
                        self.player.reset()
                        self.startNewRound()
                #Caught the wrong monster
                else:
                    self.player.dieSound.play()
                    self.player.lives -= 1
                    #Check for game over
                    if self.player.lives <= 0:
                        self.pauseGame("Final Score: " + str(self.score), "Press 'Enter' to play again")
                        self.resetGame()
                    self.player.reset()
            
        def startNewRound(self):

            self.score += int(10000*self.roundNumber/(1 + self.roundTime))
            self.roundTime = 0
            self.frameCount = 0
            self.roundNumber += 1
            self.player.warps += 1

            for monster in self.monsterGroup:
                self.monsterGroup.remove(monster)

            for i in range(self.roundNumber):
                self.monsterGroup.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-164), self.targetMonsterImages[0], 0))
                self.monsterGroup.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-164), self.targetMonsterImages[1], 1))
                self.monsterGroup.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-164), self.targetMonsterImages[2], 2))
                self.monsterGroup.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-164), self.targetMonsterImages[3], 3))

            self.chooseNewTarget()

            self.nextLevelSound.play()

        def chooseNewTarget(self):
            targetMonster = random.choice(self.monsterGroup.sprites())
            self.targetMonsterType = targetMonster.type
            self.targetMonsterImage = targetMonster.image

        def pauseGame(self, mainText, subText):

            global running
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)

            mainText = self.font.render(mainText, True, BLACK)
            main_rect = mainText.get_rect()
            main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50)

            subText = self.font.render(subText, True, BLACK)
            sub_rect = subText.get_rect()
            sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30)

            displaySurface.fill(WHITE)
            displaySurface.blit(mainText, main_rect)
            displaySurface.blit(subText, sub_rect)
            pygame.display.update()

            isPaused = True
            while isPaused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            isPaused = False
                    if event.type == pygame.QUIT:
                        isPaused = False
                        running = False
                        pygame.quit

        def resetGame(self):
            self.score = 0
            self.roundNumber = 0

            self.player.lives = 5
            self.player.warps = 2
            self.player.reset()

            self.startNewRound()

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()

            self.image = pygame.image.load("MonsterHunter/knight.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = WINDOW_WIDTH//2
            self.rect.bottom = WINDOW_HEIGHT

            self.lives = 5
            self.warps = 2
            self.velocity = 8

            self.catchSound = pygame.mixer.Sound("MonsterHunter/catch.wav")
            self.catchSound.set_volume(0.1)
            self.dieSound = pygame.mixer.Sound("MonsterHunter/die.wav")
            self.dieSound.set_volume(0.2)
            self.warpSound = pygame.mixer.Sound("MonsterHunter/warp.wav")
            self.warpSound.set_volume(0.2)

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.velocity
            if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
                self.rect.x += self.velocity
            if keys[pygame.K_UP] and self.rect.top > 100:
                self.rect.y -= self.velocity
            if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
                self.rect.y += self.velocity

        def warp(self):
            if self.warps > 0:
                self.warps -= 1
                self.warpSound.play()
                self.rect.bottom = WINDOW_HEIGHT

        def reset(self):
            self.rect.centerx = WINDOW_WIDTH//2
            self.rect.bottom = WINDOW_HEIGHT

    class Monster(pygame.sprite.Sprite):

        def __init__(self, x, y, image, monsterType):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

            #Monster type is an int 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
            self.type = monsterType

            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            self.velocity = random.randint(1, 5)

        def update(self):
            self.rect.x += self.dx*self.velocity
            self.rect.y += self.dy*self.velocity
            if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
                self.dx = -1*self.dx
            if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
                self.dy = -1*self.dy

    myPlayerGroup = pygame.sprite.Group()
    myPlayer = Player()
    myPlayerGroup.add(myPlayer)

    myMonsterGroup = pygame.sprite.Group()

    #TITLE SCREEN LOOP
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running = False

        displaySurface.fill((255,255,255))
        displaySurface.blit(titleText1, titleTextRect1)
        displaySurface.blit(titleText2, titleTextRect2)

        pygame.display.update()

    #GAME STARTS HERE
    myGame = Game(myPlayer, myMonsterGroup)
    myGame.startNewRound()

    #MAIN GAME LOOP
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    myPlayer.warp()
        
        displaySurface.fill((255, 255, 255))
        displaySurface.blit(backgroundImage, backgroundImageRect)
        myPlayerGroup.update()
        myPlayerGroup.draw(displaySurface)
        myMonsterGroup.update()
        myMonsterGroup.draw(displaySurface)
        myGame.update()
        myGame.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    
#monster()