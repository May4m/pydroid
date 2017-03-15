#!/usr/bin/kivy

#: commissioned

"""

    required permissions: RECEIVE_SMS, READ_SMS

    Usage:

    def sms_received(instance, sms):
        // Note: sms is an array of sms objects
        print "From: ", sms.getOriginatingAddress()
        print "Body: ", sms.getMessageBody()
        instance.stop() // stop receiving incoming messages

    listener = IncomingSmsListener()
    listener.bind(on_received=sms_received)


    Preferred Usage:

    class AuthenticationComponent(IncomingSmsListener):
        def on_received(self, instance, sms):
            print "From: ", sms.getOriginatingAddress()
            print "Body: ", sms.getMessageBody()
            self.stop()  # stop listening for messages

    AuthenticationComponent()
    
    
    class MySmsApp(TextMessageManager):
        def on_sms_status(self, context, intent):
            results = super(MySmsApp, self).on_sms_status(context, intent)
            if results == self.SMS_SENT:
                print 'messages sent'

    MySmsApp().send_text_message('0719316515', 'Its the kivy android api')
    
    

"""

from Android import Activity
from Android import JavaImport
from Android import Dictionary
from Android import SmsMessage, SmsManager
from Android import BroadcastReceiver

from kivy.event import EventDispatcher
from kivy.factory import Factory


Permissions = Dictionary({
    'SMS_RECEIVED': 'android.provider.Telephony.SMS_RECEIVED',
    'SENT_ACTION': 'com.androidbook.telephony.SMS_SENT_ACTION',
    'DELIVERED_ACTION': 'com.androidbook.telephony.SMS_DELIVERED_ACTION',
})


class IncomingSmsListener(EventDispatcher):

    broadcast_running = Factory.BooleanProperty()
    received_messages = Factory.ObjectProperty()

    def __init__(self, **kwargs):
        super(IncomingSmsListener, self).__init__(**kwargs)
        self.register_event_type('on_received')

        # `TelephonyInterface` is a static java class
        self.SmsListener = JavaImport('org.rooi.TelephonyServices')

        self.bc_receiver = BroadcastReceiver(self.on_receive,
                             actions=[Permissions.SMS_RECEIVED])
        self.bc_receiver.start()
        self.broadcast_running = True

        # reliability by redundancy
        self.bind(received_messages=self._on_received_messages)

    def on_receive(self, context, intent):  # should never be overridden
        # `context` and `intent` are native java objects
        # This method uses the same pattern as the native java pattern
        # No abstraction and/or interface has been added as part
        if str(intent.getAction()) == Permissions.SMS_RECEIVED:
            self.SmsListener.OnSmsReceive(intent)  # Java interface
            self.received_messages = self.SmsListener.received_messages
            return self.received_messages

    def _on_received_messages(self, *args):
        self.dispatch('on_received', *args)

    def on_received(self, *args):  # may be overridden
        pass

    def stop(self):
        """
        Stop the local broadcast receiver from listening to actions
        """
        self.bc_receiver.stop()
        self.broadcast_running = False


class TextMessageManager(EventDispatcher):

    SMS_SENT = 'SMS_SENT'
    ERROR_RADIO_OFF = 'ERROR_RADIO_OFF'
    ERROR_NO_SERVICE = 'ERROR_NO_SERVICE'
    ERROR_GENERIC_FAILURE = 'ERROR_GENERIC_FAILURE'
    UNKNOWN_STATUS = 'UNKNOWN_STATUS'
    SMS_DELIVERED = 'SMS_DELIVERED'
    SMS_NOT_DELIVERED = 'SMS_NOT_DELIVERED'
    UNKOWN_DELIVERY_CODE = 'UNKOWN_DELIVERY_CODE'

    def __init__(self, **kwargs):
        super(TextMessageManager, self).__init__(**kwargs)
        self.on_sms_status = self.on_receive
        self.b_receiver = BroadcastReceiver(
                            self.on_receive,
                            actions=[Permissions.SENT_ACTION,
                            Permissions.DELIVERED_ACTION])

    def on_receive(self, context, intent):
        action = intent.getAction()
        if Permissions.SENT_ACTION == action:
            get_result_code = self.b_receiver.receiver.getResultCode()
            if get_result_code == Activity.RESULT_OK:
                return self.SMS_SENT
            elif get_result_code == SmsManager.RESULT_ERROR_RADIO_OFF:
                return self.ERROR_RADIO_OFF
            elif get_result_code == SmsManager.RESULT_ERROR_NO_SERVICE:
                return self.ERROR_NO_SERVICE
            elif get_result_code == SmsManager.RESULT_ERROR_NULL_PDU:
                return self.ERROR_NULL_PDU
            elif get_result_code == SmsManager.RESULT_ERROR_GENERIC_FAILURE:
                return self.ERROR_GENERIC_FAILURE
            else:
                return self.UNKNOWN_STATUS

        if Permissions.DELIVERED_ACTION == action:
            get_result_code = self.b_receiver.receiver.getResultCode()
            if get_result_code == Activity.RESULT_OK:
                return self.SMS_DELIVERED
            elif get_result_code == Activity.RESULT_CANCELED:
                return self.SMS_NOT_DELIVERED
            else:
                return self.UNKOWN_DELIVERY_CODE

    @staticmethod
    def send_text_message(recipient, message):
        SmsManager.getDefault().sendTextMessage(recipient, None, message, None, None)

    @staticmethod
    def receive_text_message(intent):  # dummy
        pdu = intent.getExtras().get("pdus")
        message = SmsMessage.createFromPdu(pdu)
        return message