import numpy as np

studentsPerTF = 16

def RMS(predictions, actuals):
	return 0

def abs_TF_diff(predictions, actuals):
	assert len(predictions) == len(actuals)
	return np.mean(np.floor(np.absolute(np.subtract(predictions, actuals) / studentsPerTF)))

def abs_diff(predictions, actuals):
	assert len(predictions) == len(actuals)
	return np.mean(np.absolute(np.subtract(predictions, actuals)))
