from zope import schema

from plone.supermodel import model


class IUrl(model.Schema):
    """Interface for content type storing a URL"""
    url=schema.ASCIILine(title=u"URL")
    title=schema.ASCIILine(title=u"Title")
    description=schema.ASCIILine(title=u"Description")
