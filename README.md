# How to
Before running or deploying this application, install the dependencies using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -t lib -r requirements.txt
    
Then use to deploy:

    gcloud app deploy
    
And then to browse the app:

    gcloud app browse

To debug use:
    
    gcloud app logs read
