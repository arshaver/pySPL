from lxml import etree
from datetime import date

namespaces={"a":"urn:hl7-org:v3",}

class DrugLabel(object):
    """represents a DrugLabel in the SPL format"""
    
    def __init__(self, spl_label):
        self.url = spl_label
        self.xml = etree.parse(spl_label)
    
    def actives(self):
        return list(set(active.text for active in self.xml.xpath("//a:activeMoiety//a:activeMoiety/a:name",namespaces=namespaces)))
        #here converting to a set removes duplicates

    def start_date(self):
        """returns start marketing date as a strftime formatted python date object"""
        date_string = self.xml.findall("//{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")[0].attrib["value"]
        year = int(date_string[0:4])
        month = int(date_string[4:6])
        day = int(date_string[6:8])
        return date(year,month,day).strftime("%b %d, %Y")

    def revision_date(self):
        """returns label revision date"""
        date_string = self.xml.findall("//{urn:hl7-org:v3}effectiveTime")[0].attrib["value"]
        year = int(date_string[0:4])
        month = int(date_string[4:6])
        day = int(date_string[6:8])
        return date(year,month,day).strftime("%b %d, %Y")

    def label_type(self):
        """returns the drug label type, typically 'HUMAN OTC DRUG LABEL' or 'HUMAN PRESCRIPTION DRUG LABEL' """
        drug_type = self.xml.findall("//{urn:hl7-org:v3}code")[0].attrib["displayName"]
        return drug_type

    def ndc(self):
        "returns the drug's NDC number"
        ndc = self.xml.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}code").attrib["code"]
        return ndc

    #TODO check to make sure full name is being returned (eg maybe other tags interfering)
    def name(self):
        """returns the drug's name"""
        drug_name = self.xml.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}name").text
        return drug_name

    def dosage_form(self):
        """returns the drug's dosage form"""
        dosage_form = self.xml.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}formCode").attrib["displayName"]
        return dosage_form


    #the next two functions take file input, not lxml.etree inputs

    def check_word(file, word):
        """
        returns True if the string "word" or "Word" or "WORD" is found in any line in the file
        useful for checking if another drug, such as an interaction, is mentioned
        """
        drug = open(file)
        word = str(word).lower()
        for line in drug:
            if (word in line) or (word.capitalize() in line) or (word.upper() in line):
                return True
                break
        return False

    def get_word_line(file, word):
        """
        returns the whitespace-stripped line that contains "word" or "Word" or "WORD"
        useful for checking if the "word" listing is legitimate for your purposes
        not that this only displays the first line found containing "word" or "Word" or "WORD"
        """
        drug = open(file)
        word = str(word).lower()
        for line in drug:
            if (word in line) or (word.capitalize() in line) or (word.upper() in line):
                return line.strip()
                break
        return False

    def build_url(file):
        """builds and returns the accessdata.fda.gov URL given the XML file name/directory"""
        #first split to get the file name from the whole path, then split to get rid of the .xml
        file_name = str(file.split("/")[-1]).split(".")[0]
        #then build the url
        url = "http://www.accessdata.fda.gov/spl/data/%s/%s.xml" (file_name,file_name)
        return url