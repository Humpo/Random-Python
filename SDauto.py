#open service desk and stuff


import mechanize

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException

from time import sleep
from pywinauto import findwindows
import win32gui
import psutil
import os

class Ticket:
    class Change(object):
        def __init__(self, desk):
            self.desk = desk
            #self.number = self.get_number()
            
        def get_number(self):
            '''gets the change order number'''
            self.desk._navigate_frame("cai_main")
            element = self.desk.driver.get_element_by_xpath("/html/body/center/table[1]/tbody/tr/td[1]/h2")
            text = driver.execute_script("""
                                         return jQuery(arguments[0]).contents().filter(function() {
                                            return this.nodeType == Node.TEXT_NODE;
                                         }).text();
                                         """, element)
            self.number = tect.split()[-1]

        def set_all(self, info_dict):
            for key in info_dict.keys():
                if key == "requester":self.set_requester(info_dict[key])
                elif key == "affected_user":self.set_affected_user(info_dict[key])
                elif key == "category":self.set_category(info_dict[key])
                elif key == "status":self.set_status(info_dict[key])
                elif key == "source":self.set_source(info_dict[key])
                elif key == "location":self.set_location(info_dict[key])
                elif key == "department":self.set_department(info_dict[key])
                elif key == "email":self.set_email(info_dict[key])
                elif key == "phone":self.set_phone(info_dict[key])
                elif key == "FOC":self.set_FOC(info_dict[key])
                elif key == "assignee":self.set_assignee(info_dict[key])
                elif key == "group":self.set_group(info_dict[key])
                elif key == "impact":self.set_impact(info_dict[key])
                elif key == "start_date":self.set_start_date(info_dict[key])
                elif key == "call_back_date":self.set_call_back_date(info_dict[key])
                elif key == "root_cause":self.set_root_cause(info_dict[key])
                elif key == "clarity_project_num":self.set_clarity_project_num(info_dict[key])
                elif key == "order_summary":self.set_order_summary(info_dict[key])
                elif key == "order_description":self.set_order_description(info_dict[key])
                else:None   
            
        def set_requester(self, data):
            '''sets the requester field with data provided'''
            self.desk._set_element_value("df_0_0", data)
            #sets elements value
            
        def set_affected_user(self, data):
            '''sets the affected_user field with data provided'''
            self.desk._set_element_value("df_0_1", data)

        def set_category(self, data):
            '''sets the category field with data provided'''
            self.desk._navigate_frame('cai_main')
            self.desk._send_key_to_id("df_0_2", data)
            
        def set_status(self, data):
            '''sets the status field with data provided'''
            self.desk._set_element_value("df_0_3", data)
            
        def set_source(self, data):
            '''sets the source field with data provided'''
            self.desk.driver.switch_to_default_content()
            self.desk._navigate_frame('cai_main')
            
            inputElement = Select(self.desk.driver.find_element_by_id("df_0_4"))
            inputElement.select_by_visible_text(data)
            
        def set_location(self, data):
            '''sets the location field with data provided'''
            self.desk._set_element_value("df_1_0", data)

        def set_department(self, data):
            '''sets the department field with data provided'''
            self.desk._set_element_value("df_1_1", data)

        def set_email(self, data):
            '''sets the email field with data provided'''
            self.desk._set_element_value("df_1_2", data)
        
        def set_phone(self, data):
            '''sets the v field with data provided'''
            self.desk._set_element_value("df_1_3", data)
            
        def set_FOC(self, data):
            '''sets the FOC field with data provided'''
            self.desk._set_element_value("df_1_4", data)

        def set_assignee(self, data):
            '''sets the asignee field with data provided'''
            self.desk._set_element_value("df_2_1", data)
            
        def set_group(self, data):
            '''sets the group field with data provided'''
            self.desk.driver.switch_to_default_content()
            self.desk._navigate_frame('cai_main')
            self.desk._send_key_to_id("df_2_2", data)
            
        def set_impact(self, data):
            '''sets the impact level'''
            self.desk._set_element_value("df_2_3", data)

        def set_start_date(self, data):
            '''sets the start date'''
            self.desk._set_element_value("df_3_0", data)

        def set_call_back_date(self, data):
            '''sets the call back date'''
            self.desk._set_element_value("df_3_1", data)

        def set_root_cause(self, data):
            '''sets the start date'''
            self.desk._set_element_value("df_3_2", data)

        def set_clarity_project_num(self, data):
            '''sets the clarity project number'''
            self.desk._set_element_value("df_3_3", data)

        def set_order_summary(self, data):
            '''sets the order summary'''
            self.desk._set_element_value("df_4_0", data)

        def set_order_description(self, data):
            '''sets the order description'''
            self.desk.driver.switch_to_default_content()
            self.desk._navigate_frame('cai_main')
            self.desk._send_key_to_id("df_5_0", data)

class ServiceDesk(object):
    '''
    This class is designed for automating ticket submission
    in Unicenter Service Desk web application

    ***NOTE***
    With no feasible way to get access to an API or back end server
    I must resort to navigating the site manually.

    This class is not going to be a full API for Unicenter Service Desk
    but a simple tool designed to accomplish a small set of tasks

    I assume this is a node.js application based upon it's structure or
    some back end custom framework. Idk all I know is no one knows anything...
    '''
    def __init__(self, visible = True):

        self.visible = visible
        self.is_log_in = False
        #^by default make visible
        
        #for key, value in styles.iteritems():
        #    setattr(self, key, value)
        #^set attributes

        if self.visible:
            self._launch_visible()
        else:
            self._launch_invisible()
        #^launches visible or invisible based on user preference
        
        self.main_window = self.driver.current_window_handle
        self.driver.get("http://sykpcasdap02v/CAisd/pdmweb.exe")
        #^goes to CA website

        self.current_ticket = None
        #^ticket creation

    def log_in(self, username, password):
        '''logs into CA with defined username and password'''

        if self.is_log_in == True:
            print "Already logged in"
            return False
        #^prevents user from loggin on twice

        if type(username) != str or type(password) != str:
            print "Username or password must be string"
            return False
        #^makes sure input is valid
        
        try:
            username_element = self.driver.find_element_by_id("USERNAME")
            password_element = self.driver.find_element_by_id("PIN")
            #^get's log_in necessary elements

            username_element.send_keys(username)
            password_element.send_keys(password)
            #^sends keystrokes to those elements

            self.driver.find_element_by_id("imgBtn0_button").click()
            #clicks log in 

            try:
                self.driver.find_element_by_id("USERNAME")
            except NoSuchElementException:
                self.log_in = True
                return True

            print "Username or password invalid"
            return False
            
        except NoSuchElementException:
            print "Unable to find 'User Name' or 'password' or 'log in'"
            return False    

    def navigate_window(self, handle=None):
        '''navigates to the first window that's not the main window'''
        try:
            if handle != None:self.driver.switch_to_window(handle)
            #^handle provided try to switch to window

            handles = self.driver.window_handles
            while handles < 2:handles = self.driver.window_handles
            
            for handle in self.driver.window_handles:
                if handle != self.main_window:
                    self.driver.switch_to_window(handle)
            #^loop through all windows and switch to the first one
            return True
        except NoSuchWindowException:
            print "Invalid window handle"
            return False

    def create_new_change(self):
        '''navigates to service desk -> new change to make a new change order'''
        self.driver.switch_to_default_content()
        
        self._navigate_frame('toolbar')
        self.driver.find_element_by_id('tabhref0').click()

        self.driver.switch_to_default_content()

        self._navigate_frame('product')
        self._navigate_frame('sd')
        self._navigate_frame('scoreboard')

        self.driver.find_element_by_id("imgBtn2").click()

        handles = self.driver.window_handles
        while handles < 2:handles = self.driver.window_handles

        self.current_ticket = Ticket.Change(self)
        
        return True

    def _navigate_frame(self, name):
        '''navigates to a desired frame based on name'''
        if type(name) != str:return False
        #^authenticates input

        try:
            frame = self.driver.find_element_by_name(name)
            self.driver.switch_to_frame(frame)
            #^gets the default content of page, switches to frame
            return True
        except NoSuchElementException:
            print "No frame with that name"
            return False

    def _send_key_to_id(self, id, data):
        '''sends keystrokes to an element with specific id'''

        if type(id) != str or type(data) != str:
            print "both inputs must be strings"
            return False
        #^makes sure input is valid
        
        try:
            element = self.driver.find_element_by_id(id)
            element.send_keys(data)
            return True
        except NoSuchElementException:
            print "Element with id cannot be found"
            print id
            return False

    def _set_element_value(self, id, data):
        
        if type(id) != str or type(data) != str:
            print "both inputs must be strings"
            return False
        
        try:
            self.driver.execute_script("document.getElementById(\'"+id+"\') \
                                     .setAttribute('value', \'"+data+"\')");
            return True
        except WebDriverException:
            print "invalid data or id"
            print id
            return False

    def _click_element(self, id):
        self.driver.find_element_by_id(id).click()
        return True
    
    def _launch_visible(self):
        '''launches chrome visible to user SHOULD ONLY BE USED ONCE'''
        try:
            path = "c:\\python27\\programs\\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = path
            self.driver = webdriver.Chrome(path)
            #^launch selenium with chrome and adds driver to class
            return True
        except:
            return False
        
    def _launch_invisible(self):
        '''launches phantom js invisible SHOULD ONLY BE USED ONCE'''
        try:
            self.driver = webdriver.PhantomJS()
            window_h = findwindows.find_windows(title = r"C:\Python27\programs\phantomjs.exe")
            while len(window_h) == 0:
                window_h = findwindows.find_windows(title = r'C:\Python27\programs\phantomjs.exe')

            win32gui.ShowWindow(window_h[0], False)
            #launches PhantomJS then makes window invisible
            return True
        except:
            return False
            
    def tear_down(self):
        '''kills CA and ends session'''
        self.driver.close()
        #^kills driver

        for proc in psutil.process_iter():#loop through all processes
            try:
                if proc.name() == "phantomjs.exe":proc.kill()#if this process kill it and start a new
            except:
                None
        #^ends phantom js task

        self.log_in = False
        return True

def main2():
    user_dict = {
        'visible':True
        }

    desk = ServiceDesk()
    desk.log_in("secret","supersecret")
    desk.create_new_change()
    desk.navigate_window()

    info_dict = {
            'affected_user':"Vora, Vagmin",
            'requester':"Vora, Vagmin",
            'category':r"%Access SCM",
            'source':"E-Mail",
            'location':"Manhasset Main - 300",
            'phone':"555-5555",
            'FOC':"123456789",
            'group':"SCM - Helpdesk Support",
            'order_summary':"Jim Brown Report - 1234  Vora, Vagmin",
            'order_description':"Jim Brown Report - 1234  Vora, Vagmin",  
        }


    desk.current_ticket.set_all(info_dict)

    sleep(30)

    desk.tear_down()

if __name__ == "__main__":
    '''
    This program is designed to log into ServiceDesk Ticketing system
    for IT ticket management. This is a really old web application that
    requires manual navigation. No API has been provided for thsi application.
    This was designed for people who have ServiceDesk accounts aleady
    affiliated with NSLIJ. Will not work if an invalid username/password is not
    provided
    '''
    main2()
