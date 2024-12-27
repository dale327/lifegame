from tkinter import ttk
import tkinter as tk
import random
from shapes import shapes


class Game:
    def __init__(self, width=50, height=50, cell_size=10, speed=100):
        self.btn_dechalton = None
        self.btn_pulsar = None
        self.btn_beacon = None
        self.btn_toad = None
        self.btn_blinker = None
        self.frame_oscillators = None
        self.btn_tub = None
        self.btn_boat = None
        self.btn_loaf = None
        self.btn_beehive = None
        self.btn_cell = None
        self.btn_gosper_glider_gun = None
        self.btn_block = None
        self.frame_stable = None
        self.btn_hwss = None
        self.btn_mwss = None
        self.frame_guns = None
        self.btn_lwss = None
        self.btn_glider = None
        self.frame_planers = None
        self.notebook = None
        self.label_info = None
        self.scale = None
        self.btn4 = None
        self.frame_btns = None
        self.btn3 = None
        self.btn2 = None
        self.btn = None
        self.canvas = None
        self.frame_board = None
        self.window = None
        self.mode = 'Cell'
        self.speed = speed
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.alive_n = 0
        self.dead_n = 0
        self.generation = 0
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.running = False
        self.init_window()
        self.randomize_board()
        self.window.mainloop()

    # Функция для создания окна
    def init_window(self):
        self.window = tk.Tk()
        self.window.title('Игра "Жизнь"')
        self.window.geometry(f'{self.width * self.cell_size + 300}x{self.height * self.cell_size + 200}+200+200')
        self.window.resizable(False, False)

        self.frame_board = tk.Frame(self.window, width=self.width * self.cell_size,
                                    height=self.height * self.cell_size, bg='#FFE5B4')
        self.frame_board.place(x=10, y=10)

        self.canvas = tk.Canvas(self.frame_board, bg='black', width=self.width * self.cell_size,
                                height=self.height * self.cell_size)
        self.canvas.bind('<Button-1>', self.toggle_cell)
        self.canvas.place(x=0, y=0)
        self.update_canvas()

        self.frame_btns = tk.Frame(self.window, width=self.width * self.cell_size, height=170, bg='gray')
        self.frame_btns.place(x=10, y=20 + self.height * self.cell_size)

        self.btn = tk.Button(self.frame_btns, text='REGENERATE', font='System 16', command=self.randomize_board)
        self.btn.place(x=10, y=130)

        self.btn2 = tk.Button(self.frame_btns, text='START', font='System 16', command=self.start_simulation)
        self.btn2.place(x=10, y=10)

        self.btn3 = tk.Button(self.frame_btns, text='STOP', font='System 16', command=self.stop)
        self.btn3.place(x=10, y=70)

        self.btn4 = tk.Button(self.frame_btns, text='CLEAR', font='System 16', command=self.clear)
        self.btn4.place(x=420, y=10)

        self.scale = tk.Scale(self.frame_btns, length=200, from_=10, to=1000, orient=tk.HORIZONTAL,
                              command=self.update_speed, label='SPEED (ms)', font='System 18')
        self.scale.set(self.speed)
        self.scale.place(x=285, y=60)

        self.label_info = tk.Label(self.window,
                                   text=f'ALIVE: {self.alive_n}\nDEAD: {self.dead_n}\nGENERATION: {self.generation}\n'
                                        f'MODE: {self.mode}',
                                   font='System 18')
        self.label_info.place(x=540, y=550)

        self.notebook = ttk.Notebook(self.window, width=270, height=400)
        self.notebook.place(x=520, y=10)

        self.frame_planers = tk.Frame(self.notebook)
        self.frame_planers.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_planers, text='Planers')

        self.btn_glider = ttk.Button(self.frame_planers, text='Glider', command=lambda: self.change_mode('Glider'))
        self.btn_glider.pack()

        self.btn_lwss = ttk.Button(self.frame_planers, text='LWSS', command=lambda: self.change_mode('LWSS'))
        self.btn_lwss.pack()

        self.btn_mwss = ttk.Button(self.frame_planers, text='MWSS', command=lambda: self.change_mode('MWSS'))
        self.btn_mwss.pack()

        self.btn_hwss = ttk.Button(self.frame_planers, text='HWSS', command=lambda: self.change_mode('HWSS'))
        self.btn_hwss.pack()

        self.frame_guns = ttk.Frame(self.notebook)
        self.frame_guns.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_guns, text='Guns')

        self.btn_gosper_glider_gun = ttk.Button(self.frame_guns, text='Gosper glider gun',
                                                command=lambda: self.change_mode('GGG'))
        self.btn_gosper_glider_gun.pack()

        self.frame_stable = tk.Frame(self.notebook)
        self.frame_stable.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_stable, text='Still lifes')

        self.btn_cell = ttk.Button(self.frame_stable, text='Cell', command=lambda: self.change_mode('Cell'))
        self.btn_cell.pack()

        self.btn_block = ttk.Button(self.frame_stable, text='Block', command=lambda: self.change_mode('Block'))
        self.btn_block.pack()

        self.btn_beehive = ttk.Button(self.frame_stable, text='Beehive', command=lambda: self.change_mode('Beehive'))
        self.btn_beehive.pack()

        self.btn_loaf = ttk.Button(self.frame_stable, text='Loaf', command=lambda: self.change_mode('Loaf'))
        self.btn_loaf.pack()

        self.btn_boat = ttk.Button(self.frame_stable, text='Boat', command=lambda: self.change_mode('Boat'))
        self.btn_boat.pack()

        self.btn_tub = ttk.Button(self.frame_stable, text='Tub', command=lambda: self.change_mode('Tub'))
        self.btn_tub.pack()

        self.frame_oscillators = tk.Frame(self.notebook)
        self.frame_oscillators.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_oscillators, text='Oscillators')

        self.btn_blinker = ttk.Button(self.frame_oscillators, text='Blinker',
                                      command=lambda: self.change_mode('Blinker'))
        self.btn_blinker.pack()

        self.btn_toad = ttk.Button(self.frame_oscillators, text='Toad',
                                   command=lambda: self.change_mode('Toad'))
        self.btn_toad.pack()

        self.btn_beacon = ttk.Button(self.frame_oscillators, text='Beacon',
                                     command=lambda: self.change_mode('Beacon'))
        self.btn_beacon.pack()

        self.btn_pulsar = ttk.Button(self.frame_oscillators, text='Pulsar',
                                     command=lambda: self.change_mode('Pulsar'))
        self.btn_pulsar.pack()

        self.btn_dechalton = ttk.Button(self.frame_oscillators, text='Penta-decathlon',
                                        command=lambda: self.change_mode('Decathlon'))
        self.btn_dechalton.pack()

    # Функция для подсчета живых клеток
    def calculate_alives(self):
        result = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                result += self.board[y][x]
        return result

    def change_mode(self, new_mode):
        self.mode = new_mode
        self.update_info()

    def update_info(self):
        self.label_info.config(
            text=f'ALIVE: {self.alive_n}\nDEAD: {self.dead_n}\nGENERATION: {self.generation}\nMODE: {self.mode}')

    # Функция отрисовки поколения
    def update_canvas(self):
        self.canvas.delete('all')
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    self.canvas.create_rectangle(self.cell_size * j, self.cell_size * i,
                                                 self.cell_size * j + self.cell_size,
                                                 self.cell_size * i + self.cell_size, fill='white', outline='gray')

    # Функция для нажатия на одну клетку
    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if self.mode == 'Cell':
            self.board[y][x] = 1 - self.board[y][x]
        else:
            shape = shapes[self.mode]
            for dy in range(len(shape)):
                for dx in range(len(shape[dy])):
                    new_x, new_y = x + dx, y + dy
                    self.board[new_y % self.height][new_x % self.width] = shape[dy][dx]
        self.update_canvas()

    # Функция для генерации случайного поколения
    def randomize_board(self):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = random.randint(0, 1)
        self.update_canvas()

    # Функции для начала симуляции
    def simulate(self):
        if self.running:
            self.next_generation()
            self.window.after(self.speed, self.simulate)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.simulate()

    def stop(self):
        self.running = False

    def count_neighbour(self, x, y):
        result = 0
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for dx, dy in directions:
            nx, ny = (x + dx) % self.width, (y + dy) % self.height
            result += self.board[ny][nx]
        return result

    def next_generation(self):
        new_board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                count = self.count_neighbour(x, y)
                if self.board[y][x] == 1:
                    if 2 <= count <= 3:
                        new_board[y][x] = 1
                    else:
                        new_board[y][x] = 0

                else:
                    if count == 3:
                        new_board[y][x] = 1

                    else:
                        new_board[y][x] = 0
        self.board = new_board
        self.alive_n = self.calculate_alives()
        self.dead_n = self.width * self.height - self.alive_n
        self.generation += 1
        self.update_info()
        self.update_canvas()

    def clear(self):
        self.canvas.delete('all')
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = 0
        self.generation = 0
        self.alive_n = 0
        self.dead_n = 0
        self.update_info()
        self.update_canvas()

    def update_speed(self, value):
        self.speed = round(float(value))


Game()
