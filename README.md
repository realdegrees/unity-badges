## Unity Badges

A REST API that returns an image containing a badge that can be used on GitHub to display specific stats about a Unity project.
I made this as a side project to improve the collaborative aspect in a [Unity project repo for a game engineering course at my Uni](https://github.com/realdegrees/ur-game-engineering).

Here is a live example of the badge using that repo:
<hr> 

<img src="https://unity-badges.realdegrees.dev/scene-changes/realdegrees/ur-game-engineering?label=Example%20Label" alt="Unity Badge" width="190px">  
<hr> 

### Endpoints

#### GET `/<badge>/<owner>/<repo>`
##### Displays the specified badge for the repo


### Badges
 - `scene-change`
 Shows an overview of all `.unity` files that have changes compared to develop together with their branch
 If a scene is being modified in multiple branches that scene is displayed with a warning.
