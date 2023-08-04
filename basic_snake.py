# 1.导入库
import pgzrun
import random
# 2.初始化
# 窗口大小
WIDTH = 600
HEIGHT = 480
# 贪吃蛇
bodys = [[100, 100], [80, 100], [60, 100], [40, 100], [20, 100]]
head = [100, 100]
d = 'right'
# 食物
food = [290, 290]
# 得分
score = 0
highscore = 0

# 3.游戏窗口绘制
def draw():
    # 清空屏幕
    screen.clear()
    # 绘制蛇
    for body in bodys:
        rect = Rect(body, (20, 20))
        screen.draw.filled_rect(rect, (0, 0, 0))
        inner = [body[0] + 2, body[1] + 2]
        rect = Rect(inner, (15, 15), center='center')
        screen.draw.filled_rect(rect, (255, 255, 255))  # 白色
    # 绘制头
    rect = Rect(head, (20, 20))
    screen.draw.filled_rect(rect, (0, 200, 0))
    inner = [head[0] + 2, head[1] + 2]
    rect = Rect(inner, (15, 15))
    screen.draw.filled_rect(rect, (0, 255, 12))
    # 绘制食物 颜色为红色
    screen.draw.filled_circle(food, 10, '#ff0000')
    # 绘制得分
    screen.draw.text('score:' + str(score), (20, 20), color="red", fontsize=30)
    # 绘制最高分
    screen.draw.text('hightest_score:' + str(highscore), (20, 40), color="red", fontsize=30)


# 4.蛇的移动功能
def run():
    global food, d, head, bodys, score, highscore
    # 新增一个格子的身体
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
    # 撞墙后重新开始
    if head[0] < 0 or head[0] > 580 or head[1] < 0 or head[1] > 480 or head in bodys[1:]:
        # 蛇回到初始位置
        bodys = [[100, 100], [80, 100], [60, 100], [40, 100], [20, 100]]
        head = [100, 100]
        # 方向向右
        d = 'right'
        # 记录得分
        if highscore <= score:
            highscore = score
        score = 0
        clock.unschedule(run)
        clock.schedule_interval(run, 0.15)


# 按键控制蛇的行走方向
def on_key_down(key):
    global d
    # 改变方向
    if key == keys.DOWN and d != 'up':
        d = 'down'
    if key == keys.UP and d != 'down':
        d = 'up'
    if key == keys.LEFT and d != 'right':
        d = 'left'
    if key == keys.RIGHT and d != 'left':
        d = 'right'


# 6.启动游戏
# 定时设置
clock.schedule_interval(run, 0.15)
# 启动游戏
pgzrun.go()