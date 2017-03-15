# Android Hardware support

from Android import JavaImport


Hardware = JavaImport('org.renpy.android.Hardware')


def Vibrate(time=1.0):
    Hardware.vibrate(time)


class Accelerometer(object):

    @staticmethod
    def reading():
        x, y, z = Hardware.accelerometerReading()
        return [x, y, z]

    @staticmethod
    def disable():
        Hardware.accelerometerEnable(False)

    @staticmethod
    def enable():
        Hardware.accelerometerEnable(True)


class MagneticField(object):

    @staticmethod
    def reading():
        x, y, z = Hardware.magneticFieldSensorReading()
        return [x, y, z]

    @staticmethod
    def disable(value=True):
        Hardware.magneticFieldSensorEnable(not value)

    @staticmethod
    def enable():
        Hardware.magneticFieldSensorEnable(True)