from setuptools import find_packages, setup

package_name = 'ri_fk_ik'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='faqisna-pm-fabrickdev',
    maintainer_email='faqisna.pm@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'inverse_kinematics = ri_fk_ik.inverse_kinematics:main'
        ],
    },
)
