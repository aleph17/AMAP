# AMAP
As Much data As Possible

## Task

---

 Nanoparticles functionalized as surface enhancers for Raman spectroscopy have emerged as promising technology for imaging, sensing and catalysis. Especially gold nanostars have grown appealing for their resonant mode tunability and intense scattered electric fields at the tips of the spikes upon interaction with impinging radiation. To achieve controllable results, it is important to understand the factors affecting the final result of particle synthesis. But doing all the measurements manually is quite time consuming, which partially hampers the speed of progress in this field. Automatization of this process could greatly enhance synthesis protocols. 

## Target

---

 Develop a Computer Vision algorithm and a Deep Learning model to segment and quantitatively analyze individual nanostars - measure length and width of branches, dimensions of cores, interparticle distances (clustering),  and adjacent branch angles. 

## Input

---

 Provided input is TEM (Transmission Electron Microscopy) images (4096 x 4096) in gray scale. Image format is TIF with __ nm/pixel scale.

![GNS_01_t24h_H2O 1024 Camera Ceta 120 kx 0001 Ceta-min.jpg](https://prod-files-secure.s3.us-west-2.amazonaws.com/ee1154a0-001a-4cf8-90f4-a9e95b1a2c15/622234a3-9305-4667-82f4-d0238606d01c/GNS_01_t24h_H2O_1024_Camera_Ceta_120_kx_0001_Ceta-min.jpg)

## Results

---

As of April 2024, segmentation and quantitative analysis of nanostars not overlapping with each other have been finished. However, when the stars’ branches touch each other, the problem becomes as harder as it requires separate segmentation of individual nanostars. So far, SAM (Segment-Anything by Meta) has been used, but it didn’t give needed results. Future plan is to manually segment pictures and feed it into Deep Learning model, preferably utilizing transfer learning.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/ee1154a0-001a-4cf8-90f4-a9e95b1a2c15/7dbc3c44-0a01-4443-84d8-14569385512a/Untitled.png)
