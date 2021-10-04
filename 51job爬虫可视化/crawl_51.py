import requests
# from fake_useragent import UserAgent
import time
import pymongo
import re
import random
import json
from lxml import etree
from openpyxl import Workbook

# 设置请求头
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Cookie": "guid=ac6b5999b5be2a1c6f608ce0a2d99a4c; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; slife=lastvisit%3D210200%26%7C%26lowbrowser%3Dnot%26%7C%26; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAPython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAc%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAjava%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60060000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAPython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21"
}

# 创建几个空列表,也可以在类里面创建
now_price_list = []
salary_list = []
data_list = []

# 连接数据库
mongo_py = pymongo.MongoClient()
collection = mongo_py['51job_all']['data']


class Spider():
    def __init__(self, selection_list):
        # 传入一个列表,里面有四个数据,第一个是获取检索内容
        self.kword = selection_list[0]
        # 获取月薪范围中最低月薪,
        self.salary_min = selection_list[1]
        # 获取月薪范围中最高月薪
        self.salary_max = selection_list[2]
        # 获取输入的时间信息
        self.time = selection_list[3]
        # 获取页数值
        # url_1 = "https://search.51job.com/list/000000,000000,0000,00,9,99," + self.kword + ",2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        # response_one = requests.get(url_1, headers=head).text
        # total_page = re.findall(r'"total_page":"(.*?)",', response_one)[0]
        # print(total_page)

    # 启动爬虫
    def run_1(self):
        # 可调整页数
        for i in range(1, 2):
            # 清空列表的数据,避免重复爬取
            href_list = []
            url_list = []
            # head_1 = {
            #     "User-Agent": "{}".format(UserAgent().random)
            # }
            # 获取时间对应的字典
            time_dict = {
                "所有": 9,
                "24小时内": 0,
                "近三天": 1,
                "近一周": 2,
                "近一月": 3,
                "其他": 4
            }
            url = "https://search.51job.com/list/000000,000000,0000,00,"+str(time_dict[self.time])+","+str(self.salary_min)+"-"+str(self.salary_max)+"," + self.kword + ",2," + str(
                i) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
            try:
                # try一下避免出错
                self.r = requests.get(url, headers=head, timeout=30)
            except:
                pass
            self.r.encoding = "utf-8"
            # 得用正则爬取
            self.data = re.findall(r'"engine_jds":(.*?),"jobid_count"', self.r.text)[0]
            # 解码 JSON 数据
            self.data = json.loads(self.data)
            # 添加所有的url
            for item in self.data:
                href_list.append(item["job_href"])
            # 筛选url
            for url_1 in href_list:
                # 避免有广告之类的网址出现
                if "id" in url_1:
                    continue
                else:
                    # 得到所有需要的网址
                    url_list.append(url_1)
            # 间隔一下,避免出现网址反应过快
            # time.sleep(5)
            for u in range(len(url_list)):
                try:
                    # 遍历所有的url去调用get_data这个函数
                    # time.sleep(random.randint(1, 2))
                    print(url_list[u])
                    self.get_data(url_list[u])
                # 出现广告之类的错误就跳过
                except IndexError:
                    continue
                except UnicodeDecodeError:
                    continue
                except Exception:
                    break
        # 清空原数据库
        collection.delete_many({})
        # 把数据存入数据库
        for j in data_list:
            if j[5] == "0K-0K":
                continue
            else:
                collection.insert_one({
                    "公司名称": j[0],
                    "地点": j[1],
                    "学历": j[2],
                    "工作经验": j[3],
                    "更新时间": j[4],
                    "工资": j[5],
                    "职位名称": j[6],
                    "需求人数": j[7],
                    "职责": j[8]
                })
        # 再把数据导入到xlsx文件中
        res_list = []
        for item in collection.find():
            res_list.append(
                [item['公司名称'], item['地点'], item['学历'], item['工作经验'], item['更新时间'], item['工资'], item['职位名称'],
                 item['需求人数'], item['职责']])
        fire = Workbook()
        sheet = fire.active
        sheet.append(["公司名称", "地点", "学历", "工作经验", "更新时间", "工资", "职位名称", "需求人数", "职责"])
        for i in res_list:
            sheet.append(i)
        fire.save('%s.xlsx' % self.kword)
        return salary_list

    # 薪资处理函数
    def salary_solve(self, salary):
        if '万/月' in salary:
            # 先去除万/月,然后乘以10
            salary_1 = salary.split('万/月')
            salary_2 = salary_1[0].split('-')
            salary_fin = [str(int(float(salary_2[0]) * 10)), str(int(float(salary_2[1]) * 10))]
        elif '没有' in salary:
            # 没有就为0,0然后再处理
            pass
            salary_fin = ["0", "0"]
        elif '万/年' in salary:
            # 先去除万/年,然后乘以1.2
            salary_1 = salary.split('万/年')
            salary_2 = salary_1[0].split('-')
            salary_fin = [str(int(float(salary_2[0]) / 12 * 10)), str(int(float(salary_2[1]) / 12 * 10))]
        else:
            # 直接去除千/月,再去除-
            salary_1 = salary.split('千/月')
            salary_fin = salary_1[0].split('-')
        return salary_fin

    # 招聘人数处理函数
    def people_solve(self, people):
        if people == "没有详细说明":
            people_fin = 1
        else:
            people_1 = people.split("招")[1].split('人')[0]
            if people_1 == "若干":
                people_fin = 5
            else:
                people_fin = people_1
        return people_fin

    # 得到所需要的数据
    def get_data(self, url):
        response = requests.get(url, headers=head, timeout=20).content.decode('gbk')
        # 使用xpath获取数据
        data = etree.HTML(response)
        # 职位名称
        job_name = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()')
        job_name = "没有" if job_name == [] else job_name[0]
        # 工资
        price = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()')
        price = "没有" if price == [] else price[0]
        # 再处理工资
        price_fin = self.salary_solve(price)
        b = [price_fin[0] + "K", price_fin[1] + "K"]
        price_end = '-'.join(b)
        for sl in price_fin:
            if sl != '-':
                if sl == '0':
                    continue
                else:
                    salary_list.append(sl)
        # 公司名称
        company_name = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()')[0]
        if len(data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')) == 5 or len(
                data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')) > 5:
            # 更新时间
            issue_time = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[4].replace("  ", "")
            # 地址
            address = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[0].replace("  ", "")
            # 工作经验
            experience = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[1].replace("  ", "")
            # 学历
            education = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[2].replace("  ", "")
            # 招聘人数
            people_number = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[3].replace("  ", "")
        else:
            # 因为网址会变化,所以加了些判断
            address = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[0].replace("  ", "")
            issue_time = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[-1].replace("  ", "")
            for j in range(len(data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()'))):
                if "人" in data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[j]:
                    people_number = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[j].replace(
                        "  ", "")
                else:
                    people_number = "没有详细说明"
            for m in range(len(data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()'))):
                if "经验" in data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[m]:
                    experience = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[m].replace("  ",
                                                                                                                 "")
                else:
                    experience = "没有"
            education = "没有"
        position_information = data.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()')
        position_information = \
            "".join(position_information).strip().split("\n", 0)[0].split("职能类别", 1)[0].replace("\r\n", "").split(
                "工作时间",
                1)[
                0].split("联系人", 1)[0].replace("\xa0", "").replace("\u3000\u3000", "")
        # 再处理招聘人数
        people_number = self.people_solve(people_number)
        # 添加到列表中
        data_list.append([company_name, address, education, experience, issue_time, price_end, job_name, people_number,
                          position_information])
        # 返回工资列表
        return salary_list


if __name__ == '__main__':
    a = Spider(["java", "3000", "8000", "所有"]).run_1()
