import pygame, random
pygame.init()

WINDOW_WIDTH = 1312
WINDOW_HEIGHT = 700

BLACK = (0,0,0)
WHITE = (255,255,255)

def startGame():
    pygame.init()

def quitGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            else :
                pass

def spaceInvader():
    startGame()
    displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    FPS = 60
    clock = pygame.time.Clock()

    backgroundImage = pygame.image.load("SpaceInvader/bg.jpg")
    backgroundImageRect = backgroundImage.get_rect()
    backgroundImageRect.x = 0
    backgroundImageRect.y = 100


    class Game():

        def __init__(self, player, alienGroup, playerBulletGroup, alienBulletGroup):
            self.roundNumber = 1
            self.score = 0

            self.player = player
            self.alienGroup = alienGroup
            self.playerBulletGroup = playerBulletGroup
            self.alienBulletGroup = alienBulletGroup

            self.newRoundSound = pygame.mixer.Sound("SpaceInvader/new_round.wav")
            self.newRoundSound.set_volume(0.2)
            self.breachSound = pygame.mixer.Sound("SpaceInvader/breach.wav")
            self.breachSound.set_volume(0.3)
            self.alienHitSound = pygame.mixer.Sound("SpaceInvader/alien_hit.wav")
            self.alienHitSound.set_volume(0.3)
            self.playerHitSound = pygame.mixer.Sound("SpaceInvader/player_hit.wav")
            self.playerHitSound.set_volume(0.2)

            self.font = pygame.font.Font("SpaceInvader/Facon.ttf", 50)

        def update(self):
            self.shiftAliens()
            self.checkCollisions()
            self.checkRoundCompletion()

        def shiftAliens(self):

            shift = False

            for alien in (self.alienGroup.sprites()):
                if alien.rect.left <= 0 or alien.rect.right >= WINDOW_WIDTH:
                    shift = True

            if shift:
                breach = False
                for alien in (self.alienGroup.sprites()):
                    alien.rect.y += 10*self.roundNumber

                    alien.direction = -1*alien.direction
                    alien.rect.x += alien.direction*alien.velocity

                    if alien.rect.bottom >= WINDOW_HEIGHT - 100:
                        breach = True
                        
                if breach:
                    self.breachSound.play()
                    self.player.lives -= 1
                    self.checkGameStatus("Aliens breached the line!", "Press 'Enter' to continue")

        def checkCollisions(self):
            if pygame.sprite.groupcollide(self.playerBulletGroup, self.alienGroup, True, True):
                self.alienHitSound.play()
                self.score += 100

            if pygame.sprite.spritecollide(self.player, self.alienBulletGroup, True):
                self.playerHitSound.play()
                self.player.lives -= 1
                self.checkGameStatus("You've been hit!", "Press 'Enter' to continue")

        def checkRoundCompletion(self):
            if not (self.alienGroup):
                self.score += 1000*self.roundNumber
                self.roundNumber += 1
                
                self.startNewRound()

        def draw(self):
            scoreText = self.font.render("Score: " + str(self.score), True, BLACK)
            scoreRect = scoreText.get_rect()
            scoreRect.centerx = WINDOW_WIDTH//2
            scoreRect.top = 20

            roundText = self.font.render("Round: " + str(self.roundNumber), True, BLACK)
            roundRect = roundText.get_rect()
            roundRect.topleft = (20, 20)

            livesText = self.font.render("Lives: " + str(self.player.lives), True, BLACK)
            livesRect = livesText.get_rect()
            livesRect.topright = (WINDOW_WIDTH - 20, 20)
            
            displaySurface.blit(scoreText, scoreRect)
            displaySurface.blit(roundText, roundRect)
            displaySurface.blit(livesText, livesRect)

            pygame.draw.line(displaySurface, (255,0,0), (0,100), (WINDOW_WIDTH,100), 5)

        def startNewRound(self):
            for i in range(10):
                for j in range(3):
                    alien = Alien(64 + i*64, 64 + j*64 + 40, self.roundNumber, self.alienBulletGroup)
                    self.alienGroup.add(alien)

            self.newRoundSound.play()
            self.pauseGame("Space Invaders Round " + str(self.roundNumber), "Press 'Enter' to begin")

        def checkGameStatus(self, mainText, subText):
            self.alienBulletGroup.empty()
            self.playerBulletGroup.empty()
            self.player.reset()
            for alien in self.alienGroup:
                alien.reset()

            if self.player.lives == 0:
                self.resetGame()
            else:
                self.pauseGame(mainText, subText)

        def pauseGame(self, mainText, subText):
            global running

            mainText = self.font.render(mainText, True, WHITE)
            mainRect = mainText.get_rect()
            mainRect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40 )

            subText = self.font.render(subText, True, WHITE)
            subRect = subText.get_rect()
            subRect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10)

            displaySurface.fill(BLACK)
            displaySurface.blit(mainText, mainRect)
            displaySurface.blit(subText, subRect)
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
                        pygame.quit()

        def resetGame(self):
            self.pauseGame("Final Score: " + str(self.score), "Press 'Enter' to play again")

            self.score = 0
            self.roundNumber = 1
            self.player.lives = 5

            self.alienGroup.empty()
            self.alienBulletGroup.empty()
            self.playerBulletGroup.empty()

            self.startNewRound()

    class Player(pygame.sprite.Sprite):
        def __init__(self, bulletGroup):
            super().__init__()
            self.image = pygame.image.load("SpaceInvader/player_ship.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = WINDOW_WIDTH//2
            self.rect.bottom = WINDOW_HEIGHT

            self.lives = 5
            self.velocity = 8

            self.bulletGroup = bulletGroup

            self.shootSound = pygame.mixer.Sound("SpaceInvader/player_fire.wav")
            self.shootSound.set_volume(0.2)

        def update(self):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.velocity
            if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
                self.rect.x += self.velocity

        def fire(self):
            if len(self.bulletGroup) < 2:
                self.shootSound.play()
                PlayerBullet(self.rect.centerx, self.rect.top, self.bulletGroup)

        def reset(self):
            self.rect.centerx = WINDOW_WIDTH//2

    class Alien(pygame.sprite.Sprite):
        def __init__(self, x, y, velocity, bulletGroup):
            super().__init__()
            self.image = pygame.image.load("SpaceInvader/alien.png")
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

            self.startingX = x
            self.startingY = y

            self.direction = 1
            self.velocity = velocity
            self.bulletGroup = bulletGroup

            self.shootSound = pygame.mixer.Sound("SpaceInvader/alien_fire.wav")
            self.shootSound.set_volume(0.2)

        def update(self):
            self.rect.x += self.direction*self.velocity
            if random.randint(0, 1000) > 999 and len(self.bulletGroup) < 3:
                self.shootSound.play()
                self.fire()

        def fire(self):
            AlienBullet(self.rect.centerx, self.rect.bottom, self.bulletGroup)

        def reset(self):
            self.rect.topleft = (self.startingX, self.startingY)
            self.direction = 1

    class PlayerBullet(pygame.sprite.Sprite):
        def __init__(self, x, y, bulletGroup):
            super().__init__()
            self.image = pygame.image.load("SpaceInvader/green_laser.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

            self.velocity = 10
            bulletGroup.add(self)

        def update(self):
            self.rect.y -= self.velocity
            if self.rect.top < 100:
                self.kill()

    class AlienBullet(pygame.sprite.Sprite):
        def __init__(self, x, y, bulletGroup):
            super().__init__()
            self.image = pygame.image.load("SpaceInvader/red_laser.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

            self.velocity = 10
            bulletGroup.add(self)

        def update(self):
            self.rect.y += self.velocity

            if self.rect.top > WINDOW_HEIGHT:
                self.kill()

    myPlayerBulletGroup = pygame.sprite.Group()
    myAlienBulletGroup = pygame.sprite.Group()

    myPlayerGroup = pygame.sprite.Group()
    myPlayer = Player(myPlayerBulletGroup) 
    myPlayerGroup.add(myPlayer)

    myAlienGroup = pygame.sprite.Group()

    myGame = Game(myPlayer, myAlienGroup, myPlayerBulletGroup, myAlienBulletGroup)
    myGame.startNewRound()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    myPlayer.fire()   
        
        displaySurface.fill(WHITE)
        displaySurface.blit(backgroundImage, backgroundImageRect)
        
        myPlayerGroup.update()
        myPlayerGroup.draw(displaySurface)

        myAlienGroup.update()
        myAlienGroup.draw(displaySurface)

        myPlayerBulletGroup.update()
        myPlayerBulletGroup.draw(displaySurface)

        myAlienBulletGroup.update()
        myAlienBulletGroup.draw(displaySurface)

        myGame.update()
        myGame.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()