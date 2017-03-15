package org.rooi;

import android.content.Context;
import android.content.Intent;
import android.telephony.SmsMessage;
import android.util.Log;


public class TelephonyServices
{

	private static final String  ACTION = "android.provider.Telephony.SMS_RECEIVED";
	private static final boolean DEBUG = true;
	public static SmsMessage[]   received_messages;

	public static SmsMessage[] OnSmsReceive(Intent intent)
	{
	    if (intent != null && intent.getAction() != null &&
            ACTION.compareToIgnoreCase(intent.getAction()) == 0) {
            
			Object[] pduArray = (Object[])intent.getExtras().get("pdus");
			SmsMessage[] messages = new SmsMessage[pduArray.length];

			for(int i = 0; i < pduArray.length; i++) {
				messages[i] = SmsMessage.createFromPdu((byte[])pduArray[i]);
			}
            received_messages = messages;
			return messages;
	    }
	    return received_messages;
    }

    public static SmsMessage HandleSmsIntent(Intent intent)
	{
		SmsMessage  message;
		Object[]    pdus = (Object[])intent.getExtras().get("pdus");
		for (int i = 0; i < pdus.length; i++) {
			message = SmsMessage.createFromPdu((byte[]) pdus[i]);
		}
		return message;	    
	}
}