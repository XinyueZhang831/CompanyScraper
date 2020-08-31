import glob
import os

class CompNum:
    def __init__(self, update=False, num = 0):
        self.up = update
        self.n = num

    def create_file(self):
        if len(glob.glob(os.getcwd()+'/'+'comp_num.txt'))==0:
            file =os.getcwd()+'/'+'comp_num.txt'
            with open(file, 'w') as filetowrite:
                filetowrite.write(str(int(self.n)))
            filetowrite.close()

    def overwrite_file(self):
        file = os.getcwd() + '/' + 'comp_num.txt'
        with open(file, 'w') as filetowrite:
            filetowrite.write(str(int(self.n)))
        filetowrite.close()


    def give_num(self):
        file = open(os.getcwd()+'/'+'comp_num.txt', 'r')
        comp = file.readline()
        if self.up == True:
            CompNum.write_num(self)
        if type(comp) != str:
            comp = str(comp)
        return int(comp)

    def write_num(self):
        file = os.getcwd()+'/'+'comp_num.txt'
        with open(file, 'w') as filetowrite:
            filetowrite.write(str(int(self.n) + 1))
        filetowrite.close()
