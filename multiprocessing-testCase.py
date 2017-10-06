import multiprocessing as mp
import os
import time

def findFactors(data):
    #print(mp.current_process())
    num,start,end = data
    print("checking from {} to {}".format(start,end))
    factors = []
    for i in range(start, end):
        if num%i ==0:
            factors.append(i)
    if len(factors)>0:
        print(factors)
    return factors
    
if __name__ == "__main__":
    startTime = time.time()
    #maxNum = 12345654321
    maxNum = 1234567890
    workSize = maxNum//20
    
    numWorkers = mp.cpu_count()
    data = []
    
    for start in range(2, maxNum//2, workSize):
        data.append((maxNum, start, start+workSize))
    
    numChunks = len(data)
    print(numChunks, "elements")
    print("You have 5 seconds to cancel before all hell breaks loose.")
    time.sleep(5)
    
    factors = []
    
    pool = mp.Pool(numWorkers)
    for factorList in pool.map(findFactors, data):
        for factor in factorList:
            factors.append(factor)
    

    endTime = time.time()
    
    print(factors)
    seconds = endTime - startTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    print("Runtime:", "{} : {} : {}".format(h,m,s))
# 12.58 seconds for 123456789
# 1 min 15.36 sec for 1234567890
        
    
    
    