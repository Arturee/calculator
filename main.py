from selenium import webdriver
import smtplib


class Coronavirus():
    def __init__(self):
        self.driver = webdriver.Chrome("/home/vitaliisavchuk/Downloads/chromedriver_linux64/chromedriver")

    def get_data(self):
        self.driver.get('https://www.worldometers.info/coronavirus/')
        table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
        country_element = table.find_element_by_xpath("//td[contains(., 'Russia')]")
        row = country_element.find_element_by_xpath("./..")

        data = row.text.split(" ")
        total_cases = data[1]
        new_cases = data[2]
        total_deaths = data[3]
        new_deaths = data[4]
        active_cases = data[5]
        total_recovered = data[6]
        serious_critical = data[7]

        print("Country: " + country_element.text)
        print("Total cases: " + total_cases)
        print("New cases: " + new_cases)
        print("Total deaths: " + total_deaths)
        print("New deaths: " + new_deaths)
        print("Active cases: " + active_cases)
        print("Total recovered: " + total_recovered)
        print("Serious, critical cases: " + serious_critical)

        send_mail(country_element.text, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered)

        self.driver.close()


def send_mail(country_element, total_cases, new_cases, total_death, new_death, total_recovered, active_cases):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('your_post_server', 'your_google_app_password')

    subject = 'Coronavirus stats in ' + country_element + '!'

    body = 'Today in ' + country_element + '\
            \nThere is new data on coronavirus:\
            \nTotal cases: ' + total_cases + '\
            \nNew cases: ' + new_cases + '\
            \nTotal deaths: ' + total_death + '\
            \nNew deaths: ' + new_death + '\
            \nActive cases: ' + active_cases + '\
            \nTotal recovered: ' + total_recovered + '\
            \nCheck the link: https://www.worldometers.info/coronavirus/'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('FROM', 'TO', msg)
    print("Сообщение отправлено!")

    server.quit()


bot = Coronavirus()
bot.get_data()
