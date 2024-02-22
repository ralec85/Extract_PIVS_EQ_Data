extractPIVSeqdata.py
-----------------------------------------------------------------------------------------------------------------------
Created by Alec Ramirez (2024.02)
-----------------------------------------------------------------------------------------------------------------------
Contents
- Information
- Installation
- Execution
-----------------------------------------------------------------------------------------------------------------------
Information

This script can extract earthquake event data from PHIVOLCS-SOEPD online records, and saves it as a comma-separated output text (.txt) file.
The output text file follows the naming format: YYYY-MM.txt.

Note: This script is only tested for records from 2020 and later. Records from previous years may not be extracted correctly due to limitations
on the html parsing employed in this script.

Each earthquake event has 12 attributes /columns, as follows:

Column 1: Event ID
  The event ID follows the format: PIVSYYYYMM######
  For example, event PIVS202402000143 refers to the 143rd 	recorded earthquake event for February 2024.
  This event ID is not official, and is only generated by this 	script.

Column 2: Date-Time
	The date-time is based on Philippine Time (UTC +8), and 	follows the format YYYY-MM-DD HH:MM:SS. The time is 	expressed using the 24-hour format. 
  Note that the PHIVOLCS records only reports up to the minute 	of the earthquake occurrence. As such, the seconds field is 	only added to complete the date-time format.
  The date-time attribute can be used to display the 	earthquake data as a time-series animation, such as using 	the QGIS Temporal Controller.

Column 3: Longitude (X-coordinate)
	CRS: EPSG 4326 (WGS84).

Column 4: Latitude (Y-coordinate)
	CRS: EPSG 4326 (WGS84).

Column 5: Depth
	In kilometers.

Column 6: Magnitude
	In surface magnitude.

Columns 7, 8, 9, 10, 11: Year, Month, Day, Hour, Minute
	Date-time divided into its components.

Column 12: Earthquake Information Source
	URL of the PHIVOLCS earhtquake information for the event.

-----------------------------------------------------------------------------------------------------------------------
Installation (Windows)

Make sure the following are installed:
	a. Pyhton 3
	b. BeautifulSoup4
		To install, enter in command prompt:
			pip3 install beautifulsoup4
	c. Urllib3
		To install, enter in command prompt:
			pip3 install urllib3

-----------------------------------------------------------------------------------------------------------------------
Execution

Enter the following in command prompt
[working directory]\ python extractPIVSeqdata.py [url]

[working directory] = where the extractPIVSeqdata.py script is saved. This is also where the output file(s) will be created.
                    = example: C:\Users\alec\Downloads\PIVSEQ-Trial
                    
[url] = URL of the PHIVOLCS monthly earthquake data online record

Note: Downloading from multiple urls is possible. For example:

To generate the earthquake data for January 2024 and December 2023, enter the following in command prompt:
  
  python extractPIVSeqdata.py https://earthquake.phivolcs.dost.gov.ph/EQLatest-Monthly/2024/2024_January.html https://earthquake.phivolcs.dost.gov.ph/EQLatest-Monthly/2023/2023_December.html

If successful, the following should be returned in the command prompt:

File created:  2024-01.txt
1898 earthquake events extracted.
Last record (check for inconsistencies):
('PIVS202401000001', '2024-01-01 12:07:00', '120.73', '11.89', '026', '2.4', '2024', '01', '01', '12', '07', 'http://earthquake.phivolcs.dost.gov.ph//earthquake.phivolcs.dost.gov.ph/2023_Earthquake_Information/December/2023_1231_1607_B2.html')

File created:  2023-12.txt
4285 earthquake events extracted.
Last record (check for inconsistencies):
('PIVS202312000001', '2023-12-01 12:29:00', '121.86', '07.91', '026', '3.5', '2023', '12', '01', '12', '29', 'http://earthquake.phivolcs.dost.gov.ph/2023_Earthquake_Information/November/2023_1130_1629_B2.html')

Note: The last record is shown to check wether the earthquake data has been extracted correctly. If the html parsing has failed, the last record will have missing attributes.
