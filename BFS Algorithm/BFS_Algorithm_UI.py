import tkinter as tk
from tkinter import messagebox
from collections import deque
import random


# =========================
# CẤU HÌNH 8 PUZZLE
# =========================

GOAL_STATE = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

MOVE_DELTA = {
    "UP": -3,
    "DOWN": 3,
    "LEFT": -1,
    "RIGHT": 1
}


# =========================
# NODE CHO BFS
# =========================

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action


# =========================
# XỬ LÝ 8 PUZZLE
# =========================

def goal_test(state):
    return state == GOAL_STATE


def actions(state):
    result = []

    zero_index = state.index(0)
    row = zero_index // 3
    col = zero_index % 3

    if row > 0:
        result.append("UP")
    if row < 2:
        result.append("DOWN")
    if col > 0:
        result.append("LEFT")
    if col < 2:
        result.append("RIGHT")

    return result


def child_node(node, action):
    state = list(node.state)

    zero_index = state.index(0)
    new_zero_index = zero_index + MOVE_DELTA[action]

    state[zero_index], state[new_zero_index] = state[new_zero_index], state[zero_index]

    return Node(
        state=tuple(state),
        parent=node,
        action=action
    )


def solution(node):
    path = []

    while node.parent is not None:
        path.append(node.action)
        node = node.parent

    path.reverse()
    return path

# Thuật toán BFS
def breadth_first_search(initial_state):

    node = Node(initial_state)

    if goal_test(node.state):
        return []

    frontier = deque()
    frontier.append(node)

    explored = set()
    frontier_states = {node.state}

    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)

        explored.add(node.state)

        for action in actions(node.state):
            child = child_node(node, action)

            if child.state not in explored and child.state not in frontier_states:
                if goal_test(child.state):
                    return solution(child)

                frontier.append(child)
                frontier_states.add(child.state)

    return None


def apply_action_to_state(state, action):
    state = list(state)

    zero_index = state.index(0)
    new_zero_index = zero_index + MOVE_DELTA[action]

    state[zero_index], state[new_zero_index] = state[new_zero_index], state[zero_index]

    return tuple(state)


def is_solvable(state):
    arr = [x for x in state if x != 0]
    inversion = 0

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversion += 1

    return inversion % 2 == 0


def random_puzzle():
    state = list(GOAL_STATE)

    while True:
        random.shuffle(state)
        state_tuple = tuple(state)

        if is_solvable(state_tuple) and state_tuple != GOAL_STATE:
            return state_tuple


# =========================
# GIAO DIỆN TKINTER
# =========================

class EightPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle BFS Solver")

        # Tăng chiều cao để không bị che nút
        self.root.geometry("560x760")
        self.root.resizable(False, False)

        # Ban đầu là trạng thái đúng thứ tự
        self.state = GOAL_STATE

        self.path = []
        self.current_step = 0
        self.is_auto_running = False

        # Màu sắc
        self.bg_color = "#e8f5e9"        # xanh lá nhạt
        self.green = "#2e7d32"           # xanh lá đậm
        self.light_green = "#66bb6a"     # xanh lá
        self.orange = "#ff9800"          # cam
        self.yellow = "#ffd54f"          # vàng
        self.empty_color = "#eeeeee"     # xám
        self.text_color = "#111111"

        self.root.configure(bg=self.bg_color)

        # Frame chính
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Tiêu đề
        title = tk.Label(
            main_frame,
            text="8 Puzzle Solver",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.green
        )
        title.pack(pady=(5, 5))

        subtitle = tk.Label(
            main_frame,
            text="Thuật toán Breadth First Search - BFS",
            font=("Arial", 13),
            bg=self.bg_color,
            fg="#444444"
        )
        subtitle.pack(pady=(0, 15))

        # Khung bàn cờ
        self.board_frame = tk.Frame(
            main_frame,
            bg=self.green,
            padx=8,
            pady=8
        )
        self.board_frame.pack(pady=5)

        self.buttons = []

        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                width=4,
                height=2,
                font=("Arial", 22, "bold"),
                relief="raised",
                bd=3,
                command=lambda index=i: self.click_tile(index)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        # Thông tin
        self.info_label = tk.Label(
            main_frame,
            text="Trạng thái ban đầu: 1 2 3 / 4 5 6 / 7 8 0",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.green
        )
        self.info_label.pack(pady=12)

        # Frame chứa nút
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(pady=5)

        self.random_button = tk.Button(
            control_frame,
            text="Tạo Random",
            font=("Arial", 12, "bold"),
            width=16,
            height=2,
            bg=self.orange,
            activebackground="#fb8c00",
            fg="white",
            command=self.random_board
        )
        self.random_button.grid(row=0, column=0, padx=10, pady=7)

        self.solve_button = tk.Button(
            control_frame,
            text="Solve BFS",
            font=("Arial", 12, "bold"),
            width=16,
            height=2,
            bg=self.light_green,
            activebackground="#4caf50",
            fg="white",
            command=self.solve_bfs
        )
        self.solve_button.grid(row=0, column=1, padx=10, pady=7)

        self.next_button = tk.Button(
            control_frame,
            text="Next Step",
            font=("Arial", 12, "bold"),
            width=16,
            height=2,
            bg="#fbc02d",
            activebackground="#f9a825",
            fg="black",
            command=self.next_step
        )
        self.next_button.grid(row=1, column=0, padx=10, pady=7)

        self.auto_button = tk.Button(
            control_frame,
            text="Auto Run",
            font=("Arial", 12, "bold"),
            width=16,
            height=2,
            bg="#43a047",
            activebackground="#388e3c",
            fg="white",
            command=self.auto_run
        )
        self.auto_button.grid(row=1, column=1, padx=10, pady=7)

        guide_label = tk.Label(
            main_frame,
            text="Bấm Tạo Random → Solve BFS → Next Step hoặc Auto Run",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#555555"
        )
        guide_label.pack(pady=8)

        self.update_board()

    def update_board(self):
        for i in range(9):
            value = self.state[i]

            if value == 0:
                self.buttons[i].config(
                    text="",
                    bg=self.empty_color,
                    activebackground=self.empty_color,
                    fg=self.text_color
                )
            else:
                self.buttons[i].config(
                    text=str(value),
                    bg=self.yellow,
                    activebackground="#ffca28",
                    fg=self.text_color
                )

    def click_tile(self, index):
        zero_index = self.state.index(0)

        zero_row = zero_index // 3
        zero_col = zero_index % 3

        tile_row = index // 3
        tile_col = index % 3

        distance = abs(zero_row - tile_row) + abs(zero_col - tile_col)

        if distance == 1:
            state = list(self.state)
            state[zero_index], state[index] = state[index], state[zero_index]
            self.state = tuple(state)

            self.path = []
            self.current_step = 0
            self.is_auto_running = False

            self.update_board()
            self.info_label.config(
                text="Bạn vừa di chuyển một ô",
                fg=self.green
            )

            if self.state == GOAL_STATE:
                messagebox.showinfo("Done", "Bạn đã giải xong puzzle!")

    def random_board(self):
        self.state = random_puzzle()
        self.path = []
        self.current_step = 0
        self.is_auto_running = False

        self.info_label.config(
            text="Đã tạo trạng thái Random có thể giải được",
            fg=self.orange
        )

        self.update_board()

    def solve_bfs(self):
        if not is_solvable(self.state):
            messagebox.showerror("Error", "Puzzle này không giải được.")
            return

        self.info_label.config(
            text="Đang tìm lời giải bằng BFS...",
            fg=self.orange
        )
        self.root.update()

        result = breadth_first_search(self.state)

        if result is None:
            self.path = []
            self.current_step = 0

            self.info_label.config(
                text="Không tìm thấy lời giải",
                fg="red"
            )
            messagebox.showerror("Error", "Không tìm thấy lời giải.")
        else:
            self.path = result
            self.current_step = 0
            self.is_auto_running = False

            self.info_label.config(
                text=f"Tìm thấy lời giải BFS: {len(self.path)} bước",
                fg=self.green
            )

            print("Đường đi BFS:", self.path)

            if len(self.path) == 0:
                messagebox.showinfo("Result", "Puzzle đã ở trạng thái đích.")

    def next_step(self):
        if len(self.path) == 0:
            messagebox.showwarning("Warning", "Bạn cần bấm Solve BFS trước.")
            return

        if self.current_step >= len(self.path):
            messagebox.showinfo("Done", "Đã đi hết lời giải.")
            return

        action = self.path[self.current_step]

        self.state = apply_action_to_state(self.state, action)
        self.current_step += 1

        self.update_board()

        self.info_label.config(
            text=f"Bước {self.current_step}/{len(self.path)}: {action}",
            fg=self.orange
        )

        if self.state == GOAL_STATE:
            messagebox.showinfo("Done", "BFS đã giải xong puzzle!")

    def auto_run(self):
        if len(self.path) == 0:
            messagebox.showwarning("Warning", "Bạn cần bấm Solve BFS trước.")
            return

        if self.current_step >= len(self.path):
            messagebox.showinfo("Done", "Đã đi hết lời giải.")
            return

        if self.is_auto_running:
            return

        self.is_auto_running = True
        self.auto_step()

    def auto_step(self):
        if self.current_step < len(self.path):
            action = self.path[self.current_step]

            self.state = apply_action_to_state(self.state, action)
            self.current_step += 1

            self.update_board()

            self.info_label.config(
                text=f"Bước {self.current_step}/{len(self.path)}: {action}",
                fg=self.orange
            )

            self.root.after(400, self.auto_step)
        else:
            self.is_auto_running = False
            messagebox.showinfo("Done", "BFS đã giải xong puzzle!")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleApp(root)
    root.mainloop()