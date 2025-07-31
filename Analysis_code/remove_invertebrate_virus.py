import argparse


import pandas as pd





def main(file1_path, file2_path, output_path):


    # 读取文件1和文件2


    file1 = pd.read_csv(file1_path, sep='\t', header=None)


    file2 = pd.read_csv(file2_path, sep='\t', header=None)





    # 删除匹配的行（第3列匹配）


    file1 = file1[~file1[8].isin(file2[0])]





    # 删除匹配的行（第4列匹配）


    file1 = file1[~file1[9].isin(file2[1])]





    # 删除匹配的行（第5列匹配）


    file1 = file1[~file1[10].isin(file2[2])]





    # 删除匹配的行（第6列匹配）


    file1 = file1[~file1[11].isin(file2[3])]





    # 将结果写入新文件


    file1.to_csv(output_path, sep='\t', header=None, index=None)





if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Remove rows from file1 where the content of column 3 is present in file2 column 1, the content of column 4 is present in file2 column 2, the content of column 5 is present in file2 column 3, and the content of column 6 is present in file2 column 4.")


    parser.add_argument("file1", help="Path to file 1")


    parser.add_argument("file2", help="Path to file 2")


    parser.add_argument("output", help="Output file path")


    args = parser.parse_args()


    


    main(args.file1, args.file2, args.output)


