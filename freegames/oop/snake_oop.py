"""Snake, classic arcade game.

Exercises

1. How do you make the SnakeFast or SnakeSlow classes?
2. How do you make a SnakeSmart, that change the direction when collide with edges?
3. How would you make a new food types? When snake eat them it will more fast or decrease?
4. How do you create a Actor that will be the Head and Food superclass?
"""

from turtle import setup, hideturtle, tracer, listen, onkey, done, update, clear, ontimer
from random import randrange, choice
from freegames import square, vector

# 4. How do you create a Actor that will be the Head and Food superclass?
class Actor:
    def __init__(self, x, y):
        self.position = vector(x, y)

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

class Head(Actor):
    pass

class Food(Actor):
    color = 'Blue'
    cal = 5

#3. How would you make a new food types? When snake eat will more fast or decrease?
class Apple(Food):
    color = 'Green'
    cal = 10

class Mouse(Food):
    color = 'Brown'
    cal = 15

class BadFood(Food):
    color = 'Red'
    cal = -5

class Snake:
    SPEED = 1
    def __init__(self, x=0, y=0):
        self.head = Head(x, y)
        self.body = [vector(10, 0)]
        self.aim = vector(0*self.SPEED, -10*self.SPEED)

        self.status = 'LIVE'

    def eat(self, food):
        print('snake is eating', food.cal)
        for x in range(food.cal):
            self.body.append(self.head.position)

        for x in range(food.cal, 0):
            del self.body[0]

    def change(self, x, y):
        "Change snake direction."
        print('snake is changing')
        self.aim.x = x*self.SPEED
        self.aim.y = y*self.SPEED

    def move(self):
        "Move snake forward one segment."
        self.head = Head(*self.body[-1].copy())
        self.head.position.move(self.aim)

        if self.is_colliding_with_border():
            self.on_collision_with_border()
        elif self.is_eating_himself():
            self.on_eating_himself()
        else:
            self.body.append(self.head.position)
            self.body.pop(0) # cut the tail

    def on_collision_with_border(self):
        self.dead()

    def on_eating_himself(self):
        self.dead()

    def is_eating_himself(self):
        print(self.head.position, self.body)
        return (self.head.position in self.body)

    def dead(self):
        self.status = 'DEAD'

    def alive(self):
        return self.status != 'DEAD'

    def is_colliding_with_border(self):
       return not(-200 < self.head.x < 190 and -200 < self.head.y < 190)

# 1. How do you make the SnakeFast or SnakeSlow classes?
class SnakeFast(Snake):
    SPEED = 2

class SnakeSlow(Snake):
    SPEED = 0.5

#2. How do you make a SnakeSmart, that change the direction when collide with edges?
class SnakeSmart(Snake):
    def on_collision_with_border(self):
        self.change(10, 0)

class GameSnake:
    def __init__(self):
        self.food = self.new_food()
        self.snake = Snake()

        onkey(lambda: self.snake.change(10, 0), 'Right')
        onkey(lambda: self.snake.change(-10, 0), 'Left')
        onkey(lambda: self.snake.change(0, 10), 'Up')
        onkey(lambda: self.snake.change(0, -10), 'Down')

    def new_food(self):
        foods = [Food,
                Apple,
                Mouse,
                BadFood,
                ]
        type_food = choice(foods)
        food = type_food(0, 0)
        food.position = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
        return food

    def run(self):
        clear()
        for body in self.snake.body:
            square(body.x, body.y, 9, 'black')
        square(self.food.x, self.food.y, 9, self.food.color)
        update()

        self.snake.move()

        if self.snake.head.position == self.food.position:
            self.snake.eat(self.food)
            self.food = self.new_food()

        if self.snake.alive():
            ontimer(self.run, 100)
        else:
            print('>>> SNAKE IS DEAD <<<')
            square(self.snake.head.x, self.snake.head.y, 9, 'red')
            return

def init():
    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    listen()
    game = GameSnake()
    game.run()
    done()

if __name__ == '__main__':
    init()
