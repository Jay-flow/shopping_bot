from browser import Browser
from selenium.webdriver.support import expected_conditions
from time import sleep
from controllers.sneakers import Sneakers


class Main(Browser):
    url = "https://www.11st.co.kr/category/DisplayCategory.tmall" \
          "?method=getDisplayCategory2Depth&dispCtgrNo=1001877#id%%6161"

    def __init__(self):
        super().__init__()

    def process(self):
        self.start_chrome()
        self.loop_products()

    def wait_loading(self):
        loading_container = self.web_driver.find_element_by_css_selector("span.filter_dimmed")
        if loading_container.is_displayed():
            for time in range(30):
                if not loading_container.is_displayed():
                    return
                sleep(0.1)

    def loop_products(self) -> None:
        product_tag = "#product_listing .info_tit a"
        self.web_driver_wait((self.By.CSS_SELECTOR, product_tag),
                             expected_conditions.visibility_of_all_elements_located)
        products = self.web_driver.find_elements_by_css_selector(product_tag)
        for index, product in enumerate(products):
            self.web_driver_wait(
                (self.By.CSS_SELECTOR, product_tag),
                expected_conditions.visibility_of_all_elements_located
            )
            products = self.web_driver.find_elements_by_css_selector(product_tag)
            products[index].click()
            sleep(1)
            product_url = products[index].get_attribute("href")
            self.switch_window()
            Sneakers(self).insert(product_url)
            self.switch_window(True)

    def get_page(self) -> None:
        self.wait_loading()
        self.loop_products()
        links = self.web_driver.find_elements_by_css_selector("#list_paging a")
        for index, link in enumerate(links):
            links = self.web_driver.find_elements_by_css_selector("#list_paging a")
            links[index].click()
            self.wait_loading()
            self.loop_products()

        next_button_tag = "a.next"
        next_button = self.web_driver.find_element_by_css_selector(next_button_tag)
        if self.is_find_element(self.By.CSS_SELECTOR, next_button_tag):
            next_button.click()
            self.get_page()


if __name__ == '__main__':
    Main().process()
