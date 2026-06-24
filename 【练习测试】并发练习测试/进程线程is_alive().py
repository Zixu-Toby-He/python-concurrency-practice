import os
import time
import threading
import multiprocessing

def f(s = ""):
	time.sleep(3)
	print(s)
	
if __name__=="__main__":
	p = multiprocessing.Process(
		target = f,
	)
	print("O:", p.is_alive())
	p.start()
	for i in range(10):
		print("A:", p.is_alive())
		time.sleep(0.5)
	p.join()
	print("B:", p.is_alive())
	print()
	print()
	print()
	t = threading.Thread(target = f)
	print("O:", t.is_alive())
	t.start()
	for i in range(10):
		print("A:", t.is_alive())
		time.sleep(0.5)
	t.join()
	print("B:", t.is_alive())

	os.system("pause")