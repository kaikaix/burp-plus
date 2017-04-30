from PIL import Image
import pytesseract

image = Image.open('code.png')
code = pytesseract.image_to_string(image)

f = open('result.txt','w')
f.write(code)
f.close()