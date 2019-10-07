
[![Version](https://img.shields.io/badge/version-1.0-brightgreen.svg)](http://www.verlab.dcc.ufmg.br/fast-forward-video-based-on-semantic-extraction/#ECCVW2016)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)

# Project #

This project is based on the paper [Towards Semantic Fast-Forward and Stabilized Egocentric Videos](http://www.verlab.dcc.ufmg.br/semantic-hyperlapse/papers/Final_Draft_ECCVW_2016_Towards_Semantic_Fast_Forward_and_Stabilied_Egocentric_Videos.pdf) on the **First International Workshop on Egocentric Perception, Interaction and Computing** at **European Conference on Computer Vision Workshops** (EPIC@ECCVW 2016). It implements a semantic fast-forward method for First-Person videos with a proper stabilization method.

For more information and visual results, please access the [project page](http://www.verlab.dcc.ufmg.br/fast-forward-video-based-on-semantic-extraction).

## Contact ## 

### Authors ###

* Michel Melo da Silva - PhD student - UFMG - michelms@dcc.ufmg.com
* Washington Luis de Souza Ramos - MSc student - UFMG - washington.ramos@outlook.com
* João Pedro Klock Ferreira - Undergraduate Student - UFMG - jpklock@ufmg.br
* Mario Fernando Montenegro Campos - Advisor - UFMG - mario@dcc.ufmg.br
* Erickson Rangel do Nascimento - Advisor - UFMG - erickson@dcc.ufmg.br

### Institution ###

Federal University of Minas Gerais (UFMG)
Computer Science Department
Belo Horizonte - Minas Gerais -Brazil

### Laboratory ###

![VeRLab](https://www.dcc.ufmg.br/dcc/sites/default/files/public/verlab-logo.png)

**VeRLab:** Laboratory of Computer Vison and Robotics
http://www.verlab.dcc.ufmg.br

## Code ##

This project is a two-fold source code. The first fold¹ is composed of MATLAB code to describe the video semantically and to fast-forward it. A stabilizer proper to fast-forwarded video written in C++ using OpenCV is the second fold². You can run each fold separately.

### Dependencies ###

* MATLAB 2015a or higher
* Python 2.7 _(Tested with 2.7.12)_
* MATLAB Engine for Python
* OpenCV 2.4 _(Tested with 2.4.9 and 2.4.13)_
* Armadillo 6 _(Tested with 6.600.5 -- Catabolic Amalgamator)_
* Boost 1 _(Tested with 1.54.0 and 1.58.0)_
* Doxygen 1 _(for documentation only - Tested with 1.8.12)_

### Usage ###

**Before running the following steps, please go back to the project's main folder and execute step #7.**

If you don't want to read all the steps, feel free to use the **Quick Guide**. To see it, execute the first step and click on *Help Index* in the *Help* menu.

1.  **Running the Code:**

	Into the _PythonScripts_ directory, run the following command:
```
 user@computer:<project_path/PythonScripts>: python main.py
```

2. **Selecting the Video:**
	
	On the main screen, click on *OpenFile* in the *File* menu. Then select the video that you want to accelerate.
```
 The valid formats are: ".mp4" and ".avi"
```

3. **Choosing the Semantic Extractor**:

	After selecting the video, choose the semantic extractor that you want for your video. The extractors available are: _face_ and _pedestrian_.

4. **Choosing the SpeedUp:**

	After selecting the video, choose the speed-up that you want to apply.
```
 The speed-up rate needs to be an integer greater than 1.
```

5. **Setting the Weights:**

    4 weights control the way the video will be accelerated. They are:
	
| Weight | Description | Type | 			
|--------:|-------------|------|
| &alpha; | Tuple of weights related to the shakiness term in the edge weight formulation. | _Integer_ |
| &beta; | Tuple of weights related to the velocity term in the edge weight formulation. | _Integer_ |
| &gamma; | Tuple of weights related to the appearance term in the edge weight formulation. | _Integer_ |
| &eta; | Tuple of weights related to the semantic term in the edge weight formulation. | _Integer_ |
	
Select an integer for each weight. The first is for the semantic part and the second one for the non-semantic part. If you don't change anything, the default weights will be used. _That doesn't mean that they are the best for your video._

```
 The general formula is presented in the paper.
```

6. **Speeding-Up the Video:**
	
	After setting everything, click on the `Speed Up and Stabilize` button and check the progress on the screen that'll be opened.