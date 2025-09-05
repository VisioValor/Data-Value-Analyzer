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
        import streamlit as st
        
        # Use a more sophisticated theme detection
        # We'll inject some CSS to detect the theme and store it in session state
        if 'detected_theme' not in st.session_state:
            # Inject CSS to detect theme
            theme_detection_css = """
            <script>
            function detectStreamlitTheme() {
                const root = document.documentElement;
                const computedStyle = getComputedStyle(root);
                
                // Check various CSS variables that indicate theme
                const bgColor = computedStyle.getPropertyValue('--background-color');
                const textColor = computedStyle.getPropertyValue('--text-color');
                
                // If we can't detect, default to dark
                if (!bgColor || !textColor) return 'dark';
                
                // Simple heuristic: if background is very dark, it's dark theme
                const bgRgb = bgColor.match(/\\d+/g);
                if (bgRgb && bgRgb.length >= 3) {
                    const r = parseInt(bgRgb[0]);
                    const g = parseInt(bgRgb[1]);
                    const b = parseInt(bgRgb[2]);
                    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                    return luminance < 0.5 ? 'dark' : 'light';
                }
                
                return 'dark';
            }
            
            // Store theme in session storage
            const theme = detectStreamlitTheme();
            sessionStorage.setItem('streamlit_theme', theme);
            </script>
            """
            
            st.markdown(theme_detection_css, unsafe_allow_html=True)
            st.session_state.detected_theme = 'dark'  # Default
        else:
            return st.session_state.detected_theme
            
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
    if in_sidebar:
        # Display logo in sidebar using st.image
        logo_path = get_logo_path()
        
        # Auto-detect theme - prefer webp files for better performance
        if theme == "light" or (theme is None and detect_theme() == "light"):
            # Try webp first, fallback to svg
            logo_file = logo_path / "visiovalor_logo_black.webp"
            if not logo_file.exists():
                logo_file = logo_path / "visiovalor_logo_black.svg"
        else:
            # Try webp first, fallback to svg
            logo_file = logo_path / "visiovalor_logo_white.webp"
            if not logo_file.exists():
                logo_file = logo_path / "visiovalor_logo_white.svg"
        
        if logo_file.exists():
            # Display logo in sidebar with proper sizing
            st.sidebar.image(str(logo_file), width=width)
        else:
            # Fallback to text in sidebar
            st.sidebar.markdown(f"<div style='text-align: center; font-family: Arial, sans-serif; font-size: 18px; font-weight: bold;'>VisioValor</div>", unsafe_allow_html=True)
    else:
        # Do not display logo in main area - logo should only be in sidebar
        st.warning("Logo should only be displayed in sidebar!")

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
