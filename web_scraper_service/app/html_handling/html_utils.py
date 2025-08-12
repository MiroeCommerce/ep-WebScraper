from bs4 import BeautifulSoup
import pandas as pd
from typing import Type
from web_scraper_service.app.utils.loguru_logger import logger


class HTMLParser:
    def __init__(self, raw_html: str, parser: str):
        """
        Initializes the HTMLParser with raw HTML and a specified parser.

        Args:
            raw_html (str): Raw html of the website to be parsed.
            parser (str): Type of parser to be used (e.g., 'html.parser', 'lxml').
        """

        self.raw_html = raw_html
        self.parser = parser
        self.soup = self.parse_html_document()

    def parse_html_document(self):
        """
        Parse html document based on passed parser.

        Returns:
            BeautifulSoup: Parsed sour object or None on error.

        """
        try:
            if isinstance(self.raw_html, bytes):
                raw_html_decoded = self.raw_html.decode("utf-8", errors="replace")
            else:
                raw_html_decoded = self.raw_html
            soup = BeautifulSoup(raw_html_decoded, self.parser)
            logger.debug("HTML parsed successfully.")
            return soup
        except Exception as e:
            logger.exception("Failed to parse HTML")
            # print(f"Failed to parse HTML: {e}")
            return None

    def get_elements_by_class(self, class_name: str):
        """
        Finds all elements matching a specific class name.

        Args:
            class_name (str): The name class to be searched by.git

        Returns:
            list[tag]: List of matching elements (or empty list).

        """
        if not self.soup:
            logger.warning("Soup object is None, returning empty list.")
            return []
        try:
            elements = self.soup.find_all(class_=class_name)
            logger.debug(f"Found {len(elements)} elements with class '{class_name}'.")
            return elements
        except Exception:
            logger.exception(f"error while getting elements by class: {class_name}")
            return []

    @staticmethod
    def get_text_from_element(element):
        """
        Extracts clean, stripped text from a BeautifulSoup element.

        Args:
            element (bs4.element.Tag): The BeautifulSoup element.

        Returns:
            str: The cleaned text from the element.
        """

        if element is None:
            logger.warning("Element is None, returning empty string.")
            return ""
        text = element.get_text(separator=" ", strip=True)
        logger.debug("Extracted text from element successfully.")
        return " ".join(text.split())


class BaseProductParser:
    def __init__(self, product):
        """
        Initializes the ProductParser with a product HTML element. Each vendor class will be inherited from it.

        Args:
            product_element (bs4.element.Tag): The HTML element representing a single product.
        """

        self.product = product

    def parse_product_element(self):
        """
        Extract product info from a product HTML element.

        Returns:
            dict: product data fields like title, price, availability, description
        """
        # This method should be implemented for each vendor
        raise NotImplementedError(
            "Vendor subclasses must implement parse_product_element method."
        )


class DataFrameParser:
    def __init__(
        self,
        html_parser: HTMLParser,
        product_class: str,
        product_parser_class: Type[BaseProductParser],
    ):
        """
        Create a DataFrame with products information.

        Args:
            html_parser (HTMLParser): An instance of HTMLParser containing the parsed HTML.
            product_class (str): Class name used to identify product elements.
            product_parser_class (type[BaseProductParser]): The specific ProductParser class to use for this vendor.
        """

        self.product_class = product_class
        self.html_parser = html_parser
        self.product_parser_class = product_parser_class

    def parse_products_to_dataframe(self):
        """
        Parse all product elements from soup and return a DataFrame.

        Args:
            product_class (str): Class name used to identify product elements.

        Returns:
            pd.DataFrame: DataFrame with product data.
        """
        try:
            elements = self.html_parser.get_elements_by_class(self.product_class)
            products_data = []
            for el in elements:
                product_parser = self.product_parser_class(el)
                products_data.append(product_parser.parse_product_element())
            df = pd.DataFrame(products_data)
            return df
        except Exception:
            logger.exception("An error occured.")


class VendorProductParser(BaseProductParser):
    def parse_product_element(self):
        try:
            title = HTMLParser.get_text_from_element(self.product.select_one(".title"))
            price = HTMLParser.get_text_from_element(self.product.select_one(".price"))
            availability = HTMLParser.get_text_from_element(
                self.product.select_one(".availability")
            )
            description = HTMLParser.get_text_from_element(
                self.product.select_one(".description")
            )
            logger.debug(f"Parsed product: {title}")
            return {
                "title": title,
                "price": price,
                "availability": availability,
                "description": description,
            }

        except Exception as e:
            logger.exception("Error parsing product")
            return {
                "title": "N/A",
                "price": "0",
                "availability": "Unknown",
                "description": "",
            }