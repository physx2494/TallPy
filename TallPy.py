from xml.etree import ElementTree as ET
import sys


##Validation if no intergers are inputed

def A():
    while True:
        A.x = input('Enter party name: ')
        if A.x.isdigit() == True:
            print('Please enter a name.')
            continue
        else:
            return A.x
            break

'''def main_loop(to_search, blah):
    initialize_x(to_search)
'''

'''def initialize_x(value)
    x = value
'''
#Initialization of ElementTree and Finding the list/numbers of each Tag
def B():
    tree = ET.parse('Bills.xml')
    root = tree.getroot()
    B.billfixed = tree.findall('BILLFIXED')
    B.billcl = tree.findall('BILLCL')
    B.billdue = tree.findall('BILLDUE')
    B.billoverdue = tree.findall('BILLOVERDUE')

def C():
    y=A.x
    #Itering and ziping the orphaned childs
    for fixed, cl, due, overdue in zip(B.billfixed, B.billcl, B.billdue, B.billoverdue):
        #Getting it all lower case and then comparing
        if y.lower() == fixed.find('BILLPARTY').text.lower():

            date = fixed.find('BILLDATE').text
            ref= fixed.find('BILLREF').text
            party = fixed.find('BILLPARTY').text

            print(' * [Inv # {}] [Date {}] [Amt {}] [Due date {}] [Overdue by {} days]'.format(
            ref, date, cl.text, due.text, overdue.text
    ))
            print('******************************************************************')
        else:
            print('Party name not found!')
            sys.exit()

if __name__ == '__main__':
    A()
    B()
    C()