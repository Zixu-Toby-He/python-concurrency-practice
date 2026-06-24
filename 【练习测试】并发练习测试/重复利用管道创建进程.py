import os
import multiprocessing

def f(s,p):
	print(s + ": " + p.recv())
	
if __name__=="__main__":
	pp_m, pp_s = multiprocessing.Pipe()
	p = multiprocessing.Process(
		target = f,
		args  = ("p", pp_s,)
	)
	p.start()
	pp_m.send("hello")
	pp_m.send("hi")
	p = multiprocessing.Process(
		target = f,
		args  = ("p", pp_s,)
	)
	p.start()
	p.join()
	p.join()

	os.system("pause")