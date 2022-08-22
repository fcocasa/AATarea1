from gym_minigrid.minigrid import OBJECT_TO_IDX, IDX_TO_OBJECT
import math
import time

AGENT_DIR_TO_STR = {0: ">", 1: "V", 2: "<", 3: "^"}


def print_world(image, agent_dir, agent_pos):
    for y_axis in image:
        print("\n\t")
        for cell in y_axis:
            cell_render = AGENT_DIR_TO_STR[agent_dir] if (cell[1] == agent_pos[0] and cell[0] == agent_pos[1]) \
                else IDX_TO_OBJECT[cell[2]][0].upper() if cell[2] > -1 else '_'
            print(cell_render, end='   ')


def matrix_value(i, j, matrix):  # USES X,Y NOTATION
    return matrix[j][i][2]


def matrix_value_visibility(i, j, matrix, agent_pos=None, visibility=None):
    if visibility is None:
        return matrix_value(i, j, matrix)
    else:
        for c_shift in visibility:
            c_pos = [c_shift[0]+agent_pos[0], c_shift[1]+agent_pos[1]]
            if i == c_pos[0] and j == c_pos[1]:  # within range
                return matrix_value(i, j, matrix)
        return 0
# agent_dir [0,1,2,3] = [wall_east,wall_south,wall_west,wall_north]


def goal_step_distance(observation, agent_pos_x, agent_pos_y, agent_dir, visibility):
    l = len(observation)
    for i in range(0, l):
        for j in range(0, l):
            if matrix_value_visibility(i, j, observation, visibility) == 8:
                # we add extra steps needed when not aligned to the direction of the goal
                if i-agent_pos_x > 0:  # >>>>>
                    if agent_dir == 0:  # >
                        extra_step_x = 0
                    elif agent_dir == 1 or agent_dir == 3:  # ^ v
                        extra_step_x = 1
                    else:
                        extra_step_x = 2  # <
                else:                  # <<<<<
                    if agent_dir == 0:  # >
                        extra_step_x = 2
                    elif agent_dir == 1 or agent_dir == 3:  # ^ v
                        extra_step_x = 1
                    else:
                        extra_step_x = 0  # <

                if j-agent_pos_y > 0:  # vvvvvv
                    if agent_dir == 1:  # v
                        extra_step_y = 0
                    elif agent_dir == 0 or agent_dir == 2:  # < >
                        extra_step_y = 1
                    else:
                        extra_step_y = 2  # ^
                else:                   # ^^^^^
                    if agent_dir == 1:  # v
                        extra_step_y = 2
                    elif agent_dir == 0 or agent_dir == 2:  # < >
                        extra_step_y = 1
                    else:
                        extra_step_y = 0  # ^

                return [abs(i-agent_pos_x)+extra_step_x, abs(j-agent_pos_y)+extra_step_y]
    return[len(observation), len(observation)]


def goal_distance_orientation(observation, agent_pos_x, agent_pos_y, agent_dir):
    l = len(observation)
    find = False
    goal = []
    for i in range(0, l):
        for j in range(0, l):
            if matrix_value(i, j, observation) == 8:
                x = i
                y = j
                find = True
                break
        if find:
            break
    west = agent_pos_x-x if agent_pos_x-x >= 0 else l
    north = agent_pos_y-y if agent_pos_y-y >= 0 else l
    east = x-agent_pos_x if x-agent_pos_x >= 0 else l
    south = y-agent_pos_y if y-agent_pos_y >= 0 else l

    goal = [east, south, west, north]
    goal_dir = [abs(i-agent_pos_x), abs(j-agent_pos_y)]
    for i in range(agent_dir, agent_dir+4):
        goal_dir.append(goal[i % 4])
    # print('goalx')
    # print(x)
    # print('goaly')
    # print(y)
    # print('agent_pos_x')
    # print(agent_pos_x)
    # print('agent_pos_y')
    # print(agent_pos_y)
    # print('goal')
    # print(goal)
    # print('goal_dir')
    # print(goal_dir)
    return goal_dir


def walls_axis(observation, agent_pos_x, agent_pos_y, visibility):
    l = len(observation)
    wall = []
    for i in range(agent_pos_x, l):
        if matrix_value_visibility(i, agent_pos_y, observation, visibility) == 2 or matrix_value_visibility(i, agent_pos_y, observation, visibility) == 9 or matrix_value_visibility(i, agent_pos_y, observation, visibility) == 0:  # wall, lava or unseen
            wall.append(i-agent_pos_x)
            break

        elif matrix_value_visibility(i, agent_pos_y, observation, visibility) == 0:
            wall.append(i-agent_pos_x)
            break
    for j in range(agent_pos_y, l):
        if matrix_value_visibility(agent_pos_x, j, observation, visibility) == 2 or matrix_value_visibility(i, agent_pos_y, observation, visibility) == 9 or matrix_value_visibility(agent_pos_x, j, observation, visibility) == 0:  # wall, lava or unseen
            wall.append(j-agent_pos_y)
            break
        elif matrix_value_visibility(agent_pos_x, j, observation, visibility) == 0:  # unseen
            wall.append(j-agent_pos_y)
            break

    for i in range(agent_pos_x, -1, -1):
        if matrix_value_visibility(i, agent_pos_y, observation, visibility) == 2 or matrix_value_visibility(i, agent_pos_y, observation, visibility) == 9 or matrix_value_visibility(agent_pos_x, j, observation, visibility) == 0:  # wall, lava or unseen
            wall.append(agent_pos_x-i)
            break
        elif matrix_value_visibility(i, agent_pos_y, observation, visibility) == 0:  # unseen
            wall.append(agent_pos_x-i)
            break

    for j in range(agent_pos_y, -1, -1):
        if matrix_value_visibility(agent_pos_x, j, observation, visibility) == 2 or matrix_value_visibility(agent_pos_x, j, observation, visibility) == 9 or matrix_value_visibility(agent_pos_x, j, observation, visibility) == 0:  # wall, lava or unseen
            wall.append(agent_pos_y-j)
            break
        elif matrix_value_visibility(agent_pos_x, j, observation, visibility) == 0:  # unseen
            wall.append(agent_pos_y-j)
            break

    return wall


# calcula la distancia a cada parede segun su sentido de la orietacion
# world -> obs['image'] invertido
def walls_distance(observation, agent_pos_x, agent_pos_y, agent_dir, visibility):
    walls = walls_axis(observation, agent_pos_x, agent_pos_y, visibility)
    wall_dirs = []
    for i in range(agent_dir, agent_dir+4):
        wall_dirs.append(walls[i % 4])
    # walls[0] este
    # walls[1] surt
    # walls[2] oeste
    # walls[3] norte
    # print(walls)#(este, sur, oeste, norte)
    return wall_dirs  # (frente,derecha,atras,izquierda)


def try_forward(observation, agent_pos, agent_dir):
    # print(observation)
    # (este, sur, oeste, norte)
    if (agent_dir == 0):  # derecha
        if(matrix_value(agent_pos[0]+1, agent_pos[1], observation) != 2):
            return [agent_pos[0]+1, agent_pos[1]]
    elif(agent_dir == 2):  # izquierda
        if(matrix_value(agent_pos[0]-1, agent_pos[1], observation) != 2):
            return [agent_pos[0]-1, agent_pos[1]]
    elif(agent_dir == 1):  # abajo
        if(matrix_value(agent_pos[0], agent_pos[1]+1, observation) != 2):
            return [agent_pos[0], agent_pos[1]+1]
    elif(agent_dir == 3):  # arriba
        if(matrix_value(agent_pos[0], agent_pos[1]-1, observation) != 2):
            return [agent_pos[0], agent_pos[1]-1]
    """
    abajo y arriba estan "intercambiados", si le resto a la posicion en "y" entonces subo,
    si le sumo entonces bajo
    """
    return agent_pos  # en caso de no entrar a uno de los if retorno el mismo agent_pos


# even if i setp into lava or through a wall
def move_forward(observation, agent_pos, agent_dir):
    # print(observation)
    # (este, sur, oeste, norte)
    if (agent_dir == 0):  # derecha
        return [agent_pos[0]+1, agent_pos[1]]
    elif(agent_dir == 2):  # izquierda
        return [agent_pos[0]-1, agent_pos[1]]
    elif(agent_dir == 1):  # abajo
        return [agent_pos[0], agent_pos[1]+1]
    elif(agent_dir == 3):  # arriba
        return [agent_pos[0], agent_pos[1]-1]
# even if i setp into lava or through a wall

# def steps_over(observation, agent_pos):
#     # returns if we are stepping on lava o over a wall
#     return matrix_value(agent_pos[0], agent_pos[1], observation) == 2 or matrix_value(
#         agent_pos[0]+1, agent_pos[1], observation) == 9


def do_i_step_out_of_floor(observation, agent_pos, agent_dir):
    # print(observation)
    # (este, sur, oeste, norte)
    if (agent_dir == 0):  # derecha
        if matrix_value(agent_pos[0]+1, agent_pos[1], observation) == 2 or matrix_value(agent_pos[0]+1, agent_pos[1], observation) == 9:
            return 1
    elif(agent_dir == 2):  # izquierda
        if matrix_value(agent_pos[0]-1, agent_pos[1], observation) == 2 or matrix_value(agent_pos[0]-1, agent_pos[1], observation) == 9:
            return 1
    elif(agent_dir == 1):  # abajo
        if matrix_value(agent_pos[0], agent_pos[1]+1, observation) == 2 or matrix_value(agent_pos[0], agent_pos[1]+1, observation) == 9:
            return 1
    elif(agent_dir == 3):  # arriba
        if matrix_value(agent_pos[0], agent_pos[1]-1, observation) == 2 or matrix_value(agent_pos[0], agent_pos[1]-1, observation) == 9:
            return 1

    return 0  # you keep walking on the floor

  # last_experience = {
    #     'observation': observation,
    #     'agent_pos': self.environment.agent_pos,
    #     'agent_dir': self.environment.agent_dir,
    #     'value': start_value,
    #     'action': action,
    #     'next_observation': next_observation,
    #     'next_value': reward if done else next_value,
    #     'done': done,
    #     'reward': reward
    # }


def adjust_params(params, experience, learning_rate, error, visibility):
    [gx, gy] = goal_step_distance(
        experience['observation']['image'], experience['agent_pos'][0], experience['agent_pos'][1], experience['agent_dir'], visibility)
    [f, r, b, l] = walls_distance(experience['observation']['image'], experience['agent_pos']
                                  [0], experience['agent_pos'][1], experience['agent_dir'], visibility)
    x = [gx, gy, f, r, 1]
    print('gx, gy ---', gx, gy)
    # gf,gr,gl   front,right,left -> orden de parametros
    norm = 0
    for i in range(len(x)):
        params[i] = params[i] + learning_rate*error*x[i]
        norm += params[i]**2  # allows params to be within [-1,1]

    norm = math.sqrt(norm)

    # avoid overflow in params
    for i in range(len(x)):
        params[i] = params[i]/norm

    return params
