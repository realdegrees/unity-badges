## Unity Badges

A REST API that returns an image containing a badge that can be used on GitHub to display specific stats about a Unity project.
I made this as a side project to improve the collaborative aspect in a [Unity project repo for a game engineering course at my Uni](https://github.com/realdegrees/ur-game-engineering).

It's a Flask API that uses the route and arguments to create a badge as a png file that can be embedded into e.g. READMEs in github. The badges are created by taking the data that was queried using the repo defined in the route and applying it to a jinja template.
The resulting html is rendered using a headless browser by playwright. The page is the screenshotted and cropped to return the final badge in the request.

Here is a live example of the badge using that repo:
<hr> 

<img src="https://unity-badges.realdegrees.dev/scene-changes/realdegrees/ur-game-engineering?label=Example%20Label" alt="Unity Badge" width="190px">  
<hr> 

### Endpoints

| Type | Route                        | Generic Url Args (Can be used for all badges)  |
|------|------------------------------|-------|
| GET  | `/<badge>/<owner>/<repo>`    | label |



### Badges
| Badge | Description | Custom Url Args |
|-|-|-|
| scene-change | Checks the diffs between feature branches<br>and a base branch (base argument (Default: develop)) for .unity files.<br>The modified Unity scene files are listed in the badge.<br>Possible conflicts between the scenes are highlighted. | base
