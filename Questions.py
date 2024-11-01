
import re
import plotly.graph_objects as go
import plotly.io as pio

def create_flowchart_from_dash_app(file_path):
    # Set the default renderer
    pio.renderers.default = 'browser'

    # Read the Python file
    with open(file_path, 'r') as file:
        code = file.read()

    # Regular expression to find callbacks
    callback_pattern = r'@app\.callback\s*\([\s\S]*?\)\s*def\s*(\w+)\s*\('
    callbacks = re.findall(callback_pattern, code)
    
    if not callbacks:
        print("No callbacks found.")
        return

    # Create nodes
    nodes = [{'name': 'Start', 'x': 0.5, 'y': 1.0}]
    edges = []
    for i, callback in enumerate(callbacks):
        nodes.append({'name': callback, 'x': 0.5, 'y': 1.0 - (i + 1) * 0.15})  # Space out the nodes
        edges.append((0, i + 1))  # Connect each callback to the Start node
    
    # Create the figure
    fig = go.Figure()

    # Add nodes to the figure
    for node in nodes:
        fig.add_trace(go.Scatter(
            x=[node['x']],
            y=[node['y']],
            text=[node['name']],
            mode='text+markers',
            marker=dict(size=20, color='LightSkyBlue'),
            textfont=dict(size=14),
            showlegend=False
        ))

    # Add edges
    for start, end in edges:
        fig.add_trace(go.Scatter(
            x=[nodes[start]['x'], nodes[end]['x']],
            y=[nodes[start]['y'], nodes[end]['y']],
            mode='lines',
            line=dict(color='DarkSlateBlue', width=2),
            showlegend=False
        ))

    # Set layout properties
    fig.update_layout(
        showlegend=False,
        title='Flowchart of Dash Application Callbacks',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
    )

    # Show the figure
    fig.show()

Project_path='/home/quentin/Documents/Work/Data_analytics/Datasets/Cinema_Project/'
# Example usage
create_flowchart_from_dash_app(Project_path+'test.py')



# import plotly.graph_objects as go
# import plotly.io as pio

# # Set the default renderer to open the figure in the browser
# pio.renderers.default = 'browser'

# # Define the flowchart nodes
# nodes = [
#     {'name': 'Start', 'x': 0.5, 'y': 1},
#     {'name': 'User Inputs Text', 'x': 0.5, 'y': 0.8},
#     {'name': 'Submit Button Clicked?', 'x': 0.5, 'y': 0.6},
#     {'name': 'Update output_div', 'x': 0.5, 'y': 0.4},
#     {'name': 'Prompt: "Enter something and press submit!"', 'x': 0.3, 'y': 0.6},
#     {'name': 'Display Text: "You entered: {value}"', 'x': 0.5, 'y': 0.25},
#     {'name': 'Dropdown Selection', 'x': 0.5, 'y': 0.5},
#     {'name': 'Update dropdown-output', 'x': 0.5, 'y': 0.35},
#     {'name': 'Display Selected Option: "Selected option: {value}"', 'x': 0.5, 'y': 0.1},
#     {'name': 'End', 'x': 0.5, 'y': 0}
# ]

# # Create the figure
# fig = go.Figure()

# # Add nodes to the figure
# for node in nodes:
#     fig.add_trace(go.Scatter(
#         x=[node['x']],
#         y=[node['y']],
#         text=[node['name']],
#         mode='text+markers',
#         marker=dict(size=20, color='LightSkyBlue'),
#         textfont=dict(size=14),
#         showlegend=False
#     ))

# # Define the lines (edges) connecting the nodes
# edges = [
#     (0, 1),  # Start to User Inputs Text
#     (1, 2),  # User Inputs Text to Submit Button Clicked?
#     (2, 3),  # Submit Button Clicked? to Update output_div
#     (2, 4),  # Submit Button Clicked? to Prompt
#     (3, 5),  # Update output_div to Display Text
#     (1, 6),  # User Inputs Text to Dropdown Selection
#     (6, 7),  # Dropdown Selection to Update dropdown-output
#     (7, 8),  # Update dropdown-output to Display Selected Option
# ]

# # Add lines to represent edges
# for start, end in edges:
#     fig.add_trace(go.Scatter(
#         x=[nodes[start]['x'], nodes[end]['x']],
#         y=[nodes[start]['y'], nodes[end]['y']],
#         mode='lines+text',
#         line=dict(color='DarkSlateBlue', width=2),
#         text=["", ""],
#         textposition='middle right',
#         showlegend=False
#     ))

# # Set layout properties
# fig.update_layout(
#     showlegend=False,
#     title='Flowchart of Dash Application',
#     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#     height=600,
# )

# # Show the figure
# fig.show()