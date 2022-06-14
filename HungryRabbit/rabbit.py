import pygame,random

WINDOW_WIDTH = 950
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


def hungry_rabbit():
    startGame()

    FPS = 60
    clock = pygame.time.Clock()

    WHITE = (255,255,255)
    RED = (255,0,0)
    BLACK = (0,0,0)
    GRAY = (192,192,192)
    ORANGE = (255,69,0)
    GREEN = (0,153,0)

    score = 0
    lives = 3
    boostLevel = 100
    carrotPoints = 0
    playerNormalVelocity = 8
    playerBoostVelocity = 20
    playerVelocity = playerNormalVelocity
    carrotVelocity = 3
    carrotAcceleration = 1
    bufferDistance = 100

    displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hungry Rabbit")

    #################################### IMAGES ##########################################

    backgroundImage = pygame.image.load("HungryRabbit/garden.jpg")
    backgroundImageRect = backgroundImage.get_rect()
    backgroundImageRect.bottom = WINDOW_HEIGHT

    rabbitLeftImage = pygame.image.load("HungryRabbit/rabbit_left.png")
    rabbitRightImage = pygame.image.load("HungryRabbit/rabbit_right.png")
    playerImage = rabbitLeftImage
    playerRect = playerImage.get_rect()
    playerRect.centerx = WINDOW_WIDTH//2
    playerRect.bottom = WINDOW_HEIGHT

    carrotImage = pygame.image.load("HungryRabbit/carrot.png")
    carrotRect = carrotImage.get_rect()
    carrotRect.topleft = (random.randint(0, WINDOW_WIDTH - 48), -bufferDistance)

    ############################## LINE AND RECTANGLE ###################################

    pygame.draw.line(displaySurface, BLACK, (0,120), (WINDOW_WIDTH,120), 10)
    pygame.draw.rect(displaySurface, WHITE, (0,0,WINDOW_WIDTH,116))

    ################################# FONTS ##########################################

    titleFont = pygame.font.Font("HungryRabbit/Shadow.ttf", 70)
    hudFont = pygame.font.Font("HungryRabbit/slum.ttf", 40)
    endFont = pygame.font.Font("HungryRabbit/Celosia.otf", 40)
    welcomeFont = pygame.font.Font("HungryRabbit/regular.ttf", 150)

    titleText = titleFont.render("Hungry Rabbit", True, ORANGE)
    titleRect = titleText.get_rect()
    titleRect.centerx = WINDOW_WIDTH//2 + 20
    titleRect.y = 0

    scoreText = hudFont.render("Score: " + str(score), True, BLACK)
    scoreRect = scoreText.get_rect()
    scoreRect.topleft = (10,10)

    carrotPointsText = hudFont.render("Carrot Points: " + str(carrotPoints), True, RED)
    carrotPointsRect = carrotPointsText.get_rect()
    carrotPointsRect.topleft = (10, 60)

    livesText = hudFont.render("Lives: " + str(lives), True, BLACK)
    livesRect = livesText.get_rect()
    livesRect.topright = (WINDOW_WIDTH - 10, 10)

    boostLevelText = hudFont.render("Boost Level: " + str(boostLevel), True, BLACK)
    boostLevelRect = boostLevelText.get_rect()
    boostLevelRect.topright = (WINDOW_WIDTH - 10, 60)

    gameOverText = titleFont.render("GAME OVER", True, RED)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.centerx = WINDOW_WIDTH//2
    gameOverRect.centery = WINDOW_HEIGHT//2 - 40

    finalScoreText = hudFont.render("Final Score: " + str(score), True, BLACK)
    finalScoreRect = finalScoreText.get_rect()
    finalScoreRect.x = 10
    finalScoreRect.y = 150

    continueText = endFont.render("Press any key to play again", True, GREEN)
    continueRect = continueText. get_rect()
    continueRect.centerx = WINDOW_WIDTH//2
    continueRect.centery = WINDOW_HEIGHT//2 + 20

    welcomeText = welcomeFont.render("Hungry Rabbit", True, ORANGE)
    welcomeRect = welcomeText.get_rect()
    welcomeRect.centerx = WINDOW_WIDTH//2 
    welcomeRect.centery = WINDOW_HEIGHT//2 - 80

    startText = endFont.render("Press any key to start the game", True, RED)
    startRect = startText.get_rect()
    startRect.centerx = WINDOW_WIDTH//2
    startRect.centery = WINDOW_HEIGHT//2

    ################################# MUSIC ##########################################

    pygame.mixer.music.load("HungryRabbit/bgm.wav")
    point = pygame.mixer.Sound("HungryRabbit/point.wav")
    point.set_volume(0.5)
    miss = pygame.mixer.Sound("HungryRabbit/miss.wav")
    miss.set_volume(0.3)

    ########################### TITLE SCREEN LOOP #####################################

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running = False

        displaySurface.fill(WHITE)
        displaySurface.blit(welcomeText,welcomeRect)
        displaySurface.blit(startText,startRect)
        pygame.display.update()

    #################################### MAIN GAME LOOP ###################################

    pygame.mixer.music.play(-1,0.0)
    running = True
    freeze = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
        #RABBIT CONTROLS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and playerRect.left > 0:
            playerRect.x -= playerVelocity
            playerImage = rabbitLeftImage
        if keys[pygame.K_RIGHT] and playerRect.right < WINDOW_WIDTH:
            playerRect.x += playerVelocity
            playerImage = rabbitRightImage
        if keys[pygame.K_UP] and playerRect.top > 120:
            playerRect.y -= playerVelocity
        if keys[pygame.K_DOWN] and playerRect.bottom < WINDOW_HEIGHT:
            playerRect.y += playerVelocity

        #BOOST CONTROLS
        if keys[pygame.K_SPACE] and boostLevel > 0:
            playerVelocity = playerBoostVelocity
            boostLevel -= 1
        else:
            playerVelocity = playerNormalVelocity
            
        #MOVING CARROT AND UPDATING CARROT POINTS
        carrotRect.y += carrotVelocity
        carrotPoints = WINDOW_HEIGHT - carrotRect.y

        #CHECK FOR COLLISION
        if playerRect.colliderect(carrotRect):
            point.play()
            score += carrotPoints
            carrotVelocity += carrotAcceleration
            boostLevel += 20
            if boostLevel > 100:
                boostLevel = 100
            carrotRect.topleft = (random.randint(0, WINDOW_WIDTH - 48), -bufferDistance)

        #PLAYER MISSES THE CARROT
        if carrotRect.bottom > WINDOW_HEIGHT + 30:
            miss.play()
            lives -= 1
            carrotVelocity = 3
            boostLevel = 100
            carrotRect.topleft = (random.randint(0, WINDOW_WIDTH - 48), -bufferDistance)
            playerRect.centerx = WINDOW_WIDTH//2
            playerRect.bottom = WINDOW_HEIGHT

        #CHECK FOR GAME OVER
        if lives == 0:
            pygame.mixer.music.stop()
            livesText = hudFont.render("Lives: " + str(lives), True, BLACK)
            displaySurface.fill(WHITE)
            pygame.draw.line(displaySurface, BLACK, (0,120), (WINDOW_WIDTH,120), 10)
            displaySurface.blit(backgroundImage, backgroundImageRect)
            displaySurface.blit(playerImage, playerRect)
            displaySurface.blit(carrotImage, carrotRect)
            displaySurface.blit(titleText,titleRect)
            displaySurface.blit(scoreText, scoreRect)
            displaySurface.blit(carrotPointsText, carrotPointsRect)
            displaySurface.blit(livesText, livesRect)
            displaySurface.blit(boostLevelText, boostLevelRect)
            displaySurface.blit(gameOverText, gameOverRect)
            displaySurface.blit(finalScoreText, finalScoreRect)
            displaySurface.blit(continueText, continueRect)
            pygame.display.update()
            isPaused = True
            while isPaused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        pygame.mixer.music.play(-1,0.0)
                        score = 0
                        lives = 3
                        carrotPoints = 0
                        isPaused = False
                    elif event.type == pygame.QUIT:
                        isPaused = False
                        running = False
                        pygame.quit()
                    else:
                        pass

        #UPDATE HUD
        scoreText = hudFont.render("Score: " + str(score), True, BLACK)
        carrotPointsText = hudFont.render("Carrot Points: " + str(carrotPoints), True, RED)
        livesText = hudFont.render("Lives: " + str(lives), True, BLACK)
        boostLevelText = hudFont.render("Boost Level: " + str(boostLevel), True, BLACK)
        finalScoreText = hudFont.render("Final Score: " + str(score), True, BLACK)

        #ADDING ELEMENTS TO DISPLAY
        displaySurface.fill(WHITE)
        pygame.draw.line(displaySurface, BLACK, (0,120), (WINDOW_WIDTH,120), 10)
        displaySurface.blit(backgroundImage, backgroundImageRect)
        displaySurface.blit(playerImage, playerRect)
        displaySurface.blit(carrotImage, carrotRect)
        displaySurface.blit(titleText,titleRect)
        displaySurface.blit(scoreText, scoreRect)
        displaySurface.blit(carrotPointsText, carrotPointsRect)
        displaySurface.blit(livesText, livesRect)
        displaySurface.blit(boostLevelText, boostLevelRect)

        pygame.display.update()
        clock.tick(FPS)

    #pygame.quit()