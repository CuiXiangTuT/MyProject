from datetime import datetime
import pandas as pd
import jieba


def get_word_frequency(title, article, total_list):
    """
    对标题和文章内容进行词频统计
    :param title: 文章标题
    :param article: 文章文本内容
    :return: 词频统计
    """
    res = jieba.lcut(title) + jieba.lcut(article)
    result = pd.value_counts(res)
    data_dict = {}

    for i, v in result.items():
        if len(i) != 1 and (i in total_list):
            data_dict[i] = v
    return data_dict


def manage_time_score(time_str):
    """
    对时间进行打分
    :param time_str: 时间字符串
    :return: 时间的分值
    """
    # 获取当前时间
    now_time = datetime.now()
    result = (now_time - datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')).days
    # 满分为10分
    # 当天，时效性最高
    if result == 0:
        score = 10
    # 3天内的
    elif result in range(1, 4):
        score = 9
    # 7天（一周）内的
    elif result in range(4, 8):
        score = 8
    # 10天内的
    elif result in range(8, 11):
        score = 7
    # 15天（半个月）内的
    elif result in range(11, 16):
        score = 6
    # 30天（一个月）内的
    elif result in range(16, 32):
        score = 5
    # 超过一个月的
    else:
        score = 1
    return score


