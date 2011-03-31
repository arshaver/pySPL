from lxml import etree
from datetime import date
import csv

def get_xml_files(dir):
    """gets all XML files from a directory and
    returns them as a list with full directory"""
    import os
    filename_list = []
    
    for file in os.listdir(dir):
        if file.split(".")[-1] == "xml":
            filename_list.append(dir+file)
    return filename_list

#lists full path; NEED trailing slash here
#this directory contains all of the results (eg the *.xml files) of this query: http://labels.fda.gov/getIngredientName.cfm?beginrow=1&numberperpage=2557&searchfield=acetaminophen&OrderBy=IngredientName
file_list = get_xml_files("/Users/anthonyshaver/Documents/Pharmacy School/apap warfarin interaction project/all_apap_labels/")


def get_actives(drug):
    """returns a python list of all active moieties listed in the file"""
    actives = []
    for item in drug.findall("//{urn:hl7-org:v3}activeMoiety/{urn:hl7-org:v3}activeMoiety/{urn:hl7-org:v3}name"):
        actives.append(item.text)
    #here converting to a set removes duplicates
    return list(set(actives))

#start marketing date    
def get_start_date(drug):
    date_string = drug.findall("//{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")[0].attrib["value"]
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

#label revision date
def get_revision_date(drug):
    date_string = drug.findall("//{urn:hl7-org:v3}effectiveTime")[0].attrib["value"]
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

def get_type(drug):
    drug_type = drug.findall("//{urn:hl7-org:v3}code")[0].attrib["displayName"]
    return drug_type

#takes file input, not etree
def check_warfarin(file):
    drug = open(file)
    for line in drug:
        if ("WARFARIN" in line) or ("warfarin" in line) or ("Warfarin" in line):
            return True
    return False

# try/except for if drug doesn't have NDC - but they all seem to
def get_ndc(drug):
    try:
        ndc = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}code").attrib["code"]
        return ndc
    except:
        return None

#TODO: check to make sure full name is being returned (eg maybe other tags interfering)
def get_name(drug):
    drug_name = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}name").text
    return drug_name

def get_url(file):
    #first split to get the file name from the whole path, then split to get rid of the .xml
    file_name = str(file.split("/")[-1]).split(".")[0]
    url = "http://www.accessdata.fda.gov/spl/data/"+file_name+"/"+file_name+".xml"
    return url
    
    
#IGNORE; for testing of individual functions with a random individual drug label
# print get_name(etree.parse("http://www.accessdata.fda.gov/spl/data/787cda7d-7aa4-4909-8e5c-f2fcf68828e4/787cda7d-7aa4-4909-8e5c-f2fcf68828e4.xml"))

with open('output.csv', 'wb') as f:
    #pipe delimiter is so we can use commas elsewhere; nobody uses pipes and excel/google docs don't care
    writer = csv.writer(f,delimiter="|")
    writer.writerow(["drug name","marketing start date","revision date","type","ndc","warfarin mentioned?","#active compounds","active compounds","url"])
    for file in file_list:
        xml = etree.parse(file)
        writer.writerow([get_name(xml),get_start_date(xml),get_revision_date(xml),get_type(xml),get_ndc(xml),check_warfarin(file),len(get_actives(xml)),get_actives(xml),get_url(file)])

f.close()