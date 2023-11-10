#---------------------------# Importations #---------------------------#

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

basicmap = Image.open('noiseTexture.png')
basicmap = np.asarray(basicmap)
basicmap1 = Image.open('noiseTexture(1).png')
basicmap1 = np.asarray(basicmap1)
basicmap2 = Image.open('noiseTexture(2).png')
basicmap2 = np.asarray(basicmap2)

list_image = [basicmap, basicmap1, basicmap2]


#---------------------------# Consts #---------------------------#

SHAPE = basicmap.shape[0]
PROP = 2
RESULT_SHAPE = int(SHAPE/PROP)


#---------------------------# Functions #---------------------------#

def keep_only_alpha(matrix):
	tmp = np.zeros((SHAPE, SHAPE))
	for i in range(SHAPE):
		for j in range(SHAPE):
			tmp[i][j] = matrix[i][j][0]
	return tmp


def blend_image(list_matrix):
	matrix = list_matrix[0]
	for i in range(SHAPE):
		for j in range(SHAPE):
			for index in range(1,len(list_matrix)):
				matrix[i][j] += list_matrix[index][i][j]
	return matrix


def convert_to_matrix(matrix):
	result = np.zeros((RESULT_SHAPE, RESULT_SHAPE))
	for i in range(0, SHAPE, PROP):
		for j in range(0, SHAPE, PROP):
			mean = 0
			for k in range(PROP):
				for l in range(PROP):
					mean += matrix[i+k][j+l]
			
			mean = mean/(PROP*PROP)
			if mean < 120: 
				mean = 0.0
			elif mean < 200:
				mean = 0.4
			else:
				mean = 0.7
			result[int(i/PROP)][int(j/PROP)] = mean
	return result


def reduce_artefact(matrix):
	shape = matrix.shape[0]
	dic = {
		"0.0" : 0,
		"0.4" : 0,
		"0.7" : 0,
		"1.0" :  0
	}
	for i in range(1, shape-1):
		for j in range(1, shape-1):
			dic[str(matrix[i][j-1])] += 1
			dic[str(matrix[i][j+1])] += 1
			dic[str(matrix[i-1][j])] += 1
			dic[str(matrix[i+1][j])] += 1
			if dic[str(matrix[i][j])] >= 2:
				pass
			else:
				matrix[i][j] = max(dic, key= lambda x: dic[x])
			dic = {
				"0.0" : 0,
				"0.4" : 0,
				"0.7" : 0,
				"1.0" :  0
		 	}
	return matrix


def create_boundaries(matrix):
	shape = matrix.shape[0]-1
	matrix[::,0] = 1
	matrix[::, shape] = 1
	matrix[0, ::] = 1
	matrix[shape, ::] = 1
	return matrix


#---------------------------#  #---------------------------#

basicmap = blend_image(list_image)
basicmap = keep_only_alpha(basicmap)

basicmap = convert_to_matrix(basicmap)
basicmap = create_boundaries(basicmap)
basicmap = reduce_artefact(basicmap)

#PLT 
plt.matshow(basicmap)
plt.colorbar()
plt.show()