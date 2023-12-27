from datetime import datetime

def convert_asc_date_to_datetime(asc_date_str):
    try:
        # You may need to adjust the format based on the actual date format in your ASC log
        datetime_obj = datetime.strptime(asc_date_str, "%a %b %d %I:%M:%S %p %Y")
        return datetime_obj
    except ValueError as e:
        print(f"Error converting ASC date to datetime: {e}")
        return None

if __name__ == "__main__":
    asc_date_str = "Wed Aug 09 01:27:06 AM 2023"  # Replace with the actual ASC date string
    datetime_obj = convert_asc_date_to_datetime(asc_date_str)

    if datetime_obj:
        print("Converted Datetime:", datetime_obj)
    else:
        print("Conversion failed.")
