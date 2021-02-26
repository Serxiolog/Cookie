import pygame, sys, math, os, random

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
running = False
cookie_per_second = 0
score = 0
coeff = 1
clock = pygame.time.Clock()
tick = 1
COOKIE = pygame.USEREVENT + 1
GAME = pygame.USEREVENT + 2
LEAVE = pygame.USEREVENT + 3
DROP = pygame.USEREVENT + 4
dropped = []
delld = []
pause = True
names = {0: 'Курсор', 1: 'Бабушка', 2: 'Ферма', 3: 'Шахта', 4: 'Фабрика', 5: 'Банк',
         6: 'Храм', 7: 'Башня мага', 8: 'Ракета', 9: 'Лаборатория', 10: 'Портал'}
price = {0: 15, 1: 100, 2: 1100, 3: 12000, 4: 130000, 5: 1400000,
         6: 20000000, 7: 330000000, 8: 5100000000, 9: 75000000000,
         10: 100000000000}
menu_buttons = {0: 'Играть', 1: 'Результаты', 2: 'Выход'}


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
                text_name = font.render(f'{names[y]}', True, (100, 255, 100))
                screen.blit(text_name, (820, y * self.cell_size + 15))
                font_num = pygame.font.SysFont('Papyrus', 20)
                text = font_num.render(f'{self.board[y][0]}', True, (100, 255, 100))
                screen.blit(text, (960, y * self.cell_size + 15))
                font_price = pygame.font.SysFont('Ink Free', 20)
                price_n = font_price.render(f'{price[y]}', True, (100, 255, 100))
                screen.blit(price_n, (600, y * self.cell_size + 15))

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

    def menu_on_click(self, cell):
        if cell:
            self.menu_checker(cell[1])

    def menu_get_click(self, mouse_pos):
        cell = self.menu_get_cell(mouse_pos)
        if cell is not None:
            self.menu_on_click(cell)
        else:
            self.menu_on_click(None)

    def menu_render(self):
        for y in range(self.height):
            for x in range(self.width):
                '''pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * (self.cell_size // 2) + self.top,
                    self.cell_size, self.cell_size // 2), 1)'''
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text_name = font.render(f'{menu_buttons[y]}', True, (100, 255, 100))
                screen.blit(text_name, (430, y * (self.cell_size // 2) + 80))

    def menu_get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // (self.cell_size // 2)
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def menu_checker(self, num):
        if num == 0:
            pygame.time.set_timer(GAME, 1)
        elif num == 1:
            pass
        elif num == 2:
            pygame.time.set_timer(LEAVE, 1)


board = Board(1, 11)
board.set_view(950, 0, 55)
menu_board = Board(1, 3)
menu_board.set_view(400, 50, 250)


def cookie():
    screen.blit(image_cookie, (95, 195))


def get_cell(mouse_pos):
    cell_x = mouse_pos[0]
    cell_y = mouse_pos[1]
    if cell_x < 0 or cell_x >= width or cell_y < 0 or cell_y >= height:
        return None
    return cell_x, cell_y


def on_click(): ####!11!!
    global score
    score += coeff
    if len(dropped) < 5:
        pygame.time.set_timer(DROP, 1, 1)


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


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('bad')
    else:
        image = pygame.image.load(fullname)
        return image


def drop_cookie():
    x = random.randint(0, 950)
    dropped.append([x, 0])


def dropped_cookie(x, y):
    screen.blit(image_mini_cookie, (x, y))
    y += 10
    if y >= 600:
        return None
    return y


def print_image():
    screen.blit(image_cursor, (750, 0))
    screen.blit(image_grandma, (750, 60))
    screen.blit(image_farm, (750, 100))
    screen.blit(image_mine, (750, 160))
    screen.blit(image_factory, (750, 210))
    screen.blit(image_bank, (750, 270))
    screen.blit(image_temple, (750, 310))
    screen.blit(image_wizard, (750, 360))
    screen.blit(image_shipment, (750, 420))
    screen.blit(image_lab, (750, 480))
    screen.blit(image_portal, (750, 540))


image_bank = load_image('bank.png')
image_cursor = load_image('cursor.png')
image_factory = load_image('factory.png')
image_farm = load_image('farm.png')
image_grandma = load_image('grandma.png')
image_lab = load_image('lab.png')
image_mine = load_image('mine.png')
image_portal = load_image('portal.png')
image_shipment = load_image('shipment.png')
image_temple = load_image('temple.png')
image_wizard = load_image('wizard.png')
image_background = load_image('background.png')
image_cookie = load_image('cookie.png')
image_mini_cookie = load_image('mini_cookie.png')

pygame.time.set_timer(COOKIE, 1000)
while pause:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pause = False
            if event.type == pygame.MOUSEBUTTONUP:
                get_click(event.pos)
                board.get_click(event.pos)
            if event.type == COOKIE:
                score += cookie_per_second
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    running = False
            if event.type == DROP:
                drop_cookie()
        screen.blit(image_background, (0, 0))
        for i in range(len(dropped)):
            if i > 5:
                break
            y = dropped_cookie(dropped[i][0], dropped[i][1])
            if y:
                dropped[i] = [dropped[i][0], y]
            else:
                delld.append(i)
        delld = sorted(delld, reverse=True)
        for i in delld:
            if len(dropped) > 0:
                del dropped[0]
            else:
                delld = []
        print_image()
        board.render()
        cookie()
        scoring()
        pygame.display.flip()
        clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pause = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                running = True
        if event.type == pygame.MOUSEBUTTONUP:
            menu_board.menu_get_click(event.pos)
        if event.type == GAME:
            running = True
            pygame.time.set_timer(GAME, 0)
        if event.type == LEAVE:
            pause = False
    screen.fill(pygame.Color('Black'))
    menu_board.menu_render()
    pygame.display.flip()
pygame.quit()