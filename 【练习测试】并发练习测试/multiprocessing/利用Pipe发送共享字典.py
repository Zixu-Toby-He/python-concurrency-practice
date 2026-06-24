import multiprocessing
import threading
import time

def process1_task(pipe_end):
    """第一个进程的任务函数"""
    # 创建共享字典
    # with multiprocessing.Manager() as manager:
    #     ...
    # 等价于
    # manager = multiprocessing.Manager()
    # ...
    # manager.shutdown()
    with multiprocessing.Manager() as manager:
        srd = manager.dict()
        print(f"进程1 [PID:{multiprocessing.current_process().pid}] 创建共享字典: {srd}")
        
        # 创建并启动子线程
        def thread_task():
            time.sleep(1.7)
            print(f"子线程 [TID:{threading.get_ident()}] 发送共享字典")
            pipe_end.send(srd)  # 发送共享字典
        
        t = threading.Thread(target=thread_task)
        t.start()
        
        # 主线程监控共享字典状态
        start_time = time.time()
        while time.time() - start_time < 5:
            print(f"进程1主线程 [TID:{threading.get_ident()}] 监控: srd = {dict(srd)}")
            time.sleep(0.5)
        
        t.join()  # 等待子线程结束
        print("进程1结束")

def process2_task(pipe_end):
    """第二个进程的任务函数"""
    print(f"进程2 [PID:{multiprocessing.current_process().pid}] 等待接收共享字典...")
    srd = pipe_end.recv()  # 阻塞等待接收共享字典
    print(f"进程2收到共享字典: {srd}")
    
    # 修改共享字典
    srd["greet"] = "hello"
    print(f"进程2修改后: srd = {dict(srd)}")

if __name__ == "__main__":
    # 创建管道
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # 创建并启动两个进程
    p1 = multiprocessing.Process(target=process1_task, args=(parent_conn,))
    p2 = multiprocessing.Process(target=process2_task, args=(child_conn,))
    
    p1.start()
    p2.start()
    
    # 等待进程结束
    p1.join()
    p2.join()
    
    print("所有进程结束")