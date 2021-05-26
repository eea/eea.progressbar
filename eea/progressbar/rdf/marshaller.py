""" RDF Marshaller module for progressbar """
import surf
from zope.component import adapts, queryAdapter
from zope.interface import implements
from eea.progress.workflow.interfaces import IBaseObject, IWorkflowProgress
from eea.rdfmarshaller.interfaces import ISurfResourceModifier


class ProgressLevelSurfModifier(object):
    """ Progress Level workflow surf information
    """

    implements(ISurfResourceModifier)
    adapts(IBaseObject)

    def __init__(self, context):
        self.context = context
        surf.ns.register(wf="http://intelleo.eu/ontologies/workflow/ns#")

    def run(self, resource, *args, **kwds):
        """ Adds the wf progress level rdf resource
            <wf:currentStatus>
              <wf:DetailedProgressStatus  rdf:about="workflow_progress_level">
                <wf:progressLevel>30</wf:progressLevel>
              </wf:DetailedProgressStatus>
            </wf:currentStatus>
        """
        context = self.context
        output = []
        progress = queryAdapter(context, IWorkflowProgress)
        if not progress:
            return output
        session = resource.session
        try:
            store = session.default_store
        except AttributeError:
            store = session.get_default_store()

        progress_level = progress.progress
        wf_surf = surf.ns.WF
        store.reader.graph.bind('wf', wf_surf, override=True)
        details_progress = session.get_class(surf.ns.WF.DetailedProgressStatus)
        rdfp = session.get_resource("#workflow_state_progress",
                                    details_progress)
        rdfp[surf.ns.WF['progressLevel']] = progress_level
        rdfp.update()

        output.append(rdfp)
        resource['wf_currentStatus'] = output
        resource.save()
