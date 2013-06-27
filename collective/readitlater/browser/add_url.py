from plone.autoform.form import AutoExtensibleForm
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import form
from z3c.form import button
from zope import component
from zope import schema
from zope import interface
from collective.readitlater.i18n import _
from collective.readitlater.url import IUrl


class UrlFormSchema(IUrl):
    content = schema.Choice(
        title=_(u"Content"),
        vocabulary="collective.readitlater.vocabulary.content"
    )


class UrlFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(UrlFormSchema)

    def __init__(self, context):
        self.context = context
        self.url = None
        #import pdb; pdb.set_trace()


class UrlForm(AutoExtensibleForm, form.Form):
    schema = UrlFormSchema
    enableCSRFProtection = True
    label = _(u'Read it later')

    @button.buttonAndHandler(_(u"Read it later"))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = "Errors !"
            return
        if data.has_key['url']:
            print data['url']


class UrlFormWrapper(FormWrapper):
    form = UrlForm
