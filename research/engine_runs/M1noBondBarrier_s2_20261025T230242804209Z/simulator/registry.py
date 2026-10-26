"""Explicit hook registry; adding a chemistry does not change the engine loop."""
from .copy import CopyChemistry
from .membrane import MembraneChemistry
from .config import COPY_DEFAULTS, MEMBRANE_DEFAULTS
from .observations import CopyObserver, VesicleObserver
from .catalysis import CatalysisChemistry,CatalysisObserver,DEFAULTS as CATALYSIS_DEFAULTS
from .membrane_bath import MembraneBathChemistry,MembraneBathObserver,DEFAULTS as BATH_DEFAULTS

MODELS = {"copy": (CopyChemistry, COPY_DEFAULTS, CopyObserver),
          "membrane": (MembraneChemistry, MEMBRANE_DEFAULTS, VesicleObserver),
          "catalysis": (CatalysisChemistry, CATALYSIS_DEFAULTS, CatalysisObserver),
          "membrane_bath":(MembraneBathChemistry,BATH_DEFAULTS,MembraneBathObserver)}


def register(name, hook, defaults, observer):
    if name in MODELS:
        raise ValueError('Chemical hook already registered: '+name)
    MODELS[name] = (hook, defaults, observer)
