# AMAP
As Much data As Possible

## Task


 Nanoparticles functionalized as surface enhancers for Raman spectroscopy have emerged as a promising technology for imaging, sensing, and catalysis. In particular, gold nanostars have grown appealing for their resonant mode tunability and intense scattered electric fields at the tips of the spikes upon interaction with impinging radiation. To achieve controllable results, it is important to understand the factors affecting the final result of particle synthesis. However doing all the measurements manually is quite time-consuming, which partially hampers the speed of progress in this field. Automatization of this process could greatly enhance synthesis protocols. 

## Target


 Develop a Computer Vision algorithm and a Deep Learning model to segment and quantitatively analyze individual nanostars - measure length and width of branches, dimensions of cores, interparticle distances (clustering),  and adjacent branch angles. 

## Input


 The provided input is TEM (Transmission Electron Microscopy) images (4096 x 4096) in grayscale. The image format is TIF.


## Results


As of April 2024, the segmentation and quantitative analysis of nanostars not overlapping with each other have been finished. However, when the stars’ branches touch each other, the problem becomes harder as it requires separate segmentation of individual nanostars. The plan is to manually segment pictures with VGG Image Annotator and feed them into a Deep Learning model. There are multiple models being considered - Mask R-CNN, SSD+MobileNetV2, SOLO, YOLAct, and PolarMask.

**Preliminary plan for the model:**
The model, or there can be a need for multiple models, to be built is meant to segment the cores of the nanostars and draw skeletons of branches as lines. There should be 4 channels in the output:
 - background (white)
 - nanostar core (red)
 - nanostar branch (blue)
 - connecting point of a core and branch (green)
The plan is to build three specialized models: one for background and nanostar core detection, the other for nanostar branch skeletonization, and the remaining to separate individual nanostars as separate.

Example nanostar TEM image:
![024](https://github.com/user-attachments/assets/8276bb77-12b7-4321-97b8-a17734d77ba4)

Expected output from the model:
![Screenshot from 2024-10-28 11-41-04](https://github.com/user-attachments/assets/5e0b07fb-7e07-4cb5-8b8e-ad9bb7d70a69)

