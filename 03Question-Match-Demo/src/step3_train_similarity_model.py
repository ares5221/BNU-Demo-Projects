#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import numpy as np
from tensorflow import keras
from keras.utils import np_utils
import tensorflow as tf
import matplotlib.pyplot as plt
import csv


def train_model(train_data1, train_data2, train_label, test_data1, test_data2, test_label):
    epoch_num = 100
    batch_size_num = 32
    embedding_len = 768 #bert encoding vector length
    classes_num = 2

    # shuffle data
    indices = np.arange(train_data1.shape[0])
    np.random.shuffle(indices)
    train_data1 = train_data1[indices]
    train_data2 = train_data2[indices]
    train_label = train_label[indices]

    train_label = np_utils.to_categorical(train_label, classes_num)

    print(train_data1)
    print(train_data2)
    print(train_label)
    input1 = tf.keras.layers.Input(shape=(768,))
    input2 = tf.keras.layers.Input(shape=(768,))
    merge_vector = tf.keras.layers.concatenate([input1, input2], axis=-1)
    mlp_1 = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(merge_vector)
    mlp_2 = tf.keras.layers.Dense(32, activation=tf.nn.sigmoid)(mlp_1)
    mlp_out = tf.keras.layers.Dense(classes_num, activation=tf.nn.sigmoid)(mlp_2)
    model = tf.keras.Model([input1, input2], mlp_out)
    model.summary()

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    par_train_data = [train_data1, train_data2]
    par_train_label = train_label
    history = model.fit(par_train_data, par_train_label,
                        epochs=epoch_num,
                        batch_size=batch_size_num,
                        validation_split=0.2
                        )
    if True:
        draw_pic(history)
    # model save
    model_path = './../data/model/'
    model_name = 'bert_mlp_model.h5'
    save_path = os.path.join(model_path, model_name)
    model.save(save_path)

    # test model
    test_data = [test_data1,test_data2]
    test_label = np_utils.to_categorical(test_label, classes_num)
    results = model.evaluate(test_data, test_label)
    print('step5: 评估模型效果(损失-精度）：...', results)
    if False:
        check_result(model, test_data)
    print('模型训练结束。')


def check_result(model, test_data):
    print('step7: predict test data for count...')
    predictions = model.predict(test_data)
    predict = np.argmax(predictions, axis=1)
    print(predict)
    if False:
        with open('result_check.csv', 'w', newline='', encoding='utf-8') as csvwriter:
            spamwriter = csv.writer(csvwriter, delimiter=' ')
            for pre_val in predict:
                spamwriter.writerow([pre_val])


def draw_pic(history):
    print('step6: 开始绘图...')
    history_dict = history.history
    print(history.history)
    history_dict.keys()
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    plt.clf()  # clear figure
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print('read train and test data...')
    base_path = './../data/train_data'
    train_data1_path = os.path.join(base_path, 'train_data1.npy')
    train_data2_path = os.path.join(base_path, 'train_data1.npy')
    train_label_path = os.path.join(base_path, 'train_label.npy')

    train_data1 = np.load(train_data1_path, allow_pickle=True)
    train_data2 = np.load(train_data2_path, allow_pickle=True)
    train_label = np.load(train_label_path, allow_pickle=True)
    test_data1 = train_data1
    test_data2 = train_data2
    test_label = train_label
    # print(len(train_data1), train_data1[0])
    # print(len(train_data1[0]))
    train_model(train_data1, train_data2, train_label, test_data1, test_data2, test_label)
