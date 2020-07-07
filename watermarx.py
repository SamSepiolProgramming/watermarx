# imports
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def main():
	print("** Running program...")

	program_intro = r"""

 

 __       __             __                                                                    
|  \  _  |  \           |  \                                                                   
| $$ / \ | $$  ______  _| $$_     ______    ______   ______ ____    ______    ______  __    __ 
| $$/  $\| $$ |      \|   $$ \   /      \  /      \ |      \    \  |      \  /      \|  \  /  \
| $$  $$$\ $$  \$$$$$$\\$$$$$$  |  $$$$$$\|  $$$$$$\| $$$$$$\$$$$\  \$$$$$$\|  $$$$$$\\$$\/  $$
| $$ $$\$$\$$ /      $$ | $$ __ | $$    $$| $$   \$$| $$ | $$ | $$ /      $$| $$   \$$ >$$  $$ 
| $$$$  \$$$$|  $$$$$$$ | $$|  \| $$$$$$$$| $$      | $$ | $$ | $$|  $$$$$$$| $$      /  $$$$\ 
| $$$    \$$$ \$$    $$  \$$  $$ \$$     \| $$      | $$ | $$ | $$ \$$    $$| $$     |  $$ \$$\
 \$$      \$$  \$$$$$$$   \$$$$   \$$$$$$$ \$$       \$$  \$$  \$$  \$$$$$$$ \$$      \$$   \$$
                                                                                               
                                                                                                                                                                                         
 ::: watermarx 1.0.0 :::
 ::: Sam Sepiol :::
 Create simple watermarks for images

	"""
	print(program_intro)

	# loading source image
	image_path = input("[$] Type path to the source image: ")
	# if file doesn't exist exit program
	if not os.path.exists(image_path):
		print("[!] Oops. This file does not exist!")
		exit(0)
	try:
		# open given image file and convert it to the rgba color encoding
		image = Image.open(image_path).convert("RGBA")
		print(f"> Source image size: {image.size[0]}px x {image.size[1]}px") # print image size
	except Exception as error:
		print("[!] Something went wrong :(. We couldn't load file.")

	# create transparent "layer" containing only text
	text_img = Image.new('RGBA', image.size, (255,255,255,0)) # !!! all colors used in this image will be encoded in RGBA
	text = input("[$] Please prompt watermark text: ")
	try:
		# watermark position
		text_x_pos = int(input("[$] Watermark x position(pixels)[optional]: "))
		text_y_pos = int(input("[$] Watermark y position(pixels)[optional]: "))
	except ValueError:
		# if given values are invalid use default position values
		text_x_pos = 40
		text_y_pos = 40
		print("[-] Invalid int value: default positions will be used(x: 40px y: 40px)")

	# watermark text size is equal to 8% of totall image height
	text_size = int(image.size[1] / 100*8)
	text_position = (text_x_pos, text_y_pos) # set watermark positions
	color = "" # color of the watermark text
	while True:
		# ask if background behind watermark is more dark or light
		text_bgr_color = input("[$] Please choose text background type(dark/light): ")
		# if it is dark set watermark text color to light(white, 50% transparency)
		if text_bgr_color == "dark":
			text_color = (255, 255, 255, 100)
			color = "light"
			break
		# otherwise if it is light the used color will be dark(black, 50% transparency)
		elif text_bgr_color == "light":
			text_color = (0, 0, 0, 100)
			color = "dark"
			break
		else:
			# if given value isn't correct ask again
			print("[-] Invalid value. Choose between dark and light.")

	# print basic info
	print(f"> Watermark text: {text}")
	print(f"> Watermark text size: {text_size}px")
	print(f"> Watermark position(x, y): {text_x_pos}px {text_y_pos}px")
	print(f"> Watermark text color: {color}")

	print("Result: ")
	print("** Converting image...")
	print("Preview: ")

	# create font for a watermark text
	font = ImageFont.truetype("assets/font/Roboto-Regular.ttf", text_size) # i used robot but you can use any other font, loaded from .ttf file
	# draw image with text
	draw = ImageDraw.Draw(text_img) 
	# add text
	draw.text((text_x_pos, text_y_pos), text, fill=text_color, font=font)
	# merge new created image with text with source image
	merged = Image.alpha_composite(image, text_img)
	# show user a result image
	merged.show()

	input("\tPress enter to continue")
	# create new path for the new image file
	output = image_path.replace(".jpg", "-watermark.png")
	# save new created image with watermark as .png file wich supports RGBA colors
	merged.save(output, "PNG", quality=100)
	print(f"[+] We finished. Your new image with watermark is saved in: {os.path.abspath(output)}.")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\n** Exiting program")
		exit()