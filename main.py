import pygame
from random import randint

Vector2 = pygame.math.Vector2

parameters = {
  'frames_by_second' : 4,
  'window_size' : Vector2(640, 360),
  'background_color' : (0, 100, 0),
  'background_color2' : (0, 120, 0),
  'element_color' : (0, 65, 0),
  'element_size' : 20,
  'initial_coords' : Vector2(300, 180),
  'initial_direction' : Vector2(1, 0),
  'initial_element_count' : 2,
}

frame_time = round(1000/parameters['frames_by_second']) if parameters['frames_by_second'] else 70

class Snake:
  def __init__(self, color, size, coords, direction, elements_count):
    self.score = 0
    self.color = color
    self.size = size
    self.coords = coords
    self.direction = direction
    self.velocity = size*2
    self.elements = {}
    for i in range(elements_count):
      self.elements[i] = {'coords' : coords - (i+1)*Vector2(size*2, 0)}
    self.generate_bounty()

  def generate_bounty(self):
    x_size = (parameters['window_size'].x-2*parameters['element_size'])/(2*parameters['element_size'])
    y_size = (parameters['window_size'].y-2*parameters['element_size'])/(2*parameters['element_size'])
    
    bounty = 2*parameters['element_size']*Vector2(randint(1, x_size), randint(1, y_size))+parameters['element_size']*Vector2(1, 1)

    if not self.is_snake_in_coords(bounty):
      self.bounty = {'coords' : bounty}
    else:
      self.generate_bounty()

  def is_snake_in_coords(self, coords):
    if self.coords == coords:
      return True
    for i in self.elements:
      element = self.elements[i]
      if i != len(self.elements)-1 and element['coords'] == coords:
        return True
    return False

  def display(self):
    pygame.draw.circle(win, self.color, self.coords, self.size)
    for i in self.elements:
      element = self.elements[i]
      pygame.draw.circle(win, self.color, element['coords'], self.size)
    pygame.draw.circle(win, self.color, self.bounty['coords'], self.size/2)
  
  def set_direction(self, direction):
    self.direction = direction

  def set_direction_with_game_rules(self, direction):
    if -1*self.direction != direction:
      self.direction = direction

  def can_take_direction(self, direction):
    if -1*self.direction != direction:
      return True
    else:
      return False

  def get_direction(self, direction):
    return self.direction

  def moove(self):
    if self.is_next_moove_in_window() and not self.is_snake_in_coords(self.coords + self.direction*self.velocity):
      self.back_element_last_coords = (self.elements[len(self.elements)-1])['coords']
      for i in reversed(range(1, len(self.elements))):
        (self.elements[i])['coords'] = (self.elements[i-1])['coords']
      (self.elements[0])['coords'] = self.coords
      self.coords = self.coords + self.direction*self.velocity

  def add_element_in_back(self):
    self.elements[len(self.elements)] = {'coords' : self.back_element_last_coords}

  def check_for_bounty(self):
    if self.is_snake_in_coords(self.bounty['coords']):
      self.add_element_in_back()
      self.generate_bounty()
      self.score += 1
  
  def is_next_moove_in_window(self):
    next_coords = self.coords + self.direction*self.velocity
    if next_coords.x > 0 and next_coords.x < parameters['window_size'].x and next_coords.y > 0 and next_coords.y < parameters['window_size'].y:
      return True
    else:
      return False

pygame.init()

win = pygame.display.set_mode(parameters['window_size']+Vector2(0, 20))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 24)
run = True

snake = Snake(parameters['element_color'], parameters['element_size'], parameters['initial_coords'], parameters['initial_direction'], parameters['initial_element_count'])

def drawGame():
  win.fill((0, 0, 0))
  pygame.draw.rect(win, parameters['background_color'], (0, 0, (parameters['window_size']).x, (parameters['window_size']).y))
  pygame.draw.rect(win, parameters['background_color2'], (0, (parameters['window_size']).y, (parameters['window_size']).x, (parameters['window_size']).y+20))

  snake.display()
  img = font.render('score: ' + str(snake.score), True, parameters['element_color'])
  win.blit(img, (((parameters['window_size']).x/2)-20, (parameters['window_size']).y+3))
  pygame.display.update()


while run:
  pygame.time.delay(frame_time)

  last_key = None
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT and snake.can_take_direction(Vector2(-1, 0)):
        last_key = pygame.K_LEFT
    
      if event.key == pygame.K_RIGHT and snake.can_take_direction(Vector2(1, 0)):
        last_key = pygame.K_RIGHT
      
      if event.key == pygame.K_UP and snake.can_take_direction(Vector2(0, -1)):
        last_key = pygame.K_UP
      
      if event.key == pygame.K_DOWN and snake.can_take_direction(Vector2(0, 1)):
        last_key = pygame.K_DOWN

  if last_key != None:
    if last_key == pygame.K_LEFT:
      snake.set_direction_with_game_rules(Vector2(-1, 0))
  
    if last_key == pygame.K_RIGHT:
      snake.set_direction_with_game_rules(Vector2(1, 0))
    
    if last_key == pygame.K_UP:
      snake.set_direction_with_game_rules(Vector2(0, -1))
    
    if last_key == pygame.K_DOWN:
      snake.set_direction_with_game_rules(Vector2(0, 1))


  snake.moove()
  snake.check_for_bounty()
  drawGame()
          
pygame.quit()
