# implementation of posets.
# we use a dictionary as adjacency list, and go from there.

def poset(xs):
    return {x:[] for x in xs}

def poset_union(pos1, pos2):
    result = pos1.copy()
    for r in result:
        if r in pos2:
            result[r].append(pos2[r])
        else:
            result[r] = pos2[r]
    return result if not is_cyclic(result) else None

def is_cyclic(pos):
    return cyclic_helper(pos, None)

def cyclic_helper(pos, pvt, visited):
    if visited is None:
        return any(cyclic_helper(pos, [nxt]) for nxt in pos.keys())
    else:
        pvt = visited[0]
        for nxt in pos[pvt]:
            if nxt in visited:
                return True
            else:
                return cyclic_helper(pos,[nxt]+visited)
        return False
