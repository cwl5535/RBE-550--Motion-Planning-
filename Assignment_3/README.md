# RBE 550, Assignment 3
# Author: Colton Layhue

## Part 1 - Skid Drive Delivery Robot (Following Differential Drive Robot)
Currently follows A* workflow, where 20 neighbors of the current node are identified. The number of neighbors is determined by the `max_speed` value given to each of the wheels. These neighbors are each represented as a `State` object and have a cost attribute. Costs are determined using a the standard A* cost function, where cost for distance to next `State`, x, is affected by the Euclidean distance as well as the steering required. 


## Part 2 - Regular Truck 

## Part 3 - Truck with Trailer