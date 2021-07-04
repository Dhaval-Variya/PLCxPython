#######################################################
#  THIS CODE HAS BEEN OMITTED DUE TO CONFIDENTIALITY  #
#  DO NOT RUN THIS CODE.                              #
#######################################################

from functools import partial
from Settings import SettingWindow as sw
from Recording import Recording as rec


class PyPlcMonitorCtrl:
    """PyPLC Monitor's Controller."""

    def __init__(self, view):
        """Controller initialization."""
        self._view = view
        # self._model = model
        self._connect_buttons()
        self._connect_counters()
        self._connect_charts()

    def _settings(self):
        """Pop-up settings dialog"""
        print("Settings")
        # setting = sw(self._view)

    def _recording(self):
        """Perform screen recording."""
        print("Recording")

    def _connect_buttons(self):
        """Connect slots for buttons.
        - Settings
        - Screen recording
        """
        print("Conecting buttons")
        self._view.settings_btn.clicked.connect(
            self._settings
        )
        print("Connected Settings")
        self._view.recording_btn.clicked.connect(self._recording)
        print("Connected record screen")

    def _connect_counters(self):
        pass

    def _connect_charts(self):
        pass
