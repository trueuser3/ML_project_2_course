import os
from PIL import Image

'''Загрузка датасета https://universe.roboflow.com/vit-oru5x/shoplifting_theft_detection2/dataset/7 в формате COCO JSON'''

folder_images_path = 'project/train/images'
folder_labels_path = 'project/train/labels'

jpeg_images_files = []
ladels_files = []


for file in os.listdir(folder_images_path):
    if file.endswith('.jpg'):
        file_path = os.path.join(folder_images_path, file)
        jpeg_images_files.append(file_path)

jpeg_images_files
im = Image.open(jpeg_files[0])
im

for file in os.listdir(folder_labels_path):
    if file.endswith('.txt'):
        file_path = os.path.join(folder_labels_path, file)
        ladels_files.append(file_path)
        #сразу домножать на то что нужно
ladels_files
name = str(ladels_files[0])
lb = open(name, 'r')
print(*lb)
name
width, height = im.size
print(width, height)
# im_crop = im.crop((left, upper, right, lower))
left = int(0.39375*640)
upper = int(0.5*360)
right = int(0.25*640)
lower = int(1*360)
im_crop = im.crop((100, 100, 100, 100))
im_crop.show()
