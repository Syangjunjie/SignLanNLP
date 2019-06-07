#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Junjie Yang <yjunjie@163.com>
# Time: '2019/5/6 11:31'

from sentence_segment import sent_seg

FILTER_POS = ('q', 'uzhe', 'ule', 'uguo', 'ude1', 'ude2', 'ude3', 'usuo', 'udeng',
              'uyy', 'udh', 'uls', 'uzhi', 'ulian', 'e', 'y', 'o', 'x', 'xe', 'xm', 'xu', 'xx',
              'w', 'wkz', 'wky', 'wyz', 'wyy', 'wj', 'wt', 'wd', 'wf', 'wn', 'wm', 'ws', 'wp', 'wb', 'wh')


class SignLanTrans(object):
    def __init__(self):
        self.unfiltered_words = []
        self.stop_words = []
        self.visual_info = dict()

    def start(self, sent):
        """
        词语查询结果，其中'State'值：1为准确词，2为近义表达替换词，3为组合表达替换词, 5为过滤词；
        """
        seg_items = sent_seg(sent)
        result_list = []
        visual = self.visual_info.get(sent.replace("，", "").replace("。", ""))  # 检索句子的具象化视频
        for item in seg_items:
            word = item.word
            pos = item.nature.toString()
            item_result = dict(Word=word, State=None, Type=None, Other=None, Md5=None, Visual=visual, Emotion=None)
            if word:
                if pos in FILTER_POS and word not in self.unfiltered_words or word in self.stop_words:  # 过滤词
                    item_result['State'] = 5
                elif word in ['？', '?']:  # 对问号进行处理
                    result_list.append(
                        dict(Word=word, State=2, Type=None, Other=[dict(Word='问号', State=1, Type=None, Other=None,
                                                                        Md5=None, Visual=visual,
                                                                        Emotion=None)],
                             Md5=None, Visual=visual, Emotion=None))
                elif pos in ['m', 'mq', 't']:  # 对数字进行处理
                    num_words = [''.join(list(g)) for k, g in groupby(word, key=lambda x: x.isdigit())]
                    for num_word in num_words:
                        if num_word.encode('UTF-8').isdigit():
                            result_list.append(self.num_digit_process(num_word))
                        else:
                            chinese_num_list = re.split(num_regex, num_word)
                            for index, word in enumerate(chinese_num_list):
                                if index % 2 == 1:
                                    result_list.append(self.num_chinese_process(word))
                                elif index % 2 == 0 and word != '':
                                    result_list.append(self.word_encode(word))
                else:  # 对普通词语进行处理
                    result_list.append(self.word_encode(word, visual))
            else:
                result_list.append(
                    dict(Word=word, State=5, Type=None, Other=None, Md5=None, Visual=visual, Emotion=None))
            result_list.append(item_result)
