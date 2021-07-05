import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt 
import os

def sim_pen_eq(t, theta):
	dtheta2_dt = (-b/m)*theta[1] + (-g/L)*np.sin(theta[0]) + (1/(m*L*L))*u
	dtheta1_dt = theta[1]
	return [dtheta1_dt, dtheta2_dt]

Start_time = float(0)   
End_time = float(20)    
Sampling_Frequency = float(10) 
N = End_time*Sampling_Frequency
st = 1/Sampling_Frequency # Sampling time
Sampling_time = [0, st]
t = np.arange(Start_time, st, st/100)
l = np.arange(0, int((End_time-Start_time)/st), 1)

g = 9.81  # gravity(m/s^2)
L = 1     # Length of pendulum(m)
b = 0.5   # Damping factor(kg/s) 
m = 0.5   # Mass(kg)

a = 5     # Convergence rate
k = 3     # Switching term
ramda = 0.5

## main
theta1_ini = 0
theta2_ini = 0
theta_ini = [theta1_ini, theta2_ini]

theta1_des = math.pi
theta2_des = 0
theta_des = [theta1_des, theta2_des]

theta1_data = []
theta2_data = []

for i in l:
	theta1_err = theta_ini[0] - theta_des[0]
	theta2_err = theta_ini[1] - theta_des[1]

	# Defining the linear sliding surface
	s = a*theta1_err + theta2_err
	# Chattering free SMC design with power rate reaching law
	u = (m*L*L)*(-a*theta1_err + (g/L)*np.sin(theta1_err)) - k*abs(s)**(ramda)*np.sign(s) 
	
	theta12 = solve_ivp(sim_pen_eq, Sampling_time, theta_ini)
	theta1 = theta12.y[0,:]
	theta2 = theta12.y[1,:]
	theta1 = theta1[-1]
	theta2 = theta2[-1]
	theta1_data.append(theta1)
	theta2_data.append(theta2)
	theta_ini = [theta1, theta2]

## simulation
x =  L*np.sin(theta1_data)
y = -L*np.cos(theta1_data)

fig = plt.figure()
for point in l:
	plt.plot(x[point], y[point], 'bo')
	plt.plot([0,x[point]],[0,y[point]])
	plt.xlim(-L-0.5,L+0.5)
	plt.ylim(-L-0.5,L+0.5)
	plt.xlabel('x-direction')
	plt.ylabel('y-direction')
	plt.pause(0.01)	
	fig.clear()
plt.draw()