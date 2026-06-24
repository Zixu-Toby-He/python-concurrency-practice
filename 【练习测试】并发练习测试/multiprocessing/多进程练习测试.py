#from email.mime.multipart import MIMEMultipart
import time
import multiprocessing

def pause():
    from os import system
    system("pause")

def 从m加到n(m,n=None):
    结果=0
    if (n is None):
        n=m
        m=0
    范围=range(m,n+1)
    for i in 范围:
        结果+=i
#    print("\t\t从 {} 加到 {} 结果为 {}".format(m,n,结果))
    return 结果


def 从1加到n_单进程(n):
    开始时刻=time.time()
    结果=从m加到n(n)
    结束时刻=time.time()
    print("\t单线程结果：{}，用时 {:.2g}s。".format(结果,结束时刻-开始时刻))

# 创建进程不能用函数内函数
def 进程1任务(进程结果收集,开始时刻,中点):
    结果=从m加到n(中点)
    结束时刻=time.time()
    print("\t进程1结果：{}，用时 {:.2g}s。".format(结果,结束时刻-开始时刻))
    进程结果收集.put(结果)
def 进程2任务(进程结果收集,开始时刻,中点,终点):
    结果=从m加到n(中点+1,终点)
    结束时刻=time.time()
    print("\t进程2结果：{}，用时 {:.2g}s。".format(结果,结束时刻-开始时刻))
    进程结果收集.put(结果)
def 从1加到n_两个进程(n):
    开始时刻=time.time()
    中点=int(n/2)
    终点=n
    
    进程结果收集 = multiprocessing.Queue()
    
    进程1=multiprocessing.Process(target=进程1任务,args=(进程结果收集,开始时刻,中点))
    进程2=multiprocessing.Process(target=进程2任务,args=(进程结果收集,开始时刻,中点,终点))

    进程1.start()
    进程2.start()
    进程1.join()
    进程2.join()
    线程1结果 = 进程结果收集.get()
    线程2结果 = 进程结果收集.get()
    最终结果 = 线程1结果 + 线程2结果
    结束时刻=time.time()
    print("执行完成，最终结果为 {}，用时 {:.2g}s".format(最终结果,结束时刻-开始时刻))

# 多个进程
def 进程任务(返回结果,开始时刻,起点,终点):
    进程名称 = multiprocessing.current_process().name
    结果 = 从m加到n(起点,终点)
    结束时刻 = time.time()
    print("\t进程“{}”计算从{}加到{}".format(进程名称,起点,终点))
    print("\t进程“{}”结果：{}，用时 {:.2g}s。\n".format(进程名称,结果,结束时刻-开始时刻))
    返回结果.put(结果)
def 从1加到n_多个进程(n):
    进程数量 = int(0.5*multiprocessing.cpu_count())
    import numpy
    节点 = numpy.linspace(0,n,进程数量+1,dtype="int64")
    起点 = list(节点[:-1]+1)
    起点[0]-=1
    终点 = list(节点[1:])
    进程信息 = {"进程函数":[],"参数列表":[],"返回值收集":[]}
    所有进程 = []
    开始时刻 = time.time()
    返回值收集 = multiprocessing.Queue()
    for i in range(进程数量):
        所有进程+=[multiprocessing.Process(target=进程任务,args=(返回值收集,开始时刻,起点[i],终点[i]),name="进程{}".format(i))]
    for i in range(进程数量):
        print("进程{}开始运行".format(i))
        所有进程[i].start()
    for i in range(进程数量):
        所有进程[i].join()
    print("所有进程运行完成")
    最终结果=0
    for i in range(进程数量):
        最终结果 += 返回值收集.get()
    结束时刻 = time.time()
    print("执行完成，最终结果为 {}，用时 {:.2g}s".format(最终结果,结束时刻-开始时刻))



if __name__=="__main__":
    n = int(123456789)
    print("本程序利用计算 1+2+3+...{} 来进行计算".format(n))
    print("单进程运算开始执行\n")
    从1加到n_单进程(n)
    print("结束执行\n\n")
    print("---------------------------------")
    print("两个进程运算开始执行\n")
    从1加到n_两个进程(n)
    print("结束执行\n\n")
    print("---------------------------------")
    print("多个进程运算开始执行\n")
    从1加到n_多个进程(n)
    print("结束执行\n\n")
    pause()