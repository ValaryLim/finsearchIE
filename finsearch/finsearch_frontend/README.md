# FinSearch Frontend
FinSearch Frontend is deployed using [surge](https://surge.sh/) at [http://finsearch.surge.sh/](http://finsearch.surge.sh). It is written in JavaScript using the Vue.js framework. This frontend application provides a responsive and aesthetically pleasing user interface that users can interact with to fetch data from FinSearch.

## Project Setup
Run the following command to install the required packages.
```
npm install
```
### Compiles and Hot-Reloads for Development
```
npm run serve
```
### Compiles and Minifies for Production
```
npm run build
```
### Lints and Fixes Files
```
npm run lint
```
### Customize Configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Hosting on Surge
### Install Surge
```
npm install --global surge
```
### Host Site
1. Move into this project directory
2. Run `npm run build` to compile and minify the application for production
3. Run `surge` and Select  `finsearch_frontend/dist/` as Project Path