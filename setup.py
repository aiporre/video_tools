from setuptools import setup
requirements = [
                'opencv-python>=4.1.1.26',
                'tqdm>=4.36.1',
                'scikit-image>=0.16.1',
                'tiffile>=2018.10.18'
                ]
setup(name='vtools',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/aiporre/video_tools.git',
      author='Ariel Iporre',
      author_email='iporre@stud.uni-heidelberg.de',
      long_description=open('README.md').read(),
      install_requires=requirements,
      license='MIT',
      packages=['vtools'],
      zip_safe=False)
