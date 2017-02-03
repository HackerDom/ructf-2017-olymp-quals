import time
f = open("PI_source file.gcode","r")
rez = open("Hard.task","w")

for line in f:
    if line[0] == ";":
        pass
    else:
        rez.write(line)

time.sleep(1)
f.close()
        
