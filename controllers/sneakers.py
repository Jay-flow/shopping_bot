import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from views.browser import Browser
from selenium.webdriver.support import expected_conditions
from time import sleep
from models.tables import ProductModel, ProductImageModel
from dataclasses import dataclass
from config import WEB_DRIVER_WAIT_TIME
from typing import Optional, List


@dataclass
class Size:
    name: str
    price: Optional[str]
    quantity: int


@dataclass
class Color:
    name: str
    price: int
    sizes: List[Size]


class Sneakers:
    def __init__(self, browser: Browser):
        self.browser = browser

    def insert(self, product_url: str):
        self.browser.web_driver_wait(
            (self.browser.By.CSS_SELECTOR, ".l_product_summary"),
            expected_conditions.visibility_of_element_located
        )
        self.__insert_products(product_url)
        self.__insert_options()
        self.__insert_images()

    def __insert_images(self):
        image_container = self.browser.web_driver.find_element_by_css_selector("#smallImg")
        images = image_container.find_elements_by_css_selector("img")
        for image in images:
            url = image.get_attribute("src").replace("resize/64x64/", "")
            print(url)

    def __input_personal_customs_clearance_unique_number(self):
        if self.browser.is_find_element(self.browser.By.CSS_SELECTOR, "input[title='개인통관고유번호']"):
            self.browser.web_driver.find_element_by_css_selector("input[title='개인통관고유번호']").send_keys("1")
            self.browser.web_driver.find_element_by_id("mirroredSecondOptionButton").click()

    def __insert_products(self, product_url: str):
        name = self.browser.web_driver.find_element_by_css_selector(".title").text
        price = int(
            self.browser.web_driver.find_element_by_css_selector(".price")
                .find_element_by_tag_name("span.value").text
                .replace(",", "")
        )
        delivery_charge = re.search(
            r"\d+", self.browser.web_driver.find_element_by_css_selector(".delivery dt").text
        ).group()
        arrival_probability = int(
            self.browser.web_driver.find_element_by_css_selector(".c_product_tooltip_style3 .text_num").text
                .replace("%", "")
        )
        arrival_date = self.browser.web_driver.find_element_by_css_selector(".delivery .text_em2").text
        courier = self.browser.web_driver.find_element_by_css_selector(".delivery span.text_num").text
        benefits = [benefit.text for benefit in
                    self.browser.web_driver.find_elements_by_css_selector(".benefit .c_product_btn_more5")]
        ProductModel(
            url=product_url,
            name=name,
            price=price,
            courier=courier,
            delivery_charge=delivery_charge,
            arrival_date=arrival_date,
            arrival_probability=arrival_probability,
            benefit=benefits,
        )

    def __get_size_quantity(self, size_container: WebElement):
        try:
            if size_container.find_element_by_css_selector("span.text_em_sm").text == "품절":
                return 0
        except NoSuchElementException:
            return None

    def __get_sizes(self) -> List[Size]:
        size_container_tag = "div[class='accordion_section bot_option_section " \
                             "c_product_dropdown_wrap c_product_dropdown_style1 active'] li"
        self.browser.web_driver_wait((self.browser.By.CSS_SELECTOR, size_container_tag),
                                     expected_conditions.visibility_of_all_elements_located)
        size_containers = self.browser.web_driver.find_elements_by_css_selector(size_container_tag)
        sizes = []
        for size_container in size_containers:
            size_name = size_container.find_element_by_tag_name("strong").text
            try:
                size_raw_price = size_container.find_element_by_css_selector("span[class='num value']")
                size_price = int(size_raw_price.text.replace(",", ""))
            except NoSuchElementException:
                size_price = None
            size_quantity = self.__get_size_quantity(size_container)
            sizes.append(
                Size(
                    name=size_name,
                    price=size_price,
                    quantity=size_quantity
                )
            )
        return sizes

    def __insert_options(self):
        self.__input_personal_customs_clearance_unique_number()
        color_container_selector = "ul[class='option_item_list bot_typ_01 b_product_buy_option']"
        self.browser.web_driver_wait((self.browser.By.CSS_SELECTOR, color_container_selector),
                                     expected_conditions.visibility_of_all_elements_located)
        color_container = self.browser.web_driver.find_element_by_css_selector(color_container_selector)
        color_options = color_container.find_elements_by_tag_name("li")
        for color_option in color_options:
            color_name = color_option.find_element_by_tag_name("strong").text
            color_price = int(
                color_option.find_element_by_css_selector("span[class='num value']").text.replace(",", "")
            )
            color_option.find_element_by_tag_name("button").click()
            sizes = self.__get_sizes()
            color = Color(
                name=color_name,
                price=color_price,
                sizes=sizes
            )
            print("Test")
