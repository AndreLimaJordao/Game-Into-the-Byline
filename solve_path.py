from pyamaze import maze

def solve_path(start_coord_tuple, end_coord_tuple, m):
    start = start_coord_tuple
    end = end_coord_tuple
    possibles = [start]
    got_into = [start]
    bfs_solved_path_rev = {}
    rep = True
    while len(possibles) > 0 and rep:
        current_space = possibles.pop(0)
        if current_space == end:
            rep = False
        else:
            for d in 'EWSN':
                if m[current_space][d]:
                    if d == 'W':
                        sub_space = (current_space[0],current_space[1]-1)
                    elif d == 'E':
                        sub_space = (current_space[0],current_space[1]+1)
                    elif d == 'N':
                        sub_space = (current_space[0]-1,current_space[1])
                    else:
                        sub_space = (current_space[0]+1,current_space[1])
                    if sub_space in got_into: continue
                    possibles.append(sub_space)
                    got_into.append(sub_space)
                    bfs_solved_path_rev[sub_space]=current_space
    path = {}
    cell = end
    while cell != start:
        path[bfs_solved_path_rev[cell]] = cell
        cell = bfs_solved_path_rev[cell]
    return path
