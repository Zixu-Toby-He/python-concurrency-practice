import threading
import time

# 创建事件对象（初始状态为 False）
同步事件 = threading.Event()

def 任务线程(事件对象, 线程名称):
    """
    线程任务：等待事件触发后执行操作
    """
    print(f"[{线程名称}] 等待事件触发...")
    事件对象.wait()  # 阻塞直到事件被设置为 True
    print(f"[{线程名称}] 事件已触发，开始执行任务！")
    
    # 模拟耗时操作
    for i in range(3):
        print(f"[{线程名称}] 正在工作... ({i+1}/3)")
        time.sleep(1)
    
    print(f"[{线程名称}] 任务完成！")

if __name__ == "__main__":
    # 创建并启动线程
    线程 = threading.Thread(
        target=任务线程,
        args=(同步事件, "线程-1"),
        name="线程-1"
    )
    线程.start()
    
    # 主线程操作
    try:
        print("[主线程] 线程已启动，按回车键触发事件开始任务")
        input()  # 等待用户输入
        
        # 设置事件状态为 True（触发线程继续执行）
        同步事件.set()
        print("[主线程] 事件已触发，通知线程开始工作")
        
    except KeyboardInterrupt:
        print("\n[主线程] 用户中断操作")
    
    # 等待线程结束
    线程.join()
    print("[主线程] 程序结束")