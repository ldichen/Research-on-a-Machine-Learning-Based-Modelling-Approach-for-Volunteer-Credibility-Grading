def count_numbers(filename):
    # 创建一个空字典来保存每个数字的出现次数
    number_counts = {}

    # 打开文件
    with open(filename, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 使用点号分割每行中的数字
            numbers = line.strip().split('.')

            # 遍历分割得到的数字列表
            for number in numbers:
                # 将数字添加到字典中，如果已存在则加1，否则初始化为1
                number_counts[number] = number_counts.get(number, 0) + 1

    return number_counts


# 指定文件路径
filename = "D:\\Desktop\\test.txt"

# 调用函数并输出结果
result = count_numbers(filename)
print(result)