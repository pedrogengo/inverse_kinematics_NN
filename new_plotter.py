from matriz_homogenea import Manipulator, Joint
from matriz_homogenea import Joint
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import matplotlib.animation as animation

joint1 = Joint(140, 0, 25, 90)
joint2 = Joint(0, 50, 0, 0, link=joint1)
joint3 = Joint(0, 50, 0, 0, link=joint2)

robot = Manipulator([joint1, joint2, joint3])
robot.forward_kinematics()

X, Y, Z = [], [], []
final_X, final_Y, final_Z = [], [], []
points = []
robot.update_theta(0, 0)
robot.update_theta(1, 0)
robot.update_theta(2, -90)
theta2 = 0
theta3 = -90
for k in range(3):
    for i in range(0, 360, 15):
        robot.update_theta(0, i)
        robot.update_theta(1, theta2)
        robot.update_theta(2, theta3)
#         robot.update_theta(2, k)
        robot.forward_kinematics()
        X = robot.get_all_X()
        Y = robot.get_all_Y()
        Z = robot.get_all_Z()
        points.append([X, Y, Z])
        final_X.append(robot.get_X())
        final_Y.append(robot.get_Y())
        final_Z.append(robot.get_Z())
        theta2 += 1.25
        theta3 += 1.25

points = points
points_arm_path_x = final_X
points_arm_path_y= final_Y
points_arm_path_z = final_Z
     

def update(num, points, line, arm_path):
    line.set_data(np.array(points[num][:2]))
    line.set_3d_properties(np.array(points[num][2]))
    arm_path = ax.scatter3D(points_arm_path_x[:num+1], points_arm_path_y[:num+1], points_arm_path_z[:num+1], color = 'green')


fig = plt.figure()
ax = p3.Axes3D(fig)
# ax.set_aspect('equal')
line, = ax.plot(X, Y, Z)
arm_path = ax.scatter3D(points_arm_path_x[0], points_arm_path_y[0], points_arm_path_z[0], color = "green")

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# set_axes_equal(ax)

ani = animation.FuncAnimation(fig, update, 24*3, fargs=(points, line, arm_path),
                                       interval=10, blit=False, repeat=True)

plt.show()