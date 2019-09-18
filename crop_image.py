from PIL import Image
import requests
from io import BytesIO

response = requests.get('https://static.india.com/wp-content/uploads/2019/04/Sachin-12.jpg')
image = Image.open(BytesIO(response.content))

# imageBox = image.getbbox()
# cropped=image.crop(imageBox)
# cropped.save('L_2d_cropped.png')


image.show()
width, height = image.size   # Get dimensions
left = width/4
top = height/4
right = 3 * width/4
bottom = 3 * height/4
cropped_example = image.crop((left, top, right, bottom))

cropped_example.show()
#image.show()