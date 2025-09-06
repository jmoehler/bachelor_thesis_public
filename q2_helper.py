# ===================================================
#                      Helper Functions
# ===================================================

# 1. neighbour_checker:
#    - Checks if there are two same movements in a row and merges them.

# 2. find_index_of_fall:
#    - Finds the index of fall events and maps them to corresponding movements
#      (corresponding department).

# 3. condense_falls:
#    - Condenses the fall events, so that there are no multiple fall events 
#      in a row before a movement.

# 4. fall_integrator:
#    - Integrates the fall events into the movements and returns a list with 
#      the movements and fall events combined.

# 5. fall_scope_filter:
#    - Filters the movements and fall events based on the given scope before
#      and after the fall event.

# ******************** NOT USED *********************
# loop_checker:
#    - Checks if there are loops in the movements and deletes them.
#    - Maps the fall events to the last occurrence of the element before the loop.



import numpy as np


debug = False

#delete neighbours in movements
def neighbours_checker(data):

    # get movement and from and till time
    in_movement = data['movement']
    in_from_time = data['from_time']
    in_till_time = data['till_time']

    #init current pos and max pos
    cur_pos=1
    max_pos =len(in_movement)-1

    # init new out strings with the first element in already
    out_movement =[in_movement[0]]
    out_from_time = [in_from_time[0]]
    out_till_time = [in_till_time[0]]

    # go through all elements and check if current is equal to last, if so skip but  change till time (increase)
    # else append element with from and till time
    while cur_pos<=max_pos:
        if in_movement[cur_pos] != out_movement[-1]:
            out_movement.append(in_movement[cur_pos])
            out_from_time.append(in_from_time[cur_pos])
            out_till_time.append(in_till_time[cur_pos])
        else:
            out_till_time[-1] = in_till_time[cur_pos]

        cur_pos +=1

    #prepare output
    out = data.copy()
    out['movement'] = out_movement
    out['from_time'] = out_from_time
    out['till_time'] = out_till_time

    return out


# find index of fall
def find_index_of_fall(data):
    from_times = data['from_time']
    fall_times = data['fall_time']
    movement = data['movement']
    fall_department = data['fall_department']

    if debug:
        print('---------------')
        print(data['c_pseudonym'])


    fall_index = []

    for fall_time in fall_times:
        last_index = -1

        for i, from_time in enumerate(from_times):
            if from_time < fall_time:
                last_index = i
                continue
        

        cur_fall_dep = fall_department[fall_times.index(fall_time)]
        if debug:
            print('**')
            print('cur_fall_dep: ', cur_fall_dep)
            print('last_index: ', last_index)
            print('movement[last_index]: ', movement[last_index])
        while movement[last_index] != cur_fall_dep:
            if debug: print('not equal')
            last_index -= 1
            if last_index < 0:
                if debug: print('found no match, breaking loop, setting last_index to NaN')
                last_index = 'NaN'
                break
        
        # if there is a NaN, break the loop and return NaN
        if last_index == 'NaN':
            fall_index = 'NaN'
            break
        else:
            fall_index.append(last_index)
    
    return fall_index


# condense falls
def condense_falls(data):

    in_fall_department = data['fall_department']
    in_fall_time = data['fall_time']
    in_index_of_fall = data['index_of_fall']
    in_injury_grade = data['injury_grade']

    if debug:
        print('---------------')
        print(data['c_pseudonym'])

    # If there are no fall events, return the data as is
    if in_index_of_fall == 'NaN':
        return data

    out_fall_department = []
    out_fall_time = []
    out_index_of_fall = []
    out_injury_grade = []

    start = 0
    current_index = in_index_of_fall[0]

    if debug:
        print("Initial values:")
        print(f"in_fall_department: {in_fall_department}")
        print(f"in_fall_time: {in_fall_time}")
        print(f"in_index_of_fall: {in_index_of_fall}")

    for i in range(0, len(in_index_of_fall)):
        
        if debug: print('current index: ', current_index)

        # if the index of fall is different from the current index, append the values
        if in_index_of_fall[i] != current_index:
            if debug: print(f"Appending: {in_fall_department[start]}, {in_fall_time[start]}, {in_index_of_fall[start]}")
            out_fall_department.append(in_fall_department[start])
            out_fall_time.append(in_fall_time[start])
            out_index_of_fall.append(in_index_of_fall[start])
            out_injury_grade.append(in_injury_grade[start])

            current_index = in_index_of_fall[i]
            start = i

        if i == len(in_index_of_fall)-1:
            # Append the last set of values
            if debug: print(f"Appending last set: {in_fall_department[start]}, {in_fall_time[start]}, {in_index_of_fall[start]}")
            out_fall_department.append(in_fall_department[start])
            out_fall_time.append(in_fall_time[start])
            out_index_of_fall.append(in_index_of_fall[start])
            out_injury_grade.append(in_injury_grade[start])


        # if the injury grade is higher, update the injury grade  
        

        if len(out_injury_grade)>0 and in_injury_grade[i]>out_injury_grade[-1]:

            if debug: print(f"Checking injury grade: {in_injury_grade[i]} > {out_injury_grade[-1]}")

            out_injury_grade[-1] = in_injury_grade[i]

    out = data.copy()
    out['fall_department'] = out_fall_department
    out['fall_time'] = out_fall_time
    out['index_of_fall'] = out_index_of_fall
    out['injury_grade'] = out_injury_grade

    if debug:
        print("Final output:")
        print(f"out_fall_department: {out_fall_department}")
        print(f"out_fall_time: {out_fall_time}")
        print(f"out_index_of_fall: {out_index_of_fall}")

    return out

# integrate falls
def fall_integrator(data):

    # Extracting the relevant data from the input dictionary
    departments = data['movement'] 
    index_of_fall = data['index_of_fall'] 
    fall_department = data['fall_department'] 

    deps_and_falls = []  # Initialize an empty list to store departments and fall markers

    # Iterate through the list of department movements
    for dep_it, curr_dep in enumerate(departments):
        if debug: 
            print('current dep: ', curr_dep, '; index: ', dep_it)  

        deps_and_falls.append(curr_dep) 

        # Check if the current index is in the list of fall indices
        if dep_it in index_of_fall:
            # Get the corresponding fall index from index_of_fall
            fall_index = index_of_fall.index(dep_it)
            # Create the fall marker string
            fall_add = '#FALL_' + fall_department[fall_index] + '#'
            # Append the fall marker to the list
            deps_and_falls.append(fall_add)
        

            if debug: 
                print('appending fall') 

    return deps_and_falls


# filter movements based on scope before and after fall event
def fall_scope_filter(in_dep_and_falls, filter_element, sc_before, sc_after):


    # since we always want to include the element before the fall, we need to increase the scope
    # of sc_before by 1 if the filter element is a fall event
    if filter_element[0] == '#':
        sc_before += 1

    out_dep_and_falls = [] # Output list to store filtered events
    filter_index = [i for i, x in enumerate(in_dep_and_falls) if x == filter_element]
    filter_index_add_range = []

    if debug:
        print('##################')
        print('in_dep_and_falls: ', in_dep_and_falls)
        print('filter_element: ', filter_element)
        print('sc_before: ', sc_before)
        print('sc_after: ', sc_after)
        print('filter_index: ', filter_index)
        print('len(in_dep_and_falls): ', len(in_dep_and_falls))
        print('##################')


    # Extend indices by scope ranges
    for index in filter_index:
        sc_before_temp = sc_before
        sc_after_temp = sc_after
        filter_index_add_range.append(index)
        index_temp = index


        # Add indices within scope before the fall event
        while sc_before_temp > 0 and index_temp > 0:
            sc_before_temp -= 1
            index_temp -= 1
            filter_index_add_range.append(index_temp)


        index_temp = index

        # Add indices within scope after the fall event
        while sc_after_temp > 0 and index_temp < len(in_dep_and_falls) - 1:
            sc_after_temp -= 1
            index_temp += 1
            filter_index_add_range.append(index_temp)


    # Remove duplicates and sort the indices
    filter_index_add_range = [elem for elem in filter_index_add_range if (elem >= 0 and elem < len(in_dep_and_falls))]
    filter_index_add_range = list(set(filter_index_add_range))
    filter_index_add_range.sort()

    dot_count = 0


    # Process the filtered indices to construct the output list
    for i, cur_ind in enumerate(filter_index_add_range):
        if debug: 
            print('---------------')
            print('i: ', i)
            print('cur_ind: ', cur_ind)
            print('dot_count: ', dot_count)

        if cur_ind in filter_index:
            dot_count += 1

        gap = None
        cur_el = in_dep_and_falls[cur_ind]

        if debug: print('cur_el: ', cur_el)

        is_fall = cur_el[0] == '#'

        def dot_el(num):
            if debug: print('using dot')
            return '(' + str(num) + ')'

        if i != 0:
            gap = cur_ind - filter_index_add_range[i - 1]

        if debug:
            print('gap: ', gap)
            print('is_fall: ', is_fall)
            print('**')


        if i == 0:
            if debug: print('i == 0 -> first element')
            if cur_ind > 0:
                if is_fall:
                    if debug: print('is fall')
                    if cur_ind > 1:
                        if debug: print('cur_ind > 1')
                        
                        out_dep_and_falls.append(dot_el(dot_count))
                    out_dep_and_falls.append(in_dep_and_falls[cur_ind - 1])
                    out_dep_and_falls.append(cur_el)
                else:
                    if debug: print('not fall')
                    
                    out_dep_and_falls.append(dot_el(dot_count))
                    out_dep_and_falls.append(cur_el)
                    print(out_dep_and_falls)
            else:
                if debug: print('cur_ind == 0')
                out_dep_and_falls.append(cur_el)
            

        if i!=0 and gap is not None and gap > 1:
            if debug: print('gap not None and > 1')
            if is_fall:
                if debug: print('is fall')
                if gap > 2:
                    if debug: print('gap > 2')

                    
                    out_dep_and_falls.append(dot_el(dot_count))
                out_dep_and_falls.append(in_dep_and_falls[cur_ind - 1])
                out_dep_and_falls.append(cur_el)
            else:
                if debug: print('not fall')
                
                out_dep_and_falls.append(dot_el(dot_count))
                out_dep_and_falls.append(cur_el)
        elif i!=0:
            if debug: print('gap is None or <= 1')
            out_dep_and_falls.append(cur_el)

        if i == len(filter_index_add_range) - 1:
            
            if debug: print('last element')
            if len(in_dep_and_falls) - 1 > cur_ind:
                if debug: print('more elements after')
                out_dep_and_falls.append(dot_el(dot_count))

    return out_dep_and_falls





# set all severities of fall at point of interest
def find_fall_severities(data, point_of_interest):
    fall_dep = data['fall_department']
    fall_injury = data['injury_grade']
    fall_injury_severities = []
    
    for i, dep in enumerate(fall_dep):
        if dep == point_of_interest:
            if fall_injury[i] not in fall_injury_severities:
                fall_injury_severities.append(fall_injury[i])
                
    return fall_injury_severities
 
    



# builds tuples for visualisation
def tuple_builder(moves):
    tuples =[]
    for i, move in enumerate(moves):
        if i==0: continue
        t = (moves[i-1],move)
        tuples.append(t)
    return tuples



def only_first_falls(departments, point_of_interest):
    out = []

    for i, dep in enumerate(departments):
        if dep == point_of_interest:
            out.append(dep)
            if i+1 < len(departments):
                out.append('(1)')
            break
        else:
            out.append(dep)

    return out








# ----------------- NOT USED -----------------

# not needed currently (not sure if correct)
# delete multible loops in movements
def loop_checker(data):
    line_01 = data
    line_02 = __loop_checker_helper__(data)


    while len(line_01) != len(line_02):
        line_01 =line_02
        line_02 = __loop_checker_helper__(line_02)

    return line_02

# does the job
def __loop_checker_helper__(data):

    # init inputs
    in_movement = data['movement'].copy()
    fall_index = data['index_of_fall']

    #init current pos and max pos
    cur_pos=0
    max_pos =len(in_movement)-1

    # init outputs
    out_movement = []


    # loop checker
    while cur_pos<=max_pos:
        # e0: current element
        # e1: next occurence of current element (by definition same as e1
        # cur_pos: position of current element
        # e1_i: index of e1



        e0 = in_movement[cur_pos]

        e1_i_list = np.where(np.array(out_movement) == e0)[0]
        e1_i = None
        if e1_i_list.size >0:
            e1_i = e1_i_list[-1]


        # if the current element did not occure before, just add it
        if e1_i is None:
            out_movement.append(e0)
            cur_pos +=1
            continue

        dist =  len(out_movement) -1 -e1_i

        #if the distance between last occurence to end ( dist) is bigger then the remaining elements in in_movements, just add it
        in_movement_remaining = len(in_movement)-1 - cur_pos

        if dist>in_movement_remaining:
            out_movement.append(e0)
            cur_pos +=1
            continue

        breaki = False
        rem_dist = dist
        #while there are still elements in bewtween and there has not been an element that is different
        while (rem_dist >0 and not breaki):
            # counts which element to look at
            count  = 1
            # position of e0 and forewards in in_movement
            pos_from_e0 = cur_pos + count
            # position of e2 and forewards in out_movement
            pos_from_e1 = e1_i + count
            
            # if an element is not the same -> no loop, append and set flag
            if in_movement[pos_from_e0] != out_movement[pos_from_e1]:
                out_movement.append(e0)
                breaki = True
                continue
            
            # else, jump over the elements by increasing the cur pos
            rem_dist -= 1
            if rem_dist==0:
                # if there are any fall events during a loop, they get mapped to the before iteration
                for i in range(0,len(fall_index)):
                    if fall_index[i] >= cur_pos and fall_index[i] <= cur_pos + dist:
                       fall_index[i] = fall_index[i] - dist-1
                cur_pos = cur_pos + dist

                # jump in in movement
        
        cur_pos +=1

    #prepare output
    out = data.copy()

    out['movement'] = out_movement
    out['index_of_fall'] = fall_index

    return out



        

