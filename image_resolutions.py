import os
from PIL import Image
import glob

input_dir = '/home/anastasia/Загрузки/project/Dataset_CSV/Train_composed/'

jpg_files = glob.glob(os.path.join(input_dir, '*.jpg'))

for jpg_file in jpg_files:
    img = Image.open(jpg_file)
    new_img = img.resize((256, 192))
    filename = os.path.basename(jpg_file)
    output_file = os.path.join(input_dir, filename.split('.')[0] + '_resize.jpg')
    new_img.save(output_file)
