from distutils.core import setup
import py2exe
#usage python setup.py py2exe 

#had to install library with setup.py install_lib option to make it a module that could be imported

#had to include things manually as they show up. 

#have to include typelib numbers from /Lib/site-packages/win32com/genpy/ (delete contents, run script then not numbers.


setup(windows=[{'script': 'test1.py'}], 
    options={ 
        'py2exe': 
        { 
            "typelibs": [('{C866CA3A-32F7-11D2-9602-00C04F8EE628}',0,5,4)],
            'includes': ['pyttsx', 'pyttsx.drivers.sapi5'], 
        } 
    } 
) 
