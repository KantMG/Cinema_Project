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
