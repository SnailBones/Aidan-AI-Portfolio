import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42) # Get the same random numbers every time


# Ugly code for thinking about linear regression with gradient descent

################################################################
### Load the dataset
#my_data = np.genfromtxt('gpa.csv', delimiter=';', skip_header=1)[:10]
my_data = np.genfromtxt('djia_temp.csv', delimiter=';', skip_header=1)[:21]
date = my_data[:, 0]
dow = my_data[:, 1]
today_temp = my_data[:,2]
avg_temp = my_data[:,3]

temp_dif = today_temp-avg_temp;
#temp_dif = today_temp;
################################################################
### Init the model parameters
weight = np.random.rand(1)
bias = np.random.rand(1)
print weight, bias
print temp_dif


################################################################
### How do we change the weight and the bias to make the line's fit better?
learning_rate = 0.05
end_rate = 0.001

cost = np.sum(np.power((temp_dif*weight+bias) - dow, 2))
print cost

for i in range(1000):
	if learning_rate > end_rate:
		learning_rate = learning_rate * .995
	error = (temp_dif*weight+bias) - dow
	weight = weight - np.sum(learning_rate * error * temp_dif / len(temp_dif))
	bias = bias - np.sum(learning_rate * error * 1.0 / len(temp_dif))
	#cost = np.sum(np.power((temp_dif*weight+bias) - dow, 2))
	# print cost


################################################################
## Graph the dataset along with the line defined by the model

xs = np.arange(-20, 20)
ys = xs * weight + bias

plt.plot(temp_dif, dow, 'r+', xs, ys, 'g-')
plt.show()
