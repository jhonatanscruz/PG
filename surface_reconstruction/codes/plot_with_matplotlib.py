import numpy as np
import matplotlib.pyplot as plt
from math import pi,cos,sin
import os

def x_rotation(angle):
    rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle), cos(angle),0],[0,0,0,1]])
    return rotation_matrix

# PATHS HANDLE
cwd = os. getcwd().split('/')

if cwd[-1] == "PG_controle":
    input_path  = "surface_reconstruction/point_cloud_input/"
    output_path = "surface_reconstruction/output/"

elif cwd[-1] == "surface_reconstruction":
    input_path  = "point_cloud_input/"
    output_path = "output/"

else:
    input_path  = "../point_cloud_input/"
    output_path = "../output/"

# Create variables that hold data paths and the point cloud data
dataname    = "goku.xyz"
point_cloud = np.loadtxt(input_path+dataname,skiprows=0)

# PRE PROCESSAMENTO

# TRANSFORMA PARA COORDENADAS HOMOGÊNEAS
point_cloud = np.transpose(point_cloud)
#add a vector of ones to the house matrix to represent the house in homogeneous coordinates
point_cloud = np.vstack([point_cloud, np.ones(np.size(point_cloud,1))])

# ROTACIONA EM RELAÇÃO AO EIXO X
point_cloud = np.dot(x_rotation(pi/2),point_cloud)

# SCATTER PLOT
scatter = plt.figure()
ax1 = scatter.add_subplot(projection='3d')
ax1.set_xlim([-1,1])
ax1.set_xlabel("x axis")
ax1.set_ylim([-1,1])
ax1.set_ylabel("y axis")
ax1.set_zlim([-1,1])
ax1.set_zlabel("z axis")
ax1.scatter(point_cloud[0,:], point_cloud[1,:], point_cloud[2,:], marker='.', antialiased=True)

# PLOT3D
plot3D = plt.figure()
ax2 = plt.axes(projection='3d')
ax2.set_xlim([-1,1])
ax2.set_xlabel("x axis")
ax2.set_ylim([-1,1])
ax2.set_ylabel("y axis")
ax2.set_zlim([-1,1])
ax2.set_zlabel("z axis")
ax2.plot3D(point_cloud[0,:], point_cloud[1,:], point_cloud[2,:], color='red', antialiased=True)

# TRISURF PLOT
trisurf = plt.figure()
ax3 = trisurf.add_subplot(projection='3d')
ax3.set_xlim([-1,1])
ax3.set_xlabel("x axis")
ax3.set_ylim([-1,1])
ax3.set_ylabel("y axis")
ax3.set_zlim([-1,1])
ax3.set_zlabel("z axis")
ax3.plot_trisurf(point_cloud[0,:], point_cloud[1,:], point_cloud[2,:], cmap=plt.cm.Spectral, antialiased=True)

plt.show()