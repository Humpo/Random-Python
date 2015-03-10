#!/usr/bin/python
from pprint import PrettyPrinter
from urllib.request import Request, urlopen
import re
class fakeInfo():
        def __init__(self):
                '''
                Object designed so future functions can be added for further modularity of data recieved
                '''
                try:self.info = self.html_doc_return()  # raw html doc to find vals
                except:
                        self.user_dict={}
                        print("Connection Issues")
                try:
                        self.user_dict = self.bs4_info_filter(self.info)  # filters html using regular expressions  # user_dict = info_filter2(info)                       
                except ImportError:
                        self.user_dict = self.nobs4_info_filter(self.info)  # filters html using regular expressions  # user_dict = info_filter2(info)
        def bs4_info_filter(self,info):
                '''Uses beautiful soup to manually extract information from tags generated on the webpage'''
                from bs4 import BeautifulSoup
                info_dict={}
                htmlsoup = BeautifulSoup(info)
                info_list = []
                for i in re.findall('>[^^]*?<',str(htmlsoup.find(class_='info')),re.MULTILINE):
                        check = i.strip('<>').strip().split()
                        if check == '' or check == []:None
                        else:info_list.append(check)
                info_dict['Last Name'] = info_list[0][2]
                info_dict['Middle Initial'] = info_list[0][1].strip(' .')
                info_dict['First Name'] = info_list[0][0]

                info_dict['Address'] = ' '.join(info_list[1])

                info_dict['City'] = info_list[2][0]
                info_dict['State'] = info_list[2][1]
                info_dict['Zip'] = info_list[2][2]

                info_dict['Phone'] = info_list[8][0]

                info_dict['Email'] = info_list[10][0]
                
                info_dict['UserName'] = info_list[14][0]

                info_dict['Password'] = info_list[16][0]

                info_dict["Mother's Maiden Name"] = info_list[18][0]

                info_dict['Birthday'] = {'Day':info_list[20][1].strip(','),'Month':info_list[20][0],'Year':info_list[20][2]}

                info_dict['Age'] = info_list[20][3].strip('(')

                info_dict['Credit Card'] = {'Card':info_list[21][0],'Number':''.join(info_list[22]),'Expiration':info_list[24][0],'CVC2':info_list[26][0]}

                info_dict['SSN'] = info_list[28][0]

                info_dict['Color'] = info_list[33][0]

                info_dict['Occupation'] = ' '.join(info_list[35])

                info_dict['Company'] = ' '.join(info_list[37])

                info_dict['Website'] = info_list[39][0]

                info_dict['Vehicle'] = ' '.join(info_list[41])

                info_dict['Blood Type'] = info_list[45][0]

                info_dict['Weight'] = {'Pounds':info_list[47][0],'Kilograms':info_list[47][2].strip('(')}

                info_dict['Height'] = {'Feet':info_list[49][0]+info_list[49][1],'Centimeters':info_list[49][2].strip('(')}

                info_dict['GUID'] = info_list[51][0]

                info_dict['Geo-coordinates'] = (info_list[53][0],info_list[53][1])
                return info_dict
        def data_print(self):
                '''prints data nicely'''
                out = PrettyPrinter(indent=4)
                out.pprint(self.user_dict)
        def html_doc_return(self):
                '''grabs the html info from website'''
                url = 'http://www.fakenamegenerator.com'  # <----url to get info
                req = Request(url, headers={'User-Agent': "Magic Browser"})  # Allows python to return vals
                con = urlopen(req)  # opens the url to be read
                return (con.read())  # returns all html docs
        def nobs4_info_filter(self, info):
                '''if user does not have bs4 WARNING WILL NOT DISPLAY AS MUCH INFORMATION'''
                info_dict = {}

                ##Name##
                Name = str(re.findall(b'class=\"address\">[^^]*?</h3>', info, re.MULTILINE))
                Name = str(re.findall(r'<h3>[^^]*?</h3>', Name, re.MULTILINE))
                Name = re.sub(r'<h3>', '', Name)
                Name = re.sub(r'</h3>', '', Name)
                Name = Name.strip('[]\'')
                Name = re.split(r'\s', Name)

                info_dict['Last Name'] = Name[2]

                info_dict['Middle Initial'] = Name[1].strip(' .')

                info_dict['First Name'] = Name[0]
                ##Name##

                ##Phone##
                info_dict['Phone'] = str(re.findall(b'\d\d\d-\d\d\d-\d\d\d\d', info, re.MULTILINE))
                info_dict['Phone'] = info_dict['Phone'].strip('[]\' b')
                ##Phone##

                ##username##
                info_dict['Username'] = str(re.findall(b'Username:</li>&nbsp;[^^]*?</li><br/>', info, re.MULTILINE))
                info_dict['Username'] = str(re.findall('<li>[^^]*?</li>', info_dict['Username'], re.MULTILINE))
                info_dict['Username'] = re.sub(r'<li>', '', info_dict['Username'])
                info_dict['Username'] = re.sub(r'</li>', '', info_dict['Username'])
                info_dict['Username'] = info_dict['Username'].strip('[]\'')
                ##username##

                ##Password##
                Password = str(re.findall(b'Password:</li>&nbsp;[^^]*?</li><br/>', info, re.MULTILINE))
                Password = str(re.findall('<li>[^^]*?</li>', Password, re.MULTILINE))
                Password = re.sub(r'<li>', '', Password)
                Password = re.sub(r'</li>', '', Password)
                info_dict['Password'] = Password.strip('[]\'')
                ##Password##

                ##address##
                info_dict['Address'] = str(re.findall(b'class=\"adr\">[^^]*?</d', info, re.MULTILINE))
                info_dict['Address'] = str(re.findall(r'\d[^^]*?<br', info_dict['Address'], re.MULTILINE))
                info_dict['Address'] = re.sub(r'<br', '', info_dict['Address'])
                info_dict['Address'] = info_dict['Address'].strip('[]\'')
                ##address##

                ##State##  #INITIALS
                info_dict['State'] = str(re.findall(b'class=\"adr\">[^^]*?</d', info, re.MULTILINE))
                info_dict['State'] = str(re.findall(r',\s..\s', info_dict['State'], re.MULTILINE))
                info_dict['State'] = info_dict['State'].strip('[]\', ')
                ##State##

                ##City##
                City = str(re.findall(b'class=\"adr\">[^^]*?</d', info, re.MULTILINE))
                City = str(re.findall(r'<br/>[^^]*?\s', City, re.MULTILINE))
                City = re.sub(r'<br/>', '', City)
                info_dict['City'] = City.strip('[]\', ')
                ##City##

                ##Postal Code##
                info_dict['Postal Code'] = str(re.findall(b'class=\"adr\">[^^]*?</d', info, re.MULTILINE))
                info_dict['Postal Code'] = str(re.findall(r',\s..\s[^^]*?\s\s', info_dict['Postal Code'], re.MULTILINE))
                info_dict['Postal Code'] = re.sub(r'[A-Z][A-Z]\s', '', info_dict['Postal Code'])
                info_dict['Postal Code'] = info_dict['Postal Code'].strip('[]\', ')
                ##Postal Code##

                ##Birthday##
                Birthday = str(re.findall(b'<li class="bday">[^^]*?</li>', info, re.MULTILINE))
                Birthday = re.sub(r'<li class="bday">', '', Birthday)
                Birthday = re.sub(r'</li>', '', Birthday)
                Birthday = re.split(r'\s', Birthday)

                info_dict['Birthday'] = {}
                info_dict['Birthday']['Month'] = Birthday[0].strip('[],b\'')
                info_dict['Birthday']['Day'] = Birthday[1].strip(', ')
                info_dict['Birthday']['Year'] = Birthday[2].strip(', ')

                info_dict['Age'] = Birthday[3][1:3]
                ##Birthday##

                ##Visa##
                Visa = str(re.findall(b'\d\d\d\d\s\d\d\d\d\s\d\d\d\d\s\d\d\d\d', info, re.MULTILINE))
                info_dict['Visa'] = Visa.strip('[]\', b')
                ##Visa##

                ##Email##
                info_dict['Email'] = {}
                Email = str(re.findall(b'class=\"email\">[^^]*?</span>', info, re.MULTILINE))
                Email = re.sub(r'class=\"email\"><span class=\"value\">', '', Email)
                Email = re.sub(r'</span>', '', Email)
                Email = Email.strip('[]\', b')
                info_dict['Email']['whole'] = Email
                Email = re.split(r'@', Email)
                info_dict['Email']['Name'] = Email[0]
                info_dict['Email']['Address'] = Email[1]
                ##Email##
                
                return (info_dict)
person1 = fakeInfo()
person1.data_print()
