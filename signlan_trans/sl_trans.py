#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Junjie Yang <yjunjie@163.com>
# Time: '2019/5/6 11:31'

from copy import deepcopy
from pypinyin import pinyin, Style
import json
from itertools import groupby
import re
# import sentence_segment
# from sentence_segment import nlpir
from signlan_trans.data_load import *
from signlan_trans.sent_seg import sentence_seg

USER_DICT = r'..//OtherData//user_dict.txt'

num_keyword = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '零']
num_regex = re.compile("([一二三四五六七八九十百千万零]{1,8})")


class Translate(object):
    def __init__(self, ):
        self.item_result_struct = dict(Word='', State=5, Type=None, Other=None, Md5=None, Visual=None, Emotion=None)
        self.sign_words_list = load_sign_words()  # 标准手语词汇
        self.synonym_words_dict = load_synonym_words()  # 同义词手语词汇
        self.combine_words_dict = load_combine_words()  # 组合词手语词汇
        self.filtrate_words_list = load_filtrate_reserve_words('filtrate')  # 过滤词
        self.filtrate_poses_list = ['q', 'uzhe', 'ule', 'uguo', 'ude1', 'ude2', 'ude3', 'usuo', 'udeng',
                                    'uyy', 'udh', 'uls', 'uzhi', 'ulian', 'e', 'y', 'o', 'x', 'xe', 'xm', 'xu', 'xx',
                                    'w', 'wkz', 'wky', 'wyz', 'wyy', 'wj', 'wt', 'wd', 'wf', 'wn', 'wm', 'ws', 'wp',
                                    'wb', 'wh']
        self.reserve_words_list = load_filtrate_reserve_words('reserve')  # 保留词
        self.visual_info = load_visualization_info()  # 具象化信息
        # sentence_segment.open()
        # nlpir.ImportUserDict(USER_DICT.encode('utf-8'), 1)  # 导入用户自定义词典

    def sent_trans(self, sentence):
        """
        'State'为分词状态码：1为准确词，2为近义表达替换词，3为组合表达替换词, 5为过滤词；
        """
        result_list = []
        word_pos_list = sentence_seg(sentence)
        global_visual = self.visual_info.get(sentence.replace("，", "").replace("。", ""))  # 检索句子的具象化视频
        for word, pos in word_pos_list:
            item_result = deepcopy(self.item_result_struct)  # 初始化数据结果
            item_result['Word'] = word
            item_result['Visual'] = global_visual
            # 过滤词处理
            if pos in self.filtrate_poses_list or word in self.filtrate_words_list and word not in self.filtrate_words_list:
                item_result['State'] = 5
            # 数量词处理
            elif pos in ['m', 'mq', 't']:
                # 阿拉伯数字及其他符号
                item_result['State'] = 3
                if word.isascii():  # Python3.6中str类型没有该方法
                    num_groups = [''.join(list(g)) for k, g in groupby(word, key=lambda x: x.isdigit())]  # 数字和符号分组
                    # item_result['State'] = 2 if len(num_groups) == 1 else 3
                    for num_group in num_groups:
                        if num_group.isdigit() and int(num_group) != 0:  # 非零阿拉伯数字
                            item_result['Other'] = self.digit_num_encode(num_group)
                        # elif int(num_group) == 0:  # 数值为零阿拉伯数字    ```
                        #     item_result['Other'] = \
                        #         [self.char_encode(c, deepcopy(self.item_result_struct)) for c in num_group]
                        else:  # 其他符号（包括数值为零的数字）
                            item_result['Other'] = self.char_encode(num_group)
                # 中文数字
                else:
                    item_result['State'] = 3
                    item_result['Other'] = self.char_encode(word)
            # 普通词处理
            else:
                self.word_encode(word, item_result)
            result_list.append(item_result)
        return result_list  # 返回list到服务器程序做后续处理

    def word_encode(self, word, item_result):
        """
        :param word: 分词后的词语
        :param item_result: 分词的格式化结果
        :return: 词语查询结果：
        'State'为分词状态码：1为准确词，2为近义表达替换词，3为组合表达替换词, 5为过滤词；
        'Other'值：进行替换的词语列表；
        'Type':手指语表达词语，需要进行离线处理
        """
        item_result['Word'] = word
        if not item_result['Visual']:
            item_result['Visual'] = self.visual_info.get(word)  # 如果没有句子的具象化视频则查找分词的具象化图片
        if word in self.sign_words_list:  # 查找标准手语词汇
            item_result['State'] = 1
        elif word in self.synonym_words_dict.keys():  # 查找同义词手语词汇
            item_result['State'], item_result['Other'] = \
                2, [self.word_encode(self.synonym_words_dict[word], deepcopy(self.item_result_struct))]
        elif word in self.combine_words_dict:  # 查找组合词手语词汇
            item_result['State'], item_result['Other'] = \
                3, [self.word_encode(seg, deepcopy(self.item_result_struct)) for seg in self.synonym_words_dict[word]]
        else:  # 针对词典未登录词语进行拆分查找，'Type'字段设置为0，用于词语日志记录
            item_result['State'], item_result['Type'] = 3, 0
            item_result['Other'] = self.char_encode(word)
        return item_result

    def char_encode(self, word):
        """
        针对单个字符进行查找，未找到词语采用手指语
        :return: 单个字符的处理结果
        """
        other = []
        for char in word:
            char_result = deepcopy(self.item_result_struct)
            if char in self.sign_words_list:  # 标准词查找
                char_result['State'], char_result['Word'] = 1, char
            elif char in self.synonym_words_dict.keys():  # 近义词查找
                char_result['State'], char_result['Word'] = 1, self.synonym_words_dict[char]
            else:  # 打指语
                char_result['State'], char_result['Word'] = 1, pinyin(char, style=Style.INITIALS)[0][0].upper()
            other.append(char_result)
        return other

    def digit_num_encode(self, digit_num) -> list:
        # other = []
        if len(digit_num) > 5:  # 万位以上的数字
            unit_before = int(digit_num) // 10000
            unit_after = int(digit_num) % 10000
            w_unit = [dict(Word='万', State=1, Type=None, Other=None, Md5=None, Visual=None,
                           Emotion=None)]
            if unit_after == 0:
                other = self.digit_num_encode(str(unit_before)) + w_unit
            elif unit_before == 0:
                other = self.digit_num_encode(str(unit_after))
            else:
                other = self.digit_num_encode(str(unit_before)) + w_unit + self.digit_num_encode(str(unit_after))
        else:  # 万位以内的数字
            other = self.digit_unit_encode(str(digit_num))
        return other

    def digit_unit_encode(self, num):
        """在阿拉伯数字中插入数值单位"""
        number_unit = [None,
                       dict(Word='十', State=1, Type=None, Other=None, Md5=None, Visual=None, Emotion=None),
                       dict(Word='百', State=1, Type=None, Other=None, Md5=None, Visual=None, Emotion=None),
                       dict(Word='千', State=1, Type=None, Other=None, Md5=None, Visual=None, Emotion=None),
                       dict(Word='万', State=1, Type=None, Other=None, Md5=None, Visual=None, Emotion=None)
                       ]
        h = len(num)
        t = 0  # 数字num后面0的个数
        number = int(num)
        while not number % 10:
            number = number // 10
            t += 1
        number_list = [self.ch_num_code(n) for n in num[:h - t]]
        i = 0
        while i <= h - t - 1:
            number_list.insert(2 * i + 1, number_unit[t:h][-(i + 1)])  # number_unit[t:h] 为当前数值需要用到的数值单位
            i += 1
        number_list = [item for item in number_list if item is not None]
        # number_list = self.rm_unit_zero(number_list)  # 去除连续出现的‘零“
        return number_list

    def ch_num_code(self, char_num):
        char_num_result = deepcopy(self.item_result_struct)
        char_num_result['State'], char_num_result['Word'] = 1, self.synonym_words_dict[char_num]
        return char_num_result


if __name__ == "__main__":
    trans = Translate()
    sent = '0123456'
    out_put = trans.sent_trans(sent)
    out_by_json = json.dumps({"WordSequence": out_put}, ensure_ascii=False, indent=4)
    print(out_by_json)
