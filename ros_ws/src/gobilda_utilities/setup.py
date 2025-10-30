from setuptools import setup

package_name = 'gobilda_utilities'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gio',
    maintainer_email='gdallago@calpoly.edu',
    description='Utility nodes for GoBilda robot',
    entry_points={
        'console_scripts': [
            'bump_and_go = gobilda_utilities.bump_and_go:main',
        ],
    },
)
