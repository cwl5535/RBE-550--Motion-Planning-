 # Running the Code


 Author: Colton Layhue, Assignment 2 - RBE 550 Motion Planning - Forward Search Planners, Worcester Polytechnic Institute, Spring 2023


In order to run the provided scripts, please ensure that the following files are installed: 

- `0_coverage.npy`
- `25_coverage.npy`
- `50_coverage.npy`
- `65_coverage.npy`
- `flatland_assignment.py`
- `obstacle_field.py`


Next, open the `flatland_assignment.py` file and navigate to lines 370-373. The following variables can be edited for specific use cases: 

- grid_size: `int` - Size of environment. If desired size is 128x128, then `grid_size` = 128
- goal_location: `tuple` - coordinate location of desired location for robot to achieve
- test: `string` - This is to determine which search method to perform. Note "static plots" is to create the same obstacle fields for all search methods. You should not have to use this one. `test` can be "BFS", "DFS", "dijkstra", or "random"
- obstacle_file_location: `string`: This is the location of the `.npy` files listed above. These are presaved environment files to enable all the search algorithms to be used on the same obstacle fields. 


Once all inputs above have been changed accordingly, you can run `flatland_assignment.py`. Note: the goal location has been made (25,25) to help with processing time. The program will still take some time for coverage such as 0. The program should print all information (Coverage, What Searach is beginning, Goal Location, Whether goal was achieved, and iterations) once a search has been completed. The program will complete a search for all obstacle densities (0%, 25%, 50%, 65%).

Happy Searching! :)
