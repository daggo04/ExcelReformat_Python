from pathlib import Path
from main.ProfileApplier import ProfileApplier
import openpyxl

def test_excel_conversion():
    print("Starting the test...")
    # Paths and filenames
    test_files = [
        "ΩTest/_input/Fakturaavtale Alver husleie og felleskostnader.xlsx"
    ]

    # wb = openpyxl.load_workbook("resources/templates/Eye-Share_ImportMal13.1.2.xlsx")
    # print(wb.sheetnames)
    # print(wb.defined_names.values())
    
    #     # Loop over each worksheet in the template workbook
    # for sheet in wb.worksheets:
    #     # Loop over each name defined in the worksheet
    #     for defined_name in sheet.defined_names.values():
    #         print(defined_name.name)

    # Output directory
    output_dir = Path("ΩTest/_output")
    output_dir.mkdir(exist_ok=True)  # create output directory if it doesn't exist

    # Profile name
    profile_name = "Eye-Share_Nav-Convert_V3.1.2"

    # Process each file
    for file_path in test_files:
        input_excel = Path(file_path)
        output_excel = output_dir / (input_excel.stem + "_converted.xlsx")

        # Instantiate, apply and save
        applier = ProfileApplier(input_excel=input_excel, profile_name=profile_name)
        applier.apply()
        applier.save_output(output_excel)

        print(f"Processed {input_excel.name} -> {output_excel.name}")

test_excel_conversion()
