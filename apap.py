from pySPL import DrugLabel
from utils import file_list
import csv

#don't bother adding marketing end date, it's NONE for all labels

with open('output.csv', 'wb') as f:
    #pipe delimiter is so we can use commas elsewhere; nobody uses pipes and excel/google docs do not care
    writer = csv.writer(f,delimiter="|")
    
    #writes header row. need to keep this the same as how it's written below
    writer.writerow(
        ["distributor",
        "drug name",
        "ndc",
        "label type",
        "dosage form",
        "marketing start date",
        "revision date",
        "warfarin mentioned?",
        "#actives",
        "actives",
        "url",
        ])
    count = 1
    for xml_label in file_list:
        print "label ",count," of ",len(file_list),"(%s)" % xml_label
        label = DrugLabel(xml_label)
        #ignore kits
        if label.dosage_form() == "KIT" or label.dosage_form() == "BULK INGREDIENT":
            print "passing on %s " % xml_label
            pass
        else:
            writer.writerow([
                label.distributor(),
                label.name(),
                label.ndc(),
                label.label_type(),
                label.dosage_form(),
                label.start_date(),
                label.revision_date(),
                label.check_word("warfarin"),
                len(label.actives()),
                label.actives(),
                label.build_url(),
                ])
        count+=1
    print "success!"

f.close()