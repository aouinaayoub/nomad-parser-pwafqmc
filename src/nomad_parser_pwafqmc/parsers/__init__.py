from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class PWAFQMCEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_parser_pwafqmc.parsers.parser import PWAFQMCParser

        return PWAFQMCParser(**self.dict())


parser_entry_point = PWAFQMCEntryPoint(
    name='PWAFQMCParser',
    description='Parser for PWAFQMC code.',
    mainfile_name_re='.*INFO-GS',   # have to start with ".*" !  
    mainfile_contents_re='Planewave-AFQMC calculation *'
)
