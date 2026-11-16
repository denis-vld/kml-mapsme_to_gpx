import argparse
import xml.etree.ElementTree as ET

def kml_to_gpx_convert(kml_file_name: str, gpx_file_name: str, activity_name: str, trek_name: str):
    # make stub-file for output gpx-file
    gpx_file = open(gpx_file_name, "w")
    gpx_file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    gpx_file.write("<gpx creator=\"kml_to_gpx_convert\" version=\"1.1\">\n")
    gpx_file.write("<trk>\n<type>" + activity_name + "</type>\n</trk>\n")
    gpx_file.write("</gpx>\n")
    gpx_file.close()

    kml_data_tree = ET.parse(kml_file_name)
    gpx_data_tree = ET.parse(gpx_file_name)
    root_kml = kml_data_tree.getroot()
    root_gpx = gpx_data_tree.getroot()
    gpx_trk_elem = root_gpx.find('trk')
    subelem_trk = ET.SubElement(gpx_trk_elem, 'name')
    first_date = ""
    last_date = ""
    placemark_elem_list = root_kml.findall('.//kml:Placemark', namespaces={'kml': 'http://earth.google.com/kml/2.2'})
    for i in range(len(placemark_elem_list)-1, -1, -1):
        plcmrk = placemark_elem_list[i]
        pt_elem = plcmrk.find('.//kml:coordinates', namespaces={'kml': 'http://earth.google.com/kml/2.2'})
        if pt_elem is None:
            break
        pts = pt_elem.text
        if pts is None:
            break
        point_list = pts.split(' ')
        time_list_elem = plcmrk.findall('.//mwm:timestamp', namespaces={'mwm': 'https://maps.me'})
        gpx_elem = ET.SubElement(gpx_trk_elem, 'trkseg')
        for pt, pt_time in zip(point_list, time_list_elem):
            one_point_str_list = pt.split(',')
            gpx_pt_elem = ET.SubElement(gpx_elem, 'trkpt', attrib={'lat': one_point_str_list[1], 'lon': one_point_str_list[0]})
            subelem = ET.SubElement(gpx_pt_elem, 'ele')
            subelem.text = one_point_str_list[2]
            if pt_time is not None:
                subelem = ET.SubElement(gpx_pt_elem, 'time')
                subelem.text = pt_time.text
        if i == len(placemark_elem_list)-1:
            last_date = time_list_elem[0].text.split('T')[0]
        if i == 0:
            first_date = time_list_elem[0].text.split('T')[0]
    if trek_name is not None and trek_name != "":
        subelem_trk.text = trek_name
    else:
        subelem_trk.text = first_date + "_" + last_date
    ET.indent(gpx_data_tree, space="  ", level=0)
    gpx_data_tree.write(gpx_file_name, encoding="utf-8", xml_declaration=True)
    return

def kml_to_gpx_parse():
    parser = argparse.ArgumentParser(description="Script to convert kml-file to gpx-file")
    # Добавляем позиционный или опциональный аргумент
    parser.add_argument("-kml_file_name", type=str, help="*.kml file name (input file)")
    parser.add_argument("-gpx_file_name", type=str, help="*.gpx file name (output file)")
    parser.add_argument("-activity_name", type=str, help="Name of activity to write in gpx-file")
    parser.add_argument("-trek_name", type=str, help="Name of track to write in gpx-file")
    args = parser.parse_args()
    if args.activity_name == "":
        args.activity_name = "Ходьба"
    if args.kml_file_name == "" or args.gpx_file_name == "":
        print("Error of command line arguments")
        return
    kml_to_gpx_convert(args.kml_file_name, args.gpx_file_name, args.activity_name, args.trek_name)

if __name__ == "__main__":
    kml_to_gpx_parse()