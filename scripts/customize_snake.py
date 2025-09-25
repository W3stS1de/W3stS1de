#!/usr/bin/env python3
"""
Script for applying custom styles to generated snake.svg
"""
import re
import os
from pathlib import Path

def extract_animations_and_paths(content):
    """Extract animations and paths from original SVG"""
    
    # Extract complete @keyframes animations with proper closing
    animations_pattern = r'(@keyframes [^{]+\{[^}]+\}[^}]*\})'
    animations = re.findall(animations_pattern, content, re.DOTALL)
    
    # Extract all rect elements (grid cells) - exclude snake elements
    rects_pattern = r'(<rect class="c[^"]*"[^>]+/>)'
    rects = re.findall(rects_pattern, content)
    
    # Extract progress bars
    progress_pattern = r'(<rect class="u[^"]*"[^>]+/>)'
    progress_bars = re.findall(progress_pattern, content)
    
    # Extract snake animation elements
    snake_elements_pattern = r'(<rect class="s[^"]*"[^>]+/>)'
    snake_elements = re.findall(snake_elements_pattern, content)
    
    return {
        'animations': '\n        '.join(animations),
        'rects': '\n    '.join(rects),
        'progress_bars': '\n    '.join(progress_bars),
        'snake_elements': '\n    '.join(snake_elements)
    }

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
        
        # Create custom SVG with proper structure
        custom_svg = f'''<svg viewBox="-16 -32 880 192" width="880" height="192" xmlns="http://www.w3.org/2000/svg">
    <desc>Generated with https://github.com/Platane/snk - Custom Styled Snake</desc>
    <style>
        :root {{
            --cb: #1b1f230a;
            --cs: #8b5cf6;
            --ce: #f3f4f6;
            --c0: #f3f4f6;
            --c1: #dcfce7;
            --c2: #86efac;
            --c3: #22c55e;
            --c4: #16a34a;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --cb: #1b1f230a;
                --cs: #a855f7;
                --ce: #111827;
                --c0: #111827;
                --c1: #064e3b;
                --c2: #065f46;
                --c3: #059669;
                --c4: #10b981;
            }}
        }}
        
        .c {{
            shape-rendering: geometricPrecision;
            fill: var(--ce);
            stroke-width: 1px;
            stroke: var(--cb);
            animation: none 20300ms linear infinite;
            width: 12px;
            height: 12px;
            rx: 2;
            ry: 2;
        }}
        
        .s {{
            shape-rendering: geometricPrecision;
            fill: var(--cs);
            animation: none linear 20300ms infinite;
            filter: drop-shadow(0 0 3px var(--cs));
        }}
        
        .u {{
            transform-origin: 0 0;
            transform: scale(0,1);
            animation: none linear 20300ms infinite;
        }}
        
        /* Original animations */
        {extracted_data['animations']}
    </style>
    
    {extracted_data['rects']}
    {extracted_data['progress_bars']}
    {extracted_data['snake_elements']}
</svg>'''
        
        # Save result
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(custom_svg)
        
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
