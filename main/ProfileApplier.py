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
        operations = self.profile['operations']

        #Seperate set_column operations from other operations to determine the order of operations (set_column operations should be done last)
        # This is because set_column needs to know the last populated row in the sheet
        set_column_operations = [op for op in operations if op['type'] == 'SET_COLUMN']
        operations = [op for op in operations if op['type'] != 'SET_COLUMN']
        
        for operation in operations:
            op_type = operation['type']
            params = operation['parameters']

            if op_type == "COPY_COLUMN":
                self.handler.copy_column(
                    src_sheet=params['srcSheet'],
                    src_col=int(params['srcCol']),
                    dst_sheet=params['dstSheet'],
                    dst_col=int(params['dstCol']),
                    start_row=int(params.get('startRow', 2)),
                )
            elif op_type == "COPY_SPLIT_ROW":
                self.handler.copy_split_row(
                    src_sheet=params['srcSheet'],
                    dst_sheet=params['dstSheet'],
                    start_row=int(params['startRow']),
                    col_map=params['colMap'],
                    include_headers=params.get('includeHeaders', False),
                    header_col=int(params.get('headerCol', 0))
                )
            #TODO: Extend this to other operations
            
            
        for operation in set_column_operations:
            op_type = operation['type']
            params = operation['parameters']
            print(params)
            
            if op_type == "SET_COLUMN":
                self.handler.set_column_value(
                        sheet=params['sheet'],
                        col=int(params['col']),
                        value=params['value'],
                        start_row=int(params.get('startRow', 2)),
                        end_row=int(params.get('endRow', -1))
                    )


    def save_output(self, output_path: Path):
        self.handler.save_output_workbook(output_path)
