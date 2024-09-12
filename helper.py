from datetime import datetime
from dateutil import parser

def convert_to_standard_format(date_str):
    try:
        date_obj = parser.parse(date_str)
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Unable to parse the date string: {date_str}")

# # Example usage
# date_str = "10-10-2024"
# formatted_date = convert_to_standard_format(date_str)
# print(formatted_date)  # Output: 2024-09-10
