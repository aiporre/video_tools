# video tools
Some useful scripts to process videos as Objects. 

Installation with GPU. Notice that CUDA drivers must be installed separately.
```
$ conda create -n vtools python==3.8 pip
$ pip install tensorflow>=2.4.0
$ pip install n2v>=0.3.0 Keras>=2.3.1 tensorflow>=2.4.0 # optionally 
$ python3 setup.py sdist bdist_wheel
$ pip install dist/vtools-0.1-py3-none-any.whl
```

