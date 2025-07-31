#python script.py input.txt output.txt
import pandas as pd
import sys

def keep_first_two_columns(input_file, output_file):
    # 读取TXT文件
    data = pd.read_csv(input_file, delimiter='\t')
    
    # 只保留前两列
    data = data.iloc[:, :2]
    
    # 将结果写入新的TXT文件
    data.to_csv(output_file, index=False, sep='\t')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        keep_first_two_columns(input_file, output_file)
