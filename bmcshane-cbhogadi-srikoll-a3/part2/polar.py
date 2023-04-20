#!/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy as np
import copy

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)





# ideally calculates P(obseved column | any given hidden/actual state)
# look at Q&A board to make sure I'm doing this correctly
# each value represents the probability that the border is in that row
def emission_probabilities(observed_column, edge_column):
    ratios = edge_column/observed_column # basically a heuristic to score pixels, the higher the edge strength and lower (darker) pixel value, the higher the score
    return ratios/sum(ratios) # normalizes these scores to sum to 1 to feel like probabilities


def emission_probabilities_ir(observed_column, edge_column, ai_y):
    ratios = edge_column/observed_column 
    ratios[:ai_y+10] = 0 # entry needs to be 10 pixels lower than air_ice border, should this be 11?
    return ratios/sum(ratios) 

sigma = 5
def gaussian(prev_index, current_index):
    return (1/sigma*float(np.sqrt(2*np.pi)))*float(np.exp(-.5*(current_index-prev_index)**2))


# previous column should be a bunch of 0's and a 1
#def transition_probabilities(prev_column):
    #prev_index = np.argmax(prev_column) # finds the index of the 1 among a list of zeros (or index of highest probability)

    #transition_probabilities = np.zeros(len(prev_column))

    #for i in range(len(transition_probabilities)):
        #transition_probabilities[i] = gaussian(prev_index, i)

    #return transition_probabilities

def transition_probability(prev_index, current_index):
    return gaussian(prev_index, current_index)

def transition_probability_ir(prev_index, current_index, ai_y):
    if current_index >= ai_y+10:
        return gaussian(prev_index, current_index)
    else:
        return 0


def ai_simple(image_array, edge_array):
    y_vals = []
    for i in range(len(image_array[0])):
        observed_column = image_array[:,i]
        edge_column = edge_array[:,i]

        emissions = emission_probabilities(observed_column, edge_column)
        y_vals.append(np.argmax(emissions))

    return y_vals

def ir_simple(image_array, edge_array, ai_border):
    y_vals = []
    for i in range(len(image_array[0])):
        observed_column = image_array[:,i]
        edge_column = edge_array[:,i]

        emissions = emission_probabilities_ir(observed_column, edge_column, ai_border[i])
        y_vals.append(np.argmax(emissions)) # choosing the row index w highest probability

    return y_vals



def ai_hmm(image_array, edge_array):
    results = {}
    height = len(image_array)
    width = len(image_array[0])


    for current_col in range(width):
        results[current_col] = {}
        column = image_array[:,current_col]
        edge_col = edge_array[:,current_col]

        emissions = emission_probabilities(column, edge_col)


        for current_row_index in range(height):
            if current_col == 0:
                # priors for the first column are uniform
                results[current_col][current_row_index] = [[current_row_index], np.log(emissions[current_row_index])+np.log(1/len(column))]
            else:
                best_p = -np.inf
                best_partial_border = []

                for prev_row_index in range(height):
                    temp = results[current_col-1][prev_row_index]
                    partial_border = temp[0] # this is a NoneType here and there, investigate
                    p = temp[1]

                    probability = p + np.log(transition_probability(prev_row_index, current_row_index)) + np.log(emissions[current_row_index])

                    if probability > best_p:
                        best_p = probability
                        best_partial_border = copy.deepcopy(partial_border)
                
                best_partial_border.append(current_row_index)
                results[current_col][current_row_index] = [best_partial_border, best_p]

    best_p = -np.inf
    best_border = []


    for key in results[width-1].keys():
        ls = results[width-1][key]
        border = ls[0]
        prob = ls[1]

        if prob > best_p:
            best_p = prob
            best_border = border


    return best_border


def ir_hmm(image_array, edge_array, ai_border):
    results = {}
    height = len(image_array)
    width = len(image_array[0])


    for current_col in range(width):
        results[current_col] = {}
        column = image_array[:,current_col]
        edge_col = edge_array[:,current_col]
        ai_y = ai_border[current_col]


        emissions = emission_probabilities_ir(column, edge_col, ai_y)


        for current_row_index in range(height):
            if current_col == 0:
                # priors for the first column are uniform
                results[current_col][current_row_index] = [[current_row_index], np.log(emissions[current_row_index]) + np.log(1/len(column))]
            else:
                best_p = -np.inf
                best_partial_border = []

                for prev_row_index in range(height):
                    temp = results[current_col-1][prev_row_index]
                    partial_border = temp[0] # this is a NoneType here and there, investigate
                    p = temp[1]

                    probability = p + np.log(transition_probability_ir(prev_row_index, current_row_index, ai_y)) + np.log(emissions[current_row_index])

                    if probability > best_p:
                        best_p = probability
                        best_partial_border = copy.deepcopy(partial_border)
                
                best_partial_border.append(current_row_index) # bpb was referenced before assignment -> put in line under best_p=0
                results[current_col][current_row_index] = [best_partial_border, best_p]

    best_p = -np.inf
    best_border = []

    for key in results[width-1].keys():
        ls = results[width-1][key]
        border = ls[0]
        prob = ls[1]

        if prob > best_p:
            best_p = prob
            best_border = border

    return best_border


def ai_feedback(image_array, edge_array, air_coord):
    results = {}
    height = len(image_array)
    width = len(image_array[0])


    for current_col in range(width):
        results[current_col] = {}
        column = image_array[:,current_col]
        edge_col = edge_array[:,current_col]

        if current_col == air_coord[1]:
                emissions = np.zeros(height)
                emissions[air_coord] = 1
        else:
            emissions = emission_probabilities(column, edge_col)
        


        for current_row_index in range(height):
            if current_col == 0:
                # priors for the first column are uniform
                results[current_col][current_row_index] = [[current_row_index], np.log(emissions[current_row_index]) + np.log(1/len(column))]
            else:
                best_p = -np.inf
                best_partial_border = []

                for prev_row_index in range(height):
                    temp = results[current_col-1][prev_row_index]
                    partial_border = temp[0] # this is a NoneType here and there, investigate
                    p = temp[1]

                    probability = p + np.log(transition_probability(prev_row_index, current_row_index)) + np.log(emissions[current_row_index])

                    if probability > best_p:
                        best_p = probability
                        best_partial_border = copy.deepcopy(partial_border)
                
                best_partial_border.append(current_row_index)
                results[current_col][current_row_index] = [best_partial_border, best_p]

    best_p = -np.inf
    best_border = []


    for key in results[width-1].keys():
        ls = results[width-1][key]
        border = ls[0]
        prob = ls[1]

        if prob > best_p:
            best_p = prob
            best_border = border

    #return results
    return best_border # referenced before assignment


def ir_feedback(image_array, edge_array, ai_border, rock_coord):
    results = {}
    height = len(image_array)
    width = len(image_array[0])


    for current_col in range(width):
        results[current_col] = {}
        column = image_array[:,current_col]
        edge_col = edge_array[:,current_col]
        ai_y = ai_border[current_col]

        
        if current_col == rock_coord[1]:
            emissions = np.zeros(height)
            emissions[rock_coord[0]] = 1
        else:
            emissions = emission_probabilities_ir(column, edge_col, ai_y)


        for current_row_index in range(height):
            if current_col == 0:
                # priors for the first column are uniform
                results[current_col][current_row_index] = [[current_row_index], np.log(emissions[current_row_index]) + np.log(1/len(column))]
            else:
                best_p = -np.inf
                best_partial_border = []

                for prev_row_index in range(height):
                    temp = results[current_col-1][prev_row_index]
                    partial_border = temp[0] # this is a NoneType here and there, investigate
                    p = temp[1]

                    probability = p + np.log(transition_probability_ir(prev_row_index, current_row_index, ai_y)) + np.log(emissions[current_row_index])

                    if probability > best_p:
                        best_p = probability
                        best_partial_border = copy.deepcopy(partial_border)
                
                best_partial_border.append(current_row_index) # bpb was referenced before assignment -> put in line under best_p=0
                results[current_col][current_row_index] = [best_partial_border, best_p]

    best_p = -np.inf
    best_border = []

    for key in results[width-1].keys():
        ls = results[width-1][key]
        border = ls[0]
        prob = ls[1]

        if prob > best_p:
            best_p = prob
            best_border = border

    return best_border


# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    print(f'airice row and col: {gt_airice}')
    print(f'rockice row and col: {gt_icerock}')

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    print(f'image array shape: {image_array.shape}')
    print(f'edge strength map shape {edge_strength(input_image).shape}')

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('output/edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.

    # what's the issue here
    edge_array = edge_strength



    airice_simple = ai_simple(image_array, edge_array)
    airice_hmm = ai_hmm(image_array, edge_array)
    airice_feedback= ai_feedback(image_array, edge_array, gt_airice)

    #print('results for feedback')
    #print(len(airice_feedback))
    #curr = airice_feedback[len(image_array[0])-1]

    #print('airice feedback length')
    #print(len(airice_feedback))

    #for key, val in curr.items():
        #print(key)
        #print(val[1])
        #print(val[0])


    icerock_simple = ir_simple(image_array, edge_array, airice_simple)
    icerock_hmm = ir_hmm(image_array, edge_array, airice_hmm)
    icerock_feedback= ir_feedback(image_array, edge_array, airice_feedback, gt_icerock)

    # Now write out the results as images and a text file
    write_output_image("output/air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("output/ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("output/layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
