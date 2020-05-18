import numpy as np
from statistics import median
def npsearch(data,x=150,y=256):
    a= data.tolist()
    pattern = range(x,y)
    count = 0
    location = []
    for t in pattern:
        for i in range(len(a)):
            if t in a[i]:
                while True:
                    try:
                        location.append([i,a[i].index(t)])
                        a[i][a[i].index(t)]=-1
                        count+=1
                    except:
                        break
    location  = np.array(location)
    return location , count, (int(median(location[:,0])),int(median(location[:,1])))
"""if __name__ == '__main__':
    data = np.array([[1,2,3,4,5],
                    [150,150,200,1,2,3],
                    [6,4,5,8,9]])
    location,count, median = npsearch(data)
    
    print('locations',location)
    print('count',count)
    print('median',median)
"""
