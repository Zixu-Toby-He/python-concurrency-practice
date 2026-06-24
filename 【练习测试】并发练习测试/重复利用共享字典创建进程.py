import os
import multiprocessing

def f(d):
	print(d)
	d["hello"] += " hello"
	
if __name__=="__main__":
	with multiprocessing.Manager() as m:
		d = m.dict()
		d["hello"] = "hello"
		p = multiprocessing.Process(
			target = f,
			args  = (d,)
		)
		p.start()
		p.join()
		p = multiprocessing.Process(
			target = f,
			args  = (d,)
		)
		p.start()
		p.join()

	os.system("pause")