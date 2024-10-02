import pandas as pd
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
import os

def augment_and_save_images(positive_samples, input_folder, output_folder, csv_file, tile_size=1024):
    # 創建數據增強生成器
    datagen = ImageDataGenerator(
        # width_shift_range=0.2,        # 水平平移
        # height_shift_range=0.2,       # 垂直平移
        brightness_range=(0.8, 1.2),  # 亮度增強
        channel_shift_range=50,       # 顏色通道移位
        rotation_range=40,            # 旋轉角度
        shear_range=0.2,              # 剪切強度
        zoom_range=0.2,               # 縮放強度
        horizontal_flip=True,         # 水平翻轉
        fill_mode='nearest'           # 填充模式
    )
    
    # 讀取原始 CSV 文件
    df = pd.read_csv(csv_file)

    # 創建輸出資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    augmented_entries = []

    for img_name in positive_samples:
        img_path = os.path.join(input_folder, img_name)
        
        # 打開圖像
        image = Image.open(img_path)
        image = image.resize((1024, 1024))  # 調整圖像大小
        image_array = np.array(image)
        image_array = image_array.reshape((1,) + image_array.shape)  # 調整為 (1, height, width, channels) 的形狀

        # 生成增強後的圖像
        for i, batch in enumerate(datagen.flow(image_array, batch_size=1)):
            augmented_image = batch[0].astype('uint8')
            augmented_img_name = f"aug_{i}_{img_name}"
            augmented_img_path = os.path.join(output_folder, augmented_img_name)
            Image.fromarray(augmented_image).save(augmented_img_path)
            
            # 添加到 CSV 文件中的記錄
            augmented_entries.append({"filename": augmented_img_name, "label": 1})
            
            if i >= 5:  # 限制每張圖片生成的增強圖像數量
                break
    
    # 將增強後的圖片記錄添加到原 CSV 中
    augmented_df = pd.DataFrame(augmented_entries)
    df = pd.concat([df, augmented_df], ignore_index=True)
    
    # 保存更新後的 CSV 文件
    df.to_csv(csv_file, index=False)

# 設置輸入和輸出的資料夾
input_folder = '/Volumes/NO NAME/正射影像/第1作業區/small'
output_folder = '/Volumes/NO NAME/正射影像/第1作業區/small'
csv_file = '/Volumes/NO NAME/正射影像/第1作業區/桃園資料標注拷貝.csv'

# 選擇標註為 1 的圖片
df = pd.read_csv(csv_file)
positive_samples = df[df['label'] == 1]['filename'].tolist()

# 執行增強並更新 CSV
augment_and_save_images(positive_samples, input_folder, output_folder, csv_file)
