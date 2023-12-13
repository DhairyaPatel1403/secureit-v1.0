import streamlit as st
from PIL import Image

r=0
g=0
b=0

def rgb_to_hex(rgb_values):
    # Convert RGB values to hex format
    hex_color = "#{:02x}{:02x}{:02x}".format(rgb_values[0], rgb_values[1], rgb_values[2])
    return hex_color

def display_color(rgb_values):
    global r, g, b
    hex_color = rgb_to_hex(rgb_values)
    # Display the color using Streamlit
    # st.markdown(f'<div style="background-color: {hex_color}; width: 50px; height: 50px;"></div>', unsafe_allow_html=True)
    # st.write(f'Color: RGB({rgb_values[0]}, {rgb_values[1]}, {rgb_values[2]})')
    r += rgb_values[0]
    g += rgb_values[1]
    b += rgb_values[2]

def pixels(image):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel_value = image.getpixel((x, y))
            display_color(pixel_value)

def get_top_left_pixel(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Get the pixel value at the top-left corner (0, 0)
    top_left_pixel = image.getpixel((0, 0))

    pixels(image)

    # Close the image file
    image.close()

    return top_left_pixel

# Main Function
def main():
    st.title("Display Colors in Streamlit")
    
    top_left_pixel_value = get_top_left_pixel('100__M_Right_thumb_finger.BMP')

    st.write(f'Top-left pixel value: {top_left_pixel_value}')

    if st.button('See Values'):
        st.write(f'Values: RGB({r}, {g}, {b})')


