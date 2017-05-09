import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    edges = new_matrix()
    ident( edges )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(edges)
    stack = [ [x[:] for x in edges] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for args in commands:
        if args[0] == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(edges,
                       float(args[1]), float(args[2]), float(args[3]),
                       float(args[4]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif args[0] == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(edges,
                      float(args[1]), float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif args[0] == 'box':
            #print 'BOX\t' + str(args)
            add_box(edges,
                    float(args[1]), float(args[2]), float(args[3]),
                    float(args[4]), float(args[5]), float(args[6]))
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif args[0] == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                    float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), float(args[4]), step)

        elif args[0] == 'hermite' or args[0] == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                    float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]),
                      float(args[5]), float(args[6]),
                      float(args[7]), float(args[8]),
                      step, float(args[0]))                      
            
        elif args[0] == 'line':            
            #print 'LINE\t' + str(args)

            add_edge( edges,
                    float(args[1]), float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]), float(args[6]), )

        elif args[0] == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[1]), float(args[2]), float(args[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif args[0] == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[1]), float(args[2]), float(args[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]


        elif args[0] == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[2]) * (math.pi / 180)
            
            if args[1] == 'x':
                t = make_rotX(theta)
            elif args[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
                
        elif args[0] == 'clear':
            edges = []
            
        elif args[0] == 'ident':
            ident(transform)

        elif args[0] == 'apply':
            matrix_mult( transform, edges )

        elif args[0] == 'push':
           stack.append( [x[:] for x in stack[-1]] )
            
        elif args[0] == 'pop':
            stack.pop()
            
        elif args[0] == 'display' or line == 'save':
            if args[0] == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
    
