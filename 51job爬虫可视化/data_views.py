# 最高工资图
import pandas as pd
from pandas import DataFrame, Series
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import jieba
import os


class data_to_view():
    def __init__(self, xlsx_name):
        self.xl_name = xlsx_name
        self.max_salary()
        self.min_salary()
        self.edu_requirements()
        self.min_experience()
        self.add_requirements()
        self.edu_pie()
        self.wordcloud()
        # self.broken()
        self.showimg()


    def max_salary(self):
        max_file_name = self.xl_name
        read_name_max = "%s.xlsx" % max_file_name
        # excel
        df = pd.read_excel(read_name_max)
        # 处理数据，把工资一列变成确定的格式
        df['工资'][df['工资'].str.findall('-').str.len() != 1] == '0-0'
        # 把工资的列转换成float格式
        low = df['工资'].str.replace('K', '').str.split('-').str[1].astype('float')
        df['工资'] = low
        # 根据工资进行排序
        df = df.sort_values(by="工资")
        low = df['工资']
        # 把需求人数一列转换成整型
        people = df['需求人数'].astype('int')
        # 定义画布，大小为（12，6）
        fig = plt.figure(figsize=(12, 6))
        # 添加图标
        axe = fig.add_subplot(1, 1, 1)
        # 显示中文
        plt.rcParams['font.sans-serif'] = ['simhei']
        x = low.tolist()
        y = people.tolist()
        axe.scatter(x, y, marker='.')
        max_title_name = max_file_name + "最高工资人数需求散点图"
        # 标题
        axe.set_title(max_title_name)
        # x轴标签
        axe.set_xlabel("工 资(单位/千)", fontsize=13)
        # y轴标签
        axe.set_ylabel("需 要 人 数", fontsize=13)
        max_salary_svg = max_file_name + "最高工资人数需求散点图.svg"
        # 保存图片
        plt.savefig(max_salary_svg)
        # 展示图片
        # plt.show()


    def min_salary(self):
        min_file_name = self.xl_name
        read_name_min = "%s.xlsx" % min_file_name
        # excel
        df = pd.read_excel(read_name_min)
        # 处理数据，把工资一列变成确定的格式
        df['工资'][df['工资'].str.findall('-').str.len() != 1] == '0-0'
        # 把工资的列转换成float格式
        low = df['工资'].str.replace('K', '').str.split('-').str[0].astype('float')
        df['工资'] = low
        # 根据工资进行排序
        df = df.sort_values(by="工资")
        low = df['工资']
        # 把需求人数一列转换成整型
        people = df['需求人数'].astype('int')
        # 定义画布，大小为（12，6）
        fig = plt.figure(figsize=(12, 6))
        # 添加图标
        axe = fig.add_subplot(1, 1, 1)
        # 显示中文
        plt.rcParams['font.sans-serif'] = ['simhei']
        x = low.tolist()
        y = people.tolist()
        axe.scatter(x, y, marker='.')
        min_title_name = min_file_name + "最低工资人数需求散点图"
        # 标题
        axe.set_title(min_title_name)
        # x轴标签
        axe.set_xlabel("工 资(单位/千)", fontsize=13)
        # y轴标签
        axe.set_ylabel("需 要 人 数", fontsize=13)
        min_salary_svg = min_file_name + '最低工资人数需求散点图.svg'
        # 保存图片
        plt.savefig(min_salary_svg)
        # 展示图片
        # plt.show()


    def edu_requirements(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        # excel
        df = pd.read_excel(read_name_cyl)
        # 学历
        names = df['学历'].value_counts().index.tolist()[:5]
        # 定义一个列表，用作X轴的位置
        x = range(len(names))
        # 显示中文的设置
        plt.rcParams['font.sans-serif'] = ['simhei']
        # y轴数据
        y = df['学历'].value_counts().tolist()[:5]
        # 定义一个画布
        fig = plt.figure(figsize=(12, 6))
        # 添加图表
        axe = fig.add_subplot(1, 1, 1)
        # 绘制柱状图
        axe.bar(x, y, tick_label=names)
        for i in range(len(names)):
            # 显示柱状图柱子上的数字
            axe.text(x[i] - 0.15, y[i] + 2, y[i])
        cyl_title_name = read_name_cyl + "学历要求柱状图"
        # 添加标题
        axe.set_title(cyl_title_name)
        edu_col_svg = read_name_cyl + '学历要求柱状图.svg'
        # 保存图片
        plt.savefig(edu_col_svg)
        # 展示图片
        # plt.show()


    def min_experience(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        df = pd.read_excel(read_name_cyl)  # excel
        min_ex = df["工作经验"].value_counts().index.tolist()
        # 定义一个列表，用作X轴的位置
        x = range(len(min_ex))
        # y轴数据
        y = df['工作经验'].value_counts().tolist()
        # 显示中文的设置
        plt.rcParams['font.sans-serif'] = ['simhei']
        # 定义一个画布
        fig = plt.figure(figsize=(12, 6))
        # 添加图表
        axe = fig.add_subplot(1, 1, 1)
        # 绘制柱状图
        axe.bar(x, y, tick_label=min_ex)
        for i in range(len(min_ex)):
            # 显示柱状图柱子上的数字
            axe.text(x[i] - 0.15, y[i] + 2, y[i])
        cyl_title_name = read_name_cyl + "工作经验要求柱状图"
        # 添加标题
        axe.set_title(cyl_title_name)
        exp_col_svg = read_name_cyl + '工作经验要求柱状图.svg'
        # 保存
        plt.savefig(exp_col_svg)
        # 显示
        # plt.show()


    def add_requirements(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        df = pd.read_excel(read_name_cyl)  # excel
        address = df["地点"].str[:2].value_counts().index.tolist()[:20]
        # 定义一个列表，用作X轴的位置
        x = range(len(address))
        # y轴数据
        y = df['地点'].value_counts().tolist()[:20]
        # 显示中文的设置
        plt.rcParams['font.sans-serif'] = ['simhei']
        # 定义一个画布
        fig = plt.figure(figsize=(12, 6))
        # 添加图表
        axe = fig.add_subplot(1, 1, 1)
        # 绘制柱状图
        axe.bar(x, y, tick_label=address)
        for i in range(len(address)):
            # 显示柱状图柱子上的数字
            axe.text(x[i] - 0.15, y[i] + 2, y[i])
        cyl_title_name = read_name_cyl + "城市出现的次数前20柱状图"
        # 添加标题
        axe.set_title(cyl_title_name)
        add_col_svg = read_name_cyl + '城市出现的次数前20柱状图.svg'
        # 保存
        plt.savefig(add_col_svg)
        # 显示
        # plt.show()


    def edu_pie(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        # excel
        df = pd.read_excel(read_name_cyl)
        # 学历
        names = df['学历'].value_counts().index.tolist()[:5]
        # 定义一个列表，用作X轴的位置
        x = range(len(names))
        # 显示中文的设置
        plt.rcParams['font.sans-serif'] = ['simhei']
        fig = plt.figure(figsize=(12, 6))
        axe = fig.add_subplot(1, 1, 1)
        # y轴数据
        y = df['学历'].value_counts().tolist()[:5]
        axe.pie(x=y, labels=names, autopct='%.2f%%')
        edu_pie_svg = read_name_cyl + '学历要求饼状图'
        axe.set_title(edu_pie_svg)
        edu_pie_svg = read_name_cyl + '学历要求饼状图.svg'
        # 保存图片
        plt.savefig(edu_pie_svg)
        # 展示图片
        # plt.show()


    def wordcloud(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        # excel
        df = pd.read_excel(read_name_cyl)
        # 职位名称
        title = "".join(df['职位名称'].value_counts().index.tolist())
        # 分词
        cut = jieba.cut(title)
        string = " ".join(cut)
        # 打开遮罩图片
        img = Image.open(r"prcie.jpg")
        # 将图片转换为数组
        img_array = np.array(img)
        # 设置参数
        wc = WordCloud(
            background_color='white',
            mask=img_array,
            font_path="msyh.ttc"
        )
        wc.generate_from_text(string)
        plt.figure(figsize=(12, 6))
        plt.imshow(wc)
        # 是否显示坐标轴
        plt.axis('off')
        # 显示生成的词云图片,可以直接保存就注释了
        word_cloud = read_name_cyl + '词云.jpg'
        # 保存
        plt.savefig(word_cloud)
        # 显示
        # plt.show()


    def change_num(self, a):
        res_list = []
        for i in a:
            res = i.split("K")[0]
            res_list.append(float(res))
        return sum(res_list)//len(res_list)

    def broken(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        # excel
        plt.rcParams['font.sans-serif'] = ['simhei']
        df = pd.read_excel(read_name_cyl)
        df2 = df[df['工作经验'].isin(["1年经验"])]
        result_2 = self.change_num(df2['工资'])
        df3 = df[df['工作经验'].isin(["2年经验"])]
        result_3 = self.change_num(df3['工资'])
        df4 = df[df['工作经验'].isin(["3-4年经验"])]
        result_4 = self.change_num(df4['工资'])
        df5 = df[df['工作经验'].isin(["5-7年经验"])]
        result_5 = self.change_num(df5['工资'])
        df6 = df[df['工作经验'].isin(["无需经验"])]
        result_6 = self.change_num(df6['工资'])
        df7 = df[df['工作经验'].isin(["没有"])]
        result_7 = self.change_num(df7['工资'])
        list_one = ["无需经验","没有","1年经验","2年经验","3-4年经验","5-7年经验"]
        list_two = [result_6, result_7, result_2, result_3, result_4, result_5]
        plt.figure(figsize=(20, 8), dpi=80)
        plt.plot(list_one, list_two)
        plt.xlabel("工作经验")
        plt.ylabel("工资(单位/K)")
        plt.title("工资和工作经验对应关系图")
        # 保存
        # plt.savefig(word_cloud, dpi=500)
        plt.show()


    def showimg(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx" % cyl_file_name
        html = open(r"./img.html", "w")
        html.write(
            '<!DOCtype HTML><head><title>图片</title></head>\n<body><table><tr><td><img src="./'+cyl_file_name+'最低工资人数需求散点图.svg"></td></tr><tr><td><img src="./'+cyl_file_name+'最高工资人数需求散点图.svg"></td></tr><tr><td><img src="./'+read_name_cyl + '学历要求柱状图.svg"></td></tr><tr><td><img src="./'+read_name_cyl + '工作经验要求柱状图.svg"></td></tr><tr><td><img src="./'+read_name_cyl + '城市出现的次数前20柱状图.svg"></td></tr></table><tr><td><img src="./'+read_name_cyl + '学历要求饼状图.svg"></td></tr><tr><td><img src="./'+read_name_cyl + '词云.jpg"></td></tr></body>')
        html.close()


if __name__ == '__main__':
    data_to_view("python")
