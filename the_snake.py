"""Основной файл с данными и взаимодействиями."""


from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Общий материнский класс для змейки и яблока."""

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    body_color = BOARD_BACKGROUND_COLOR

    def __init__(self):
        """Инициализация класса."""
        pass

    def draw(self):
        """Общие принципы отрисовки игровых объектов."""
        pass


class Apple (GameObject):
    """Описывает яблоко."""

    position = (0, 0)  # координаты яблока на поле
    body_color = (255, 0, 0)  # цвет яблока

    def __init__(self, snake_positions=(0, 0)):
        """Инициализация класса."""
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Генерация случайной позиции."""
        while True:
            x = randint(0, (GRID_WIDTH - 1)) * GRID_SIZE
            y = randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
            new_position = (x, y)

            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake (GameObject):
    """Описывает действия змейки."""

    body_color = (0, 255, 0)  # цвет змейки

    def __init__(self):
        """Инициализация класса."""
        self.length = 1  # длина змейки
        self.positions = [self.position]  # координаты всех сегментов
        self.direction = RIGHT  # текущее направление движения
        self.next_direction = None  # следующее направление движения

    def move(self):
        """Описание движения змейки."""
        head_position = self.get_head_position()
        x, y = head_position
        x_dir, y_dir = self.direction
        x_new, y_new = x + (x_dir * GRID_SIZE), y + (y_dir * GRID_SIZE)

        # проход сквозь границы поля по сторонам:
        if x_new >= SCREEN_WIDTH or x_new < 0:
            x_new %= SCREEN_WIDTH

        if y_new >= SCREEN_HEIGHT or y_new < 0:
            y_new %= SCREEN_HEIGHT

        head_position_new = (x_new, y_new)

        self.positions.insert(0, head_position_new)
        # удаление последнего элемента списка positions:
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс игры после столкновения."""
        self.length = 1
        self.positions = [GameObject.position]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # возвращает первый элемент списка positions
    def get_head_position(self):
        """Позиция головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Задает новое направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def main():
    """Инициализация PyGame."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        # Описание основной логики игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake_head = snake.get_head_position()

        # Действие, если змея съела яблоко.
        if snake_head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.randomize_position(snake.positions)

        # Проверка самостолкновений:
        for unit in snake.positions[1:]:
            if unit == snake_head:
                snake.reset()
                apple.randomize_position(snake.positions)
                break

        # Обновление экрана:
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
