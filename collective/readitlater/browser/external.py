from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope import interface


class IShowAll(interface.Interface):
    def getBookmark():
        """ Get script to bookmark """


class ShowAll(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.getBookmark()
        return self.index()

    def getBookmark(self):
        context = self.context.aq_inner
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state'
        )
        path = portal_state.navigation_root_url()
        self.url = '%s/@@collective_readitlater_script' % path
        self.script = (
            "javascript:void((function(){"
            "var%20hsb=document.createElement('script');"
            "hsb.setAttribute('src','%s');"
            "hsb.setAttribute('type','text/javascript');"
            "document.getElementsByTagName('head')[0].appendChild(hsb);"
            "})());"
        ) % self.url
        return self.script


class Script(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context.aq_inner
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state'
        )
        path = portal_state.navigation_root_url()
        self.url_iframe = '%s/@@collective_readitlater_iframe' % path
        self.url_css = '%s/@@collective_readitlater_style' % path
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
