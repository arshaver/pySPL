from pySPL import *
from utils import file_list

#
with open('output.csv', 'wb') as f:
    #pipe delimiter is so we can use commas elsewhere; nobody uses pipes and excel/google docs do not care
    writer = csv.writer(f,delimiter="|")
    
    #writes header row. need to keep this the same as how it's written below
    writer.writerow(
        ["drug name",
        "ndc",
        "marketing start date",
        "revision date",
        "type",
        "warfarin mentioned?",
        "warfarin line",
        "dosage form",
        "#actives",
        "active compounds",
        "url",
        ])
    for xml_file in file_list:
        xml = etree.parse(xml_file)
        #ignore kits
        if get_dosage_form(xml) == "KIT":
            pass
        else:
            writer.writerow([
                get_name(xml),
                get_ndc(xml),
                get_start_date(xml),
                get_revision_date(xml),
                get_label_type(xml),
                check_word(xml_file,"warfarin"),
                get_word_line(xml_file,"warfarin"),
                get_dosage_form(xml),
                len(get_actives(xml)),
                get_actives(xml),
                get_url(xml_file),
                ])

f.close()