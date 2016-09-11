# sea_level_against_volume
Code that tries to set sea_level versus additional volume of water added to the global ocean. Files need to be archived as downloaded from SRTM or other source. I used http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm

volume_vs_height.py - given topographic data in .hgt files returns in a list where elements 0 to 100 respond to the area of the Earth at a height of 0 to 100m, Writes it down to results.txt. Last list in file is the complete list
calculate.py - when given the list from results.txt gives the volume of water needed to increase the water level. Writes it down to results_calc.txt
