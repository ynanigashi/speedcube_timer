import random

def generate_wca_cube_scramble(length=20):
    moves = ['F', 'B', 'U', 'D', 'L', 'R']
    modifiers = ['', "'", '2']
    
    axis_map = {'F': 'FB', 'B': 'FB', 'U': 'UD', 'D': 'UD', 'L': 'LR', 'R': 'LR'}

    scramble = []
    last_face = None
    last_axis = None  

    for _ in range(length):
        while True:
            face = random.choice(moves)
            axis = axis_map[face]
            
            if face == last_face:
                continue
            
            if len(scramble) >= 2 and axis == last_axis == axis_map[scramble[-2][0]]:
                continue

            break
        
        modifier = random.choice(modifiers)
        scramble.append(face + modifier)

        last_face = face
        last_axis = axis
    
    return ' '.join(scramble)