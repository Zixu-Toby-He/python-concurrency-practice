import time
import threading
import queue
def pause():
    from os import system
    system("pause")

def 从m加到n(m,n=None):
    结果 = 0
    if (n is None):
        n = m
        m = 0
    范围 = range(m,n+1)
    for i in 范围:
        结果+=i
#    print("\t\t从 {} 加到 {} 结果为 {}".format(m,n,结果))
    return 结果


def 从1加到n_单线程(n):
    开始时刻 = time.time()
    结果     = 从m加到n(n)
    结束时刻 = time.time()
    print("\t单线程结果：{}，用时 {:.2g}s。".format(结果,结束时刻-开始时刻))

def 从1加到n_两个线程(n):
    def 线程1任务(返回结果,开始时刻,中点):
        结果 = 从m加到n(中点)
        结束时刻=time.time()
        print("\t线程1结果：1+2+3+...+{}={}，用时 {:.2g}s。".format(中点,结果,结束时刻-开始时刻))
        返回结果.put(结果)
    def 线程2任务(返回结果,开始时刻,中点,终点):
        结果 = 从m加到n(中点+1,终点)
        结束时刻 = time.time()
        print("\t线程2结果：{}+{}+...+{}={}，用时 {:.2g}s。".format(中点+1,中点+2,终点,结果,结束时刻-开始时刻))
        返回结果.put(结果)
    开始时刻 = time.time()
    中点 = int(n/2)
    终点 = n
    结果收集 = queue.Queue()
    线程1 = threading.Thread(target=线程1任务,args=(结果收集,开始时刻,中点))
    线程2 = threading.Thread(target=线程2任务,args=(结果收集,开始时刻,中点,终点))
    线程1.start()
    线程2.start()
    线程1.join()
    线程2.join()
    最终结果=0
    while (not(结果收集.empty())):
        最终结果 += 结果收集.get()
    结束时刻 = time.time()
    print("\t单线程结果：{}，用时 {:.2g}s。".format(最终结果,结束时刻-开始时刻))

def 从1加到n_多个线程(n):
    def 生成线程任务(线程序号):
        def 线程任务(返回结果,开始时刻,起点,终点):
            结果 = 从m加到n(起点,终点)
            结束时刻 = time.time()
            print("\t线程{}计算从{}加到{}".format(线程序号,起点,终点))
            print("\t线程{}结果：{}，用时 {:.2g}s。\n".format(线程序号,结果,结束时刻-开始时刻))
            返回结果.put(结果)
        return (线程序号,线程任务)
    from multiprocessing import cpu_count
    线程数量 = int(cpu_count())
    import numpy
    节点 = numpy.linspace(0,n,线程数量+1,dtype="int")
    起点 = list(节点[:-1]+1)
    起点[0]-=1
    终点 = list(节点[1:])
#    import pandas
#    print(pandas.DataFrame({"起点":起点,"终点":终点}))
    线程信息 = {"线程函数":[],"参数列表":[],"返回值收集":[]}
    所有线程 = []
    开始时刻 = time.time()
    for i in range(线程数量):
        线程信息["线程函数"]+=[生成线程任务(i)[1]]
        线程信息["返回值收集"]+=[queue.Queue()]
        线程信息["参数列表"]+=[(线程信息["返回值收集"][i],开始时刻,起点[i],终点[i])]
        # print("\t已生成线程{}，线程函数是{}，参数列表是{}".format(i,线程信息["线程函数"][i],线程信息["参数列表"][i]))
    for i in range(线程数量):
        所有线程+=[threading.Thread(target=线程信息["线程函数"][i],args=线程信息["参数列表"][i])]
    for i in range(线程数量):
        print("线程{}开始运行".format(i))
        所有线程[i].start()
    for i in range(线程数量):
        所有线程[i].join()
    print("所有线程运行完成")
    最终结果=0
    for i in range(线程数量):
        最终结果+=线程信息["返回值收集"][i].get()
    结束时刻 = time.time()
    print("\t多线程结果：{}，用时 {:.2g}s。".format(最终结果,结束时刻-开始时刻))


        
if __name__=="__main__":
    n=int(123456789)
    print("本程序利用计算 1+2+3+...{} 来进行计算".format(n))
    print("单线程运算开始执行\n")
    从1加到n_单线程(n)
    print("结束执行\n\n")
    print("---------------------------------")
    print("两个线程运算开始执行\n")
    从1加到n_两个线程(n)
    print("结束执行\n\n")
    print("---------------------------------")
    print("多个线程运算开始执行\n")
    从1加到n_多个线程(n)
    print("结束执行\n\n")
    pause()
