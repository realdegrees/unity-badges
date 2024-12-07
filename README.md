# Unity Badges

## Description
A REST API that returns an image containing a badge that can be used on GitHub to display specific stats about a Unity project.
I made this as a side project to improve the collaborative aspect in a [Unity project repo for a game engineering course at my Uni](https://github.com/realdegrees/ur-game-engineering).

It's a Flask API that uses the route and arguments to create a badge as a png file that can be embedded into e.g. READMEs in github. The badges are created by taking the data that was queried using the repo defined in the route and applying it to a [**Jinja**](https://jinja.palletsprojects.com/en/stable/) template.
The resulting html is rendered using a headless browser by [**Playwright**](https://github.com/microsoft/playwright). A cropped screenshot of the page shows the final badge which is then returned in the response.

Basic Caching using Flask-Caching and redis and a rate limiter using Flask-Limiter are included.
If unable to connect to redis the app defaults to in-memory caching.
Launching the app with [start.sh](./start.sh) uses gunicorn to run 4 worker processes running the app.

<hr>

Here is a live example of the [*scene-changes*](./badges/scene-changes/) badge using the [**unitystation**](https://github.com/unitystation/unitystation) repo as an example:

<img src="https://unity-badges.realdegrees.dev/scene-changes/unitystation/unitystation?label=Unitystation%20Scene%20Conflicts" alt="Unity Badge" width="300px"> 

## Requirements
#### Playwright Setup
While playwright is part of the [requirements](./requirements.txt) it needs to install dependencies and the chromium browser before launching the app. This is automated in the [Dockerfile](./Dockerfile) and [packages](https://github.com/realdegrees/unity-badges/pkgs/container/unity-badges) if deploying with docker.  
`playwright install-deps`  
`playwright install chromium`

 
 

## Endpoints

| Type | Route                        | Generic Url Args (Can be used for all badges)  |
|------|------------------------------|-------|
| GET  | `/<badge>/<owner>/<repo>`    | label |



## Badges
| Badge | Description | Custom Url Args |
|-|-|-|
| scene-change | Checks the diffs between feature branches<br>and a base branch (base argument (Default: develop)) for .unity files.<br>The modified Unity scene files are listed in the badge.<br>Possible conflicts between the scenes are highlighted. | base
