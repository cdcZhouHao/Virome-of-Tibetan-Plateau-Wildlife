import pandas as pd

def merge_files(file1, file2, output_file):
    # 读取第一个文件
    df1 = pd.read_csv(file1, sep='\t', header=None, dtype=str, engine='python')
    
    # 读取第二个文件
    df2 = pd.read_csv(file2, sep='\t', header=None, dtype=str, engine='python')
    
    # 获取df1的最后一列的列索引
    last_column_index = len(df1.columns) - 1
    
    # 合并两个 DataFrame，现在使用df1的最后一个列和df2的第一个列进行匹配
    merged_df = pd.merge(df1, df2, left_on=last_column_index, right_on=0, how='inner')
    
    # 删除重复的列（如果有的话）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    
    # 将合并后的 DataFrame 写入输出文件
    merged_df.to_csv(output_file, sep='\t', index=False, header=False)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1> <file2> <output_file>")
        sys.exit(1)
        
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
    merge_files(file1, file2, output_file)
