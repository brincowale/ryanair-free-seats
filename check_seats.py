import time
import datetime
import argparse
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Ryanair:

    def __init__(self, args):
        self.driver = self.create_driver()
        self.reservation = args.reservation
        self.email = args.email
        self.check_seat()

    def check_seat(self):
        self.get_to_seat_map()
        self.save_seat_map()
        self.driver.quit()

    def create_driver(self):
        # spoof the useragent
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/46.0")
        # set options from browser
        service_args = ['--load-images=true', '--proxy-type=None', '--ignore-ssl-errors=true',
                        '--webdriver-loglevel=OFF', '--ssl-protocol=tlsv1', '--debug=false']
        driver = webdriver.PhantomJS(
            desired_capabilities=dcap, service_args=service_args)
        # Set window size
        driver.set_window_size(2400, 2400)
        return driver

    def get_to_seat_map(self):
        print('getting url')
        self.driver.get('https://www.ryanair.com/gb/en/')
        self.screenshot('homepage')
        self.element_wait(
            "//*[@id='manage-trips']/a"
        ).click()
        self.screenshot('clicked')
        self.element_wait(
            "//*[@name='reservationNum']"
        ).send_keys(self.reservation)
        self.element_wait(
            "//*[@name='email']"
        ).send_keys(self.email)
        self.screenshot('filled')
        self.element_wait(
            "button[translate='trips.my_trips.go']", By.CSS_SELECTOR
        ).click()
        self.screenshot('manage_page')
        self.element_wait(
            "button[translate='trips.active.spotlight.seats.button']", By.CSS_SELECTOR
        ).click()
        self.element_wait(
            'seat-type-icon', By.CLASS_NAME)
        self.screenshot('seat_map')

    def element_wait(self, selector, by=By.XPATH, timeout=20):
        print('Waiting for element %s by %s' % (selector, by))
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(
            (by, selector)))

    def save_seat_map(self):
        # get dimenstion of seat map
        element = self.element_wait("//div[@class='seat-map-plane']")
        left = int(element.location['x'])
        top = int(element.location['y'])
        right = left + element.size['width']
        bottom = top + element.size['height']
        # take screenshot and crop it
        self.screenshot('seats_page')
        im = Image.open('seats_page.png')
        im = im.crop((left, top, right, bottom))
        filename = 'seats_%s.png' % datetime.datetime.now().strftime("%H-%M-%S-%M%p_%B-%d-%Y")
        print('Saving %s' % filename)
        im.save(filename)

    def screenshot(self, filename):
        print('Saving screenshot as: %s.png' % filename)
        self.driver.get_screenshot_as_file('%s.png' % filename)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reservation', required=True,
                        help='Flight reservation number')
    parser.add_argument('-e', '--email', required=True,
                        help='Email address used for reservation')
    parser.add_argument('-t', '--poll-interval', type=int, default=600,
                        help='Time in seconds between checks')
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        Ryanair(args)
        print('Sleeping for %d seconds' % args.poll_interval)
        time.sleep(args.poll_interval)


if __name__ == '__main__':
    main()
