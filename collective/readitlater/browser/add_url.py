from zope import component
from zope import interface

from plone.autoform.form import AutoExtensibleForm
from plone.z3cform.layout import FormWrapper

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form import form
from z3c.form import button

from collective.readitlater.url import IUrl


class UrlFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(IUrl)

    def __init__(self, context):
        self.context = context
        self.url = None
        #import pdb; pdb.set_trace()


class UrlForm(AutoExtensibleForm, form.Form):
    schema = IUrl
    enableCSRFProtection = True
    label = 'Read it later'

    @button.buttonAndHandler(u"Read it later")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = "Errors !"
            return
        if data.has_key['url']:
            print data['url']


class UrlFormWrapper(FormWrapper):
    form = UrlForm
