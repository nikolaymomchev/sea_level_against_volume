# sea_level_against_volume
Code that tries to set sea_level versus additional volume of water added to the global ocean
volume_vs_height.py - given topographic data in .hgt files - tipically from SRTM- returns in a list where elements 0 to 100 respond to the area at a height of 0 to 100m, Writes it down to results.txt. Last list in file is the complete list
calculate.py - when given the list from results.txt gives the volume of water needed to increase the water level by how much. Writes it down to results_calc.txt
