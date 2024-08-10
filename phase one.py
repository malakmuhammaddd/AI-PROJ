import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
import heapq
import time
from tkinter import simpledialog, messagebox
from functools import partial
# Global Variables for Graph Representation
graph = {}
node_positions = {}
is_directed = False

# Graph Creation Functions
def add_node(x, y, heuristic):
    node_id = len(graph) + 1
    graph[node_id] = {'heuristic': heuristic}
    node_positions[node_id] = (x, y)
    canvas.create_oval(x - 35, y - 35, x + 35, y + 35, fill="yellow")
    canvas.create_text(x, y, text=str(node_id))
    canvas.create_text(x , y - 50, text="h = " + str(heuristic))

def add_edge(start, end, weight):
    graph[start].setdefault('edges', []).append((end, weight))
    x1, y1 = node_positions[start]
    x2, y2 = node_positions[end]
    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="gray")
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    canvas.create_text(mid_x, mid_y, text=str(weight))

def change_graph_type():
    global is_directed
    is_directed = not is_directed

# Search Algorithms
def depth_first_search(start, goals):
    visited = set()
    exploration_path = []

    def dfs(node):
        if node not in visited:
            visited.add(node)
            exploration_path.append(node)
            if node in goals:
                return True
            for neighbor, _ in graph[node].get('edges', []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            exploration_path.pop()
            return False

    dfs(start)
    return exploration_path

def breadth_first_search(start, goals):
    visited = set()
    exploration_path = []
    queue = [(start, [start])]

    while queue:
        node, path = queue.pop(0)
        if node not in visited:
            visited.add(node)
            exploration_path.append(node)
            if node in goals:
                return exploration_path
            neighbors = [neighbor for neighbor, _ in graph[node].get('edges', []) if neighbor not in visited]
            for neighbor in neighbors:
                queue.append((neighbor, path + [neighbor]))

    return exploration_path

def uniform_cost_search(start, goals):
    visited = set()
    exploration_path = []
    queue = [(0, start, [start])]

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            exploration_path.append(node)
            if node in goals:
                return exploration_path
            neighbors = [(neighbor, weight) for neighbor, weight in graph[node].get('edges', []) if neighbor not in visited]
            for neighbor, weight in neighbors:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

    return exploration_path
def greedy_search(start, goals):
    visited = set()
    exploration_path = []
    queue = [(heuristic(start, goals), start)]
    while queue: 
        _, node = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            exploration_path.append(node)
            if node in goals:
                return exploration_path
            neighbors = [(neighbor, heuristic(neighbor, goals)) for neighbor, _ in graph[node].get('edges', []) if neighbor not in visited]
            neighbors.sort(key=lambda x: x[1])  # Sort by heuristic value
            for neighbor, _ in neighbors:
                heapq.heappush(queue, (heuristic(neighbor, goals), neighbor))
    return exploration_path

def visualize_search_algorithm(search_algorithm):
    if not graph:
        messagebox.showwarning("Graph Not Constructed", "Please construct the graph before running a search algorithm.")
        return

    def explore_nodes(path, goals):
        G = nx.DiGraph() if is_directed else nx.Graph()

        for node in graph:
            G.add_node(node)
            G.nodes[node]['heuristic'] = graph[node]['heuristic']

        for node in graph:
            for edge in graph[node].get('edges', []):
                end, weight = edge
                G.add_edge(node, end, weight=weight)

        pos = node_positions
        labels = {node: f"{node}\nHeuristic: {G.nodes[node]['heuristic']}" for node in G.nodes()}

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, font_weight='bold')

        for i, node in enumerate(path):
            exploration_path = path[:i + 1]
            unexplored_nodes = [n for n in G.nodes() if n not in exploration_path]

            nx.draw_networkx_nodes(G, pos, nodelist=unexplored_nodes, node_color='lightgrey', node_size=500)

            if i == len(path) - 1:
                nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='green', node_size=500)
                plt.text(pos[node][0], pos[node][1] + 40, f'Path: {path}', ha='center', va='center', color='green', fontsize=15, bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.5')) #pathhbox
                plt.title(f'Exploring: {node} (Goal Node)')
            else:
                nx.draw_networkx_nodes(G, pos, nodelist=exploration_path, node_color='lightblue', node_size=500)
                plt.title(f'Exploring: {node}')

            plt.axis('off')
            plt.draw()
            plt.pause(2)  # Pause between steps

        plt.show()

        print(f"Path from Start to Goal: {path}")

    if search_algorithm == "Depth First Search":
        start_node = simpledialog.askinteger("Start Node", "Enter start node:")
        goal_nodes_str = simpledialog.askstring("Goal Nodes", "Enter goal nodes separated by commas:")
        goal_nodes = [int(node.strip()) for node in goal_nodes_str.split(",")]
        exploration_path = depth_first_search(start_node, goal_nodes)
        if exploration_path:
            explore_nodes(exploration_path, goal_nodes)
        else:
            messagebox.showinfo("Path not found", "Path from start to goal does not exist.")

    elif search_algorithm == "Breadth First Search":
        start_node = simpledialog.askinteger("Start Node", "Enter start node:")
        goal_nodes_str = simpledialog.askstring("Goal Nodes", "Enter goal nodes separated by commas:")
        goal_nodes = [int(node.strip()) for node in goal_nodes_str.split(",")]
        exploration_path = breadth_first_search(start_node, goal_nodes)
        if exploration_path:
            explore_nodes(exploration_path, goal_nodes)
        else:
            messagebox.showinfo("Path not found", "Path from start to goal does not exist.")

    elif search_algorithm == "Uniform Cost Search":
        start_node = simpledialog.askinteger("Start Node", "Enter start node:")
        goal_nodes_str = simpledialog.askstring("Goal Nodes", "Enter goal nodes separated by commas:")
        goal_nodes = [int(node.strip()) for node in goal_nodes_str.split(",")]
        exploration_path = uniform_cost_search(start_node, goal_nodes)
        if exploration_path:
            explore_nodes(exploration_path, goal_nodes)
        else:
            messagebox.showinfo("Path not found", "Path from start to goal does not exist.")

    elif search_algorithm == "A* Search":
        start_node = simpledialog.askinteger("Start Node", "Enter start node:")
        goal_nodes_str  = simpledialog.askinteger("Goal Node", "Enter goal nodes separated by commas:")
        goal_nodes = [int(node.strip()) for node in goal_nodes_str.split(",")]
        exploration_path = a_star_search(start_node, goal_nodes)
        if exploration_path:
            explore_nodes(exploration_path, goal_nodes)
        else:
            messagebox.showinfo("Path not found", "Path from start to goal does not exist.")
    elif search_algorithm == "Greedy":
        start_node = simpledialog.askinteger("Start Node", "Enter start node:")
        goal_nodes_str  = simpledialog.askinteger("Goal Node", "Enter goal nodes separated by commas:")
        goal_nodes = [int(node.strip()) for node in goal_nodes_str.split(",")]
        exploration_path = a_star_search(start_node, goal_nodes)
        if exploration_path:
            explore_nodes(exploration_path, goal_nodes)
        else:
            messagebox.showinfo("Path not found", "Path from start to goal does not exist.")

# A* Search Heuristic (Euclidean Distance Heuristic)
def heuristic(node, goal):
    # Euclidean heuristic based on node positions
    x1, y1 = node_positions[node]
    x2, y2 = node_positions[goal]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def a_star_search(start, goals):
    visited = set()
    exploration_path = []
    queue = [(heuristic(start, goals), start, [start])]

    while queue:
        _, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            exploration_path.append(node)
            if node in goals:
                return exploration_path
            neighbors = [(neighbor, weight) for neighbor, weight in graph[node].get('edges', []) if neighbor not in visited]
            for neighbor, weight in neighbors:
                heapq.heappush(queue, (len(path) + heuristic(neighbor, goals), neighbor, path + [neighbor]))

    return exploration_path

# Visualization Function
def visualize_path(path):
    G = nx.DiGraph() if is_directed else nx.Graph()

    for node in graph:
        G.add_node(node)
        G.nodes[node]['heuristic'] = graph[node]['heuristic']

    for node in graph:
        for edge in graph[node].get('edges', []):
            end, weight = edge
            G.add_edge(node, end, weight=weight)

    pos = node_positions
    labels = {node: f"{node}\nHeuristic: {G.nodes[node]['heuristic']}" for node in G.nodes()}

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title('Graph Visualization')
    plt.axis('off')
    plt.show()

# Tkinter Interface Functions
def add_node_click(event):
    x, y = event.x, event.y
    proximity_threshold = 40  # Adjust the threshold based on your preference

    # Check if the click is close to any existing node
    for node, pos in node_positions.items():
        dist = ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** 0.5
        if dist < proximity_threshold:
            # Click is close to an existing node, don't add a new one
            return
    heuristic = simpledialog.askinteger("Heuristic Value", "Enter heuristic value:")
    if heuristic is not None:
        add_node(event.x, event.y, heuristic)

def add_edge_click():
    start = simpledialog.askinteger("Start Node", "Enter start node:")
    end = simpledialog.askinteger("End Node", "Enter end node:")
    weight = simpledialog.askinteger("Edge Weight", "Enter edge weight:")
    if start in graph and end in graph:
        add_edge(start, end, weight)
    else:
        messagebox.showwarning("Error", "Node(s) not found.")

def create_window():
    window = tk.Tk()
    window.title("Search Algorithms Visualization")

    global canvas
    canvas = tk.Canvas(window, width=1500, height=700, bg="sky blue")
    canvas.pack()
    canvas.bind("<Button-1>", add_node_click)

    # Styling for buttons
    button_style = {
        'bg': 'lightblue',
        'fg': 'black',
        'relief': 'raised',
        'font': ('Arial', 12, 'bold')
    }

    add_edge_button = tk.Button(window, text="Add Edge", command=add_edge_click, **button_style)
    add_edge_button.pack(side=tk.LEFT, padx=10)

    change_graph_type_button = tk.Button(window, text="Change Graph Type", command=change_graph_type, **button_style)
    change_graph_type_button.pack(side=tk.LEFT, padx=10)

    search_algorithms = ["Depth First Search", "Breadth First Search", "Uniform Cost Search", "A* Search", "Greedy"]

    for algo in search_algorithms:
        algo_button = tk.Button(window, text=algo, command=partial(visualize_search_algorithm, algo), **button_style)
        algo_button.pack(side=tk.LEFT, padx=10)

    window.mainloop()

if __name__ == "__main__":
    create_window()