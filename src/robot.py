import numpy as np
import plotly.graph_objects as go
from math import radians, sin, cos

class Manipulator():
    def __init__(self, joints):
        self.joints = joints
    
    def forward_kinematics(self):
        for joint in self.joints:
            joint._update_matrix()
    
    def get_joint_index(self):
        return {joint: i for i, joint in enumerate(joints)}
    
    def update_theta(self, joint_index, theta):
        self.joints[joint_index].update_theta(theta)
    
    def plot_workspace(self, theta_list, initial):
        X, Y, Z = [], [], []
    
        for theta1 in theta_list[0]:
            for theta2 in theta_list[1]:
                for theta3 in theta_list[2]:
                    self.update_theta(0, theta1)
                    self.update_theta(1, theta2)
                    self.update_theta(2, theta3)
                    
                    self.forward_kinematics()
                    X.append(self.get_X())
                    Y.append(self.get_Y())
                    Z.append(self.get_Z())
                    
        for i in range(len(self.joints)):
            self.update_theta(i, initial[i])
        self.forward_kinematics()
                    
        X_ = self.get_all_X()
        Y_ = self.get_all_Y()
        Z_ = self.get_all_Z()
        
        fig = go.Figure(data=go.Scatter3d(
            x=X, y=Y, z=Z,
            mode = 'markers',
            marker=dict(
                size=0,
                color="green",
                opacity=0.5
                )
            ))
        
        fig.add_trace(go.Scatter3d(
                            x=X_, y=Y_, z=Z_,
                            marker=dict(
                                size=0,
                                color=3,
                                colorscale='Viridis',
                            ),
                            line=dict(
                                color='darkblue',
                                width=5
                            )
                        ))

        fig.update_layout(scene = dict(
                                        xaxis = dict(nticks=8, range=[min(X) - 1,max(X) + 1]),
                                        yaxis = dict(nticks=8, range=[min(Y) - 1,max(Y) + 1]),
                                        zaxis = dict(nticks=8, range=[min(Z) - 1,max(Z) + 1])),
                           width=700, height=700, autosize=False, scene_aspectmode='cube', showlegend=False)
        fig.show()
    
    def static_plot(self):
        X = self.get_all_X()
        Y = self.get_all_Y()
        Z = self.get_all_Z()

        fig = go.Figure(data=go.Scatter3d(
            x=X, y=Y, z=Z,
            marker=dict(
                size=0,
                color=3,
                colorscale='Viridis',
            ),
            line=dict(
                color='darkblue',
                width=2
            ),
        ))

        fig.update_layout(scene = dict(
                                        xaxis = dict(nticks=8, range=[min(X) - 1,max(X) + 1]),
                                        yaxis = dict(nticks=8, range=[min(Y) - 1,max(Y) + 1]),
                                        zaxis = dict(nticks=8, range=[min(Z) - 1,max(Z) + 1])),
                           autosize=False,
                           width=700,
                           height=700,)
        fig.show()

    def get_all_X(self):
        X = [0]
        for joint in self.joints:
            X.append(joint.get_XYZ()[0])
        return X
    
    def get_all_Y(self):
        Y = [0]
        for joint in self.joints:
            Y.append(joint.get_XYZ()[1])
        return Y
    
    def get_all_Z(self):
        Z = [0]
        for joint in self.joints:
            Z.append(joint.get_XYZ()[2])
        return Z

    def get_X(self):
        return self.joints[-1].get_XYZ()[0]
    
    def get_Y(self):
        return self.joints[-1].get_XYZ()[1]
    
    def get_Z(self):
        return self.joints[-1].get_XYZ()[2]
    


class Joint():

    def __init__(self, d, a, theta, alpha, link = None):
        self.d = d
        self.a = a
        self.theta = theta
        self.alpha = alpha
        self.link = link
        self.matrix = self._generate_matrix()
        self.updated_matrix = None

        
    def _generate_matrix(self):
        matrix = np.identity(4)
        matrix[0,0] = cos(radians(self.theta))
        matrix[0,1] = -sin(radians(self.theta)) * cos(radians(self.alpha))
        matrix[0,2] = sin(radians(self.theta)) * sin(radians(self.alpha))
        matrix[0,3] = self.a * cos(radians(self.theta))
        matrix[1,0] = sin(radians(self.theta))
        matrix[1,1] = cos(radians(self.theta)) * cos(radians(self.alpha))
        matrix[1,2] = -cos(radians(self.theta)) * sin(radians(self.alpha))
        matrix[1,3] = self.a * sin(radians(self.theta))
        matrix[2,1] = sin(radians(self.alpha))
        matrix[2,2] = cos(radians(self.alpha))
        matrix[2,3] = self.d
        return matrix
    
    def update_theta(self, theta):
        self.theta = theta
        self.matrix = self._generate_matrix()

    def _update_matrix(self):
        if self.link is not None:
            self.updated_matrix = np.dot(self.link.updated_matrix, self.matrix)
        else:
            self.updated_matrix = self.matrix
        return self.updated_matrix

    def get_XYZ(self):
        if self.updated_matrix is None:
            raise "Please, use the forward kinematics function first."
        return self.updated_matrix[0,3], self.updated_matrix[1,3], self.updated_matrix[2,3]
    
    def __repr__(self):
        line = ''
        for i in range(4):
            for j in range(4):
                line += str(round(self.matrix[i][j], 2)) + '  '
            line += '\n'
        return line

if __name__ == "__main__":
    matriz_teste = Joint(10, 1, 0, 90)
    print(matriz_teste)