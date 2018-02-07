# Faces or Places
This git repository contains my submission for the Onfido Tech Test. This README gives an overview of the approach of to
tackling the problem. There also exist two saved Jupyter notebooks as HTML files:

image_conversion.html - the file which reduces the image sizes and converts to numpy arrays which are pickled.
train_classifier.html - where the training of the classifier was done.

To see the server logic, look in server.py.

The classifier was deployed to Heroku to test the working server. It however only currently accepts .jpg images, so apologies for that if you have to convert your image to .jpg. Images can be uploaded one at a time. It also goes to sleep if it hasnt had many requests in a while, so do be a little patient with your first upload.

No images have been uploaded, so running the actual training wont work unless you populate the the correct folders.

## Approach
My approach to this task followed these steps. The approach was considered in light of a pressing deadline.

1) Research Potential Data sources online.
2) Convert data into manageable format.
3) Get a cheap classifier working on small amounts of data to see if any signal.
4) Attempt to deploy cheap classifier to server to see if any pitfalls there.
5) Source more data.
5) Optimise Classifier.
6) Deploy best classifier to Heroku.

### Step 1: Research Data Sources.
Ideally a source like ImageNet would have been fantastic for this, however, I could not get access to it.
Luckily, scikit learn have a readily available image data base. Concerning the places, I downloaded a 
chrome extension that bulk downloads images from your screen. It also allows you to deselect innapropriate images
helping massively with the issue of false positives. Multiple 'place' terms were used such as 'monument', 'landscapes'
'city' and 'town'.

### Step 2: Convert Data into manageable format.
An issue is that not all images are the same size. So an approach was taken whereby an image is reduced in size
to a smaller width and height. This uses the python package 'resize-image'. Conveniently, it does not just crop the photo
it also keeps the aspect ratio. This results in blurrier images but they are all now the same size, with a manageable
feature dimension of width x height x 3. Where the 3 are the RGB channels. 100 x 100 x 3 was chosen.

### Step 3: Cheap Classifier on small amounts of data.
The pressing deadline of the task made me take the decision to simply get a cheap and lightweight classifier working.
Notably, Random Forest commonly fits this bill and are very easy to implement. The results were also a lot more accurate
than I had expected. This was done with simple 2 fold Cross-validation and then application to the test set. Preliminary
hyper-parameter searches were done, but with no real depth.

### Step 4: Deploy Cheap Classifier.
Again, due to time constraints, it was prudent to deploy this classifier to see the potential pitfalls of deployment.
A very lightweight server framework of Python's 'Flask' was chosen for its sheer simpilicity. Then, research was done in
to how to submit jpeg images via command line. Curl has such a functionality. The server was constructed to easily
accept a HTTP request with a JPEG attached. The classifier is stored using pickle. The accepted jpeg is then converted
into the correct format and the classifier predicts it. The server then responds simply with 'face' or 'place'. The design of
this server was aimed to be as simple as possible. Ideally, the server code does not have to change at all between subsequent retrains of the model, so steps were taken to keep the server simple.

### Step 5: Source more data.
The remarkable performance of the classifying on the data after very little engineering made me suspect that perhaps
the classifier might not be recognising faces, but perhaps other features due to the distribution that the faces were drawn
from. This meant looking for other data sources to make sure this was not happening. After adding faces and pictures 
drawn from other distributions, the classifier still seemed to perform very well. The performance on the images
for which onfido said the 'private' set was ok for both face and places (although admittedly a
tiny dataset), suggesting maybe that the classifier would generalise well and wasnt overfitting a specific distibution of images. Ended up with 465 face images and 350 place images.

### Step 6: Optimise Classifier.
Very little hyperparameter search was done to train the cheap classifier, so here I decided to do a much more in depth
scan of parameters to improve performance. The training score was at 100% accuracy, which suggested high variance, even though
cross validation was employed. However, Random Forests are normally very good with avoiding overfitting because they select
random subsets of features. I decided to try a different algorithm, K Nearest Neigbhours, to compare its performance.

### Step 7: Deploy Best Classifier.
The server has been deployed to heroku and accepts .jpg files. You can also test a local version. Instructions for testing it are below.

## Instructions for testing live Heroku hosted Classification Server
```
curl -X GET -F 'image=@path-to-your-image.jpg' http://faces-or-places.herokuapp.com/upload
```
The server will respond with either 'face' or 'place'. Unfortunately, I only allowed functionality for .jpg images. So apologies for that if your test images now need to be converted. Furthermore, the image must be greater than 100x100 in size.

## Instructions for deploying locally
Firstly, install python packages in requirements.txt.
Then run:
```
$ gunicorn server:app
```
This will start the app listening on port 8000.

To upload an image to the local server and classify it, use curl.
```
$ curl -X POST -F 'image=@path-to-your-jpg-image.jpg' localhost:8000/upload
```

## Improving the Classification Results
1) The classifier was not trained on a huge amount of data. Collecting more images from more distirbutions would most likely help performance and generalisation. The final test on a completely different source for the faces and the places showed a drop in performance, suggesting that the original distribution did not generalise well.

2) Combined with more data, training a Convolutional Neural Net on the data would also likely improve results. This would also add significant amounts of time to the training process however.

3) Reduce the images to larger sizes. For this test, the images were reduced to 100 x 100. The classification would most likely increase with a greater resolution.

4) Apply image Scaling. No feature scaling was used for this project. Although Random Forests dont really need scaling, it might have helped in conjunction with other algorithms.

5) Image manipulation. Methods such as adjusting for lighting might have helped here to help with the darker images.

6) Greater Hyper Parameter Searching would also quite possibly help.


## Server Improvements
1) Allow ability to upload multiple files at onces and return the classified results all in one go.
2) Ability to upload non .jpg formats.
3) Allow images of all sizes to be uploaded.





