import pygame, random

WINDOW_WIDTH = 900
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

def snake():
    startGame()
    

    displaySurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) 
    pygame.display.set_caption("Snake")

    BLUE = (0,255,255)
    DARK_BLUE = (0,64,255)
    BLACK  = (0,0,0)

    FPS = 24
    clock = pygame.time.Clock() 

    #BODY VARIABLES
    snakeSize = 20
    headX = WINDOW_WIDTH//2
    headY = WINDOW_HEIGHT//2

    #MOVEMENT VARIABLES
    snakeDX = 0
    snakeDY = 0

    score = 0

    headCord = (headX, headY, snakeSize, snakeSize)
    headRect = pygame.draw.rect(displaySurface, BLUE, headCord)

    bodyCords = []

    ################################################ IMAGES #########################################################

    appleIMG = pygame.image.load("Snake/apple.png")
    appleRect = appleIMG.get_rect()
    appleRect.x = random.randint(0, WINDOW_WIDTH-48)
    appleRect.y = random.randint(150, WINDOW_HEIGHT-48)

    backgroundIMG = pygame.image.load("Snake/img.jpg")
    backgroundRect = backgroundIMG.get_rect()
    backgroundRect.x = 0
    backgroundRect.bottom = WINDOW_HEIGHT

    pygame.draw.line(displaySurface, (0,0,0), (0,100), (WINDOW_WIDTH,100), 10)

    ################################################ AUDIOS #########################################################

    pygame.mixer.music.load("Snake/backgroundbgm.wav")
    point = pygame.mixer.Sound("Snake/pick.wav")
    point.set_volume(0.3)
    miss = pygame.mixer.Sound("Snake/Zap.wav")
    miss.set_volume(0.3)

    ############################################### FONTS ###########################################################

    Font = pygame.font.Font("Snake/lemon.otf", 70)
    endFont = pygame.font.Font("Snake/lemon.otf", 50)
    welcomeFont = pygame.font.Font("Snake/lemon.otf", 90)
    startFont = pygame.font.Font("Snake/lemon.otf", 45)

    titleText = Font.render("SNAKE", True, BLACK)
    titleRect = titleText.get_rect()
    titleRect.x = 20
    titleRect.y = 0

    scoreText = Font.render("Score: " + str(score), True, BLACK)
    scoreRect = scoreText.get_rect()
    scoreRect.topright = (WINDOW_WIDTH - 40, 0)

    gameOverText = endFont.render("GAME OVER", True, BLACK, (255,255,255))
    gameOverRect = gameOverText.get_rect()
    gameOverRect.centerx = WINDOW_WIDTH//2
    gameOverRect.centery = WINDOW_HEIGHT//2 - 50

    continueText = endFont.render("Press enter to play again", True, (255,255,255), BLACK)
    continueRect = continueText.get_rect()
    continueRect.centerx = WINDOW_WIDTH//2
    continueRect.centery = WINDOW_HEIGHT//2 + 30

    welcomeText = welcomeFont.render("SNAKE", True, BLACK)
    welcomeRect = welcomeText.get_rect()
    welcomeRect.centerx = WINDOW_WIDTH//2
    welcomeRect.centery = WINDOW_HEIGHT//2 - 60

    startText = startFont.render("Press any key to start the game", True,(255,255,255), BLACK)
    startRect = startText.get_rect()
    startRect.centerx = WINDOW_WIDTH//2
    startRect.centery = WINDOW_HEIGHT//2 + 20

    ######################################### TITLE SCREEN LOOP #####################################################

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                running = False

        displaySurface.fill((255,255,255))
        displaySurface.blit(welcomeText, welcomeRect)
        displaySurface.blit(startText, startRect)
        pygame.display.update()

    ########################################## MAIN GAME LOOP #######################################################

    pygame.mixer.music.play(-1, 0.0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit
            
            #MOVEMENT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snakeDX != 1 * snakeSize:
                        snakeDX = -1 * snakeSize
                        snakeDY = 0
                if event.key == pygame.K_RIGHT:
                    if snakeDX != -1 * snakeSize:
                        snakeDX = 1 * snakeSize
                        snakeDY = 0
                if event.key == pygame.K_UP:
                    if snakeDY != 1 * snakeSize:
                        snakeDX = 0
                        snakeDY = -1 * snakeSize
                if event.key == pygame.K_DOWN:
                    if snakeDY != -1 * snakeSize:
                        snakeDX = 0
                        snakeDY = 1 * snakeSize

        #SNAKE BODY WILL FOLLOW ALONG
        bodyCords.insert(0, headCord)
        bodyCords.pop()

        #MOVEMENT
        headX += snakeDX
        headY += snakeDY  
        headCord = (headX, headY, snakeSize, snakeSize)
        
        #CHECK FOR GAME OVER
        if headRect.left < 0 or headRect.right > WINDOW_WIDTH or headRect.top < 100 or headRect.bottom > WINDOW_HEIGHT or headCord in bodyCords:
            miss.play()
            pygame.mixer.music.stop()
            displaySurface.blit(gameOverText,gameOverRect)
            displaySurface.blit(continueText, continueRect)
            pygame.display.update()
            isPaused = True
            while isPaused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            score = 0
                            headX = WINDOW_WIDTH//2
                            headY = WINDOW_HEIGHT//2 + 100
                            headCord = (headX, headY, snakeSize, snakeSize)
                            bodyCords = []
                            snakeDX = 0
                            snakeDY = 0
                            pygame.mixer.music.play(-1, 0.0)
                            isPaused = False
                    elif event.type == pygame.QUIT:
                        isPaused = False
                        running = False
                        pygame.quit
                    else:
                        pass
                    

        #DISPLAY
        displaySurface.fill((255,255,255))
        displaySurface.blit(backgroundIMG, backgroundRect)
        pygame.draw.line(displaySurface, (0,0,0), (0,100), (WINDOW_WIDTH,100), 10)
        displaySurface.blit(titleText, titleRect)
        displaySurface.blit(scoreText, scoreRect)
        headRect = pygame.draw.rect(displaySurface, BLUE, headCord)
        pygame.draw.rect(displaySurface, (0,0,0), headRect, 3)
        displaySurface.blit(appleIMG, appleRect)

        #CHECK FOR POINTS
        if headRect.colliderect(appleRect):
            point.play()
            score += 1
            appleRect.x = random.randint(0, WINDOW_WIDTH-48)
            appleRect.y = random.randint(150, WINDOW_HEIGHT-48)  
            bodyCords.append(headCord)

        scoreText = Font.render("Score: " + str(score), True, BLACK)

        #INCREMENTING SNAKE BODY
        for body in bodyCords:
            pygame.draw.rect(displaySurface, DARK_BLUE, body)
            pygame.draw.rect(displaySurface, (0,0,0), body, 3)
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()