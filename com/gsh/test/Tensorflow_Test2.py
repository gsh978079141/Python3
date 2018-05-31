#import modules
import numpy as np
import matplotlib.pyplot as plt
#from sklearn.metrics import confusion_matrix
import tensorflow as tf
import time
from datetime import timedelta
import math
from tensorflow.examples.tutorials.mnist import input_data


def new_weights(shape):
    return tf.Variable(tf.truncated_normal(shape,stddev=0.05))
def new_biases(length):
    return tf.Variable(tf.constant(0.1,shape=length))
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
def max_pool_2x2(inputx):
    return tf.nn.max_pool(inputx,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#import data
data = input_data.read_data_sets("./data", one_hot=True)  # one_hot means [0 0 1 0 0 0 0 0 0 0] stands for 2

print("Size of:")
print("--Training-set:\t\t{}".format(len(data.train.labels)))
print("--Testing-set:\t\t{}".format(len(data.test.labels)))
print("--Validation-set:\t\t{}".format(len(data.validation.labels)))
data.test.cls = np.argmax(data.test.labels,axis=1)   # show the real test labels:  [7 2 1 ..., 4 5 6], 10000values

x = tf.placeholder("float",shape=[None,784],name='x')
x_image = tf.reshape(x,[-1,28,28,1])

y_true = tf.placeholder("float",shape=[None,10],name='y_true')
y_true_cls = tf.argmax(y_true,dimension=1)
# Conv 1
layer_conv1 = {"weights":new_weights([5,5,1,32]),
               "biases":new_biases([32])}
h_conv1 = tf.nn.relu(conv2d(x_image,layer_conv1["weights"])+layer_conv1["biases"])
h_pool1 = max_pool_2x2(h_conv1)
# Conv 2
layer_conv2 = {"weights":new_weights([5,5,32,64]),
               "biases":new_biases([64])}
h_conv2 = tf.nn.relu(conv2d(h_pool1,layer_conv2["weights"])+layer_conv2["biases"])
h_pool2 = max_pool_2x2(h_conv2)
# Full-connected layer 1
fc1_layer = {"weights":new_weights([7*7*64,1024]),
            "biases":new_biases([1024])}
h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,fc1_layer["weights"])+fc1_layer["biases"])
# Droupout Layer
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)
# Full-connected layer 2
fc2_layer = {"weights":new_weights([1024,10]),
             "biases":new_weights([10])}
# Predicted class
y_pred = tf.nn.softmax(tf.matmul(h_fc1_drop,fc2_layer["weights"])+fc2_layer["biases"])  # The output is like [0 0 1 0 0 0 0 0 0 0]
y_pred_cls = tf.argmax(y_pred,dimension=1)  # Show the real predict number like '2'
# cost function to be optimized
cross_entropy = -tf.reduce_mean(y_true*tf.log(y_pred))
optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cross_entropy)
# Performance Measures
correct_prediction = tf.equal(y_pred_cls,y_true_cls)
accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    train_batch_size = 50
    def optimize(num_iterations):
        total_iterations=0
        start_time = time.time()
        for i in range(total_iterations,total_iterations+num_iterations):
            x_batch,y_true_batch = data.train.next_batch(train_batch_size)
            feed_dict_train_op = {x:x_batch,y_true:y_true_batch,keep_prob:0.5}
            feed_dict_train = {x:x_batch,y_true:y_true_batch,keep_prob:1.0}
            sess.run(optimizer,feed_dict=feed_dict_train_op)
            # Print status every 100 iterations.
            if i%100==0:
                # Calculate the accuracy on the training-set.
                acc = sess.run(accuracy,feed_dict=feed_dict_train)
                # Message for printing.
                msg = "Optimization Iteration:{0:>6}, Training Accuracy: {1:>6.1%}"
                # Print it.
                print(msg.format(i+1,acc))
        # Update the total number of iterations performed
        total_iterations += num_iterations
        # Ending time
        end_time = time.time()
        # Difference between start and end_times.
        time_dif = end_time-start_time
        # Print the time-usage
        print("Time usage:"+str(timedelta(seconds=int(round(time_dif)))))
    test_batch_size = 256
    def print_test_accuracy():
        # Number of images in the test-set.
        num_test = len(data.test.images)
        cls_pred = np.zeros(shape=num_test,dtype=np.int)
        i = 0
        while i < num_test:
            # The ending index for the next batch is denoted j.
            j = min(i+test_batch_size,num_test)
            # Get the images from the test-set between index i and j
            images = data.test.images[i:j, :]
            # Get the associated labels
            labels = data.test.labels[i:j, :]
            # Create a feed-dict with these images and labels.
            feed_dict={x:images,y_true:labels,keep_prob:1.0}
            # Calculate the predicted class using Tensorflow.
            cls_pred[i:j] = sess.run(y_pred_cls,feed_dict=feed_dict)
            # Set the start-index for the next batch to the
            # end-index of the current batch
            i = j
        cls_true = data.test.cls
        correct = (cls_true==cls_pred)
        correct_sum = correct.sum()
        acc = float(correct_sum) / num_test
        # Print the accuracy
        msg = "Accuracy on Test-Set: {0:.1%} ({1}/{2})"
        print(msg.format(acc,correct_sum,num_test))
    # Performance after 10000 optimization iterations
    optimize(num_iterations=10000)
    print_test_accuracy()
    savew_hl1 = layer_conv1["weights"].eval()
    saveb_hl1 = layer_conv1["biases"].eval()
    savew_hl2 = layer_conv2["weights"].eval()
    saveb_hl2 = layer_conv2["biases"].eval()
    savew_fc1 = fc1_layer["weights"].eval()
    saveb_fc1 = fc1_layer["biases"].eval()
    savew_op = fc2_layer["weights"].eval()
    saveb_op = fc2_layer["biases"].eval()

    np.save("savew_hl1.npy", savew_hl1)
    np.save("saveb_hl1.npy", saveb_hl1)
    np.save("savew_hl2.npy", savew_hl2)
    np.save("saveb_hl2.npy", saveb_hl2)
    np.save("savew_hl3.npy", savew_fc1)
    np.save("saveb_hl3.npy", saveb_fc1)
    np.save("savew_op.npy", savew_op)
    np.save("saveb_op.npy", saveb_op)