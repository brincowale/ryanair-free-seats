import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Ryanair:

    def __init__(self, reservation_number, mail, origin, destination):
        driver = self.create_driver()
        driver = self.select_paid_seat(driver, reservation_number, mail, origin, destination)
        self.get_captcha_square(driver)
        driver.quit()

    def create_driver(self):
        # spoof the useragent
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/46.0")
        # set options from browser
        service_args = ['--load-images=true', '--proxy-type=None', '--ignore-ssl-errors=true', '--webdriver-loglevel=OFF', '--ssl-protocol=tlsv1', '--debug=false']
        driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        # Set window size
        driver.set_window_size(2400, 2400)
        return driver

    def select_paid_seat(self, driver, reservation_number, mail, origin, destination):
        driver.get('https://www.bookryanair.com/SkySales/Booking.aspx?culture=es-ES&amp;lc=es-ES#Security')
        driver.find_element_by_xpath("//input[@id='BookingRetrieveSecurity_CONFIRMATIONNUMBER1']").send_keys(reservation_number)
        driver.find_element_by_xpath("//input[@id='BookingRetrieveSecurity_CONTACTEMAIL1']").send_keys(mail)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='BookingRetrieveSecurity_ORIGINCITY1']//option[@value='" + origin + "']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='BookingRetrieveSecurity_DESTINATIONCITY1']//option[@value='" + destination + "']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='BookingRetrieveSecurity_Buttons_Container']/button[@type='submit']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submitbutton']"))).click()
        # select paid seat, from 30 days before fly
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='seatOpt1']"))).click()
        return driver

    def get_captcha_square(self, driver):
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cabin fll']")))
        location = element.location
        size = element.size
        # get the size and position of element
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        # save image only from seats
        driver.save_screenshot('seats_page.png')
        im = Image.open('seats_page.png')
        im = im.crop((left, top, right, bottom))
        im.save('seats_' + datetime.datetime.now().strftime("%H-%M-%S-%M%p_%B-%d-%Y") + '.png')