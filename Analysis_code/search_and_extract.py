import sys
import pandas as pd

# 检查参数数量
if len(sys.argv) != 4:
    print("Usage: python script.py list_file.txt table_file.tsv output_file.tsv")
    sys.exit(1)

# 获取命令行参数
list_file = sys.argv[1]
table_file = sys.argv[2]
output_file = sys.argv[3]

# 读取列表文件
with open(list_file, 'r') as f:
    search_terms = f.read().splitlines()

# 读取制表符分隔的文件，不使用文件的第一行作为列名
df = pd.read_csv(table_file, sep='\t', header=None)

# 查找第6列（索引为5）是否包含列表中的任何项
# 假设第6列是字符串类型，如果不是，你可能需要先将其转换为字符串
matches = df[df.iloc[:, 11].astype(str).str.contains('|'.join(search_terms), na=False)]

# 将匹配的行写入新的TSV文件，使用制表符分隔
matches.to_csv(output_file, sep='\t', index=False, header=None)

print(f"匹配的行已写入文件：{output_file}")
