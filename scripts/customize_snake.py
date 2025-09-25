#!/usr/bin/env python3
"""
Script for applying custom styles to generated snake.svg
"""
import re
import os
from pathlib import Path

def apply_custom_styles(input_file, output_file):
    """Apply custom styles to generated SVG"""
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Simply replace the style section with our custom styles
        # Keep everything else from the original file intact
        
        # Find the existing style block
        style_pattern = r'<style>(.*?)</style>'
        
        # Our custom style block
        custom_styles = """
        :root {
            --cb: #1b1f230a;
            --cs: #8b5cf6;
            --ce: #f3f4f6;
            --c0: #f3f4f6;
            --c1: #dcfce7;
            --c2: #86efac;
            --c3: #22c55e;
            --c4: #16a34a;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --cb: #1b1f230a;
                --cs: #a855f7;
                --ce: #111827;
                --c0: #111827;
                --c1: #064e3b;
                --c2: #065f46;
                --c3: #059669;
                --c4: #10b981;
            }
        }
        
        .c {
            shape-rendering: geometricPrecision;
            fill: var(--ce);
            stroke-width: 1px;
            stroke: var(--cb);
            animation: none 20300ms linear infinite;
            width: 12px;
            height: 12px;
        }
        
        .s {
            shape-rendering: geometricPrecision;
            fill: var(--cs);
            animation: none linear 20300ms infinite;
            filter: drop-shadow(0 0 3px var(--cs));
        }
        
        .u {
            transform-origin: 0 0;
            transform: scale(0,1);
            animation: none linear 20300ms infinite;
        }"""
        
        # Extract and preserve all original animations
        original_style_match = re.search(style_pattern, original_content, re.DOTALL)
        if original_style_match:
            original_style = original_style_match.group(1)
            
            # Extract all @keyframes and other animations
            keyframes_pattern = r'(@keyframes[^}]+}[^}]*})'
            keyframes = re.findall(keyframes_pattern, original_style, re.DOTALL)
            
            if keyframes:
                custom_styles += "\n        \n        /* Original animations */\n        "
                custom_styles += "\n        ".join(keyframes)
        
        # Replace the style block
        custom_content = re.sub(
            style_pattern, 
            f'<style>{custom_styles}\n    </style>', 
            original_content, 
            flags=re.DOTALL
        )
        
        # Update description
        custom_content = re.sub(
            r'<desc>.*?</desc>',
            '<desc>Generated with https://github.com/Platane/snk - Custom Styled Snake</desc>',
            custom_content
        )
        
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
