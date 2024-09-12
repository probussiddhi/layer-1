import pandas as pd
import fitz  # PyMuPDF
import re
from io import BytesIO

def extract_text_from_pdf_pc(pdf_file):
    """
    Extract text from a PDF file. Handles both file paths and BytesIO objects.
    """
    # Handle both file path and BytesIO stream
    if isinstance(pdf_file, str):
        pdf_document = fitz.open(pdf_file)
    elif isinstance(pdf_file, BytesIO):
        pdf_document = fitz.open(stream=pdf_file, filetype="pdf")

    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text


def extract_name(text):
    return extract_field_value(text, r"Insured's Name:\s*(.+?)\s*Insured's GST No.")


def extract_date_of_issue(text):
    date_pattern = re.compile(r"Date of Issue:\s*(\d{2}/\d{2}/\d{4})")
    match = date_pattern.search(text)
    if match:
        return match.group(1)
    return None


def extract_phone_number(text):
    phone_pattern = re.compile(r'\+?\d{10,12}')
    match = phone_pattern.search(text)
    if match:
        return match.group(0)
    return None


def extract_period_of_insurance(text):
    period_pattern = re.compile(r"Period of Insurance:\s*(\d{2}/\d{2}/\d{4})\s*to\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
    match = period_pattern.search(text)
    if match:
        return match.group(1), match.group(2)
    return None, None


def extract_policy_number(text):
    policy_pattern = re.compile(r"Policy\s+No\.\s*(\d{5,30})", re.IGNORECASE)
    match = policy_pattern.search(text)
    if match:
        return match.group(1)
    return None


def extract_email_id(text):
    return extract_field_value(text, r"Email\s*ID\s*[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")


def extract_detail(lines, index):
    """
    Extract details from lines based on the index provided.
    """
    detail = None
    if index < len(lines) - 1:
        detail = lines[index + 1].strip()
    return detail


def extract_vehicle_details(pdf_file):
    """
    Extract details related to the vehicle from the PDF.
    Handles both file paths and BytesIO objects.
    """
    if isinstance(pdf_file, str):
        document = fitz.open(pdf_file)
    elif isinstance(pdf_file, BytesIO):
        document = fitz.open(stream=pdf_file, filetype="pdf")

    make = model = variant = year_of_manufacture = seating_capacity = engine_number = chassis_number = None
    try:
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text = page.get_text()
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if "Make" in line:
                    make = extract_detail(lines, i)
                elif "Model" in line:
                    model = extract_detail(lines, i)
                    variant = extract_detail(lines, i + 1)
                    if '&' in model:
                        model, variant = map(str.strip, model.split('&', 1))
                    else:
                        model = variant
                elif "Year of Manufacture" in line:
                    year_of_manufacture = extract_detail(lines, i)
                elif "Seating Capacity" in line:
                    seating_capacity = extract_detail(lines, i)
                elif "Engine No." in line or "Engine Number" in line:
                    engine_number = extract_detail(lines, i)
                elif "Chassis No." in line or "Chassis Number" in line:
                    chassis_number = extract_detail(lines, i)
        document.close()
    except Exception as e:
        print(f"Error extracting vehicle details: {e}")
    
    return make, model, variant, year_of_manufacture, seating_capacity, engine_number, chassis_number


def extract_field_value(text, field_pattern):
    match = re.search(field_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_insurance_data(pdf_file):
    """
    Extract insurance-related data from the PDF.
    """
    if isinstance(pdf_file, str):
        document = fitz.open(pdf_file)
    elif isinstance(pdf_file, BytesIO):
        document = fitz.open(stream=pdf_file, filetype="pdf")

    text = ""
    for page in document:
        text += page.get_text()

    data = {}
    base_premium_match = re.search(r"Base Premium including Premium for TPPD\s+₹\s*([0-9,.]+)", text)
    if base_premium_match:
        data["base_premium"] = base_premium_match.group(1)

    total_liability_premium_match = re.search(r"Total liability premium\s+₹\s*(.*)", text)
    if total_liability_premium_match:
        data["total_liability_premium"] = total_liability_premium_match.group(1)

    cgst_match = re.search(r"CGST @\d+%\s+₹\s*([0-9,.]+)", text)
    if cgst_match:
        data["cgst"] = cgst_match.group(1)

    sgst_match = re.search(r"SGST @\d+%\s+₹\s*([0-9,.]+)", text)
    if sgst_match:
        data["sgst"] = sgst_match.group(1)

    final_premium_match = re.search(r"Final premium\s+₹\s*([0-9,.]+)", text)
    if final_premium_match:
        data["final_premium"] = final_premium_match.group(1)

    return data


def extract_data_from_pdf_pc(pdf_file):
    """
    Extract complete data from the PDF for the PC-based insurance.
    """
    try:
        pdf_text = extract_text_from_pdf_pc(pdf_file)
        name = extract_name(pdf_text)
        phone_number = extract_phone_number(pdf_text)
        email = extract_email_id(pdf_text)
        date_of_issue = extract_date_of_issue(pdf_text)
        policy_number = extract_policy_number(pdf_text)
        start_date, end_date = extract_period_of_insurance(pdf_text)
        make, model, variant, year_of_manufacture, seating_capacity, engine_number, chassis_number = extract_vehicle_details(pdf_file)
        insurance_data = extract_insurance_data(pdf_file)

        data_dict = {
            "Name": name,
            "Contact Number": phone_number,
            "Date of Issue": date_of_issue,
            "Policy Number": policy_number,
            "Email": email,
            "Period of Insurance Start": start_date,
            "Period of Insurance End": end_date,
            "Make": make,
            "Model": model,
            "Variant": variant,
            "Year of Manufacture": year_of_manufacture,
            "Seating Capacity": seating_capacity,
            "Engine Number": engine_number,
            "Chassis Number": chassis_number,
            "Insurance Data": insurance_data,
        }

        return data_dict

    except Exception as e:
        print(f"Error extracting data: {e}")
        return None
