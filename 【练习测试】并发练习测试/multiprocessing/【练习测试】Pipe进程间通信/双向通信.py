"""
程序功能：
	石头剪刀布
"""

import random
import multiprocessing
import os
import time

裁判电脑端口_裁判, 裁判电脑端口_电脑 = multiprocessing.Pipe()
裁判玩家端口_裁判, 裁判玩家端口_玩家 = multiprocessing.Pipe()
输入端口_主进程, 输入端口_玩家  = multiprocessing.Pipe()

def 解析手势(输入内容):
	try:
		输入 = int(输入内容)
	except:
		return None
	if 输入 in range(0,3):
		return 输入
	else:
		None

def 判断输赢(手势1, 手势2):
	if (手势1 == 手势2):
		return 0
	elif(手势1 - 手势2 == -1):
		return 1
	elif((手势1,手势2) == (2,0)):
		return 1
	else:
		return -1

def 输赢打印(用户,输赢):
	match(输赢):
		case (-1):
			print(f"{用户}：我认输")
		case (0):
			print(f"{用户}：我不赢不输")
		case (1):
			print(f"{用户}：我赢了")

def 电脑(裁判端口):
	while(True):
		手势 = random.randint(0,3)
		裁判端口.send(手势)
		输赢 = 裁判端口.recv()
		输赢打印("电脑",输赢)

def 玩家(裁判端口,输入端口):
	while(True):
		手势 = 输入端口.recv()
		裁判端口.send(手势)
		输赢 = 裁判端口.recv()
		输赢打印("玩家",输赢)

def 裁判(电脑端口,玩家端口):
	while(True):
		电脑手势 = 电脑端口.recv()
		玩家手势 = 玩家端口.recv()
		输赢判断 = 判断输赢(玩家手势,电脑手势)
		电脑端口.send( 输赢判断)
		玩家端口.send(-输赢判断)

def main():
	电脑进程 = multiprocessing.Process(target = 电脑, args=(裁判电脑端口_电脑,))
	玩家进程 = multiprocessing.Process(target = 玩家, args=(裁判玩家端口_玩家,输入端口_玩家))
	裁判进程 = multiprocessing.Process(target = 裁判, args=(裁判电脑端口_裁判, 裁判玩家端口_裁判,))
	电脑进程.start()
	玩家进程.start()
	裁判进程.start()
	while(True):
		输入内容 = input("请输入手势（0：石头，1：剪刀，2：布）：")
		解析结果 = 解析手势(输入内容)
		if (解析结果!=None):
			输入端口_主进程.send(解析结果)
	电脑进程.join()
	玩家进程.join()
	裁判进程.join()

if __name__=="__main__":
	main()