import re
from dataclasses import dataclass
from typing import Optional, List, Union
from enum import Enum
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from sqlalchemy import null

from models.tables import ProductModel
from views.browser import Browser


class OptionType(Enum):
    COLOR = "color"
    SIZE = "size"


@dataclass
class OptionData:
    name: str
    price: Optional[str]
    quantity: int


@dataclass
class Option:
    title: str
    element: WebElement
    data: Optional[List[OptionData]]


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
        try:
            self.browser.web_driver.find_element_by_css_selector("input[title='개인통관고유번호']").send_keys("1")
            self.browser.web_driver.find_element_by_id("mirroredSecondOptionButton").click()
            return True
        except NoSuchElementException:
            return False

    def __insert_products(self, product_url: str):
        name = self.browser.web_driver.find_element_by_css_selector("h1.title").text
        price = int(
            self.browser.web_driver.find_element_by_css_selector(".price")
                .find_element_by_tag_name("span.value").text
                .replace(",", "")
        )
        find_delivery_charge = ''.join(
            re.findall(r"\d+[^개원,]", self.browser.web_driver.find_element_by_css_selector(".delivery dt").text)
        )
        delivery_charge = 0 if find_delivery_charge == '' else find_delivery_charge
        find_arrival_probability = self.browser.web_driver \
            .find_element_by_css_selector(".c_product_tooltip_style3 .text_num").text
        arrival_probability = None if find_arrival_probability == '' else int(find_arrival_probability.replace("%", ""))
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

    # def __get_sizes(self) -> List[Size]:
    #     size_container_tag = "div[class='accordion_section bot_option_section " \
    #                          "c_product_dropdown_wrap c_product_dropdown_style1 active'] li"
    #     self.browser.web_driver_wait(
    #         (self.browser.By.CSS_SELECTOR, size_container_tag),
    #         expected_conditions.visibility_of_all_elements_located
    #     )
    #     size_containers = self.browser.web_driver.find_elements_by_css_selector(size_container_tag)
    #     sizes = []
    #     for size_container in size_containers:
    #         size_name = size_container.find_element_by_tag_name("strong").text
    #         try:
    #             size_raw_price = size_container.find_element_by_css_selector("span[class='num value']")
    #             size_price = int(size_raw_price.text.replace(",", ""))
    #         except NoSuchElementException:
    #             size_price = None
    #         size_quantity = self.__get_quantity(size_container)
    #         sizes.append(
    #             Size(
    #                 name=size_name,
    #                 price=size_price,
    #                 quantity=size_quantity
    #             )
    #         )
    #     return sizes

    def __get_quantity(self, option: WebElement) -> int:
        try:
            find_text = option.find_element_by_css_selector("span.text_em_sm").text
            if find_text == "품절":
                return 0

            find_quantity = re.search(r"\d+", find_text)
            if find_quantity is not None:
                return int(find_quantity.group())
        except NoSuchElementException:
            pass
        return null()

    def __get_first_option(self, option_elements: List[WebElement]) -> WebElement:
        for idx, element in enumerate(option_elements):
            option_type = element.find_element_by_tag_name("input").get_attribute("value")
            if option_type == "색상":
                return element
            elif option_type == "사이즈":
                return element
        raise ValueError("알 수 없는 옵션입니다.")

    def __get_option_data(self, option_elements):
        for option_element in option_elements:
            name = option_element.find_element_by_tag_name("strong").text
            quantity = self.__get_quantity(option_element)
            pass

    def __insert_options(self):
        is_exist_clearance_number = self.__input_personal_customs_clearance_unique_number()
        option_selector = "#buyList > li"
        self.browser.web_driver_wait((self.browser.By.CSS_SELECTOR, option_selector),
                                     expected_conditions.visibility_of_all_elements_located)
        option_elements = self.browser.web_driver.find_elements_by_css_selector(option_selector)
        if is_exist_clearance_number:
            option_elements.pop(0)
        self.__get_option_data(option_elements)
        # color_name = color_option.find_element_by_tag_name("strong").text
        # color_quantity = self.__get_quantity(color_option)
        # sizes = null()
        # color_price = null()
        # if color_quantity != 0:
        #     color_price = int(
        #         color_option.find_element_by_css_selector("span[class='num value']").text.replace(',', '')
        #     )
        #     if self.browser.is_find_element(self.browser.By.CSS_SELECTOR, "input[value='색상']"):
        #         color_option.find_element_by_tag_name("button").click()
        #         sizes = self.__get_sizes()
        #         if idx < len(color_options) - 1:
        #             self.browser.web_driver.find_element_by_css_selector(".selected .btn").click()
        # color = Color(
        #     name=color_name,
        #     price=color_price,
        #     quantity=color_quantity,
        #     sizes=sizes
        # )
