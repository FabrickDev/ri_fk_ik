import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class InverseKinematics(Node):

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

        # Subscribers Based:
            # https://github.com/FabrickDev/ri-fk-ik/blob/main/assets/subscribers.jpeg
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

        self.get_logger().info(
            f'[ri-ikfk-node] Inverse Kinematics aktif | V={self.Vel} m/s | omega={self.Omega} rad/s'
        )

    def velocity_callback(self, msg):
        # Variable Update
        self.Vel = msg.linear.x
        self.Omega = msg.angular.z

    def publish_wheels(self):
        ThisVel = self.Vel
        ThisOmega = self.Omega

        ThisRadius = self.wheel_radius
        ThisSeparation = self.wheel_separation

        # Formula IK Based:
            # https://github.com/FabrickDev/ri-fk-ik/blob/main/assets/ik.jpeg
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

    # Ambil argumen user (buang argumen khusus ROS seperti --ros-args)
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

    node = InverseKinematics(Vel, Omega)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()