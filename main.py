import os
from bs4 import BeautifulSoup
import re

from dotenv import load_dotenv

# Loading environment data
load_dotenv()

# This functions write data in the ner_training_data file taking the website as a parameter and searching it
def create_training_data(website_request):
    html_soup = BeautifulSoup(website_request.text, 'html.parser')

    # This is a list of possible words to filter during experiments with the function
    skip_word = os.getenv('EXCLUDE_WORDS').split(',')

    # For a cleaner output we exclude all the tags that are unnecessary since products won't be in those
    for unwanted_tags in html_soup(["script", "style","svg"]):
        unwanted_tags.extract()

    # Almost always products are in divs so check for any div related to products using regex
    divs = html_soup.find_all("div", {"class": re.compile(r"product")} or {"id": re.compile(r"product")})

    # Extract the text from the tags, getting the products and storing them inside a list
    training_data = []
    for div in divs:
        product_tags = div.find_all(["p", "span"], {"class": re.compile(r"product")})

        for product in product_tags:
            product_text = product.get_text().strip()
            # Stripping any white space allows for a cleaner and easier to manage list
            if re.search(r"\A\d", product_text):
                continue
            elif re.search(r"^\$[0-9]|^£[0-9]|^€[0-9]", product_text):
                continue
            elif any(re.search(r"(price|amount|cost)", cls, re.IGNORECASE) for cls in product.get('class')):
                continue  # Skip this product tag if it has price-related classes
            elif any(re.search(r"(description|descr)", cls, re.IGNORECASE) for cls in product.get('class')):
                continue  # Skip this product tag if it has price-related classes
            elif any(keyword.lower() in product_text.lower() for keyword in skip_word):
                continue
            training_data.append(product_text)

    final_data = []
    for item in list(set(training_data)):
        entity = item.split()
        # Every new entity will have an index of 0 ,and thus we will change the notation
        for idx, token in enumerate(entity):
            if idx == 0:
                final_data.append((token,"B-PRODUCT"))
            else:
                final_data.append((token, "I-PRODUCT"))

    # Create the file with write mode first and then append to it
    with open("ner_training_data.txt","a") as f:
        for product in final_data:
            # A product has the item name and the label it has , beginning or inside to filter out we check the tag
            token, tag = product
            if tag == "B-PRODUCT":
                # Adding a new line separates products
                f.write(f"\n{token} {tag}\n")
            else:
                f.write(f"{token} {tag}\n")
        f.write('\n')
