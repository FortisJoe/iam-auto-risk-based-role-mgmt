"""An optional package init file for the component."""

from idmlib.components import component_log
from idmlib.components.hook import Hooks
from .model import RiskClassficiationEvalTreatmentLookup


module_log = component_log.getChild(__package__)


class ComponentHooks(Hooks):
    """Component Hooks subclass.

    :var component: The Component object.
    :var file in_hdl: The input handle to use for user interaction.
    :var file out_hdl: The output handle to use for user interaction.

    """

    def hook_install(self):
        """Hook that is called on component install."""

        log = module_log.getChild('install')

        log.info('Creating table if necessary')

        RiskClassficiationEvalTreatmentLookup.create_model()

        log.info('Done')

    def hook_remove(self):
        """Hook that is called on component removal."""

        log = module_log.getChild('remove')

        log.info('Removing table')

        RiskClassficiationEvalTreatmentLookup.remove_model()

        log.info('Done')
