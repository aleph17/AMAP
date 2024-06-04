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
