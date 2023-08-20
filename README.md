# Excel Converter Web App
## Description
This web application provides a simple interface for converting Excel documents from one format to another based on a predefined set of JSON profiles and an Excel template. It is built using Flask and the openpyxl library.

## Features
- Upload multiple Excel files for conversion
- Select a profile to apply to the uploaded files
- Convert files based on the selected profile
- Download the converted files

## Usage
A demo for the application can be found [here](https://excelreformat.azurewebsites.net).

1. pload Excel Files: Drag and drop or select Excel files for upload (.xls and .xlsx file types are supported).
2. Select a Profile: Choose a profile from the dropdown menu. Profiles are JSON files containing instructions for converting Excel documents.
3. Convert Files: Click the "Convert" button to start the conversion process.
4. Download Files: Once the conversion is complete, download the converted files.

--- 
## Installation
1. Clone the repository.
2. Install the required dependencies by `running pip install -r requirements.txt``.
3. Run the Flask app with flask run.
### Configuration
- `MAX_FILES`: Maximum number of files that can be uploaded at once (default is 10).
- `MAX_TOTAL_SIZE_MB`: Maximum total size of all uploaded files in MB (default is 10 MB).
- `ALLOWED_EXTENSIONS`: Allowed file extensions for upload (default is {`xlsx`, `xls`}).
## Custom Profiles
Profiles are JSON files that define how to convert Excel documents. The application comes with a few predefined profiles, but you can create your own by following the profile schema.

## Credits
This project was developed by Dag Himle.