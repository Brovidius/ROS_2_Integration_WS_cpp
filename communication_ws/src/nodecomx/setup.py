import os
from glob import glob
from setuptools import setup

package_name = 'nodecomx'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ovidius',
    maintainer_email='oviad@protonmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'processing = nodecomx.processing_node:main',
            'receiver = nodecomx.receiver_node:main',
            'transmitter = nodecomx.transmitter_node:main'
        ],
    },
)
