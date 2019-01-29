import pandas as pd 
from bs4 import BeautifulSoup
import os
import math

IMAGE_SIZE = 512

def find_all_files(root, suffix = None):
    res = [] 
    for path, _, files in os.walk(root):
        for f in files:
            if suffix is not None and not f.endswith(suffix):
                continue
            res.append(os.path.join(path, f))
    return res

def parse_xml(xml_file, only_one = True):
    pos_lines = []
    extended_lines = []
    with open(xml_file, 'rb') as xml_f:
        markup = xml_f.read()
    xml_ = BeautifulSoup(markup, features="xml")

    if xml_.LidcReadMessage is None:
        return None, None
    patient_id = xml_.LidcReadMessage.ResponseHeader.SeriesInstanceUid.text
    imsop_uid = None

    reading_sessions = xml_.LidcReadMessage.find_all("readingSession")
    for reading_session in reading_sessions:
        ser_ist_id = reading_session.servicingRadiologistID.text
        nodules = reading_session.find_all("unblindedReadNodule")
        for nodule in nodules:
            nodule_id = nodule.noduleID.text
            # print(nodule_id) 
            rois = nodule.find_all("roi")
            x_min = y_min = 999999
            x_max = y_max = -999999
            # print(len(rois))
            if len(rois) < 2:
                continue 

            for roi in rois:
                imsop_uid = roi.imageSOP_UID.text 
                edge_maps = roi.find_all("edgeMap")
                for edge_map in edge_maps:
                    x = round( int(edge_map.xCoord.text) / IMAGE_SIZE, 4)
                    y = round( int(edge_map.yCoord.text) / IMAGE_SIZE, 4)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)
                if x_max == x_min:
                    continue 
                if y_max == y_min:
                    continue  

            x_diameter = x_max - x_min        #width
            x_center = x_min + x_diameter / 2
            y_diameter = y_max - y_min        #height
            y_center = y_min + y_diameter / 2                   
            diameter = max(x_diameter , y_diameter)

            if nodule.characteristics is None:
                print("!!!!Nodule:", nodule_id, " has no charecteristics")
                continue
            if nodule.characteristics.malignancy is None:
                print("!!!!Nodule:", nodule_id, " has no malignacy")
                continue

            malignacy = nodule.characteristics.malignancy.text
            sphericiy = nodule.characteristics.sphericity.text
            margin = nodule.characteristics.margin.text
            spiculation = nodule.characteristics.spiculation.text
            texture = nodule.characteristics.texture.text
            calcification = nodule.characteristics.calcification.text
            internal_structure = nodule.characteristics.internalStructure.text
            lobulation = nodule.characteristics.lobulation.text
            subtlety = nodule.characteristics.subtlety.text

            line = [[imsop_uid, ser_ist_id, nodule_id, x_center, y_center, diameter, malignacy, x_min, y_min, x_max, y_max]]
            extended_line = [patient_id, imsop_uid, nodule_id, x_diameter, y_diameter, malignacy, x_min, y_min, x_max, y_max, sphericiy, margin, spiculation, texture, calcification, internal_structure, lobulation, subtlety ]
            pos_lines.append(line)
            extended_lines.append(extended_line)

    if only_one:
        filtered_lines = pos_lines
        for pos_line1 in pos_lines:
            uid1 = pos_line1[0][0]
            id1 = pos_line1[0][1]
            for pos_line2 in pos_lines:
                uid2 = pos_line2[0][0]
                id2 = pos_line2[0][1]
                if uid1 == uid2 and id1 != id2:
                   filtered_lines.remove(pos_line2)
        pos_lines = filtered_lines
    
    return pos_lines

    # list to dict, keyed by imsop_uid
def list_to_dict(pos_lines):
    pos_dict = {}
    for pos_line in pos_lines:
        if pos_line[0][0] in pos_dict.keys():
            pos_dict[pos_line[0][0]].append(pos_line[0][6::1])
        else:
            pos_dict[pos_line[0][0]] = [pos_line[0][6::1]]
    return pos_dict

def save_txt(pos_dict):
    for uid, nodule_info in pos_dict.items():
        df_annos = pd.DataFrame(nodule_info, columns=["malignacy", "x_min", "y_min", "x_max", "y_max"])
        df_annos.to_csv(settings.EXTRACTED_IMAGE_DIR + uid + ".txt", index=False)


if __name__ == "__main__":
    root = "./data/"
    xml_files = find_all_files(root,".xml")

    for xml_file in xml_files:
        nodule_lines = parse_xml(xml_file)
        nodule_dict = list_to_dict(nodule_lines)
        save_txt(nodule_dict)

    print("Done!")
    

