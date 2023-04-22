#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True


def _agent_dis_to_end(long [:,:,:] board_view, int agent_id, int board_size):
    cdef int pos_x, pos_y
    cdef int i, j
    cdef int cnt = 0, tail = 0
    cdef int there_x, there_y
    cdef int goal = (1-agent_id) * 8
    cdef int queue_x[81]
    cdef int queue_y[81]
    cdef int visited[81][81]
    cdef int directions[4][2]

    for i in range(9):
        for j in range(9):
            visited[i][j] = 0

    if agent_id:
        directions[0][:] = [0, -1]
        directions[1][:] = [1, 0]
        directions[2][:] = [-1, 0]
        directions[3][:] = [0, 1]
    else:
        directions[0][:] = [0, 1]
        directions[1][:] = [1, 0]
        directions[2][:] = [-1, 0]
        directions[3][:] = [0, -1]

    (pos_x, pos_y) = _agent_pos(board_view, agent_id, board_size)
    if pos_y == goal:   return 0

    queue_x[tail] = pos_x
    queue_y[tail] = pos_y
    tail += 1
    visited[pos_x][pos_y] = 1

    for i in range(board_size * board_size):
        if cnt == tail: break
        pos_x = queue_x[cnt]
        pos_y = queue_y[cnt]
        cnt += 1
        for j in range(4):
            there_x = pos_x + directions[j][0]
            there_y = pos_y + directions[j][1]
            if not (0 <= there_x < board_size and 0 <= there_y < board_size):
                continue
            if visited[there_x][there_y]:
                continue
            if _check_wall_blocked(board_view, pos_x, pos_y, there_x, there_y):
                continue
            if there_y == goal:
                return visited[pos_x][pos_y] + 1
            visited[there_x][there_y] = visited[pos_x][pos_y] + 1
            queue_x[tail] = there_x
            queue_y[tail] = there_y
            tail += 1

    return 0

cdef int _check_wall_blocked(long[:,:,:] board_view, int cx, int cy, int nx, int ny):
    cdef int i
    if nx > cx:
        for i in range(cx, nx):
            if board_view[3, i, cy]:
                return 1
        return 0
    if nx < cx:
        for i in range(nx, cx):
            if board_view[3, i, cy]:
                return 1
        return 0
    if ny > cy:
        for i in range(cy, ny):
            if board_view[2, cx, i]:
                return 1
        return 0
    if ny < cy:
        for i in range(ny, cy):
            if board_view[2, cx, i]:
                return 1
        return 0
    return 0

cdef (int, int) _agent_pos(long[:,:,:] board_view, int agent_id, int board_size):
    cdef int i, j
    for i in range(board_size):
        for j in range(board_size):
            if board_view[agent_id, i, j]:
                return (i, j)
    return (-1, -1)
