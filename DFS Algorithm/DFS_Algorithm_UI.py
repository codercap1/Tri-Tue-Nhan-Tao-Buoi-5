import tkinter as tk
from tkinter import messagebox
import random

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
# NODE CHO DFS
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
    """
    Trả về danh sách hành động có thể đi.
    State là mảng 1 chiều.
    Số 0 là ô trống.

    Index:
        0 1 2
        3 4 5
        6 7 8
    """
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
    """
    Tạo node con từ node hiện tại và hành động.
    """
    state = list(node.state)

    zero_index = state.index(0)
    new_zero_index = zero_index + MOVE_DELTA[action]

    state[zero_index], state[new_zero_index] = (
        state[new_zero_index],
        state[zero_index]
    )

    return Node(
        state=tuple(state),
        parent=node,
        action=action
    )


def solution(node):
    """
    Truy vết lời giải từ node đích về node ban đầu.
    """
    path = []

    while node.parent is not None:
        path.append(node.action)
        node = node.parent

    path.reverse()
    return path


# =========================
# THUẬT TOÁN DFS
# =========================

def depth_first_search(initial_state, max_depth=50):

    node = Node(initial_state)

    if goal_test(node.state):
        return []

    # frontier <- LIFO-STACK()
    frontier = []

    # frontier.INSERT(node)
    frontier.append((node, 0))

    # explored <- empty set
    explored = set()

    # Lưu trạng thái đang có trong frontier
    frontier_states = {node.state}

    while len(frontier) > 0:

        # node <- frontier.REMOVE()
        # DFS dùng LIFO nên lấy node cuối cùng
        node, depth = frontier.pop()
        frontier_states.remove(node.state)

        # explored <- explored U {node.STATE}
        explored.add(node.state)

        # Giới hạn độ sâu để tránh DFS chạy quá lâu
        if depth >= max_depth:
            continue

        # for each action in problem.ACTIONS(node.STATE)
        for action in actions(node.state):

            # child <- CHILD-NODE(problem, node, action)
            child = child_node(node, action)

            if child.state not in explored and child.state not in frontier_states:

                # if GOAL-TEST(child.STATE)
                if goal_test(child.state):
                    return solution(child)

                # frontier.INSERT(child)
                frontier.append((child, depth + 1))
                frontier_states.add(child.state)

    return None


def apply_action_to_state(state, action):
    """
    Áp dụng hành động vào state hiện tại.
    """
    state = list(state)

    zero_index = state.index(0)
    new_zero_index = zero_index + MOVE_DELTA[action]

    state[zero_index], state[new_zero_index] = (
        state[new_zero_index],
        state[zero_index]
    )

    return tuple(state)


def is_solvable(state):
    """
    Kiểm tra 8 puzzle có giải được không.

    Với bảng 3x3:
    Nếu số nghịch thế là chẵn thì giải được.
    """
    arr = [x for x in state if x != 0]

    inversion = 0

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversion += 1

    return inversion % 2 == 0


def random_puzzle():
    """
    Tạo trạng thái random nhưng chắc chắn giải được.
    """
    state = list(GOAL_STATE)

    while True:
        random.shuffle(state)
        state_tuple = tuple(state)

        if is_solvable(state_tuple) and state_tuple != GOAL_STATE:
            return state_tuple


def state_to_text(state):
    """
    Hiển thị state 1 chiều theo dạng dễ nhìn.
    """
    return f"{state[0:3]} / {state[3:6]} / {state[6:9]}"


# =========================
# GIAO DIỆN TKINTER
# =========================

class EightPuzzleDFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle DFS Solver")

        # Kích thước cửa sổ đã chỉnh gọn hơn
        self.root.geometry("520x720")
        self.root.resizable(False, False)

        # Ban đầu là trạng thái đích
        self.state = GOAL_STATE

        self.path = []
        self.current_step = 0
        self.auto_job = None

        # Màu sắc
        self.bg_color = "#e8f5e9"       # nền xanh lá nhạt
        self.green = "#2e7d32"          # xanh lá đậm
        self.light_green = "#66bb6a"    # xanh lá
        self.orange = "#fb8c00"         # cam
        self.yellow = "#ffd54f"         # vàng
        self.empty_color = "#eeeeee"    # xám
        self.text_color = "#111111"

        self.root.configure(bg=self.bg_color)

        # Frame chính
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Tiêu đề
        title = tk.Label(
            main_frame,
            text="8 Puzzle Solver",
            font=("Arial", 22, "bold"),
            bg=self.bg_color,
            fg=self.green
        )
        title.pack(pady=(5, 3))

        subtitle = tk.Label(
            main_frame,
            text="Thuật toán Depth First Search - DFS",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#444444"
        )
        subtitle.pack(pady=(0, 10))

        # Khung bàn cờ
        self.board_frame = tk.Frame(
            main_frame,
            bg=self.green,
            padx=8,
            pady=8
        )
        self.board_frame.pack(pady=8)

        # Kích thước bàn cờ đã giảm
        self.canvas_size = 330
        self.cell_size = 110

        self.canvas = tk.Canvas(
            self.board_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=self.green,
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Label thông tin
        self.info_label = tk.Label(
            main_frame,
            text=f"Trạng thái ban đầu: {state_to_text(self.state)}",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.green
        )
        self.info_label.pack(pady=10)

        # Frame nút
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(pady=3)

        self.random_button = tk.Button(
            control_frame,
            text="Tạo Random",
            font=("Arial", 11, "bold"),
            width=14,
            height=1,
            bg=self.orange,
            activebackground="#ef6c00",
            fg="white",
            command=self.random_board
        )
        self.random_button.grid(row=0, column=0, padx=8, pady=6)

        self.solve_button = tk.Button(
            control_frame,
            text="Solve DFS",
            font=("Arial", 11, "bold"),
            width=14,
            height=1,
            bg=self.light_green,
            activebackground="#4caf50",
            fg="white",
            command=self.solve_dfs
        )
        self.solve_button.grid(row=0, column=1, padx=8, pady=6)

        self.next_button = tk.Button(
            control_frame,
            text="Next Step",
            font=("Arial", 11, "bold"),
            width=14,
            height=1,
            bg="#fbc02d",
            activebackground="#f9a825",
            fg="black",
            command=self.next_step
        )
        self.next_button.grid(row=1, column=0, padx=8, pady=6)

        self.auto_button = tk.Button(
            control_frame,
            text="Auto Run",
            font=("Arial", 11, "bold"),
            width=14,
            height=1,
            bg="#43a047",
            activebackground="#388e3c",
            fg="white",
            command=self.auto_run
        )
        self.auto_button.grid(row=1, column=1, padx=8, pady=6)

        guide_label = tk.Label(
            main_frame,
            text="Tạo Random → Solve DFS → Next Step hoặc Auto Run",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#555555"
        )
        guide_label.pack(pady=6)

        self.update_board()

    # =========================
    # VẼ Ô TAM GIÁC
    # =========================

    def draw_triangle_tile(self, row, col, value):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Xóa nền từng ô
        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=self.green,
            outline=self.green
        )

        # Tam giác nhỏ hơn để vừa với cell_size = 110
        margin = 14

        points = [
            cx, y1 + margin,
            x1 + margin, y2 - margin,
            x2 - margin, y2 - margin
        ]

        if value == 0:
            self.canvas.create_polygon(
                points,
                fill=self.empty_color,
                outline="#9e9e9e",
                width=2
            )
        else:
            self.canvas.create_polygon(
                points,
                fill=self.yellow,
                outline="#f9a825",
                width=3
            )

            self.canvas.create_text(
                cx,
                cy + 14,
                text=str(value),
                font=("Arial", 20, "bold"),
                fill=self.text_color
            )

    def update_board(self):
        self.canvas.delete("all")

        for i in range(9):
            row = i // 3
            col = i % 3
            value = self.state[i]

            self.draw_triangle_tile(row, col, value)

    # =========================
    # CLICK VÀO CANVAS
    # =========================

    def on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < 3 and 0 <= col < 3:
            index = row * 3 + col
            self.click_tile(index)

    def click_tile(self, index):
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None

        zero_index = self.state.index(0)

        zero_row = zero_index // 3
        zero_col = zero_index % 3

        tile_row = index // 3
        tile_col = index % 3

        distance = abs(zero_row - tile_row) + abs(zero_col - tile_col)

        if distance == 1:
            state = list(self.state)

            state[zero_index], state[index] = (
                state[index],
                state[zero_index]
            )

            self.state = tuple(state)

            self.path = []
            self.current_step = 0

            self.update_board()

            self.info_label.config(
                text=f"State hiện tại: {state_to_text(self.state)}",
                fg=self.green
            )

            if self.state == GOAL_STATE:
                messagebox.showinfo("Done", "Bạn đã giải xong puzzle!")

    # =========================
    # CHỨC NĂNG NÚT
    # =========================

    def random_board(self):
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None

        self.state = random_puzzle()
        self.path = []
        self.current_step = 0

        self.info_label.config(
            text=f"Random: {state_to_text(self.state)}",
            fg=self.orange
        )

        self.update_board()

    def solve_dfs(self):
        if not is_solvable(self.state):
            messagebox.showerror("Error", "Puzzle này không giải được.")
            return

        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None

        self.info_label.config(
            text="Đang tìm lời giải bằng DFS...",
            fg=self.orange
        )
        self.root.update()

        result = depth_first_search(self.state, max_depth=50)

        if result is None:
            self.path = []
            self.current_step = 0

            self.info_label.config(
                text="DFS không tìm thấy lời giải trong giới hạn độ sâu",
                fg="red"
            )

            messagebox.showerror(
                "Error",
                "DFS không tìm thấy lời giải trong giới hạn độ sâu 50."
            )
        else:
            self.path = result
            self.current_step = 0

            self.info_label.config(
                text=f"Tìm thấy lời giải DFS: {len(self.path)} bước",
                fg=self.green
            )

            print("Đường đi DFS:", self.path)

            if len(self.path) == 0:
                messagebox.showinfo("Result", "Puzzle đã ở trạng thái đích.")

    def next_step(self):
        if len(self.path) == 0:
            messagebox.showwarning("Warning", "Bạn cần bấm Solve DFS trước.")
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
            messagebox.showinfo("Done", "DFS đã giải xong puzzle!")

    def auto_run(self):
        if len(self.path) == 0:
            messagebox.showwarning("Warning", "Bạn cần bấm Solve DFS trước.")
            return

        if self.current_step >= len(self.path):
            messagebox.showinfo("Done", "Đã đi hết lời giải.")
            return

        if self.auto_job is None:
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

            self.auto_job = self.root.after(450, self.auto_step)
        else:
            self.auto_job = None
            messagebox.showinfo("Done", "DFS đã giải xong puzzle!")

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleDFSApp(root)
    root.mainloop()