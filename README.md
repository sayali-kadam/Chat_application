# What is this?

A simple sample app for the Messaging App project at branch.co

# How do I get started?
## Prerequisites
We assume you have the following installed already:
  * Python 3 (we tested with 3.7, the latest major version as of April 2019),
    including the virtualenv tool. Installation instructions
    [here](https://docs.python-guide.org/starting/installation/)
  * Postgres (we used Postgres 10.4, but newer or older versions should also
  work). Installation instructions for all platforms can be found
  [here](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup). Alternatively,
  a simple SQLite database could also work.


## Setup

  * Clone the repo and navigate into the top-level directory.
  * Create a virtual environment (venv) for installing Python packages, then
  activate it and install all required packages:
  ```bash
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
  * Make sure that Postgres is running: `ps x | grep /bin/postgres` should
    return something along the lines of `/usr/local/opt/postgresql/bin/postgres
    -D /usr/local/var/postgres`. If it isn't, follow installation and
    troubleshooting instructions above.
  * Create the database: `createdb customer-service-messaging`
  * Run the setup script: `python init_db_and_populate_with_testdata.py`
  * Start the server: `FLASK_APP=app.py FLASK_DEBUG=1 flask run`
  * Navigate to http://localhost:5000/admin/customers to see the agent
  interface.
  * Navigate to http://localhost:5000/customer_test to submit customer messages.
