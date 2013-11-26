import unittest2 as unittest
from collective.readitlater.tests import base
from collective.readitlater.browser import add_url
from plone.protect import createToken


class TestURLForm(base.IntegrationTestCase):

    def test_form_adapter(self):
        adapter = add_url.UrlFormSchema(self.portal)
        self.assertTrue(hasattr(adapter, "url"))
        self.assertTrue(hasattr(adapter, "title"))
        self.assertTrue(hasattr(adapter, "description"))
        self.assertTrue(hasattr(adapter, "tags"))
        self.assertTrue(hasattr(adapter, "folder"))
        self.assertEqual(type(adapter.url), str)
        self.assertEqual(type(adapter.title), unicode)
        self.assertEqual(type(adapter.description), unicode)
        self.assertEqual(type(adapter.tags), tuple)
        self.assertIsNone(adapter.folder)

    def test_form(self):
        token = createToken()
        self.request.form = {
            "url": "http://example.com",
            "title": "my example page",
            "description": "an example description",
            "tags": "tag1,tag2, tag3",
        }
        form = add_url.UrlForm(self.portal, self.request)
        #test update
        form.update()
        self.assertEqual(form.widgets['url'].mode, 'hidden')
        self.assertEqual(form.widgets['title'].value, 'my example page')
        self.assertEqual(form.widgets['description'].value,
                         'an example description')
        self.assertEqual(form.widgets['tags'].value, 'tag1\ntag2\ntag3')
        folder = self.portal['test-folder']
        folder_uid = folder.UID()
        self.assertEqual(len(folder.objectIds()), 0)
        #test handleApply
        self.request.form = {
            "form.widgets.folder": folder_uid,
            "form.widgets.url": 'http://example.com',
            "form.widgets.title": u'my example page',
            "form.widgets.description": u'my example page',
            "form.widgets.tags": u"tag1\ntag2\ntag3",
            "form.buttons.submit": u'Read it later',
            "_authenticator": token
        }
        """(Pdb) form.actions
        <AuthenticatedButtonActions None>
        (Pdb) form.actions.values()[0]
        <ButtonAction 'form.buttons.submit' u'Read it later'>
        """
        form.update()
        folder = self.portal['test-folder']
        self.assertEqual(len(folder.objectIds()), 1)
        link = folder['my-example-page']
        self.assertEqual(link.Title(), 'my example page')
        self.assertEqual(link.Description(), 'my example page')
        self.assertEqual(link.Subject(), ('tag1', 'tag2', 'tag3'))
        self.assertEqual(link.remote_url(), "http://example.com")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
