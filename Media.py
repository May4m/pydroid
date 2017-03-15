"""
    >>>from Android.Media import Camera
    >>>class TakePic(Camera.CameraSnap)
    >>>    def on_snap(self, instance, pic, time):
    >>>        print "Picture path is: ", pic
    >>>TakePic().take_picture()

"""

from functools import partial
from os.path import exists

try:
    from android import activity
    from Android import MediaStore, Intent, Uri, Activity
    from Android import register_on_results_methods
    from Android.Java import cast
except:
    Activity = object()
    pass

from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class Camera:  # poses as a namespace

    def __init__(self):
        pass

    class CameraSnap(object):

        def __init__(self):
            register_on_results_methods(self.on_activity_result)
            self.last_fn = None
            self.uri = None

        def on_activity_result(self, requestCode, resultCode, intent):
            if requestCode == 0x123:
                Clock.schedule_once(partial(self.on_snap, self.last_fn), 0)

        def on_snap(self, instance, last_fn, time):
            pass

        def take_picture(self):
            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            self.last_fn = self.get_filename()
            self.uri = Uri.parse('file://' + self.last_fn)
            self.uri = cast('android.os.Parcelable', self.uri)
            intent.putExtra(MediaStore.EXTRA_OUTPUT, self.uri)
            Activity.startActivityForResult(intent, 0x123)

        def get_filename(self):
            while True:
                self.index += 1
                fn = '/sdcard/takepicture{}.png'.format(self.index)
                if not exists(fn):
                    return fn


class Audio:

    def __init__(self):
        pass

    class AudioRecorder(object):
        pass

    class AudioPlayer():
        def __init__(self, filename):

            self.filename = filename
            self.sound = SoundLoader.load(filename)

        def play(self):
            self.sound.play()

        def stop(self):
            self.sound.stop()

        def seek(self, position):
            self.sound.seek(position)

        @property
        def length(self):
            return self.sound.length()

        @property
        def volume(self):
            return self.sound.length()