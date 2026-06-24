"""
程序功能：
进程1：从0开始每0.3秒将计数+1，
	打印出来，直到100，并将每个5的
	倍数将数字通过管道传输出去
进程2：接收到数字后将接收到的数字打印出来累加。
"""
import time
import multiprocessing

端口1, 端口2 = multiprocessing.Pipe()

def 进程1函数(管道端口):
	i = 0
	while(i<=100):
		print(i)
		time.sleep(0.3)
		i += 1
		if (i%5 == 0):
			管道端口.send(i)
	管道端口.send("end")

def 进程2函数(管道端口):
	和 = 0
	接收值 = None
	while (接收值 != "end"):
		接收值 = 管道端口.recv()
		if (接收值 != "end"):
			和 += 接收值
			print("接收到端口对面数值“{}”，当前和为{}".format(接收值,和))
		else:
			print("端口接收结束")

if __name__=="__main__":
	进程1 = multiprocessing.Process(target = 进程1函数, args=(端口1,))
	进程2 = multiprocessing.Process(target = 进程2函数, args=(端口2,))
	进程1.start()
	进程2.start()
	进程1.join()
	进程2.join()
	print("程序结束")
