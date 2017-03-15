"""
Required permissions: android.permission.USE_SIP, android.permission.INTERNET, android.permission.RECORD_AUDIO
                      android.permission.WAKE_LOCK, android.permission.ACCESS_WIFI_STATE
"""
from Android import BroadcastReceiver
from Android import Activity
from Android import JavaImport

from kivy.event import EventDispatcher

TelephonyServices = JavaImport('org.rooi.TelephonyServices')
SipAudioCall = JavaImport('android.net.sip.SipAudioCall')

ACTION = ['android.SipDemo.INCOMING_CALL']


def SipManager():  # returns an instantiated `SipManager` object
    sip_mngr = JavaImport('android.net.sip.SipManager')
    return sip_mngr.newInstance(Activity)


class IncomingCallReceiver(EventDispatcher):
    def __init__(self, **kwargs):
        super(IncomingCallReceiver, self).__init__(**kwargs)
        self.register_event_type('on_incoming_call')
        self.b_receiver = BroadcastReceiver(self.on_receive, actions=[ACTION])
        self.b_receiver.start()

    def on_receive(self, context, intent):
        # `context` and `intent` are native java objects
        if str(intent.getAction()) == ACTION:  # android pattern
            TelephonyServices.SipIncomingCallHandler(context, intent)  # invoke the java/python abstract
            # this will dispatch `sipCallerProfile` and `sipCall` which are native
            # java objects
            self.dispatch('on_incoming_call', TelephonyServices.sipCallerProfile,
                          TelephonyServices.sipCall)

    def on_incoming_call(self, instance, call_profile, call):
        pass

    def stop(self):  # stop listening for incoming sip calls
        self.b_receiver.stop()