'''
Version trying to add menu and bottons to control the programme

'''
import pygame
from queue import PriorityQueue
from tkinter import *
from tkinter import ttk
import random
import threading


# 实例化object，建立窗口window
root = Tk()
# 给窗口的可视化起名字

#root.maxsize(900, 900)
root.config(bg="black")

root.title("Path Finding Algorithm")

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
selected_mode = StringVar()

pygame.init()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

        self.f = float("inf")

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def set_f_value(self, f_value):
        self.f = f_value

    def updata_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    # this is very important for PriorityQueue to judge which one is the smaller one!!!!
    def __lt__(self, other):
        return self.f <= other.f


def h(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put(start)
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) + g_score[start]

    open_set_hash = {start}  # check things in open_set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()
        current.set_f = f_score[current]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                f_value = f_score[neighbor]
                neighbor.set_f_value(f_value)

                if neighbor not in open_set_hash:
                    open_set.put(neighbor)
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main():
    width = width_setter.get()
    ROWS = row_setter.get()
    grid = make_grid(ROWS, width)
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Path Finding Algorithm")

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = None

                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updata_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


#main(screen, WIDTH)



def thread_it(func, *args):  # 卡死主要是因为这里给他改成多线程处理就可以啦！！！
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()




def Generate():
    global data
    print("Algo Selected: ")

    data = []



# frame / base layout

# UI : User interface design 用户界面设计
# frame : 框架
#  grid有两个最为重要的参数，用来指定将组件放置到什么位置，一个是row,另一个是column。如果不指定row,会将组件放置到第一个可用的行上，如果不指定column，则使用第一列。
UI_frame = Frame(root, width=900, height=900, bg='white')
UI_frame.grid(row=0, column=0)


# User Interface Area
# Row[0]
'''
签控件（Label）指定的窗口中显示的文本和图像。 
部分参数介绍：
anchor
文本或图像在背景内容区的位置，默认为 center，可选值为（n,s,w,e,ne,nw,sw,se,center）eswn 是东南西北英文的首字母，表示：上北下南左西右东

bg
标签背景颜色

bd
标签的大小，默认为 2 个像素

padx
x 轴间距，以像素计，默认 1。


pady
y 轴间距，以像素计，默认 1。


text
设置文本，可以包含换行符(\n)。

'''
Label(UI_frame, text="Algorithm: ", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=W)
# Tkinter 下拉列表-combobox 是用户可用来选择的下拉列表。它是 Entry 和 drop-down 控件的组合。
# The advantage to using a StringVar comes when you want to either
# a) have two widgets share the same variable so that one is updated when the other is changed
# b) attach one or more traces to the StringVar
algMenu = ttk.Combobox(UI_frame, textvariable=selected_mode,
                       values=["A* path finding"])

algMenu.grid(row=0, column=1, padx=5, pady=5)
algMenu.current(0)

'''
Scale控件允许用户通过移动滑动条来选择数值。你可以设置最小值和最大值，滚动的滑条取值在最大值和最小值之间。
digits
如果用于控制比例数据的控制变量是字符串类型，则此选项用于指定将数字比例转换为字符串时的位数。
resolution
设置为对刻度值进行的最小变化。
https://www.py.cn/manual/python-tkinter-scale.html
'''


'''
按钮组件用于在 Python 应用程序中添加按钮，按钮上可以放上文本或图像，按钮可用于监听用户行为，能够与一个 Python 函数关联，当按钮被按下时，自动调用该函数。
https://www.runoob.com/python/python-tk-button.html
'''
Button(UI_frame, text="Start", command=lambda: thread_it(main()), bg="red").grid(row=0, column=2, padx=5,
                                                                                         pady=5)

# Row[1]
'''
Entry 文本框用来让用户输入一行文本字符串。
https://www.runoob.com/python/python-tkinter-entry.html
'''
width_setter = Scale(UI_frame, from_=500, to=2000, resolution=50, orient=HORIZONTAL, label="Width")
width_setter.grid(row=1, column=1, padx=5, pady=5, sticky=W)

row_setter = Scale(UI_frame, from_=10, to=100, resolution=5, orient=HORIZONTAL, label="Rows")
row_setter.grid(row=1, column=2, padx=5, pady=5, sticky=W)


# 主窗口循环显示
root.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，
# 如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，
# mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。

