import urllib
from AccessControl import Unauthorized
from plone.autoform.form import AutoExtensibleForm
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from z3c.form import form
from z3c.form import button
from z3c.form.interfaces import ActionExecutionError
from zope import component
from zope import schema
from zope import interface

from collective.readitlater.i18n import _


class UrlFormSchema(model.Schema):
    url = schema.ASCIILine(title=_(u"URL"))
    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )
    tags = schema.Tuple(
        title=_(u'Tags'),
        value_type=schema.TextLine(),
        required=False
    )
    folder = schema.Choice(
        title=_(u"Folder"),
        vocabulary="collective.readitlater.vocabulary.content"
    )


class UrlFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(UrlFormSchema)

    def __init__(self, context):
        self.context = context


class UrlForm(AutoExtensibleForm, form.Form):
    schema = UrlFormSchema
    enableCSRFProtection = True
    label = _(u'Read it later')

    def update(self):
        super(UrlForm, self).update()
        self.widgets['url'].mode = 'hidden'
        if self.widgets['url'].value:
            return
        url = self.request.form.get('url', '')
        self.widgets['url'].value = url
        title = self.request.form.get('title', '')
        self.widgets['title'].value = title
        description = self.request.form.get('description', '')
        if description != 'undefined':
            self.widgets['description'].value = description
        tags = self.request.form.get('tags', '')
        if tags != 'undefined':
            self.widgets['tags'].value = tags.replace(', ', '\n')\
                .replace(',', '\n')

    @button.buttonAndHandler(_(u"Read it later"), name='submit')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        folder = self._getFolder(data['folder'])
        if folder is None:
            error = interface.Invalid(_(u'Unknown folder.'))
            raise ActionExecutionError(error)
        try:
            self._createUrl(folder, data)
        except Unauthorized:
            error = interface.Invalid(_(u'Permission denied.'))
            raise ActionExecutionError(error)
        except ValueError:
            error = interface.Invalid(_(u'Could not add to folder.'))
            raise ActionExecutionError(error)
        else:
            self.request.response.redirect('@@collective_readitlater_urladded')

    def _createUrl(self, folder, data):
        normalize = component.getUtility(IIDNormalizer)
        id = normalize.normalize(data['title'])
        if id in folder:
            i = 1
            while '%s-%d' % (id, i) in folder:
                i += 1
            id = '%s-%d' % (id, i)
        url = folder.invokeFactory(type_name='Link', id=id)
        link = folder[url]
        link.remoteUrl = data['url']
        link.title = data['title']
        link.description = data['description']
        link.subject = data['tags']
        link.reindexObject()

        # Dexterity Only
        #url = createContent('Link')
        #url.remoteUrl = data['url']
        #url.title = data['title']
        #url.description = data['description']
        #addContentToContainer(folder, url)

    def _getFolder(self, folder_uid):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(
            UID={'query': folder_uid},
        )
        if len(brains) == 0:
            return None
        brain = brains[0]
        if brain is None:
            return None
        return brain.getObject()


class UrlFormWrapper(FormWrapper):
    form = UrlForm

    def update(self):
        super(UrlFormWrapper, self).update()
        portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name="plone_portal_state"
        )
        if portal_state.anonymous():
            url = self.request.form.get('url', '')
            title = self.request.form.get('title', '')
            description = self.request.form.get('description', '')
            next_url = '@@collective_readitlater_iframe?'
            next_url += 'url=%s&title=%s&description=%s' % (
                url, title, description
            )
            next_url = urllib.quote(next_url.encode('utf-8'))
            next_url = 'login?ajax_load=1&next=%s' % next_url
            self.request.response.redirect(next_url)
