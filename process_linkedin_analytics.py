import csv
import datetime
import os
import re

#script_path = "/Users/salvadorcostas/Documents/MarketingContextFiles/"
script_path = "C:/Users/cbello/Documents/RAW Data"


def process_file(input_file, output_file,region):
    with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
        # Create CSV reader and writer objects
        reader = csv.reader(csv_in)
        writer = csv.writer(csv_out, quoting=csv.QUOTE_NONE)  # Disable quoting

        first_line = csv_in.readline().strip()

        # Extract the date (assuming it's the first word in the file)
        file_date = first_line.split(',')[0].replace('"', '')

        # Parse the extracted date (assuming it's in the format YYYYMMDD)
        parsed_date = datetime.datetime.strptime(file_date, '%m/%d/%Y')

        # Format the date as "Month - Year"
        formatted_date = parsed_date.strftime('%B-%Y')


        # Skip the first row (header) in the input file
        #next(reader, None)

        # Read the header from the input file
        header = next(reader, None)

        # Add 'Date' to the header
        header.append('Date')

        # Add 'REGION' to the header
        header.append('Region')

        # Write the updated header to the output file
        writer.writerow(header)

        # Get the current date
        current_date = formatted_date

        # Write the remaining rows with the added date column
        for row in reader:
            row.append(current_date)
            row.append(region)
            writer.writerow(row)


    print(f'The first line has been removed, and the result has been saved to {output_file}.')


def is_ctx_folder(folder_path):
    # Get the base name of the folder (the last part of the path)
    folder_name = os.path.basename(folder_path)

    # Check if the folder name starts with "CTX -"
    return folder_name.startswith("CTX -")

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")


def process_files_in_folder(folder,folder_path, output_folder):
    csv_pattern = re.compile(r'.*\.csv$', re.IGNORECASE)
    region = folder[len('CTX - '):]  # Remove the prefix
    create_folder(output_folder)

    # List files in the specified folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file_name in files:
        if csv_pattern.match(file_name):
            print("filename "+file_name)
            input_file = os.path.join(folder_path, file_name)
            output_file = os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}_processed.csv')

            # Check if the file is not already processed
            if not os.path.exists(output_file):
                process_file(input_file, output_file, region)

def process_files_in_all_folders(script_path):
    # Get the path of the script's directory
    script_dir = os.path.abspath(script_path)
    print("  script dir  " + script_dir)
    #script_dir = "script_path"

    # Iterate through all subdirectories
    for root, dirs, files in os.walk(script_dir):
        for folder in dirs:

            if is_ctx_folder(folder):
                folder_path = os.path.join(root, folder)
                #print("folder"+folder)
                print("folder_path: "+folder_path)
                output_folder = os.path.join(folder_path, 'output')  # Adjust as needed
                #print("folder_path" + output_folder)
                process_files_in_folder(folder,folder_path, output_folder)


# Example usage:
#input_file_name = "example.csv"
#output_file_name = "example_mofified.csv"

process_files_in_all_folders(script_path)
