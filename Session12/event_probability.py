import sys
import numpy as np
from scipy.special import erf

#computes the probability of an event
#of magnitude x or greater from
#a gaussian distribution

def event_probability(x,mu=0.0,s=1.0):
	#x is the value of the event
	#mu is the gaussian mean (default 0.0)
	#s is the gaussian std dev (default 1.0)

	#z is how many sigma away x is from mean
	z = np.fabs((x-mu)/s)
	#def zfunc(z):
	#	return 0.5*(1.0+erf(z/np.sqrt(2)))

	return 1.0 - erf(z/np.sqrt(2))

def main():
	x = 3.0 #default is 3 sigma

	#if another number is provided
	#on the command line, use it for x
	if(len(sys.argv)>1):
		x = float(sys.argv[1])

	#get the event probability
	prob = event_probability(x)

	print(f'The Gaussian probability of events larger than {x} is {prob*100:6.4f}%.')
	print(f'The Gaussian probability of events smaller than {x} is {(1-prob)*100:6.4f}%.')

#run the program
if __name__ == '__main__':
	main()

