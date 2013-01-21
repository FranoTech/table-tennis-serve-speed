from distutils.core import setup
import py2exe
#usage python setup.py py2exe 

#had to install library with setup.py install_lib option to make it a module that could be imported

#had to include things manually as they show up. 

#have to include typelib numbers from /Lib/site-packages/win32com/genpy/ (delete contents, run script then get numbers.


setup(windows=[{'script': 'TTTrack.py'}], 
    options={ 
        'py2exe': 
        { 
            "typelibs": [('{C866CA3A-32F7-11D2-9602-00C04F8EE628}',0,5,4)],
            'includes': ['pyttsx', 'pyttsx.drivers.sapi5'], 
        } 
    } 
) 

"""
Build currently depends on: 
 OLEAUT32.dll - C:\Windows\system32\OLEAUT32.dll
 USER32.dll - C:\Windows\system32\USER32.dll
 IMM32.dll - C:\Windows\system32\IMM32.dll
 SHELL32.dll - C:\Windows\system32\SHELL32.dll
 ole32.dll - C:\Windows\system32\ole32.dll
 COMDLG32.dll - C:\Windows\system32\COMDLG32.dll
 COMCTL32.dll - C:\Windows\system32\COMCTL32.dll
 ADVAPI32.dll - C:\Windows\system32\ADVAPI32.dll
 GDI32.dll - C:\Windows\system32\GDI32.dll
 WS2_32.dll - C:\Windows\system32\WS2_32.dll
 WINSPOOL.DRV - C:\Windows\system32\WINSPOOL.DRV
 mfc90.dll - C:\Python27\lib\site-packages\Pythonwin\mfc90.dll
 VERSION.dll - C:\Windows\system32\VERSION.dll
 KERNEL32.dll - C:\Windows\system32\KERNEL32.dll

 """