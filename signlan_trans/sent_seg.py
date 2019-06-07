#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Junjie Yang <yjunjie@163.com>
# Time: '2019/5/6 9:41'

from pyhanlp import HanLP, CustomDictionary


def sentence_seg(sent):
    seg_items = HanLP.segment(sent)
    word_pos_list = [(item.word, item.nature.toString()) for item in seg_items]
    print(word_pos_list)
    return word_pos_list


def get_shengmu():
    # convertToPinyinFirstCharString
    for item in HanLP.convertToPinyinList('你好'):
        print(item.getShengmu())


def add_custom_dict(cust_items):
    for item in cust_items:
        CustomDictionary.add(item)


if __name__ == "__main__":
    sentence = "这里有二十几个人"
    print(sentence_seg(sentence))
    # custom_items = ['攻城狮', '单身狗']
    # add_custom_dict(custom_items)
    # print(sent_seg(sentence))
