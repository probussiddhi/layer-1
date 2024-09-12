import pdfplumber
import re

class Layer :
    @staticmethod
    def extract_text_from_pdf(pdf_file):
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
# Function to identify the company name from the extracted text
    @staticmethod
    def identify_company_name(extracted_text):
        # List of possible company names
        companies = ["Magma", "LTGIC", "ZUNO", "KOTAK", "KOTAKlife", "BAJAJ", "TATAAIG",
                    "icici", "universalsompo", "united", "tatalife", "tata", "starhealth",
                    "shriramlife", "sbilife", "sbi", "shriram","Royal Sundaram", "reliancelife",
                    "pnbmetlife", "oriental", "nivabupa", "newindia", "national", "maxny",
                    "manipalsigma", "libertyvgi", "indiafirstlife", "iffcotokio", "hdfclife",
                    "hdfcergo", "hdfc", "futurelife", "edelweisslife", "digitlife", "cholamandalam",
                    "bhartilife", "bajajlife", "avivalife", "appolo", "ageaslife", "adityabirlalife",
                    "adic", "acko"]
        # Create regex pattern dynamically from the company list
        company_pattern = r'\b(?:' + '|'.join(companies) + r')\b'
        # Search for the company name in the text
        match = re.search(company_pattern, extracted_text, re.IGNORECASE)
        if match:
            return match.group(0)
        else:
            return None
    # Function to identify the product from the extracted text
    @staticmethod
    def identify_product(extracted_text):
        # List of motor-related sub-products

        # List of motor sub-products
        motor_sub_products = [
            "Two-wheeler", "Private Car", "Goods Carrying", "Passenger Carrying",
            "Misc", "Two Wheeler", "Goods Carrying Vehicle", "Passenger Carrying Vehicle"
        ]

        # Check if any motor sub-products are present in the text
        for sub_product in motor_sub_products:
            if re.search(r'\b' + re.escape(sub_product) + r'\b', extracted_text, re.IGNORECASE):
                return "motor"

        # List of general products
        products = ["health", "life", "motor", "miscellaneous", "sme", "travel"]
        product_pattern = r'\b(' + '|'.join([re.escape(product) for product in products]) + r')\b'

        # Check for specific motor-related keywords
        if re.search(r'\bCentral Motor Vehicles Rules\b', extracted_text, re.IGNORECASE):
            return "motor"

        # Search for any other products
        match = re.search(product_pattern, extracted_text, re.IGNORECASE)
        if match:
            return match.group(0)

        return None
    # Function to identify the sub-product from the extracted text
    @staticmethod
    def identify_subproduct(extracted_text, product):
        sub_product_pattern = r'\b(two\s?-?wheeler|private\s?-?car|goods\s?-?carrying|Passenger\s?-?Carrying|misc)\b'
        # First check for specific keywords
        if re.search(r'\b(motorcycle|bike|scooter|two\s?-?wheeler)\b', extracted_text, re.IGNORECASE):
            return "Two wheeler"
        if re.search(r'\b(sedan|hatchback|maruti|MARUTI|swift\s?-?dzire|car)\b', extracted_text, re.IGNORECASE):
            return "Private Car"
        if re.search(r'\b(goods\s?-?carrying|truck|lorry)\b', extracted_text, re.IGNORECASE):
            return "Goods carrying"
        if re.search(r'\b(passenger\s?-?carrying|bus|van)\b', extracted_text, re.IGNORECASE):
            return "passenger carrying"
        if re.search(r'\b(miscellaneous|other)\b', extracted_text, re.IGNORECASE):
            return "Misc"
        # Match against the general sub-product pattern
        match = re.search(sub_product_pattern, extracted_text, re.IGNORECASE)
        if match:
            return match.group(0)
        else:
            return None
    # Function to identify the segment from the extracted text 
 
    @staticmethod
    def identify_segment( extracted_text):
        # Example segment_map
        segment_map = {
            1: ['Comprehensive', 'Package', 'Comp', 'Comphrensive', 'Package Policy'],
            2: ['SAOD', 'Standalone Own Damage', 'OD Only'],
            3: ['SATP', 'Standalone TP', 'TP Only', 'Liability']
        }

        flattened_segments = [(segment_id, segment.lower()) for segment_id, segments in segment_map.items() for segment in segments]
        segment_pattern = r'\b(' + '|'.join([re.escape(segment) for _, segment in flattened_segments]) + r')\b'
        match = re.search(segment_pattern, extracted_text, re.IGNORECASE)
        
        if match:
            matched_segment = match.group(0).lower()
            for segment_id, segment in flattened_segments:
                if matched_segment == segment:
                    return segment_id

        fallback_match = re.search(r'(\b\w+\b)\s+[Pp]olicy\b', extracted_text)
        
        if fallback_match:
            matched_segment = fallback_match.group(1).lower()
            for segment_id, segment in flattened_segments:
                if matched_segment == segment:
                    return segment_id

        return None