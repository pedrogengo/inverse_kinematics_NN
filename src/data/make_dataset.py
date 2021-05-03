import numpy as np


def create_theta_list(thetas):
    '''
    Funcao responsavel por receber uma lista de listas contendo
    os valores dos angulos thetas que serao usados para gerar
    a base de treinamento. Retorna uma lista de listas onde cada
    elemento e uma tripla de theta1, theta2 e theta3.
    '''
    theta1, theta2, theta3 = thetas
    train_list = []
    for i in theta1:
        for j in theta2:
            for k in theta3:
                train_list.append([float(i),float(j),float(k)])
    return train_list

def create_train_points(theta_list, robot):
    '''
    Funcao responsavel por gerar a base de treino (X e y). Recebe
    uma lista de coordenadas thetas e, por meio da cinematica direta
    aplicada ao robo, calcula as coordenadas do end effector, que sera
    a entrada do nosso treinamento.
    '''
    coord_endeffector = []
    new_theta_list = []
    for theta1, theta2, theta3 in theta_list:
        robot.update_theta(0, theta1)
        robot.update_theta(1, theta2)
        robot.update_theta(2, theta3)
        
        robot.forward_kinematics()

        coord_endeffector.append([
                                  robot.get_X(),
                                  robot.get_Y(),
                                  robot.get_Z()
                                ])
    return np.array(coord_endeffector), np.array(theta_list)

def make_dataset(robot, thetas, dataset_name):
    theta_list = create_theta_list(thetas)
    X, y = create_train_points(theta_list, robot)
    dataset = ''

    for i, j in zip(X, y):
        dataset += ','.join(str(i)) + ',' + ','.join(str(j)) + '\n'
    with open(f'data/{dataset_name}.csv', 'w') as f:
        f.write(dataset)
    
    return X, y