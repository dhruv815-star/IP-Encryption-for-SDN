import subprocess
import csv

#class switch comprising of the attributes of switches
class switch:
    def __init__(self,mode):
        self.mode = mode
        if mode=='e':
            proc1 = subprocess.run(['python', 'encrypt.py', 'data.csv', 'data2.csv', '1', '2', mode], shell=True)
        elif mode=='d':
            proc2 = subprocess.run(['python', 'encrypt.py', 'data2.csv', 'data3.csv', '1', '2', mode], shell=True)
        else:
            print("Enter a valid mode")

    def path_enc(self):
        with open('data2.csv', 'r') as csvfile:
            index = []
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                flag=row[0]
                sw = switch_in(flag)
                index.append(row[0])

class switch_in:
    def __init__(self,code):
        self.code=code
        print("<----------  Via path-{}  ------------->".format(code))
        if(code=='a'):
            s2=switch2()
            s3=switch3()
            s4=switch4()
        elif(code=='b'):
            s2=switch2()
            s4=switch4()
        elif(code=='c'):
            s3=switch3()
            s4=switch4()
        elif(code=='d'):
            s4=switch4()
        else:
            print("NONE")
        
        
class switch2:
    def __init__(self):
        print("Packet recieved by switch-2")
        print("Packet transmitted by switch-2")

class switch3:
    def __init__(self):
        print("Packet recieved by switch-3")
        print("Packet transmitted by switch-3")

class switch4:
    def __init__(self):
        s = switch('d')
        print("Packet received by switch-4")
        print("Broadcasted the following ip_addresses to gateway")
        with open('data3.csv', 'r') as cfile:
            reader = csv.reader(cfile)
            for row in reader:
                print(row)

if __name__ == '__main__':
    s1 = switch('e')
    s1.path_enc()