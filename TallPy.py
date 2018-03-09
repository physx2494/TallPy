from xml.etree import ElementTree as ET
import sys
import urllib.request



##Validation if no intergers are inputed
while True:
    x = input('Enter party name: ')
    if x.isdigit() == True:
        print('Please enter a name.')
        continue
    else:
        break

#Initialization of ElementTree
tree = ET.parse('Bills.xml')
root = tree.getroot()

#Finding the list/numbers of each Tag
billfixed = tree.findall('BILLFIXED')
billcl = tree.findall('BILLCL')
billdue = tree.findall('BILLDUE')
billoverdue = tree.findall('BILLOVERDUE')

#Iterating and ziping the orphaned childs
for fixed, cl, due, overdue in zip(billfixed, billcl, billdue, billoverdue):
    #Getting it all lower case and then comparing
    if x.lower() == fixed.find('BILLPARTY').text.lower():

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

