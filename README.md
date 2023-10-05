# Spherical-Grid-Generator

This plugin for Visual Components lets the user determine the size and density of a spherical grid.
It is designed to test the volumetric accuracy of a metrology system through the whole working volume
of a robot cell. Using Visual Components this can be done with any robot manufacturer the program has access 
to.

User Inputs explained
Sphere Radius: The radius of the sphere that will be generated
point spacing X, Y, Z: The space/ travel between each point in the respective direction.
Z Cutoff: Removes points below this layer e.g. input the height of the ground
Void Radius: Does not generate points in this area e.g. close to the robot
Rx, Ry, Rz: Rotation on the points
Speed: Robot speed
Linear/Joint: Points will be linear or joint moves.

To use - put this file into your My Commands folder held in your Visual Components folder.
