from AccessControl import getSecurityManager
from plone.i18n.normalizer.base import baseNormalize
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def contentVocabulary(context):
    sm = getSecurityManager()
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.searchResults(
        Type={'query': 'Folder'},
    )
    terms = []
    for brain in brains:
        if sm.checkPermission('collective.readitlater: addUrl', brain.getObject()):
            terms.append(SimpleTerm(
                baseNormalize(brain.UID),
                baseNormalize(brain.UID),
                brain.Title.decode('utf-8')
            ))
    return SimpleVocabulary(terms)
