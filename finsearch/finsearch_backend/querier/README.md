# FinSearch Backend: Querier Microservice
The Querier microservice exposes REST API endpoints for the Frontend service to access data, and is served using Apache. The querier service parses the API requests received, and generates the queries in a format that can be used by our Embedder Microservice.

## Getting Started
### Prerequisites
This project was built to run on Python 3.9. Refer to the (Python installation page)[https://www.python.org/downloads/] for more instructions. Alternatively, if Anaconda is installed, a separate conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.9
```

The Querier microservice is served by Apache 2. If you wish to deploy the server locally:
1. Install Apache Server
    ```sh
    apt-get install apache2
    ```
2. Start Apache Process
    ```sh
    /etc/init.d/apache2 start
    ```
3. Verify Service is Running
    ```sh
    /etc/init.d/apache2 status
    ```

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the FinSearch Backend Querier Microservice directory
    ```sh
    cd finsearchIE/finsearch/finsearch_backend/querier/
    ```
3. Install Python packages
    ```sh
    pip install -r requirements.txt
    ```

## Local Development
To start the project locally:
1. Move into the FinSearch Backend Querier Microservice Application directory
    ```sh
    cd finsearchIE/finsearch/finsearch_backend/querier/app/
    ```
2. Run application
    ```sh
    python app.py
    ```

## Deployment
The Querier microservice is deployed on Apache2. We provide the following installation instructions

## Instructions for Running on Apache Server
We provide a version of the Querier microservice with Apache2 configurations to be hosted on a server. 
```
#  Restart Process
/etc/init.d/apache2 restart
```

### Configure Apache Server
1. Copy the files in [finsearchIE/finsearch_backend_query/apache/sites-available/](https://github.com/ValaryLim/finsearchIE/tree/main/finsearch_backend_query/apache/sites-available/) into `/etc/apache2/sites-available/` directory
2. Copy the files in [finsearchIE/finsearch_backend_query/apache/html/](https://github.com/ValaryLim/finsearchIE/tree/main/finsearch_backend_query/apache/html/) into `/var/www/html/` directory
3. Restart Apache2 by calling `/etc/init.d/apache2 restart`

## Built With
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.1.x/)
* [Apache](https://httpd.apache.org/)