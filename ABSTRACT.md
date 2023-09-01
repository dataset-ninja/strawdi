**StrawDI: The Strawberry Digital Images Data Set** сontains 8000 images of strawberries, taken from 20 plantations, within an approximate area of 150 hectares, in the province of Huelva, Spain. The plantations were not changed in any way for the experiment and the images were taken from real production conditions during a full picking campaign (from mid-December 2018 to early May 2019).

The capture device used was a Samsung Galaxy S7 Edge smartphone attached to an extendable arm. In order to build a data set close to the target application, the images were taken under different conditions of brightness, at a distance of approximately 20 cm from the ridge, at about 35 +-10 cm height and an approximate angle of 25 +-10º. The images have a 4032x3024 resolution and are stored in a JPEG format.

<img src="https://github.com/supervisely/supervisely/assets/78355358/febce694-9cc5-411e-b594-2da769375ae2" alt="image" width="800">

From the total set of images that make up the StrawDI data set, <i>3100 images have been selected at random</i>. For each of these images, a ground truth labelled image has been manually generated containing the individual segmentation of all the strawberries appearing in the image.

To reduce the computational demands on the models, the images have been rescaled to 1008 x 756 and stored in PNG format. This set of images constitutes the **StrawDI_Db1** database. This database is divided into *train* (2800 images), *validation* (100 images) and *test* (200 images) subsets.

The image labelling process has been validated by three blind reviews of the data with four reviewers, thus guaranteeing the quality of the segmentation. The criterion followed in the labelling process consists of creating as accurate a mask as possible for each of the strawberries appearing in the image, including extreme cases such as strawberries that are almost imperceptible due to distance, occlusions, being at the edges of the image or still unripe.
