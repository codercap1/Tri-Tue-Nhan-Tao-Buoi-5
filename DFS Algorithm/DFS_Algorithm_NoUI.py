from collections import deque
import copy
import sys

# Tăng giới hạn đệ quy của Python đề phòng trường hợp DFS đi quá sâu
sys.setrecursionlimit(10000)

# NHẬP KÍCH THƯỚC MA TRẬN TỪ NGƯỜI DÙNG
ROWS = int(input("Nhập số hàng của ma trận: "))
COLS = int(input("Nhập số cột của ma trận: "))

def input_matrix(matrix_name):
    print(f"\n--- Nhập {matrix_name} (Nhập các số cách nhau bằng khoảng trắng) ---")
    matrix = []
    for i in range(ROWS):
        row = [int(x) for x in input(f"Nhập hàng {i+1}: ").split()]
        while len(row) != COLS:
            print(f"Lỗi: Hàng phải có đúng {COLS} phần tử. Vui lòng nhập lại!")
            row = [int(x) for x in input(f"Nhập hàng {i+1}: ").split()]
        matrix.append(row)
    return matrix

START_STATE = input_matrix("TRẠNG THÁI ĐẦU (START)")
GOAL_STATE = input_matrix("TRẠNG THÁI ĐÍCH (GOAL)")


# NODE 
class Node:
    def __init__(self, state, parent=None, action=None):
        self.STATE = state      # Ma trận kích thước R x C
        self.PARENT = parent    # Node cha để truy vết đường đi
        self.ACTION = action    # Hành động dẫn đến trạng thái này


# CÁC HÀM HỖ TRỢ 
def find_blank(state):
    """Tìm vị trí ô trống (số 0)"""
    for r in range(ROWS):
        for c in range(COLS):
            if state[r][c] == 0:
                return r, c
    return -1, -1

def get_actions_and_children(node):
    """Sinh các node con dựa trên kích thước ROWS và COLS linh hoạt"""
    children = []
    r, c = find_blank(node.STATE)
    
    # Định nghĩa các hướng di chuyển của ô trống
    moves = {
        'Up': (r - 1, c),
        'Down': (r + 1, c),
        'Left': (r, c - 1),
        'Right': (r, c + 1)
    }
    
    for action, (nr, nc) in moves.items():
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            new_state = copy.deepcopy(node.STATE)
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            
            child_node = Node(state=new_state, parent=node, action=action)
            children.append(child_node)
            
    return children

def goal_test(state):
    return state == GOAL_STATE

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


#  THUẬT TOÁN DEPTH-FIRST-SEARCH 
def depth_first_search():
    # node <- NODE(problem.INITIAL)
    initial_node = Node(state=START_STATE)
    
    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    if goal_test(initial_node.STATE):
        return initial_node
        
    # frontier <- LIFO-STACK()
    frontier = deque()             
    frontier.append(initial_node)  # frontier.INSERT(node)
    
    # giúp kiểm tra nhanh
    frontier_set = {state_to_tuple(START_STATE)}
    explored = set()               
    
    # while not EMPTY?(frontier) do
    while frontier:                
        # node <- frontier.REMOVE()
        node = frontier.pop()  
        
        current_tuple = state_to_tuple(node.STATE)
        if current_tuple in frontier_set:
            frontier_set.remove(current_tuple)
        
        # explored <- explored u {node.STATE}
        explored.add(current_tuple)
        
        # for each action in problem.ACTIONS(node.STATE) do
        # child <- CHILD-NODE(problem, node, action)
        for child in get_actions_and_children(node):
            child_tuple = state_to_tuple(child.STATE)
            
            # if child.STATE không thuộc explored và child không thuộc frontier
            if child_tuple not in explored and child_tuple not in frontier_set:
                # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
                if goal_test(child.STATE):
                    return child
                
                # frontier.INSERT(child)
                frontier.append(child)
                frontier_set.add(child_tuple)
                
    return None # return failure


#IN KẾT QUẢ ĐƯỜNG ĐI
def print_solution(node):
    if node is None:
        print("\n[Kết quả]: Không tìm thấy lời giải bằng thuật toán DFS!")
        return
    
    path = []
    current = node
    while current.PARENT is not None:
        path.append((current.ACTION, current.STATE))
        current = current.PARENT
    path.reverse()
    
    print("\n================ KẾT QUẢ TÌM KIẾM (DFS) ================")
    print("--- TRẠNG THÁI ĐẦU ---")
    for row in START_STATE:
        print(row)
        
    print(f"\nTìm thấy lời giải sau {len(path)} bước dịch chuyển của DFS:")
    for step, (action, state) in enumerate(path, 1):
        print(f"\nBước {step}: Ô trống di chuyển sang hướng [{action}]")
        for row in state:
            print(row)

# Tiến hành chạy thuật toán DFS
solution_node = depth_first_search()
print_solution(solution_node)