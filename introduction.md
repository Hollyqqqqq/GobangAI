### <center>GoBang Report</center>

#### 1. Preliminaries 

##### 1.1 Problem Description

Gobang is a kind of pure strategy chess game played by two people, usually the two sides respectively use black and white pieces, under the board line and the crossing point of the horizontal line, the first to form 5 sub-line winner.

Artificial intelligence (AI) is a new and comprehensive frontier science which is developing rapidly. Game theory is one of the main research fields of artificial intelligence. It involves reasoning technology, search method and decision planning in artificial intelligence. In this report, an intelligent Gobang system is designed to realize the game between human and computer.

##### 1.2 Problem Applications

This paper discusses and studies the design principle and implementation method of gobang algorithm, including data structure, game tree algorithm, Alpha beta pruning and evaluation function.

Studying the typical problem of artificial intelligence through game tree has the following advantages:

1. The game problem is limited to a small and typical scope, and it is easy to study deeply.

2. Game problem is a concentrated reflection of human intelligence, which is enough to provide new ideas for the real world methods and new models.

3. Expertise is easy to acquire.

4. Progress can be accurately demonstrated and demonstrated, and the advantages and disadvantages of different methods and models are easy  to compare.

#### 2.Methodology 

##### 2.1 Notation:

**eval** is "evaluate" or "evaluation" for short.

##### 2.2 Data Structure:

`chessboard` :  a two-dimensional list store chess pieces positions.

`chess_type*` :  a two-dimensional list store the count of chess type.

`*empty` : a list of chess board's empty positions that deserve to consider.

`score` (Hyper parameter): a two-dimensional list store the value of chess type.

`candidate_list` : a list of the most valuable positions which have found.

***** There are about 20 kinds of chess types (use black chess as example):

![1570629211622](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570629211622.png)

<center>Fig.0 (from cnblogs.com)</center>

I classify them by count and type.

For `live` type, the chess is continuous and no blocks in two ends.

For `run` type, there is one blank between two black points (call it jump) and no blocks in two ends.

For `sleep` type, there are two or more jumps between two black points or one or two block in two ends. 

So, we can tell different chess type by "live3" or "run4" and so on. Different chess type has different value. It is obviously that **value of live type >= run type >= sleep type**. 

There are also some certainly win chess type: 

live4,  (run4/sleep4) & (run4/sleep4), (run4/sleep4) & (live3/run3), (live3/run3) & (live3/run3) .

##### 2.3 Model Design:

Gobang seems to have a variety of moves, but if we extend each step of the movement, is a huge game tree.

Let's start with something simple. Consider a tic-tac-toe, not gobang. In **Fig.1** shows how to consider one movement of tic-tac-toe. 

* First step (player1), has 3 kinds of movement available. 

* And if he choose the first situation, then second step (palyer2) has 5 kinds of movement available.  

* And the rest can be done in the same manner. We can go down step by step and it forms a tree called game tree. 

* Until one player win. Then we can know the movement of each path is beneficial to the winner.

* So, we can draw the conclusion: **The first step we should consider the position that is more likely leading our part to win.**

  ==**But how to quantitatively measure "likely leading our part to win" ? ----------This is major problem to do a good move.**==


![查看源图像](https://cn.bing.com/th?id=OIP.WAxMtdO1rQHuVexejaWLbQAAAA&pid=Api&rs=1)

<center>Fig.1 (from bing.com)</center>

**Back to the gobang topic**, since its chess  board is much larger than tic-tac-toe's chess board. There are 15*15 = 255 positions. If the game ends after 50 movements and each step we only consider 10 positions. The time complexity will reach $O(10^{50})$. But in fact, there more positions and more steps need to be considered. So, **it is unpractical to go down the step by step until one player win**. But it is possible to see the game situation is favorable to whom after several movements. So, we change the major problem into:==**"Quantitatively measure "likely leading our part at favorable situation after several round."**==

The roughly process of deciding one move is as **Fig.2-a** shows:

![1570544422137](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570544422137.png)

<center>Fig.2-a &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Fig.2-b</center>For finding empty positions, it can be easily realize by python. So, I won't mention too much.

**1)** For finding empty positions, it can be easily realize by python. So, I won't mention too much.

**2)** And the algorithm use game tree to find the most valuable position is **MinMax algorithm and Alpha beta pruning** , which are implement in the function `min_max_decision()`.

When we go through this game tree it's pretty obvious how we're going to pick branches, as following shows:

![查看源图像](https://assignment.essayshark.com/blog/wp-content/uploads/2016/10/Minimax-alpha-bera-pruning-4.png)

<center>Fig.3 (from bing.com)</center>

In the tree:

The layer at which our part moves is called the MAX level, and in order to maximize our own benefits, the computer needs to choose the node with the highest score; The layer where the player moves is called the MIN layer. In this layer, the player will choose the node with the lowest score if he wants to maximize his own interests. That's where the name **minimax algorithm** comes from.

The score of each node is determined by its children, so the main work is to complete an evaluation function, which needs to give a more accurate score of the current situation. That is what `total_eval()` function does.

In the max layer, *alpha* stores the current maximum value of that max layer, and in the mini layer, *beta* stores the current minimum value of that min layer. If the value of the child node of the next node (B) of a min layer node (A), is less than or equal to the value of the current *beta*, then all the remaining nodes of node B need not be considered. Also, If the value of the child node of the next node (C) of a max layer node (D), is more than or equal to the value of the current *alpha*, then all the remaining nodes of node D need not be considered. This is called **Alpha beta pruning**. C1, C2, C3 are the pruning of the algorithm. By doing this, we don't need to search all the situations in the game tree. It can reduce a certain part of time.

**3)** For the total evaluation of chess situation, I use function `total_eval()` to implement. As mentioned in 2.2, there are many chess types and different type has different value. The idea of total evaluation is to count the changing chess types after several chess movements. And changing chess types relative to type scores that we can easily get the changing score of our part or opposite part. 

For example, in the following Fig.4:

![1570567971175](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570567971175.png)

<center>Fig.4</center>

If we go a white chess at (7,11) change the situation from left to the right, then for black player, he lost a run4 and gets nothing. But for white player, he lost a run2 ((4, 8) (5, 9)) and get a live3 ((4,8) (5,9) (7,11)). It's obviously that white player get benefit in the step. This can be calculate by exact score since each chess type has exact value.

**4)** Then we look at Fig2-b, there is another process `evaluate point value`. It can be easily understand that the total chess board evaluation  is a gather of each point evaluation. So this process is linked to the total evaluation. But besides this, point evaluation can be done before running game tree. After finding the empty positions, we evaluate all the point, and sort the points according to evaluate score by acceding order. So that, we can only choose the first several points to build the tree(In my design, I only choose first 4 points). This is another important pruning of the game tree. 

For point evaluation, we consider four directions of the point and then check the chess type in each direction to get the point value. Just as the following shows. 

![1570569919678](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570569919678.png)

<center>Fig.5</center>

##### 2.4 Detail of algorithms:

suppose I am black player, and enemy is white player.

<< pseudo-code of game tree algorithm >>:

```tx
def min_max_decision(chessboard, depth)

	def max_value(chessboard, old_chessboard, d, alpha, beta):
        if d == depth or someone win
        	return total_eval(chessboard, old_chessboard)
    	sort_empty[] <- find_sort_empty(chessboard)
        for each in sort_empty:
            chessboard[each] <- black
        	value <- max(value, min_value(chessboard, old_chessboard, d+1, alpha, beta))
            if value >= beta, return value
        	alpha = max(alpha, value)
    def min_value(chessboard, old_chessboard, d, alpha, beta):
        if d == depth or someone win
        	return total_eval(chessboard, old_chessboard)
    	sort_empty[] <- find_sort_empty(chessboard)
        for each in sort_empty:
            chessboard[each] <- black
        	value <- min(value, max_value(chessboard, old_chessboard, d+1, alpha, beta))
            if value <= alpha, return value
        	beta = min(beta, value)
            
	sort_empty[] <- find_sort_empty(chessboard)
	best_score <- -infinity
	best_action <- None
	beta <- infinity
	for each of the first 4 element in sort_empty:
		old_chess_board <- chess_board.copy
		chessboard[each] <- black
		value <- min_value(chessboard, old_chessboard, 1, best_score, beta)
		if value > best_score:
			best_score <- value, best_action <- each
            
	return best_action
```

<< evaluation functions >>:

```tx
def total_eval(chessboard, old_chessboard)
	update_pos[] <- find update positions by comparing chessboard with old_chessboard
    effect_points[] <- find points close to update positions that are within five grids distance of 4 directions
	for each of update_pos:
        if chessboard[each] == black
        	me_get <- point_eval(chessboard, each, black)
            me_lost <- point_eval(old_chessboard, each, black)
        elif chessboard[each] == white
            enemy_get <- point_eval(chessboard, point, white)
            enemy_lost <- point_eval(old_chessboard, each, white)
    total_value <- (me_get-me_lost)-(enemy_get-enemy_lost)
    return total_value
    
def point_eval(chessboard, point, color, chess_type)
	direction[] <- [1, 2, 3, 4] # 4 directions showed in Fig.5 
    point_value = 0
	for i = 1 to 4
		line[] <- extend point in one direction until meet enemy point or goes 5 grids, via this to form a line list
        point_value += point_value_1direction(line, color)
    if can find the certainly win chess type:
    	increase point_value by a large amount
    return point_value

def point_value_1direction(line, col) # col means color
	if len(line) < 5, return 0
	score <- 0
	sublist[] <- find a sublist of line which has length 5 and has maxmum count of points whose color = col
    (int)count <- number of point where sublist[i] = col
    (int)jump <- number of empty points of sublist between non-empty points.
    (bool)bolck <- whether the two boundary points (whose color = col) is blocked by enemy points or not
    if jump == 0 and !block: # live type
    	socore += live[count]
    elif jump == 1 and !block: # run type
        score += run[count]
    elif jump >= 2 or block: # sleep type
		score += sleep[count]
    return score
```



#### 3.Empirical Verification 

##### 3.1 Dataset:

Except for the data that carp platform supply, I use data that is download from gobang platform when I lose a game.  Or generate some special according to my thoughts by the two dimensional chessboard list, like the following fig shows:

![1570631249513](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570631249513.png)



##### 3.2 Performance measure:

In the point_eval function, each time consider 4 directions, and each direction need to do 5 times comparation. So, it is 20 times comparation. Suppose there are n points need to be evaluate each time. So it costs 20n times comparation. In my game tree, each step I consider only 4 points. And the depth of the tree is 4, which means I only consider 2 rounds of the game each time. And at leave node, there will be a total evaluation, which contains point evaluation. Thus time complexity for this is 64*20n times comparation.  And at most n = 255. It will cost a long time. So I first join one point into candidate_list just by point evaluation in order to avoid that the calculating time of game tree exceed 5 seconds and cause candidate_list empty error.

The following is the performance of my AI.

![1570631858937](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570631858937.png)

##### 3.3 Hyperparameters:

My value of different chess type changed from lab1 to lab3 is as following:

![1570632030313](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570632030313.png)

The total thought is **value of live type >= run type >= sleep type** and **count5 > count4 >= count3 >= count2 >= count1**

When my AI plays with other player, if it lose the game, I will analysis why I lose and what infect my AI to move the wrong position but not the expected position. Usually, it is because that two or more smaller value points may add up to more than the larger value points, which is not excepted. So I need to adjust the value little by little until reach a more stable situation.

##### 3.4 Experimental results:

![1570631858937](C:\Users\91426\AppData\Roaming\Typora\typora-user-images\1570631858937.png)

##### 3.5 Conclusion:

This paper discusses and studies the design principle and implementation method of gobang algorithm, including data structure, game tree algorithm, Alpha beta pruning and evaluation function.Basically, it can achieve a good gobang AI, which can be used for reference in the study of simple game. However, the search efficiency still needs to be improved, especially the algorithm of single point evaluation function.In addition, the depth and breadth of game tree can be increased after optimizing other parts.Achieve a better chess AI.

#### 4.Reference

[1]GitHub. (2019). *五子棋AI教程第二版二：博弈算法的前世今生 · Issue #12 · lihongxun945/myblog*. [online] Available at: https://github.com/lihongxun945/myblog/issues/12 [Accessed 9 Oct. 2019].

[2]"五子棋AI的思路 - 我是老邱 - 博客园", *Cnblogs.com*, 2019. [Online]. Available: https://www.cnblogs.com/songdechiu/p/5768999.html. [Accessed: 09- Oct- 2019].
