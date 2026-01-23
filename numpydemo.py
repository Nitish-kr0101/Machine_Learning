import numpy as np

list = np.array([10, 20, 30, 40, "sd", True])
list1 = np.array([10, 20, 30, 40, 50])
list2 = np.array([60, 70, 80, 90, 100])

#print(type(list[1]))
#print(list[-20])   #error: index out of range

print(list1+list2)  

print(np.sum(list1))

print(np.isin(50, list1))

arr2d = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print(arr2d)

#resize array
arr2d.resize(4,3)   

#reshape array
arr2d = arr2d.reshape(2,6)
print(f"reshape",arr2d)


