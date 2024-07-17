Solution for mirror maze problem.

Usage is:
`python main --file PATH_TO_MAZE_DEFINITION_FILE`

General algorithm is to create lists of active mirrors possible in each row/column for each direction of up/down/left/right.
This allows for finding the next mirror to hit to be found by binary search (implemented using `bisect` module).
Binary search has the advantage of allowing the board size to scale and 
runtime to be constrained more by the number of mirrors hit.

This code also checks for potential infinite loops in the reflection and raises an exception if detected.

Ideally there would be tests, but I did not spend the time to write them.