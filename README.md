# About

Fitness tracking application for informal workout meetups occurring
at the Hacker Dojo. We used to keep track of our workouts on paper
but of course the hacker siren song called out for this process
to be appified somehow. 
 
# Hacking

Grab the Google App Engine SDK for Python from here:

[https://developers.google.com/appengine/downloads](https://developers.google.com/appengine/downloads)

Assuming the SDK is in your path, run the development server using 

    dev_appserver.py <path-to-dojo-fit> 

Take a look at the issues on GitHub for hints on what 
kind of things need to be done still.

# Status

This is just a prototype for the most part. A very early 
attempt at producing something that works.

# API

Example usage using curl

$ curl -XPOST http://localhost:8080/service/newsession -d ""
17

$ curl -XPOST http://localhost:8080/service/adduser -d "sid=17&user=dan"
$ curl -XPOST http://localhost:8080/service/newset/17 -d "user=dan&exercise=pullups&reps=10"
$ curl http://localhost:8080/service/session/17
{"exercises": ["pullups", "pushups"], "users": [{"exercises": {"pushups": [], "pullups": [10]}, "name": "dan"}]}dan@X200:~/Desktop/sandbox/dojofit$ 

