def writef(strings):
    f = open("돈목록.txt",'w')
    f.write(strings + '\n')
    f.close()

def readf():
    f = open("돈목록.txt", 'r')
    lines = f.readlines()
    f.close()
    return lines