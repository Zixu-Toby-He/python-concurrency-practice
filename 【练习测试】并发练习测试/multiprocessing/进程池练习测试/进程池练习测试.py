from locale import currency
import os
import time
import concurrent.futures
import moviepy.editor

待转化存储目录 = "待转化文件"
已转化存储目录 = "已转化文件"
所有待转化文件名 = os.listdir(待转化存储目录)

def 任务_转化为音频(文件名):
    输入文件路径 = os.path.join(待转化存储目录,文件名)
    输出文件路径 = os.path.join(已转化存储目录,文件名[:-1]+"3")
    输入视频 = moviepy.editor.VideoFileClip(输入文件路径)
    输出音频 = 输入视频.audio
    输出音频.write_audiofile(输出文件路径)
    输入视频.close()

if __name__=="__main__":
    进程池 = concurrent.futures.ProcessPoolExecutor(8)
    print("开始转化")
    开始时刻 = time.time()
    所有转化任务 = []
    
    for 文件名 in 所有待转化文件名:
        任务 = 进程池.submit(任务_转化为音频, 文件名)
        所有转化任务.append(任务)
    进程池.shutdown(True)
    结束时刻 = time.time()
    print("转化完成，用时{} s".format(结束时刻-开始时刻))
    '''
    线程池 = concurrent.futures.ThreadPoolExecutor(100)
    
    
    线程池.shutdown(True)
    concurrent.futures.wait(所有转化任务)
    
    '''