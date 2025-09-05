"""
Logo utility functions for VisioValor branding
"""
import streamlit as st
from pathlib import Path
import base64

def get_logo_path():
    """Get the path to the logo directory"""
    return Path(__file__).parent.parent.parent / "assets" / "logos"

def detect_theme():
    """Detect if the current theme is light or dark"""
    try:
        # Use CSS to detect theme by checking background color
        # This is injected via st.markdown with unsafe_allow_html=True
        theme_detection_script = """
        <script>
        function detectTheme() {
            const root = document.documentElement;
            const computedStyle = getComputedStyle(root);
            const bgColor = computedStyle.getPropertyValue('--background-color').trim();
            
            // Check if background is dark (low luminance)
            if (bgColor) {
                const rgb = bgColor.match(/\\d+/g);
                if (rgb && rgb.length >= 3) {
                    const r = parseInt(rgb[0]);
                    const g = parseInt(rgb[1]);
                    const b = parseInt(rgb[2]);
                    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                    return luminance < 0.5 ? 'dark' : 'light';
                }
            }
            return 'dark'; // Default to dark
        }
        
        // Store theme in session storage for access
        sessionStorage.setItem('streamlit_theme', detectTheme());
        </script>
        """
        
        # For now, we'll use a simple approach
        # In a real implementation, you might want to use st.components.v1.html
        # or check Streamlit's theme configuration
        return "dark"  # Default to dark theme
    except:
        return "dark"

def get_logo_html(theme=None, width=200, height=80):
    """
    Get the appropriate logo HTML based on theme
    
    Args:
        theme (str): 'light' or 'dark'. If None, will auto-detect
        width (int): Logo width in pixels
        height (int): Logo height in pixels
    
    Returns:
        str: HTML string for the logo
    """
    if theme is None:
        theme = detect_theme()
    
    logo_dir = get_logo_path()
    
    if theme == "dark":
        logo_file = logo_dir / "visiovalor_logo_white.svg"
    else:
        logo_file = logo_dir / "visiovalor_logo_black.svg"
    
    if logo_file.exists():
        with open(logo_file, 'r', encoding='utf-8') as f:
            logo_svg = f.read()
        
        # Update the SVG dimensions
        logo_svg = logo_svg.replace('width="200"', f'width="{width}"')
        logo_svg = logo_svg.replace('height="80"', f'height="{height}"')
        
        return logo_svg
    else:
        # Fallback to text logo
        return f'<div style="font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; color: {"white" if theme == "dark" else "black"};">VisioValor</div>'

def display_logo(theme=None, width=200, height=80, align="center", use_theme_toggle=False, in_sidebar=False):
    """
    Display the VisioValor logo in Streamlit
    
    Args:
        theme (str): 'light' or 'dark'. If None, will auto-detect
        width (int): Logo width in pixels
        height (int): Logo height in pixels
        align (str): 'left', 'center', or 'right'
        use_theme_toggle (bool): If True, adds a theme toggle button
        in_sidebar (bool): If True, displays in sidebar with proper formatting
    """
    if use_theme_toggle and not in_sidebar:
        # Add theme toggle in sidebar
        if 'logo_theme' not in st.session_state:
            st.session_state.logo_theme = 'auto'
        
        theme_options = ['auto', 'light', 'dark']
        selected_theme = st.sidebar.selectbox(
            "Logo Theme", 
            theme_options, 
            index=theme_options.index(st.session_state.logo_theme),
            key="logo_theme_selector"
        )
        
        if selected_theme != st.session_state.logo_theme:
            st.session_state.logo_theme = selected_theme
            st.rerun()
        
        # Use selected theme
        if st.session_state.logo_theme == 'auto':
            actual_theme = None
        else:
            actual_theme = st.session_state.logo_theme
    else:
        actual_theme = theme
    
    if in_sidebar:
        # Display logo in sidebar using st.image
        logo_path = get_logo_path()
        
        if actual_theme == "light" or (actual_theme is None and detect_theme() == "light"):
            logo_file = logo_path / "visiovalor_logo_black.svg"
        else:
            logo_file = logo_path / "visiovalor_logo_white.svg"
        
        if logo_file.exists():
            # Center the logo in sidebar
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(str(logo_file), width=width)
        else:
            # Fallback to text
            st.markdown(f"<div style='text-align: center; font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; color: {'black' if actual_theme == 'light' else 'white'};'>VisioValor</div>", unsafe_allow_html=True)
    else:
        # Display logo in main area using HTML
        logo_html = get_logo_html(actual_theme, width, height)
        
        # Add alignment styling
        alignment_style = {
            "left": "text-align: left;",
            "center": "text-align: center;",
            "right": "text-align: right;"
        }.get(align, "text-align: center;")
        
        # Wrap in a container with alignment
        full_html = f"""
        <div style="{alignment_style}">
            {logo_html}
        </div>
        """
        
        st.markdown(full_html, unsafe_allow_html=True)

def get_favicon_data():
    """Get favicon data as base64 encoded string"""
    favicon_path = get_logo_path() / "favicon.svg"
    
    if favicon_path.exists():
        with open(favicon_path, 'r', encoding='utf-8') as f:
            favicon_svg = f.read()
        
        # Convert SVG to base64
        favicon_base64 = base64.b64encode(favicon_svg.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{favicon_base64}"
    
    return None
