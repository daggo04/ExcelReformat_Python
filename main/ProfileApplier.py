import json
from pathlib import Path
from typing import Dict
from main.ExcelHandler import ExcelHandler

class ProfileApplier:
    def __init__(self, input_excel: Path, profile_name: str, profiles_dir: Path = Path("resources/profiles")):
        self.input_excel = input_excel
        self.profile_path = profiles_dir / f"{profile_name}.json"

        # Load profile
        with open(self.profile_path, 'r') as profile_file:
            self.profile = json.load(profile_file)

        template_path = Path("resources") / self.profile['templatePath']
        self.handler = ExcelHandler(self.input_excel, template_path)

    def apply(self):
        print(f"Applying profile for {self.input_excel.name}")
        operations = self.profile['operations']

        for operation in operations:
            op_type = operation['type']
            params = operation['parameters']

            if op_type == "COPY_COLUMN":
                print(f"Copying column {params['srcCol']} from {params['srcSheet']} to column {params['dstCol']} in {params['dstSheet']}")
                self.handler.copy_column(
                    src_sheet=params['srcSheet'],
                    src_col=int(params['srcCol']),
                    dst_sheet=params['dstSheet'],
                    dst_col=int(params['dstCol']),
                    start_row=int(params.get('startRow', 2)),
                )
            elif op_type == "COPY_SPLIT_ROW":
                print(params)
                print(f"Copying split row from sheet {params['srcSheet']} to sheet {params['dstSheet']} starting from row {params['startRow']}")
                self.handler.copy_split_row(
                    src_sheet=params['srcSheet'],
                    dst_sheet=params['dstSheet'],
                    start_row=int(params['startRow']),
                    col_map=params['colMap'],
                    include_headers=params.get('includeHeaders', False),
                    header_col=int(params.get('headerCol', 0))
                )
            #TODO: Extend this to other operations

    def save_output(self, output_path: Path):
        print(f"Saving output to {output_path}")  
        self.handler.save_output_workbook(output_path)
