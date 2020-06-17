# -*- coding: utf-8 -*-
'''
Author: Zhaoning Li
'''

import re
import pickle
from tqdm import tqdm


dictPart = pickle.load(open('your_terminology_path', 'rb'))[0]


def newPred(ls):
    new_ls = []
    for i in range(len(ls)):
        temp = ls[i]
        if temp in [4, 5, 6]:
            temp = 4
        new_ls.append(temp)
    return new_ls


def findIdx(ls):
    r1, r2, r3 = [], [], []
    element = set(ls)
    if 1 in element:
        for i in re.finditer('14+|1', ''.join([str(i) for i in ls])):
            r1.append([i for i in range(i.start(), i.end())])
    if 2 in element:
        for i in re.finditer('24+|2', ''.join([str(i) for i in ls])):
            r2.append([i for i in range(i.start(), i.end())])
    if 3 in element:
        for i in re.finditer('34+|3', ''.join([str(i) for i in ls])):
            r3.append([i for i in range(i.start(), i.end())])
    return r1, r2, r3


def nerFilter(sent, yp_idx):
    np_idx, i = [], 0
    if len(yp_idx[0]) == 1:
        np_idx.append(yp_idx[0][0])
    elif len(yp_idx[0]) > 1:
        for _ in range(len(yp_idx[0])):
            if i+1 < len(yp_idx[0]):
                if yp_idx[0][i+1][0] - yp_idx[0][i][-1] == 1 and ''.join(sent[yp_idx[0][i][0]:yp_idx[0][i+1][-1]+1]) in dictPart:
                    np_idx.append(yp_idx[0][i] + yp_idx[0][i+1])
                    i += 2
                else:
                    np_idx.append(yp_idx[0][i])
                    i += 1
            if i+1 == len(yp_idx[0]):
                if yp_idx[0][i][-1] not in sum(np_idx, []):
                    np_idx.append(yp_idx[0][i])
                break

    clp_idx, clq_idx, clu_idx = [], [], []
    for i in np_idx:
        if len(i) == 1:
            try:
                if sent[i[0]] not in ['洞', '骨', '各']:
                    clp_idx.append(i)
                    continue
            except:
                pass
        if len(i) == 2:
            clp_idx.append(i)
            continue
        if len(i) == 3:
            try:
                if ''.join(sent[i[-1]-1:i[-1]+1]) in ['右壁', '下壁', '后壁']:
                    clp_idx.append(i[:-2])
                    clp_idx.append(i[-2:])
                elif ''.join(sent[i[0]:i[-1]+1]) == '两肺肺':
                    clp_idx.append(i[0:2])
                    clp_idx.append([i[-1]])
                elif ''.join(sent[i[0]:i[-1]+1]) == '支气管':
                    if i[0] - 2 > 0:
                        if ''.join(sent[i[0]-2:i[0]]) == '远端':
                            clp_idx.append([i[0]-2]+[i[0]-1]+i)
                        else:
                            clp_idx.append(i)
                    else:
                        clp_idx.append(i)
                else:
                    clp_idx.append(i)
                continue
            except:
                pass
        if len(i) == 4:
            try:
                if ''.join(sent[i[-1]-1:i[-1]+1]) in ['右壁', '下壁', '后壁']:
                    clp_idx.append(i[:-2])
                    clp_idx.append(i[-2:])
                elif ''.join(sent[i[0]:i[-1]+1]) == '主动脉壁':
                    clp_idx.append(i[0:3])
                    clp_idx.append([i[-1]])
                else:
                    try:
                        if sent[i[-1]+1] == '处':
                            clp_idx.append(i+[i[-1]+1])
                        else:
                            clp_idx.append(i)
                    except:
                        pass
                continue
            except:
                pass
        if len(i) >= 5:
            try:
                if ''.join(sent[i[-1]-1:i[-1]+1]) in ['右壁', '下壁', '后壁']:
                    clp_idx.append(i[:-2])
                    clp_idx.append(i[-2:])
                elif ''.join(sent[i[0]:i[-1]+1]) == '主动脉型心':
                    clu_idx.append(i)
                else:
                    try:
                        if sent[i[-1]+1] == '处':
                            clp_idx.append(i+[i[-1]+1])
                        else:
                            clp_idx.append(i)
                    except:
                        pass
                continue
            except:
                pass

    for i in yp_idx[1]:
        if len(i) == 1:
            try:
                if sent[i[0]] == '稍' and sent[i[0]+1] == '著':
                    clu_idx.append(i+[i[0]+1])
                elif ''.join(sent[i[0]-2:i[0]]) in ['多发', '散在'] and sent[i[0]] == '小':
                    pass
                else:
                    clq_idx.append(i)
                continue
            except:
                pass
        elif len(i) == 2:
            try:
                if ''.join(sent[i[0]:i[-1]+1]) in ['多发', '散在'] and sent[i[-1]+1] == '小':
                    clq_idx.append(i+[i[0]+1])
                else:
                    clq_idx.append(i)
                continue
            except:
                pass
        else:
            clq_idx.append(i)
            continue

    for i in yp_idx[-1]:
        if len(i) == 1:
            try:
                if sent[i[-1]] == '突' and sent[i[-1]+1] == '起':
                    clu_idx.append(i+[i[-1]+1])
                elif sent[i[0]] not in ['密']:
                    clu_idx.append(i)
                    continue
            except:
                pass
        if len(i) == 2:
            try:
                if ''.join(sent[i[0]:i[-1]+1]) not in ['骨桥', '金属']:
                    if ''.join(sent[i[0]:i[-1]+1]) == '指状' and ''.join(sent[i[-1]+1:i[-1]+3]) == '改变':
                        clu_idx.append(i+[i[-1]+1]+[i[-1]+2])
                    elif sent[i[-1]] == '突' and sent[i[-1]+1] == '起':
                        clu_idx.append(i+[i[-1]+1])
                    else:
                        clu_idx.append(i)
                continue
            except:
                pass
        if len(i) == 8:
            try:
                if sent[i[-1]] == '突' and sent[i[-1]+1] == '起':
                    clu_idx.append(i+[i[-1]+1])
                elif ''.join(sent[i[0]:i[-1]+1]) == '形态不规则空洞影':
                    clu_idx.append(i[5:])
                else:
                    clu_idx.append(i)
                continue
            except:
                pass
        if len(i) not in [1, 2, 8]:
            try:
                if '金属' not in ''.join(sent[i[0]:i[-1]+1]):
                    if sent[i[-1]] == '突' and sent[i[-1]+1] == '起':
                        clu_idx.append(i+[i[-1]+1])
                    else:
                        clu_idx.append(i)
                continue
            except:
                pass

    if clu_idx == []:
        return ([], [], [])
    return (clp_idx, clq_idx, clu_idx)
                
    
def viterbi(nodes, trans):
    paths = nodes[0]
    for l in range(1, len(nodes)):
        paths_old, paths = paths, {}
        for n, ns in nodes[l].items():
            max_path, max_score = '', -1e10
            for p, ps in paths_old.items():
                score = ns + ps + trans[p[-1]+n]
                if score > max_score:
                    max_path, max_score = p+n, score
            paths[max_path] = max_score
    return max(paths, key=paths.get)
    

def splitText(texts):
    new_sents, clean_sents = [], []
    for i in range(len(texts)):
        text = ''.join(texts[i])
        sentences = re.split('(。)', text)
        new_sent = []
        for i in range(int(len(sentences)/2)):
            sent = sentences[2*i] + sentences[2*i+1]
            new_sent.append(sent)
        if len(sentences) // 2 != len(sentences) / 2 and sentences[-1] != '':
            new_sent.append(sentences[-1])
        if new_sent == []:
            new_sent = [text]
        new_sents.extend(new_sent)        
    for i, sent in enumerate(new_sents):
        temp_sent = []
        for idx, c in enumerate(sent):
            if c not in [' ', '\n', '\t']:
                temp_sent.append(c)
        if len(temp_sent) > 2:
            clean_sents.append(temp_sent)
    return clean_sents


def decode(extractor, probas):
    _ = extractor.get_weights()[-1][:7, :7]
    tag2id = {'O': 0, 'P': 1, 'Q': 2, 'U': 3, 'p': 4, 'q': 5, 'u': 6}
    trans = {}
    for i in 'OPQUpqu':
        for j in 'OPQUpqu':
            trans[i+j] = _[tag2id[i], tag2id[j]]
    result = []
    for i in tqdm(range(len(probas))):
        nodes = [dict(zip('OPQUpqu', i))
                    for i in probas[i][:, :7]]
        nodes[0] = {i: j for i, j in nodes[0].items() if i in 'OPQU'}
        nodes[-1] = {i: j for i, j in nodes[-1].items() if i in 'Opqu'}
        tags = viterbi(nodes, trans)
        yp = [tag2id[t] for t in tags]
        result.append(yp)
    return result


def generateResult(text, y_pred):
    results, count = [], 0
    for i in range(len(text)):
        result, length = [], 0
        sent = splitText([text[i]])
        sent = [''.join(s) for s in sent]
        for j in range(len(sent)):
            length += len(sent[j]) if j != 0 else 0 
            y_true_idx = nerFilter(
                sent[j], findIdx(newPred(y_pred[count])))
            result.extend([{'word': ''.join(sent[j][idx[0]:idx[-1]+1]), 'start': length+idx[0], 'end': length+idx[-1]+1, 'type': 'position'} for idx in y_true_idx[0] if ''.join(sent[j][idx[0]:idx[-1]+1]) != ''])
            result.extend([{'word': ''.join(sent[j][idx[0]:idx[-1]+1]), 'start': length+idx[0], 'end': length+idx[-1]+1, 'type': 'quantifier'} for idx in y_true_idx[1] if ''.join(sent[j][idx[0]:idx[-1]+1]) != ''])
            result.extend([{'word': ''.join(sent[j][idx[0]:idx[-1]+1]), 'start': length+idx[0], 'end': length+idx[-1]+1, 'type': 'unusual'} for idx in y_true_idx[-1] if ''.join(sent[j][idx[0]:idx[-1]+1]) != ''])
            count += 1
        results.append(result)
    return results