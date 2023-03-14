'''多线程一般的实现方式'''
import threading
thread_obj = threading.Thread(group= None, target = None, name = None, args = ('...','...'),kwargs = {'A': 0}, name = '...')
#group:暂无可用，未来功能的预留参数
#target:执行的目标任务名
#args:以元组的方式给执行任务传参
#kwargs：以字典的方式给执行任务传参
#name：线程名，一般不用设置


'''范例'''
import time
import threading

def song(a,b,c):
	print(a, b, c)
	for i in range(5):
		print("song")
		time.sleep(1)

def dance(d,e,f):
	print(d, e, f)
	for i in range(5):
		print("dance")
		time.sleep(1)

if __name__ == "__main__":
	threading.Thread(target=song,args=(1,2,3)).start()
	threading.Thread(target=dance,args=(4,5,6)).start()


