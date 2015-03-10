'''
Requires Win32 to run
'''



import win32gui, win32com, win32con, win32com.client,win32api
from time import sleep
shell = win32com.client.Dispatch("WScript.Shell")
shell.Run("Notepad")

sleep(0.5)

shell.AppActivate('Notepad')
handle = win32gui.FindWindow(None,r'Untitled - Notepad')

shell.SendKeys("This is a sentence that is being written in notepad")
sleep(5)
win32gui.SetForegroundWindow(handle)
win32gui.SendMessage(handle,win32con.WM_CLOSE,0,0)
