

def parse_receipt_text(text):
    # Extract item names
    items = []
    total_price = None
    subtotal_price = None
    tax_price = None

    # Split text into lines
    lines = text.split("<sep/>")
    
    for line in lines:
        # Parse lines containing item names and prices
        if "<s_nm>" in line and "<s_price>" in line:
            name_start = line.find("<s_nm>") + len("<s_nm>")
            name_end = line.find("</s_nm>", name_start)
            item_name = line[name_start:name_end].strip()

            price_start = line.find("<s_price>") + len("<s_price>")
            price_end = line.find("</s_price>", price_start)
            item_price = line[price_start:price_end].strip()

            items.append((item_name, item_price))
        
        # Extract total, tax, and subtotal information
        if "<s_subtotal_price>" in line:
            subtotal_price = line.split("<s_subtotal_price>")[1].split("</s_subtotal_price>")[0].strip()
        if "<s_tax_price>" in line:
            tax_price = line.split("<s_tax_price>")[1].split("</s_tax_price>")[0].strip()
        if "<s_total_price>" in line:
            total_price = line.split("<s_total_price>")[1].split("</s_total_price>")[0].strip()

    return items, subtotal_price, tax_price, total_price

