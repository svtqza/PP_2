import re
import json
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


# 1. Extract prices

price_pattern = r"\d[\d ]*,\d{2}"
prices = re.findall(price_pattern, text)

prices_clean = [p.replace(" ", "").replace(",", ".") for p in prices]
prices_float = [float(p) for p in prices_clean]


# 2. Extract product names

product_pattern = r"\d+\.\n(.+)"
products = re.findall(product_pattern, text)


# 3. Extract date and time

datetime_pattern = r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}"
datetime_match = re.search(datetime_pattern, text)
datetime_value = datetime_match.group() if datetime_match else None


# 4. Extract payment method

payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)
payment_method = payment_match.group() if payment_match else "Unknown"


# 5. Extract total

total_pattern = r"ИТОГО:\s*([\d\s]+,\d{2})"
total_match = re.search(total_pattern, text)

if total_match:
    total = total_match.group(1).replace(" ", "").replace(",", ".")
    total = float(total)
else:
    total = None


# 6. Create structured output

data = {
    "products": products,
    "prices": prices_float,
    "total_amount": total,
    "date_time": datetime_value,
    "payment_method": payment_method
}


print(json.dumps(data, indent=4, ensure_ascii=False))