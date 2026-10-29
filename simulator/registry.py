"""Explicit hook registry; adding a chemistry does not change the engine loop."""
from .copy import CopyChemistry
from .membrane import MembraneChemistry
from .config import COPY_DEFAULTS, MEMBRANE_DEFAULTS
from .observations import CopyObserver, VesicleObserver
from .catalysis import CatalysisChemistry,CatalysisObserver,DEFAULTS as CATALYSIS_DEFAULTS
from .membrane_bath import MembraneBathChemistry,MembraneBathObserver,DEFAULTS as BATH_DEFAULTS
from .coupled_bath import CoupledBathChemistry,CoupledBathObserver,DEFAULTS as COUPLED_DEFAULTS
from .mixing import MixingChemistry,MixingObserver,DEFAULTS as MIXING_DEFAULTS

MODELS = {"copy": (CopyChemistry, COPY_DEFAULTS, CopyObserver),
          "membrane": (MembraneChemistry, MEMBRANE_DEFAULTS, VesicleObserver),
          "catalysis": (CatalysisChemistry, CATALYSIS_DEFAULTS, CatalysisObserver),
          "membrane_bath":(MembraneBathChemistry,BATH_DEFAULTS,MembraneBathObserver),
          "coupled_bath":(CoupledBathChemistry,COUPLED_DEFAULTS,CoupledBathObserver),
          "mixing":(MixingChemistry,MIXING_DEFAULTS,MixingObserver)}


def register(name, hook, defaults, observer):
    if name in MODELS:
        raise ValueError('Chemical hook already registered: '+name)
    MODELS[name] = (hook, defaults, observer)
