# FinSearch Backend: Querier Microservice
The Querier microservice exposes REST API endpoints for the Frontend service to access data, and is served using Apache. The querier service parses the API requests received, and generates the queries in a format that can be used by our Embedder Microservice.

## Getting Started
### Prerequisites
This project was built to run on Python 3.9. Refer to the [Python Installation Guide](https://www.python.org/downloads/) for more instructions. Alternatively, if Anaconda is installed, a separate conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.9
```

The Querier microservice is served by Apache 2. If you wish to deploy the server locally:
1. Install Apache Server
    ```sh
    apt-get install apache2
    sudo apt-get install libapache2-mod-wsgi-py3
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
    cd finsearchIE/finsearch/finsearch_backend/querier/finsearch_querier/
    ```
2. Run application
    ```sh
    python app.py
    ```

## Deployment
The Querier microservice is deployed on Apache 2. To run the application on the Apache server:

1. Copy the [`finsearch_querier` app](finsearch_querier/) directory into your local `/var/www/html` directory
    ```sh
    sudo cp -r querier_app /var/www/html/
    ```
2. Copy the [`FinsearchQuerier.conf` file](FinsearchQuerier.conf) into the `/etc/apache2/sites-available` directory
    ```sh
    sudo cp FinsearchQuerier.conf /etc/apache2/sites-available/
    ```
3. Retrieve your Machine's IP Address
    ```sh
    curl ifconfig.me
    ```
4. Retrieve your Python path
    ```sh
    which python
    ```
5. Modify the `FinsearchQuerier.conf` file in  `/etc/apache2/sites-available`:
    - Replace the ServerName with your Machine's IP Address
    - Replace `python-path` variable in WSGIDaemonProcess (Line 6) with your Python path retrieved
    - Replace `python-home` variable in WSGIDaemonProcess (Line 6) with your Python home (e.g. If your Python path shows `/home/vlim/anaconda3/bin/python`, then your Python home will be `/home/vlim/anaconda3`)
6. Enable Finsearch Querier
    ```sh
    sudo a2ensite FinsearchQuerier.conf
    ```
7. Disable Default Site
    ```sh
    a2dissite 000-default.conf
    ```
8. Restart the Apache Process
    ```sh
    /etc/init.d/apache2 restart
    ```

## Built With
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.1.x/)
* [Apache](https://httpd.apache.org/)