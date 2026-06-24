import sys
import ctypes
import ctypes.wintypes
import numpy as np
import cv2
import time
from multiprocessing import shared_memory

# Windows API 定义
user32 = ctypes.windll.user32
gdi32  = ctypes.windll.gdi32

# Windows 常量
SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize',           ctypes.c_ulong),
        ('biWidth',          ctypes.c_long),
        ('biHeight',         ctypes.c_long),
        ('biPlanes',         ctypes.c_ushort),
        ('biBitCount',       ctypes.c_ushort),
        ('biCompression',    ctypes.c_ulong),
        ('biSizeImage',      ctypes.c_ulong),
        ('biXPelsPerMeter',  ctypes.c_long),
        ('biYPelsPerMeter',  ctypes.c_long),
        ('biClrUsed',        ctypes.c_ulong),
        ('biClrImportant',   ctypes.c_ulong)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', ctypes.c_ulong * 3)
    ]

def create_shared_memory(size):
    """创建共享内存区域"""
    shm = shared_memory.SharedMemory(create=True, size=size)
    return shm

def draw_image(hwnd, image_ptr, width, height, channels):
    """在目标窗口上绘制图像"""
    # 获取设备上下文
    hdc = user32.GetDC(hwnd)
    if not hdc:
        print("无法获取设备上下文")
        return False
    
    try:
        # 创建内存设备上下文
        mem_hdc = gdi32.CreateCompatibleDC(hdc)
        if not mem_hdc:
            print("无法创建内存DC")
            return False
        
        # 设置位图信息
        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height  # 负高度表示从上到下的位图
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 24 if channels == 3 else 32
        bmi.bmiHeader.biCompression = 0  # BI_RGB
        bmi.bmiHeader.biSizeImage = 0
        
        # 创建DIB段
        ppv_bits = ctypes.POINTER(ctypes.c_ubyte)()
        hbitmap = gdi32.CreateDIBSection(
            mem_hdc, 
            ctypes.byref(bmi), 
            DIB_RGB_COLORS, 
            ctypes.byref(ppv_bits), 
            None, 
            0
        )
        
        if not hbitmap:
            print("无法创建DIB段")
            return False
        
        # 将位图选入内存DC
        old_bitmap = gdi32.SelectObject(mem_hdc, hbitmap)
        
        # 将图像数据复制到DIB
        bytes_per_pixel = 3 if channels == 3 else 4
        bytes_per_row = width * bytes_per_pixel
        total_size = height * bytes_per_row

        # 在draw_image函数中使用指针
        ctypes.memmove(ppv_bits, image_ptr, total_size)
        
        # 获取窗口尺寸
        rect = ctypes.wintypes.RECT()
        user32.GetClientRect(hwnd, ctypes.byref(rect))
        win_width = rect.right - rect.left
        win_height = rect.bottom - rect.top
        
        # 计算缩放比例
        scale_x = win_width / width
        scale_y = win_height / height
        scale = min(scale_x, scale_y)
        
        # 计算目标位置
        target_width = int(width * scale)
        target_height = int(height * scale)
        target_x = (win_width - target_width) // 2
        target_y = (win_height - target_height) // 2
        
        # 执行位块传输
        gdi32.BitBlt(
            hdc, 
            target_x, 
            target_y, 
            target_width, 
            target_height, 
            mem_hdc, 
            0, 
            0, 
            SRCCOPY
        )
        
        # 清理资源
        gdi32.SelectObject(mem_hdc, old_bitmap)
        gdi32.DeleteObject(hbitmap)
        gdi32.DeleteDC(mem_hdc)
        
        return True
    
    finally:
        user32.ReleaseDC(hwnd, hdc)

def main(hwnd):
    """图像处理进程主函数"""
    # 创建测试图像
    width, height = 800, 600
    channels = 3
    image_size = width * height * channels
    
    # 创建共享内存
    shm = create_shared_memory(image_size)
    print(f"共享内存创建: {shm.name}")
    
    # 获取numpy数组视图
    image_np = np.ndarray((height, width, channels), 
                          dtype=np.uint8, 
                          buffer=shm.buf)
    # 获取共享内存的指针
    image_ptr = image_np.ctypes.data_as(ctypes.c_void_p)
    
    frame_count = 0
    last_time = time.time()
    
    try:
        while True:
            # 检查窗口是否仍然存在
            if not user32.IsWindow(hwnd):
                print("目标窗口已关闭")
                break
            ctypes.memset(
                image_np.ctypes.data_as(ctypes.c_void_p),
                0,
                image_np.nbytes
            )
            # 生成测试图像（实际应用中可替换为真实图像源）
            cv2.circle(image_np, 
                      (int(width/2 + 200 * np.sin(frame_count * 0.1)), 
                      int(height/2)), 
                      int(100 + 80 * np.cos(frame_count * 0.05)), 
                      (0, 255 * np.abs(np.sin(frame_count * 0.02)), 
                      255 * np.abs(np.cos(frame_count * 0.03))), 
                      -1)
            
            #cv2.imshow("image_np",image_np)
            #cv2.waitKey()
            # 绘制图像到目标窗口
            success = draw_image(hwnd, image_ptr, width, height, channels)
            
            if not success:
                print("绘图失败")
                break
            
            # 计算帧率
            frame_count += 1
            current_time = time.time()
            if current_time - last_time >= 1.0:
                fps = frame_count / (current_time - last_time)
                print(f"帧率: {fps:.1f} FPS")
                frame_count = 0
                last_time = current_time
            
            time.sleep(0.01)  # 控制帧率
    
    finally:
        # 清理资源
        shm.close()
        shm.unlink()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供窗口句柄参数")
        sys.exit(1)
    
    try:
        hwnd = int(sys.argv[1])
        print(f"图像进程启动，目标窗口ID: {hwnd}")
        main(hwnd)
    except Exception as e:
        print("发生错误:")
        import traceback
        traceback.print_exc()