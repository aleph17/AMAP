# AMAP
As Much data As Possible

## Task


 Nanoparticles functionalized as surface enhancers for Raman spectroscopy have emerged as a promising technology for imaging, sensing, and catalysis. In particular, gold nanostars have grown appealing for their resonant mode tunability and intense scattered electric fields at the tips of the spikes upon interaction with impinging radiation. To achieve controllable results, it is important to understand the factors affecting the final result of particle synthesis. However doing all the measurements manually is quite time-consuming, which partially hampers the speed of progress in this field. Automatization of this process could greatly enhance synthesis protocols. 

## Target


 Develop a Computer Vision algorithm and a Deep Learning model to segment and quantitatively analyze individual nanostars - measure length and width of branches, dimensions of cores, interparticle distances (clustering),  and adjacent branch angles. 

## Input


 The provided input is TEM (Transmission Electron Microscopy) images (4096 x 4096) in grayscale. The image format is TIF.


## Results


As of April 2024, the segmentation and quantitative analysis of nanostars not overlapping with each other have been finished. However, when the stars’ branches touch each other, the problem becomes harder as it requires separate segmentation of individual nanostars. So far, SAM (Segment-Anything by Meta) has been used, but it hasn’t given the desired results. The plan is to manually segment pictures and feed them into a Deep Learning model, preferably utilizing transfer learning.

As of August 2024, a part of the data processing is completed, and a sample U-net to be used to segment the nanostars is prepared. What's left is to manually prepare the data to be fed into the model. 

**Preliminary plan for the model:**
The model, or there can be a need for multiple models, to be built is meant to segment the cores of the nanostars and draw skeletons of branches as lines. There should be 4 channels in the output:
 - background
 - nanostar
 - nanostar core
 - nanostar branch
The plan is to build three specialized models: one for background and nanostar core detection, the other for nanostar branch skeletonization, and the remaining to separate individual nanostars as separate.

Example nanostar TEM image:
![024](https://github.com/user-attachments/assets/8276bb77-12b7-4321-97b8-a17734d77ba4)

Expected output from the first model:
![024 (1)](https://github.com/user-attachments/assets/22ca5d6c-7640-4677-9517-a59756fd2455)
(The preparation of the segmented data to be fed into the model can be further simplified by applying Gaussian filter and using it as a mask to mark the rough background.)

Expected output from the second model (it may need to use an approach of zoom-in and out concurrently):
![024 (2)](https://github.com/user-attachments/assets/5a3f8943-9797-4d01-98e6-6ca707c7bd17)
The items on the right bottom corner of the image are meant to be erased for cleanliness of the data.

Expected out from the third model:
![024 (4)](https://github.com/user-attachments/assets/1f2fa5dc-3962-4ef3-8f2d-3258313a5597)
The purple dots are there to mark the home core of a branch.

Once the models give the final output, the plan is to use a CV algorithm to separate nanostar structures individually and measure their core area, branch length.

As the final addition to the project a UI is planned to be implemented so that the user can delete unwanted length and core estimations.
