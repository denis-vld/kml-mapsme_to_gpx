# kml-mapsme_to_gpx
Python script to convert kml-file with time info in Extended Data to gpx-file

This script is launched from terminal using:

  python kml_to_gpx.py <kml-file> <gpx-file> [<activity name>] [<track name>]
  
  <kml-file> - filename of input kml-file
  <gpx-file> - filename of output gpx-file
  <activity_name> - name of activity (for example, Hiking, Running, Ski, etc). Will be passed in field <type> of gpx-file. If there is no value for activity_name, will be set value "Ходьба".
  <track_name> - name of this track (for example, "Trip in The Grand Canyon"). If there is no value for activity_name, will be set value with first and last date of track (2026-07_12-2026-07-24).

To launch the script you must install Python v3.x on your computer.
  
