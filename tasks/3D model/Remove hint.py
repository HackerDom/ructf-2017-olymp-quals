#file = "Hard"
file = "Easy" 

f = open(file+"_Task.gcode","r")
rez = open(file+".task","w")

for line in f:
    if line[0] == ";":
        pass
    else:
        rez.write(line)
        
