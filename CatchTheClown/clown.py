import pygame, random, sys

WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600

def startGame():
    pygame.init()

def quitGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            else :
                pass

#start of game execution
def catch_the_clown():
    startGame()

    FPS = 60
    clock = pygame.time.Clock()

    GREEN = (181,230,29)
    BROWN = (185,122,87)

    score = 0
    lives = 5

    clownVelocity = 5
    clownAccerlation = 0.75
    clownDX = random.choice([-1 , 1])
    clownDY = random.choice([-1 , 1])

    displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Catch The Clown")

    ################################################ IMAGES #########################################################

    backgroundImage = pygame.image.load("CatchTheClown/background.png")
    backgroundImageRect = backgroundImage.get_rect()
    backgroundImageRect.topleft = (0,0)
    
    clownImage = pygame.image.load("CatchTheClown/clown.png")
    clownImageRect = clownImage.get_rect()
    clownImageRect.centerx = WINDOW_WIDTH//2
    clownImageRect.centery = WINDOW_HEIGHT//2

    ############################################### FONTS ###########################################################

    titleFont = pygame.font.Font("CatchTheClown/Celosia.otf", 50)
    hudFont = pygame.font.Font("CatchTheClown/Celosia.otf", 40)

    titleText = titleFont.render("Catch The Clown", True, GREEN)
    titleRect = titleText.get_rect()
    titleRect.topleft = (20, 10)

    scoreText = hudFont.render("Score: " + str(score), True, BROWN)
    scoreRect = scoreText.get_rect()
    scoreRect.topright = (WINDOW_WIDTH-20, 5)

    livesText = hudFont.render("Lives: " + str(lives), True, BROWN)
    livesRect = livesText.get_rect()
    livesRect.topright = (WINDOW_WIDTH-20, 55)

    gameOverText = titleFont.render("GAME OVER", True, GREEN, BROWN)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.centerx = WINDOW_WIDTH//2
    gameOverRect.centery = WINDOW_HEIGHT//2

    continueText = hudFont.render("Click anywhere to play again", True, BROWN, GREEN)
    continueRect = continueText.get_rect()
    continueRect.centerx = WINDOW_WIDTH//2
    continueRect.centery = WINDOW_HEIGHT//2 + 50

    welcomeText = titleFont.render("Catch The Clown", True, GREEN, BROWN)
    welcomeRect = welcomeText.get_rect()
    welcomeRect.centerx = WINDOW_WIDTH//2
    welcomeRect.centery = WINDOW_HEIGHT//2 - 45

    startText = hudFont.render("Click anywhere to start the game", True, BROWN, GREEN)
    startRect = startText.get_rect()
    startRect.centerx = WINDOW_WIDTH//2
    startRect.centery = WINDOW_HEIGHT//2 + 10

    ################################################ AUDIOS #########################################################

    point = pygame.mixer.Sound("CatchTheClown/SonicRingg.wav")
    point.set_volume(0.7)
    miss = pygame.mixer.Sound("CatchTheClown/Zap.wav")
    miss.set_volume(0.2)
    pygame.mixer.music.load("CatchTheClown/clownbgm.wav")

    ########################################## TITLE SCREEN LOOP ####################################################

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        displaySurface.blit(backgroundImage, backgroundImageRect)
        displaySurface.blit(welcomeText, welcomeRect)
        displaySurface.blit(startText, startRect)
        displaySurface.blit(clownImage, (685,225))
        displaySurface.blit(clownImage, (195,225))
        pygame.display.update()

    ########################################## MAIN GAME LOOP #######################################################

    pygame.mixer.music.play(-1, 0.0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            #CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                #CLICK ON CLOWN
                if clownImageRect.collidepoint(mouseX, mouseY):
                    point.play()
                    score += 1
                    clownVelocity += clownAccerlation
                    previousDX = clownDX
                    previousDY = clownDY
                    while previousDX == clownDX and previousDY == clownDY:
                        clownDX = random.choice([-1, 1])
                        clownDY = random.choice([-1, 1])

                #MISS
                else:
                    miss.play()
                    lives -= 1

        #CHECK FOR GAME OVER
        if lives == 0:
            pygame.mixer.music.stop()
            displaySurface.blit(gameOverText, gameOverRect)
            displaySurface.blit(continueText,continueRect)
            pygame.display.update()

            isPaused = True
            while isPaused:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        score = 0
                        lives = 5
                        clownImageRect.centerx = WINDOW_WIDTH//2
                        clownImageRect.centery = WINDOW_HEIGHT//2
                        clownVelocity = 5
                        pygame.mixer.music.play(-1, 0.0)
                        isPaused = False
                    elif event.type == pygame.QUIT:
                        isPaused = False
                        running = False
                        pygame.quit()
                    else:
                        pass


        #UPDATE HUD
        scoreText = hudFont.render("Score: " + str(score), True, BROWN)
        livesText = hudFont.render("Lives: " + str(lives), True, BROWN)

        #MOVING THE CLOWN
        clownImageRect.x += clownDX * clownVelocity
        clownImageRect.y += clownDY * clownVelocity

        #BOUNCING THE CLOWN OFF THE EDGES
        if clownImageRect.left <= 0 or clownImageRect.right >= WINDOW_WIDTH:
            clownDX = clownDX * -1
        if clownImageRect.top <= 0 or clownImageRect.bottom >= WINDOW_HEIGHT:
            clownDY = clownDY * -1

        #DISPLAY
        displaySurface.blit(backgroundImage, backgroundImageRect)
        displaySurface.blit(titleText, titleRect)
        displaySurface.blit(scoreText, scoreRect)
        displaySurface.blit(livesText, livesRect)
        displaySurface.blit(clownImage, clownImageRect)


        pygame.display.update()
        clock.tick(FPS)

    #pygame.quit()