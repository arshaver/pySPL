from lxml import etree
from datetime import date
import csv


#returns a python list of all active moieties listed in the file
def get_actives(drug):
    actives = []
    for active in drug.findall("//{urn:hl7-org:v3}activeMoiety/{urn:hl7-org:v3}activeMoiety/{urn:hl7-org:v3}name"):
        actives.append(active.text)
    #here converting to a set removes duplicates
    return list(set(actives))

#start *marketing* date (much larger range than get_revision_date() function below)
def get_start_date(drug):
    date_string = drug.findall("//{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")[0].attrib["value"]
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

#label *revision* date
def get_revision_date(drug):
    date_string = drug.findall("//{urn:hl7-org:v3}effectiveTime")[0].attrib["value"]
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

def get_label_type(drug):
    drug_type = drug.findall("//{urn:hl7-org:v3}code")[0].attrib["displayName"]
    return drug_type

# try/except for if drug doesn't have NDC - but they all seem to
def get_ndc(drug):
    try:
        ndc = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}code").attrib["code"]
        return ndc
    except:
        return None

#TODO check to make sure full name is being returned (eg maybe other tags interfering)
def get_name(drug):
    drug_name = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}name").text
    return drug_name


#the next two functions take file input, not etree

#Returns True if the string "word", "Word" or "WORD" are found in any line in the file.
def check_word(file, word):
    drug = open(file)
    word = str(word).lower()
    for line in drug:
        if (word in line) or (word.capitalize() in line) or (word.upper() in line):
            return True
            break
    return False

def get_url(file):
    #first split to get the file name from the whole path, then split to get rid of the .xml
    file_name = str(file.split("/")[-1]).split(".")[0]
    #then build the url
    url = "http://www.accessdata.fda.gov/spl/data/"+file_name+"/"+file_name+".xml"
    return url
    
def get_dosage_form(drug):
    dosage_form = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}formCode").attrib["displayName"]
    return dosage_form