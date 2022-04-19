# FinSearch Frontend
FinSearch Frontend is written in Javascript using the Vue.js framework. The application provides a responsive and aesthetically pleasing user interface that users can interact with to fetch data from FinSearch. It is intuitive and allows users to easily identify what parameters the service can accept and tweak.

## Getting Started
### Prerequisites
* npm
    ```sh
    npm install npm@latest -g
    ```
* Vue.js
    ```sh
    npm install vue
    ```
* Vuetify.js
    ```
    npm install @nuxtjs/vuetify -D
    ```

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the FinSearch Frontend directory
    ```sh
    cd finsearchIE/finsearch/finsearch_frontend/
    ```
3. Install NPM packages
    ```sh
    npm install
    ```

## Local Development
To start your project locally, run:
```
npm run serve
```

## Deployment
FinSearch Frontend is deployed using [surge](https://surge.sh/) at [http://finsearch.surge.sh/](http://finsearch.surge.sh). To deploy the application on Surge:

1. Move into the FinSearch Frontend directory
    ```sh
    cd finsearchIE/finsearch/finsearch_frontend/
    ```
2. Install surge
    ```sh
    npm install --global surge
    ```
3. Compile and minify project for production
    ```sh
    npm run build
    ```
4. Publish site
    ```
    surge
    ```
    Select `finsearch_frontend/dist/` as project path when asked.

## Built With
* [Vue.js](https://vuejs.org/)
* [Vuetify.js](https://vuetifyjs.com/en/)