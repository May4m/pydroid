
from Android import Activity, Intent
from Android.Java import cast
from Android.Java import String


class AndroidEmail(object):

    @staticmethod
    def send(**kwargs):
        intent = Intent(Intent.ACTION_SEND)
        intent.setType('text/plain')

        recipient = kwargs.get('recipient')
        subject = kwargs.get('subject')
        text = kwargs.get('text')
        create_chooser = kwargs.get('create_chooser')

        if recipient:
            intent.putExtra(Intent.EXTRA_EMAIL, [recipient])
        if subject:
            android_subject = cast('java.lang.CharSequence',
                                   String(subject))
            intent.putExtra(Intent.EXTRA_SUBJECT, android_subject)
        if text:
            android_text = cast('java.lang.CharSequence',
                                String(text))
            intent.putExtra(Intent.EXTRA_TEXT, android_text)

        if create_chooser:
            chooser_title = cast('java.lang.CharSequence',
                                 String('Send message with:'))
            Activity.startActivity(Intent.createChooser(intent,
                                                        chooser_title))
        else:
            Activity.startActivity(intent)