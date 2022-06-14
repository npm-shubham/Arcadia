import pygame
import random
import os


FPS = 40
SCREENSIZE = (640, 640)
SKIER_IMAGE_PATHS = [
    os.path.join(os.getcwd(), 'Skier/resources/images/skier_forward.png'),
    os.path.join(os.getcwd(), 'Skier/resources/images/skier_right1.png'),
    os.path.join(os.getcwd(), 'Skier/resources/images/skier_right2.png'),
    os.path.join(os.getcwd(), 'Skier/resources/images/skier_left2.png'),
    os.path.join(os.getcwd(), 'Skier/resources/images/skier_left1.png'),
    os.path.join(os.getcwd(), 'Skier/resources/images/skier_fall.png')
]
OBSTACLE_PATHS = {
    'tree': os.path.join(os.getcwd(), 'Skier/resources/images/tree.png'),
    'flag': os.path.join(os.getcwd(), 'Skier/resources/images/flag.png')
}
MENUPATH = os.path.join(os.getcwd(), 'Skier/resources/music/menu_bgm.mp3')
BGMPATH = os.path.join(os.getcwd(), 'Skier/resources/music/bgm.mp3')
GAMESTARTPATH = os.path.join(
    os.getcwd(), 'Skier/resources/sfx/sfx_game_start.wav')
FLAGPATH = os.path.join(os.getcwd(), 'Skier/resources/sfx/sfx_flag.wav')
CRASHPATH = os.path.join(os.getcwd(), 'Skier/resources/sfx/sfx_crash.wav')
GAMEOVERPATH = os.path.join(
    os.getcwd(), 'Skier/resources/sfx/sfx_game_over.wav')
FONTPATH = os.path.join(os.getcwd(), 'Skier/resources/font/PressStart2P.TTF')


def quitGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            else:
                pass


class SkierClass(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.direction = 0
        self.imagepaths = SKIER_IMAGE_PATHS[:-1]
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.speed = [self.direction, 6-abs(self.direction)*2]

    def turn(self, num):
        self.direction += num
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = [self.direction, 6-abs(self.direction)*2]
        return self.speed

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)

    def setFall(self):
        self.image = pygame.image.load(SKIER_IMAGE_PATHS[-1])

    def setForward(self):
        self.direction = 0
        self.image = pygame.image.load(self.imagepaths[self.direction])


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, img_path, location, attribute):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.attribute = attribute
        self.passed = False

    def move(self, num):
        self.rect.centery = self.location[1] - num


def createObstacles(s, e, num=10):
    obstacles = pygame.sprite.Group()
    locations = []
    for i in range(num):
        row = random.randint(s, e)
        col = random.randint(0, 9)
        location = [col*64+20, row*64+20]
        if location not in locations:
            locations.append(location)
            attribute = random.choice(list(OBSTACLE_PATHS.keys()))
            img_path = OBSTACLE_PATHS[attribute]
            obstacle = ObstacleClass(img_path, location, attribute)
            obstacles.add(obstacle)
    return obstacles


def AddObstacles(obstacles0, obstacles1):
    obstacles = pygame.sprite.Group()
    for obstacle in obstacles0:
        obstacles.add(obstacle)
    for obstacle in obstacles1:
        obstacles.add(obstacle)
    return obstacles


def ShowStartInterface(screen, screensize):
    screen.fill((255, 255, 255))
    tfont = pygame.font.Font(FONTPATH, screensize[0]//11)
    cfont = pygame.font.Font(FONTPATH, screensize[0]//30)
    title = tfont.render(u'Skier Game', True, (255, 0, 0))
    content = cfont.render(u'Press any key to START.', True, (0, 0, 255))
    trect = title.get_rect()
    trect.midtop = (screensize[0]/2, screensize[1]/5)
    crect = content.get_rect()
    crect.midtop = (screensize[0]/2, screensize[1]/2)
    screen.blit(title, trect)
    screen.blit(content, crect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()


def ShowEndInterface(screen, screensize):
    screen.fill((255, 255, 255))
    tfont = pygame.font.Font(FONTPATH, screensize[0]//10)
    cfont = pygame.font.Font(FONTPATH, screensize[0]//30)
    title = tfont.render(u'Game Over', True, (255, 0, 0))
    content = cfont.render(u'Press any key to PLAY AGAIN.', True, (0, 0, 255))
    trect = title.get_rect()
    trect.midtop = (screensize[0]/2, screensize[1]/3)
    crect = content.get_rect()
    crect.midtop = (screensize[0]/2, screensize[1]/2)
    screen.blit(title, trect)
    screen.blit(content, crect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()


def showScore(screen, score, lives, pos=(10, 10)):
    font = pygame.font.Font(FONTPATH, 25)
    score_text = font.render("Score: %s" % score, True, (0, 0, 0))
    lives_text = font.render("Lives: %s" % lives, True, (0, 0, 0))
    screen.blit(score_text, pos)
    screen.blit(lives_text, (435, 10))


def updateFrame(screen, obstacles, skier, score, lives):
    screen.fill((255, 255, 255))
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    showScore(screen, score, lives)
    pygame.display.update()


def game(game_repeated=False):
    pygame.init()
    # music
    pygame.mixer.init()
    if not game_repeated:
        pygame.mixer.music.load(MENUPATH)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    # sounds
    flag_sfx = pygame.mixer.Sound(FLAGPATH)
    crash_sfx = pygame.mixer.Sound(CRASHPATH)
    gameover_sfx = pygame.mixer.Sound(GAMEOVERPATH)
    gamestart_sfx = pygame.mixer.Sound(GAMESTARTPATH)

    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Skier Game')

    if not game_repeated:
        ShowStartInterface(screen, SCREENSIZE)
        pygame.mixer.music.unload()

    pygame.mixer.Sound.play(gamestart_sfx)
    pygame.time.delay(800)
    pygame.mixer.music.load(BGMPATH)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    skier = SkierClass()

    obstacles0 = createObstacles(20, 29)
    obstacles1 = createObstacles(10, 19)
    obstaclesflag = 0
    obstacles = AddObstacles(obstacles0, obstacles1)

    clock = pygame.time.Clock()

    distance = 0

    score = 0
    lives = 3
    speed = [0, 6]

    is_running = True

    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    speed = skier.turn(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    speed = skier.turn(1)
        skier.move()
        distance += speed[1]
        if distance >= 640 and obstaclesflag == 0:
            obstaclesflag = 1
            obstacles0 = createObstacles(20, 29)
            obstacles = AddObstacles(obstacles0, obstacles1)

        if distance >= 1280 and obstaclesflag == 1:
            obstaclesflag = 0
            distance -= 1280
            for obstacle in obstacles0:
                obstacle.location[1] = obstacle.location[1] - 1280
            obstacles1 = createObstacles(10, 19)
            obstacles = AddObstacles(obstacles0, obstacles1)

        for obstacle in obstacles:
            obstacle.move(distance)

        hitted_obstacles = pygame.sprite.spritecollide(skier, obstacles, False)
        if hitted_obstacles:
            if hitted_obstacles[0].attribute == "tree" and not hitted_obstacles[0].passed:
                pygame.mixer.Sound.play(crash_sfx)
                score -= 50
                lives -= 1
                skier.setFall()
                updateFrame(screen, obstacles, skier, score, lives)
                pygame.time.delay(1000)
                if lives == 0:
                    pygame.mixer.music.fadeout(500)
                    pygame.mixer.Sound.play(gameover_sfx)
                    is_running = False

                skier.setForward()
                speed = [0, 6]
                hitted_obstacles[0].passed = True

            elif hitted_obstacles[0].attribute == "flag" and not hitted_obstacles[0].passed:
                pygame.mixer.Sound.play(flag_sfx)
                score += 10
                obstacles.remove(hitted_obstacles[0])

        updateFrame(screen, obstacles, skier, score, lives)
        clock.tick(FPS)

    ShowEndInterface(screen, SCREENSIZE)
    pygame.quit()


# if __name__ == '__main__':
def skier():
    game()
    while True:
        game(game_repeated=True)
