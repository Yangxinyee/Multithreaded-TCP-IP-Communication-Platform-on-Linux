# 1.Import the library
import pgzrun
import random
# 2.initialize
# window size
WIDTH = 600
HEIGHT = 480
# Gluttonous Snake
bodys = [[100, 100], [80, 100], [60, 100], [40, 100], [20, 100]]
head = [100, 100]
d = 'right'
# food
food = [290, 290]
# score
score = 0
highscore = 0

# 3.Game window drawing
def draw():
    # Clear the screen
    screen.clear()
    # Draw Snake
    for body in bodys:
        rect = Rect(body, (20, 20))
        screen.draw.filled_rect(rect, (0, 0, 0))
        inner = [body[0] + 2, body[1] + 2]
        rect = Rect(inner, (15, 15), center='center')
        screen.draw.filled_rect(rect, (255, 255, 255))  # white
    # Draw head
    rect = Rect(head, (20, 20))
    screen.draw.filled_rect(rect, (0, 200, 0))
    inner = [head[0] + 2, head[1] + 2]
    rect = Rect(inner, (15, 15))
    screen.draw.filled_rect(rect, (0, 255, 12))
    # Color the food: red
    screen.draw.filled_circle(food, 10, '#ff0000')
    # Plot score
    screen.draw.text('score:' + str(score), (20, 20), color="red", fontsize=30)
    # Draw maximum score
    screen.draw.text('hightest_score:' + str(highscore), (20, 40), color="red", fontsize=30)


# 4.The snake's moving function
def run():
    global food, d, head, bodys, score, highscore
    # Add a grid to the body
    if d == 'right':
        head[0] += 20
    elif d == 'left':
        head[0] -= 20
    elif d == 'up':
        head[1] -= 20
    else:
        head[1] += 20
    bodys.insert(0, list(head))
    if head[0] == food[0] - 10 and head[1] == food[1] - 10:
        food = [random.randint(1, 30) * 20 - 10, random.randint(1, 20) * 20 - 10]
        score += 1
        if score > 5:
            clock.unschedule(run)
            clock.schedule_interval(run, 0.05)
    else:
        bodys.pop()
    # Hit the wall and start over
    if head[0] < 0 or head[0] > 580 or head[1] < 0 or head[1] > 480 or head in bodys[1:]:
        # The snake returns to its original position
        bodys = [[100, 100], [80, 100], [60, 100], [40, 100], [20, 100]]
        head = [100, 100]
        # Direction to the right
        d = 'right'
        # Record score
        if highscore <= score:
            highscore = score
        score = 0
        clock.unschedule(run)
        clock.schedule_interval(run, 0.15)


# The key controls the direction of the snake
def on_key_down(key):
    global d
    # change the direction
    if key == keys.DOWN and d != 'up':
        d = 'down'
    if key == keys.UP and d != 'down':
        d = 'up'
    if key == keys.LEFT and d != 'right':
        d = 'left'
    if key == keys.RIGHT and d != 'left':
        d = 'right'


# 6.Launch the game
# Timing setting
clock.schedule_interval(run, 0.15)
# Launch the game
pgzrun.go()
