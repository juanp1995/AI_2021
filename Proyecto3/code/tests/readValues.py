x = open('../x.txt', 'r')
f = open('../f.txt', 'r')

values = []

while True:
    xValue, fValue = x.readline(), f.readline()
    if not xValue:
        break
    
    newVal = [int(xValue, 10), int(fValue, 10)]
    values.append(newVal)

x.close()
f.close()

print(values)