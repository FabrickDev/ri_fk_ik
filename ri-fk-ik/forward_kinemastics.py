import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class ForwardKinematics(Node):

    def __init__(self):
        super().__init__('ri-ikfk-node')

        # Param Robot Based: 
            # https://github.com/Bakso14/robin_bringup
            # https://github.com/Bakso14/robin_description
        self.wheel_radius = 0.03
        self.wheel_separation = 0.17

        # INitialize Velocities for Wheels (R n L)
        self.Vel_L = 0.0
        self.Vel_R = 0.0

        # Subscribers Based: 
            # https://github.com/FabrickDev/ri-fk-ik/blob/main/assets/subscribers.jpeg

        # Subscriber Left Wheel
        self.create_subscription(
            Float64,
            '/left_wheel/velocity',
            self.left_callback,
            10
        )

        # Subscriber Right WHeel
        self.create_subscription(
            Float64,
            '/right_wheel/velocity',
            self.right_callback,
            10
        )

        self.get_logger().info('[ri-ikfk-node] Forward Kinematics Active')


    # Callbacks Functions for Subscribers:
    def left_callback(self, msg):

        self.Vel_L = msg.data
        self.fk_calculation()

    def right_callback(self, msg):

        self.Vel_R = msg.data
        self.fk_calculation()

    # Our Formula or WHatever
    def fk_calculation(self):

        r = self.wheel_radius
        s = self.wheel_separation

        # FK Formula Based: 
            # https://github.com/FabrickDev/ri-fk-ik/blob/main/assets/fk.jpeg

        V = (r / 2) * (self.Vel_L + self.Vel_R) # Velocity linear
        Omega = (r / s) * (self.Vel_R - self.Vel_L) # Omega angular

        self.get_logger().info(
            f'[ri-ikfk-node] Forward Kinematics Logger | '
            f'Vel_L={self.Vel_L:.2f} rad/s | '
            f'Vel_R={self.Vel_R:.2f} rad/s | '
            f'V={V:.2f} m/s | '
            f'omega={Omega:.2f} rad/s'
        )


def main(args=None):

    rclpy.init(args=args)

    node = ForwardKinematics()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()