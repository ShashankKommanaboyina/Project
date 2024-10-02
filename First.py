import zxing

def scan_barcode(image_path):
    # Create a ZXing reader
    reader = zxing.BarCodeReader()

    # Decode the barcode
    barcode = reader.decode("/content/maggi1.jpeg")

    # Check if a barcode was found
    if barcode:
        s_barcode=barcode.parsed
        print(f"Found barcode: {barcode.parsed}")
    else:
        print("No barcode found")
    return s_barcode

# Set the path for the image you want to scan
barcode=scan_barcode('C:\Users\shashank\Desktop\Project\8d8d90e0-6dba-4fb9-ab81-e3e89baa5b86.jpeg')
