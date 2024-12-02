from typing import (
    TYPE_CHECKING, Optional
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )
    
#from simulationworkflowschema import SinglePoint
from nomad.config import config
from nomad.parsing.parser import MatchingParser
from nomad_simulations.schema_packages.model_system import AtomicCell, ModelSystem

from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.file_parser import Quantity, TextParser
#from nomad_parser_pwafqmc.schema_packages.schema_package import AFQMC
from nomad_simulations.schema_packages.general import Simulation, Program
from nomad.units import ureg
from nomad_simulations.schema_packages.outputs import Outputs
from nomad_simulations.schema_packages.properties import TotalEnergy

configuration = config.get_plugin_entry_point(
    'nomad_parser_pwafqmc.parsers:parser_entry_point'
)

class INFOGSParser(TextParser): 
    def init_quantities(self): 
        self._quantities=[
            Quantity("total_energy", 
                     r" *|TOT> total energy *: *(.*)", 
                     repeats=False, unit="rydberg"
                     ) , 
            Quantity("error_energy", 
                     r".* with error *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("psp_core_energy", 
                     r".* pseudopotential .* energy: *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("ewald_energy", 
                     r".* ewald energy .*: *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("self_energy", 
                     r".* self-energy energy .*: *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("kinetic_energy", 
                     r".* kinetic energy .*: *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("psp_local_energy", 
                     r".* psp. local energy .*: *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("psp_nonlocal_energy", 
                     r".* psp. NL energy .*: *(.*)", 
                     repeats=False, unit="rydberg"
                     ),
            Quantity("run_time", 
                     r"WALLTIME STATS\n.* Total run time = *(.*) secs", 
                     repeats=False, unit="second"
                     ),
            
        ]
        
class PWAFQMCParser(MatchingParser):        

    def parse_model_system(self, logger: 'BoundLogger') -> Optional[ModelSystem]: 
        pass 
    
    def parse_model_method(self): 
        pass 
    
    def parse_outputs(self, simulation: Simulation, logger: 'BoundLogger') -> Outputs : 
        #afqmc_output=INFOGSParser(mainfile=mainfile)
        #afqmc_output.logger=logger

        outputs=Outputs()
        if simulation.model_system: 
            outputs.model_system_ref=simulation.model_system[-1]
            
        if simulation.model_method: 
            outputs.model_method_ref=simulation.model_method[-1]
        
        # Energies 
        sec_total_energy = TotalEnergy(value=self.afqmc_output.total_energy)
        outputs.total_energies.append(sec_total_energy)    
        return outputs
    
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        print(f"I am called with {mainfile} archive {archive} logger {logger} child_archives {child_archives}")
        self.afqmc_output = INFOGSParser(mainfile=mainfile, logger=logger)
        #afqmc_output=INFOGSParser(mainfile=mainfile)
        #afqmc_output.logger=logger
        afqmc_output=self.afqmc_output

        # Adding Simulation 
        simulation = Simulation()
        archive.data = simulation 
        program = Program(name="PWAFQMC" , version="6.Petascale-028b")
        simulation.program = program 
        simulation.wall_start= 0 * ureg.second
        simulation.wall_end = afqmc_output.run_time
        

        
        # ModelSystem parsing 
        model_system=self.parse_model_system(logger)
        if model_system: 
            simulation.model_system.append(model_system)
        
        # ModelAFQMC (ModelMehtod) parsing 
        model_method=self.parse_model_method()
        if model_method: 
            simulation.model_method.append(model_method)
        
        # Output parsing
        outputs = self.parse_outputs(simulation,logger)
        simulation.outputs.append(outputs)
        print(afqmc_output.results)
        print(simulation.outputs)


        
        # Workflow section 
        #Workflow =SinglePoint() 
        #self.archive.workflow2 =Workflow 
        
        #logger.info('PWAFQMCParser.parse', parameter=configsimulationuration.parameter)
        #archive.workflow2 = Workflow(name='test-afqmc')
        
        
#PWAFQMCParser().parse(mainfile=..., archive=EntryArchive(), logger=BoundLogger())
#archive.data.outputs[0].total_energy