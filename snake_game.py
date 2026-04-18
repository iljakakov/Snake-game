import random
import tkinter as tk


WINDOW_WIDTH = 720
WINDOW_HEIGHT = 780
HUD_HEIGHT = 60
PLAY_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT
CELL_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = PLAY_HEIGHT // CELL_SIZE

BACKGROUND = "#101820"
GRID_COLOR = "#1f2d3a"
SNAKE_HEAD = "#7ae582"
SNAKE_BODY = "#38b764"
FOOD_COLOR = "#ff6b6b"
TEXT_COLOR = "#f3f7f0"
PANEL_COLOR = "#17222c"
ACCENT = "#ffd166"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<a>", lambda event: self.change_direction("Left"))
        self.root.bind("<d>", lambda event: self.change_direction("Right"))
        self.root.bind("<w>", lambda event: self.change_direction("Up"))
        self.root.bind("<s>", lambda event: self.change_direction("Down"))
        self.root.bind("<r>", self.restart_game)
        self.root.bind("<R>", self.restart_game)
        self.root.bind("<space>", self.toggle_pause)

        self.best_score = 0
        self.reset_state()
        self.game_loop()

    def reset_state(self):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2

        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.spawn_food()
        self.score = 0
        self.speed = 140
        self.paused = False
        self.game_over = False

    def spawn_food(self):
        while True:
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if position not in self.snake:
                return position

    def change_direction(self, new_direction):
        if self.game_over:
            return

        opposites = {
            "Left": "Right",
            "Right": "Left",
            "Up": "Down",
            "Down": "Up",
        }
        if opposites[new_direction] != self.direction:
            self.next_direction = new_direction

    def toggle_pause(self, event=None):
        if not self.game_over:
            self.paused = not self.paused

    def move_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1
        elif self.direction == "Up":
            head_y -= 1
        else:
            head_y += 1

        new_head = (head_x, head_y)
        eating_food = new_head == self.food
        body_to_check = self.snake if eating_food else self.snake[:-1]

        if (
            head_x < 0
            or head_x >= GRID_WIDTH
            or head_y < 0
            or head_y >= GRID_HEIGHT
            or new_head in body_to_check
        ):
            self.game_over = True
            self.best_score = max(self.best_score, self.score)
            return

        self.snake.insert(0, new_head)

        if eating_food:
            self.score += 1
            self.best_score = max(self.best_score, self.score)
            self.food = self.spawn_food()
            self.speed = max(70, 140 - (self.score // 5) * 10)
        else:
            self.snake.pop()

    def draw_background(self):
        self.canvas.create_rectangle(
            0,
            0,
            WINDOW_WIDTH,
            PLAY_HEIGHT,
            fill=BACKGROUND,
            outline="",
        )

        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, PLAY_HEIGHT, fill=GRID_COLOR)

        for y in range(0, PLAY_HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, WINDOW_WIDTH, y, fill=GRID_COLOR)

        self.canvas.create_rectangle(
            0,
            PLAY_HEIGHT,
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            fill=PANEL_COLOR,
            outline="",
        )

    def draw_snake(self):
        for index, (x, y) in enumerate(self.snake):
            x1 = x * CELL_SIZE + 3
            y1 = y * CELL_SIZE + 3
            x2 = x1 + CELL_SIZE - 6
            y2 = y1 + CELL_SIZE - 6
            color = SNAKE_HEAD if index == 0 else SNAKE_BODY

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="",
                width=0,
            )

    def draw_food(self):
        x, y = self.food
        x1 = x * CELL_SIZE + 6
        y1 = y * CELL_SIZE + 6
        x2 = x1 + CELL_SIZE - 12
        y2 = y1 + CELL_SIZE - 12

        self.canvas.create_oval(x1, y1, x2, y2, fill=FOOD_COLOR, outline="")

    def draw_hud(self):
        self.canvas.create_text(
            90,
            PLAY_HEIGHT + 18,
            text="Score: {}".format(self.score),
            fill=TEXT_COLOR,
            font=("Helvetica", 18, "bold"),
        )
        self.canvas.create_text(
            250,
            PLAY_HEIGHT + 18,
            text="Best: {}".format(self.best_score),
            fill=TEXT_COLOR,
            font=("Helvetica", 18, "bold"),
        )
        self.canvas.create_text(
            470,
            PLAY_HEIGHT + 18,
            text="Arrows or WASD",
            fill=TEXT_COLOR,
            font=("Helvetica", 15, "bold"),
        )
        self.canvas.create_text(
            600,
            PLAY_HEIGHT + 18,
            text="Space: Pause",
            fill=TEXT_COLOR,
            font=("Helvetica", 15, "bold"),
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            PLAY_HEIGHT + 42,
            text="Press R to restart",
            fill=ACCENT,
            font=("Helvetica", 16, "bold"),
        )

    def draw_overlay(self):
        if not self.game_over and not self.paused:
            return

        self.canvas.create_rectangle(
            110,
            220,
            WINDOW_WIDTH - 110,
            PLAY_HEIGHT - 120,
            fill="#0b1016",
            outline=ACCENT,
            width=3,
        )

        if self.game_over:
            title = "Game Over"
            message = "Final score: {}".format(self.score)
            footer = "Press R to play again"
        else:
            title = "Paused"
            message = "Take a break and press Space to continue"
            footer = "Press R to restart"

        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            300,
            text=title,
            fill=TEXT_COLOR,
            font=("Helvetica", 32, "bold"),
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            360,
            text=message,
            fill=TEXT_COLOR,
            font=("Helvetica", 20, "bold"),
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            410,
            text=footer,
            fill=ACCENT,
            font=("Helvetica", 18, "bold"),
        )

    def draw(self):
        self.canvas.delete("all")
        self.draw_background()
        self.draw_food()
        self.draw_snake()
        self.draw_hud()
        self.draw_overlay()

    def restart_game(self, event=None):
        self.reset_state()

    def game_loop(self):
        if not self.game_over and not self.paused:
            self.move_snake()

        self.draw()
        self.root.after(self.speed, self.game_loop)


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
