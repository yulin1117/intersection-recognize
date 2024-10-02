from PIL import Image
import os

def split_image_with_overlap(image_path, output_folder, tile_size=1024, overlap_size=256):
    # 打開大圖
    image = Image.open(image_path)
    img_width, img_height = image.size

    # 計算分塊的行數和列數
    rows = (img_height - overlap_size) // (tile_size - overlap_size) + 1
    cols = (img_width - overlap_size) // (tile_size - overlap_size) + 1

    # 創建輸出資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 切割圖片
    for row in range(rows):
        for col in range(cols):
            left = col * (tile_size - overlap_size)
            top = row * (tile_size - overlap_size)
            right = left + tile_size
            bottom = top + tile_size

            # 裁切出的小圖
            tile = image.crop((left, top, right, bottom))
            
            # 儲存小圖
            tile_path = os.path.join(output_folder, f"{os.path.basename(image_path).replace('.tif', '')}_{row}_{col}.tif")
            tile.save(tile_path)
            print(f"Saved: {tile_path}")

def process_all_images(input_folder, output_folder, tile_size=1024, overlap_size=256):
    # 遍歷資料夾中的所有.tif文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.tif'):
            image_path = os.path.join(input_folder, filename)
            split_image_with_overlap(image_path, output_folder, tile_size, overlap_size)

# 設置輸入和輸出的資料夾
input_folder = '/Volumes/NO NAME/正射影像/第1作業區/桃園市'
output_folder = '/Volumes/NO NAME/正射影像/第1作業區/small'

# 開始處理所有圖片
process_all_images(input_folder, output_folder)
