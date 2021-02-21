import pygame, sys, math

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
running = True
cookie_per_second = 0
score = 0
coeff = 1
clock = pygame.time.Clock()
tick = 1
MYEVENTTYPE = pygame.USEREVENT + 1
names = {0: 'Курсор', 1: 'Бабушка', 2: 'Ферма', 3: 'Шахта', 4: 'Фабрика', 5: 'Банк',
         6: 'Храм', 7: 'Башня мага', 8: 'Ракета', 9: 'Лаборатория', 10: 'Портал', 11: 'Машина времени'}
price = {0: 15, 1: 100, 2: 1100, 3: 12000, 4: 130000, 5: 1400000,
         6: 20000000, 7: 330000000, 8: 5100000000, 9: 75000000000,
         10: 100000000000, 11: 1400000000000}


class Board:
    # создание поля
    def __init__(self, width, height, left=10, right=10, cell_size=10):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left
        self.top = right
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                                 x * self.cell_size + self.left, y * self.cell_size + self.top,
                                 self.cell_size, self.cell_size), 1)
                font = pygame.font.Font(None, 30)
                text = font.render(f'{self.board[y][0]}', True, (100, 255, 100))
                screen.blit(text, (960, y * self.cell_size + 15))
                text_name = font.render(f'{names[y]}', True, (100, 255, 100))
                screen.blit(text_name, (750, y * self.cell_size + 15))
                font = pygame.font.Font(None, 20)
                price_n = font.render(f'{price[y]}', True, (100, 255, 100))
                screen.blit(price_n, (650, y * self.cell_size + 15))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def checker(self, num):
        global coeff, cookie_per_second
        if num == 1:
            cookie_per_second += 1
        elif num == 2:
            cookie_per_second += 8
        elif num == 3:
            cookie_per_second += 47
        elif num == 4:
            cookie_per_second += 260
        elif num == 5:
            cookie_per_second += 1400
        elif num == 6:
            cookie_per_second += 7800
        elif num == 7:
            cookie_per_second += 44000
        elif num == 8:
            cookie_per_second += 260000
        elif num == 9:
            cookie_per_second += 1600000
        elif num == 10:
            cookie_per_second += 10000000
        elif num == 11:
            cookie_per_second += 65000000
        elif num == 0:
            coeff += 1

    def on_click(self, cell):
        global score
        if cell:
            if price[cell[1]] <= score:
                self.checker(cell[1])
                score -= price[cell[1]]
                price[cell[1]] *= 1.1
                price[cell[1]] = int(price[cell[1]])
                self.board[cell[1]][0] += 1

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)
        else:
            self.on_click(None)


board = Board(1, 12)
board.set_view(950, 0, 50)


def cookie():
    pygame.draw.circle(screen, pygame.Color(65, 25, 0), (200, 300), 100)


def get_cell(mouse_pos):
    cell_x = mouse_pos[0]
    cell_y = mouse_pos[1]
    if cell_x < 0 or cell_x >= width or cell_y < 0 or cell_y >= height:
        return None
    return cell_x, cell_y


def on_click():
    global score
    score += coeff


def on_circle(cell):
    x = cell[0]
    y = cell[1]
    sqx = (x - 200) ** 2
    sqy = (y - 300) ** 2
    if math.sqrt(sqx + sqy) < 100:
        return True


def scoring():
    font = pygame.font.Font(None, 50)
    text = font.render(f'Score:{score}', True, (100, 255, 100))
    screen.blit(text, (20, 20))


def get_click(mouse_pos):
    cell = get_cell(mouse_pos)
    if on_circle(cell):
        on_click()

pygame.time.set_timer(MYEVENTTYPE, 1000)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            get_click(event.pos)
            board.get_click(event.pos)
        if event.type == MYEVENTTYPE:
            score += cookie_per_second
    screen.fill(pygame.Color(77, 113, 152))
    board.render()
    cookie()
    scoring()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()