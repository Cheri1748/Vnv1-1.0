import os
import shutil
import random

datasets_path =  r'Z:\Dataset\Vndateset\all\cut'
classes = ['airplane', 'people','vehicle'] # 这里按照顺序写
train_path =r'Z:\Dataset\Vndateset\all\train'
test_path =r'Z:\Dataset\Vndateset\all\test'
if not os.path.exists(train_path):
    os.makedirs(train_path)
if not os.path.exists(test_path):
    os.makedirs(test_path)

for index, label in enumerate(classes):
    label_path = datasets_path +'\\' +label  # 单类别的图片集地址

    # 获取源文件夹中的所有文件名
    file_names = os.listdir(label_path)
    # 计算划分的索引位置
    split_index = int(0.8 * len(file_names))  # 80% 划分给训练文件夹，20% 划分给测试文件夹
    # 随机打乱文件名顺序
    random.shuffle(file_names)
    train_folder = train_path + '\\' +str(index)
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    test_folder = test_path + '\\' +str(index)
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    # 将文件划分到训练文件夹
    for file_name in file_names[:split_index]:
        source_file_path = os.path.join(label_path, file_name)
        target_file_path = os.path.join(train_folder, file_name)
        shutil.copy2(source_file_path, target_file_path)

    # 将文件划分到测试文件夹
    for file_name in file_names[split_index:]:
        source_file_path = os.path.join(label_path, file_name)
        target_file_path = os.path.join(test_folder, file_name)
        shutil.copy2(source_file_path, target_file_path)
