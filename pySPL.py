from lxml import etree
from datetime import date

#http://www.accessdata.fda.gov/spl/stylesheet/spl-common.xsl
namespaces={"v3":"urn:hl7-org:v3",}

def normalize_date(date_string):
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

class DrugLabel(object):
    """represents a Drug Label in the SPL format.
    takes one argument, spl_label, which can be either an url or a file"""
    
    def __init__(self, spl_label):
        self.label_data = spl_label
        self.xml = etree.parse(spl_label)
            
    def actives(self):
        """returns a list of active compounds"""
        #here converting to a set removes duplicates
        return list(set(active.text for active in self.xml.xpath("//v3:ingredientSubstance/v3:activeMoiety/v3:activeMoiety/v3:name",namespaces=namespaces)))

    def start_date(self):
        """returns start marketing date as a strftime formatted python date object"""
        date_string = self.xml.xpath("//v3:subjectOf/v3:marketingAct/v3:effectiveTime/v3:low/@value",namespaces=namespaces)[0]
        return normalize_date(date_string)

    def end_date(self):
        """returns end marketing date as a strftime formatted python date object or None if not defined
        refers to the expiration date of the last lot released to the market
        (from http://spl-work-group.wikispaces.com/file/view/creating_otc_sp_documentsl.pdf)"""
        try:
            date_string = self.xml.xpath("//v3:subjectOf/v3:marketingAct/v3:effectiveTime/v3:high/@value",namespaces=namespaces)[0]
            return normalize_date(datestring)
        except:
            return "None"

    def marketing_category(self):
        """returns the marketing category"""
        return self.xml.xpath("//v3:subjectOf/v3:approval/v3:code/@displayName",namespaces=namespaces)[0]

    def revision_date(self):
        """returns label revision date"""
        date_string = self.xml.xpath("/v3:document/v3:effectiveTime/@value",namespaces=namespaces)[0]
        return normalize_date(date_string)

    def label_type(self):
        """returns the drug label type, typically 'HUMAN OTC DRUG LABEL' or 'HUMAN PRESCRIPTION DRUG LABEL' """
        return self.xml.xpath("//v3:code/@displayName",namespaces=namespaces)[0]

    def ndc(self):
        """returns the drug's NDC number"""
        #xpath query is NOT from the xsl file
        return self.xml.xpath("//v3:manufacturedProduct/v3:manufacturedProduct/v3:code/@code",namespaces=namespaces)[0]

    def name(self):
        """returns the drug's name"""
        return self.xml.xpath("//v3:manufacturedProduct/v3:manufacturedProduct/v3:name",namespaces=namespaces)[0].text
    
    def distributor(self):
        """returns the drug's distributor"""
        return self.xml.xpath("//v3:author/v3:assignedEntity/v3:representedOrganization/v3:name",namespaces=namespaces)[0].text
    
    def dosage_form(self):
        """returns the drug's dosage form"""
        return self.xml.xpath("//v3:manufacturedProduct/v3:manufacturedProduct/v3:formCode/@displayName",namespaces=namespaces)[0]

    def build_url(self):
        """helper function that builds and returns the accessdata.fda.gov URL given the XML file name/directory"""
        #maybe won't work on windows because slash direction?
        guid = self.label_data.split("/")[-1].split(".")[0]
        return "http://www.accessdata.fda.gov/spl/data/%s/%s.xml" %(guid,guid)
    
    def check_word(self, word):
        """checks if the xml contains 'word','Word' or 'WORD' and returns True if found or False if not"""
        word = str(word)
        query = "//*[text()[contains(.,'%s') or contains(.,'%s') or contains(.,'%s')]]" %(word.lower(),word.upper(),word.capitalize())
        return True if self.xml.xpath(query,namespaces=namespaces) else False
