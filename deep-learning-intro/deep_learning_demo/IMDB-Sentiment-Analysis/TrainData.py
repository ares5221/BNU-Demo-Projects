from __future__ import print_function
import numpy as np
import pathlib
import tensorflow as tf
from six.moves import cPickle as pickle
from tensorboard.backend.event_processing.event_accumulator import namedtuple
from tensorflow.contrib.layers.python.layers import initializers
from tqdm import tqdm
from distutils.dir_util import copy_tree
import time

##################load data#####################

print("Loading data")

all_data = pickle.load(open('dataset.pickle', 'rb'))
train_data = all_data['train_dataset']
test_data = all_data['test_dataset']
valid_data = all_data['valid_dataset']

train_labels = all_data['train_labels']
test_labels = all_data['test_labels']
valid_labels = all_data['valid_labels']
n_words = all_data['num_of_words']

del all_data


# save best overall model in best_model directory and save its info
def save_best_overall_model_data(data):
    pathlib.Path('./best_model').mkdir(parents=True, exist_ok=True)
    pickle_file = './best_model/best_model_info.pickle'
    try:
        f = open(pickle_file, 'wb')
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        print("Done")
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise


# load best overall model info to check if we find a better one this run
try:
    best_accuracy_on_test_file = pickle.load(open('./best_model/best_model_info.pickle', 'rb'))
    best_accuracy_on_test = best_accuracy_on_test_file['best_test_accuracy']
    del best_accuracy_on_test_file
except:
    save_best_overall_model_data({'best_test_accuracy': 0})
    best_accuracy_on_test = 0


# Create the batches for the training, validation data, and testing

def get_batches(x, y, batch_size):
    n_batches = len(x) // batch_size
    x, y = x[:n_batches * batch_size], y[:n_batches * batch_size]
    for ii in range(0, len(x), batch_size):
        yield x[ii:ii + batch_size], y[ii:ii + batch_size]


def build_rnn(n_words, embed_size, lstm_sizes, starting_learning_rate, output_hidden_units,
              learning_rate_decay_rate_every_epoch=0.50, gradient_clipping_by=1.0):
    '''Build the Recurrent Neural Network'''

    tf.reset_default_graph()

    # Declare placeholders we'll feed into the graph
    with tf.name_scope('inputs'):
        inputs = tf.placeholder(tf.int32, [None, None], name='inputs')
        lstm_output_keep_prob = tf.placeholder(tf.float32, name='lstm_output_keep_prob')
        fully_connected_keep_prob = tf.placeholder(tf.float32, name='fully_connected_keep_prob')
        batch_size = tf.placeholder(tf.int32, shape=(), name='batch_size')
    with tf.name_scope('labels'):
        labels = tf.placeholder(tf.int32, [None, None], name='labels')

    # Create the embeddings
    with tf.name_scope("embeddings"):
        embedding = tf.get_variable("embeddings", shape=(n_words + 1, embed_size),
                                    initializer=initializers.xavier_initializer())

        embed = tf.nn.embedding_lookup(embedding, inputs)

    # Build the RNN layers
    with tf.name_scope("RNN_layers"):
        # build dynamic dropout lstm cells
        cells = [
            tf.nn.rnn_cell.DropoutWrapper(
                tf.nn.rnn_cell.LSTMCell(num_units=n, initializer=initializers.xavier_initializer()),
                output_keep_prob=lstm_output_keep_prob)
            for n
            in lstm_sizes]

        cell = tf.nn.rnn_cell.MultiRNNCell(cells)
    # Set the initial state
    with tf.name_scope("RNN_init_state"):
        initial_state = cell.zero_state(batch_size, tf.float32)

    # Run the data through the RNN layers
    with tf.name_scope("RNN_forward"):
        outputs, final_state = tf.nn.dynamic_rnn(
            cell,
            embed,
            initial_state=initial_state)

        # Create the fully connected layers
    with tf.name_scope("fully_connected"):
        # Initialize the weights and biases
        weights_initializer = initializers.xavier_initializer()
        biases = tf.zeros_initializer()

        dense = tf.contrib.layers.fully_connected(outputs[:, -1],
                                                  num_outputs=output_hidden_units[0],
                                                  activation_fn=tf.nn.relu,
                                                  weights_initializer=weights_initializer,
                                                  biases_initializer=biases)

        dense = tf.contrib.layers.dropout(dense, fully_connected_keep_prob)

        # add hidden layers depending on sent list
        for i in range(1, len(output_hidden_units)):
            dense = tf.contrib.layers.fully_connected(dense,
                                                      num_outputs=output_hidden_units[i],
                                                      activation_fn=tf.nn.relu,
                                                      weights_initializer=weights_initializer,
                                                      biases_initializer=biases)

            dense = tf.contrib.layers.dropout(dense, fully_connected_keep_prob)  # add dropout

    # Make the predictions
    with tf.name_scope('predictions'):
        predictions = tf.contrib.layers.fully_connected(dense,
                                                        num_outputs=1,
                                                        activation_fn=tf.sigmoid,
                                                        weights_initializer=weights_initializer,
                                                        biases_initializer=biases)

        predictions = tf.identity(predictions, name="predictions")

        tf.summary.histogram('predictions', predictions)

    # Calculate the cost
    with tf.name_scope('cost'):
        cost = tf.losses.mean_squared_error(labels, predictions)
        tf.summary.scalar('cost', cost)

    # Train the model
    with tf.name_scope('train'):
        global_step = tf.Variable(0, trainable=False, name='global_step')
        learning_rate = tf.train.exponential_decay(starting_learning_rate, global_step, len(train_data) // batch_size,
                                                   learning_rate_decay_rate_every_epoch,
                                                   staircase=True,
                                                   name='learning_rate')  # use learning rate decay every epoch
        # Optimizer.
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars),
                                          gradient_clipping_by)  # gradient clipping
        optimize = optimizer.apply_gradients(
            zip(grads, tvars),
            global_step=global_step, name='optimize')

    # Determine the accuracy
    with tf.name_scope("accuracy"):
        correct_pred = tf.equal(tf.cast(tf.round(predictions),
                                        tf.int32), labels)
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        tf.summary.scalar('accuracy', accuracy)

    # Merge all of the summaries
    merged = tf.summary.merge_all()

    # Export the nodes
    export_nodes = ['inputs', 'labels', 'fully_connected_keep_prob', 'lstm_output_keep_prob', 'batch_size',
                    'learning_rate', 'initial_state',
                    'final_state', 'accuracy', 'predictions', 'cost',
                    'optimizer', 'optimize', 'merged']
    Graph = namedtuple('Graph', export_nodes)
    local_dict = locals()
    graph = Graph(*[local_dict[each] for each in export_nodes])

    return graph


# train the RNN
def train(model, epochs, log_string):
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        # Used to determine when to stop the training early
        valid_loss_summary = []

        # Keep track of which batch iteration is being trained
        iteration = 0

        print("Training Model: {}".format(log_string))

        train_writer = tf.summary.FileWriter('./saved_model/model_{}/logs/train'.format(log_string), sess.graph)
        valid_writer = tf.summary.FileWriter('./saved_model/model_{}/logs/valid'.format(log_string))

        for e in range(epochs):

            # Record progress with each epoch
            train_loss = []
            train_acc = []
            val_acc = []
            val_loss = []
            learning_rates = []
            # training set
            with tqdm(total=len(train_data)) as pbar:
                for _, (x, y) in enumerate(get_batches(train_data, train_labels, batch_size), 1):
                    feed = {model.inputs: x,
                            model.batch_size: batch_size,
                            model.labels: y[:, None],
                            model.lstm_output_keep_prob: lstm_output_keep_prob,
                            model.fully_connected_keep_prob: fully_connected_keep_prob}
                    summary, loss, acc, state, lr, _ = sess.run([model.merged,
                                                                 model.cost,
                                                                 model.accuracy,
                                                                 model.final_state,
                                                                 model.learning_rate,
                                                                 model.optimize],
                                                                feed_dict=feed)

                    # Record the loss and accuracy of each training batch
                    train_loss.append(loss)
                    train_acc.append(acc)
                    learning_rates.append(lr)
                    # Record the progress of training
                    train_writer.add_summary(summary, iteration)

                    iteration += 1
                    pbar.update(batch_size)

            # Average the training loss and accuracy of each epoch
            avg_train_loss = np.mean(train_loss)
            avg_train_acc = np.mean(train_acc)

            # validation set
            with tqdm(total=len(valid_data)) as pbar:
                for x, y in get_batches(valid_data, valid_labels, batch_size):
                    feed = {model.inputs: x,
                            model.batch_size: batch_size,
                            model.labels: y[:, None],
                            model.lstm_output_keep_prob: 1.0,
                            model.fully_connected_keep_prob: 1.0}
                    summary, batch_loss, batch_acc, val_state = sess.run([model.merged,
                                                                          model.cost,
                                                                          model.accuracy,
                                                                          model.final_state],
                                                                         feed_dict=feed)

                    # Record the validation loss and accuracy of each epoch
                    val_loss.append(batch_loss)
                    val_acc.append(batch_acc)
                    pbar.update(batch_size)

            # Average the validation loss and accuracy of each epoch
            avg_valid_loss = np.mean(val_loss)
            avg_valid_acc = np.mean(val_acc)
            valid_loss_summary.append(avg_valid_loss)

            # Record the validation data's progress
            valid_writer.add_summary(summary, iteration)

            # Print the progress of each epoch
            print("Epoch: {}/{}".format(e, epochs),
                  "Starting Learning Rate: {:.10f}".format(max(learning_rates)),
                  "Ending Learning Rate: {:.10f}".format(min(learning_rates)),
                  "Train Loss: {:.3f}".format(avg_train_loss),
                  "Train Acc: {:.3f}".format(avg_train_acc),
                  "Valid Loss: {:.3f}".format(avg_valid_loss),
                  "Valid Acc: {:.3f}".format(avg_valid_acc))

            # Stop training if the validation loss does not decrease after 3 epochs
            if avg_valid_loss > min(valid_loss_summary):
                print("No Improvement.")
                stop_early += 1
                if stop_early == early_stopping_by:
                    break

                    # Reset stop_early if the validation loss finds a new low
            # Save a checkpoint of the model
            else:
                print("New Record!")
                stop_early = 0
                checkpoint = "./saved_model/model_{}/model.ckpt".format(
                    log_string)
                saver.save(sess, checkpoint)

        # test set
        test_acc = []
        test_loss = []
        with tqdm(total=len(test_data)) as pbar:
            for x, y in get_batches(test_data, test_labels, batch_size):
                feed = {model.inputs: x,
                        model.batch_size: batch_size,
                        model.labels: y[:, None],
                        model.lstm_output_keep_prob: 1.0,
                        model.fully_connected_keep_prob: 1.0}
                summary, batch_loss, batch_acc, test_state = sess.run([model.merged,
                                                                       model.cost,
                                                                       model.accuracy,
                                                                       model.final_state],
                                                                      feed_dict=feed)

                # Record the test loss and accuracy
                test_loss.append(batch_loss)
                test_acc.append(batch_acc)
                pbar.update(batch_size)

        # Average the test loss and test acc
        avg_test_loss = np.mean(test_loss)
        avg_test_acc = np.mean(test_acc)
        # Print test results
        print("Test Loss: {:.3f}".format(avg_test_loss),
              "Test Acc: {:.3f}".format(avg_test_acc))
        # check if found new overall best model
        if avg_test_acc > best_accuracy_on_test:
            print("Found a new best overall model !! ")

            saveData = {
                'best_test_accuracy': avg_test_acc,
                'folder_name': "model_{}".format(log_string),
                'embed_size': embed_size,
                'batch_size': batch_size,
                'lstm_sizes': lstm_sizes,
                'lstm_output_keep_prob': lstm_output_keep_prob,
                'fully_connected_keep_prob': fully_connected_keep_prob,
                'starting_learning_rate': starting_learning_rate,
                'output_hidden_units': output_hidden_units,
                'learning_rate_decay_rate_every_epoch': learning_rate_decay_rate_every_epoch,
                'gradient_cipping_by': gradient_clipping_by,
                'epochs': epochs,
                'early_stoping_by': early_stopping_by
            }
            # save it
            save_best_overall_model_data(saveData)
            copy_tree("./saved_model/model_{}".format(log_string), "./best_model/model_{}".format(log_string))


# The parameters of the model
embed_size = 300
batch_size = 100
lstm_sizes = [64]
lstm_output_keep_prob = 0.5
fully_connected_keep_prob = 0.5
starting_learning_rate = 0.001
epochs = 50
early_stopping_by = 5
output_hidden_units = [64]
learning_rate_decay_rate_every_epoch = 0.8
gradient_clipping_by = 1.0

log_string = 'lstm_sizes={},output_hidden_units={},time={}'.format(lstm_sizes,
                                                                   output_hidden_units,
                                                                   int(time.time()))
model = build_rnn(n_words=n_words,
                  embed_size=embed_size,
                  lstm_sizes=lstm_sizes,
                  starting_learning_rate=starting_learning_rate,
                  output_hidden_units=output_hidden_units,
                  learning_rate_decay_rate_every_epoch=learning_rate_decay_rate_every_epoch,
                  gradient_clipping_by=gradient_clipping_by)

train(model, epochs, log_string)
