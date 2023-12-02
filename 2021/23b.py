from collections import deque
import heapq
import bisect

energy = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

amphipods = sorted(energy.keys())

def read_input():
    grid = []
    while True:
        try:
            row = input()
            grid.append(row)
        except EOFError:
            break
    return grid
        
def printgrid(grid):
    for row in grid:
        print(row)

def grid_to_state(grid):
    hallway = ["" if c == "." else None for c in grid[1]] # hallway[i] is None if wall and "" if empty space
    room_indexes = [] # x coordinate of room relative to hallway
    rooms = [] 
    for r in grid[2:]:
        index = 0
        for i, c in enumerate(r):
            if c in energy.keys():
                if len(room_indexes) <= index:
                    rooms.append([c])
                    room_indexes.append(i)
                else:
                    rooms[index].insert(0, c)
                index += 1
    
    return {
        "hallway": hallway, 
        "rooms": rooms,
        "room_indexes": room_indexes
    }
    
def copy_state(state):
    return {
        "hallway": list(state["hallway"]),
        "rooms": [list(room) for room in state["rooms"]],
        "room_indexes": state["room_indexes"],
        "cost": state["cost"],
        "num_invalid": state["num_invalid"],
        "num_moves": state["num_moves"]
    }
    
def insert(q, state):
    bisect.insort_left(q, state, key=lambda s: (1000-s["num_moves"], s["cost"], s["num_invalid"]))
    
def is_room_done(room_idx, room):
    for a in room:
        if a not in amphipods[room_idx]:
            return False
    return True
    
def is_done(state):
    for a in energy.keys():
        if a in state["hallway"]:
            return False
    
    for i, room in enumerate(state["rooms"]):
        if not is_room_done(i, room):
            return False

    return True
    
def count_invalid(state):
    count = 0
    for i, room in enumerate(state["rooms"]):
        for ia, a in enumerate(room):
            if a != amphipods[i]:
                count += len(room) - ia
                break
    for a in state["hallway"]:
        if a in amphipods:
            count += 1
    return count
       
def walk(state):
    """
    at any moment in time, the following actions may be possible:
    - move amphipod from room into hallway
        - cannot stop right outside of a room
    - move amphipod from hallway into room
        - can only move into final destination room
    """
    ROOM_SIZE = len(state["rooms"][0])
    amphipods = sorted(energy.keys())
    state["cost"] = 0
    state["num_invalid"] = count_invalid(state)
    state["num_moves"] = 0
    q = deque()
    insert(q, state)
    
    best_cost = None
    nodes_searched = 0
    PRINT_INTERVAL = 100000
    while True:
        state = q.popleft()
        nodes_searched += 1
        if is_done(state):
            if best_cost is None or state["cost"] < best_cost:
                best_cost = state["cost"]
                print(f">>> PB COST: {best_cost}")
                print(f">>> st: {state}")
            continue
        else:
            if best_cost is not None and state["cost"] > best_cost: # no point in continuing, F4 F4 F4
                continue
        
        if nodes_searched % PRINT_INTERVAL == 0:
            print(f"q={len(q)} {state}")
            
        # state change: move amphipod from hallway into room
        for i, a in enumerate(state["hallway"]):
            if a in amphipods:
                target_room_idx = amphipods.index(a)
                target_room_location = state["room_indexes"][target_room_idx]
                room = state["rooms"][target_room_idx]
                if len(room) == ROOM_SIZE: # can't move into room yet
                    # print("   target room is full")
                    continue
                else:
                    room_done = True
                    for a_room in room:
                        if a_room != a: # cannot move into room if other types of amphipods haven't moved out yet
                            room_done = False
                    if not room_done:
                        # print("   target room is not done")
                        continue
                        
                # check if any amphipods are blocking the way
                direction = 1 if target_room_location > i else -1
                idx = i
                path_clear = True
                # print(f"path check: start={idx}, direction={direction}, dest={target_room_location}")
                while idx != target_room_location:
                    idx += direction
                    if state["hallway"][idx] != "":
                        # print(f"...obstacle at idx={idx}!")
                        path_clear = False
                        break
                if not path_clear: # cannot enter the room
                    # print("   hallway path is not clear")
                    continue
                
                # can move into the room
                distance = abs(target_room_location - i) + (ROOM_SIZE - len(room))
                cost = energy[a] * distance
                
                new_state = copy_state(state)
                new_state["cost"] += cost
                new_state["rooms"][target_room_idx].append(a)                
                new_state["hallway"][i] = ""
                new_state["num_invalid"] = count_invalid(new_state)
                new_state["num_moves"] += 1
                
                insert(q, new_state)
        
        # state change: move amphipod into hallway
        for i, room in enumerate(state["rooms"]):
            if len(room) == 0: # do not move out empty room
                continue
            elif is_room_done(i, room): # do not move out of room if room is done
                continue
                
            distance = 1 + (ROOM_SIZE - len(room))
            a = room[-1]
            enter_idx = state["room_indexes"][i]
            
            # build list of stopping points
            stops = []
            idx = enter_idx-1
            while idx >= 0 and state["hallway"][idx] == "":
                if idx not in state["room_indexes"]: # cannot stop in front of a room
                    stops.append(idx)
                idx -= 1
            idx = enter_idx + 1
            while idx < len(state["hallway"]) and state["hallway"][idx] == "":
                if idx not in state["room_indexes"]: # cannot stop in front of a room
                    stops.append(idx)
                idx += 1
            
            # queue
            for stop in stops:
                total_distance = distance + abs(stop - enter_idx)
                cost = energy[a] * total_distance
                new_state = copy_state(state)
                new_state["cost"] += cost
                new_state["rooms"][i].pop()
                new_state["hallway"][stop] = a
                new_state["num_invalid"] = count_invalid(new_state)
                new_state["num_moves"] += 1
                
                insert(q, new_state)
        
grid = read_input()
printgrid(grid)

state = grid_to_state(grid)
print(f"state: {state}")

walk(state)
