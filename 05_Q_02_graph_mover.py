import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Load your graph data (replace this with your own method of loading graph data)
graph_tuples = pd.read_pickle("data/out/graph_tuples.pkl")

G = nx.DiGraph()
edges = graph_tuples['tuple']
G.add_weighted_edges_from(edges)

# define special nodes
start_nodes = ['*START*']
end_nodes = ['*END*']
orange_nodes = [node for node in G.nodes() if node.startswith('#')]
grey_nodes = [node for node in G.nodes() if node.startswith('...')]


# Initialize positions for the nodes (you can set initial positions if needed)
pos = nx.spring_layout(G)


# add edge weights and labels

# Calculate edge widths based on weights and normalize to range [1, 10]
edge_weights = [d['weight'] for u, v, d in G.edges(data=True)]
min_weight = min(edge_weights)
max_weight = max(edge_weights)
edge_widths = [1 + (9 * (d['weight'] - min_weight) / (max_weight - min_weight)) for u, v, d in G.edges(data=True)]



edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}



# Variables to track dragging state
dragging = False
selected_node = None

# Create a function to handle node dragging
def on_press(event):
    global dragging, selected_node
    if event.button == 1 and event.inaxes is not None:
        x, y = event.xdata, event.ydata
        closest_node = None
        min_dist = float('inf')
        
        # Find the closest node to the mouse click
        for node in G.nodes():
            node_pos = pos[node]
            dist = (node_pos[0] - x)**2 + (node_pos[1] - y)**2
            if dist < min_dist:
                closest_node = node
                min_dist = dist
        
        # If close enough to a node, start dragging it
        if min_dist < 0.01:  # Adjust this threshold as needed
            dragging = True
            selected_node = closest_node

def on_release(event):
    global dragging
    dragging = False

def on_motion(event):
    global dragging
    if dragging:
        x, y = event.xdata, event.ydata
        pos[selected_node] = (x, y)
        draw()


def draw():
    plt.clf()
    
    # Draw the graph rounded
    #nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, width=edge_widths, connectionstyle='arc3,rad=0.2')
    
    # Draw the graph with sharp edges
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, width=edge_widths)
    
    # draw edge labels
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')


    # Hebe Start- und Endknoten hervor
    nx.draw_networkx_nodes(G, pos, nodelist=start_nodes, node_color='green', node_size=1500)
    nx.draw_networkx_nodes(G, pos, nodelist=end_nodes, node_color='red', node_size=1500)

    # Färbe Knoten, die mit '#' beginnen, orange
    nx.draw_networkx_nodes(G, pos, nodelist=orange_nodes, node_color='orange', node_size=1500)

    nx.draw_networkx_nodes(G, pos, nodelist=grey_nodes, node_color='grey', node_size=1500)

    plt.draw()

# Draw the initial graph
draw()

# Connect the event handlers for mouse events
plt.gcf().canvas.mpl_connect('button_press_event', on_press)
plt.gcf().canvas.mpl_connect('button_release_event', on_release)
plt.gcf().canvas.mpl_connect('motion_notify_event', on_motion)

# Show the plot
plt.show()
