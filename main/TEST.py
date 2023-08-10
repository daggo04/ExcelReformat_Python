from pathlib import Path
from ProfileApplier import ProfileApplier

def test_excel_conversion():
    print("Starting the test...")
    # Paths and filenames
    test_files = [
        "Test/Input/Fakturaavtale Alver husleie og felleskostnader.xlsx"
    ]

    # Output directory
    output_dir = Path("Test/Output")
    output_dir.mkdir(exist_ok=True)  # create output directory if it doesn't exist

    # Profile name
    profile_name = "Eye-share13.2_Nav_Convert"

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
