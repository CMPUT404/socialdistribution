# 404 Social Distribution

[![Build Status](https://travis-ci.org/CMPUT404/socialdistribution.svg?branch=master)](https://travis-ci.org/CMPUT404/socialdistribution)

[App](http://socshizzle.divshot.io/)

[Project Specifications](https://github.com/abramhindle/CMPUT404-project-socialdistribution)

[API Documentation](https://github.com/CMPUT404/socialdistribution/wiki).

### Setup
Getting things up and running is a bit more complicated because we're running a separate purely restful backend and a React.js frontend.

### Frontend Installation
```bash
npm install
bower install
```
#### How To Run
You're going to need "gulp" to build our frontend. So you need to run `npm install -g gulp`. Then running the command below should automatically build everything and open a tab in your browser with the app running. By default the app is not configured to find our remote production api so you'll need to follow the instructions below on starting the api up as well.

```bash
gulp serve
```

### Backend Installation
```
pip install -r requirements
./manage.py migrate
```

#### Testing
```
./manage.py test
```

#### Libraries and Frameworks  
[Back End](https://github.com/CMPUT404/socialdistribution/blob/master/requirements.txt)  
[Front End](https://github.com/CMPUT404/socialdistribution/blob/master/package.json#L7-L49)
