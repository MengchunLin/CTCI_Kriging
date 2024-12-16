import pandas as pd
from tkinter import Tk, filedialog
original_soil_type = []

def fill_missing_values_in_soil_type(file_path):
    # 讀取第一個檔案
    df = pd.read_excel(file_path)
    
    # 填補 Soil Type 欄位的缺值
    # 線性插值
    if '合併後' in df.columns:
        df['合併後'].interpolate(method='linear', inplace=True)
        print("已填補 Soil Type 欄位的缺值。")
    else:
        print("未找到 Soil Type 欄位。")
    
    # 儲存修改後的檔案的Soil Type列
    original_soil_type = df['Soil Type']
    return original_soil_type

def round_depth_columns(file_path):
    # 讀取第二個檔案
    df = pd.read_excel(file_path)
    
    # 四捨五入 Upper depth 和 Lower depth 欄位到整數
    if 'Upper Depth' in df.columns and 'Lower Depth' in df.columns:
        df['Upper Depth'] = df['Upper Depth'].round()
        df['Lower Depth'] = df['Lower Depth'].round()
        print("已對 Upper Depth 和 Lower Depth 欄位進行四捨五入。")
    else:
        print("未找到 Upper Depth 或 Lower Depth 欄位。")
    
    # 根據修改後的 Upper Depth 和 Lower Depth 欄位計算Type欄位的數字要重複加入幾次
    length = len(df)
    type_list = []
    count = 0
    for i in range(length):
        type = df['Type'][i]
        times = int((df['Lower Depth'][i] - df['Upper Depth'][i])/0.02)
        count += times
        for j in range(times+1):
            type_list.append(type)
            j += 1
    print("Type欄位的數字要重複加入", count, "次。")
    return type_list

# 對比兩個檔案的差異

def compare_files(original_soil_type, type_list):
    difference = 0
    start = 2000
    end = 3000
    total = end - start
    for i in range(start, end):
        if original_soil_type[i] != type_list[i]:
            difference += 1
    correct_rate = (total - difference) / total
    return correct_rate


def main():
    # 使用者選擇檔案
    Tk().withdraw()  # 隱藏主視窗
    print("請選擇第一個 Excel 檔案 (處理 Soil Type 欄位)...")
    file1 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file1:
        original_soil_type = fill_missing_values_in_soil_type(file1)
        print(original_soil_type)
    
    print("請選擇第二個 Excel 檔案 (四捨五入 Upper depth 和 Lower depth 欄位)...")
    file2 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file2:
        type_list = round_depth_columns(file2)
        print(type_list)

    # 對比兩個檔案的差異
    correct_rate = compare_files(original_soil_type, type_list) * 100
    print(correct_rate,'%')

if __name__ == "__main__":
    main()
