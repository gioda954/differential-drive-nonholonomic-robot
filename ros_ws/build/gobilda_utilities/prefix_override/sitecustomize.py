import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/gobilda_sim/ros_ws/install/gobilda_utilities'
