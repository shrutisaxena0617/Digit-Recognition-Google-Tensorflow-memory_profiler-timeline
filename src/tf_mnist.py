# TF Example using MNIST Data
import resource
from memory_profiler import profile
from time import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.client import timeline

t00 = time()

mnist = input_data.read_data_sets("/tmp/data", one_hot = True)
n_nodes_hl1 = 400
n_nodes_hl2 = 400
n_nodes_hl3 = 500
n_classes = 10
batch_size = 100
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

@profile
def neural_network_model(data):
  hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784, n_nodes_hl1])),
                    'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
  hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                    'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
  hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                    'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
  output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}

  # Model: (input_data * weights) + biases

  l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
  l1 = tf.nn.relu(l1)

  l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
  l2 = tf.nn.relu(l2)

  l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
  l3 = tf.nn.relu(l3)

  output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

  return output

@profile
def train_neural_network(x):
  prediction = neural_network_model(x)
  cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = y))
  #learning_rate = 0.001 (taking the default value. Changing this does not boost the accuracy much)
  optimizer = tf.train.AdamOptimizer().minimize(cost)
  hm_epochs = 20

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for epoch in range(hm_epochs):
      epoch_loss = 0
      for _ in range(int(mnist.train.num_examples/batch_size)):
        epoch_x, epoch_y = mnist.train.next_batch(batch_size)
        _, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y: epoch_y})
        epoch_loss += c
      print('Epoch', epoch, 'completed out of', hm_epochs, 'loss: ', epoch_loss)
    correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y,1))

    accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

    print('Accuracy', accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

m1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
train_neural_network(x)
m2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - m1

t22 = time()

print ("start time: " + str(t00))
print ("end time: " + str(t22))
print ("memory usage: " + str(m2))
