from idmlib.components.test import CommonTest
from unittest.mock import MagicMock, patch

from Functional.hid_global_configuration.config import ConfigData


class TestRiskTreatment(CommonTest):

    @patch.object(ConfigData, "get_rows")
    def test_take_no_action(self, get_rows):
        get_rows.return_value = list()

