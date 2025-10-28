import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors  # Added to convert hex colors
from io import BytesIO      # Added for download button

# --- Original Functions (Unchanged) ---

def random_palette(k=5):
    """Returns k random RGB tuples."""
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def heart(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """
    Generate coordinates for a wobbly heart shape.
    Uses the famous parametric equation for a heart.
    """
    t = np.linspace(0, 2*math.pi, points)
    
    # 1. Basic heart equation
    base_x = 16 * np.sin(t)**3
    base_y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

    # 2. Normalize and apply radius 'r'
    x_norm = base_x / 16.0
    y_norm = base_y / 16.0

    # 3. Create random wobble factor
    wobble_factor = 1 + wobble*(np.random.rand(points)-0.5)

    # 4. Calculate final coordinates
    x = center[0] + x_norm * r * wobble_factor
    y = center[1] + y_norm * r * wobble_factor

    return x, y

# --- New Function to Generate the Poster ---

def create_poster(title, subtitle, n_layers, k_palette, max_wobble, alpha_range, radius_range, bg_color_hex):
    """
    Generates the Matplotlib figure based on UI controls.
    """
    # 1. Setup Figure
    fig, ax = plt.subplots(figsize=(7, 10))
    plt.axis('off')

    # 2. Set Background Color (converted from hex)
    bg_rgb = matplotlib.colors.to_rgb(bg_color_hex)
    ax.set_facecolor(bg_rgb)

    # 3. Generate Palette
    palette = random_palette(k_palette)

    # 4. Main drawing loop
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(radius_range[0], radius_range[1])
        
        # Use the max_wobble from the slider
        wobble_val = random.uniform(0.05, max_wobble)
        x, y = heart(center=(cx, cy), r=rr, wobble=wobble_val)
        
        color = random.choice(palette)
        
        # Use the alpha_range from the slider
        alpha = random.uniform(alpha_range[0], alpha_range[1])
        
        plt.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    # 5. Add Text
    plt.text(0.05, 0.95, title, fontsize=18, weight='bold', transform=ax.transAxes)
    plt.text(0.05, 0.91, subtitle, fontsize=11, transform=ax.transAxes)

    # 6. Set limits and return
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    return fig

# --- Streamlit UI (User Interface) ---

st.set_page_config(layout="wide")
st.title("Generative Heart Poster 💖")

# --- Sidebar (Controls) ---
st.sidebar.title("Poster Controls")

# Text Controls
title = st.sidebar.text_input("Title", "Generative Poster")
subtitle = st.sidebar.text_input("Subtitle", "Streamlit Cloud Edition")

# Numeric Controls
n_layers = st.sidebar.slider("Number of Hearts", 1, 30, 8)
k_palette = st.sidebar.slider("Palette Colors", 1, 10, 6)
max_wobble = st.sidebar.slider("Max Wobble", 0.05, 1.0, 0.25)
alpha_range = st.sidebar.slider("Transparency (Alpha)", 0.0, 1.0, (0.25, 0.6))
radius_range = st.sidebar.slider("Heart Size (Radius)", 0.1, 1.0, (0.15, 0.45))
bg_color = st.sidebar.color_picker("Background Color", "#F9F9F7") # Original was (0.98,0.98,0.97)

# --- Random Seed Management (Important!) ---
st.sidebar.subheader("Generation")

# Initialize seed in session state if it doesn't exist
if 'random_seed' not in st.session_state:
    st.session_state['random_seed'] = random.randint(0, 10000)

# Button to get a new seed (re-randomize layout)
if st.sidebar.button("New Random Layout"):
    st.session_state['random_seed'] = random.randint(0, 10000)

st.sidebar.text(f"Current Seed: {st.session_state['random_seed']}")

# --- Main Area (Plot) ---

# Set the seed *before* calling the drawing function.
# This ensures that tweaking sliders (which reruns the script)
# doesn't change the layout, *until* the user clicks the button.
random.seed(st.session_state['random_seed'])
np.random.seed(st.session_state['random_seed']) # Also seed numpy for the wobble

# Generate the poster
fig = create_poster(
    title, subtitle, n_layers, k_palette, 
    max_wobble, alpha_range, radius_range, bg_color
)

# Display the plot in Streamlit
st.pyplot(fig)

# --- Download Button ---
buf = BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches='tight', facecolor=bg_color)

st.sidebar.download_button(
    label="Download Poster (PNG)",
    data=buf.getvalue(),
    file_name=f"poster_{st.session_state['random_seed']}.png",
    mime="image/png"
)
