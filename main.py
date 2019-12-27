#encoding: utf-8
#create time: 2019/1/16

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver_path = "/Users/suntie/PycharmProjects/chromedriver"

# print(driver.page_source)

class Qiangpiao(object):
    def __init__(self):
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        self.initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
        self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init"
        self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

        self.driver = webdriver.Chrome(executable_path = driver_path)

    def wait_input(self):
        self.from_station = input("出发地: ")
        self.to_station = input("目的地：")
        self.depart_time = input("出发日: ")
        self.passengers = input("乘客姓名（如有多个乘客，用英文逗号隔开）: ").split(",")
        self.trains = input("车次（如有多个车次，用英文逗号隔开）: ").split(",")
        # ["G1002","G72"]

    def _login(self):
        self.driver.get(self.login_url)
        # 显示等待
        WebDriverWait(self.driver,1000).until(
            EC.url_to_be(self.initmy_url)
        )
        print('登录成功！')

    def _order_ticker(self):
        self.driver.get(self.search_url)
        print("进入查询页面")

        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,"fromStationText"),self.from_station)
        )
        print("校验出发地正确")

        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "toStationText"), self.to_station)
        )
        print("校验目的地正确")

        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "train_date"), self.depart_time)
        )
        print("校验出发日正确")

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.ID,"query_ticket"))
        )
        print("查询按钮可以点击")
        # 执行查询点击按钮
        searchBtn = self.driver.find_element_by_id("query_ticket")
        searchBtn.click()
        print("查询按钮点击")

        # 等待判断查询的车次信息是否显示
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH,".//tbody[@id='queryLeftTable']/tr"))
        )

        # 找到所有没有datatran属性的标签，这些标签存储了车次信息
        tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")

        # 便利所有满足条件的tr标签
        for tr in tr_list:
            train_number = tr.find_element_by_class_name("number").text
            print(train_number)
            if train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[4]").text
                print(left_ticket)
                if left_ticket == "有" or left_ticket.isdigit():
                    print(train_number + "有票")
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()
                    #等待是否来到了乘客页面
                    WebDriverWait(self.driver, 1000).until(
                        EC.url_to_be(self.passenger_url)
                    )
                    print("乘客页面加载成功")
                    #等待所有乘客信息是否都被加载进来
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.XPATH,".//ul[@id='normal_passenger_id']/li"))
                    )
                    print("乘客信息显示成功")
                    #获取所有乘客信息
                    passenger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passenger_label in passenger_labels:
                        name = passenger_label.text
                        if name in self.passengers:
                            passenger_label.click()
                            print("已选要选的乘客")
                    #获取提交订单的按钮
                    submitBtn = self.driver.find_element_by_id("submitOrder_id")
                    submitBtn.click()
                    print("提交订单")

                    # 显示等待确认订单的对话框是否已经加载出来了
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME,"dhtmlx_wins_body_outer"))
                    )

                    #显示等待确认按钮显示出来
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.ID, "qr_submit_id"))
                    )

                    confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                    confirmBtn.click()

                    while confirmBtn:
                        confirmBtn.click()
                        confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                        # if(EC.url_changes(self.passenger_url)):
                        #     print("抢票成功!!!!!!!!!!!!!!")
                        #     return;


                    return

            print('=' * 20)
#G1002,G72,K1348,G1004,G74,G1008

#G1005,G1007,G1009,G1035,G1031,G1013,G1015,G279,G817,G1017,G821,G1019,G6033,G75,G1021,G825,G6027

    def run(self):
        self.wait_input()
        self._login()
        self._order_ticker()

if __name__ == '__main__':
    spider = Qiangpiao()
    spider.run()



