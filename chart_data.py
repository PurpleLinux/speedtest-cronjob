import json
import re
from make_graph import plot

def print_formatted_json(data):
    formatted_json = json.dumps(data, indent=2)
    print(formatted_json)

# Specify your input file and list of speedtest json objects
input_file_path = 'speedtest_data.json'
speedtest_list = []

# Open the file and read 45 lines at a time
with open(input_file_path, 'r') as file:


    # line represents the json block of 1 speedtest, and i is the line number within that block
    lines = ""
    i = 1
    
    while True:

        # Read the line
        line = file.readline()

        # Break the loop if there are no more lines
        if not line:
            break

        # Strip the line after checking 'if not line' to prevent empty lines from breaking the loop
        line = line.strip()
        
        # if the patter matches '"speedtest": {' and this isn't the second line (i.e. the first
        # occurance of '"speedtest": {'), reset the block
        if i > 2 and line == '"speedtest": {':
            i = 1

            # Remove the '{' from the end
            lines = lines[:-1]

            # NOTE: START OF CORRECTION 1: Bash script has error in json building--this code block corrects this error
            # Define the PCRE2 regex pattern to fix {} after timestamp
            pattern1 = re.compile(r'{},')
            # Replace all instances of {} with '{'
            lines = pattern1.sub('{', lines)
            lines += "}"
            # NOTE: END OF CORRECTION 1

            # Create a JSON object from the lines
            try:
                json_object = json.loads(lines)
            except:
                # This is needed for when the network goes down
                # NOTE: START OF CORRECTION 1: Bash script has error in json building--this code block corrects this error
                # Instead of saving 0.0 for when the network is down, it simply leaves a blank space
                lines = '{"speedtest": {"Sun Nov 12 07:00:00 PM -05 2023": {"No connection": {"download": 0.0,"upload": 0.0}}}}'
                json_object = json.loads(lines)

            # Append the JSON object to the output list
            speedtest_list.append(lines)

            # Re-add '{"speedtest": {' to the start, because we detected this 2 lines into the next block
            lines = '{"speedtest": {'
        else:
            lines += line
            i += 1

plot(speedtest_list)
