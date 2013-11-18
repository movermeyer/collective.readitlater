from AccessControl import getSecurityManager
from plone.dexterity.browser.view import DefaultView
from Products.CMFCore.permissions import ModifyPortalContent


class View(DefaultView):
    """Overide default view from dexterity to redirect to view if the user
    do not have Modify portal content permission on the context
    """

    def __call__(self):
        super(View, self).__call__()
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.getContent()):
            return self.index()
        url = self.widgets['url'].value
        self.request.response.redirect(url)
