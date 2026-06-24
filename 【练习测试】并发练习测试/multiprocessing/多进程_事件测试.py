# -*- coding: utf-8 -*-
import multiprocessing
import time

def 任务进程(事件对象, 进程名称):
    """
    子进程任务：等待事件触发后执行操作
    """
    print(f"[{进程名称}] 等待事件触发...")
    事件对象.wait()  # 阻塞直到事件被设置为 True
    print(f"[{进程名称}] 事件已触发，开始执行任务！")
    
    # 模拟耗时操作
    for i in range(3):
        print(f"[{进程名称}] 正在工作... ({i+1}/3)")
        time.sleep(1)
    
    print(f"[{进程名称}] 任务完成！")

if __name__ == "__main__":
    # 创建事件对象（初始状态为 False）
    同步事件 = multiprocessing.Event()
    
    # 创建并启动子进程
    子进程 = multiprocessing.Process(
        target=任务进程,
        args=(同步事件, "子进程-1"),
        name="子进程-1"
    )
    子进程.start()
    
    # 主进程操作
    try:
        print("[主进程] 子进程已启动，按回车键触发事件开始任务")
        input()  # 等待用户输入
        
        # 设置事件状态为 True（触发子进程继续执行）
        同步事件.set()
        print("[主进程] 事件已触发，通知子进程开始工作")
        
    except KeyboardInterrupt:
        print("\n[主进程] 用户中断操作")
    
    # 等待子进程结束
    子进程.join()
    print("[主进程] 程序结束")