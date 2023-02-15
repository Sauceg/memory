# MARVIN UWALAKA 
# Memory is a game where a player tests their memory by trying to match two hidden images that are revealed once they are picked and close if they do not maatch

# imported functions 
import pygame
import random 
import time 
# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.
   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # surface game is played on 
      self.surface = surface
      self.bg_color = pygame.Color('black')
      self.FPS = 60                          #frame rate the game runs at. Frames per second(fps)
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects'
      self.game_Clock = pygame.time.Clock()
      self.board_size = 4  # set board size 
      self.score = 0 # set score to 0 
      self.matched_tiles  = []   # images that have been matched 
      self.image_list = []   # images to be displayed 
      self.load_images()  # call load images to 
      self.selected_tiles = []    # tiles that have been clicked in the game 
      self.board = [] # will be represented by a list of lists
      self.create_board() # call create board 
  
    # loads_images creates images and appends them to a list of images 
   def load_images(self):        # self is of type game
      # load the images from the files into the image list
      for i in range(1,self.board_size + self.board_size+ 1 ): 
         image = pygame.image.load('image'+str(i)+'.bmp') # you have to load 7 more 
         self.image_list.append(image)
      # afer loading all 8 images double the images so they can be 2 of each images to be matched together 
      self.image_list = self.image_list + self.image_list
      # shuffle the list so they appear in random positions on the board when every game starts 
      random.shuffle(self.image_list) 
   def create_board(self):
      i = 0  # set ounter to 0
      
      # position of image on the board
      for row_index in range(0,self.board_size):
         row = []
         for col_index in range(0,self.board_size):
            image = self.image_list[i]
            width = image.get_width() # image is a surface object so we can get the width and height
            height = image.get_height() 
            x = col_index * width   # multiplay width by row index to get the horizontal position of the tile 
            y = row_index * height  # multiplay height by col index to get the vertical  position of the tile
            tile = Tile(x,y,width,height,image,self.surface) # create tiles where the images would be places 
            row.append(tile)         # add tiles to row lists to make up each row of the board 
            i += 1
         self.board.append(row)      # add rows of the board 
         
         
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game: # if there is a click and he game is running call handle_mouse_up method 
            self.handle_mouse_up(event.pos)
            
   def handle_mouse_up(self,position):
      # position is bound to event.pos
      #position is the (x,y) location of the click
      for row in self.board:
         for tile in row:
            if tile.select(position) and tile.is_hidden(): # asking the tile have you been selected?
               tile.set_hidden(False)     # reveal the tile that has been clicked 
               self.selected_tiles.append(tile)  # append to tiles that have been clicked list 
      
      
   def draw(self):
      # Draw all game objects.
      # self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.draw_score()      # draw score 
      # draw the board
      for row in self.board: 
         for tile in row:
            tile.draw()
      pygame.display.update() # make the updated surface appear on the display
      
      
      
   def draw_score(self):
      #  self is the Game this is drawn in 
      font= pygame.font.SysFont('',90)                                    # text size 
      test_image = font.render(str(self.score),True, pygame.Color('white'), self.bg_color) # text and the text color 
      location = (self.surface.get_width() - test_image.get_width() ,0)   # where txt is to be drawn 
      self.surface.blit(test_image,location)                              # blits the text to surface and intended location  
      
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      
      if self.continue_game == True:
         self.score = pygame.time.get_ticks()//1000 # the score of the game is he amount of seconds the player take to finish the game  
      if len(self.selected_tiles) == 2:   # when the number of clicked tiles is 2 check if they match 
         if not self.selected_tiles[0].equal(self.selected_tiles[1]): # if they dont match close them 
            time.sleep(.5)
            self.selected_tiles[0].set_hidden(True)    
            self.selected_tiles[1].set_hidden(True) 
            
         else: # if they do match leave them open and add them to the matched images list 
            self.matched_tiles .append(self.selected_tiles[0])
            self.matched_tiles .append(self.selected_tiles[1])
         self.selected_tiles = []    # empty the list of clicked tiles 
            
      
      
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      
      for tiles in self.matched_tiles :
         if len(self.matched_tiles) == len(self.image_list): # if tiles that are open are equal to the number of tiles on the board then the game ends 
            self.continue_game = False
            

class Tile:
   def __init__(self,x,y,width,height,image,surface): 
      self.rect = pygame.Rect(x,y,width,height)
      self.boarder_color = pygame.Color('black') # colour of the boarder 
      self.border_width = 3  # width of boarder 
      self.hidden_image = pygame.image.load('image0.bmp')
      self.hidden = True
      self.revealed_image = image
      self.surface = surface
   
   def equal(self,other_tile):  # checks if one image is equal to another return true of false 
                                # other tile is of type Tile 
      if self.revealed_image == other_tile.revealed_image:
         return True
      else:
         return False
      
   def select(self,position):   # selects a tile by checking if its been clicked 
      # position is the (x,y) of the location of the click
      selected = False
      if self.rect.collidepoint(position): # is there a click in that tile?
         selected = True
      return selected  
   
   # Assigns self.hidden to a value, usually True or Flase
   def set_hidden(self, value):
      self.hidden = value
      
   # checks if the tile is open 
   def is_hidden(self): # self is of type Tile 
      return self.hidden
   
   # draw hidden or revealed image depending on if the imgage is hidden
   def draw(self):
      location = (self.rect.x, self.rect.y) 
      if self.hidden:  # if self.hidden is true draw hidden image 
         self.surface.blit(self.hidden_image,location) 
      else: # else draw revealed image 
         self.surface.blit(self.revealed_image, location)
      pygame.draw.rect(self.surface,self.boarder_color ,self.rect, self.border_width)
      #self.draw_content()
      
      # draws tiles in the right position 
   def draw_content(self):
      font = pygame.font.SysFont('',133) # height of the surface is 400 //3 = 133
      text_box = font.render(self.hidden_image,True,self.boarder_color )
      # text_box is a pygame.Surface object - get the rectangle from the surface
      rect1 = text_box.get_rect()
      #rect1  <---->  self.rect
      rect1.center = self.rect.center
      location = (rect1.x,rect1.y)
      self.surface.blit(text_box,location)


main()
