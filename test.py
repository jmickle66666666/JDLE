import sys
f = open("output.txt","w")
f.write(str(sys.argv))
f.close()