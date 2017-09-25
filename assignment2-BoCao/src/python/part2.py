
# coding: utf-8

# In[3]:


'''
Author: Bryan Bo Cao
Email: boca7588@colorado.edu or bo.cao-1@colorado.edu
Github Repo: https://github.com/BryanBo-Cao/neuralnets-deeplearning

Note that input layer is noted as layer0, hidden layer is noted as layer1, and output layer is noted is layer2
'''
import numpy as np
import random
import copy
import matplotlib.pyplot as plt

train_data = np.genfromtxt('../data/assign2_train_data.txt', delimiter=',')
#print "train_data:", train_data

t = train_data[:,2]
hu = train_data[:,3]
lt = train_data[:,4]
co2 = train_data[:,5]
hu_r = train_data[:,6]

o = train_data[:,7]

#data
data = np.column_stack((t, hu, lt, co2, hu_r))
print "data:", data

print "np.shape(train_data): ", np.shape(train_data)
#print "np.shape(t): ", np.shape(t)

print "t: ", t
print "hu: ", hu
print "lt: ", lt
print "co2: ", co2
print "hu_r: ", hu_r
print "o: ", o


# In[4]:


def normalize(data):
    #normalize train data
    #normalize t
    t = data[:, 0]
    t_min = np.min(t)
    t_max = np.max(t)
    d_t = t_max - t_min
    #normalized t: n_t
    n_t = []
    for each in t:
        n_t.append((each - t_min) / d_t)

    #normalize hu
    hu = data[:, 1]
    hu_min = np.min(hu)
    hu_max = np.max(hu)
    d_hu = hu_max - hu_min
    #normalized h: n_hu
    n_hu = []
    for each in hu:
        n_hu.append((each - hu_min) / d_hu)

    #normalize lt
    lt = data[:, 2]
    lt_min = np.min(lt)
    lt_max = np.max(lt)
    d_lt = lt_max - lt_min
    #normalized lt: n_lt
    n_lt = []
    for each in lt:
        n_lt.append((each - lt_min) / d_lt)

    #normalize co2
    co2 = data[:, 3]
    co2_min = np.min(co2)
    co2_max = np.max(co2)
    d_co2 = co2_max - co2_min
    #normalized co2: n_co2
    n_co2 = []
    for each in co2:
        n_co2.append((each - co2_min) / d_co2)

    #normalize hu_r
    hu_r = data[:, 4]
    hu_r_min = np.min(hu_r)
    hu_r_max = np.max(hu_r)
    d_hu_r = hu_r_max - hu_r_min
    #normalized hu_r: n_hu_r
    n_hu_r = []
    for each in hu_r:
        n_hu_r.append((each - hu_r_min) / d_hu_r)

    #normalized data: n_data
    n_data = np.column_stack((n_t, n_hu, n_lt, n_co2, n_hu_r))

    return n_data


# In[5]:


n_data = normalize(data)
print "n_data:", n_data


# In[6]:


def initialize_weights1():
    w_t = random.random()
    w_hu = random.random()
    w_lt = random.random()
    w_co2 = random.random()
    w_hu_r = random.random()
    b = random.random()

    #weights
    ws1 = [w_t, w_hu, w_lt, w_co2, w_hu_r, b]
    return ws1

init_ws1 = initialize_weights1()
ws1 = copy.deepcopy(init_ws1)
print "ws1: ", ws1


# In[7]:


# initialize random weights from layer with i neurons to layer with j neurons -- fully connected layer including bias
# note that each row is the weights list from former layer to jth neuron in the latter layer
def initialize_weights(i, j):
    ws = np.random.rand(j, i + 1)
    return ws


# In[8]:


# test inner
a = [1, 2, 3]
b = [2, 0, 5]
c = 4
#np.inner(a, b)
np.inner(a, c)


# In[9]:


def sigmoid(x):
    # print "sigmoid(x): ", 1 / (1 + np.exp(-x))
    return 1 / (1 + np.exp(-x))

# Reference: https://www.youtube.com/watch?v=GlcnxUlrtek
def sigmoidPrime(x):
    #Derivative of Sigmoid Function
    return np.exp(-x) / ((1 + np.exp(-x) ** 2))

def activation(x): # use sigmoid as activation function
    a = sigmoid(x)
    if a >= 0.5:
        return 1
    else:
        return 0

def perceptron(sum_of_inputs):
    return activation(sum_of_inputs)

# Reference: http://cs229.stanford.edu/notes/cs229-notes1.pdf
# squared error
def error_function(o, y):
    return (o - y) ** 2 / 2


# In[16]:


def train(n_data, o, lr, H, bs):
    print "Training starts: len of data:", len(n_data)

    accuracies = []
    epoch = 0
    n_t = n_data[:, 0]
    n_hu = n_data[:, 1]
    n_lt = n_data[:, 2]
    n_co2 = n_data[:, 3]
    n_hu_r = n_data[:, 4]
    n_b = np.ones(len(n_t))

    train_n_data = np.column_stack((n_t, n_hu, n_lt, n_co2, n_hu_r, n_b))
    print "n_t:", n_t
    print "n_hu:", n_hu
    print "n_lt:", n_lt
    print "n_b:", n_b
    print "train_n_data:", train_n_data

    #ws0 are the weights from input layer to hidden layer
    init_ws0 = initialize_weights(5, H)
    ws0 = copy.deepcopy(init_ws0)
    print "ws0 before training:", ws0

    #ws1 are the weights from hidden layer to output layer
    init_ws1 = initialize_weights(H, 1)
    init_ws1 = init_ws1[0]
    ws1 = copy.deepcopy(init_ws1)
    print "ws1 before training:", ws1

    epoch = 1

    delta2 = 0 # delta from the output layer
    delta1 = [] # deltas from hidden layer nodes
    while epoch <= 100:

        i_data = 0 # index in the traning data list
        i_bs = 0 # index of batch size
        err2 = 0 # output layer error
        # one epoch
        while i_data < len(n_t):

            # each hidden neuron
            hidden_os = [] # hidden layer outputs
            for i in range(H):
                #print "i_data:",i_data
                hidden_o_i = sigmoid(np.inner(ws0[i], train_n_data[i_data])) # one output of one hidden layer neuron
                hidden_os.append(hidden_o_i)

            hidden_os.append(1) # append bias
            #print "hidden_os:", hidden_os

            sum_to_output_layer = np.inner(hidden_os, ws1) # output layer output
            net_o = sigmoid(sum_to_output_layer)
            # print "net_o:", net_o

            err2 += error_function(net_o, o[i_data]) # output layer error
            # print "err2: ", err2

            # only update weights after bs batch_size
            # print "o:",o
            if i_bs >= bs:
                ### update ws1: weights from hidden layer to output layer
                # Derivative of err2 with respect to ws1
                # Reference: https://www.youtube.com/watch?v=zpykfC4VnpM, https://page.mi.fu-berlin.de/rojas/neural/chapter/K7.pdf
                # d_err2_ws1 = -(net_o - o[i_data]) * sigmoidPrime(net_o) * hidden_os
                delta2 = net_o * (1 - net_o) * (net_o - o[i_data])# output layers delta
                #ws1 += ws1 + lr * err2 * hidden_os
                # print "delta2:", delta2

                delta_ws1 = []
                for i_hidden_node in range(H):
                    # print "hidden_os[i_hidden_node]:", hidden_os[i_hidden_node]
                    delta1.append(hidden_os[i_hidden_node] *
                                  (1 - hidden_os[i_hidden_node]) *
                                  delta2 *
                                  ws1[i_hidden_node])
                    #print "delta1: ", delta1

                    delta_ws1.append(-lr * delta2 * hidden_os[i_hidden_node])

                # append bias delta
                delta_b1 = lr * delta2
                delta_ws1.append(delta_b1)
                # print "delta_ws1: ", delta_ws1

                # print "ws1 before updated: ", ws1
                # print "delta_ws1: ", delta_ws1
                # update ws1 - weights from hidden layer to output layer
                for ii in range(len(ws1)):
                    # print "ws1[ii]: ", ws1[ii]
                    # print "delta_ws1[ii]:" , delta_ws1[ii]
                    ws1[ii] += delta_ws1[ii]
                    #ws1[ii] += 100
                # print "ws1 after  updated: ", ws1
                # print "   "
                ### end of updating ws1

                ### update ws0: weights from input layer to hidden layer
                delta1 = []
                ins = train_n_data[i_data] # one input layer
                # print "ins: ", ins
                for ii in range(len(ins)):
                    sum_of_delta2_ws0 = 0
                    ws0_input_node_i_to_all_hidden_nodes = ws0[:, ii]
                    for jj in range(len(ws0_input_node_i_to_all_hidden_nodes)):
                        sum_of_delta2_ws0 += delta2 * ws0_input_node_i_to_all_hidden_nodes[jj]
                    deltaii = ins[ii] * (1 - ins[ii]) * sum_of_delta2_ws0
                    # print "deltajj:", deltajj
                    delta1.append(deltaii)

                # print "delta1: ", delta1
                # print "len(ins):" , len(ins)
                # print "len(delta1):", len(delta1)

                ## update ws0 specifically
                # print "ws0 before updated: ", ws0
                for ii in range(len(ws0)): # each row is the list of weights from all inputs layer to one hidden layer
                    for jj in range(len(ws0[0])):
                        delta_w = -lr * delta1[jj] * ins[jj]
                        ws0[ii][jj] += delta_w
                # print "ws0 after  updated: ", ws0
                # print "     "
                ## end of updating ws0 specifically
                ### end of updating ws0

                delta2 = 0
                err2 = 0
                i_bs = -1

            hidden_os = []
            i_data += 1
            i_bs += 1


        #test every epoch
        accuracy = get_one_feedforward_accuracy(train_n_data, H, ws0, ws1, o)
        accuracies.append(accuracy)
        #print "ws0: ", ws0
        #print "ws1: ", ws1
        #if epoch % 100 == 0:
        print "   "
        print "ws0: ", ws0
        print "ws1: ", ws1
        print "epoch:", epoch, " accuracy:",accuracy

        epoch += 1

    print "Training ends."
    print "Initial input to hidden layer weights:", init_ws0
    print "Trained input to hidden layer weights:", ws0
    print "Initial hidden to output layer weights:", init_ws1
    print "Trained hidden to output layer weights:", ws1
    test_data = np.genfromtxt('../data/assign2_test_data.txt', delimiter=',')
    # print "test_data:", test_data
    test(test_data, H, ws0, ws1)
    plot_accuracy(accuracies, lr, bs, stage="train")

def test(test_data, H, ws0, ws1):
    print "Testing starts: len of data:", len(test_data)
    #normalize test data
    #normalize t
    n_test_data = normalize(test_data)
    n_t = n_test_data[:, 0]
    n_hu = n_test_data[:, 1]
    n_lt = n_test_data[:, 2]
    n_co2 = n_test_data[:, 3]
    n_hu_r = n_test_data[:, 4]
    o_test = test_data[:, 7]
    accuracy = get_one_feedforward_accuracy(n_test_data, H, ws0, ws1, o_test)
    print "Test data accuracy:",accuracy

def get_one_feedforward_accuracy(n_data, H, ws0, ws1, o_t):

    # print "ws0: ", ws0
    # print "ws1: ", ws1
    # print "n_data: ", n_data
    #calculate accuracy

    os = [] #outputs of output layer

    for each in zip(n_data):
        for ins in each: # each sample
            # print "ins: ", ins
            hidden_os = [] # hidden layer outputs
            for i_hidden in range(H):
                sum_input = np.inner(ins, ws0[i_hidden])
                output = sigmoid(sum_input)
                hidden_os.append(output)
            hidden_os.append(1)
            # print "hidden_os: ", hidden_os
            sum_input_to_output_layer = np.inner(hidden_os, ws1)
            print "sum_input_to_output_layer: ", sum_input_to_output_layer
            output = perceptron(sum_input_to_output_layer) # predict output of the whole neural network
            # print "output:", output
            os.append(output)
            print "    "

    # print "os: ", os
    # print "o: ", o
    #count correct output number
    correct_cnt = 0
    for o_t_i, os_i in zip(o_t, os):
        if (o_t_i == os_i):
            correct_cnt += 1
    accuracy = float(correct_cnt) / float(len(o_t))
    ##calculate accuracy
    return accuracy

def plot_accuracy(train_accuracies, test_accuracies, lr, bs):
    train_accs_y = np.array(train_accuracies)
    epochs = []
    for i in range(len(train_accuracies)):
        epochs.append(i)
    epochs_x = np.array(epochs)
    plt.plot(epochs_x, train_accs_y, label = "train accuracy")
    test_accs_y = np.array(test_accuracies)
    plt.plot(epochs_x, test_accs_y, label = "test accuracy")
    title = stage
    title += ' lr:'
    title += str(lr)
    title += ' batch_size:'
    title += str(bs)
    plt.title(title)
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.show()

# In[25]:


train(n_data, o, lr = 0.0001, H = 2, bs = 1)


# In[ ]:





# In[ ]:
