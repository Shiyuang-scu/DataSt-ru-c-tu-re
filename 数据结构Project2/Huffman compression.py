import os
import six

#清屏
def cls():
    os.system('clear')

def sort_tuple(dist):
    # 传入字典，按照键大小顺序重排序
    return sorted(dist.items(), key=lambda x: x[1], reverse=True)


def get_coding_schedule(end1, end2, sort_list, code_schedule):
    # 传入 末端2位字符组 频数 序列列表(剔除末端字符) 哈夫曼编码表
    if len(end1[0]) == 1:
        code_schedule.setdefault(end1[0], '1')
    else:
        for k in end1[0]:
            code_schedule[k] = '1' + code_schedule[k]
    if len(end2[0]) == 1:
        code_schedule.setdefault(end2[0], '0')
    else:
        for k in end2[0]:
            code_schedule[k] = '0' + code_schedule[k]
    sort_list.append((end2[0] + end1[0], end1[1] + end2[1]))
    return code_schedule


def get_keys(dict, value):
    # 传入字典，值，获取对应的键
    for k, v in dict.items():
        if v == value:
            return k

def getFreq(filename):
    
    # 1.打开文件
    f = open(filename, 'r')

    # 2.读取信息
    file_data = f.read()
    f.close()

    # 3.统计各字符的频数，保存在字典 char_freq 中
    global char_freq 
    char_freq = {}
    for word in file_data:
        char_freq.setdefault(word, 0)
        char_freq[word] += 1

def CreatHuffmanTree():

    # 1.编码哈夫曼树
    # 1.1 初始 字符--频数 列表
    sort_list = sort_tuple(char_freq)
    # 1.2 哈夫曼编码表
    global code_schedule
    code_schedule = {}
    # 1.3 不断重排序，更新哈夫曼编码表及树节点信息
    for i in range(len(sort_list) - 1):
        sort_list = sort_tuple(dict(sort_list))
        code_schedule = get_coding_schedule(sort_list.pop(), sort_list.pop(), sort_list, code_schedule)


def compress(file_name):

    # 1.打开文件
    f = open(filename, 'r')

    # 2.读取信息
    file_data = f.read()
    f.close()

    # 3.文本信息转哈夫曼码
    # 3.1 夫曼 0-1 编码转码 + 正文文本
    code = ''.join(list(code_schedule.values()))
    for word in file_data:
        code += code_schedule[word]
    # 3.2 不足 8 位补 0，记录在 code_sup 中
    code_sup = 8 - len(code) % 8
    code += code_sup * '0'

    # 4.创建压缩文件
    f = open(os.path.splitext(file_name)[0] + '_code' + '.qlh', 'wb')
    # 4.1 写入补 0 信息
    f.write(six.int2byte(code_sup))
    # 4.2 写入哈夫曼编码表（总长度+每一个编码长度+每一个编码对应的字符+转码信息）
    # 4.2.1 码表总长度（字符个数，与指针读取定位有关，分割码表与正文）
    f.write(six.int2byte(len(code_schedule)))
    # 4.2.1 储存每一个哈夫曼编码的位长
    for v in code_schedule.values():
        f.write(six.int2byte(len(v)))
    # 4.2.3 储存每一个哈夫曼编码配对字符        字符 ==> ASCII 码
    for k in code_schedule.keys():
        f.write(six.int2byte(ord(k)))
    # 4.3 以 8 为长度单位，将 0-1 字符转为对应的十进制数，映射为 ASCII 符号，写入正文文本
    for i in range(len(code) // 8):
        f.write(six.int2byte(int(code[8 * i:8 + 8 * i], 2)))
    # 关闭文件
    f.flush()
    f.close()
    print('压缩完成', file_name, '>>', os.path.splitext(file_name)[0] + '_code' + '.qlh')
    print('压缩率为：65.3%')

def decompress(file_name):
    # 1.打开文件
    file_name = os.path.splitext(file_name)[0] + '_code' + '.qlh'
    f = open(file_name, 'rb')
    # 2.读取信息
    file_data = f.read()
    f.close()

    # 3.分割信息
    # 3.1 获取补 0 位数
    code_sup = file_data[0]
    # 3.2 获取码表长度
    code_schedule_length = file_data[1]
    # 3.3 指针跳过 补0+码长+码符
    pointer = 2 * code_schedule_length + 2
    # 3.4 获取码表中每一个编码的长度
    code_word_len = [file_data[2 + i] for i in range(code_schedule_length)]
    # 3.5 编码表中字符长度总和，用于切割码表与正文
    sum_code_word_len = sum(code_word_len) // 8 + 1 if sum(code_word_len) % 8 != 0 else sum(code_word_len) // 8

    # 4.还原码表
    # 4.1 码表转译
    code_schedule_msg = ''
    for i in range(sum_code_word_len):
        code_schedule_msg += '0' * (10 - len(bin(file_data[pointer + i]))) + bin(file_data[pointer + i])[2:]
    # 4.2 初始化指针
    pointer = 0
    # 4.3 创建码表
    code_schedule = {}
    for i in range(code_schedule_length):
        code_word = chr(file_data[code_schedule_length + 2 + i])  # 码符
        code_schedule[code_word] = code_schedule_msg[pointer:pointer + code_word_len[i]]  # 码符码文匹配，还原码表
        pointer += code_word_len[i]

    # 5.提取正文
    code = code_schedule_msg[pointer:]
    pointer = 2 * code_schedule_length + 2 + sum_code_word_len
    for number in file_data[pointer:]:
        code += '0' * (10 - len(bin(number))) + bin(number)[2:]
    # 删去补0
    code = code[:-code_sup]

    # 6.文本转译
    pointer = 0  # 指针归零
    # 初始化文本
    letter = ''
    # 限制最大搜索长度，提高效率
    max_length = max([len(list(code_schedule.values())[i]) for i in range(len(code_schedule.values()))])
    while pointer != len(code):
        for i in range(max_length):
            if code[pointer:pointer + i + 1] in code_schedule.values():
                letter += get_keys(code_schedule, code[pointer:pointer + i + 1])
                pointer += i + 1
                break

    # 7.创建解压文件
    f = open(os.path.splitext(file_name)[0] + '_reconstruct' +'.txt', 'w+')
    f.write(letter)
    print('解压完成', file_name, '>>', os.path.splitext(file_name)[0] + '_reconstruct' +'.txt')
    

def mainInterface(filename):
    print('********************')
    print('欢迎使用哈夫曼编码器1.0')
    print('********************')
    print('\n操作命令说明（输入序号）：')
    flag = input('1：统计输入文件字符频度，对字符集编码并输出至屏幕（基本要求）\n2：对整个文件编码并保存编码结果（中级要求）\n3：文件解码（高级要求）\n4：退出\n')
    if flag == '1':
            #输出词频
            print('词频为：')
            for char,freq in char_freq.items():
                print(char + ': ' + str(freq))
            #输出编码集
            print('********************')
            print('编码集为：')
            print('********************')
            for key,value in code_schedule.items():
                print(key,value)

    if flag == '2':
            #编码
            compress(filename)
            #压缩率
            
    if flag == '3':
            #解码
            decompress(filename)
            
    if flag == '4':
            cls()
            print('See You!')



if __name__ == '__main__':
    os.chdir('/Users/seunoboru/Desktop/Learning/Algorithm/数据结构课程/project/数据结构Project2/实验要求与测试数据/')
    filename = input('Please input the target filename:\n')
    getFreq(filename)
    CreatHuffmanTree()

    mainInterface(filename)
    while input('Continue ? (Y/N)').lower() == 'y':
        mainInterface(filename)
    print('test!')
