# imageProcessorWebApp
Basic Image Processing web app using flask and opencv

# [To run] 

make folder named uploads to store files after uploading and processing
install pyenv

Then,
In terminal -> 

$ pyenv exec python venv .venv

 source .venv/bin/activate (inLinxu) , in windows in may be in different folder run accordingly
 
 Now virtual python environment is active
 
 $ pip install (all required modules)
 
 see requrements in requirements.txt

$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run

Voila!! The application is now running on local server
Open preffered Browser (firefox/chrome)
http://127.0.0.1:5000/ - to open the app in browser

# [Features]

1.Convert to Binary

2.Constrast Stretching

3.Histogram Equalization in R G B and then Merge

4.Convert to Negative

5.Power level transform

6.Remove Noise using bilateralFiltering
