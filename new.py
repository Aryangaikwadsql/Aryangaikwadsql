from PIL import Image

def convert_jpg_to_balanced_dot_svg(
    image_path, 
    output_svg_path, 
    grid_size=150,          # Number of dots across width
    dot_spacing=8,          # Center-to-center dot distance
    min_radius=2.2,         # Keeps dark areas visible (prevents huge black gaps)
    max_radius=4.5,         # Allows bright areas to touch/overlap (max gap coverage = 4.0+)
    min_brightness=0.01,    # Lower threshold to keep subtle dark detail
    gamma=0.5,              # Values < 1.0 lift mid-tones and stop image from looking too dark
    bg_color="#0d1117"      # Set to "#ffffff" for a white background
):
    img = Image.open(image_path).convert("RGB")
    
    aspect_ratio = img.height / img.width
    grid_w = grid_size
    grid_h = int(grid_size * aspect_ratio)
    
    img_resized = img.resize((grid_w, grid_h), Image.Resampling.LANCZOS)
    
    svg_width = grid_w * dot_spacing
    svg_height = grid_h * dot_spacing
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" style="background-color: {bg_color};">',
        '  <style>',
        '    @keyframes reveal { to { opacity: 1; } }',
        '    .dot { opacity: 0; animation: reveal .18s ease-out var(--reveal-delay) forwards; }',
        '    @media (prefers-reduced-motion: reduce) { .dot { opacity: 1; animation: none; } }',
        '  </style>'
    ]
    
    for y in range(grid_h):
        for x in range(grid_w):
            r, g, b = img_resized.getpixel((x, y))
            
            # Standard perceived luminance
            brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            
            if brightness < min_brightness:
                continue
            
            # Lift mid-tones using gamma (< 1.0 expands darks/midtones so dots stay larger)
            adjusted_brightness = brightness ** gamma
            
            # Map adjusted brightness to radius
            radius = min_radius + (max_radius - min_radius) * adjusted_brightness
            
            cx = x * dot_spacing + (dot_spacing / 2)
            cy = y * dot_spacing + (dot_spacing / 2)
            reveal_delay = y * 0.032 + x * 0.0003
            
            svg_lines.append(
                f'  <circle class="dot" style="--reveal-delay:{reveal_delay:.3f}s" '
                f'cx="{cx:.2f}" cy="{cy:.2f}" r="{radius:.2f}" fill="rgb({r},{g},{b})" />'
            )
            
    svg_lines.append('</svg>')
    
    with open(output_svg_path, 'w') as f:
        f.write('\n'.join(svg_lines))

# Usage
convert_jpg_to_balanced_dot_svg(
    image_path="input.jpg", 
    output_svg_path="portrait_dots.svg", 
    grid_size=150,
    dot_spacing=8,
    min_radius=2.2,     # Increase to 2.8+ if it still feels too dark
    max_radius=4.5,     # Overlaps adjacent dots slightly in bright spots
    gamma=0.5,          # Boosts mid-tone visibility (try 0.4 for even brighter result)
    bg_color="#0d1117"
)