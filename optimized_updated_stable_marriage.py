# Importing the necessary module
import time

# Start time measurement
start = time.time()

# Function to find the man in the current stable matching
def find_man(stable_matching, new_woman):
    """
    Find the man associated with a given woman in the current stable matching.

    Args:
    - stable_matching (dict): Dictionary representing the current stable matching.
    - new_woman (str): Woman for whom to find the associated man.

    Returns:
    - str or None: The man associated with the given woman, or None if not found.
    """
    for m in stable_matching.keys():
        if stable_matching[m] == new_woman:
            return m
    return None

# Function to update the stable matching
def update_stable_matching(current_m_pref, current_w_pref, prev_m_pref, prev_w_pref, stable_matching):
    """
    Update the stable matching based on changes in preference lists.

    Args:
    - current_m_pref (dict): Current preference lists of men.
    - current_w_pref (dict): Current preference lists of women.
    - prev_m_pref (dict): Previous preference lists of men.
    - prev_w_pref (dict): Previous preference lists of women.
    - stable_matching (dict): Current stable matching.

    Returns:
    - dict: Updated stable matching.
    """
    removed_pairs = []
    potential_blocking_pairs = []

    # Check for changes in men's preferences (MALE OPTIMAL) 
    for man, woman in stable_matching.items():
        if current_m_pref[man] != prev_m_pref[man]:
            for prev_woman in prev_m_pref[man]:
                if prev_m_pref[man].index(woman) < prev_m_pref[man].index(prev_woman):
                    potential_blocking_pairs.append(prev_woman)

            for new_woman in current_m_pref[man]:
                if new_woman == stable_matching[man]: #OPTIMIZATION USING THEOREM 1
                    break
                if new_woman in potential_blocking_pairs:
                    if current_w_pref[new_woman].index(man) < current_w_pref[new_woman].index(find_man(stable_matching, new_woman)):
                        removed_pairs.append((man, woman))

    # Check for changes in women's preferences (WOMEN OPTIMAL)
    for man, woman in stable_matching.items():
        if current_w_pref[woman] != prev_w_pref[woman]:
            for prev_man in prev_w_pref[woman]:
                if prev_w_pref[woman].index(man) < prev_w_pref[woman].index(prev_man):
                    potential_blocking_pairs.append(prev_man)

            for new_man in current_w_pref[woman]:
                if new_man == find_man(stable_matching, woman): #OPTIMIZATION USING THEOREM 1
                    break
                if new_man in potential_blocking_pairs:
                    if current_m_pref[new_man].index(woman) < current_m_pref[new_man].index(stable_matching[new_man]):
                        removed_pairs.append((man, woman))

    # Update stable matching by removing the pairs
    for pair in removed_pairs:
        del stable_matching[pair[0]]

    # Create a list of members already in the stable matching
    room_member = []
    for k in stable_matching.keys():
        room_member.append(k)
    for v in stable_matching.values():
        room_member.append(v)
    # Create a list of members removed from the stable matching
    queue_member  = [e for pair in removed_pairs for e in pair]
    # Copy the stable matching to be updated
    M = stable_matching.copy()
    # Iterate over the members removed from the stable matching
    for qm in queue_member:
        # Add the removed member to the list of members already in the stable matching
        room_member.append(qm)
        # Call the path_to_stability function to reestablish stability
        M = path_to_stability(current_m_pref, current_w_pref, M, qm, room_member)
    return M

# Function to reestablish stability
def path_to_stability(man_prefers, woman_prefers, M, new_member, room_member):
    """
    Reestablish stability in the matching by finding suitable replacements for members removed from the stable matching.

    Args:
    - man_prefers (dict): Preference lists of men.
    - woman_prefers (dict): Preference lists of women.
    - M (dict): Current stable matching without any blocking pairs.
    - new_member (str): Member to be reintroduced into the stable matching.
    - room_member (list): List of members already in the stable matching.

    Returns:
    - dict: Updated stable matching.
    """
    free_member = [new_member]
    while free_member:
        proposer = free_member.pop(0)
        if proposer[0] == 'w':
            woman_list = woman_prefers[proposer]
            for man in woman_list:
                if man in room_member:
                    man_list = man_prefers[man]
                    man_fiance = M[man]
                    if man_list.index(proposer) < man_list.index(man_fiance):
                        free_member.append(man_fiance)
                        M[man] = proposer
                        break
                else:
                    M[man] = proposer                    
                    break
        else:
            man_list = man_prefers[proposer]
            for woman in man_list:
                if woman in room_member:
                    woman_list = woman_prefers[woman]
                    woman_fiance = find_man(M,woman)
                    if woman_list.index(proposer) < woman_list.index(woman_fiance):
                        free_member.append(woman_fiance)
                        M[proposer] = woman
                        break
                else:
                    M[proposer] = woman
                    break
    return M

# Hard coded input for quick testing:-
# current_m_pref ={
#     'm1': ['w4', 'w1', 'w2', 'w3'],
#     'm2': ['w2', 'w1', 'w3', 'w4'],
#     'm3': ['w3', 'w1', 'w2', 'w4'],
#     'm4': ['w4', 'w1', 'w2', 'w3']
# }

# current_w_pref = {
#     'w1': ['m1', 'm2', 'm3', 'm4'],
#     'w2': ['m2', 'm1', 'm3', 'm4'],
#     'w3': ['m3', 'm1', 'm2', 'm4'],
#     'w4': ['m1', 'm4', 'm2', 'm3']
# }

# prev_m_pref = {
#     'm1': ['w1', 'w2', 'w3', 'w4'],
#     'm2': ['w2', 'w1', 'w3', 'w4'],
#     'm3': ['w3', 'w1', 'w2', 'w4'],
#     'm4': ['w4', 'w1', 'w2', 'w3']
# }

# prev_w_pref = {
#     'w1': ['m1', 'm2', 'm3', 'm4'],
#     'w2': ['m2', 'm1', 'm3', 'm4'],
#     'w3': ['m3', 'm1', 'm2', 'm4'],
#     'w4': ['m1', 'm4', 'm2', 'm3']
# }

# stable_matching = {'m1': 'w1', 'm2': 'w2', 'm3': 'w3', 'm4': 'w4'}

def take_preference_input():
    """
    Take user input for preference lists.

    Returns:
    - dict: Dictionary representing preference lists.
    """
    pref_dict = {}
    num_people = int(input("Enter the number of people: "))
    for i in range(1, num_people + 1):
        person_name = input(f"Enter the name of person {i}: ")
        pref_list = input(f"Enter the preference list for {person_name} separated by commas: ").split(',')
        pref_dict[person_name] = pref_list
    return pref_dict

# Function to take user input for stable matching
def take_stable_matching_input():
    """
    Take user input for stable matching.

    Returns:
    - dict: Dictionary representing the stable matching.
    """
    stable_matching = {}
    num_pairs = int(input("Enter the number of pairs in the stable matching: "))
    for i in range(1, num_pairs + 1):
        person1 = input(f"Enter the name of person {i}: ")
        person2 = input(f"Enter the name of the partner for {person1}: ")
        stable_matching[person1] = person2
    return stable_matching

# Take user input for previous preference lists and stable matching
print("enter previous preferences of males")
prev_m_pref = take_preference_input()
print("enter previous preferences of females")
prev_w_pref = take_preference_input()
print("enter current preferences of males")
current_m_pref = take_preference_input()
print("enter current preferences of females")
current_w_pref = take_preference_input()
print("enter initial stable matches")
stable_matching = take_stable_matching_input()


c = int(input("Enter the number of instances to take as input: "))
while c>0:
    # Update the stable matching
    updated_stable_matching = update_stable_matching(current_m_pref, current_w_pref, prev_m_pref, prev_w_pref, stable_matching)

        # Print the updated stable matching
    print("Updated stable matching:", updated_stable_matching)

    prev_m_pref = current_m_pref.copy()
    prev_w_pref = current_w_pref.copy()
    print("enter current preferences of males")
    current_m_pref = take_preference_input()
    print("enter current preferences of females")
    current_w_pref = take_preference_input()
    c-=1

end = time.time()
print(f"Total elapsed time: {end-start}")