###Victim World
Here we have a working gazebo world with victims in it. This world file can be used in Robocup virtual rescue competitions.
For using this world you should first copy all file inside `models` folder to your `~/.gazebo/models` directory.
Then locate the world (from `worlds` folder) somewhere like `~/GazeboTest/victim_world.world` and bring it up in Gazebo with 
this command:
```
gazebo ~/GazeboTest/victim_world.world
``` 

#### Using for your robots
For usuing this world with a robot spwaned in it you should change the `world_name` parameter in your robot's 
launch file and change it to this (`~/GazeboTest/victim_world.world`) world and run it with `roslaunch` command.