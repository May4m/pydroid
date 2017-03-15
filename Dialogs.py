from Android import Activity
from Android import Context
from Android import PythonJavaClass
from Android import run_on_ui_thread
from Android import DatePicker, TimePicker
from Android import AlertDialog as alert_dialog
from Android.Java import Calender
from Android.Java import java_method, cast
from Android.Java import JavaImport, ArrayList, String
from kivy.factory import Factory
from kivy.event import EventDispatcher
from kivy.weakmethod import WeakMethod
from functools import partial


_ProgressDialog = JavaImport('android.app.ProgressDialog')
_AlertDialog = JavaImport('android.app.AlertDialog')
_DatePickerDialog = JavaImport('android.app.DatePickerDialog')
_TimePickerDialog = JavaImport('android.app.TimePickerDialog')


class IDialog:
    THEME_DEVICE_DEFAULT_DARK = _AlertDialog.THEME_DEVICE_DEFAULT_DARK
    THEME_DEVICE_DEFAULT_LIGHT = _AlertDialog.THEME_DEVICE_DEFAULT_LIGHT
    THEME_HOLO_DARK = _AlertDialog.THEME_HOLO_DARK
    THEME_HOLO_LIGHT = _AlertDialog.THEME_HOLO_LIGHT
    THEME_TRADITIONAL = _AlertDialog.THEME_TRADITIONAL


class OnMultiChoiceClickListener(PythonJavaClass):
    __javainterfaces__ = ['android.content.DialogInterface$OnMultiChoiceClickListener']
    __javacontext__ = 'app'

    def __init__(self, on_click=None):
        self._on_click = WeakMethod(on_click) if on_click else None
        super(OnMultiChoiceClickListener, self).__init__()

    @java_method('(Landroid/content/DialogInterface;IZ)V')
    def onClick(self, dialog, which, is_checked):
        self.on_click(dialog, which, is_checked)

    def on_click(self, dialog, which, is_checked):
        if self._on_click:
            call = self._on_click()
            call(dialog, which, is_checked)


class BaseListener(PythonJavaClass):
    __javainterfaces__ = ['android.content.DialogInterface$OnClickListener',
                          'android.content.DialogInterface$OnCancelListener',
                          'android.content.DialogInterface$OnDismissListener',
                          'android.app.TimePickerDialog$OnTimeSetListener']
    __javacontext__ = 'app'

    def __init__(self, on_click=None, on_cancel=None,
           on_dismiss=None, on_time_set=None):

        self._on_click = WeakMethod(on_click) if on_click else None
        self._on_cancel = WeakMethod(on_cancel) if on_cancel else None
        self._on_dismiss = WeakMethod(on_dismiss) if on_dismiss else None
        self._on_time_set = WeakMethod(on_time_set) if on_time_set else None

        super(BaseListener, self).__init__()
        

    @java_method('(Landroid/content/DialogInterface;I)V')
    def onClick(self, dialog, which):
        self.on_click(dialog, which)

    def on_click(self, dialog, which):
        if self._on_click:
            call = self._on_click()
            call(dialog, which)


    @java_method('(Landroid/content/DialogInterface;)V')
    def onCancel(self, dialog):
        self.on_cancel(dialog)

    def on_cancel(self, dialog):
        if self._on_cancel:
            call = self._on_cancel()
            call(dialog)

    @java_method('(Landroid/content/DialogInterface;)V')
    def onDismiss(self, dialog):
        self.on_dismiss(dialog)

    def on_dismiss(self, dialog):
        if self._on_dismiss:
            call = self._on_dismiss()
            call(dialog)

    @java_method('(Landroid/widget/TimePicker;II)V')
    def onTimeSet(self, time_picker, hour, minute):
        self.on_time_set(time_picker, hour, minute)

    def on_time_set(self, view, hour, minute):
        if self._on_time_set:
            call = self._on_time_set()
            call(time_picker, hour, minute)


class ProgressDialog(EventDispatcher, IDialog):

    STYLE_HORIZONTAL = _ProgressDialog.STYLE_HORIZONTAL
    STYLE_SPINNER = _ProgressDialog.STYLE_SPINNER

    def set_progress_style(self, _style):
        self.dialog.setProgressStyle(_style)

    def set_progress(self, value):
        self.dialog.setProgress(value)

    def get_progress(self):
        return self.dialog.getProgress()

    progress = Factory.NumericProperty()

    max = Factory.NumericProperty()

    @run_on_ui_thread
    def __init__(self, message, title=None,
                 set_indeterminate=True,
                 set_cancelable=True):
        super(ProgressDialog, self).__init__()

        self.register_event_type('on_cancel')
        self.dialog = _ProgressDialog(Activity)
        if title:
            self.dialog.setTitle(String(title))
        self.dialog.setMessage(String(message))
        #self.dialog.setIndeterminate(set_indeterminate)
        self.dialog.setCancelable(set_cancelable)

        on_cancel_listener = BaseListener(on_cancel=_on_cancel)
        self.dialog.setOnCancelListener(on_cancel_listener)

        self.bind(progress=self._set_progress,
                  max=self._set_max)

    def _set_max(self, instance, value):
        self.dialog.setMax(value)

    def _set_progress(self, instance, value):
        self.set_progress(value)

    def set_button(self, id, text, callback):
        self.dialog.setButton(id, String(text), BaseListener(callback))
        
    @property
    def is_indeterminate(self):
        return self.dialog.isIndeterminate()

    @run_on_ui_thread
    def show(self):
        return self.dialog.show()

    def _on_cancel(self, dialog):
        dialog.dismiss()
        self.dispatch('on_cancel', dialog)

    def on_cancel(self, *args):
        pass

    def dismiss(self):
        self.dialog.dismiss()


class AlertDialog(EventDispatcher, IDialog):

    def __init__(self, message=None, title=None, theme=IDialog.THEME_HOLO_LIGHT):
        super(AlertDialog, self).__init__()

        self.register_event_type('on_positive')
        self.register_event_type('on_negative')
        self.register_event_type('on_neutral')

        self.dialog = None
        self.message = message
        if theme:
            # create a dialog with a theme
            self.builder = alert_dialog(cast('android.app.Activity', Activity), theme)
        else:
            self.builder = alert_dialog(cast('android.app.Activity', Activity))

        if self.message:
            self.builder.setMessage(String(self.message))
        if title:
            self.builder.setTitle(String(title))

    def set_positive_button(self, text, on_click=None):
        self.builder.setPositiveButton(String(text),
		  BaseListener(on_click if on_click and callable(on_click) else self._on_positive)
          )

    def set_negative_button(self, text, on_click=None):
        self.builder.setNegativeButton(String(text),
          BaseListener(on_click if on_click and callable(on_click) else self._on_negative)
          )

    def set_items(self, array, on_click):
        items = list(String(i) for i in array)
        self.builder.setItems(items, BaseListener(on_click))

    def set_single_choice_items(self, array, on_click):
        items = list(String(i) for i in array)
        self.builder.setSingleChoiceItems(items, 0, BaseListener(on_click))

    def set_multi_choice_items(self, dict_items, on_click):
        """
        items = {'Monday': True, 'Tuesday': True, 'Wednesday': False}
        set_multi_choice_items(items, lambda dialog, id: None)
        """
        keys = list(String(i) for i in dict_items.keys())
        values = list(i for i in dict_items.values())
        self.builder.setMultiChoiceItems(keys, values, OnMultiChoiceClickListener(on_click))

    def set_neutral_button(self, text):
        self.builder.setNeutralButton(String(text), BaseListener(self._on_neutral))

    def _on_neutral(self, *args):
        self.dispatch('on_neutral', *args)

    def on_neutral(self, *args):
        pass

    def answer(self, answer):
        self.callback(answer)

    def _on_positive(self, *args):
        self.dispatch('on_positive', *args)

    def _on_negative(self, *args):
        self.dispatch('on_negative', *args)

    def on_positive(self, *args):
        pass

    def on_negative(self, *args):
        pass

    @run_on_ui_thread
    def show(self):
        self.dialog = self.builder.create()
        self.dialog.show()


class TimePickerDialog(EventDispatcher, IDialog):

    calender = Calender.getInstance()
    hour = Factory.NumericProperty(calender.get(Calender.HOUR_OF_DAY))
    minute = Factory.NumericProperty(calender.get(Calender.MINUTE))

    __events__ = ('on_time_set',)

    @run_on_ui_thread
    def __init__(self, hour=None, minute=None):
        if hour:
            self.hour = hour
        if minute:
            self.minute = minute

        super(TimePickerDialog, self).__init__()

        listener = BaseListener(on_time_set=self._on_time_set)       
        self.dialog = _TimePickerDialog(Activity, listener, self.hour, self.minute, True)

    @run_on_ui_thread
    def set_theme(self, theme):
        self.dialog.setTheme(theme)

    def on_time_set(self, *args):
        pass

    def _on_time_set(self, view, hour, minute):
        self.hour = hour
        self.minute = minute
        self.dipatch('on_time_set', view, hour, minute)

    @run_on_ui_thread
    def show(self):
        self.dialog.show()