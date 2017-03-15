from jnius import autoclass
from Android import Activity, SDK_VERSION

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(Activity.getPackageName()))


class AndroidNotification(object):
    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = Activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def _notify(self, **kwargs):
        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))
        noti = NotificationBuilder(Activity)
        noti.setContentTitle(AndroidString(
            kwargs.get('title').encode('utf-8')))
        noti.setContentText(AndroidString(
            kwargs.get('message').encode('utf-8')))
        noti.setTicker(AndroidString(
            str('New Message Alert').encode('utf-8')))
        noti.setSmallIcon(icon)
        noti.setAutoCancel(True)

        if SDK_VERSION >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(0, noti)
    notify = _notify


def Notification():
    return AndroidNotification()