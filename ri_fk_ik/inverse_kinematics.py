import sys
import rclpy
from rclpy.node import Node
from rclpy.utilities import remove_ros_args

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class inverse_kinematics(Node):

    def __init__(self, Vel=0.0, Omega=0.0):
        super().__init__('inverse_kinematics')

        # Param Robot Based:
            # https://github.com/Bakso14/robin_bringup
            # https://github.com/Bakso14/robin_description
        self.wheel_radius = 0.03
        self.wheel_separation = 0.17

        # Nilai kecepatan awal dari argumen terminal
        self.Vel = Vel
        self.Omega = Omega

        # self.IKInit_Publisher = self.create_publisher(
        #     Twist,
        #     '/input_ik',
        #     10
        # )
        
        # ThisInitData = Twist()
        # ThisInitData.linear.x = self.Vel
        # ThisInitData.angular.z = self.Omega
        # self.IKInit_Publisher.publish(ThisInitData)

        # Subscribers Based:
            # https://github.com/FabrickDev/ri_fk_ik/blob/main/assets/subscribers.jpeg
        # Subscriber Robin Speed (OPtional to Use Value from Terminal/Arguments)
        self.create_subscription(
            Twist,
            '/input_ik',
            self.velocity_callback,
            10
        )

        # Publisher Left Wheel
        self.left_publisher = self.create_publisher(
            Float64,
            '/left_wheel/command',
            10
        )

        # Publisher Right Wheel
        self.right_publisher = self.create_publisher(
            Float64,
            '/right_wheel/command',
            10
        )

        #self.create_timer(0.1, self.publish_sheels)

        self.get_logger().info(
            f'[ri-ikfk-node] Inverse Kinematics Active | V={self.Vel} m/s | omega={self.Omega} rad/s'
        )

    def velocity_callback(self, msg):
        # Update kecepatan dari topic /input_ik
        self.Vel = msg.linear.x
        self.Omega = msg.angular.z
        ThisVel = self.Vel
        ThisOmega = self.Omega
        
        ThisRadius = self.wheel_radius
        ThisSeparation = self.wheel_separation

        # Formula IK Based:
            # https://github.com/FabrickDev/ri_fk_ik/blob/main/assets/ik.jpeg
        phi_L = (2 * ThisVel - ThisOmega * ThisSeparation) / (2 * ThisRadius)
        phi_R = (2 * ThisVel + ThisOmega * ThisSeparation) / (2 * ThisRadius)

        left_msg = Float64()
        right_msg = Float64()
        left_msg.data = phi_L
        right_msg.data = phi_R

        # PUBLISHHHHH
        self.left_publisher.publish(left_msg)
        self.right_publisher.publish(right_msg)

        # Yapper
        self.get_logger().info(
            f'[ri-ikfk-node] Inverse Kinematics Logger | '
            f'V={ThisVel:.2f} unit/s | '
            f'omega={ThisOmega:.2f} rad/s | '
            f'phi_L={phi_L:.2f} rad/s | '
            f'phi_R={phi_R:.2f} rad/s'
        )

    # Not Used Yet, But Can Be Used for Timer Based Publish
    def publish_sheels(self):
        # Variable Update

        ThisVel = self.Vel
        ThisOmega = self.Omega

        ThisRadius = self.wheel_radius
        ThisSeparation = self.wheel_separation

        # Formula IK Based:
            # https://github.com/FabrickDev/ri_fk_ik/blob/main/assets/ik.jpeg
        phi_L = (2 * ThisVel - ThisOmega * ThisSeparation) / (2 * ThisRadius)
        phi_R = (2 * ThisVel + ThisOmega * ThisSeparation) / (2 * ThisRadius)

        left_msg = Float64()
        right_msg = Float64()
        left_msg.data = phi_L
        right_msg.data = phi_R

        # PUBLISHHHHH
        self.left_publisher.publish(left_msg)
        self.right_publisher.publish(right_msg)

        # Yapper
        self.get_logger().info(
            f'[ri-ikfk-node] Inverse Kinematics Logger | '
            f'V={ThisVel:.2f} unit/s | '
            f'omega={ThisOmega:.2f} rad/s | '
            f'phi_L={phi_L:.2f} rad/s | '
            f'phi_R={phi_R:.2f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)

    user_args = remove_ros_args(args=sys.argv)[1:]

    Vel = 0.0
    Omega = 0.0
    try:
        if len(user_args) >= 1:
            Vel = float(user_args[0])
        if len(user_args) >= 2:
            Omega = float(user_args[1])
    except ValueError:
        print('Argumen must be Floating Number Mate!!')
        print('For Example:ros2 run ir-fk-ik ir-fkik 0.2 0.5')
        rclpy.shutdown()
        return

    node = inverse_kinematics(Vel, Omega)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()