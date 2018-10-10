#coding=utf-8
import numpy as np

class KMeans(object):
    def __init__(self):
        self.k = 2
        self.episode = 10
        self.point = np.zeros((5, 3))
        self.center = np.zeros((self.k, 3))
        self.new_center = np.zeros((self.k, 3))
        self.buildAllPoint()
        self.buildCenterpoint()

    def buildAllPoint(self):
        x1 = np.array([1, 2])
        x2 = np.array([4, 7])
        x3 = np.array([3, 1])
        x4 = np.array([6, 8])
        x5 = np.array([2, 5])
        x = np.vstack((x1, x2, x3, x4, x5))

        self.point[:, :-1] = x

    def buildCenterpoint(self):
        self.center = self.point[np.random.randint(self.point.shape[0], size=self.k), :]
        self.center[:, -1] = range(1, self.k + 1)

    def operationAll(self):
        for _ in range(self.episode):
            self.operationOne()

    def operationOne(self):
        for i in range(self.point.shape[0]):

            self.updatePointLabel(i)

        self.buildCenterpoint()

        print self.point


    def updatePointLabel(self, number):
        label = 1
        self.point[number, -1] = label
        minDist = np.linalg.norm(self.point[number, :-1] - self.center[0, :-1])
        for i in range(1, self.k):
            if np.linalg.norm(self.point[number, :-1] - self.center[i, :-1]) < minDist:
                label = i+1
                self.point[number, -1] = label

    def updateCentralPoint(self):
        # label
        for i in range(1, self.k + 1):
            tmp = self.point[self.point[:, -1] == i, :-1]
            self.new_center[i-1, :-1] = np.mean(tmp)
            self.new_center[i-1, -1] = i

if __name__ == '__main__':
    k = KMeans()
    k.operationAll()
