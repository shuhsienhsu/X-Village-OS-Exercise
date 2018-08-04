import numpy as np
import threading
import multiprocessing
import time

def thread_func(matA, matB, result, row):
    result[row] = np.matmul(matA, matB)

#@profile
def thread_func_02(matA, matB, result, rows, i):
    for j in range(rows):
        result[i * rows + j] = np.matmul(matA[j], matB)

#@profile
def multithread_func(matA, matB, result_queue, i):
    result_queue.put((np.matmul(matA, matB), i))
    #result_queue.put(np.matmul(matA, matB))
    #index_queue.put(i)

def main():
    matA = np.random.randint(10, size = (1000, 1000))
    matB = np.random.randint(10, size = (1000, 1000))
    result = np.zeros((matA.shape[0], matB.shape[1]))
    result_multi = np.zeros((matA.shape[0], matB.shape[1]))
    result_multi02 = np.zeros((matA.shape[0], matB.shape[1]))

    matA_temp = []
    threads = []
    thread_num = 10
    
    start_time = time.time()
    #for i in range(matA.shape[0]):
        #thread = threading.Thread(target = thread_func, args = (matA[i], matB, result, i))
        #threads.append(thread)
    print(matA.shape[0] // thread_num)
    #print(matA[0:(matA.shape[0] // thread_num * (i + 1)), 0:matA.shape[1]])

    for i in range(thread_num):
        matA_temp = matA[matA.shape[0] // thread_num * i : matA.shape[0] // thread_num * (i + 1), 0:matA.shape[1]]
        thread = threading.Thread(target = thread_func_02, args = (matA_temp, matB, result, matA.shape[0] // thread_num, i))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    print('Time elapsed:', end_time - start_time)
    print('Answer(thread) is correct:', np.all(np.matmul(matA, matB) == result))

    result_queue = multiprocessing.Manager().Queue()
    #index_queue = multiprocessing.Manager().Queue()
    
    start_time = time.time()
    jobs = []
    #for i in range(matA.shape[0]):
        #process = multiprocessing.Process(target = multithread_func, args = (matA[i], matB, result_queue))
        #jobs.append(process)
    for i in range(thread_num):
        matA_temp = matA[matA.shape[0] // thread_num * i : matA.shape[0] // thread_num * (i + 1), 0:matA.shape[1]]
        process = multiprocessing.Process(target = multithread_func, args = (matA_temp, matB, result_queue, i))
        #temp = result_queue.get()
        #print(temp)
        #for j in range(matA.shape[0] // thread_num):
            #result_multi[i * matA.shape[0] // thread_num + j] = temp[j]
        jobs.append(process)
    for process in jobs:
        process.start()
    for process in jobs:
        process.join()

    while not result_queue.empty():
        theresult = result_queue.get()
        #index = index_queue.get()
        index = theresult[1]
        theresult = theresult[0]
        for i in range(matA.shape[0]):
            if(index == i):
                for j in range(matA.shape[0] // thread_num):
                    result_multi[i * (matA.shape[0] // thread_num) + j] = theresult[j]

    end_time = time.time()
    print('Time elapsed:', end_time - start_time)
    print('Answer(process) is correct:', np.all(np.matmul(matA, matB) == result_multi))

    # Generate random matrix and result matrix
    result_normal = np.zeros((matA.shape[0], matB.shape[1]))
    
    start_time = time.time()
    for row in range(0, matA.shape[0]):
        result_normal[row] = np.matmul(matA[row], matB)
    end_time = time.time()

    # Compare with numpy's multiplication result
    print('Time elapsed:', end_time - start_time)
    print('Answer(normal) is correct:', np.all(np.matmul(matA, matB) == result_normal))
    
if __name__ == "__main__":
    main()