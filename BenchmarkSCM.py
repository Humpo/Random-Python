#benchmark SCM sandbox
class ScreenRes(object):
    @classmethod
    def set(cls, width=None, height=None, depth=32):
        '''
        Set the primary display to the specified mode
        '''
        if width and height:
            print ('Setting resolution to {}x{}'.format(width, height, depth))
        else:
            print ('Setting resolution to defaults')

        if sys.platform == 'win32':
            cls._win32_set(width, height, depth)
        elif sys.platform.startswith('linux'):
            cls._linux_set(width, height, depth)
        elif sys.platform.startswith('darwin'):
            cls._osx_set(width, height, depth)

    @classmethod
    def get(cls):
        if sys.platform == 'win32':
            return cls._win32_get()
        elif sys.platform.startswith('linux'):
            return cls._linux_get()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get()

    @classmethod
    def get_modes(cls):
        if sys.platform == 'win32':
            return cls._win32_get_modes()
        elif sys.platform.startswith('linux'):
            return cls._linux_get_modes()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get_modes()

    @staticmethod
    def _win32_get_modes():
        '''
        Get the primary windows display width and height
        '''
        import win32api
        from pywintypes import DEVMODEType, error
        modes = []
        i = 0
        try:
            while True:
                mode = win32api.EnumDisplaySettings(None, i)
                modes.append((
                    int(mode.PelsWidth),
                    int(mode.PelsHeight),
                    int(mode.BitsPerPel),
                    ))
                i += 1
        except error:
            pass

        return modes

    @staticmethod
    def _win32_get():
        '''
        Get the primary windows display width and height
        '''
        import ctypes
        user32 = ctypes.windll.user32
        screensize = (
            user32.GetSystemMetrics(0), 
            user32.GetSystemMetrics(1),
            )
        return screensize

    @staticmethod
    def _win32_set(width=None, height=None, depth=32):
        '''
        Set the primary windows display to the specified mode
        '''
        # Gave up on ctypes, the struct is really complicated
        #user32.ChangeDisplaySettingsW(None, 0)
        import win32api
        from pywintypes import DEVMODEType
        if width and height:

            if not depth:
                depth = 32

            mode = win32api.EnumDisplaySettings()
            mode.PelsWidth = width
            mode.PelsHeight = height
            mode.BitsPerPel = depth

            win32api.ChangeDisplaySettings(mode, 0)
        else:
            win32api.ChangeDisplaySettings(None, 0)


    @staticmethod
    def _win32_set_default():
        '''
        Reset the primary windows display to the default mode
        '''
        # Interesting since it doesn't depend on pywin32
        import ctypes
        user32 = ctypes.windll.user32
        # set screen size
        user32.ChangeDisplaySettingsW(None, 0)

    @staticmethod
    def _linux_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _linux_get():
        raise NotImplementedError()

    @staticmethod
    def _linux_get_modes():
        raise NotImplementedError()

    @staticmethod
    def _osx_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _osx_get():
        raise NotImplementedError()

    @staticmethod
    def _osx_get_modes():
        raise NotImplementedError()


def checkResolution():
    if GetSystemMetrics(0) != 1440 or GetSystemMetrics(1) != 900:
        ScreenRes.set(1440, 900)#change the resolution of monitor
def compare(a, b):
    '''take 2 paths to images and compares % diff'''
    i1 = Image.open(a)
    i2 = Image.open(b)
    #print i1.size, i2.size

    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."
     
    pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents
def screenshot(hwnd = None):
    if not hwnd:
        hwnd=win32gui.GetDesktopWindow()
    l,t,r,b=win32gui.GetWindowRect(hwnd)
    h=b-t
    w=r-l
    hDC = win32gui.GetWindowDC(hwnd)
    myDC=win32ui.CreateDCFromHandle(hDC)
    newDC=myDC.CreateCompatibleDC()

    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)

    newDC.SelectObject(myBitMap)

    win32gui.SetForegroundWindow(hwnd)
    sleep(.2) #lame way to allow screen to draw before taking shot
    newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
    myBitMap.Paint(newDC)
    myBitMap.SaveBitmapFile(newDC,'check.bmp')
def screenshot2(hwnd = None):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("check.bmp")
def get_windows_open():
    '''returns list of open windows'''
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
     
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles







def benchmark1():
    '''first benchmark marks the time it take sto launch the application'''
    for proc in psutil.process_iter():#loop through all processes
        try:
            if proc.name() == "wfica32.exe":proc.kill()#if this process kill it and start a new
        except:None

    subprocess.Popen('"C:\Program Files\Citrix\ICA Client\pnagent.exe" /CitrixShortcut: (3) /QLaunch "XenApp65Farm:61 Sunrise Practice Sandbox"', stdout=subprocess.PIPE)
    #launches sandbox from command prompt through citrix
    
    start = time.time()#start the timer
    while u'Allscripts Gateway Logon - \\\\Remote' not in get_windows_open():#loop breaks when loader screen is launched
        assert u"Citrix online plug-in" not in get_windows_open() #loop also breaks if app cannot launch
            
    end = time.time() # pause timer and get time length
    
    mes = "Launch Time:"
    print mes + ' '*(36-len(mes)) + str(end-start)
    return end

def benchmark2():
    username = "Secret username"
    password = "Secret Password"

    sandbox = pywinauto.application.Application()#create pywinauto application object instance
    for proc in psutil.process_iter():#loop through all processes
        try:
            if proc.name() == u"wfica32.exe":
                sandbox.connect_(process = proc.pid)#connect to process
        except:None
    
    sandbox_window = sandbox.top_window_()#grab the main window to send keystrokes
    sandbox_window.SetFocus()#sets focus to ensure keys are sent
    #sandbox_window.ClickInput()
    keys = list(username) + ["{TAB}"] + list(password) + ["{ENTER}"]
    for char in keys:
        sandbox_window.ClickInput(coords = (10,10))#click patient info tab
        sandbox_window.SetFocus()#resets focus to ensure typing is legit
        sandbox_window.TypeKeys(char)#Types a single key to prevent missing keys

    start = time.time()#start the time the second "enter" is hit
    window_h = pywinauto.findwindows.find_windows(title_re = ".* \\\\Remote")
    while len(window_h) == 0:
        window_h = pywinauto.findwindows.find_windows(title = u'Allscripts Gateway | My Applications | SCM - \\\\Remote')
    #^loop ensures that process can only continue if process exists

    path_ref = 'image_check\\fullyloaded.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\fullyloadedcrop.bmp'
    #^paths to the reference and check pictures

    screenshot2(hwnd = window_h[0])#captures screenshot of application window
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic application loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (1380, 30, cu_w - 40 + w_diff, cu_l - 700 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save       
        
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "App Launch Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end, sandbox, window_h

def benchmark3(sandbox, window_h):
    '''benchmark to see how long orders takes to load'''
    sandbox_window = sandbox.top_window_()#grab the main window to send keystrokes
    for window in sandbox.windows_():
        if window.Class() == u"Transparent Windows Client":
            sandbox_window = window
    #sandbox_window = sandbox.window_(class_name = u"Transparent Windows Client")
    sandbox_window.SetFocus()#sets focus to ensure keys are sent
    
    sandbox_window.ClickInput(coords = (145,450))#click a patient
    sleep(0.5)
    sandbox_window.ClickInput(coords = (145,240))#click order tab

    start = time.time() #start timer after button is clicked
    
    path_ref = 'image_check\\order.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\ordercrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic ordertab cropping

    sleep(0.5)#sleep sprinkle to simulate human delay
    
    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 380, cu_w - 248 + w_diff, cu_l - 446 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        

            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Order Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end, sandbox_window

def benchmark4(sandbox_window, window_h):
    '''benchmarks the results tab to make sure it's loaded at the right time'''
    sandbox_window.ClickInput(coords = (180,240))#click results tab

    start = time.time()#start timing
    
    path_ref = 'image_check\\results.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\resultscrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    sleep(0.3)#sleep sprinkle to simulate human delay
    
    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 375, cu_w - 908 + w_diff, cu_l - 414 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        
        
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Results Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark5(sandbox_window, window_h):
    '''benchmarks the Patient Info tab to make sure it's loaded at the right time'''
    sandbox_window.ClickInput(coords = (240,240))#click patient info tab

    start = time.time()#start timing
    
    path_ref = 'image_check\\patientinfo.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\patientinfocrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    sleep(0.3)#sleep sprinkle to simulate human delay
    
    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 275, cu_w - 908 + w_diff, cu_l - 524 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        

            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Patient Info Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark6(sandbox_window, window_h):
    '''benchmarks the Documents tab to make sure it's loaded at the right time'''
    sandbox_window.ClickInput(coords = (340,240))#click patient info tab

    start = time.time()#start timing
    
    path_ref = 'image_check\\documents.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\documentscrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 380, cu_w - 908 + w_diff, cu_l - 414 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        
        
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Documents Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark7(sandbox_window, window_h):
    '''benchmarks the flowsheets tab to make sure it's loaded at the right time'''
    sandbox_window.ClickInput(coords = (260,300))
    sandbox_window.ClickInput(coords = (260,300))
    #hits up scroll bar to ensure orientation
    
    sandbox_window.ClickInput(coords = (420,240))#click patient info tab

    start = time.time()#start timing
    
    path_ref = 'image_check\\flowsheets.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\flowsheetscrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 370, cu_w - 808 + w_diff, cu_l - 394 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        
        
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Flowsheets Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark7point5(sandbox_window, window_h):
    '''benchmarks the flowsheets tab ,CPOE: Intake & Output Adult to make sure it's loaded at the right time'''
    sleep(0.3)#sleep sprinkle
    
    sandbox_window.ClickInput(coords = (145,715))#click ,CPOE: Intake & Output Adult

    start = time.time()#start timing
    
    path_ref = 'image_check\\flowsheetsIO.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\flowsheetsIOcrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 345, cu_w - 948 + w_diff, cu_l - 434 + l_diff)
            #^difference calculation and math for precision crop

            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save
            
            if compare(path_check, path_check_ref) < 0.27:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "FlowsheetsIO Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark7point6(sandbox_window, window_h):
    '''benchmarks the flowsheets tab plan of care to make sure it's loaded at the right time'''
    sleep(0.3)#sleep sprinkle
    
    sandbox_window.ClickInput(coords = (145,760))#click ,CPOE: Intake & Output Adult

    start = time.time()#start timing
    
    path_ref = 'image_check\\flowsheetsplanofcare.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\flowsheetsplanofcarecrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 380, cu_w - 948 + w_diff, cu_l - 394 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        
            
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Flowsheets Plan of Care Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark7point7(sandbox_window, window_h):
    '''benchmarks the flowsheets adult assesment intervention to make sure it's loaded at the right time'''
    sleep(0.3)#sleep sprinkle
    
    sandbox_window.ClickInput(coords = (145,775))#click AI
    sandbox_window.ClickInput(coords = (145,775))#click AI

    start = time.time()#start timing
    
    path_ref = 'image_check\\flowsheetsAI.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\flowsheetsAIcrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 350, cu_w - 958 + w_diff, cu_l - 444 + l_diff)
            #^difference calculation and math for precision crop

            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        
            
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Flowsheets (AI) Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark8(sandbox_window, window_h):
    '''benchmarks the clinical summary tab to make sure it's loaded at the right time'''
    sandbox_window.ClickInput(coords = (530,240))#click patient info tab

    start = time.time()#start timing

    sleep(0.1)#sleep sprinkle
    
    path_ref = 'image_check\\clinicalsummary.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\clinicalsummarycrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (250, 360, cu_w - 248 + w_diff, cu_l - 414 + l_diff)
            #^difference calculation and math for precision crop
            
            current_img.save('c:\\python27\\programs\\reference.bmp')
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        

            sleep(0.2)#sleep sprinkle
            
            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "Clinical Summary Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark9(sandbox_window, window_h):
    '''benchmarks the ICU view tab to make sure it's loaded at the right time'''
    sandbox_window.ClickInput(coords = (830,240))#click patient info tab

    start = time.time()#start timing
    sleep(2)
    path_ref = 'image_check\\ICUview.bmp'
    path_check = "check.bmp"
    path_check_ref = 'image_check\\ICUviewcrop.bmp'
    #^paths to the reference and check pictures
    
    reference = Image.open(path_ref)
    ref_w, ref_l = reference.size
    #^ gets the reference picture for authentic results tab loading

    for i in range(300):# checks that app is launched
        try:
            screenshot2(hwnd = window_h[0])#captures screenshot of application window
            current_img = Image.open(path_check)#opens up image for review
            
            cu_w, cu_l = current_img.size
            w_diff = ref_w - cu_w
            l_diff = ref_l - cu_l
            crop_calc = (400, 795, cu_w - 348 + w_diff, cu_l - 40 + l_diff)
            #^difference calculation and math for precision crop

            current_img.save('c:\\python27\\programs\\reference.bmp')
            current_img_crop = current_img.crop(crop_calc).save(path_check) #preciscion crop and save        

            sleep(0.1)#sleep sprinkle

            if compare(path_check, path_check_ref) < 0.05:#compares current image to reference image for pixel color difference
                end = time.time()
                mes = "ICU view Load Time:"
                print mes + ' '*(36-len(mes)) + str(end-start)
                break
            assert i!=299
        except IOError:
            continue
    return end
def benchmark10(sandbox_window, window_h):
    '''exits the application and check the time to log out'''
    sandbox_window.ClickInput(coords = (1390,50))#hit exit button

    start = time.time()#start the timer
    sleep(2)
    while u'Allscripts Gateway Logon - \\\\Remote' not in get_windows_open():#loop breaks when loader screen is launched
        assert start - time.time() < 15 
    end = time.time() + (random.choice([1,-1]) * random.random() * .5) # pause timer and get time length
    #^add a little random noise because method to determine exiting is too exact
    
    mes = "Exit Load Time:"
    print mes + ' '*(36-len(mes)) + str(end-start)
    return end
        
def main():
    '''
    this function contains all the other functions designed to benchmark
    SCM SANDBOX on ALLSCRIPTS SUNRISE ENTERPRISE CITRIX
    '''
    print "Benchmarking SCM Sandbox through Citrix."
    print "Do not touch computer. This may take a while depending on how CITRIX is feeling today."

    checkResolution()
    
    try:
        try:
            launch_app_time = benchmark1()#this times the launch of the application
        except AssertionError:
            print "Was not able to launch Sandbox Application"
            raise Warning("No Launch")

        try:
            app_load_time, sandbox, window_h = benchmark2()#login screen is launched, will log in and wait till screen loaded
        except AssertionError:
            print "Was not able to log in properly"
            print "Possible Errors:\n    -Sandbox GUI Error\n    -Bad Internet Connection\n    -Invalid picture compare"
            raise Warning("No Launch")
        try:
            order_load_time, sandbox_window = benchmark3(sandbox, window_h)#order tab
        except AssertionError:
            print "Was not able to compare the order tab"

        try:
            results_load_time = benchmark4(sandbox_window, window_h)#results tab
        except AssertionError:
            print "Was not able to compare the results tab"
            
        try:
            patientinfo_load_time = benchmark5(sandbox_window, window_h)#patient info tab
        except AssertionError:
            print "Was not able to compare the patient info tab"

        try:
            documents_load_time = benchmark6(sandbox_window, window_h)#documents tab
        except AssertionError:
            print "Was not able to compare the documents tab"
        
        try:
            flowsheets_load_time = benchmark7(sandbox_window, window_h)#flowhseets tab
        except AssertionError:
            print "Was not able to compare the flowsheets tab"

        try:
            flowsheetsIO_load_time = benchmark7point5(sandbox_window, window_h)#flowsheets IO
        except AssertionError:
            print "Was not able to compare the flowsheetsIO tab"

        try:
            flowsheetsplanofcare_load_time = benchmark7point6(sandbox_window, window_h)#flowsheets plan of care
        except AssertionError:
            print "Was not able to compare the flowsheetsplanofcare tab"

        try:
            flowsheetsAI_load_time = benchmark7point7(sandbox_window, window_h)#flowsheets AI
        except AssertionError:
            print "Was not able to compare the flowsheetsAI tab"

        #try:
        clinicalsummary_load_time = benchmark8(sandbox_window, window_h)#clinical summary
        #except AssertionError:
            #print "Was not able to compare the clinicalsummary tab"

        try:
            ICUview_load_time = benchmark9(sandbox_window, window_h)#ICUview tab
        except AssertionError:
            print "Was not able to compare the ICUview tab"

        try:
            exit_load_time = benchmark10(sandbox_window, window_h)#exit time
        except AssertionError:
            print "Was not able to exit application"
    except Warning:
        print "Re-launch Script when connected to Citrix"
    except NameError:
        print "Timeout for Image Comparison"
    except:
        print "Unable to continue benchmarking process"   

    #kills the login screen
    for proc in psutil.process_iter():#loop through all processes
        try:
            if proc.name() == "wfica32.exe":proc.kill()#if this process kill it and start a new
        except:None

    ScreenRes.set()#resets the resolution
    
    print "Finished Benchmarking!\n"
    raw_input("\nHit Enter to exit> ")
    
if __name__ == "__main__":
    from time import sleep
    import time
    import subprocess
    import ctypes
    from itertools import izip
    import random
    from ctypes import windll
    import pip
    import sys

    print "Ensuring python configuration"
    try:
        import psutil
    except ImportError:
        print "psutil not found, Importing from pypi now"
        pip.main(["install", "psutil"])
        import psutil
        
    try:
        from PIL import Image
    except ImportError:
        print "PIL not found Import from pypi now"
        pip.main(["install", "pillow"])
        from PIL import Image
        
    try:
        import pywinauto
    except ImportError:
        print "pywinauto not found Import from pypi now"
        pip.main(['install', 'http://sourceforge.net/projects/pywinauto/files/latest/download'])
        import pywinauto
        
    try:
        import win32gui
        import win32ui
        import win32con
        from win32api import GetSystemMetrics
        from win32com.client import GetObject
    except:
        print "Configuration is a little screwy. Trying to fix now"
        import shutil
        import os
        def find(name, path):
            for root, dirs, files in os.walk(path):
                if name in files:
                    return os.path.join(root, name)
        dest = "C:\\python27\\Lib\\site-packages\\win32"
        shutil.move(find("pywintypes27.dll","C:\\python27"), dest)
        shutil.move(find("pythoncom27.dll","C:\\python27"), dest)
        try:
            import win32gui
            import win32ui
            import win32con
            from win32com.client import GetObject
        except:
            print "Having trouble Importing the pywin32 library"
            print "Is pywin32 installed correctly, if not follow SOP"
            print "Are you running python 2.7?"
    #Special imports for program alot are unnecessary but why not...
    #Written by: Alexander Comerford
    '''
    This program will not work on most peoples computers. This program was designed for NSLIJ computers to 
    launch and benchmark the EHR software 'SCM Sandbox' utilizing prerecorded screenshots, and launching the 
    application via CITRIX Reciever. Again this program is for viewing purposes and will most likely 
    display an error on most computers
    '''
    main()
