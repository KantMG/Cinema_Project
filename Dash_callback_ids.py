#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:58:40 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for callback.

#=============================================================================
   #=============================================================================
   #============================================================================="""


import re
import plotly.graph_objects as go
import plotly.io as pio


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def get_component_ids(layout):

    """
    Goal: 
    - Get all the current ids in dash.
    
    Parameters:
    - layout: Dash layout.
    
    Returns:
    - ids: List of the current ids in dash.
    """

    ids = []
    
    # Handle layout as a component
    if hasattr(layout, 'id'):
        if layout.id:  # Check if id is not None or empty string
            ids.append(layout.id)

    # Handle layout as a list or tuple (children)
    if isinstance(layout, (list, tuple)):
        for item in layout:
            ids.extend(get_component_ids(item))
    
    # Handle layout as a component's children
    if hasattr(layout, 'children'):
        # Recursively get IDs from children
        ids.extend(get_component_ids(layout.children))

    return ids


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def create_flowchart_from_dash_app(file_path, target_ids=None):
    # Read the Python file
    with open(file_path, 'r') as file:
        code = file.read()
    
    # Regular expression to find imports with aliases
    import_pattern = r'import\s+(\w+)\s+as\s+(\w+)'
    imports = dict(re.findall(import_pattern, code))

    # Regular expression to find callbacks and their bodies
    callback_pattern = r'@app\.callback\s*\(([\s\S]*?)\)\s*def\s*(\w+)\s*\(.*?\):([\s\S]*?)(?=\n\s*def|\Z)'
    callback_matches = re.findall(callback_pattern, code)

    if not callback_matches:
        print("No callbacks found.")
        return

    # Store callback dependencies (outputs and inputs) for connection
    callback_dependencies = {}

    # Create nodes
    nodes = [{'name': 'Start', 'x': 0.5, 'y': 1.0}]
    edges = []
    communication_edges = []
    chain_edges = []
    space_between_nodes = 0.15  # Base space between nodes
    current_y = 1.0

    for i, (callback_decorators, callback_name, callback_body) in enumerate(callback_matches):
        function_calls = []
        outputs = []
        inputs = []

        # Capture outputs and inputs from callback decorators
        output_pattern = r'Output\(([^)]+)\)'
        input_pattern = r'Input\(([^)]+)\)'
        outputs.extend(re.findall(output_pattern, callback_decorators))
        inputs.extend(re.findall(input_pattern, callback_decorators))

        # Map callback dependencies
        callback_dependencies[callback_name] = {'outputs': outputs, 'inputs': inputs}

        # Detect function calls in the callback body
        for alias in imports.values():
            function_pattern = rf'{alias}\.(\w+)\('
            called_functions = re.findall(function_pattern, callback_body)
            function_calls.extend([f'{alias}.{func}' for func in called_functions])

        # Create a functions summary for hover info
        if function_calls:
            functions_summary = "Functions:<br>" + "<br>".join(function_calls)
        else:
            functions_summary = "Functions: None"
        
        # Adjust space based on the node existence
        node_gap = space_between_nodes
        current_y -= node_gap

        # Add the node with just the callback name and store the functions summary in hoverinfo and hovertext
        nodes.append({
            'name': callback_name,
            'x': 0.5,
            'y': current_y,
            'hoverinfo': functions_summary  # This will be accessed as hovertext
        })
        edges.append((0, i + 1))  # Connect each callback to the Start node

    # Identify callback communication and chain edges
    for start_callback, start_deps in callback_dependencies.items():
        for output in start_deps['outputs']:
            for end_callback, end_deps in callback_dependencies.items():
                if output in end_deps['inputs']:
                    start_index = next(i for i, node in enumerate(nodes) if node['name'] == start_callback)
                    end_index = next(i for i, node in enumerate(nodes) if node['name'] == end_callback)
                    communication_edges.append((start_index, end_index))  # Store the edge for red arrows
                    
    # Check for chains starting from each target ID
    if target_ids:
        # Extract component IDs from output strings and compare against target_ids
        target_callbacks = set()
        # Loop through each callback and check if any of its outputs match the target_ids
        for cb_name, deps in callback_dependencies.items():
            for output_str in deps['outputs']:
                # Extract the component ID from the output string, e.g., "'tabs-content', 'children'" -> "tabs-content"
                output_id = re.search(r"'([^']+)'", output_str)  # Extracts the first quoted text as component ID
                if output_id and output_id.group(1) in target_ids:
                    target_callbacks.add(cb_name)
        
        print("Target Callbacks:", target_callbacks)
        
        for start_callback in target_callbacks:
            to_visit = [start_callback]
            visited = set()

            # Traverse callbacks triggered by the starting callback
            while to_visit:
                current_callback = to_visit.pop()
                visited.add(current_callback)
                
                print(visited)
                # Find the outputs that are used as inputs in other callbacks
                for output in callback_dependencies[current_callback]['outputs']:
                    for next_callback, deps in callback_dependencies.items():
                        if output in deps['inputs'] and next_callback not in visited:
                            start_index = next(i for i, node in enumerate(nodes) if node['name'] == current_callback)
                            end_index = next(i for i, node in enumerate(nodes) if node['name'] == next_callback)
                            chain_edges.append((start_index, end_index))  # Chain edges for selected target IDs
                            to_visit.append(next_callback)
                            print(start_index, end_index)
                            
    print("to_visit=",to_visit)
    print("communication_edges=",communication_edges)
    
    # Create the figure
    fig = go.Figure()

    # Add nodes to the figure
    for node in nodes:
        # Adding hovertext from functions summary defined earlier
        hover_text = node.get('hoverinfo', 'No functions associated')
        fig.add_trace(go.Scatter(
            x=[node['x']],
            y=[node['y']],
            text=[node['name']],
            mode='text+markers',
            marker=dict(size=40, color='darkolivegreen'),
            textfont=dict(size=14),
            showlegend=False,
            hoverinfo='text',
            hovertext=hover_text  # Set hover info for the marker
        ))

    # Add default edges with arrows at the end
    for start, end in edges:
        x_coords = [nodes[start]['x'], nodes[end]['x']]
        y_coords = [nodes[start]['y'], nodes[end]['y']]

        # Draw lines
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color='DarkSlateBlue', width=2),
            showlegend=False,
            hoverinfo='none'
        ))

        # Add arrow annotations at end of line
        fig.add_annotation(
            x=x_coords[1],
            y=y_coords[1],
            ax=x_coords[0],
            ay=y_coords[0],
            showarrow=True,
            arrowsize=1,
            arrowhead=3,
            arrowcolor='DarkSlateBlue',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        )

    # Add red arrows for communication edges
    for start, end in communication_edges:
        x_coords = [nodes[start]['x'], nodes[end]['x']]
        y_coords = [nodes[start]['y'], nodes[end]['y']]

        # Draw red lines for communication edges
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color='red', width=2, dash='dash'),  # Dashed red line for communication
            showlegend=False,
            hoverinfo='none'
        ))

        # Add red arrow annotations at end of line
        fig.add_annotation(
            x=x_coords[1],
            y=y_coords[1],
            ax=x_coords[0],
            ay=y_coords[0],
            showarrow=True,
            arrowsize=1,
            arrowhead=3,
            arrowcolor='red',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        )

    # Add blue arrows for chain edges starting from target IDs
    for start, end in chain_edges:
        x_coords = [nodes[start]['x'], nodes[end]['x']]
        y_coords = [nodes[start]['y'], nodes[end]['y']]

        # Draw blue lines for chain edges
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color='blue', width=2),  # Solid blue line for chains
            showlegend=False,
            hoverinfo='none'
        ))

        # Add blue arrow annotations at end of line
        fig.add_annotation(
            x=x_coords[1],
            y=y_coords[1],
            ax=x_coords[0],
            ay=y_coords[0],
            showarrow=True,
            arrowsize=1,
            arrowhead=3,
            arrowcolor='blue',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        )

    # Update layout for dark mode and titles
    figname = 'Flowchart of Dash Application Callback Chains for Target IDs'
    fig.update_layout(
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font=dict(color='white'),
        title=figname,
        title_font=dict(size=20, color='white'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        height=1000,
    )

    return fig


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def create_detailed_flowchart(file_path, target_ids=None):
    # Read the Python file
    with open(file_path, 'r') as file:
        code = file.read()
    
    # Regular expression to find imports with aliases
    import_pattern = r'import\s+(\w+)\s+as\s+(\w+)'
    imports = dict(re.findall(import_pattern, code))

    # Regular expression to find callbacks and their bodies
    callback_pattern = r'@app\.callback\s*\(([\s\S]*?)\)\s*def\s*(\w+)\s*\(.*?\):([\s\S]*?)(?=\n\s*def|\Z)'
    callback_matches = re.findall(callback_pattern, code)

    if not callback_matches:
        print("No callbacks found.")
        return

    # Store callback dependencies (outputs and inputs) for connection
    callback_dependencies = {}

    # Create nodes
    nodes = [{'name': 'Start', 'x': 0.5, 'y': 1.0}]
    edges = []
    branch_edges = []
    space_between_nodes = 0.15  # Base space between nodes
    current_y = 1.0

    # Parse each callback for dependencies and setup nodes
    for i, (callback_decorators, callback_name, callback_body) in enumerate(callback_matches):
        function_calls = []
        outputs = []
        inputs = []

        # Capture outputs and inputs from callback decorators
        output_pattern = r'Output\(([^)]+)\)'
        input_pattern = r'Input\(([^)]+)\)'
        outputs.extend(re.findall(output_pattern, callback_decorators))
        inputs.extend(re.findall(input_pattern, callback_decorators))

        # Map callback dependencies
        callback_dependencies[callback_name] = {'outputs': outputs, 'inputs': inputs}

        # Detect function calls in the callback body
        for alias in imports.values():
            function_pattern = rf'{alias}\.(\w+)\('
            called_functions = re.findall(function_pattern, callback_body)
            function_calls.extend([f'{alias}.{func}' for func in called_functions])

        # Adjust space based on the node existence
        node_gap = space_between_nodes
        current_y -= node_gap

        # Add the node with just the callback name
        nodes.append({
            'name': callback_name,
            'x': 0.5,
            'y': current_y,
            'hoverinfo': "Functions:<br>" + "<br>".join(function_calls) if function_calls else "Functions: None"
        })
        edges.append((0, i + 1))  # Connect each callback to the Start node

    # Identify branches starting from the "render_content" callback
    for callback_name, deps in callback_dependencies.items():
        if "render_content" in callback_name:
            render_content_index = next(i for i, node in enumerate(nodes) if node['name'] == callback_name)
            tab_branches = ['tabs-1', 'tabs-2', 'tabs-3']

            for tab_index, tab in enumerate(tab_branches):
                branch_y_offset = current_y - (tab_index + 1) * space_between_nodes * 2
                tab_node_name = f"Branch {tab}"
                
                # Add branch node for each tab
                nodes.append({
                    'name': tab_node_name,
                    'x': 0.5 + (tab_index - 1) * 0.3,  # Space out each branch horizontally
                    'y': branch_y_offset,
                    'hoverinfo': f"Branch for {tab}"
                })
                branch_edges.append((render_content_index, len(nodes) - 1))  # Connect render_content to each branch

                # Identify and connect sub-branches (inputs) associated with this tab
                for sub_callback_name, sub_deps in callback_dependencies.items():
                    print("sub_callback_name=",sub_callback_name)
                    print("sub_deps=",sub_deps)
                    for sub_input in sub_deps['inputs']:
                        sub_input_id = re.search(r"'([^']+)'", sub_input)
                        print(sub_input_id , tab , sub_input_id.group(1))
                        if sub_input_id and tab in sub_input_id.group(1):
                            sub_node_y = branch_y_offset - space_between_nodes
                            sub_node_name = f"{sub_input_id.group(1)} for {tab}"
                            nodes.append({
                                'name': sub_node_name,
                                'x': 0.5 + (tab_index - 1) * 0.3,  # Keep sub-branches under each main branch
                                'y': sub_node_y,
                                'hoverinfo': f"Input: {sub_input_id.group(1)} for {tab}"
                            })
                            branch_edges.append((len(nodes) - 2, len(nodes) - 1))  # Link to sub-branch
                            print(branch_edges)

                            # Further connect to the callback affected by this input
                            sub_callback_node_y = sub_node_y - space_between_nodes
                            nodes.append({
                                'name': sub_callback_name,
                                'x': 0.5 + (tab_index - 1) * 0.3,
                                'y': sub_callback_node_y,
                                'hoverinfo': f"Callback: {sub_callback_name}"
                            })
                            branch_edges.append((len(nodes) - 2, len(nodes) - 1))  # Link input to callback

                            # Update branch offset for next node
                            branch_y_offset = sub_callback_node_y

    # Create the figure
    fig = go.Figure()

    # Add nodes to the figure
    for node in nodes:
        fig.add_trace(go.Scatter(
            x=[node['x']],
            y=[node['y']],
            text=[node['name']],
            mode='text+markers',
            marker=dict(size=40, color='darkolivegreen'),
            textfont=dict(size=14),
            showlegend=False,
            hoverinfo='text',
            hovertext=node.get('hoverinfo', 'No functions associated')
        ))

    # Add default edges with arrows at the end
    for start, end in edges:
        x_coords = [nodes[start]['x'], nodes[end]['x']]
        y_coords = [nodes[start]['y'], nodes[end]['y']]

        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color='DarkSlateBlue', width=2),
            showlegend=False,
            hoverinfo='none'
        ))

        fig.add_annotation(
            x=x_coords[1],
            y=y_coords[1],
            ax=x_coords[0],
            ay=y_coords[0],
            showarrow=True,
            arrowsize=1,
            arrowhead=3,
            arrowcolor='DarkSlateBlue',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        )

    # Add branch edges with arrows at the end
    for start, end in branch_edges:
        x_coords = [nodes[start]['x'], nodes[end]['x']]
        y_coords = [nodes[start]['y'], nodes[end]['y']]

        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color='red', width=2),
            showlegend=False,
            hoverinfo='none'
        ))

        fig.add_annotation(
            x=x_coords[1],
            y=y_coords[1],
            ax=x_coords[0],
            ay=y_coords[0],
            showarrow=True,
            arrowsize=1,
            arrowhead=3,
            arrowcolor='red',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        )

    # Update layout for dark mode and titles
    figname = 'Detailed Flowchart of Dash Application Callback Chains with Branches and Inputs'
    fig.update_layout(
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font=dict(color='white'),
        title=figname,
        title_font=dict(size=20, color='white'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        height=1000,
    )

    return fig

