from Android.Java import JavaImport, PythonJavaClass
from Android.Java import run_on_ui_thread, java_method
from Android import Activity

from kivy.event import EventDispatcher
from kivy.factory import Factory


_WebView = JavaImport('android.webkit.WebView')


class WebViewClient(PythonJavaClass):
    __javainterfaces__ = ['android/webkit/WebViewClient']
    __javacontext__ = 'app'

    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
    def onPageFinished(self, web_view, url):
        self.on_page_finished(web_view, url)

    def on_page_finished(self, *args):
        pass

    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;Landroid/graphics/Bitmap;)V')
    def onPageStarted(self, web_view, url, image):
        self.on_page_started(web_view, url, image)

    def on_page_started(self, *args):
        pass


class WebBrowser(EventDispatcher):

    address = Factory.StringProperty()
    background_color = Factory.NumericProperty()
    html_data = Factory.StringProperty()
    clear_cache = Factory.BooleanProperty()

    __events__ = ('on_address', 'on_background_color', 'on_html_data', 'on_clear_cache')

    @run_on_ui_thread
    def __init__(self, address='http://www.kivy.org'):
        if address:
            self.address = address
        self.web_view = _WebView(Activity)
        self.web_client_view = WebViewClient()
        self.web_view.setWebViewClient(self.web_client_view)
        if self.address:
            self.web_view.loadUrl(self.address)

    def on_address(self, instance, value):
        self.web_view.loadUrl(self.address)

    def on_background_color(self, instance, value):
        self.web_view.setBackgroundColor(value)

    def on_html_data(self, instance, value):
        self.web_view.loadData(value)

    @property
    def can_go_back(self):
        """
        Returns True if WebView can return to the previous page
        """
        return self.web_view.canGoBack()

    @property
    def can_go_forward(self):
        """
        Returns True if WebView can return to the forward page
        """
        return self.web_view.canGoForward()

    def on_clear_cache(self, instance, value):
        """
        Clears the cached data, images and conent
        """
        self.web_view.clearCache(value)

    def clear_form_data(self):
        """
        Clear the data on forms
        """
        self.web_view.clearFormData()

    def clear_history(self):
        self.web_view.clearHistory()

    def destroy(self):
        self.web_view.destroy()

    def get_content_height(self):
        """
        returns the height of the rendered content
        returns: `int`
        """
        return self.web_view.getContentHeight()

    def get_favicon(self):
        """
        returns the favicon
        returns:`<class android.graphics.Bitmap>`
        """
        return self.web_view.getFavicon()

    def get_original_url(self):
        """
        returns the url loaded when first initialized
        return: `str`
        """
        return str(self.web_view.getOriginalUrl())

    def get_title(self):
        """
        returns the web page title
        return: `str`
        """
        return str(self.web_view.getTitle())

    def get_url(self):
        """
        return: `str`
        """
        return str(self.web_view.getUrl())

    def go_back(self):
        """
        returns to the previous page
        """
        self.web_view.goBack()

    def go_forward(self):
        self.web_view.goForward()

    def reload(self):
        self.web_view.reload()