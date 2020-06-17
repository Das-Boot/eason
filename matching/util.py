# -*- coding: utf-8 -*-
'''
Author: Zhaoning Li
'''

import re
import pickle


dictPart, falseKb, partTwo, partThree, reversedTriplets, exceptTriplets = pickle.load(open('your_terminology_path.pkl', 'rb'))


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


def buildTriplet(text, t, r, e1_list, e2_list):
    for e1 in e1_list:
        for e2 in e2_list:
            flag = 0
            triplet = (text[e1[0]:e1[-1]+1], r, text[e2[0]:e2[-1]+1])
            length = max(e1[0]-(e2[-1]+1), e2[0]-(e1[-1]+1))
            if e1[0] >= e2[-1] and triplet not in reversedTriplets:
                flag = 1
            if triplet[1] == 'P2P':
                if triplet[0] in partThree:
                    flag = 1
                if triplet[0] in partTwo and triplet[-1] in partTwo:
                    flag = 1
                if triplet[-1] not in partTwo+partThree and triplet not in exceptTriplets:
                    flag = 1
            if triplet[1] == 'Q2U':
                if triplet[0] == '弥漫' and '扩张' in triplet[2]:
                    flag = 1
            if triplet in falseKb:
                flag = 1
            if e1 != e2 and flag == 0:
                t.append(((triplet[0], (e1[0], e1[-1]+1), triplet[1],
                           triplet[2], (e2[0], e2[-1]+1)), length))
                

def filter(text, t):
    nt, scope = [], []
    P1 = sorted(list(set([(i[0][0], i[0][1]) for i in t if 'P' in i[0][2] and i[0][0] not in partTwo+partThree])), key=lambda x: x[-1][0])
    P2 = sorted(list(set([(i[0][0], i[0][1]) for i in t if 'P' in i[0][2] and i[0][0] in partTwo])), key=lambda x: x[-1][0])
    P3 = sorted(list(set([(i[0][0], i[0][1]) for i in t if 'P' in i[0][2] and i[0][0] in partThree])), key=lambda x: x[-1][0])
    Q = sorted(list(set([(i[0][0], i[0][1]) for i in t if 'Q' in i[0][2]])), key=lambda x: x[-1][0])
    U = sorted(list(set([(i[0][-2], i[0][-1]) for i in t if 'U' in i[0][2]])), key=lambda x: x[-1][0])
    for i in range(len(P1)):        
        if i < len(P1)-1:
            if P1[i+1][-1][0] not in scope:
                if '及' not in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]) and '、' not in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]):
                    scope.append(P1[i+1][-1][0])
                elif '及' in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]) and '（' in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]) and '）' in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]):
                    pass
                elif '、' in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]) and '（' in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]) and '）' in ''.join(text[P1[i][-1][-1]:P1[i+1][-1][0]]):
                    pass
                elif P1[i+1][-1][0] - P1[i][-1][-1] > 5:
                    scope.append(P1[i+1][-1][0])
                    
    if P1 == []:
        for i in range(len(P2)):        
            if i < len(P2)-1:
                if P2[i+1][-1][0] not in scope:
                    if '及' not in ''.join(text[P2[i][-1][-1]:P2[i+1][-1][0]]) and '、' not in ''.join(text[P2[i][-1][-1]:P2[i+1][-1][0]]):
                        scope.append(P2[i+1][-1][0])
                    elif P2[i+1][-1][0] - P2[i][-1][-1] > 5:
                        scope.append(P2[i+1][-1][0])
    
    if P1 == [] and P2 == []:
        for i in range(len(P3)):        
            if i < len(P3)-1:
                if P3[i+1][-1][0] not in scope:
                    if '及' not in ''.join(text[P3[i][-1][-1]:P3[i+1][-1][0]]) and '、' not in ''.join(text[P3[i][-1][-1]:P3[i+1][-1][0]]):
                        scope.append(P3[i+1][-1][0])
                    elif P3[i+1][-1][0] - P3[i][-1][-1] > 5:
                        scope.append(P3[i+1][-1][0])
    
    scope = [0] + scope + [10000]
    for idx, s in enumerate(scope):
        s1 = s 
        if idx < len(scope)-1:
            s2 = scope[idx+1]
        else:
            s2 = s
        if s1 != s2:
            p1 = [p for p in P1 if p[1][-1] < s2 and p[1][0] >= s1]
            p2 = [p for p in P2 if p[1][-1] < s2 and p[1][0] >= s1]
            p3 = [p for p in P3 if p[1][-1] < s2 and p[1][0] >= s1]
            pa = p1 + p2 + p3
            q = [q for q in Q if q[1][-1] < s2 and q[1][0] >= s1]
            u = [u for u in U if u[1][-1] < s2 and u[1][0] >= s1]
            for tt in t:
                if tt[0][1][-1] < s2 and tt[0][-1][-1] < s2 and tt[0][1][0] >= s1 and tt[0][-1][0] >= s1:
                    if tt[0][2] == 'P2P':
                        if p1 != [] and p2 != [] and p3 != []:
                            if tt[0][:2] in p1 and tt[0][-2:] in p2 and tt[0] not in nt:
                                nt.append(tt[0])
                            if tt[0][:2] in p2 and tt[0][-2:] in p3 and tt[0] not in nt:
                                nt.append(tt[0])
                        if p1 == [] and p2 != [] and p3 != []:
                            if tt[0][:2] in p2 and tt[0][-2:] in p3 and tt[0] not in nt:
                                nt.append(tt[0])
                        if p1 != [] and p2 == [] and p3 != []:
                            if tt[0][:2] in p1 and tt[0][-2:] in p3 and tt[0] not in nt:
                                nt.append(tt[0])
                        if p1 != [] and p2 != [] and p3 == []:
                            if tt[0][:2] in p1 and tt[0][-2:] in p2 and tt[0] not in nt:
                                nt.append(tt[0])
            for qq in q:
                temp_t, temp_length = [], 10000
                for tt in t:
                    if qq == tt[0][:2] and tt[-1] < temp_length and tt[0][2] == 'Q2U' and tt[0][-1][-1] < s2 and tt[0][-1][0] >= s1:
                        temp_length = tt[-1]
                        temp_t = tt[0]
                if temp_t not in nt and temp_t != []:
                    nt.append(temp_t)
            
            for uu in u:
                temp_t, temp_length = [], 10000
                for tt in t:
                    if uu == tt[0][-2:] and tt[-1] < temp_length and tt[0][2] == 'Q2U' and tt[0][1][-1] < s2 and tt[0][1][0] >= s1:
                        temp_length = tt[-1]
                        temp_t = tt[0]
                if temp_t not in nt and temp_t != []:
                    nt.append(temp_t)
            
            for p in pa:
                temp_t, temp_length = [], 10000
                for tt in t:
                    if p == tt[0][:2] and tt[-1] < temp_length and tt[0][2] == 'P2U' and tt[0][-1][-1] < s2 and tt[0][-1][0] >= s1:
                        temp_length = tt[-1]
                        temp_t = tt[0]
                if temp_t not in nt and temp_t != []:
                    nt.append(temp_t)
                    
    for u in U:
        temp_t, temp_length = [], 10000
        for tt in t:
            if u == tt[0][-2:] and tt[-1] < temp_length and tt[0][2] == 'P2U':
                temp_length = tt[-1]
                temp_t = tt[0]
        if temp_t not in nt and temp_t != []:
            nt.append(temp_t)
    
    for _ in range(100):
        l1 = len(nt)
        for ntt in nt:
            if ntt[2] == 'P2U':
                temp_t = [tt[0] for tt in t if tt[0][2]
                          == 'P2U' and tt[0][-2:] == ntt[-2:]]
                for tp_t in temp_t:
                    if tp_t not in nt:
                        if ntt[1][0]-tp_t[1][-1] < 5:
                            if '及' in text[tp_t[1][-1]:ntt[1][0]] or '、' in text[tp_t[1][-1]:ntt[1][0]]:
                                nt.append(tp_t)
        l2 = len(nt)
        if l1 == l2:
            break
        
    for _ in range(100):
        l1 = len(nt)
        for ntt in nt:
            if ntt[2] == 'P2P':
                temp_t = [tt[0] for tt in t if tt[0][2]
                          == 'P2P' and tt[0][-2:] == ntt[-2:]]
                for tp_t in temp_t:
                    if tp_t not in nt:
                        if ntt[1][0]-tp_t[1][-1] < 6:
                            if '及' in text[tp_t[1][-1]:ntt[1][0]] or '、' in text[tp_t[1][-1]:ntt[1][0]]: 
                                nt.append(tp_t)
                        
        l2 = len(nt)
        if l1 == l2:
            break

    ct = []
    for att in nt:
        if att[2] == 'P2P':
            for btt in nt:
                if att[-2:] == btt[:2] and btt[2] == 'P2U' and att not in ct:
                    ct.append(att)
                if att[-2:] == btt[:2] and btt[2] == 'P2P':
                    for ctt in nt:
                        if btt[-2:] == ctt[:2] and ctt[2] == 'P2U' and att not in ct:
                            ct.append(att)
        if att[2] == 'P2U':
            if att not in ct:
                ct.append(att)
        if att[2] == 'Q2U':
            if att not in ct:
                ct.append(att)
                
    ct_d = {t: 1 for t in ct}
    for att in ct:
        if att[2] == 'P2U':
            for btt in ct:
                if att[:2] == btt[-2:] and btt[2] == 'P2P':
                    if (btt[0], btt[1], 'P2U', att[-2], att[-1]) in ct:
                        ct_d[(btt[0], btt[1], 'P2U', att[-2], att[-1])] = 0
                    for ctt in ct:
                        if btt[:2] == ctt[-2:] and ctt[2] == 'P2P' and (ctt[0], ctt[1], 'P2U', att[-2], att[-1]) in ct:
                            ct_d[(ctt[0], ctt[1], 'P2U', att[-2], att[-1])] = 0
                    
    ct = [t for t in ct if ct_d[t] == 1]
                    
    return [t for t in ct if t[0] != '' and t[-2] != '']


def matchEntity(text, idx):
    triplet = []
    if idx[0] != [] and idx[-1] != []:
        buildTriplet(text, triplet, 'P2U', idx[0], idx[-1])
    if idx[0] != []:
        buildTriplet(text, triplet, 'P2P', idx[0], idx[0])
    if idx[1] != [] and idx[-1] != []:
        buildTriplet(text, triplet, 'Q2U', idx[1], idx[-1])
    return filter(text, triplet)
    

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


def combination(triplet):
    result = []
    for t in triplet:
        if t[2] == 'P2P':
            for tt in triplet:
                if tt != t and tt[2] == 'P2P' and tt[:2] == t[-2:]:
                    for ttt in triplet:
                        if ttt[2] == 'P2U' and ttt[:2] == tt[-2:]:
                            temp = [t[0]+t[-2]+tt[-2], ttt[-2], t[1], t[-1], tt[-1], ttt[-1]]
                            if temp not in result:
                                result.append(temp)
                if tt[2] == 'P2U' and tt[:2] == t[-2:]:
                    temp = [t[0]+t[-2], tt[-2], t[1], t[-1], tt[-1]]
                    if temp not in result:
                        result.append(temp)
        if t[2] == 'P2U':
            temp = [t[0], t[-2], t[1], t[-1]]
            if temp not in result:
                result.append(temp)

    clean_result = []
    for r in result:
        if len(r) == 6:
            clean_result.append(r)
        if len(r) == 5:
            if r[2:] not in [[_[-3], _[-2], _[-1]] for _ in result if len(_) == 6]:
                clean_result.append(r)
        if len(r) == 4:
            if r[2:] not in [[_[-2], _[-1]] for _ in result if len(_) in [5, 6]]:
                clean_result.append(r)
    final_result = []
    for r in clean_result:
        temp = ''
        for t in triplet:
            if t[2] == 'Q2U' and t[-2] == r[1] and t[-1] == r[-1]:
                temp += t[0]
        final_result.append([r[0]]+[temp]+r[1:])
    for t in triplet:
        if t[2] == 'Q2U' and t[-1] not in [r[-1] for r in final_result]:
            final_result.append(['', t[0], t[-2]])
    return [(i[0], i[1], i[2]) for i in final_result]


def generateResult(text, y_pred):
    triplets, count = [], 0
    for i in range(len(text)):
        triplet = []
        sent = splitText([text[i]])
        sent = [''.join(s) for s in sent]
        for j in range(len(sent)):
            y_true_idx = nerFilter(
                sent[j], findIdx(newPred(y_pred[count])))
            temp = matchEntity(sent[j], y_true_idx)
            temp_ent = [''.join(sent[j][idx[0]:idx[-1]+1]) for idx in y_true_idx[-1]]
            temp_tri = [_[-1] for _ in combination(sorted(temp, key=lambda x: (x[1][0], x[-1][0])))]
            t_ = []
            for e in temp_ent:
                if e not in temp_tri+t_ and e not in [[], '']:
                    t_.append(('', '', e))
            if t_ != []:
                triplet.extend(t_+combination(sorted(temp, key=lambda x: (x[1][0], x[-1][0]))))
            else:
                triplet.extend(combination(sorted(temp, key=lambda x: (x[1][0], x[-1][0]))))
            count += 1
        triplets.append(triplet)
    return triplets


def finalResult(r, predText):
    result = []
    for i in range(len(r)):
        text = predText[i]
        d = r[i]
        d = [dd for dd in d if dd[-1] not in ['“', '"', '”', '、', '/', '-', '——', '一', '－', '/或', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
        d = [dd if dd[-1][0] not in ['/', '-', '——', '－'] else [dd[0], dd[1], dd[-1][1:]] for dd in d if dd[-1]]
        d = [dd for dd in d if dd[-1] != '']
        temp_result = []
        for j in range(len(d)):
            temp_result.append((d[j][0], d[j][1], d[j][2]))
        result.append(temp_result)
    return result