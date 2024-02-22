import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime


def extract_PIVS_eq_data(input):

    with urlopen(input) as webpage: #opens webpage
        seisdata = webpage.read().decode() #reads webpage html 
    webpage.close() #closes webpage
    
    tab_start = re.search(r'<!-+ enter', seisdata) #searches for start of eq data table
    i_s = tab_start.start() #index for start of eq data table
    
    tab_end = re.search(r'event -+>', seisdata) #searches for end of eq data table
    i_e = tab_end.end() #index for end of eq data table
    
    seisdata = seisdata[i_s:i_e] #extracts eq data table html

    seistab = BeautifulSoup(seisdata, 'html.parser') #creates BeautifulSoup object from html for parsing

    seis_datetime = seistab.find_all('a') #parses eq url, date and time from html
    seis_lat = seistab.find_all('td', attrs={'class': 'auto-style90'}) #parses eq latitude from html
    seis_all = seistab.find_all('td', attrs={'class': 'auto-style56'}) #parses eq longitude, depth, and magnitude from html

    #initializes lists for earthquake data 
    eq_temporal = []
    eq_yr = []
    eq_mo = []
    eq_day = []
    eq_hr = []
    eq_min = []
    eq_lat = []
    eq_long = []
    eq_dep = []
    eq_mag = []
    eq_src = []
    eq_id = []
    eq_table = []
   
    k=0
    
    while k < len(seis_datetime): #loops through all earthquake events
        
        j=k*3 #for seis_all, which contains a list of longitude, depth, and magnitude
        
        eq_td_0 = seis_datetime[k].text.strip() #extracts the earthquake date and time as a string and removes leading and trailing whitespaces
        eq_td_conv = datetime.strptime(eq_td_0, "%d %B %Y - %H:%M %p") #formats the eq date and time string as a datetime object
        
        eq_url = seis_datetime[k]['href'] #extracts the PHIVOLCS earthquake information bulletin url
        eq_url = eq_url.replace('\\','/') #replaces backslash
        eq_url = 'http://earthquake.phivolcs.dost.gov.ph/' + eq_url[7:] #completes the PHIVOLCS earthquake information bulletin url
        
        eq_temporal.append(eq_td_conv.strftime("%Y-%m-%d %H:%M:%S")) #appends list of eq date and time, with time in 24 hour time format
        eq_yr.append(eq_td_conv.strftime("%Y")) #appends list of eq year
        eq_mo.append(eq_td_conv.strftime("%m")) #appends list of eq month
        eq_day.append(eq_td_conv.strftime("%d")) #appends list of eq day
        eq_hr.append(eq_td_conv.strftime("%H")) #appends list of eq hour 
        eq_min.append(eq_td_conv.strftime("%M")) #appends list of eq minute
        eq_lat.append(seis_lat[k].text.strip()) #appends list of eq epicenter latitudes
        eq_long.append(seis_all[j].text.strip()) #appends list of eq epicenter longitudes
        eq_dep.append(seis_all[j+1].text.strip()) #appends list of eq hypocenter depths
        eq_mag.append(seis_all[j+2].text.strip()) #appends list of eq magnitudes
        eq_src.append(eq_url) #appends list of eq information source urls
        
        pref_code = "PIVS" #prefix for eq_id code
        id_yr_mo = str(int(eq_yr[k] + eq_mo[k])*1000000 + len(seis_datetime) - k) #assigns sequential id num for earthquake
        
        eq_id.append(pref_code + id_yr_mo) #appends list of earthquake event id
        
        eq_compiled = (eq_id[k], eq_temporal[k], eq_long[k], eq_lat[k], eq_dep[k], eq_mag[k], eq_yr[k], eq_mo[k], eq_day[k], eq_hr[k], eq_min[k], eq_src[k]) #compiles all eq event attributes into a tuple
        eq_table.append(eq_compiled) #compiles all eq event tuples in a list        
        
        k=k+1
    
    return eq_table 
  

def main():
    
    args = sys.argv[1:]
    
    if not args:
        print('Usage: [url1] [url2] [url3] ...')
        print('Input url(s) from PHIVOLCS website (e.g. https://earthquake.phivolcs.dost.gov.ph/EQLatest-Monthly/2024/2024_January.html)')
    
    else:
        for items in args:
            input = items
            eq_data = extract_PIVS_eq_data(input)
            
            f_year = eq_data[0][6]
            f_month = eq_data[0][7]
            outputfile = f_year + '-' + f_month + '.txt'
            
            with open(outputfile, 'w') as f:
                for line in eq_data:
                    event = str(line)
                    event = str(re.sub(r'[\'\(\)]','',event))
                    event = str(event.replace(r', ',','))
                    event = event + '\n'
                    f.write(event)
                    
                
            f.close()
            
            print('File created: ', outputfile)
            print(len(eq_data),'earthquake events extracted.')
            print('Last record (check for inconsistencies):')
            print(eq_data[-1],'\n')


if __name__ == '__main__':
  main()    
    
    
