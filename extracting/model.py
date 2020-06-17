# -*- coding: utf-8 -*-
'''
Author: Zhaoning Li
'''

from keras_bert import load_trained_model_from_checkpoint, Tokenizer
import codecs
import keras
import numpy as np
import os
import random as rn
import tensorflow as tf
from keras import backend as K
from keras.layers import *
from keras.optimizers import *
from keras.models import Model


def seqPadding(X, padding=0, maxlen=None):
    if maxlen is None:
        L = [len(x) for x in X]
        ML = max(L)
    else:
        ML = maxlen
    return np.array([
        np.concatenate([x[:ML], [padding] * (ML - len(x))]) if len(x[:ML]) < ML else x for x in X
    ])


class NewTokenizer(Tokenizer):
    def _tokenize(self, text):
        R = []
        for c in text:
            if c in self._token_dict:
                R.append(c)
            elif self._is_space(c):
                R.append('[unused1]')
            else:
                R.append('[UNK]')
        return R


class DataGenerator(keras.utils.Sequence):
    def __init__(self, args, list_IDs, x, maxlen=None):
        self.args = args
        self.list_IDs = list_IDs
        self.x = x
        self.maxlen = maxlen

    def __len__(self):
        return int(np.ceil(len(self.list_IDs) / self.args.batch_size))

    def __getitem__(self, index):
        list_IDs_temp = self.list_IDs[index * self.args.batch_size:(index + 1) *
                                      self.args.batch_size]
        return self.__data_generation(list_IDs_temp)

    def __data_generation(self, list_IDs_temp):
        x, y = [], []
        token_dict = {}
        with codecs.open(self.args.erniePath+'/vocab.txt', 'r', 'utf8') as reader:
            for line in reader:
                token = line.strip()
                token_dict[token] = len(token_dict)
        tokenizer = NewTokenizer(token_dict)
        x1, x2 = [], []
        for i, ID in enumerate(list_IDs_temp):
            _x1, _x2 = tokenizer.encode(self.x[ID])
            x1.append(_x1)
            x2.append(_x2)
        x1 = seqPadding(x1, maxlen=self.maxlen)
        x2 = seqPadding(x2, maxlen=self.maxlen)
        return [x1, x2], None


class CRF(Layer):
    def __init__(self, init, ignore_last_label=False, **kwargs):
        self.init = initializers.get(init)
        self.ignore_last_label = 1 if ignore_last_label else 0
        self.supports_masking = True
        super(CRF, self).__init__(**kwargs)

    def build(self, input_shape):
        self.num_labels = input_shape[-1] - self.ignore_last_label
        self.trans = self.add_weight(name='crf_trans',
                                     shape=(self.num_labels, self.num_labels),
                                     initializer=self.init,
                                     trainable=True)

    def log_norm_step(self, inputs, states):
        states = K.expand_dims(states[0], 2)
        trans = K.expand_dims(self.trans, 0)
        output = K.logsumexp(states+trans, 1)
        return output+inputs, [output+inputs]

    def path_score(self, inputs, labels):
        point_score = K.sum(K.sum(inputs*labels, 2), 1, keepdims=True)
        labels1 = K.expand_dims(labels[:, :-1], 3)
        labels2 = K.expand_dims(labels[:, 1:], 2)
        labels = labels1 * labels2
        trans = K.expand_dims(K.expand_dims(self.trans, 0), 0)
        trans_score = K.sum(K.sum(trans*labels, [2, 3]), 1, keepdims=True)
        return point_score+trans_score

    def compute_mask(self, input, mask=None):
        if mask is not None:
            return K.any(mask, axis=1)
        return mask

    def call(self, inputs, mask=None):
        return inputs

    def loss(self, y_true, y_pred):
        mask = 1-y_true[:, 1:, -1] if self.ignore_last_label else None
        y_true, y_pred = y_true[:, :,
                                :self.num_labels], y_pred[:, :, :self.num_labels]
        init_states = [y_pred[:, 0]]
        log_norm, _, _ = K.rnn(
            self.log_norm_step, y_pred[:, 1:], init_states, mask=mask)
        log_norm = K.logsumexp(log_norm, 1, keepdims=True)
        path_score = self.path_score(y_pred, y_true)
        return log_norm - path_score

    def accuracy(self, y_true, y_pred):
        mask = 1-y_true[:, :, -1] if self.ignore_last_label else None
        y_true, y_pred = y_true[:, :,
                                :self.num_labels], y_pred[:, :, :self.num_labels]
        isequal = K.equal(K.argmax(y_true, 2), K.argmax(y_pred, 2))
        isequal = K.cast(isequal, 'float32')
        if mask == None:
            return K.mean(isequal)
        else:
            return K.sum(isequal*mask) / K.sum(mask)
        

class ChineseClinicalExtracter:
    def __init__(self, args):
        self.args = args
        self.reproducibility()
        self.kernel_initializer = keras.initializers.glorot_uniform(
            seed=666)

    def reproducibility(self):
        os.environ['PYTHONHASHSEED'] = str(666)
        os.environ['CUDA_VISIBLE_DEVICES'] = str(self.args.cuda_devices)
        np.random.seed(666)
        rn.seed(666)
        session_conf = tf.ConfigProto(
            device_count={'CPU': 1},
            intra_op_parallelism_threads=1,
            inter_op_parallelism_threads=1,
            gpu_options=tf.GPUOptions(allow_growth=True),
            allow_soft_placement=True)
        tf.set_random_seed(666)
        sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
        K.set_session(sess)

    def slm(self):
        bert_model = load_trained_model_from_checkpoint(self.args.erniePath+'/bert_config.json',
                                                        self.args.erniePath+'/bert_model.ckpt',
                                                        training=False,
                                                        trainable=True,
                                                        output_layer_num=1)
        x1_indices = Input(shape=(None,), name='INPUT_INDICES')
        x2_segments = Input(shape=(None,), name='INPUT_SEGMENTS')
        x = bert_model([x1_indices, x2_segments])
        x = Lambda(lambda x: x[:, 1:], name='REMV_CLS')(x)   
        dense = TimeDistributed(Dense(8,
                                      activation=None,
                                      kernel_initializer=self.kernel_initializer),
                                name='DENSE')(x)
        crf = CRF(init=self.kernel_initializer,
                  ignore_last_label=True, name='CRF')
        model = Model([x1_indices, x2_segments], [crf(dense)])
        model.compile(loss=crf.loss, optimizer=Adam())
        return model