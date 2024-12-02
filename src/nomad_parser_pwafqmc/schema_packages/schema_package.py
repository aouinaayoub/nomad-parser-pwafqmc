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
import numpy as np

configuration = config.get_plugin_entry_point(
    'nomad_parser_pwafqmc.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class NewSchemaPackage(Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    message = Quantity(type=str)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        logger.info('NewSchema.normalize', parameter=configuration.parameter)
        self.message = f'Hello {self.name}!'



class AFQMC(Schema):
    
    #flat_info = Quantity(type=JSON)    
    # # INPUT FILE 
    # kpt_red = Quantity(type=float, shape=['3'])
    # n_indp_det = Quantity(type=int)
    # nwlk = Quantity(type=int)
    # nwlk_min = Quantity(type=int)
    # nwlk_max = Quantity(type=int)
    # if_calc_dens = Quantity(type=int)
    
    # # random number generator               
    # rng_type = Quantity(type=int)
    # sprng_seed =Quantity(type=int)
    
    # nblkstep = Quantity(type=int)             # steps per block   
    # itv_Em =    Quantity(type=int)            # steps per measurement (recommend nblkstep/itv_Em=integer)
    # nreq=     Quantity(type=int)           # number of blocks in equilibrium phase
    # nblk=       Quantity(type=int)           # number of blocks in measurement phase
    # deltau =    Quantity(type=float)          # step length [Ry^-1] 
    # etrial =    Quantity(type=float, unit="rydberg")             # one electron cntrib from DFT output 
    
    # # pop control and orthonormalization                       
    # itv_pc_eq= Quantity(type=int)            # steps per population control in equilibration phase
    # itv_pc= Quantity(type=int)           # steps per population control in measurement phase
    # itv_modgs= Quantity(type=int)                    # steps per modified Gram-schmidt orthonormalization 
    # backpro= Quantity(type=int)                      # 1=back-propagation on 
    # itv_bp= Quantity(type=int)                    # BP-run interval (in steps)
    # itv_bpstore= Quantity(type=int)              # how many actual BP steps in a BP-run     
    
    
    # grid_num = Quantity(type=np.int32, shape=['3'])         # FFT grid 
    # grid_origin = Quantity(type=np.float32, shape=['3'])
    # grid_vector = Quantity(type=np.float32, shape=['(3,3)']) 
    # ECUT =Quantity(type=float, unit="rydberg")
    
    # INFO - GS
    total_energy= Quantity(type=float, unit='rydberg')

    
    def normalize(self,archive,logger):
        if not (n_indp_det in [1,2]):
            raise ValueError("n_indpt_det is invalid") 
        

m_package.__init_metainfo__()
