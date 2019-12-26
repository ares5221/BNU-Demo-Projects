#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import numpy as np
from tensorflow import keras
from keras.utils import np_utils
import tensorflow as tf
import matplotlib.pyplot as plt
import csv


def train_model(train_data, train_label, test_data, test_label):
    epoch_num = 100
    batch_size_num = 32
    max_len = len(train_data[0])
    classes_num = 2
    # shuffle data
    indices = np.arange(train_data.shape[0])
    np.random.shuffle(indices)
    train_data = train_data[indices]
    train_label = train_label[indices]

    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            padding='post',
                                                            maxlen=max_len)
    train_label = np_utils.to_categorical(train_label, classes_num)

    model = keras.Sequential()
    model.add(keras.layers.Dense(128, activation=tf.nn.relu, input_shape=(2311,)))
    # model.add(keras.layers.Dense(64, activation=tf.nn.relu))
    model.add(keras.layers.Dense(32, activation=tf.nn.relu))
    model.add(keras.layers.Dense(classes_num, activation=tf.nn.softmax))
    model.summary()

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    train_val_split = int(len(train_data) * 0.8)
    partial_x_train = train_data[:train_val_split]
    partial_y_train = train_label[:train_val_split]

    history = model.fit(partial_x_train, partial_y_train,
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
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                           padding='post',
                                                           maxlen=max_len)
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
    acc = history.history['acc']
    val_acc = history.history['val_acc']
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
    train_data_path = os.path.join(base_path, 'train_data.npy')
    train_label_path = os.path.join(base_path, 'train_label.npy')

    train_data = np.load(train_data_path, allow_pickle=True)
    train_label = np.load(train_label_path, allow_pickle=True)
    test_data = train_data
    test_label = train_label
    print(len(train_data), train_data[0])
    print(len(train_data[0]))
    train_model(train_data, train_label, test_data, test_label)
