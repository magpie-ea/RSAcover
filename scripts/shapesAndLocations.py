'''
Created on May 13, 2010

@author: chris
'''

import math
import cairo
import sys

#definition of Shape class
class Shape(object):
    #constructor
    def __init__(self, context, cx, cy, cr, color, *args):
        
        #super(object, self).__init__()
        self.context = context
        self.cx = cx
        self.cy = cy
        self.cr = cr
        self.color = color
        self.parameters = (cx, cy, cr, color)

    #methods
    def get_parameters(self):
        return self.parameters
        
    
    def get_extents(self, cx, cy, cr):
        return (cx - cr, cy - cr, cx + cr, cy + cr)
    
    def set_color(self):
        if self.color == 'orange':
            self.context.set_source_rgb(0.9, 0.65, 0.0)
        elif self.color == 'blue' or self.color == 'blau':
            self.context.set_source_rgb(0.35, 0.7, 0.9)
        elif self.color == 'grey':
            self.context.set_source_rgb(0.55, 0.51, 0.53)
        elif self.color == 'brown' or self.color == 'braun':
            self.context.set_source_rgb(0.53, 0.27, 0.07)
        elif self.color == 'black' or self.color == 'schwarz':
            self.context.set_source_rgb(0, 0, 0)
        elif self.color == 'green':
            self.context.set_source_rgb(0.67, 1, 0.18)
    
#definition of Circle class        
class Circle(Shape):
    
    #constructor
    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)
    
    #methods
    def draw(self):
        
        self.set_color()
        self.context.arc(self.cx, self.cy, self.cr, 0, 2 * math.pi)
        self.context.fill()
    
#definition of Landmark class        
class Landmark(Shape):
    
    #constructor
    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)
    
    #methods
    def draw(self):
        
        self.set_color()
        costum_size_adjustment = 0.8
        self.cr = costum_size_adjustment * self.cr
        cx1, cy1, cx2, cy2 = self.get_extents(self.cx, self.cy, self.cr)
        self.context.rectangle(cx1, cy1, cx2 - cx1, cy2 - cy1)
        self.context.fill()
    
#definition of Square class        
class Square(Shape):
    
    #constructor
    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)
    
    def draw(self):
        
        self.set_color()
        cx1, cy1, cx2, cy2 = self.get_extents(self.cx, self.cy, self.cr)
        self.context.rectangle(cx1, cy1, cx2 - cx1, cy2 - cy1)
        self.context.fill()
    
#definition of Triangle class        
class Triangle(Shape):
    
    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)
        
    def draw(self):
        
        self.set_color()
        cx1, cy1, cx2, cy2 = self.get_extents(self.cx, self.cy, self.cr)
        self.context.move_to(self.cx, cy1)
        self.context.line_to(cx1, cy2)
        self.context.line_to(cx2, cy2)
        self.context.line_to(self.cx, cy1)
        self.context.fill()
        
#definition of Cross class        
class Cross(Shape):
    
    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)
        
    def draw(self):
        
        self.set_color()
        costum_size_adjustment = 1 #control the size
        self.cr = costum_size_adjustment * self.cr
        cx1, cy1, cx2, cy2 = self.get_extents(self.cx, self.cy, self.cr)
        self.context.move_to(cx1, self.cy)
        self.context.line_to(cx2, self.cy)
        self.context.move_to(self.cx, cy1)
        self.context.line_to(self.cx, cy2)
        self.context.set_line_width(self.cr / 2)

        self.context.stroke()

# Definition of heart class
class Heart(Shape):

    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)

    def draw(self):
        cx, cy, cr, color = self.get_parameters()
        costum_size_adjustment = 30 #control the size
        y_x_ratio_constant = 0.6
        self.set_color()
        xoffset = cr
        yoffset1 = y_x_ratio_constant * cr
        yoffset2 = y_x_ratio_constant * cr
        self.context.move_to(cx, cy)
        self.context.curve_to(cx, cy - yoffset1, cx - xoffset, cy - yoffset1, cx - xoffset, cy)
        self.context.curve_to(cx - xoffset, cy + yoffset1, cx, cy + yoffset2, cx, cy + 2 * yoffset1)
        self.context.curve_to(cx, cy + yoffset2, cx + xoffset, cy + yoffset1, cx + xoffset, cy)
        self.context.curve_to(cx + xoffset, cy - yoffset1, cx, cy - yoffset1, cx, cy)
        self.context.fill_preserve()
        self.context.set_source_rgba(0, 0, 0, 1)
        self.context.set_line_width(1)
        self.context.stroke()
        self.context.save()

class Star(Shape):

    def __init__(self, context, cx, cy, cr, color):
        Shape.__init__(self, context, cx, cy, cr, color)

    def draw(self):
        x, y, degree, color = self.get_parameters()
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

#the following is executed; sys.argv is an array of command line arguments                
def main():
    landmark_size = 64
    landmark_color = sys.argv[1]
    trajector_color = sys.argv[2]
    #trajector_shape = sys.argv[3]
    trajector_shape = "circle"
    x_coordinate = (int(sys.argv[4])* math.cos(math.pi/180*float(sys.argv[5])))+320
    y_coordinate = 640-((int(sys.argv[4])* math.sin(math.pi/180*float(sys.argv[5])))+320)#+landmark_size	
    trajector_size = int(sys.argv[6])
    filename = sys.argv[7]
    s = cairo.SVGSurface(file(filename, 'w'), 640, 640)
    c = cairo.Context(s)
    c.set_source_rgb(0.9, 0.9, 0.9)
    c.rectangle(0, 0, 640, 640)
    c.fill()
    tmp = Landmark(c, 320, 320, landmark_size, landmark_color)
    tmp.draw()
    
    print(sys.argv)	
    print(x_coordinate,y_coordinate)
    if trajector_shape == 'square':
        tmp = Square(c, x_coordinate, y_coordinate, trajector_size, trajector_color)
        tmp.draw()	
    elif trajector_shape == 'triangle':
        tmp = Triangle(c, x_coordinate, y_coordinate, trajector_size, trajector_color)
        tmp.draw()
    elif trajector_shape == 'circle':
        tmp = Circle(c, x_coordinate, y_coordinate, trajector_size, trajector_color)
        tmp.draw()
    elif trajector_shape == 'cross':
        tmp = Cross(c, x_coordinate, y_coordinate, trajector_size, trajector_color)
        tmp.draw()		
        
	
    s.finish()
    	
   
	
  
if __name__ == '__main__':
    main()     