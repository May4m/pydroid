#!/usr/bin/kivy

#: commissioned

from kivy.config import platform


try:
    from jnius import autoclass, cast, java_method
    from android.runnable import run_on_ui_thread
    from android import activity
    from jnius import PythonJavaClass
    from android import get_keyboard_height
    from android.broadcast import BroadcastReceiver
except:
    autoclass = None
    run_on_ui_thread = None
    BroadcastReceiver = None
    cast = None

AndroidImport = autoclass
JavaImport = autoclass

on_results_methods = []
FILE_SELECT_CODE = 0

if platform == 'android':
    # Primitives
    String = autoclass('java.lang.String')

    # Android
    Activity = autoclass('org.renpy.android.PythonActivity').mActivity
    Bundle = autoclass('android.os.Bundle')
    Dialog = autoclass('android.app.Dialog')
    AlertDialog = autoclass('android.app.AlertDialog$Builder')
    WindowParams = autoclass('android.view.WindowManager$LayoutParams')
    Intent = autoclass('android.content.Intent')
    PendingIntent = autoclass('android.app.PendingIntent')
    View = autoclass('android.view.View')
    Uri = autoclass('android.net.Uri')
    ContentProvider = autoclass('android.content.ContentProvider')
    Context = autoclass('android.content.Context')
    Cursor = autoclass('android.database.Cursor')
    Toast = autoclass('android.widget.Toast')
    Contacts = autoclass('android.provider.ContactsContract$Contacts')
    Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
    ContactsData = autoclass('android.provider.ContactsContract$Data')
    SmsMessage = autoclass('android.telephony.SmsMessage')
    SmsManager = autoclass('android.telephony.SmsManager')
    ConnectivityManager = autoclass('android.net.ConnectivityManager')
    Settings = autoclass('android.provider.Settings')
    NotificationBuilder = JavaImport('android.app.Notification$Builder')
    Notification = JavaImport('android.app.Notification')
    NotificationManager = JavaImport('android.app.NotificationManager')   
    MediaStore = autoclass('android.provider.MediaStore')
    MediaPlayer = autoclass('android.media.MediaPlayer')
    MediaRecorder = autoclass('android.media.MediaRecorder')
    Drawable = JavaImport("{}.R$drawable".format(Activity.getPackageName()))
    BluetoothDevice = JavaImport('android.bluetooth.BluetoothDevice')
    BluetoothAdapter = JavaImport('android.bluetooth.BluetoothAdapter')
    BluetoothServerSocket = JavaImport('android.bluetooth.BluetoothServerSocket')
    BluetoothSocket = JavaImport('android.bluetooth.BluetoothSocket')
    Message = JavaImport('android.os.Message')
    Handler = JavaImport('android.os.Handler')
    SDK_VERSION = autoclass('android.os.Build$VERSION').SDK_INT
    Account = JavaImport('android.accounts.Account')
    AccountManager = JavaImport('android.accounts.AccountManager')
    AuthenticatorDescription = JavaImport('android.accounts.AuthenticatorDescription')
    OnAccountsUpdateListener = JavaImport('android.accounts.OnAccountsUpdateListener')
    ContentProviderOperation = JavaImport('android.content.ContentProviderOperation')
    NfcAdapter = JavaImport('android.nfc.NfcAdapter')
    NdefMessage = JavaImport('android.nfc.NdefMessage')
    NdefRecord = JavaImport('android.nfc.NdefRecord')
    Sensor = JavaImport('android.hardware.Sensor')
    SensorEvent = JavaImport('android.hardware.SensorEvent')
    SensorEventListener = JavaImport('android.hardware.SensorEventListener')
    SensorManager = JavaImport('android.hardware.SensorManager')
    UsbConstants = JavaImport('android.hardware.usb.UsbConstants')
    UsbDevice = JavaImport('android.hardware.usb.UsbDevice')
    UsbDeviceConnection = JavaImport('android.hardware.usb.UsbDeviceConnection')
    UsbEndpoint =  JavaImport('android.hardware.usb.UsbEndpoint')
    UsbInterface = JavaImport('android.hardware.usb.UsbInterface')
    UsbManager = JavaImport('android.hardware.usb.UsbManager')
    UsbRequest =  JavaImport('android.hardware.usb.UsbRequest')
    WifiP2pConfig = JavaImport('android.net.wifi.p2p.WifiP2pConfig')
    WifiP2pDevice = JavaImport('android.net.wifi.p2p.WifiP2pDevice')
    WifiP2pManager = JavaImport('android.net.wifi.p2p.WifiP2pManager')
    ActionListener = JavaImport('android.net.wifi.p2p.WifiP2pManager$ActionListener')
    Channel = JavaImport('android.net.wifi.p2p.WifiP2pManager$Channel')
    PeerListListener = JavaImport('android.net.wifi.p2p.WifiP2pManager$PeerListListener')
    ChannelListener = JavaImport('android.net.wifi.p2p.WifiP2pManager$ChannelListener')
    DatePicker = JavaImport('android.widget.DatePicker')
    TimePicker = JavaImport('android.widget.TimePicker')
    SpeechRecognizer = JavaImport('android.speech.RecognizerIntent')
else:
    SDK_VERSION = 16
    Activity = None
    WindowManager = None
    Intent = None
    View = None