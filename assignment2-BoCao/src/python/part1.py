
# coding: utf-8

# In[59]:


import numpy as np
import random

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


# In[60]:


#normalize inputs

#normalize t
t_min = np.min(t)
t_max = np.max(t)
d_t = t_max - t_min
#normalized t: n_t
n_t = []
for each in t:
    n_t.append((each - t_min) / d_t)

#normalize hu
hu_min = np.min(hu)
hu_max = np.max(hu)
d_hu = hu_max - hu_min
#normalized h: n_hu
n_hu = []
for each in hu:
    n_hu.append((each - hu_min) / d_hu)

#normalize lt
lt_min = np.min(lt)
lt_max = np.max(lt)
d_lt = lt_max - lt_min
#normalized lt: n_lt
n_lt = []
for each in lt:
    n_lt.append((each - lt_min) / d_lt)

#normalize co2
co2_min = np.min(co2)
co2_max = np.max(co2)
d_co2 = co2_max - co2_min
#normalized co2: n_co2
n_co2 = []
for each in co2:
    n_co2.append((each - co2_min) / d_co2)

#normalize hu_r
hu_r_min = np.min(hu_r)
hu_r_max = np.max(hu_r)
d_hu_r = hu_r_max - hu_r_min
#normalized hu_r: n_hu_r
n_hu_r = []
for each in hu_r:
    n_hu_r.append((each - hu_r_min) / d_hu_r)

#normalized data: n_data
n_data = np.column_stack((n_t, n_hu, n_lt, n_co2, n_hu_r))
print "n_data:", n_data


# In[61]:


def initialize_weights():
    w_t = random.random()
    w_hu = random.random()
    w_lt = random.random()
    w_co2 = random.random()
    w_hu_r = random.random()
    b = random.random()

    #weights
    ws = [w_t, w_hu, w_lt, w_co2, w_hu_r, b]
    return ws

ws = initialize_weights()
print "ws: ", ws


# In[80]:


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def activation(x): # use sigmoid as activation function
    a = sigmoid(x)
    if a >= 0.5:
        return 1
    else:
        return 0

def perceptron(ins, ws):
    sum = 0
    for x, w in zip(ins, ws):
        sum += x * w
    return activation(sum)

# lr - learning rate
# bs - batch size
def train(n_data, lr, bs):

    print "len of data:", len(n_data)

    accuracy = []
    epoch = 0
    while epoch <= 2500:
        # train
        i = 0
        for (n_t_i, n_hu_i, n_lt_i, n_co2_i, n_hu_r_i, o_i) in zip(n_t, n_hu, n_lt, n_co2, n_hu_r, o):
            sum_error_w_t = 0
            sum_error_w_hu = 0
            sum_error_w_lt = 0
            sum_error_w_co2 = 0
            sum_error_w_hu_r = 0
            sum_error_b = 0

            error = o_i - (n_t_i * ws[0] + n_hu_i * ws[1] + n_lt_i * ws[2] + n_co2_i * ws[3] + n_hu_r_i * ws[4] + ws[5])
            sum_error_w_t += error * n_t_i
            sum_error_w_hu += error * n_hu_i
            sum_error_w_lt += error * n_lt_i
            sum_error_w_co2 += error * n_co2_i
            sum_error_w_hu_r += error * n_hu_r_i
            sum_error_b += error

            if i >= bs: # only update weights after one batch size
                ws[0] += lr * sum_error_w_t
                ws[1] += lr * sum_error_w_hu
                ws[2] += lr * sum_error_w_lt
                ws[3] += lr * sum_error_w_co2
                ws[4] += lr * sum_error_w_hu_r
                ws[5] += lr * sum_error_b
                sum_error_w_t = 0
                sum_error_w_hu = 0
                sum_error_w_lt = 0
                sum_error_w_co2 = 0
                sum_error_w_hu_r = 0
                sum_error_b = 0
                i = 1
                continue

            #calculate accuracy
            #outputs
            os = []
            for each in zip(n_data):
                for ins in each:
                    os.append(perceptron(ins, ws))

            #count correct output number
            correct_cnt = 0
            for o_i, os_i in zip(o, os):
                if (o_i == os_i):
                    correct_cnt += 1
            accuracy = float(correct_cnt) / float(len(o))
            print "epoch:", epoch, "correct_cnt:", correct_cnt, " accuracy",accuracy
            ##calculate accuracy

            i += 1

        # count

        epoch += 1


# In[81]:


train(n_data, lr = 0.0001, bs = 1)


# In[ ]:





# In[ ]:
