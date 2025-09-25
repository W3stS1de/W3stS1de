#!/usr/bin/env python3
"""
Simple script to replace colors in snake SVG
"""
import os

def main():
    input_file = "dist/snake-generated.svg"
    output_file = "snake.svg"
    
    print(f"Looking for input file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"ERROR: Input file {input_file} does not exist!")
        print("Files in dist directory:")
        try:
            files = os.listdir("dist")
            for f in files:
                print(f"  - {f}")
        except:
            print("  dist directory does not exist")
        return
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r') as f:
        content = f.read()
    
    print("Applying custom styles...")
    
    # Replace colors
    content = content.replace('--cs:purple', '--cs:#8b5cf6')
    content = content.replace('--ce:#ebedf0', '--ce:#f3f4f6')
    content = content.replace('--ce:#161b22', '--ce:#111827')
    
    # Replace description
    content = content.replace(
        'Generated with https://github.com/Platane/snk',
        'Generated with https://github.com/Platane/snk - Custom Styled Snake'
    )
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w') as f:
        f.write(content)
    
    print("SUCCESS: Custom snake SVG created!")

if __name__ == "__main__":
    main()
