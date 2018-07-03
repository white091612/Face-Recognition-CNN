# Face-Recognition-CNN

https://github.com/kpzhang93/MTCNN_face_detection_alignment

# Requirement
1. CUDA 
  - NVIDIA Homepage has this
2. cuDNN
  - NVIDIA Homepage has this
3. caffe
  - Read Below
4. CMake
5. Visual Studio 2015(Recommand to download this version)
6. Anaconda
7. Python 3.5(Only 3.5 Supporeted)

# How to Install Requirements
1. Unzip util.zip file
2. Install all 6 files except .cmd file
   - install vs_community.exe very first
   - when install git, try to read option and check
     using windows command line as default (important)
   - install cuda_8.0.61 to 
     C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0
   - unzip cudnn-7.5 and move files to 
     C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0
   - unzip caffe.7z and find pycaffe
     (I used python)
   - open anaconda and create virtual environment with python 3.5 (important)
     type these command
     conda config --add channels conda-forge
     conda config --add channels willyd
     conda install --yes cmake ninja numpy scipy      protobuf==3.1.0 six scikit-image pyyaml pydotplus      graphviz
   - import caffe to confirm you installed all files correctly.
   - install mtcnn with
     pip install mtcnn
    
