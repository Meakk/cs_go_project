import multiprocessing
import time

def prnt_cu(n):
    for i in range(13):     
        n = n * n * n 
    print("done")

def test(n):
    for i in range(12):   
        c = n + i  
        print("call for process")
        proc1 = multiprocessing.Process(target=prnt_cu, args=(5, ))
        # Initiating process 1
        proc1.start()
    

if __name__ == "__main__":
    start = time.time()
    # creating multiple processes
    test(5)
    end = time.time()
    print("Time spent Multiprocessing:",end - start,"s")
    start = time.time()
    for i in range(12):
        prnt_cu(5)
    end = time.time()
    print("Time spent :",end - start,"s")