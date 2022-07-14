import pygame,sys,random

# General Stuff
pygame.init()
clock = pygame.time.Clock()

# Screen Settings
screenWidth = 400
screenHeight = 500

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tyler's Breakout")

# Fonts
small_font = pygame.font.Font(None, 20)
medium_font = pygame.font.Font(None, 40)
large_font = pygame.font.Font(None, 60)

# Colors
#(r, g, b, alpha)
light_black = pygame.Color(10, 10, 10)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0 , 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
orange = pygame.Color(255, 128, 0)
purple = pygame.Color(87, 0, 128)

# This color is generally used for collision boxes
hidden = pygame.Color(0, 0, 0, 0)

# Important Variables
game_scene = "main menu" # Decides what state the game is in.

# Classes
class Ball:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x - (width/2), y - (height/2), width, height)
        
        # Ball speed values
        self.speed_x = random.choice((2,-2))
        self.speed_y = 2
    
    def update(self, color):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y
        
        #This will be used for bounce colisions
        #(x, y, width, height)
        self.toprect = pygame.Rect(self.rect.x + 1, self.rect.y, 8, 1)
        self.bottomrect = pygame.Rect(self.rect.x + 1, self.rect.y + 9, 8, 1)
        self.leftrect = pygame.Rect(self.rect.x, self.rect.y + 1, 1, 8)
        self.rightrect = pygame.Rect(self.rect.x + 9, self.rect.y + 1, 1, 8)
        
        # Draws the invisible collision boxes for the ball instance.
        pygame.draw.rect(screen, hidden, self.toprect)
        pygame.draw.rect(screen, hidden, self.bottomrect)
        pygame.draw.rect(screen, hidden, self.leftrect)
        pygame.draw.rect(screen, hidden, self.rightrect)
        
        # Draws the ball instance
        pygame.draw.rect(screen, color, self)

class Border:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
        
    def update(self, color):
        # What happens if a ball's left or right rect collides with a object.
        if ball.leftrect.colliderect(self) or ball.rightrect.colliderect(self):
            ball.speed_x *= -1 
        # What happens if a ball's top or bottom rect collides with a object.
        if ball.toprect.colliderect(self) or ball.bottomrect.colliderect(self):
            ball.speed_y *= -1
            ball.speed_x *= random.choice((-1,1))
        
        #Draws the border instance.
        pygame.draw.rect(screen, color, self)

class Player(Border):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x - (width/2), y - (height/2), width, height)
        # Basic speed values
        self.speed = 4

    def update(self, color):
        # Moves player when key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.move_ip(-self.speed, 0)
            if event.key == pygame.K_RIGHT:
                self.rect.move_ip(self.speed, 0)
        
        # This simply stops the player from going through the borders
        if self.rect.left <= 20:
            self.rect.left = 20
        if self.rect.right >= 380:
            self.rect.right = 380
        
        # Thanks to class inheritance, the is class and all of it's instances should be able to have ball collision.
        return super().update(color)

class blockClass(Border):
    def __init__(self, x, y):
        # This checks if block is destroyed.
        self.destroyed = 0
        super().__init__(x, y, 40, 20)
    
    def update(self, color):
        # If the self.destroyed is 1, then the block will disappear
        if self.destroyed == 0:
            # What happens if ball collides with block
            if ball.rect.colliderect(self):
                self.destroyed = 1
                
            # I don't need to code the basic ball collision because the class is the child of Border and it should inherit most of the code typed into the Border Class
            return super().update(color)
        
        
# Game States
def title_screen():
    global game_scene
    # Renders the title screen elements
    title_text = large_font.render("Break Out", True, white)
    credits_text = small_font.render("Break Out clone made by: Tyler Dillard, 2022", True, white)
    play_button = medium_font.render("Play", True, white)
    
    # This gets the position of mouse and the rect of play_button
    pos = pygame.mouse.get_pos()
    button = play_button.get_rect()
    button.center = 200, 250
    
    # Checks if mouse cursor is hovering over button.
    if button.collidepoint(pos):
        # This changes the text color to red if cursor is hovering over button.
        play_button = medium_font.render("Play", True, red)
        # Starts the game if button is pressed.
        if pygame.mouse.get_pressed()[0] == 1:
            game_scene = "game"
            print("Starting the game...")
    else:
        # This changes the text color back to white if not.
        play_button = medium_font.render("Play", True, white)
        
    # Draws everything on to the screen
    screen.blit(title_text, (100, 100))
    screen.blit(credits_text, (0, 485))
    screen.blit(play_button, button)
    

def game_screen():
    global game_scene
    # Draws all the instances onto the screen
    ball.update(white)
    player.update(white)
    
    wall_top.update(white)
    wall_left.update(white)
    wall_right.update(white)
    
    # Updating Block Rows
    for item in block_row1:
        item.update(red)
    for item in blockrow2:
        item.update(orange)
    for item in blockrow3:
        item.update(yellow)
    for item in blockrow4:
        item.update(green)
    for item in blockrow5:
        item.update(blue)
    for item in blockrow6:
        item.update(purple)
    
    # Takes you back to the title screen and resets the everything if ball gets offscreen.
    if ball.rect.y > 550:
        ball.rect.center = ((200,450))
        player.rect.center = ((200, 490))
        
        ball.speed_y *= -1
        ball.speed_x *= random.choice((-1,1))
        
        for item in everyBlock:
            for i in item:
                i.destroyed = 0
        
        print("Game Over")
        game_scene = "main menu"

# Class Instances
ball = Ball(200, 450, 10, 10)
player = Player(200, 490, 25, 10)

wall_top = Border(0, 0, 400, 20)
wall_left = Border(0, 20, 20, 500)
wall_right = Border(380, 20, 20, 500)

# This will always activate no matter what, it's there so I can collapse the block instance code in my IDE so I can read my code easier
if True: # Block Instances
    # Block Row 1 - (x, y)
    b1 = blockClass(20, 80)
    b2 = blockClass(60, 80)
    b3 = blockClass(100, 80)
    b4 = blockClass(140, 80)
    b5 = blockClass(180, 80)
    b6 = blockClass(220, 80)
    b7 = blockClass(260, 80)
    b8 = blockClass(300, 80)
    b9 = blockClass(340, 80)
    block_row1 = [b1,b2,b3,b4,b5,b6,b7,b8,b9]
    
    # Block Row 2
    b10 = blockClass(20, 100)
    b11 = blockClass(60, 100)
    b12 = blockClass(100, 100)
    b13 = blockClass(140, 100)
    b14 = blockClass(180, 100)
    b15 = blockClass(220, 100)
    b16 = blockClass(260, 100)
    b17 = blockClass(300, 100)
    b18 = blockClass(340, 100)
    blockrow2 = [b10,b11,b12,b13,b14,b15,b16,b17,b18]
    
    #Block Row 3
    b19 = blockClass(20, 120)
    b20 = blockClass(60, 120)
    b21 = blockClass(100, 120)
    b22 = blockClass(140, 120)
    b23 = blockClass(180, 120)
    b24 = blockClass(220, 120)
    b25 = blockClass(260, 120)
    b26 = blockClass(300, 120)
    b27 = blockClass(340, 120)
    blockrow3 = [b19,b20,b21,b22,b23,b24,b25,b26,b27]
    
    #Block Row 4
    b28 = blockClass(20, 140)
    b29 = blockClass(60, 140)
    b30 = blockClass(100, 140)
    b31 = blockClass(140, 140)
    b32 = blockClass(180, 140)
    b33 = blockClass(220, 140)
    b34 = blockClass(260, 140)
    b35 = blockClass(300, 140)
    b36 = blockClass(340, 140)
    blockrow4 = [b28,b29,b30,b31,b32,b33,b34,b35,b36]
    
    #Block Row 5
    b37 = blockClass(20, 160)
    b38 = blockClass(60, 160)
    b39 = blockClass(100, 160)
    b40 = blockClass(140, 160)
    b41 = blockClass(180, 160)
    b42 = blockClass(220, 160)
    b43 = blockClass(260, 160)
    b44 = blockClass(300, 160)
    b45 = blockClass(340, 160)
    blockrow5 = [b37,b38,b39,b40,b41,b42,b43,b44,b45]
    
    #Block Row 6
    b46 = blockClass(20, 180)
    b47 = blockClass(60, 180)
    b48 = blockClass(100, 180)
    b49 = blockClass(140, 180)
    b50 = blockClass(180, 180)
    b51 = blockClass(220, 180)
    b52 = blockClass(260, 180)
    b53 = blockClass(300, 180)
    b54 = blockClass(340, 180)
    blockrow6 = [b46,b47,b48,b49,b50,b51,b52,b53,b54]
    
    everyBlock = [block_row1,blockrow2,blockrow3,blockrow4,blockrow5,blockrow6]


# Game Loop
while True:
    for event in pygame.event.get():
        # Allow the player to quit the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Refreshes the screen with light_black every frame        
    screen.fill(light_black)
    
    # If game_scene is "main menu" then the game will draw the title screen.
    if game_scene == "main menu":
        title_screen()
    
    if game_scene == "game":
        game_screen()
    
    # Updates the game
    pygame.display.flip()
    clock.tick(60)