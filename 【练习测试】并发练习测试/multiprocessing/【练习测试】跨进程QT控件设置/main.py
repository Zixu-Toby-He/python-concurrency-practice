import sys
import os
import multiprocessing as mp
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setMinimumSize(640, 480)
        
    def winIdInt(self):
        """返回窗口ID的整数值"""
        return int(self.winId())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("跨进程图像显示")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建图像显示控件
        self.image_widget = ImageWidget()
        layout.addWidget(self.image_widget)
        
        # 获取窗口ID
        hwnd = self.image_widget.winIdInt()
        print(f"主窗口ID: {hwnd}")
        
        # 启动图像处理进程
        self.start_image_process(hwnd)
    
    def start_image_process(self, hwnd):
        """启动图像处理子进程"""
        script_path = os.path.join(os.path.dirname(__file__), 'image_process.py')
        self.process = mp.Process(
            target=run_image_process,
            args=(hwnd,)
        )
        self.process.daemon = True
        self.process.start()

def run_image_process(hwnd):
    """启动图像处理进程的包装函数"""
    import subprocess
    subprocess.Popen([sys.executable, 'image_process.py', str(hwnd)])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())