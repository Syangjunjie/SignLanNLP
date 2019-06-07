#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Junjie Yang <yjunjie@163.com>
# Time: '2019/5/6 11:31'
from collections import defaultdict


STD_SIGN_PATH = r'..//SignWordData//1_1_standard_sign_words.txt'  # 标准手语词典
EXT_SIGN_PATH = r'..//SignWordData//1_2_extend_sign_words.txt'
ALPHABET_PATH = r'..//SignWordData//1_3_alphabet_words.txt'
SYNONYM_SIGN_PATH = r'..//SignWordData//2_1_synonym_sign_words.txt'
NUM_SIGN_PATH = r'..//SignWordData//2_2_num_sign_words.txt'
COMBINE_SIGN_PATH = r'..//SignWordData//3_combine_words.txt'
FILTRATE_WORDS_PATH = r'..//SignWordData//5_1_filtrate_words.txt'
RESERVE_WORDS_PATH = r'..//SignWordData//5_2_reserve_words.txt'

VISUALIZATION_INFO = r'..//OtherData//visualization_info.txt'


def load_sign_words():
    sign_words_list = []
    for path in [STD_SIGN_PATH, EXT_SIGN_PATH, ALPHABET_PATH, NUM_SIGN_PATH]:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                sign_word = line.strip().split(' ')[0]
                sign_words_list.append(sign_word)
    return sign_words_list


def load_synonym_words():
    synonym_words_dict = defaultdict(str)
    for path in [STD_SIGN_PATH, EXT_SIGN_PATH, SYNONYM_SIGN_PATH, NUM_SIGN_PATH]:
        with open(path, 'r', encoding='utf-8') as sf:
            for line in sf.readlines():
                line_words = line.strip().split(' ')
                tag = line_words[0]
                for word in line_words[1:]:
                    synonym_words_dict[word] = tag
    return synonym_words_dict


def load_combine_words():
    combine_words_dict = defaultdict(list)
    with open(COMBINE_SIGN_PATH, 'r', encoding='utf-8') as cf:
        for line in cf.readlines():
            line_words = line.strip().split(' ')
            combine_word = line_words[0]
            combine_words_dict[combine_word] = line_words[1:]
    return combine_words_dict


def load_filtrate_reserve_words(t='filtrate'):
    path = FILTRATE_WORDS_PATH if t == 'filtrate' else RESERVE_WORDS_PATH
    words = []
    with open(path, 'r', encoding='utf-8') as frf:
        for line in frf.readlines():
            word = line.strip()
            words.append(word)
    return words


def load_visualization_info():
    visual_info = dict()
    with open(VISUALIZATION_INFO, 'r', encoding='utf-8') as vf:
        for line in vf.readlines():
            split = line.splitlines()[0].strip().split(' ', 1)
            if len(split) != 2:
                continue
            visual_info[split[0]] = split[1]
    return visual_info

#
# # eg: {'爱护' , '爱情' , '爱人'}
# def load_sign_dict(*params):  # 读取手语词表词语
#     sign_words = []
#     for param in params:
#         with open(param, 'r', encoding='utf-8') as sf:
#             for line in sf.readlines():
#                 line_words = line.strip().split(' ')
#                 for word in line_words:
#                     sign_words.append(word)
#     return set(sign_words)
#
#
# # eg: {'大姨'：'阿姨'，'姨娘'：'阿姨'}
# def load_syn_dict(syn_dict_path):  # 读取手语近义词词典
#     syn_word_dict = defaultdict(str)
#     with open(syn_dict_path, 'r', encoding='utf-8') as sf:
#         for line in sf.readlines():
#             line_words = line.splitlines()[0].strip().split(' ')
#             tag = line_words[0]
#             for word in line_words[1:]:
#                 syn_word_dict[word] = tag
#     return syn_word_dict
#
#
# # eg: {'国标':['国家','标准'], '正常人':['正常','人']}
# def load_seg_dict(seg_dict_path):  # 读取词语分割字典
#     seg_dict = defaultdict(list)
#     with open(seg_dict_path, 'r', encoding='utf-8') as seg_f:
#         for line in seg_f.readlines():
#             line_words = line.splitlines()[0].strip().split(' ')
#             seg_word = line_words[0]
#             seg_dict[seg_word] = line_words[1:]
#     return seg_dict
#
#
# # eg: {'二百', '三百'}， {'200':'二百', '两百':'二百', '300':'三百'}
# def load_extend_dict(extend_dict_path):  # 读取扩充词汇
#     extend_dict = []
#     extend_syn_dict = defaultdict(str)
#     with open(extend_dict_path, 'r', encoding='utf-8') as sf:
#         for line in sf.readlines():
#             line_words = line.splitlines()[0].strip().split(' ')
#             extend_dict.append(line_words[0])
#             for word in line_words[1:]:
#                 extend_syn_dict[word] = line_words[0]
#     return set(extend_dict), extend_syn_dict
#
#
# # eg: {'国家标准':['国家','标准']}
# def load_seg_syn_dict(seg_syn_dict_path, seg_dict):  # 读取组合表达词汇的近义词
#     seg_syn_dict = defaultdict(str)
#     with open(seg_syn_dict_path, 'r', encoding='utf-8') as sf:
#         for line in sf.readlines():
#             line_words = line.splitlines()[0].strip().split(' ')
#             tag = line_words[0]
#             express_word = seg_dict[tag]
#             for word in line_words[1:]:
#                 seg_syn_dict[word] = express_word
#     return seg_syn_dict
#
#
# # eg: {'啊', '哦'}
# def load_stop_words(stop_word_path):
#     stop_words = [' ']  # 默认空格为停用词
#     with open(stop_word_path, mode="r", encoding='utf-8') as rf:
#         for line in rf.readlines():
#             word = line.strip()
#             stop_words.append(word)
#     stop_words = set(stop_words)
#     return stop_words
#
#
# def load_reserve_words(unfilter_word_path):  # 非过滤词
#     unfilter_words = []
#     with open(unfilter_word_path, mode='r', encoding='utf-8') as rf:
#         for line in rf.readlines():
#             word = line.strip()
#             unfilter_words.append(word)
#     unfilter_words = set(unfilter_words)
#     return unfilter_words
#
#
# def load_emotion_dict(emotion_dict_path):
#     with open(emotion_dict_path, 'r', encoding='utf-16') as ef:
#         emotion_dict = defaultdict(str)
#         for line in ef.readlines():
#             line_elements = line.strip().split('\t')
#             emotion_dict[line_elements[0]] = line_elements[4]
#     return emotion_dict
#
#
# def load_visualization_info(visualization_info_path):  # 读取词语具象化信息
#     visual_info = dict()
#     with open(visualization_info_path, 'r', encoding='utf-8') as sf:
#         for line in sf.readlines():
#             split = line.splitlines()[0].strip().split(' ', 1)
#             if len(split) != 2:
#                 continue
#             visual_info[split[0]] = split[1]
#     return visual_info
#
#
# def load_polysemy_info(polysemy_info_path):  # 一词多义优先级
#     polysemy_info = dict()
#     with open(polysemy_info_path, 'r', encoding='utf-8') as rf:
#         for line in rf.readlines():
#             line = line.strip().split(' ')
#             polysemy_info[line[0]] = line[1]
#     return polysemy_info
#
#
# def load_poetry_info(poetry_info_path):  # 读取古诗词
#     poetry_info = dict()
#
#     with open(poetry_info_path, 'r', encoding='utf-8') as rf:
#         for line in rf.readlines():
#             direct_trans, free_trans = [], []
#             line = line.strip().split(',')
#             for word in line[1].strip().split(' '):
#                 direct_trans.append(word)
#             for word in line[3].strip().split(' '):
#                 free_trans.append(word)
#             poetry_info[line[0]] = [direct_trans, line[2].strip(), free_trans]
#     return poetry_info
#
#
# def load_computer_dict(computer_path):  # 读取计算机词汇
#     computer_dict = defaultdict(str)
#     with open(computer_path, 'r', encoding='utf-8') as sf:
#         for line in sf.readlines():
#             line_words = line.splitlines()[0].strip().split(' ')
#             tag = line_words[0]
#             computer_dict[tag] = tag
#     return computer_dict
#
#
# def load_art_dict(art_path):  # 读取美术词汇
#     art_dict = defaultdict(str)
#     with open(art_path, 'r', encoding='utf-8') as sf:
#         for line in sf.readlines():
#             line_words = line.splitlines()[0].strip().split(' ')
#             tag = line_words[0]
#             art_dict[tag] = tag
#     return art_dict
# #
#


if __name__ == '__main__':
    res = load_sign_words()
    print(res)
