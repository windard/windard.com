from  pytesser import *
im1 = Image.open("code.png")
text1 = image_to_string(im1)
print text1
print "\n"
im2 = Image.open("fonts_test.png")
text2 = image_to_string(im2)
print text2
