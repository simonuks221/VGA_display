import math

f = open("sine.txt", "w")


arrayus = [1, 2, 3]


for i in range(0, 360):
    r = math.sin(i * math.pi / 180)*100
    f.write(str(int(r)) + '\n')

#f.write("Now the file has more content!")
f.close()
