""" Browser controllers
"""
from Products.Five.browser import BrowserView

class ZMIStateProgressEdit(BrowserView):
    """ ZMI edit for state progress monitoring
    """

    def setProperties(self, form):
        """ Update properties
        """
        progress = form.get('progress', 0)
        self.context.progress = progress

    def __call__(self, **kwargs):
        form = self.request.form
        form.update(kwargs)

        submit = form.get('submit', None)
        if not submit:
            return self.index()

        self.setProperties(form)

        redirect = form.get('redirect', self.__name__)
        self.request.response.redirect(
            redirect + '?manage_tabs_message=Changes saved')

class ZMIWorkflowProgressEdit(BrowserView):
    """ ZMI edit for workflow progress monitoring
    """
    def states(self):
        """ Defined states
        """
        def compare(a, b):
            """ Sort
            """
            a_progress = getattr(a[1], 'progress', None) or 0
            b_progress = getattr(b[1], 'progress', None) or 0
            return cmp(a_progress, b_progress)

        items = self.context.states.items()
        items = sorted(items, cmp=compare)
        return items
