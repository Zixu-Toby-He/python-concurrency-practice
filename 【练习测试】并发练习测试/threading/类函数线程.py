import os
import time
import threading

class A:
	a=5
	def f():
		time.sleep(3)
		print(A.a)

def f():
	global A
	time.sleep(1)
	A.a = 3
	
if __name__=="__main__":
	t1 = threading.Thread(target=A.f)
	t2 = threading.Thread(target=f)
	t1.start()
	t2.start()
	t2.join()
	t1.join()
	print()
	os.system("pause")