import os

image_folder = "/data/IQA-Dataset/SPAQ/TestImage"

# 获取所有图片文件的路径，并按文件名排序
image_files = sorted(
    [os.path.join(image_folder, file)
     for file in os.listdir(image_folder)
     if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
)

print(image_files)
print(len(image_files))