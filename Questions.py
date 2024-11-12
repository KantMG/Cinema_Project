columns = df.columns

I have 

# Calculate widths, ensuring 'title' is handled specifically
column_widths = {col: get_column_width(col) for col in columns}

if need_dropdown == True:
    # Create dropdowns using calculated widths
    dropdowns_with_labels = []
    for col in columns:
        dtype = df[col].dtype
        dropdown_style = {'width': f'{column_widths[col]}px', 'height': '40px', 'boxSizing': 'border-box'}
    
        # Container for each input/dropdown
        container_style = {'display': 'flex', 'flexDirection': 'column', 'width': '100%'}  # Flex for vertical stacking
        element = None

        if dtype == "float64":
            element = dcc.Input(
                id=f'{col}-dropdown-table-' + tab,
                type='text',
                debounce=True,
                className='dynamic-width',
                style=dropdown_style
            )
        else:
            # Collect all unique values, splitting them by commas and ensuring uniqueness
            all_roles = set()
            for value in df[col].dropna().unique():
                roles = [role.strip() for role in str(value).split(',')]
                all_roles.update(roles)
    
            unique_values = sorted(all_roles)
    
            element = dcc.Dropdown(
                id=f'{col}-dropdown-table-' + tab,
                options=[{'label': val, 'value': val} for val in unique_values],
                className='dynamic-width',
                style=dropdown_style,
                multi=True,
                clearable=True
            ) 

        # dropdowns_with_labels.append(dropdown_with_label)
        # Append each element wrapped in a container
        dropdowns_with_labels.append(html.Div(
            children=[element],
            style=container_style  # Use flexbox styling for the container
        ))


else:
    dropdowns_with_labels = None
    
    
with the css doing :

/* General styles for the body */
body {
    background-color: #101820; /* Dark background for the app */
    color: white; /* Default text color for the entire body */
    margin: 50px; /* Remove default margin */
    font-family: Arial, sans-serif; /* Use a clean font */
}

/* General styles for the tabs container */
.tabs-container {
    width: 100%; /* Full width for the container */
    display: flex;
    justify-content: center; /* Center the tabs horizontally */
    position: absolute; /* Positioning at the top */
    top: 0; /* Aligns to the top */
}

/* Style for each tab */
.Tab {
    border-radius: 10px; /* Round corners for the tabs */
    transition: background-color 0.3s; /* Smooth transition for hover effects */
    text-align: center; /* Center text horizontally */
    line-height: 20px; /* Vertical alignment for text */
    background-color: #DAA520; /* Default background color */
    color: white; /* Default text color */
    width: 80%; /* Width of each tab */
    height: 30px; /* Fixed height for all tabs */
    display: flex; /* Use flexbox for alignment */
    align-items: center; /* Center vertically */
    justify-content: center; /* Center horizontally */
    margin-right: 10px; /* Space to the right between tabs */

    /* Font styling */
    font-size: 30px; /* Larger text size */
    font-weight: bold; /* Bold text */
}

/* Remove right margin for the last tab */
.Tab:last-child {
    margin-right: 0; /* No margin on the right side of the last tab */
}

/* Custom styles for the Tabs */
.Tab.selected {
    background-color: #DAA520; /* Background for the selected tab */
    color: black; /* Text color for the selected tab */
    font-weight: bold;  /* Highlight selected tab */
}

/* Adjust hover properties if needed */
.Tab:hover {
    background-color: #FFC300; /* Lighter shade on hover for better UX */
}


/* General styles for the dropdown component */
.dash-dropdown {
    background-color: #1e1e1e !important; /* Dark background for dropdown */
    color: #f8f9fa !important; /* White text color */
    border: 1px solid #555 !important; /* Dark border */
    border-radius: 5px !important; /* Rounded corners */
    width: 160px !important; /* Set a consistent width */
    height: 40px !important; /* Set a consistent height */
}

/* Specify styles for dropdown items */
.dash-dropdown .Select-control {
    background-color: #1e1e1e; /* Ensure background is dark */
    color: #f8f9fa; /* Text color */
    border: none; /* Remove default border if necessary */
    min-height: 40px; /* Ensure the height is set properly */
}

/* Additional styles to enforce dimensions */
.dash-dropdown .Select-control input {
    height: 40px; /* Set input height */
    line-height: normal; /* Reset line-height to avoid overflow */
}

/* Dropdown menu options */
.dash-dropdown .Select-menu-outer {
    background-color: #1e1e1e !important; /* Ensure dark background for menu */
    color: white !important; /* White text */ 
}

/* Individual options */
.dash-dropdown .Select-option {
    background-color: #1e1e1e !important; /* Background color for options */
    color: white !important; /* Text color */
}

/* Focused option */
.dash-dropdown .Select-option.is-focused {
    background-color: #FFC300 !important; /* Highlight color on hover */
    color: white !important; /* Ensure text color remains white */
}

/* Ensure selected text in the dropdown remains solid white */
.dash-dropdown Select-value-label {
    color: white !important; /* Ensure solid white (with !important to override) */
    font-weight: normal; /* Ensure it's not bold if preferred */ 
}

/* Ensure dropdown placeholder text is also solid white */
.dash-dropdown Select-placeholder {
    color: rgba(255, 255, 255, 0.5); /* Shaded color for placeholder */
}

/* General styling for input fields */
.input-field {
    background-color: #1e1e1e; /* Dark background for input */
    color: #f8f9fa; /* White text color */
    border: 1px solid #555; /* Dark border */
    border-radius: 5px; /* Rounded corners */
    width: 160px; /* Set consistent width */
    height: 40px; /* Set consistent height */
    padding: 0 10px; /* Add some padding for better appearance */
    box-sizing: border-box; /* Ensure padding does not affect width */
}

/* Placeholder text style */
.input-field::placeholder {
    color: rgba(255, 255, 255, 0.5); /* Light placeholder text */
}


.dropdown-container {
    display: flex; /* Use flexbox to layout elements */
    flex-direction: column; /* Stack elements vertically */
    gap: 10px; /* Consistent spacing between elements */
    width: 100%; /* Full-width container */
}

.dynamic-width {
    max-width: 100%; /* Responsive width */
    width: 100%; /* Full width */
    box-sizing: border-box; /* Include padding/border in element's total width/height */
}

.dropdown-container > div {
    margin-bottom: 10px; /* Adds space between elements */
}
    
but it seems that dash-dropdown is affecting the dropdown even when use the class dynamic-width and not dash-dropdown