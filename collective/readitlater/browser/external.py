from Products.Five.browser import BrowserView


class ShowAll(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.url = 'http://localhost:8080/Plone/@@collective_readitlater_script'
        self.script = "javascript:void((function(){"
        self.script += "var%20hsb=document.createElement('script');"
        self.script += "hsb.setAttribute('src','%s');" % self.url
        self.script += "hsb.setAttribute('type','text/javascript');"
        self.script += "document.getElementsByTagName('head')[0].appendChild(hsb);"
        self.script += "})());"
        return self.index()


class IFrame(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.url = self.request.form.get("url", "")
        return self.index()


class Script(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.url_iframe = 'http://localhost:8080/Plone/@@collective_readitlater_iframe'
        self.url_css = 'http://localhost:8080/Plone/@@collective_readitlater_style'
        self.request.response.setHeader('Content-Type',
                                        'text/javascript')
        return self.index()


class Style(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.setHeader('Content-Type',
                                        'text/css')
        return self.index()
