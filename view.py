import base64
from io import BytesIO
from flask import request, jsonify , Blueprint
from Zuno.zunotw import extract_data_from_pdf_tw 
from Zuno.zunopc import extract_data_from_pdf_pc
from Zuno.zunopcv import extract_data_from_pdf_pcv
from controller import Layer

api = Blueprint('view', __name__)

# @api.route('/layer-1', methods=['POST'])
# def handle_pdf_upload():
#     data = request.get_json()
    
#     # Check if the 'file' key exists in the data
#     if 'file' not in data:
#         return jsonify({"error": "No file provided"}), 400

#     # Decode the base64 PDF file
#     pdf_data = base64.b64decode(data['file'])
#     pdf_file = BytesIO(pdf_data)

#     # Extract text from PDF
#     layer = Layer()
#     extracted_text = layer.extract_text_from_pdf(pdf_file)

#     # Identify the product, company, and sub-product
#     product = layer.identify_product(extracted_text)
#     company = layer.identify_company_name(extracted_text)
#     sub_product = layer.identify_subproduct(extracted_text, product)

#     # Define motor sub-products
#     motor_sub_products = ["Two-wheeler", "private car", "goods carrying", "Passenger Carrying", "misc", 
#                         "Two wheeler", "Goods Carrying", "Private Car", "Two-Wheeler", "Misc"]

#     # Check if the sub_product belongs to motor sub-products
#     if sub_product in motor_sub_products:
#         product = "motor"
#     else:
#         product = layer.identify_product(extracted_text)  # Re-identify product if sub-product is not in the list

#     # Identify the segment
#     segment_id = layer.identify_segment(extracted_text)

#     # If company is Zuno and sub_product is Two-wheeler, call the Zuno-specific function
#     if company.lower() == 'zuno' and sub_product.lower() == 'two wheeler':
#         zuno_pdf_data = extract_data_from_pdf_tw(pdf_file)  # Call Zuno-specific function
#         if zuno_pdf_data:
#             # Add Zuno-specific data to the response
#             return jsonify({
#                 "company_name": company,
#                 "product": product,
#                 "sub_product": sub_product,
#                 "segment_id": segment_id,
#                 "zuno_data": zuno_pdf_data
#             }), 200
#         else:
#             return jsonify({"error": "Failed to extract data for Zuno Two-wheeler"}), 500
        
#     if company.lower() =='zuno' and sub_product.lower()=='private car':
#         zuno_pdf_data = extract_data_from_pdf_pc(pdf_file)  # Call Zuno-specific function
#         if zuno_pdf_data:
#             # Add Zuno-specific data to the response
#             return jsonify({
#                 "company_name": company,
#                 "product": product,
#                 "sub_product": sub_product,
#                 "segment_id": segment_id,
#                 "zuno_data": zuno_pdf_data
#             }), 200
#         else:
#             return jsonify({"error": "Failed to extract data for Zuno Private-Car"}), 500
        
#     if company.lower() =='zuno' and sub_product.lower()=='passenger carrying':
#         zuno_pdf_data = extract_data_from_pdf_pcv(pdf_file)  # Call Zuno-specific function
#         if zuno_pdf_data:
#             # Add Zuno-specific data to the response
#             return jsonify({
#                 "company_name": company,
#                 "product": product,
#                 "sub_product": sub_product,
#                 "segment_id": segment_id,
#                 "zuno_data": zuno_pdf_data
#             }), 200
#         else:
#             return jsonify({"error": "Failed to extract data for Zuno passenger carrying vechile"}), 500
        



#     # Default response if not Zuno and Two-wheeler
#     response = {
#         "company_name": company,
#         "product": product,
#         "sub_product": sub_product,
#         "segment_id": segment_id
#     }

#     return jsonify(response), 200
@api.route('/layer-1', methods=['POST'])
def handle_pdf_upload():
    data = request.get_json()

    # Check if the 'file' key exists in the data
    if 'file' not in data:
        return jsonify({"error": "No file provided"}), 400

    # Decode the base64 PDF file
    pdf_data = base64.b64decode(data['file'])
    pdf_file = BytesIO(pdf_data)

    # Extract text from PDF
    layer = Layer()
    extracted_text = layer.extract_text_from_pdf(pdf_file)

    # Identify the product, company, and sub-product
    product = layer.identify_product(extracted_text)
    company = layer.identify_company_name(extracted_text)
    sub_product = layer.identify_subproduct(extracted_text, product)

    # Define motor sub-products
    motor_sub_products = ["Two-wheeler", "private car", "goods carrying", "Passenger Carrying", "misc", 
                          "Two wheeler", "Goods Carrying", "Private Car", "Two-Wheeler", "Misc"]

    # Check if the sub_product belongs to motor sub-products
    if sub_product in motor_sub_products:
        product = "motor"
    else:
        # Re-identify product if sub-product is not in the list
        product = layer.identify_product(extracted_text)

    # Identify the segment
    segment_id = layer.identify_segment(extracted_text)

    # Handle specific cases for Zuno
    if company.lower() == 'zuno':
        if sub_product.lower() == 'two wheeler':
            zuno_pdf_data = extract_data_from_pdf_tw(pdf_file)  # Call Zuno-specific function for two-wheeler
            if zuno_pdf_data:
                return jsonify({
                    "company_name": company,
                    "product": product,
                    "sub_product": sub_product,
                    "segment_id": segment_id,
                    "zuno_data": zuno_pdf_data
                }), 200
            else:
                return jsonify({"error": "Failed to extract data for Zuno Two-wheeler"}), 500
        
        elif sub_product.lower() == 'private car':
            zuno_pdf_data = extract_data_from_pdf_pc(pdf_file)  # Call Zuno-specific function for private car
            if zuno_pdf_data:
                return jsonify({
                    "company_name": company,
                    "product": product,
                    "sub_product": sub_product,
                    "segment_id": segment_id,
                    "zuno_data": zuno_pdf_data
                }), 200
            else:
                return jsonify({"error": "Failed to extract data for Zuno Private Car"}), 500
        
        elif sub_product.lower() == 'passenger carrying':
            zuno_pdf_data = extract_data_from_pdf_pcv(pdf_file)  # Call Zuno-specific function for passenger carrying
            if zuno_pdf_data:
                return jsonify({
                    "company_name": company,
                    "product": product,
                    "sub_product": sub_product,
                    "segment_id": segment_id,
                    "zuno_data": zuno_pdf_data
                }), 200
            else:
                return jsonify({"error": "Failed to extract data for Zuno Passenger Carrying Vehicle"}), 500
        
        else:
            # Sub-product not recognized for Zuno
            return jsonify({"error": f"Zuno does not support the sub-product: {sub_product}"}), 400

    # Default case: If the company is not Zuno
    else:
        if not company:
            return jsonify({"error": "No valid company identified"}), 400
        
        # Add additional conditions for other companies as needed
        return jsonify({
            "company_name": company,
            "product": product,
            "sub_product": sub_product,
            "segment_id": segment_id,
            "error": "Company not supported or no specific extraction process available."
        }), 400