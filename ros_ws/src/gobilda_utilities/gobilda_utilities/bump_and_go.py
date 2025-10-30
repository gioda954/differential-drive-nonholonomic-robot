#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
from sensor_msgs.msg import LaserScan

class BumpAndGo(Node):
    FORWARD, BACK, TURN, STOP = range(4)
    def __init__(self):
        super().__init__('bump_and_go')
        # params
        self.declare_parameter('cmd_topic','/gobilda/cmd_vel')   # in sim è TwistStamped
        self.declare_parameter('use_stamped', True)
        self.use_stamped = self.get_parameter('use_stamped').get_parameter_value().bool_value
        self.declare_parameter('v_fwd', 0.25)
        self.declare_parameter('v_back', -0.20)
        self.declare_parameter('w_turn', 0.6)
        self.declare_parameter('front_thresh', 1.0)
        self.declare_parameter('rear_thresh', 1.0)
        self.declare_parameter('clear_thresh', 4.0)
        self.declare_parameter('scan_timeout', 0.6)
        self.declare_parameter('back_time', 1.0)
        self.state = self.STOP
        self.last_scan_t = 0.0
        self.scan = None
        self.back_start = None
        self.turn_dir = 1.0
        msg_type = TwistStamped if self.get_parameter('use_stamped').value else Twist
        self.pub = self.create_publisher(msg_type, self.get_parameter('cmd_topic').value, 10)
        self.sub = self.create_subscription(LaserScan, '/scan', self.on_scan, 10)
        self.timer = self.create_timer(0.05, self.step)  # 20 Hz

    def on_scan(self, msg: LaserScan):
        self.scan = msg
        self.last_scan_t = self.get_clock().now().nanoseconds * 1e-9

    def sector_min(self, center, half_width):
        s = self.scan
        if s is None: return float('inf')
        a0 = max(s.angle_min, center - half_width)
        a1 = min(s.angle_max, center + half_width)
        i0 = max(0, int((a0 - s.angle_min)/s.angle_increment))
        i1 = min(len(s.ranges)-1, int((a1 - s.angle_min)/s.angle_increment))
        if i1 < i0: i0, i1 = i1, i0
        vals = [r for r in s.ranges[i0:i1+1] if math.isfinite(r) and r > s.range_min]
        return min(vals) if vals else float('inf')

    def front_min(self): return self.sector_min(0.0, math.radians(30))
    def rear_min(self):  return self.sector_min(math.pi, math.radians(30))
    def left_min(self):  return self.sector_min(math.pi/2, math.radians(60))
    def right_min(self): return self.sector_min(-math.pi/2, math.radians(60))

    def send(self, vx, wz):
       m = TwistStamped() if self.use_stamped else Twist()
       vx = float(vx)
       wz = float(wz)
       if self.use_stamped:
           m.header.stamp = self.get_clock().now().to_msg()
           m.twist.linear.x = vx
           m.twist.angular.z = wz
       else:
           m.linear.x = vx
           m.angular.z = wz
       self.pub.publish(m)


    def step(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        if now - self.last_scan_t > self.get_parameter('scan_timeout').value:
            self.state = self.STOP; self.send(0,0); return
        fmin = self.front_min()
        rmin = self.rear_min()
        front_obs   = fmin < self.get_parameter('front_thresh').value
        rear_obs    = rmin < self.get_parameter('rear_thresh').value
        front_clear = fmin >= self.get_parameter('clear_thresh').value

        if self.state == self.STOP:
            self.state = self.FORWARD

        elif self.state == self.FORWARD:
            self.send(self.get_parameter('v_fwd').value, 0.0)
            if front_obs:
                self.state = self.BACK
                self.back_start = now

        elif self.state == self.BACK:
            self.send(self.get_parameter('v_back').value, 0.0)
            if rear_obs or (now - self.back_start) >= self.get_parameter('back_time').value:
                self.turn_dir = +1.0 if self.left_min() > self.right_min() else -1.0
                self.state = self.TURN

        elif self.state == self.TURN:
            self.send(0.0, self.turn_dir * self.get_parameter('w_turn').value)
            if front_clear:
                self.state = self.FORWARD
        else:
            self.send(0.0,0.0); self.state = self.STOP

def main():
    rclpy.init(); node = BumpAndGo(); rclpy.spin(node); node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__': main()
