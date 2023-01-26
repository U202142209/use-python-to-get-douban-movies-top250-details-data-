import requests                 # 网络请求模块
from lxml import etree          # 数据解析模块
                                # 请求头信息
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'
}
                                # 功能函数，胡哦去列表的而第一个元素
def get_first_text(list):
    try:
        return list[0].strip()  # 返回第一个字符串，除去两端的空格
    except:
        return ""               # 返回空字符串

import pandas as pd
df=pd.DataFrame(columns=["序号","标题","链接","导演","评分","评价人数","简介"])

                                # 使用列表生成式表示10个页面的地址
urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i * 25)) for i in range(10)]
count = 1                       # 用来计数
for url in urls:
    res = requests.get(url=url, headers=headers)  # 发起请求
    html = etree.HTML(res.text)  # 将返回的文本加工为可以解析的html
    lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')  # 获取每个电影的li元素
                                # 解析数据
    for li in lis:
        title = get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))  # 电影标题
        src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))  # 电影链接
        dictor = get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))  # 导演
        score = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))  # 评分
        comment = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))  # 评价人数
        summary = get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))  # 电影简介
        print(count, title, src, dictor, score, comment, summary)  # 输出

        df.loc[len(df.index)]=[count,title,src,dictor,score,comment,summary]

        count += 1

df.to_excel("豆瓣电影top250数据.xlsx",sheet_name="豆瓣电影top250数据",na_rep="")
