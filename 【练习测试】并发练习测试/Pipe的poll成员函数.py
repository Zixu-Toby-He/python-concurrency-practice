import multiprocessing
import time
import random
from datetime import datetime

def sender(conn):
    """发送端：随机间隔发送10条消息"""
    for i in range(10):
        sleep_time = random.uniform(0.7, 1.3)
        time.sleep(sleep_time)
        msg = f"消息{i} (延迟{sleep_time:.2f}s)"
        conn.send(msg)
        print(f"[发送 {datetime.now().strftime('%H:%M:%S.%f')}]", msg)
    conn.send("END")  # 结束标记
    conn.close()

def receiver(conn):
    """接收端：1秒超时检测"""
    count = 0
    while True:
        start_time = time.time()
        poll_ret = conn.poll(timeout=1.0)  # 1秒超时
        data = None
        if poll_ret:
            data = conn.recv()
            elapsed = time.time() - start_time
            if data == "END":
                print("接收完成")
                break
            print(f"poll_ret = {poll_ret}，poll到对象 {repr(data)}，用时{elapsed:.3f}s\n")
            count += 1
        else:
            elapsed = time.time() - start_time
            print(f"poll_ret = {poll_ret}，上回poll到 {repr(data)}，用时{elapsed:.3f}s\n")

    print(f"总计收到 {count} 条消息")

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    
    p_sender = multiprocessing.Process(target=sender, args=(child_conn,))
    p_receiver = multiprocessing.Process(target=receiver, args=(parent_conn,))
    
    p_sender.start()
    p_receiver.start()
    
    p_sender.join()
    p_receiver.join()