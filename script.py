import rospy
import numpy as np

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import Empty
from std_msgs.msg import String

executing = False
pub = None

positions = [
    [-10000, 155000],
    [-35000, 155000],
    [-65000, 155000],
    [-10000, 120000],
    [-35000, 120000],
    [-65000, 120000],
    [-10000, 85000],
    [-35000, 85000],
    [-65000, 85000],
]

curx = 0
cury = 0
r = None

def think(msgs):
    global curx, cury, positions, r
    print(msgs.data)
    data = [int(x) for x in msgs.data]
    idxs = sorted(range(9), key=lambda k:data[k])
    mat = Float32MultiArray()
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim[0].label = "height"
    mat.layout.dim[1].label = "width"
    mat.layout.dim[0].size = 2
    mat.layout.dim[1].size = 9
    mat.data = [0]*18
    print(idxs)
    for i in range(len(idxs)):
        pos = positions[idxs[i]]
        print(pos)
        tx = pos[0] - curx
        ty = pos[1] - cury
        curx = pos[0]
        cury = pos[1]
        mat.data[i * 2] = tx
        mat.data[i * 2 + 1] = ty
    print(mat)
    pub.publish(mat)
    r.sleep()
def result(msgs):
    global r
    mat = Float32MultiArray()
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim[0].label = "height"
    mat.layout.dim[1].label = "width"
    mat.layout.dim[0].size = 2
    mat.layout.dim[1].size = 1
    mat.data = [0]*2
    mat.data[0] = -35000
    mat.data[1] = 47000
    pub.publish(mat)
    r.sleep()
def main():
    global executing, pub, r
    rospy.init_node('think')
    executing = False
    pub = rospy.Publisher('route2', Float32MultiArray, queue_size=1)
    rospy.Subscriber('result', String, result)
    rospy.Subscriber('board', Float32MultiArray, think)
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        r.sleep()
if __name__ == "__main__":
    main()
