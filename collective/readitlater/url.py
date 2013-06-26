from zope import schema
from zope import interface

class IUrl(interface.Interface):
    """Interface for content type storing a URL"""
    url=schema.ASCIILine(title=u"URL")
