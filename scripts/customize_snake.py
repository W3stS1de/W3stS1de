#!/usr/bin/env python3
"""
Script for applying custom styles to generated snake.svg
"""
import re
import os
from pathlib import Path

def extract_animations_and_paths(content):
    """Extract animations and paths from original SVG"""
    
    # Extract all @keyframes animations
    animations_pattern = r'(@keyframes [^}]+})'
    animations = re.findall(animations_pattern, content, re.DOTALL)
    
    # Extract all rect elements (grid cells)
    rects_pattern = r'(<rect[^>]+/>)'
    rects = re.findall(rects_pattern, content)
    
    # Extract all snake animation elements
    snake_elements_pattern = r'(<rect class="s[^"]*"[^>]+/>)'
    snake_elements = re.findall(snake_elements_pattern, content)
    
    return {
        'animations': '\n'.join(animations),
        'rects': '\n'.join(rects),
        'snake_elements': '\n'.join(snake_elements)
    }

def create_custom_svg(original_content, extracted_data):
    """Create custom SVG while preserving activity data"""
    
    custom_svg = f'''<svg viewBox="-16 -32 880 192" width="880" height="192" xmlns="http://www.w3.org/2000/svg">
    <desc>Generated with https://github.com/Platane/snk - Custom Styled Snake</desc>
    <style>
        :root{{
            --cb: #1b1f230a;
            --cs: #8b5cf6;  /* Purple snake */
            --ce: #f3f4f6;  /* Light background */
            --c0: #f3f4f6;
            --c1: #dcfce7;  /* Light green */
            --c2: #86efac;  /* Medium green */
            --c3: #22c55e;  /* Bright green */
            --c4: #16a34a;  /* Dark green */
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --cb: #1b1f230a;
                --cs: #a855f7;  /* Brighter purple for dark mode */
                --ce: #111827;  /* Dark background */
                --c0: #111827;
                --c1: #064e3b;  /* Dark green variants */
                --c2: #065f46;
                --c3: #059669;
                --c4: #10b981;
            }}
        }}
        
        /* Cell styles */
        .c {{
            shape-rendering: geometricPrecision;
            fill: var(--ce);
            stroke-width: 1px;
            stroke: var(--cb);
            width: 12px;
            height: 12px;
            rx: 2;
            ry: 2;
            transition: all 0.2s ease;
        }}
        
        .c:hover {{
            stroke-width: 2px;
            stroke: var(--cs);
        }}
        
        /* Styles for different activity levels */
        .c.c0 {{ fill: var(--c0); }}
        .c.c1 {{ fill: var(--c1); }}
        .c.c2 {{ fill: var(--c2); }}
        .c.c3 {{ fill: var(--c3); }}
        .c.c4 {{ fill: var(--c4); }}
        
        /* Snake styles */
        .s {{
            shape-rendering: geometricPrecision;
            fill: var(--cs);
            animation: none linear 20300ms infinite;
            rx: 4;
            ry: 4;
            filter: drop-shadow(0 0 3px var(--cs));
        }}
        
        /* Progress bar styles */
        .u {{
            transform-origin: 0 0;
            transform: scale(0,1);
            animation: none linear 20300ms infinite;
            rx: 6;
            ry: 6;
        }}
        
        .u.u0 {{ fill: var(--c1); }}
        .u.u1 {{ fill: var(--c2); }}
        .u.u2 {{ fill: var(--c3); }}
        .u.u3 {{ fill: var(--c4); }}
        
        /* Animations from original file */
        {extracted_data['animations']}
        
        /* Additional effects */
        @media (prefers-reduced-motion: no-preference) {{
            .c {{
                animation: pulse 2s infinite;
            }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
        }}
    </style>
    
    <!-- Activity cells -->
    {extracted_data['rects']}
    
    <!-- Progress bars -->
    <!-- These elements will be added automatically -->
    
    <!-- Snake -->
    {extracted_data['snake_elements']}
</svg>'''
    
    return custom_svg

def apply_custom_styles(input_file, output_file):
    """Apply custom styles to generated SVG"""
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Extract data from original file
        extracted_data = extract_animations_and_paths(original_content)
        
        # Create custom SVG
        custom_content = create_custom_svg(original_content, extracted_data)
        
        # Save result
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(custom_content)
        
        print(f"Success: Custom SVG created: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return False

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent
    
    # File paths
    generated_file = base_dir / "dist" / "snake-generated.svg"
    output_file = base_dir / "snake.svg"
    
    print("Applying custom styles to Snake SVG...")
    
    if apply_custom_styles(str(generated_file), str(output_file)):
        print("Done! Custom snake updated")
    else:
        print("Something went wrong...")

if __name__ == "__main__":
    main()
