import json
import csv
import shapesAndLocations
import math
import cairo
import sys
from scipy.stats import truncnorm
import numpy as np

#some overall parameters
window_size = 800 # mid point is (256,256)
landmark_size = 80
trajector_size = 30

x_coordinate_landmark_1 = window_size / 4
y_coordinate_landmark_1 = window_size / 4 
x_coordinate_landmark_2 = window_size / 4 * 3
y_coordinate_landmark_2 = window_size / 4 * 3

radius_mean = 200
radius_std = 25
radius_upper = 250
radius_lower = 175

#create dict with relevant data
def create_dict(line):
    line_string = ";".join(str(x) for x in line)
    line_cells = line_string.split(";")
    return {"item": line_cells[0],
        "sentence": line_cells[1],
        "landmark_color_1": line_cells[2],
        "trajector_color_1": line_cells[3],
        "landmark_color_2": line_cells[4],
        "trajector_color_2": line_cells[5],
        "reference_trajector_1": line_cells[6],
        "second_trajector": line_cells[7],
        "reference_trajector_2": line_cells[8],
        'list': line_cells[9],
        "verb": line_cells[10],
        "landmark_form": line_cells[11],
        "trajector_form": line_cells[12],
        "second_landmark": line_cells[13],
        "condition": line_cells[14],
        "rotation_number": line_cells[15],
        "prep": line_cells[16],
        'trajector_degree_1' : sample_data(my_mean = 0, my_std = 45, myclip_a = -45, myclip_b = 45, size = 1),
        'trajector_radius_1' : sample_data(my_mean = radius_mean, my_std = radius_std, myclip_a = radius_lower, myclip_b = radius_upper, size = 1),
        'trajector_degree_2' : sample_data(my_mean = 0, my_std = 45, myclip_a = -45, myclip_b = 45, size = 1),
        'trajector_radius_2' : sample_data(my_mean = radius_mean, my_std = radius_std, myclip_a = radius_lower, myclip_b = radius_upper, size = 1),
        'question': '???'
        }



#sample relevant data with truncnorm distribution
def sample_data(my_mean,my_std,myclip_a,myclip_b,size):
    a, b = (myclip_a - my_mean) / my_std, (myclip_b - my_mean) / my_std
    r = float(truncnorm.rvs(a, b, loc = my_mean, scale = my_std, size = size))
    return r


#calculate x and y coordinate of trajector(s)
def trajector_position(degree, radius, reference_object):
    if reference_object == "1":
        x_coordinate = x_coordinate_landmark_1 + radius* math.cos(math.pi/180*(degree-45)) 
        y_coordinate = y_coordinate_landmark_1 - radius* math.sin(math.pi/180*(degree-45)) 
    elif reference_object == "2":
        x_coordinate = x_coordinate_landmark_2 + radius* math.cos(math.pi/180*(degree+135)) 
        y_coordinate = y_coordinate_landmark_2 - radius* math.sin(math.pi/180*(degree+135))
    return x_coordinate,y_coordinate

def overlap_control(trajector_size, x_1, y_1, x_2, y_2):
    # take trajector_size (radius of trajector) as a quadrat
    # compute this quadrat of first trajector first
    x_upper = x_1 + trajector_size
    x_lower = x_1 - trajector_size
    y_upper = y_1 + trajector_size
    y_lower = y_1 - trajector_size
    # change to 2 * trajector_size to completely avoid overlapping

    if (x_2 < x_upper and x_2 > x_lower) and (y_2 < y_upper and y_2 > y_lower):
        return False

def determine_landmark_form(landmark_form):
    if landmark_form == "Dreieck":
        return shapesAndLocations.Triangle
    else: 
        return shapesAndLocations.Landmark

def determine_trajector_form(trajector_form):
    if trajector_form == "Kreuz":
        return shapesAndLocations.Cross
    elif trajector_form == "Stern":
        return shapesAndLocations.Star
    elif trajector_form == "Kreis":
        return shapesAndLocations.Circle

def rotate(point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = (400,400)
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def extents(cx, cy, cr):
        return (cx - cr, cy - cr, cx + cr, cy + cr)

def generate_experiment_stimuli(source_file = "all_stimuli_with_sentences.csv", output_file = "all_stimuli_output_final.csv", practice = False):
    #read csv file as df
    with open(source_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        #skip header
        next(reader, None)
        stimuli_file = list(reader)

    #create list of dicts for each extracted line
    trial_dicts_list = list(map(create_dict, stimuli_file))



    for t in trial_dicts_list:
        # Define the output file location
        filename = "web/pictures/" + "pic-list-" + t["list"] + "-item-" + t["item"] + "-cond-" + t["condition"] + ".svg"

        # Define the colors and forms of the objects
        landmark_color_1 = t["landmark_color_1"]
        trajector_color_1 = t["trajector_color_1"]
        landmark_color_2 = t["landmark_color_2"]
        trajector_color_2 = t["trajector_color_2"]
        second_trajector = t["second_trajector"]
        second_landmark = t["second_landmark"]
        landmark_form = t["landmark_form"]
        trajector_form = t["trajector_form"]
        rotation_number = t["rotation_number"]


        #print(rotation_number)
        #print(type(rotation_number))
        if rotation_number == "0":
            rotation = 0
        elif rotation_number == "1":
            rotation = math.pi / 2
        elif rotation_number == "2":
            rotation = math.pi
        elif rotation_number == "3":
            rotation = math.pi / 2 * 3

        # Determine x,y coordinates for two landmarks
        x_coordinate_landmark_1_rotated, y_coordinate_landmark_1_rotated = rotate((x_coordinate_landmark_1, y_coordinate_landmark_1), rotation)
        x_coordinate_landmark_2_rotated, y_coordinate_landmark_2_rotated = rotate((x_coordinate_landmark_2, y_coordinate_landmark_2), rotation)

        trajector_degree_1 = sample_data(my_mean = 0, my_std = 45, myclip_a = -45, myclip_b = 45, size = 1)
        trajector_radius_1 = sample_data(my_mean = radius_mean, my_std = radius_std, myclip_a = radius_lower, myclip_b = radius_upper, size = 1)
        trajector_position_1 = trajector_position(trajector_degree_1,trajector_radius_1, t['reference_trajector_1'])
        trajector_position_1_rotated = rotate((trajector_position_1[0], trajector_position_1[1]), rotation)

        if trajector_form == "Stern":
            extents_trajector_1 = extents(trajector_position_1_rotated[0],trajector_position_1_rotated[1],100)
        else:
            extents_trajector_1 = extents(trajector_position_1_rotated[0],trajector_position_1_rotated[1],60)
        
        overlap = True
        while overlap:
            trajector_degree_2 = sample_data(my_mean = 0, my_std = 45, myclip_a = -45, myclip_b = 45, size = 1)
            trajector_radius_2 = sample_data(my_mean = radius_mean, my_std = radius_std, myclip_a = radius_lower, myclip_b = radius_upper, size = 1)
            trajector_position_2 = trajector_position(trajector_degree_2,trajector_radius_2, t['reference_trajector_1'])
            trajector_position_2_rotated = rotate((trajector_position_2[0], trajector_position_2[1]), rotation)
            x1,y1,x2,y2 = extents_trajector_1
            #print(extents_trajector_1)
            if (x1 < trajector_position_2_rotated[0]) & (trajector_position_2_rotated[0] < x2) & (y1 < trajector_position_2_rotated[1]) & (y2 > trajector_position_2_rotated[1]):
                overlap = True
            else:
                overlap = False

        t["trajector_degree_1"] = trajector_degree_1
        t["trajector_radius_1"] = trajector_radius_1
        t["trajector_degree_2"] = trajector_degree_2
        t["trajector_radius_2"] = trajector_radius_2

        # Draw the background
        s = cairo.SVGSurface(filename, window_size, window_size)
        c = cairo.Context(s)
        
        c.set_source_rgb(0.9, 0.9, 0.9)
        c.rectangle(0, 0, window_size, window_size)
        c.fill()
        
        # TODO: Randomize positions of landmark
        # Draw the first landmark
        tmp = determine_landmark_form(landmark_form)(c, x_coordinate_landmark_1_rotated, y_coordinate_landmark_1_rotated, landmark_size, landmark_color_1)
        tmp.draw()

        # Draw the second landmark if necessary
        if second_landmark == "Y":
            tmp = determine_landmark_form(landmark_form)(c, x_coordinate_landmark_2_rotated, y_coordinate_landmark_2_rotated, landmark_size, landmark_color_2)
            tmp.draw()


        # Draw the first trajector
        
        tmp = determine_trajector_form(trajector_form)(c, trajector_position_1_rotated[0], trajector_position_1_rotated[1], trajector_size, trajector_color_1)
        tmp.draw()


        # Draw the second trajector if necessary
        if second_trajector == "Y":
            tmp = determine_trajector_form(trajector_form)(c, trajector_position_2_rotated[0], trajector_position_2_rotated[1], trajector_size, trajector_color_2)
            tmp.draw()

        s.finish()

    keys = trial_dicts_list[0].keys()
    with open(output_file, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(trial_dicts_list)
    
    trials = json.dumps(trial_dicts_list, ensure_ascii=False)
    #trials = trials.encode('utf8')
    if practice:
        out = "const trainingtrials =" + trials
        out = out.encode('utf8')
        #save file as practice.js
        f = open("web/js/practice.js","wb")
        f.write(out)
        f.close()
    else:
        out = "const maintrials ="+trials
        out = out.encode('utf8')
        #save file as stimuli.js
        f = open("web/js/stimuli.js","wb")
        f.write(out)
        f.close()

def main():
    # Set seed for reproducibility
    # The seed used for the experiment was 1
    np.random.seed(1)

    # Generate sentences for the practice trials
    generate_experiment_stimuli(source_file="all_practice_stimuli_with_sentences.csv", output_file="all_practice_stimuli_final.csv", practice=True)
    
    # Generate sentences for the experiment trials
    generate_experiment_stimuli(source_file="all_stimuli_with_sentences.csv", output_file="all_stimuli_final.csv")
    

if __name__=='__main__':
    main()

