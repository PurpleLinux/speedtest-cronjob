import json
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import MaxNLocator


def plot(speedtest_list):
    # Extracting data for plotting
    download_values = defaultdict(list)
    upload_values = defaultdict(list)
    dates = []

    for json_str in speedtest_list:
        data = json.loads(json_str)
        for date, values in data['speedtest'].items():
            dates.append(date)
            for key, val in values.items():
                download_values[date].append(val['download'])
                upload_values[date].append(val['upload'])

    # Plotting the data
    plot = plt.figure(figsize=(10, 6))

    for date in download_values:
        plt.scatter([date] * len(download_values[date]), download_values[date], color='teal', alpha=0.1, edgecolor='none')
        plt.scatter([date] * len(upload_values[date]), upload_values[date], color='pink', alpha=0.08, edgecolor='none')

    # Beautifying the plot
    plt.xlabel('Date/Fecha', fontweight='bold')
    plt.ylabel('Upload/Carga & Download/Descarga (Mbps)', fontweight='bold')
    plt.title('WiFi Download and Upload Speeds Sampled Hourly\nVelocidades de descarga y carga de WiFi muestreadas por hora', fontweight='bold')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(MaxNLocator(10))

    # Create custom legend elements
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Download/Descarga', markerfacecolor='teal', markersize=10, alpha=1),
        plt.Line2D([0], [0], marker='o', color='w', label='Upload/Carga', markerfacecolor='pink', markersize=10, alpha=1)
    ]

    # Add the legend with custom legend elements
    plt.legend(handles=legend_elements)

    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    test_data = [(
"{\"speedtest\": {\"Sun Dec 17 07:00:00 AM -05 2023\": {\"foobar1 - fooloc1\": "
"{\"download\": 659.61,\"upload\": 159.6},\"foobar2 - fooloc2\": {\"download\": 8.12,"
"\"upload\": 633.52},\"foobar3 - fooloc3\": {\"download\": "
"623.33,\"upload\": 693.27},\"foobar4 - fooloc4\": {\"download\": "
"653.37,\"upload\": 695.38},\"foobar5 - fooloc5\": {\"download\": 630.2,\"upload\": "
"684.59},\"foobar6 - fooloc6\": {\"download\": 111.77,"
"\"upload\": 281.93},\"foobar7 - fooloc7\": {\"download\": 597.2,\"upload\": 57.86},"
"\"foobar8. - fooloc8\": {\"download\": 657.26,\"upload\": 687.66},"
"\"foobar9 - fooloc9\": {\"download\": 621.52,\"upload\": 689.67},"
"\"foobar10 - fooloc10\": {\"download\": 581.09,\"upload\": 692.07}}}}"
    ),
    (
"{\"speedtest\": {\"Sun Dec 14 04:00:00 AM -03 2023\": {\"goobar1 - gooloc1\": "
"{\"download\": 639.61,\"upload\": 139.6},\"goobar2 - gooloc2\": {\"download\": 8.12,"
"\"upload\": 633.32},\"goobar3 - gooloc3\": {\"download\": "
"623.33,\"upload\": 693.24},\"goobar4 - gooloc4\": {\"download\": "
"633.34,\"upload\": 693.38},\"goobar3 - gooloc3\": {\"download\": 630.2,\"upload\": "
"684.39},\"goobar6 - gooloc6\": {\"download\": 111.44,"
"\"upload\": 281.93},\"goobar4 - gooloc4\": {\"download\": 394.2,\"upload\": 34.86},"
"\"goobar8. - gooloc8\": {\"download\": 634.26,\"upload\": 684.66},"
"\"goobar9 - gooloc9\": {\"download\": 621.32,\"upload\": 689.64},"
"\"goobar10 - gooloc10\": {\"download\": 381.09,\"upload\": 692.04}}}}"
    )]
    plot(test_data)