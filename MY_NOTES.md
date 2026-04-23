Implementing Flee
For every square, check all other squares iteratively like my collision.
If the other square is significantly larger like 20%, then it is considered a larger square
If the larger square is close enough it triggers the funciton
Change the vx vy of the smaller square

Implementing Chase
Use the same logic as the flee function as it already detects threats and can be used to detect targets.
Modify the flee function where under similar circumstances the larger square changes its vx and vy towards the smaller.