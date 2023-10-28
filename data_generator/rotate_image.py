from math import pi
import numpy as np
import cv2

def get_rad(theta, phi, gamma):
    return (deg_to_rad(theta),
            deg_to_rad(phi),
            deg_to_rad(gamma))

def get_deg(rtheta, rphi, rgamma):
    return (rad_to_deg(rtheta),
            rad_to_deg(rphi),
            rad_to_deg(rgamma))

def deg_to_rad(deg):
    return deg * pi / 180.0

def rad_to_deg(rad):
    return rad * 180.0 / pi

def rotate_along_axis(image, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0):
    h, w, _ = image.shape
    # Get radius of rotation along 3 axes
    rtheta, rphi, rgamma = get_rad(theta, phi, gamma)
    
    # Get ideal focal length on z axis
    # NOTE: Change this section to other axis if needed
    d = np.sqrt(h**2 + w**2)
    focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)
    dz = focal

    # Get projection matrix
    mat = get_M(image.shape, rtheta, rphi, rgamma, dx, dy, dz)
    
    return cv2.warpPerspective(image.copy(), mat, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))


""" Get Perspective Projection Matrix """
def get_M(shape, theta, phi, gamma, dx, dy, dz):
    
    w = shape[1]
    h = shape[0]
    f = dz

    # Projection 2D -> 3D matrix
    A1 = np.array([ [1, 0, -w/2],
                    [0, 1, -h/2],
                    [0, 0, 1],
                    [0, 0, 1]])
    
    # Rotation matrices around the X, Y, and Z axis
    RX = np.array([ [1, 0, 0, 0],
                    [0, np.cos(theta), -np.sin(theta), 0],
                    [0, np.sin(theta), np.cos(theta), 0],
                    [0, 0, 0, 1]])
    
    RY = np.array([ [np.cos(phi), 0, -np.sin(phi), 0],
                    [0, 1, 0, 0],
                    [np.sin(phi), 0, np.cos(phi), 0],
                    [0, 0, 0, 1]])
    
    RZ = np.array([ [np.cos(gamma), -np.sin(gamma), 0, 0],
                    [np.sin(gamma), np.cos(gamma), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

    # Composed rotation matrix with (RX, RY, RZ)
    R = np.dot(np.dot(RX, RY), RZ)

    # Translation matrix
    T = np.array([  [1, 0, 0, dx],
                    [0, 1, 0, dy],
                    [0, 0, 1, dz],
                    [0, 0, 0, 1]])

    # Projection 3D -> 2D matrix
    A2 = np.array([ [f, 0, w/2, 0],
                    [0, f, h/2, 0],
                    [0, 0, 1, 0]])

    # Final transformation matrix
    return np.dot(A2, np.dot(T, np.dot(R, A1)))

# image = cv2.imread("shape/cross.png")
# image = rotate_along_axis(image, gamma=10)
# cv2.imshow("rotated", image)
# cv2.waitKey(0)