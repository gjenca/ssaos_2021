from numpy import array,dot,cos,sin,radians

def rotmatrix(theta_deg):

    theta = radians(theta_deg)
    return array([[cos(theta),-sin(theta)],[sin(theta),cos(theta)]])

def triangle_over(node1,node2):

    a=array(node1.position)
    b=array(node2.position)
    c=dot(rotmatrix(60),a-b)+b
    return (c[0],c[1])

