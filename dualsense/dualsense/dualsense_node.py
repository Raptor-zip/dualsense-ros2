#!/usr/bin/env python3
"""
dualsense - ROS2 DualSense controller node

Publishes: /gamepad/p{player}  (custom_messages/Gamepad)
Subscribes: /dualsense/feedback (custom_messages/DualSenseFeedback)
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

from custom_messages.msg import Gamepad, DualSenseFeedback

from pydualsense import pydualsense, TriggerModes


TRIGGER_MODE_MAP = {
    0: TriggerModes.Off,
    1: TriggerModes.Rigid,
    2: TriggerModes.Pulse_A,
}


class DualSenseNode(Node):
    def __init__(self):
        super().__init__('dualsense_node')

        # Parameters
        self.declare_parameter('publish_rate', 100.0)
        self.declare_parameter('player', 1)
        self.declare_parameter('l2_threshold', 20)
        self.declare_parameter('r2_threshold', 20)
        self.declare_parameter('stick_deadzone', 8)

        rate = self.get_parameter('publish_rate').value
        player = self.get_parameter('player').value
        self._l2_thresh = self.get_parameter('l2_threshold').value
        self._r2_thresh = self.get_parameter('r2_threshold').value
        self._deadzone = self.get_parameter('stick_deadzone').value

        # DualSense
        self._ds = pydualsense()
        self._ds.init()
        self.get_logger().info('DualSense connected.')

        # Publisher (BestEffort for real-time gamepad data)
        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT,
        )
        topic = f'/gamepad/p{player}'
        self._pub = self.create_publisher(Gamepad, topic, qos)

        # Subscriber
        self._sub = self.create_subscription(
            DualSenseFeedback,
            '/dualsense/feedback',
            self._feedback_callback,
            10,
        )

        # Timer
        self._timer = self.create_timer(1.0 / rate, self._publish_gamepad)

        self.get_logger().info(
            f'Publishing to {topic} at {rate} Hz'
        )

    # ------------------------------------------------------------------
    # Publisher callback
    # ------------------------------------------------------------------
    def _publish_gamepad(self):
        state = self._ds.state
        dz = self._deadzone

        def axis(raw):
            centered = raw - 128
            if abs(centered) <= dz:
                return 0.0
            return centered / 128.0

        msg = Gamepad()
        # Buttons
        msg.a = bool(state.cross)
        msg.b = bool(state.circle)
        msg.x = bool(state.square)
        msg.y = bool(state.triangle)
        msg.lb = bool(state.L1)
        msg.rb = bool(state.R1)
        msg.lt = state.L2_value > self._l2_thresh
        msg.rt = state.R2_value > self._r2_thresh
        msg.up = bool(state.DpadUp)
        msg.right = bool(state.DpadRight)
        msg.down = bool(state.DpadDown)
        msg.left = bool(state.DpadLeft)
        msg.back = bool(state.share)
        msg.start = bool(state.options)
        msg.power = bool(state.ps)
        msg.ls = bool(state.L3)
        msg.rs = bool(state.R3)
        # Axes
        msg.lx = axis(state.LX)
        msg.ly = axis(state.LY)
        msg.rx = axis(state.RX)
        msg.ry = axis(state.RY)
        # Analog triggers
        msg.l2 = state.L2_value / 255.0
        msg.r2 = state.R2_value / 255.0

        msg.header.stamp = self.get_clock().now().to_msg()
        self._pub.publish(msg)

    # ------------------------------------------------------------------
    # Feedback subscriber
    # ------------------------------------------------------------------
    def _feedback_callback(self, msg: DualSenseFeedback):
        ds = self._ds
        ds.light.setColorI(msg.led_r, msg.led_g, msg.led_b)
        ds.setLeftMotor(msg.rumble_left)
        ds.setRightMotor(msg.rumble_right)

        l_mode = TRIGGER_MODE_MAP.get(msg.trigger_l_mode, TriggerModes.Off)
        r_mode = TRIGGER_MODE_MAP.get(msg.trigger_r_mode, TriggerModes.Off)
        ds.triggerL.setMode(l_mode)
        ds.triggerL.setForce(1, msg.trigger_l_force)
        ds.triggerR.setMode(r_mode)
        ds.triggerR.setForce(1, msg.trigger_r_force)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    def destroy_node(self):
        self.get_logger().info('Shutting down DualSense node...')
        ds = self._ds
        ds.light.setColorI(0, 0, 0)
        ds.setLeftMotor(0)
        ds.setRightMotor(0)
        ds.triggerL.setMode(TriggerModes.Off)
        ds.triggerR.setMode(TriggerModes.Off)
        ds.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DualSenseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
