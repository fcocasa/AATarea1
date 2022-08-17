def matrix_value(i, j, matrix):  # USES X,Y NOTATION
    return matrix[j][i][2]


def goal_distance(observation, agent_pos_x, agent_pos_y):
    l = len(observation)
    for i in range(0, l):
        for j in range(0, l):
            if matrix_value(i, j, observation) == 8:
                return [abs(i-agent_pos_x), abs(j-agent_pos_y)]

# [wall_east,wall_south,wall_west,wall_north]


def _walls_axis(observation, agent_pos_x, agent_pos_y):
    l = len(observation)
    wall = []
    curiosity = 3
    for i in range(agent_pos_x, l):
        if matrix_value(i, agent_pos_y, observation) == 2 or matrix_value(i, agent_pos_y, observation) == 9:  # wall or lava
            wall.append(i-agent_pos_x)
            break
        # unseen # TODO: check var curiosity
        elif matrix_value(i, agent_pos_y, observation) == 0:
            wall.append(i-agent_pos_x + curiosity)
            break
    for j in range(agent_pos_y, l):
        if matrix_value(agent_pos_x, j, observation) == 2 or matrix_value(i, agent_pos_y, observation) == 9:  # wall or lava
            wall.append(j-agent_pos_y)
            break
        elif matrix_value(agent_pos_x, j, observation) == 0:  # unseen
            wall.append(j-agent_pos_y + curiosity)
            break

    for i in range(agent_pos_x, -1, -1):
        if matrix_value(i, agent_pos_y, observation) == 2 or matrix_value(i, agent_pos_y, observation) == 9:  # wall or lava
            wall.append(agent_pos_x-i)
            break
        elif matrix_value(i, agent_pos_y, observation) == 0:  # unseen
            wall.append(agent_pos_x-i + curiosity)
            break

    for j in range(agent_pos_y, -1, -1):
        if matrix_value(agent_pos_x, j, observation) == 2 or matrix_value(agent_pos_x, j, observation) == 9:  # wall or lava
            wall.append(agent_pos_y-j)
            break
        elif matrix_value(agent_pos_x, j, observation) == 0:  # unseen
            wall.append(agent_pos_y-j + curiosity)
            break

    return wall


# calcula la distancia a cada parede segun su sentido de la orietacion
# world -> obs['image'] invertido
def walls_distance(observation, agent_pos_x, agent_pos_y, agent_dir):
    walls = _walls_axis(observation, agent_pos_x, agent_pos_y)
    wall_dirs = []
    for i in range(agent_dir, agent_dir+4):
        wall_dirs.append(walls[i % 4])
    # print(walls)#(este, sur, oeste, norte)
    return wall_dirs  # (frente,derecha,atras,izquierda)
