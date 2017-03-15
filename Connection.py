"""
required permissions:  INTERNET, ACCESS_NETWORK_STATE
"""

#: commissioned

from Android import Activity
from Android import Intent
from Android import Settings
from Android import Context
from Android import Dictionary
from Android import BluetoothDevice
from Android import BluetoothAdapter
from Android import BroadcastReceiver
from Android.Java import cast

from kivy.app import App
from kivy.logger import Logger
from kivy.event import EventDispatcher


Permissions = Dictionary({
    "CONNECTIVITY_ACTION": "android.net.ConnectivityManager.CONNECTIVITY_ACTION",
    "ACTION_WIRELESS_SETTINGS": Settings.ACTION_WIRELESS_SETTINGS,
    "ACTION_REQUEST_ENABLE": BluetoothAdapter.ACTION_REQUEST_ENABLE
})

class ConnectivityService(EventDispatcher):
    CONNECTIVITY_ACTION = "android.net.ConnectivityManager.CONNECTIVITY_ACTION"  

    def __init__(self, kivy_app=App):
        self.app = kivy_app
        self._callback = None
        super(ConnectivityService, self).__init__()

    @staticmethod
    def connection_available():
        cm = Activity.getSystemService(Context.CONNECTIVITY_SERVICE)
        if cm is None:
            return False

        info = cm.getActiveNetworkInfo()
        if info is not None:
            connected = info.isConnectedOrConnecting()
            Logger.debug('Connected or connecting: {}'.format(connected))
        return connected

    def request_connection(self, callback=None):
        callback = callback if callback else lambda *args, **kwargs: None
        if self.connection_available():
            callback(True)
        else:
            self._callback = callback
            self._open_settings(True)

    def _open_settings(self, try_connect):
        if try_connect:
            app = self.app.get_running_app()
            app.bind(on_resume=self._settings_callback)
            Activity.startActivityForResult(
                Intent(Permissions.ACTION_WIRELESS_SETTINGS), 0)
        else:
            self._callback(False)

    def _settings_callback(self, *args):
        app = self.app.get_running_app()
        app.unbind(on_resume=self._settings_callback)        
        self._callback(self.connection_available())


class Bluetooth(EventDispatcher):

    def __init__(self, **kwargs):
        self.bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        
    def turn_on(self):
        if not self.bluetooth_adapter.isEnabled():
            turn_on = Intent(Permissions.ACTION_REQUEST_ENABLE)
            Activity.startActivityForResult(turn_on, 0)
            Logger.info('[ Android ] Bluetooth turned on')
        else:
            Logger.info('[ Android ] Bluetooth already turned on')

    def list_paired_devices(self):
        paired_devices = self.bluetooth_adapter.getBondedDevices()
        _devices = []
        for dev in paired_devices:
            _devices.append(cast(BluetoothDevice, dev))
        return _devices

    def turn_off(self):
        self.bluetooth_adapter.disable()
        Logger.info('[ Android ] Bluetooth disabled')

    @staticmethod
    def intent(action):
        _intent = Intent(action)
        Activity.startActivityForResult(_intent, 0)