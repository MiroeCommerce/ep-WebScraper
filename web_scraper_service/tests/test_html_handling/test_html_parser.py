from bs4 import BeautifulSoup
from web_scraper_service.app.html_handling import html_utils
import pandas as pd
from unittest.mock import MagicMock


SAMPLE_HTML = """
<html>
  <head><title>Sample Store</title></head>
  <body>
    <div class="product-listing">
      <div class="product" data-id="101">
        <h2 class="title">Wireless Mouse</h2>
        <span class="price">$25.99</span>
        <p class="description">A smooth and responsive wireless mouse.</p>
        <span class="availability">In stock</span>
      </div>
      <div class="product" data-id="102">
        <h2 class="title">Mechanical Keyboard</h2>
        <span class="price">$89.50</span>
        <p class="description">Durable keyboard with backlit keys.</p>
        <span class="availability">Out of stock</span>
      </div>
    </div>
  </body>
</html>
"""

SAMPLE_HTML_MISSING = """
<div class="product">
    <span class="price">$10.00</span>
    <span class="availability">In stock</span>
    </div>
"""


# This helper class is used by the tests below
class VendorProductParser(html_utils.BaseProductParser):
    def parse_product_element(self):
        try:
            title = html_utils.HTMLParser.get_text_from_element(
                self.product.select_one(".title")
            )
            price = html_utils.HTMLParser.get_text_from_element(
                self.product.select_one(".price")
            )
            availability = html_utils.HTMLParser.get_text_from_element(
                self.product.select_one(".availability")
            )
            description = html_utils.HTMLParser.get_text_from_element(
                self.product.select_one(".description")
            )

            return {
                "title": title,
                "price": price,
                "availability": availability,
                "description": description,
            }
        except Exception as e:
            print(f"Error parsing product: {e}")
            return {
                "title": "N/A",
                "price": "0",
                "availability": "Unknown",
                "description": "",
            }


def test_parse_html_document():
    parser_instance = html_utils.HTMLParser(SAMPLE_HTML, "lxml")
    assert isinstance(parser_instance.soup, BeautifulSoup)
    assert parser_instance.soup.title.text == "Sample Store"


def test_parse_html_document_with_bytes():
    html_bytes = b"<html><body><p>Bytes content</p></body></html>"
    parser_instance = html_utils.HTMLParser(html_bytes, "lxml")
    assert isinstance(parser_instance.soup, BeautifulSoup)
    assert parser_instance.soup.find("p").text == "Bytes content"


def test_parse_html_document_with_invalid_html():
    parser_instance = html_utils.HTMLParser(12345, "lxml")
    assert parser_instance.soup is None


def test_get_elements_by_class():
    parser_instance = html_utils.HTMLParser(SAMPLE_HTML, "lxml")
    elements = parser_instance.get_elements_by_class("product")
    assert len(elements) == 2
    assert elements[0]["data-id"] == "101"


def test_get_elements_by_class_empty():
    parser_instance = html_utils.HTMLParser(SAMPLE_HTML, "lxml")
    elements = parser_instance.get_elements_by_class("products")
    assert len(elements) == 0


def test_parse_product_element():
    html_parser_instance = html_utils.HTMLParser(SAMPLE_HTML, "lxml")
    product_el = html_parser_instance.soup.select_one(".product")
    # FIX: Use the correct class name 'VendorProductParser'
    product_parser_instance = VendorProductParser(product_el)
    product_data = product_parser_instance.parse_product_element()

    assert product_data["title"] == "Wireless Mouse"
    assert product_data["price"] == "$25.99"
    assert product_data["availability"] == "In stock"
    assert product_data["description"] == "A smooth and responsive wireless mouse."


def test_parse_product_element_with_missing_fields():
    html_parser_instance = html_utils.HTMLParser(SAMPLE_HTML_MISSING, "lxml")
    el = html_parser_instance.soup.select_one(".product")

    # FIX: Use the correct class name 'VendorProductParser'
    product_parser_instance = VendorProductParser(el)
    result = product_parser_instance.parse_product_element()

    assert result["title"] == ""
    assert result["description"] == ""
    assert result["price"] == "$10.00"
    assert result["availability"] == "In stock"


def test_parse_product_error():
    broken_element = MagicMock()
    broken_element.select_one.side_effect = Exception("Broken HTML")

    # FIX: Use the correct class name 'VendorProductParser'
    product_parser_instance = VendorProductParser(broken_element)
    result = product_parser_instance.parse_product_element()

    assert result == {
        "title": "N/A",
        "price": "0",
        "availability": "Unknown",
        "description": "",
    }


def test_parse_products_to_dt():
    html_parser_instance = html_utils.HTMLParser(SAMPLE_HTML, "lxml")
    # FIX: Use the correct class name 'VendorProductParser'
    df_parser = html_utils.DataFrameParser(
        html_parser_instance, "product", VendorProductParser
    )
    df = df_parser.parse_products_to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "title" in df.columns
    assert df.iloc[0]["title"] == "Wireless Mouse"
    assert df.iloc[1]["title"] == "Mechanical Keyboard"
    assert len(df) == 2


def test_parse_products_to_dt_empty():
    html_parser_instance = html_utils.HTMLParser(SAMPLE_HTML, "lxml")
    # FIX: Use the correct class name 'VendorProductParser'
    df_parser = html_utils.DataFrameParser(
        html_parser_instance, "item", VendorProductParser
    )
    df = df_parser.parse_products_to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert df.empty
