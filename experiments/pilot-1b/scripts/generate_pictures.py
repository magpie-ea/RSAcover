from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple, Any
import random
import math
import copy
import os
import json
import numpy
import csv
from csv import DictReader
import sys
import numpy as np
# from shapes import Triangle
# from shapes import Cross
# import shapes
import cairo
import pandas as pd

@dataclass
class Object:
    x: int = 0
    y: int = 0
    radius: int = 0
    context: Any = 'None'
    color: str = 'None'
    shape: str = 'None'
    number: int = 1
    position: str = None

    def get_parameters(self):
        parameters = (self.x, self.y, self.radius)
        return parameters

    def test_unused_argument(self):
        return self.radius

    def set_color(self):
        if self.color == 'orange':
            self.context.set_source_rgb(1, 0.51, 0)
        elif self.color == 'blue' or self.color == 'blau':
            self.context.set_source_rgb(0.35, 0.7, 0.9)
        elif self.color == 'grey' or self.color == 'grau':
            self.context.set_source_rgb(0.55, 0.51, 0.53)
        elif self.color == 'brown' or self.color == 'braun':
            self.context.set_source_rgb(0.53, 0.27, 0.07)
        elif self.color == 'black' or self.color == 'schwarz':
            self.context.set_source_rgb(0, 0, 0)
        elif self.color == 'green' or self.color == 'grün':
            self.context.set_source_rgb(0.67, 1, 0.18)
        elif self.color == 'purple' or self.color == 'lila':
            self.context.set_source_rgb(0.5, 0, 0.5)
        elif self.color == 'yellow' or self.color == 'gelb':
            self.context.set_source_rgb(1, 1, 0)
        elif self.color == 'turquoise' or self.color == 'türkis':
            self.context.set_source_rgb(0.25, 0.88, 0.82)
        elif self.color == 'red' or self.color == 'rot':
            self.context.set_source_rgb(1, 0, 0)
        elif self.color == 'pink':
            self.context.set_source_rgb(1, 0.07, 0.57)

    def draw_heart(self):
        x, y, radius = self.get_parameters()
        self.set_color()
        xoffset = 0.8 * radius
        yoffset1 = 0.6 * xoffset
        yoffset2 = 0.7 * xoffset
        y = y - yoffset1
        self.context.move_to(x, y)
        self.context.curve_to(x, y - yoffset1, x - xoffset, y - yoffset1, x - xoffset, y)
        self.context.curve_to(x - xoffset, y + yoffset1, x, y + yoffset2, x, y + 2 * yoffset1)
        self.context.curve_to(x, y + yoffset2, x + xoffset, y + yoffset1, x + xoffset, y)
        self.context.curve_to(x + xoffset, y - yoffset1, x, y - yoffset1, x, y)
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()
        self.context.save()

    def draw_triangle(self):
        x, y, radius = self.get_parameters()
        self.set_color()
        radius = radius / math.sqrt(3) * 3
        self.context.move_to(x, y - (math.sqrt(3) / 3 * radius))
        self.context.line_to(x - radius / 2, y + (3 / math.sqrt(3) / 6 * radius))
        self.context.line_to(x + radius / 2, y + (3 / math.sqrt(3) / 6 * radius))
        self.context.line_to(x, y - (math.sqrt(3) / 3 * radius))
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()
        self.context.save()

    def draw_rectangle(self):
        x, y, radius = self.get_parameters()
        self.set_color()
        radius = 2 * radius / math.sqrt(2)
        points = [
            (x - (radius / 2), y - (radius / 2)),
            (x - (radius / 2), y + (radius / 2)),
            (x + (radius / 2), y + (radius / 2)),
            (x + (radius / 2), y - (radius / 2)),
            (x - (radius / 2), y - (radius / 2))
        ]
        for i in range(len(points)):
            self.context.line_to(points[i][0], points[i][1])
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()
        self.context.save()

    def draw_cross(self):
        x, y, radius = self.get_parameters()
        self.set_color()
        b = radius / 3
        a = 2 * b
        self.context.move_to(x - (b / 2), y - (b / 2))
        points = [
            (x - (b / 2), y - (b / 2)),
            (x - (b / 2) - a, y - (b / 2)),
            (x - (b / 2) - a, y - (b / 2) + b),
            (x - (b / 2), y - (b / 2) + b),

            (x - (b / 2), y + (b / 2) + a),
            (x + (b / 2), y + (b / 2) + a),
            (x + (b / 2), y + (b / 2)),

            (x + (b / 2) + a, y + (b / 2)),
            (x + (b / 2) + a, y - (b / 2)),
            (x + (b / 2), y - (b / 2)),

            (x + (b / 2), y - (b / 2) - a),
            (x - (b / 2), y - (b / 2) - a),
            (x - (b / 2), y - (b / 2))
        ]
        for i in range(len(points)):
            self.context.line_to(points[i][0], points[i][1])
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()
        self.context.save()

    def draw_circle(self):
        x, y, radius = self.get_parameters()
        radius = radius / math.sqrt(2)
        self.set_color()
        self.context.arc(x, y, radius, 0, 2 * math.pi)
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()

    def draw_star(self):
        x, y, degree = self.get_parameters()
        self.set_color()
        costum_size_adjustment = 0.8 #control the size
        degree = degree * costum_size_adjustment
        bottom = degree
        diag = bottom / math.cos(math.pi / 5)
        points = (
            (x, y),
            (x + diag, y),
            (x + diag + bottom / 2, y - diag * math.cos(math.pi / 10)),
            (x + diag + bottom, y),
            (x + (2 * diag) + bottom, y),
            (x + (2 * diag) + bottom - diag * math.cos(math.pi / 5), y + diag * math.sin(math.pi / 5)),
            (x + (2 * diag + bottom) * math.cos(math.pi / 5), y + (2 * diag + bottom) * math.sin(math.pi / 5)),
            (x + diag + bottom / 2, y + (bottom + diag) * math.sin(math.pi / 5)),
            (x + (((2 * diag) + bottom) - (2 * diag + bottom) * math.cos(math.pi / 5)),
             y + (2 * diag + bottom) * math.sin(math.pi / 5)),
            (x + diag * math.cos(math.pi / 10), y + diag * math.sin(math.pi / 5)),
            (x, y),
        )
        for i in range(11):
            self.context.line_to(points[i][0], points[i][1])
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()
        self.context.save()


def draw_object(c, objs):
    for _ in objs:
        _.context = c
        if _.shape == "triangle":
            _.draw_triangle()
        elif _.shape == "heart":
            _.draw_heart()
        elif _.shape == "square":
            _.draw_rectangle()
        elif _.shape == "cross":
            _.draw_cross()
        elif _.shape == "circle":
            _.draw_circle()
        elif _.shape == "star":
            _.draw_star()


def no_overlap(objs, x, y, radius):
    """Checks whether a new obj will have any overlap with an existing
    array of objs.

    Args:
        objs: an iterable of `Object`s
        x: x-value of center of new obj
        y: y-value of center of new obj
        r: radius of new obj

    Returns:
        True if the new dot has no overlap with any of the dots in `dots',
        False otherwise
    """
    radius = radius * 2
    #condition = (x < (obj.x + 2 * radius) and x > (obj.x - 2 * radius)) and (y < (obj.y + 2 * radius) and y > (obj.y - 2 * radius))
    #return all([(x < (obj.x + radius) and x > (obj.x - radius)) and (y < (obj.y - radius) and y > (obj.y + radius)) for obj in objs])
    return all([(x - obj.x) ** 2 + (y - obj.y) ** 2 > (radius + obj.radius) ** 2
                for obj in objs])


def clip(val, min_val, max_val):
    """Clips `val` to be in the range [min_val, max_val]. """
    return max(min(val, max_val), min_val)


def get_random_radii(min_radius, max_radius, std=1):
    """Gets random radii of shapes for a shapes_dict.  Radii are sampled from
    a Gaussian distribution with mean (max_r - min_r) / 2 and standard
    deviation std, then clipped.

    Args:
        color_dict: dictionary of colors, with integer values
        min_radius: smallest radius
        max_radius: biggest radius
        std: standard deviation

    Returns:
        a dictionary, with the same keys as shapes_dict, and values a list of
        shapes_dict[shape] floating point numbers
    """
    mean = (max_radius - min_radius) / 2
    radius = clip(random.gauss(mean, std), min_radius, max_radius)
    return radius


def get_area_controlled_radii(shapes_dict, min_radius, max_radius, std=0.5,
                              total_area=None):
    """Gets area controlled radii: the sum of the areas of each shapes will be equal (either to total_area or to the total area taken by the
    largest number in shapes_dict dots of mean radius).

    Args:
        shapes_dict: as above
        min_radius: as above
        max_radius: as above
        std: as above
        total_area: a float, the total area to distribute to each color.  If
            not specified, this will be set to N*(max_radius - min_radius)/2^2,
            where N is the largest value in shapes_dict

    Returns:
        a dictionary, as above
    """
    mean = (max_radius - min_radius) / 2
    if not total_area:
        total_area = math.pi * (mean ** 2) * max(shapes_dict.values())
    radii = {shape: [] for shape in shapes_dict}
    for shape in shapes_dict:
        num_remaining = shapes_dict[shape]
        area_remaining = total_area
        while num_remaining > 1:
            mean = math.sqrt(area_remaining / (num_remaining * math.pi))
            # get radius that is not too big to use up all remaining area!
            found_r = False
            while not found_r:
                r = clip(random.gauss(mean, std), min_radius, max_radius)
                if math.pi * r ** 2 < area_remaining:
                    found_r = True
            radii[shape].append(r)
            area_remaining -= math.pi * r ** 2
            num_remaining -= 1
        radii[shape].append(math.sqrt(area_remaining / math.pi))
    return radii


def scattered_random(objs, area_control=False,
                     total_area=None,
                     num_pixels=(512, 512), padding=20,
                     min_radius=30, max_radius=40, std=5):
    """Generates ScatteredRandom images: the dots are scattered
    randomly through the image. """
    if area_control:
        radii = get_area_controlled_radii(min_radius, max_radius,
                                          std=std, total_area=total_area)
    else:
        radii = get_random_radii(min_radius, max_radius, std=std)
    # print({color: sum([math.pi*r**2 for r in radii[color]]) for color in radii})
    for _ in objs:
        radius = get_random_radii(min_radius, max_radius, std)
        x_min, y_min = padding + radius, padding + radius
        x_max, y_max = num_pixels[0] - padding - radius, num_pixels[1] - padding - radius
        new_obj_added = False
        while not new_obj_added:
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            # avoid overlap with existing circles
            if no_overlap(objs, x, y, radius):
                _.x, _.y, _.radius = x, y, radius
                new_obj_added = True
    return objs


def scattered_split(shapes_dict, area_control=False,
                    num_pixels=(512, 512), padding=24,
                    min_radius=1, max_radius=5, std=0.5,
                    shape_order=None):
    """Generates ScatteredSplit images: the dots are scattered randomly through
    the image, but each color has its own region of the image, with different
    colors laid out horizontally. """
    width_per = num_pixels[0] / len(shapes_dict)
    mean = (max_radius - min_radius) / 2
    total_area = math.pi * (mean ** 2) * max(shapes_dict.values())
    shape_objs = {shape: scattered_random(
        {shape: shapes_dict[shape]}, area_control=area_control,
        total_area=total_area,
        num_pixels=(width_per, num_pixels[1]), padding=padding,
        min_radius=min_radius, max_radius=max_radius, std=std)
        for shape in shapes_dict}
    objs = []
    if not shape_order:
        shapes = list(shapes_dict.keys())
        random.shuffle(shapes)
    else:
        shapes = shape_order
    for idx in range(len(shapes)):
        objs.extend([obj._replace(x=obj.x + idx * width_per)
                     for obj in shape_objs[shapes[idx]]])
    return objs


def shift_position(position, obj):
    if position == 'left':
        obj.x, obj.y = obj.x, obj.y
    elif position == "right":
        # central_width defines area in the middle with no objects, set to 100 pixels; defined here and below in main; has to be changed twice, if required
        central_width = 100
        obj.x = obj.x + 256 + central_width
        obj.y = obj.y + 256 + central_width
    return obj

def adjust_size(max_size, size, coefficient):
    size = max_size * size * coefficient
    if size >= max_size:
        size = max_size
    return size

def sum_dict(a, b):
    temp = {}
    for key in a.keys() | b.keys():
        temp[key] = sum([d.get(key, 0) for d in (a, b)])
    return temp

def get_grouped_objs(row, objs1, objs2, groupby):
    random_number = [random.randint(1, 3) for _ in range(2)]
    if groupby == "Color":
        for i, obj in enumerate(objs1):
            obj.color = row['Color1']
            obj.shape = row['Shape1']
            if i in random_number:
                obj.shape = row['Shape2']
        for i, obj in enumerate(objs2):
            obj.color = row['Color2']
            obj.shape = row['Shape2']
            if i in random_number:
                obj.shape = row['Shape1']

    if groupby == "Shape":
        for i, obj in enumerate(objs1):
            obj.color = row['Color1']
            obj.shape = row['Shape1']
            if i in random_number:
                obj.color = row['Color2']
        for i, obj in enumerate(objs2):
            obj.color = row['Color2']
            obj.shape = row['Shape2']
            if i in random_number:
                obj.color = row['Color1']
    return objs1 + objs2

def encode_objects(row, matchness = "random", groupby='Color', central_width=100):
    groupby = row['Grouped']
    number_color1 = int(row['Number1'])
    number_color2 = int(row['Number2'])
    total_number = number_color1 + number_color2
    if matchness == 'random':
        objs1 = [Object() for _ in range(number_color1)]
        objs2 = [Object() for _ in range(number_color2)]
        objs1 = scattered_random(objs1, num_pixels=(512, 512), padding=50)
        objs2 = scattered_random(objs2, num_pixels=(512, 512), padding=50)
        # Distribute colors and shapes
        for obj in objs1:
            if random.choice([True, False]):
                obj.color = row['Color1']
                obj.shape = row['Shape1']
            else:
                obj.color = row['Color2']
                obj.shape = row['Shape2']
        for obj in objs2:
            obj.x = obj.x + 512 + central_width
            if random.choice([True, False]):
                obj.color = row['Color2']
                obj.shape = row['Shape2']
            else:
                obj.color = row['Color1']
                obj.shape = row['Shape1']
        objs = objs1 + objs2
    else:
        objs1 = [Object() for _ in range(number_color1)]
        objs2 = [Object() for _ in range(number_color2)]
        objs1 = scattered_random(objs1, num_pixels=(512, 512), padding=50)
        objs2 = scattered_random(objs2, num_pixels=(512, 512), padding=50) 
        for obj in objs2:
            obj.x = obj.x + 512 + central_width
        random_number = [random.randint(1, 3) for _ in range(2)]
        if matchness == "+match":
            objs = get_grouped_objs(row, objs1, objs2, groupby = groupby)
        if matchness == "-match":
            groupby_list = ["Color", "Shape"]
            other_groupby = groupby_list[1] if groupby == groupby_list[0] else groupby_list[0]
            objs = get_grouped_objs(row, objs1, objs2, groupby = other_groupby)
       
    return objs

quandrant_width = 256

def main():
    # Read csv to retrieve relevant information for generating stimuli
    file_path = '../experiments/pilot-1/trials/items.csv'
    df = pd.read_csv(file_path)
    print(df.head())
    fillerNr_list = [901, 902, 903, 904, 905, 906]
    # Iterate the rows of the dataframe
    for i, row in df.iterrows():
        if row.itemNr not in fillerNr_list:
            objs = encode_objects(row, row.F2_matchness)
        else:
            objs = encode_objects(row, matchness = "random")

    # Define a background for drawing the objects
        filename = "../experiments/pilot-1/pictures/" + 'img_l' + str(row['List']) + '_' + 'i' + str(row['itemNr']) + ".svg"
        sub_window_width = 512
        line_width = 5
        # area in the middle with no objects, set to 100 pixels
        central_width = 150
        window_width = 2 * sub_window_width + central_width + line_width
        window_height = sub_window_width + line_width
        s = cairo.SVGSurface(filename, window_width, window_height)
        c = cairo.Context(s)
        c.set_source_rgb(0.9, 0.9, 0.9)
        c.rectangle(0, 0, window_width, window_height)
        c.fill()

    # Draw the objects
        draw_object(c, objs)
        s.finish()





if __name__ == main():
    main()
