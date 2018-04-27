
def loadFloatArray(name, length):
    
    file = open(name + '.txt', 'r')
    array = []
    for i in range(length):
        array.append(float(file.readline()))
    return array

def loadFloatMatrix(name, length0, length1):
    
    file = open(name + '.txt', 'r')
    array = []
    for i in range(length0):
        temp = []
        for j in range(length1):
            temp.append(float(file.readline()))
        array.append(temp)
    return array

#