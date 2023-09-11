#!/bin/bash

# Set path variable
export PATH=/usr/local/bin:/usr/bin:/bin

# Set the working directory inside the script
cd /home/boaz/Documents/speedtest-cronjob

# Set file path of where you want to save the speed test data
data_file="./speedtest_data.json"

# Check if data file exists, that it is readable, and writable. If any of these fail, fix, then restart the loop.
if [ -e "$data_file" ] && [ -r "$data_file" ] && [ -w "$data_file" ]; then
	:  # File exists, is readable and writeable. No action needed.
elif ! [ -e "$data_file" ]; then
	$(umask 066 && touch "$data_file") || $(sudo umask 066 && sudo touch "$data_file")
	chmod a+r "$data_file"
elif ! [ -r "$data_file" ]; then
	chmod u+r "$data_file" || sudo chmod u+r "$data_file"
elif ! [ -w "$data_file" ]; then
	chmod u+w "$data_file" || sudo chmod u+w "$data_file"
fi

chmod a+r "$data_file"

# set existing data from file to variable
existing_data=$(<"$data_file")
# Check if the '.speedtest' object exists in the existing JSON data
if ! [ $(jq 'has("speedtest")' <<< "$existing_data") ]; then
  # Create the .speedtest object if it doesn't exist
  echo "no speedtest found in \$existing_data"
  existing_data='{"speedtest":""}'
fi
# One date to rule them all. One date to find them. One date to bring them all and in the darkness bind them.
# When The clock hits the 00-minute mark, each speed test is run one after the other, but this approximates all timestamps as being on the hour
date=$(date -d "$(date -d 'now' '+%H:00:00')")

date_json=$(jq -n --argjson "$date" {} \
              '$ARGS.named'
)

# Run the loop with output redirected to a process substitution
while read -r p # The value of p is set by the "done < <(speedtest..." statement at the bottom of the loop
do
        # Run the speedtest for the server with id of $p
        raw_data=$(speedtest --server-id="$p")
        # This greps through the data to find the server name then applies regex to remove everything before "Server: " and everything after and including " (<word>:" and limits to 1 result
        server_name=$(echo "$raw_data" | grep -m 1 -oP 'Server: \K.*(?= \(\w+:)')
        # The final Upload and Download speeds are in the same line as "(data used:"
        speed_data=$(echo "$raw_data" | grep "(data used:")
        # if statement to make sure that if there is a null result due to the speed-test failing, it just skips to the next speed test
        if [ -n "$speed_data" ]; then
                # Greps using a Regex pattern for 3 leading and 3 trailing digits (there should be 2 results for upload and download)
                download="$(grep "Download:" <<< "$speed_data" | grep -oP "[\d]{1,3}.[\d]{2}")"
                upload="$(grep "Upload:" <<< "$speed_data" | grep -oP "[\d]{1,3}.[\d]{2}")"
        fi
        # Here we have the time, the server name, the upload and download speed. Put it into json format and save it to the file.
        # Put upload and download speeds in json format
	download_upload_json=$(jq -n --arg download "$download" \
                           --arg upload "$upload" \
                           -r '{
                             "download": ($download | tonumber),
                             "upload": ($upload | tonumber)
                            }')
        # Nest upload and download speeds json into the server name json
	server_name_json=$(jq -n --argjson "$server_name" "$download_upload_json" \
		-r '$ARGS.named')
        # Merge the server name json into the date json
	echo "Running speedtest for: "$server_name_json
        date_json=$(jq --argjson existing_entries "$date_json" --argjson new_server_entry "$server_name_json" \
                '. * $new_server_entry' <<< "$date_json")
done < <(speedtest -L | awk 'FNR >= 5 {print $1}')

# Now that all the data is collected and stored in the date_json variable, save it to the file under the '.speedtest' object
# Merge the existing data with the new object using jq and the "*" operator

# ERROR: the variable $existing_data is empty and this is what's causing the code to break
updated_data=$(jq --argjson existing_data "$existing_data" --argjson date_json "$date_json" \
                '.speedtest |= $date_json' <<<"$existing_data")

# Overwrite the file with the updated JSON data
echo "$updated_data" | sudo tee -a "$data_file"

# This section is so that you don't have to keep your computer on all the time to passively run this script
# This uses rtcwake (Real Time Clock Wake) and xprintidle (prints time the computer has been idle in ms)
# to check if the computer is idle, and if so, suspend it until the 59-minute mark of the next hour,
# wakes up the machine, then the script gets run by the cron job at the 00-minute mark, then puts it
# the script puts the machine back to sleep till the next 59-minute mark

# Get the idle time in milliseconds using xprintidle
idle_time=$(xprintidle)

# Define the threshold in milliseconds for considering the user as idle
threshold=900000  # 15 minutes (15 * 60 * 1000) = 900000

# Compare the idle time with the threshold
if [ "$idle_time" -ge "$threshold" ]; then
    # User is idle, suspend until the 59-minute mark of the current hour, otherwise don't suspend the machine
    rtcwake -l -m mem -t "$(date -d "$(date -d 'now' '+%H:59:00')" '+%s')"
fi
