# DFA-Minimization
DFA minimization done using Unger-Paulla showing each step.

### File representing automate

Sample automate file:

```
6-zz
-4z-
41zz
51y-
2--z
53y-
```

would represent in such Mealy Automate:

Q  |   |  a|  b|   |  a|  b
:-:|:-:|:-:|:-:|:-:|:-:|:-:
1  |   |  6|  -|   |  z|   z
2  |   |  -|  4|   |  z|   -
3  |   |  4|  1|   |  z|   z
4  |   |  5|  1|   |  y|   -
5  |   |  2|  -|   |  -|   z
6  |   |  5|  3|   |  y|   -

in order to create Moore's Automate from such Automate:


Q  |   |  a|  b|   |  f
:-:|:-:|:-:|:-:|:-:|:-:
1  |   |  6|  -|   |  z
2  |   |  -|  4|   |  z
3  |   |  4|  1|   |  z
4  |   |  5|  1|   |  y
5  |   |  2|  -|   |  -
6  |   |  5|  3|   |  y

simply double the f column:

```
6-zz
-4zz
41zz
51yy
2---
53yy
```

### Running the code

```zsh
$ python3 automat.py $1 $2
```

We need two arguments:
$1 - amount of outputs (letters)
$2 - name of our automate file

So in order to call my automate:

```
autmat.txt
6-zz
-4z-
41zz
51y-
2--z
53y-
```

I would type:

```sh
$ python3 automat.py 2 autmat.txt
```

### Sample results

```
AUTOMATE:
 |ab|ab
-----------------
1|6-|zz
2|-4|z-
3|41|zz
4|51|y-
5|2-|-z
6|53|y-

TRIANGLE:
2|√   
3|46  |14  
4|X   |X   |X   
5|26  |√   |24  |25  
6|X   |X   |X   |13  |25  
 |1   |2   |3   |4   |5   

Filtering triangle...
32 was deleted beacuse of "X" in 41
53 was deleted beacuse of "X" in 42
51 was deleted beacuse of "X" in 62
TRIANGLE FILTERED:
2|√   
3|46  |X   
4|X   |X   |X   
5|X   |√   |X   |25  
6|X   |X   |X   |13  |25  
 |1   |2   |3   |4   |5   

SEARCH:
5|56 
4|56 45 46 
3|456 
2|456 25 
1|456 25 12 13 

456 25 12 13
Q1  Q2 Q3 Q4

FULL COVERAGE POSSIBILITIES:
Q1Q2Q4 Q1Q3Q4 Q1Q2Q3Q4

CHECKING POSSIBLE COVERAGE: Q1 Q2 Q4

 |Q1 |Q2|Q4
 |456|25|13
-------------------
a|525|-2|64
b|1-3|4-|-1

  |ab|ab
-----------------
P1|23|yz
P2|21|zz
P3|13|zz

AUTOMATE OK
```

#### ToDo
- [ ] resign from forcing user to give number of letters
- [ ] fix bug in `search` algorythm that sometimes causes the programm not to find the absolute minimum automate






