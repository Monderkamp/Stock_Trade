import matplotlib.pyplot as plt
import numpy as np

#Zeit,TSLA,AAPL,EA,GOOG

S = "2019_Feb_27_stock_data.txt"

def printlines(A):
  for line in A:
    print(line)

def get_data(S):
  A = []
  with open(S,'r') as f:
    for line in f:
      A.append(f.readlines())
  A=A[0]
  A = np.array(A)
  B = []
  T = []
  for idx,item in enumerate(A):
    line = item.split(' ')
    T.append(line[3])
    B.append(line[4])

  for idx,item in enumerate(B):
    B[idx] = B[idx].split(',')
    for i,val in enumerate(B[idx]):
      B[idx][i] = float(B[idx][i])
  B = np.array(B)
  B =B[:,1:]
  for idx,item in enumerate(T):
    T[idx] = float(T[idx][0:2]) + float(T[idx][3:5])/60 + float(T[idx][6:])/3600
  T = np.array(T)
  return [T,B]
[T,D] = get_data(S)  
#printlines(T)
#printlines(D)
#Zeit,TSLA,AAPL,EA,GOOG

plt.subplot(2,2,1)
plt.plot(T,D[:,0])
plt.legend(['TSLA'])
plt.xlabel('T in hours')
plt.ylabel('Stock value in \$')


plt.subplot(2,2,2)
plt.plot(T,D[:,1])
plt.legend(['AAPL'])
plt.xlabel('T in hours')
plt.ylabel('Stock value in \$')


plt.subplot(2,2,3)
plt.plot(T,D[:,2])
plt.legend(['EA'])
plt.xlabel('T in hours')
plt.ylabel('Stock value in \$')


plt.subplot(2,2,4)
plt.plot(T,D[:,3])
plt.legend(['GOOG'])
plt.xlabel('T in hours')
plt.ylabel('Stock value in \$')
plt.show()

