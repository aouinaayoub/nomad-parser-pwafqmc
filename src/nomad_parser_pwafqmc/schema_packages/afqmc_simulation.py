from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Quantity, SchemaPackage
from nomad_simulations.schema_packages.general import Simulation 
import numpy as np

configuration = config.get_plugin_entry_point(
    'nomad_parser_pwafqmc.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class AFQMCSimulation(Simulation):
    sprng_seed = Quantity(type=int) 

m_package.__init_metainfo__()
