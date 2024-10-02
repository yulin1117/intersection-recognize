import pandas as pd
import os
import shutil

# 設定資料夾路徑
source_folder = '/Users/yulin/Desktop/專題程式/img'
train_folder = '/Users/yulin/Desktop/專題程式/train'
test_folder = '/Users/yulin/Desktop/專題程式/test'

# 讀取標註 CSV 文件
df = pd.read_csv('/Users/yulin/Desktop/專題程式/路口標注.csv')

# 讀取分割後的 CSV 文件
train_df = pd.read_csv('/Users/yulin/Desktop/專題程式/train.csv')
test_df = pd.read_csv('/Users/yulin/Desktop/專題程式/test.csv')

# 創建目標資料夾
os.makedirs(os.path.join(train_folder, '有路口'), exist_ok=True)
os.makedirs(os.path.join(train_folder, '無路口'), exist_ok=True)
os.makedirs(os.path.join(test_folder, '有路口'), exist_ok=True)
os.makedirs(os.path.join(test_folder, '無路口'), exist_ok=True)

def move_images(df, target_folder):
    for _, row in df.iterrows():
        img_name = row['filename']
        label = '有路口' if row['label'] == 1 else '無路口'
        src_path = os.path.join(source_folder, img_name)
        dest_path = os.path.join(target_folder, label, img_name)
        
        # 移動圖像
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)

# 移動訓練集圖像
move_images(train_df, train_folder)

# 移動測試集圖像
move_images(test_df, test_folder)

print("Image splitting and moving completed.")
