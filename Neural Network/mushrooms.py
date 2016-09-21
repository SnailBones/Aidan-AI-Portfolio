import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def dsigmoid(x):
    return x * (1 - x)

class Brain:
    def __init__(self, l, learning_rate, min_learning_rate, decrease):
        self.layers = l
        self.learning_rate = learning_rate
        self.min_lr = min_learning_rate
        self.decrease = decrease

    def reportAccuracy(self, X, y):
        out = X
        for layer in self.layers:
            out = layer.forward(out)
        out = np.round(out)
        count = np.count_nonzero(y - out)
        correct = len(X) - count
        print "%.4f" % (float(correct)*100.0 / len(X))

    def calculateDerivError(self, y, pred):
        return 2*(y - pred)

    def calculateError(self, y, pred):
        return (np.sum(np.power((y - pred), 2)))

    def iteration(self, X, y):
        out = X
        for layer in self.layers:
            out = layer.forward(out)
        #print out
        deriv_err = self.calculateDerivError(y, out)
        for layer in reversed(self.layers):
            deriv_err = layer.backward(deriv_err, self.learning_rate).T
        return out

    def train(self, X, y, test_x, test_y, number_epochs, how_frequent):
        for i in range(number_epochs):
            me = self.iteration(X, y)
            if self.learning_rate > self.min_lr:
                self.learning_rate *= self.decrease
            if i % how_frequent == 0:
                print me
                self.reportAccuracy(X, y)
                self.reportAccuracy(test_x, test_y)

class Layer:

    def __init__(self, size, nodes):
        self.size = size
        self.nodes = nodes
        self.weights = np.random.rand(size, nodes) #size by nodes

    def forward(self, X): #x is 1d array
        self.incoming = X
        act = X.dot(self.weights)    #dot product
        act = sigmoid(act)     #sigmoid
        self.outputs = act
        return act


    def backward(self, err, learning_rate):
        err = err * dsigmoid(self.outputs)
        update = learning_rate * self.incoming.T.dot(err)
        passback = self.weights.dot(err.T)
        self.weights += update
        return passback




def loadDataset(filename, size, test_size = 100):
    my_data = np.genfromtxt(filename, delimiter=',', skip_header=0)

    # The labels of the cases
    # Raw labels are either 4 (cancer) or 2 (no cancer)
    # Normalize these classes to 0/1
    y = (my_data[:size, 0])

    # Case features
    X = my_data[:size, 1:]
    #print y.size
    # Normalize the features to (0, 1)
    X_norm = X / X.max(axis=0)

    cut = size-test_size

    test_x = X_norm[cut:, :]
    learn_x = X_norm[:cut,:]

    test_y = y[cut:]
    learn_y = y[:cut]


    return learn_x, learn_y, test_x, test_y

def gradientChecker(model, X, y):
    epsilon = 1E-5

    for layer in (model.layers):
        layer.weights[1] += epsilon
        out1 = layer.forward(X)
        err1 = model.calculateError(y, out1)

        layer.weights[1] -= 2*epsilon
        out2 = layer.forward(X)
        err2 = model.calculateError(y, out2)

        numeric = (err2 - err1) / (2*epsilon)
        print numeric

        layer.weights[1] += epsilon
        out3 = layer.forward(X)
        err3 = model.calculateDerivError(y, out3)
        derivs = layer.backward(err3, .01)
        print derivs[0][1]




if __name__=="__main__":
    #size = 4000
    testsize = 500;
    size = 8124
    X, y, test_x, test_y = loadDataset("mushrooms.csv", size, testsize)
    # X = X
    y = y.reshape(size-testsize, 1)
    test_y = test_y.reshape(testsize, 1)
    print X
    print y
    print X.shape, y.shape
    layers = []
    layer1 = Layer(19, 5)
    layer2 = Layer(5, 1)
    layers.append(layer1)
    layers.append(layer2)
    model = Brain(layers, .001, .001, 1)
    #gradientChecker(model, X, y)
    model.train(X, y, test_x, test_y, 10000,100)
