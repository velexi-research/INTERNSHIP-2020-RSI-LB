import numpy as np
samples = np.loadtxt("../data/data_bin_4.csv")
ls = []
rs = []
s1 = []
s2 = []
s3 = []
s4 = []
ns = []
for i in range(1000):
    ls.append(str(320*i)+"u,1")
    ls.append(str(320*i+1)+"u,0")
    ls.append(str(320*i+310)+"u,0")
    ls.append(str(320*i+311)+"u,1")
    ns.append(str(320*i+6)+"u,0")
    ns.append(str(320*i+7)+"u,1")
    ns.append(str(320*i+310)+"u,1")
    ns.append(str(320*i+311)+"u,0")
    rs.append(str(320*i+1)+"u,0")
    rs.append(str(320*i+2)+"u,1")
    rs.append(str(320*i+5)+"u,1")
    rs.append(str(320*i+6)+"u,0")
    s1.append(str(320*i+1)+"u,"+str(samples[i][0]))
    s1.append(str(320*i+320)+"u,"+str(samples[i][0]))
    s2.append(str(320*i+1)+"u,"+str(samples[i][1]))
    s2.append(str(320*i+320)+"u,"+str(samples[i][1]))
    s3.append(str(320*i+1)+"u,"+str(samples[i][2]))
    s3.append(str(320*i+320)+"u,"+str(samples[i][2]))
    s4.append(str(320*i+1)+"u,"+str(samples[i][3]))
    s4.append(str(320*i+320)+"u,"+str(samples[i][3]))
f = open("../data/latch.txt","w+")
f.writelines([i+"\n" for i in ls])
f.close()
f = open("../data/reset.txt","w+")
f.writelines([i+"\n" for i in rs])
f.close()
f = open("../data/in1.txt","w+")
f.writelines([i+"\n" for i in s1])
f.close()
f = open("../data/in2.txt","w+")
f.writelines([i+"\n" for i in s2])
f.close()
f = open("../data/in3.txt","w+")
f.writelines([i+"\n" for i in s3])
f.close()
f = open("../data/in4.txt","w+")
f.writelines([i+"\n" for i in s4])
f.close()
f = open("../data/norm_latch.txt","w+")
f.writelines([i+"\n" for i in ns])
f.close()

from random import random
from math import sqrt
icstr=""
for i in range(4):
    icstr+=".ic"
    r1=random()
    r2=random()
    r3=random()
    r4=random()
    rs = [r1,r2,r3,r4]
    a = sqrt(r1*r1+r2*r2+r3*r3+r4*r4)
    for j in range(4):
        icstr+=" V(h"+str(i+1)+str(j+1)+":intbias)="+str(rs[j]/a)
    icstr+="\n"
print(icstr)