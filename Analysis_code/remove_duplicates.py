#python remove_duplicates.py input.txt output.txt
#这将读取 input.txt 文件，去除重复值，并将结果保存到 output.txt 文件。
import sys
import pandas as pd

def remove_duplicates(input_file, output_file):
    # 读取txt文件
    df = pd.read_csv(input_file, sep="\t", header=None)
    
    # 去除重复值
    df_unique = df.drop_duplicates()
    
    # 保存到输出文件
    df_unique.to_csv(output_file, sep="\t", header=False, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_duplicates.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    remove_duplicates(input_file, output_file)
