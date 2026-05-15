from collections import deque
import copy
class Node: 
    def __init__(self, state, parent = None, action = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

# Nhap array
ROWS = int(input("Nhập số hàng của ma trận: "))
COLS = int(input("Nhập số cột của ma trận: "))
def input_matrix(matrix_name): 
    print(f"\n--- Nhập {matrix_name} (Nhập các số trên cùng một dòng, cách nhau bằng khoảng trắng) ---")
    matrix = []
    for i in range(ROWS): 
        row = [int(x) for x in input(f"Nhập hàng {i + 1}: ").split()]
        while len(row) != COLS:
            print(f"Lỗi: Hàng phải có đúng {COLS} phần tử. Vui lòng nhập lại!")
            row = [int(x) for x in input(f"Nhập hàng {i + 1}: ").split()]
        matrix.append(row)

    return matrix


# Nhập trạng thái ban đầu và trạng thái đích
START_STATE = input_matrix("TRẠNG THÁI ĐẦU (START)")
GOAL_STATE = input_matrix("TRẠNG THÁI ĐÍCH (GOAL)")

# Node
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.STATE = state
        self.PARENT = parent
        self.ACTION = action
        self.PATH_COST = path_cost

# find location of zero number
def find_zero(state): 
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] == 0:
                return i, j
            
    return -1, -1

# rule and action 
def get_actions_and_children(node):
    
    Children = []
    r, c = find_zero(node.STATE)
    moves = {
        'Up': (r - 1, c),
        'Down': (r + 1, c),
        'Left': (r, c - 1),
        'Right': (r, c + 1)
    }
    #Taking suitable nodes 
    for action, (nr, nc) in moves.items():
        if 0 <= nr < ROWS and 0 <= nc < COLS: 
            new_state = copy.deepcopy(node.STATE)

            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]

            child_node = Node(state=new_state, parent=node, action = action, path_cost=node.PATH_COST + 1)
            Children.append(child_node)
    return Children

# check with goal
def goal_test(state):
    return state == GOAL_STATE

#convert list to tuple so that I can save in a "set"
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

#BFS algorithm
def breadth_first_search():
    initial_node = Node(state = START_STATE)

    if goal_test(initial_node):
        return initial_node
    
    frontier = deque()
    frontier.append(initial_node)

    frontier_set = {state_to_tuple(START_STATE)}
    explored = set()

    while frontier:
        node = frontier.popleft()
        current_tuple = state_to_tuple(node.STATE)

        if current_tuple in frontier_set:
            frontier_set.remove(current_tuple)
        
        explored.add(current_tuple) 
        for child in get_actions_and_children(node):
            child_tuple = state_to_tuple(child.STATE)

            if child_tuple not in explored and child_tuple not in frontier_set:
                if goal_test(child.STATE): 
                    return child
                
                frontier.append(child)
                frontier_set.add(child_tuple)
    
    return None

# IN KẾT QUẢ ĐƯỜNG ĐI
def print_solution(node):
    if node is None:
        print("\n[Kết quả]: Không tìm thấy lời giải sau khi duyệt hết trạng thái!")
        return
    
    path = []
    current = node
    while current.PARENT is not None:
        path.append((current.ACTION, current.STATE, current.PATH_COST))
        current = current.PARENT
    path.reverse()
    
    print("\n================ KẾT QUẢ TÌM KIẾM ================")
    print("--- TRẠNG THÁI ĐẦU ---")
    for row in START_STATE:
        print(row)
        
    print(f"\nTìm thấy lời giải ngắn nhất sau {len(path)} bước dịch chuyển:")
    for step, (action, state, path_cost) in enumerate(path, 1):
        print(f"\nBước {step}: Ô trống di chuyển sang hướng [{action}], path_cost: {path_cost}")
        for row in state:
            print(row)

# Tiến hành chạy thuật toán
solution_node = breadth_first_search()
print_solution(solution_node)


