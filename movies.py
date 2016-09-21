import matplotlib.pyplot as plt
import numpy as np
import math
import random

class SparseVector:
	#uses nested dictionaries
	def __init__(self):
		self.my_data = {}
	def setMe(self, movie, user, rating):
		if self.my_data.has_key(movie):
			# my_score = {}
			# my_score[user] = rating	#add new pair to inner dictionary
			# self.my_data[movie] = my_score
			self.my_data[movie][user]=rating
			return
		my_row = {}
		my_row[user] = rating		#add new dictionary and append
		self.my_data[movie]= my_row
		return
	# def setMe(self, point):	#point is a dictionary. one movie with multiple ratings
	# 	if self.my_data.has_key(point):
	# 		my_score = {}
	# 		for user in point:
	# 			my_score[user] = rating	#add new pair to inner dictionary
	# 		self.my_data[movie] = my_score
	# 		return
	# 	my_row = {}
	# 	my_row[user] = rating		#add new dictionary and append
	# 	self.my_data[movie]= my_row
	# 	return
	def getAverage(self):
		total = 0
		count = 0
		for movie in self.my_data:
			for user in movie:
				total += movie[user]
				count += 1
		return total/count

	# def getDistance(self, movie1, movie2):
	# 	dist = 0
	# 	count = 0
	# 	m1 = self.my_data[movie1]
	# 	m2 = self.my_data[movie2]
	# 	for person in m1:
	# 		if person in m2:
	# 			#dist += (math.pow(m1[person],2)-math.pow(m2[person],2))
	# 			dist += abs(m1[person]-m2[person])
	# 	distance = dist/count
	# 	return distance;

# def getMean(m1, m2):
# 	mean_movie = {}
# 	for person in m1:
# 		if person in m2:
# 			mean_rating = (m1[person] + m2[person])/2
# 		else:
# 			mean_rating = m1[person]
# 		mean_movie[person] = mean_rating
# 	for person in m2:
# 		if not person in mean_movie:
# 			mean_movie[person] = m2[person]
# 	return mean_movie

def getMean(points): #list of points
	mean_movie = {}
	#construct dictionary of people
	people = {}	#each person should correspond to a list of ratings
	for movie in points:
		for person in points[movie]:
			if not person in people:
				people[person] = []
			people[person].append(points[movie][person])	#add the rating
	for person in people:
		mean_rating = np.mean(people[person])
		mean_movie[person] = mean_rating
	return mean_movie

def getClosest(point, centroids):
	min_dist = float('inf')
	#print centroids.my_data
	for centroid in centroids.my_data:
		#print point, centroids.my_data[centroid]
		dist = getDistance(point, centroids.my_data[centroid])
		if dist < min_dist:
			min_dist = dist
			closest = centroid
	return closest

def getDistance(m1, m2):
	dist = 0
	count = 0
	connect = 0
	for person in m1:
		if person in m2:
			#dist += (math.pow(m1[person],2)-math.pow(m2[person],2))
			dist += abs(m1[person]-m2[person])
			connect = 1
			count += 1
	if connect:
		distance = dist/count
	else:
		distance = 100
	return distance;

def cluster(points, k):
	centroids = SparseVector()
	for i in range(k):
		movie = random.choice(points.my_data.keys())
		human = random.choice(points.my_data[movie].keys())
		rating = points.my_data[movie][human]
		centroids.setMe(movie, human, rating)
	domains = {}
	old_distance = float('inf')
	distance = 0
	epochs = 0
	while distance < old_distance: # and epochs < 5:
		if  epochs > 0:
			old_distance = distance
		distance = 0
		domains = {}
		#print domains
		for point in points.my_data:
		 	my_centroid = getClosest(points.my_data[point], centroids)
			if domains.has_key(my_centroid):
				for human in points.my_data[point]:
					rating = points.my_data[point][human]
					domains[my_centroid].setMe(point,human,rating)
			else:
				domain = SparseVector()
				for human in points.my_data[point]:
					rating = points.my_data[point][human]
					domain.setMe(point, human, rating)
				domains[my_centroid] = domain
			distance += getDistance(points.my_data[point], centroids.my_data[my_centroid])

			#update each centroid
		#for centroid in centroids.my_data:
		for centroid in domains:
			#print centroid
			#print domains[centroid]
			#print domains[centroid].my_data
			centroids.my_data[centroid] = getMean(domains[centroid].my_data)
			# for point in domains[centroid].my_data:
			# 	centroids.my_data[centroid] = getMean(centroids.my_data[centroid], domains[centroid].my_data[point])
		epochs += 1
		print "epoch ", epochs
		print distance
		#print old_domains
	return domains;

def test(clusters, k = 10):
	c = 0
	size = 0
	for centroid in clusters:
		c += 1
		print "cluster ", c
		print "size ", len(clusters[centroid].my_data)
		size += len(clusters[centroid].my_data)
		for i in range(k):
			movie = random.choice(clusters[centroid].my_data.keys())
			#human = random.choice(clusters[centroid].my_data[movie].keys())
			#rating = clusters[centroid].my_data[movie][human]
			print "movie #", movie
		print "total size ", size


def loadDataset(filename='u.data'):
	in_data = np.genfromtxt(filename)
	#person movie rating
	#initialize sparse vector
	movies = SparseVector()
	for row in in_data:
		movies.setMe(row[1],row[0],row[2])
	return movies

if __name__=="__main__":
	movies = loadDataset()
	clusters = cluster(movies, 20)
	test(clusters)

#1682 movies
