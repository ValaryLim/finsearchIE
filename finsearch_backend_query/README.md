# FinSearch Backend Querier Microservice
The Querier microservice exposes REST API endpoints for the frontend services to access data, and is served using Apache. It is deployed on a server from the NUS School of Computing, and is written in Python, relying on the Flask framework. The Querier service parses the API requests received and generates the queries in a format that can be used by our Embedder microservice.

## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.7
```

A [requirements.txt](https://github.com/ValaryLim/finsearchIE/tree/main/finsearch_backend_query/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```

## Usage
Run the following commands to enter the conda environment and start the application:
```bash
conda activate finsearch_backend_querier
python app.py
```

## Instructions for Running on Apache Server
We provide a version of the Querier microservice with Apache2 configurations to be hosted on a server. 
### Install Apache Server
```bash
# Install Apache
apt-get install apache2

# Start Apache Process
/etc/init.d/apache2 start

# Verify Service is Running
/etc/init.d/apache2 status

# Restart Process
/etc/init.d/apache2 restart
```

### Configure Apache Server
1. Copy the files in [finsearchIE/finsearch_backend_query/apache/sites-available/](https://github.com/ValaryLim/finsearchIE/tree/main/finsearch_backend_query/apache/sites-available/) into `/etc/apache2/sites-available/` directory
2. Copy the files in [finsearchIE/finsearch_backend_query/apache/html/](https://github.com/ValaryLim/finsearchIE/tree/main/finsearch_backend_query/apache/html/) into `/var/www/html/` directory
3. Restart Apache2 by calling `/etc/init.d/apache2 restart`