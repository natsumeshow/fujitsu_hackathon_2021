# 富士通ハッカソン2021 チームI


## Install
Our method is based on tf-openpose. Before using our dance scoring system, you should first prepare tf-openpose.

$ git clone https://www.github.com/ildoonet/tf-pose-estimation
$ cd tf-pose-estimation

### Dependencies

You need dependencies below.

- python3
- tensorflow 1.4.1+
- opencv3, protobuf, python3-tk
- slidingwindow
  - https://github.com/adamrehn/slidingwindow
  - I copied from the above git repo to modify few things.


$ conda create -n score_system python=3.6


$ conda activate score_system


# if you want to use GPU 

$ conda install -c anaconda tensorflow-gpu==1.14

# if you want to use CPU 

$ conda install -c conda-forge tensorflow==1.14

$ conda install -c https://conda.anaconda.org/menpo opencv3

$ conda install -c anaconda protobuf

$ apt-get install tk-dev python-tk or sudo apt-get install tk-dev python-tk

$ apt-get install libllvm-7-ocaml-dev libllvm7 llvm-7 llvm-7-dev llvm-7-doc llvm-7-examples llvm-7-runtime

$ export LLVM_CONFIG=/usr/bin/llvm-config-7

$ pip3 install -r requirements.txt

$ cd tf_pose/pafprocess

$ swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace

$ cd ../../

$ python setup.py install

$ cd models/graph/cmu

$ bash download.sh



# Maybe need install opencv again for video or webcam.

$conda install -c conda-forge opencv=4.1.0

$ cd ~

$ git clone https://github.com/natsumeshow/fujitsu_hackathon_2021.git

## Copy pre-trained tf-openpose models to our score system folder.

$ cp -r tf-pose-estimation/models/ fujitsu_hackathon_2021/

## Demo
To Do....


