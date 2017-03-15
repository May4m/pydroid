
#: commissioned

from kivy.config import platform

try:
    from jnius import autoclass, cast, java_method
    from android.runnable import run_on_ui_thread
    from jnius import PythonJavaClass
except ImportError:
    autoclass = None
    cast = None
    java_method = None

AndroidImport = autoclass
JavaImport = autoclass

if platform == 'android':
    String = autoclass('java.lang.String')
    List = autoclass('java.util.List')
    ListIterator = autoclass('java.util.ListIterator')
    Iterator = autoclass('java.util.Iterator')
    ArrayList = autoclass('java.util.ArrayList')
    Object = autoclass('java.lang.Object')
    Collection  = autoclass('java.util.Collection')
    System = autoclass('java.lang.System')
    Calender = autoclass('java.util.Calendar')
else:
    String = None
    ArrayList = None
    List = None