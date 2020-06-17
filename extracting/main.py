# -*- coding: utf-8 -*-
'''
Author: Zhaoning Li
'''

from model import *
from util import *
import argparse

         
def initialize(args):
    extractor = ChineseClinicalExtracter(args).slm()
    extractor.load_weights(args.modelPath)
    return extractor


def predict(extractor, predText, args):
    index2tag = {
    0: 'O',
    1: 'B-position',
    2: 'B-quantifier',
    3: 'B-unusual',
    4: 'I-position',
    5: 'I-quantifier',
    6: 'I-unusual'   
    }
    predSent = splitText(predText)
    predSent = [list(''.join(s)) for s in predSent]
    maxlen = max([len(i) for i in predSent]) + 2
    predict_generator = DataGenerator(args,
                                      [i for i in range(len(predSent))],
                                      x=predSent,
                                      maxlen=maxlen)    
    probas = extractor.predict_generator(
        predict_generator, verbose=1)[:len(predSent)]
    
    tagResult = decode(extractor, probas)
    return generateResult(predText, tagResult), [[index2tag[i] for i in t] for t in tagResult]
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ep', '--erniePath', type=str, default="your_ernie_path")
    parser.add_argument('-mp', '--modelPath', type=str, default="your_weights_path")
    parser.add_argument('-cuda', '--cuda_devices', type=int, default=0)
    parser.add_argument('-cpu', '--cpu_core', type=int, default=1)
    parser.add_argument('-bs', '--batch_size', type=int, default=16, help="")
    args = parser.parse_args()    
    predText = ['胸廓对称。两肺纹理增著，肺实质未见明显异常。两肺门不大，纵隔未见增宽。心影大小、形态、位置未见异常。主动脉迂曲增宽，弓部见钙化影。气管及两侧主支气管通畅。两膈面光滑，两侧肋膈角锐利。两侧肋骨未见异常。胸11、12椎体成形术后改变，内见高密度骨水泥充填。', '对比2017-12-26胸片：右上肺见一类圆形肿块影，边界欠清，边缘不光整，似可见短毛刺，周围胸膜牵拉凹陷；余肺可见弥漫多发斑点、结节影，部分边缘模糊，部分边缘尚清。右胸膜增厚。两肺门稍增著，纵隔未见明显增宽。心影不大，主动脉增宽迂曲，弓部可见钙化影。大气道通畅。右膈上抬，两膈面尚清，两侧肋膈角变钝，右侧为著。——所见大致同前']
    extractor = initialize(args)
    print(predict(extractor, predText, args))