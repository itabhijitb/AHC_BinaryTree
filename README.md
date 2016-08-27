#Social Network

Suppose there is a social network of experts where each expert is associated with one or more skills. A collaborative task is one which requires a set of skills. And the team formation problem is to find a team of experts who are able to cover all the required skills and communicate with one another in an effective manner. The communication cost between 2 experts is the shortest distance between them in the given social network.

Given a task T with a required skillset, we need to find a team of experts [X, Y, Z…] such that among the members of the team we have collectively covered all the required skills with the minimum cost of communication. Discuss various approaches to solve it.

Hint: In large graphs a heuristic approach which may not give the most optimized solution but a reasonably good solution, is also acceptable.



#Input:

A weighted graph in adjacency matrix form where each node represents an expert, the value of a node represents the skills possessed by that expert and the weight of an edge represents the communication cost between two experts.



Expectation:

An algorithm and code with the analysis of time and space complexity.

Example:

D:\Projects\DoSelect\Amazon\SocialNetwork>python PB3.py < in.txt
ACO: cost = 7, path = [7, 9]
Nearest Neighbour: cost = 7, path = [0, 9, 6, 2, 4]
Brute Force: cost = 6, path = [9, 0, 3]
