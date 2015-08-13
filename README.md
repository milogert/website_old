# Milo Gertjejansen's Personal Website.
My personal website.

# Hosting
The site is hosted at [milogert.com](milogert.com).

For beta features, head to [dev.milogert.com](dev.milogert.com).

# Running
The site uses Flask and WSGI to run. I don't think it will work as is (this is closer to the development version than the production version) but you certainly can try running through Apache or Nginx.

If you want to run as a program clone the repository, create a virutal environment, and install the packages in `requirements.txt` with `pip`. Once you have activated the virutal environment, run `python run.py` and browse to `localhost:5000`.

This will likely not work since the databases are not on your system. It's another thing I am working on.
