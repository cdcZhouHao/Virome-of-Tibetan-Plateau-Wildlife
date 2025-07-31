import os
import shutil
import sys

# 从命令行参数获取源文件夹和目标文件夹+新的命名
src_folder = sys.argv[1]
dst_file_path = sys.argv[2]

# 遍历源文件夹中的所有文件
for file_name in os.listdir(src_folder):
    # 判断文件是否符合提取条件，这里以文件名包含"final.contigs.fa"为例
    if 'final.contigs.fa' in file_name:
        # 获取文件的完整路径
        src_file_path = os.path.join(src_folder, file_name)
        # 将文件移动到目标文件夹，并重命名
        shutil.move(src_file_path, dst_file_path)

#python script/final_contig_extren.py 源文件夹路径 目标文件夹+新的文件名
#python script/final_contig_extren.py /home/user/source_folder /home/user/destination_folder/new_name.fa 注意在同一父目录下更改
