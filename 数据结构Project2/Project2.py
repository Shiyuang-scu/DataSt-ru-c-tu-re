import collections
import os

#清屏
def cls():
    os.system('clear')
    
#得到词频
def getStatics(string):
    count = collections.Counter(string)
    return count

# 树节点类构建
class TreeNode(object):
    def __init__(self, data):
        self.val = data[0]
        self.priority = data[1]
        self.leftChild = None
        self.rightChild = None
        self.code = ""
# 创建树节点队列函数
def creatnodeQ(codes):
    q = []
    for code in codes:
        q.append(TreeNode(code))
    return q
# 为队列添加节点元素，并保证优先度从大到小排列
def addQ(queue, nodeNew):
    if len(queue) == 0:
        return [nodeNew]
    for i in range(len(queue)):
        if queue[i].priority >= nodeNew.priority:
            return queue[:i] + [nodeNew] + queue[i:]
    return queue + [nodeNew]
# 节点队列类定义
class nodeQeuen(object):

    def __init__(self, code):
        self.que = creatnodeQ(code)
        self.size = len(self.que)

    def addNode(self,node):
        self.que = addQ(self.que, node)
        self.size += 1

    def popNode(self):
        self.size -= 1
        return self.que.pop(0)
# 各个字符在字符串中出现的次数，即计算优先度
def freChar(string):
    d ={}
    for c in string:
        if not c in d:
            d[c] = 1
        else:
            d[c] += 1
    return sorted(d.items(),key=lambda x:x[1])
# 创建哈夫曼树
def creatHuffmanTree(nodeQ):
    while nodeQ.size != 1:
        node1 = nodeQ.popNode()
        node2 = nodeQ.popNode()
        r = TreeNode([None, node1.priority+node2.priority])
        r.leftChild = node1
        r.rightChild = node2
        nodeQ.addNode(r)
    return nodeQ.popNode()


# 由哈夫曼树得到哈夫曼编码表
def HuffmanCodeDic(head, x):
    global codeDic, codeList
    if head:
        HuffmanCodeDic(head.leftChild, x+'0')
        head.code += x
        if head.val:
            codeDic2[head.code] = head.val
            codeDic1[head.val] = head.code
        HuffmanCodeDic(head.rightChild, x+'1')

# 字符串编码
def TransEncode(string):
    global codeDic1
    transcode = ""
    for c in string:
        transcode += codeDic1[c]
    return transcode

# 字符串解码
def TransDecode(StringCode):
    global codeDic2
    code = ""
    ans = ""
    for ch in StringCode:
        code += ch
        if code in codeDic2:
            ans += codeDic2[code]
            code = ""
    return ans

#输出词频集
def outputWordStatics(string):
    mycount = getStatics(string)
    for key,value in mycount.most_common():
        print(key,value)

#编码
def encode(filename, string):
    a = TransEncode(string)
    fw = open(filename,'w')
    fw.write(a)
    fw.close()

#解码
def decode(filename):
    fr = open(filename)
    transdecode = fr.read()
    aa = TransDecode(transdecode)
    print(aa)

#计算压缩率
def compressRate(n,string):
    m = 0
    mycount = getStatics(string)
    for key,value in codeDic1.items():
       m = m + len(value)*mycount[key]
    return m/n*8

def mainInterface():
    print('********************')
    print('欢迎使用哈夫曼编码器1.0')
    print('********************')
    print('\n操作命令说明（输入序号）：')
    flag = input('1：统计输入文件字符频度，对字符集编码并输出至屏幕（基本要求）\n2：对整个文件编码并保存编码结果（中级要求）\n3：文件解码（高级要求）\n4：退出\n')
    return flag

if __name__ == '__main__':
    codeDic1 = {}
    codeDic2 = {}
    f = open('/Users/seunoboru/Desktop/Learning/Algorithm/数据结构课程/project/数据结构Project2/实验要求与测试数据/f3.txt')
    string = f.read()
    n = len(string)
    f.close()
    t = nodeQeuen(freChar(string))
    tree = creatHuffmanTree(t)
    HuffmanCodeDic(tree, '')
    filename_transcode = '/Users/seunoboru/Desktop/Learning/Algorithm/数据结构课程/project/数据结构Project2/实验要求与测试数据/f3_code.huf'
    
    flag = 0
    while(flag!='4'):
        flag = mainInterface()
        if flag == '1':
            #输出词频
            print('词频为：')
            outputWordStatics(string)
            #输出编码集
            print('********************')
            print('编码集为：')
            print('********************')
            for key,value in codeDic1.items():
                print(key,value)
        if flag == '2':
            #编码
            encode(filename_transcode,string)
            print('文件编码已完成')
            #压缩率
            print('压缩率为：',compressRate(n,string),'%')
        if flag == '3':
            #解码
            decode(filename_transcode)
            print('解码已完成')
        if flag == '4':
            cls()
            print('See You!')
            break
        choose = input('是否继续？[Y/y][N/n]')
        if(choose=='Y' or choose=='y'):
            cls()
            continue
        else:
            cls()
            print('See You!')
            break
        
        

    




