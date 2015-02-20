Connect n ropes with minimum cost
---------------------------------

There are given n ropes of different lengths, we need to connect these
ropes into one rope. The cost to connect two ropes is equal to sum of
their lengths.<span id="more-130846"></span> We need to connect the
ropes with minimum cost.

For example if we are given 4 ropes of lengths 4, 3, 2 and 6. We can
connect the ropes in following ways.  
 1) First connect ropes of lengths 2 and 3. Now we have three ropes of
lengths 4, 6 and 5.  
 2) Now connect ropes of lengths 4 and 5. Now we have two ropes of
lengths 6 and 9.  
 3) Finally connect the two ropes and all ropes have connected.

Total cost for connecting all ropes is 5 + 9 + 15 = 29. This is the
optimized cost for connecting ropes. Other ways of connecting ropes
would always have same or more cost. For example, if we connect 4 and 6
first (we get three strings of 3, 2 and 10), then connect 10 and 3 (we
get two strings of 13 and 2). Finally we connect 13 and 2. Total cost in
this way is 10 + 13 + 15 = 38.

**We strongly recommend to minimize the browser and try this yourself
first.**  
 If we observe the above problem closely, we can notice that the lengths
of the ropes which are picked first are included more than once in total
cost. Therefore, the idea is to connect smallest two ropes first and
recur for remaining ropes. This approach is similar to [Huffman
Coding](http://www.geeksforgeeks.org/greedy-algorithms-set-3-huffman-coding/).
We put smallest ropes down the tree so that they can be repeated
multiple times rather than the longer ropes.

Following is complete algorithm for finding the minimum cost for
connecting n ropes.  
 Let there be n ropes of lengths stored in an array len[0..n-1]  
 1) Create a min heap and insert all lengths into the min heap.  
 2) Do following while number of elements in min heap is not one.  
 ……a) Extract the minimum and second minimum from min heap  
 ……b) Add the above two extracted values and insert the added value to
the min-heap.  
 3) Return the value of only left item in min heap.

Following is C++ implementation of above algorithm.

    // C++ program for connecting n ropes with minimum cost
    #include <iostream>
    using namespace std;

    // A Min Heap:  Collection of min heap nodes
    struct MinHeap
    {
        unsigned size;    // Current size of min heap
        unsigned capacity;   // capacity of min heap
        int *harr;  // Attay of minheap nodes
    };

    // A utility function to create a min heap of given capacity
    struct MinHeap* createMinHeap(unsigned capacity)
    {
        struct MinHeap* minHeap = new MinHeap;
        minHeap->size = 0;  // current size is 0
        minHeap->capacity = capacity;
        minHeap->harr = new int[capacity];
        return minHeap;
    }

    // A utility function to swap two min heap nodes
    void swapMinHeapNode(int* a, int* b)
    {
        int temp = *a;
        *a = *b;
        *b = temp;
    }

    // The standard minHeapify function.
    void minHeapify(struct MinHeap* minHeap, int idx)
    {
        int smallest = idx;
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;

        if (left < minHeap->size &&
            minHeap->harr[left] < minHeap->harr[smallest])
          smallest = left;

        if (right < minHeap->size &&
            minHeap->harr[right] < minHeap->harr[smallest])
          smallest = right;

        if (smallest != idx)
        {
            swapMinHeapNode(&minHeap->harr[smallest], &minHeap->harr[idx]);
            minHeapify(minHeap, smallest);
        }
    }

    // A utility function to check if size of heap is 1 or not
    int isSizeOne(struct MinHeap* minHeap)
    {
        return (minHeap->size == 1);
    }

    // A standard function to extract minimum value node from heap
    int extractMin(struct MinHeap* minHeap)
    {
        int temp = minHeap->harr[0];
        minHeap->harr[0] = minHeap->harr[minHeap->size - 1];
        --minHeap->size;
        minHeapify(minHeap, 0);
        return temp;
    }

    // A utility function to insert a new node to Min Heap
    void insertMinHeap(struct MinHeap* minHeap, int val)
    {
        ++minHeap->size;
        int i = minHeap->size - 1;
        while (i && (val < minHeap->harr[(i - 1)/2]))
        {
            minHeap->harr[i] = minHeap->harr[(i - 1)/2];
            i = (i - 1)/2;
        }
        minHeap->harr[i] = val;
    }

    // A standard funvtion to build min heap
    void buildMinHeap(struct MinHeap* minHeap)
    {
        int n = minHeap->size - 1;
        int i;
        for (i = (n - 1) / 2; i >= 0; --i)
            minHeapify(minHeap, i);
    }

    // Creates a min heap of capacity equal to size and inserts all values
    // from len[] in it. Initially size of min heap is equal to capacity
    struct MinHeap* createAndBuildMinHeap(int len[], int size)
    {
        struct MinHeap* minHeap = createMinHeap(size);
        for (int i = 0; i < size; ++i)
            minHeap->harr[i] = len[i];
        minHeap->size = size;
        buildMinHeap(minHeap);
        return minHeap;
    }

    // The main function that returns the minimum cost to connect n ropes of
    // lengths stored in len[0..n-1]
    int minCost(int len[], int n)
    {
        int cost = 0;  // Initialize result

        // Create a min heap of capacity equal to n and put all ropes in it
        struct MinHeap* minHeap = createAndBuildMinHeap(len, n);

        // Iterate while size of heap doesn't become 1
        while (!isSizeOne(minHeap))
        {
            // Extract two minimum length ropes from min heap
            int min     = extractMin(minHeap);
            int sec_min = extractMin(minHeap);

            cost += (min + sec_min);  // Update total cost

            // Insert a new rope in min heap with length equal to sum
            // of two extracted minimum lengths
            insertMinHeap(minHeap, min+sec_min);
        }

        // Finally return total minimum cost for connecting all ropes
        return cost;
    }

    // Driver program to test above functions
    int main()
    {
        int len[] = {4, 3, 2, 6};
        int size = sizeof(len)/sizeof(len[0]);
        cout << "Total cost for connecting ropes is " << minCost(len, size);
        return 0;
    }

Output:

    Total cost for connecting ropes is 29

***Time Complexity:*** Time complexity of the algorithm is O(nLogn)
assuming that we use a O(nLogn) sorting algorithm. Note that heap
operations like insert and extract take O(Logn) time.

***Algorithmic Paradigm:*** Greedy Algorithm

  
 **A simple implementation with STL in C++**  
 Following is a simple implementation that uses
[priority\_queue](http://www.cplusplus.com/reference/queue/priority_queue/)
available in STL. Thanks to Pango89 for providing below code.

    #include<iostream>
    #include<queue>
    using namespace std;

    int minCost(int arr[], int n)
    {
        // Create a priority queue ( http://www.cplusplus.com/reference/queue/priority_queue/ )
        // By default 'less' is used which is for decreasing order
        // and 'greater' is used for increasing order
        priority_queue< int, vector<int>, greater<int> > pq(arr, arr+n);

        // Initialize result
        int res = 0;

        // While size of priority queue is more than 1
        while (pq.size() > 1)
        {
            // Extract shortest two ropes from pq
            int first = pq.top();
            pq.pop();
            int second = pq.top();
            pq.pop();

            // Connect the ropes: update result and
            // insert the new rope to pq
            res += first + second;
            pq.push(first + second);
        }

        return res;
    }

    // Driver program to test above function
    int main()
    {
        int len[] = {4, 3, 2, 6};
        int size = sizeof(len)/sizeof(len[0]);
        cout << "Total cost for connecting ropes is " << minCost(len, size);
        return 0;
    }

Output:

    Total cost for connecting ropes is 29

This article is compiled by **Abhishek**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/connect-n-ropes-minimum-cost/>

Graph Coloring | Set 2 (Greedy Algorithm)
-----------------------------------------

We introduced [graph coloring and
applications](http://www.geeksforgeeks.org/graph-coloring-applications/)
in previous post. As discussed in the previous post, graph coloring is
widely used. <span id="more-123945"></span>Unfortunately, there is no
efficient algorithm available for coloring a graph with minimum number
of colors as the problem is a known [NP Complete
problem](http://www.geeksforgeeks.org/np-completeness-set-1/). There are
approximate algorithms to solve the problem though. Following is the
basic Greedy Algorithm to assign colors. It doesn’t guarantee to use
minimum colors, but it guarantees an upper bound on the number of
colors. The basic algorithm never uses more than d+1 colors where d is
the maximum degree of a vertex in the given graph.

**Basic Greedy Coloring Algorithm:**

    1. Color first vertex with first color.
    2. Do following for remaining V-1 vertices.
              a) Consider the currently picked vertex and color it with the 
                 lowest numbered color that has not been used on any previously
                 colored vertices adjacent to it. If all previously used colors 
                 appear on vertices adjacent to v, assign a new color to it.

Following is C++ implementation of the above Greedy Algorithm.

    // A C++ program to implement greedy algorithm for graph coloring
    #include <iostream>
    #include <list>
    using namespace std;

    // A class that represents an undirected graph
    class Graph
    {
        int V;    // No. of vertices
        list<int> *adj;    // A dynamic array of adjacency lists
    public:
        // Constructor and destructor
        Graph(int V)   { this->V = V; adj = new list<int>[V]; }
        ~Graph()       { delete [] adj; }

        // function to add an edge to graph
        void addEdge(int v, int w);

        // Prints greedy coloring of the vertices
        void greedyColoring();
    };

    void Graph::addEdge(int v, int w)
    {
        adj[v].push_back(w);
        adj[w].push_back(v);  // Note: the graph is undirected
    }

    // Assigns colors (starting from 0) to all vertices and prints
    // the assignment of colors
    void Graph::greedyColoring()
    {
        int result[V];

        // Assign the first color to first vertex
        result[0]  = 0;

        // Initialize remaining V-1 vertices as unassigned
        for (int u = 1; u < V; u++)
            result[u] = -1;  // no color is assigned to u

        // A temporary array to store the available colors. True
        // value of available[cr] would mean that the color cr is
        // assigned to one of its adjacent vertices
        bool available[V];
        for (int cr = 0; cr < V; cr++)
            available[cr] = false;

        // Assign colors to remaining V-1 vertices
        for (int u = 1; u < V; u++)
        {
            // Process all adjacent vertices and flag their colors
            // as unavailable
            list<int>::iterator i;
            for (i = adj[u].begin(); i != adj[u].end(); ++i)
                if (result[*i] != -1)
                    available[result[*i]] = true;

            // Find the first available color
            int cr;
            for (cr = 0; cr < V; cr++)
                if (available[cr] == false)
                    break;

            result[u] = cr; // Assign the found color

            // Reset the values back to false for the next iteration
            for (i = adj[u].begin(); i != adj[u].end(); ++i)
                if (result[*i] != -1)
                    available[result[*i]] = false;
        }

        // print the result
        for (int u = 0; u < V; u++)
            cout << "Vertex " << u << " --->  Color "
                 << result[u] << endl;
    }

    // Driver program to test above function
    int main()
    {
        Graph g1(5);
        g1.addEdge(0, 1);
        g1.addEdge(0, 2);
        g1.addEdge(1, 2);
        g1.addEdge(1, 3);
        g1.addEdge(2, 3);
        g1.addEdge(3, 4);
        cout << "Coloring of Graph 1 \n";
        g1.greedyColoring();

        Graph g2(5);
        g2.addEdge(0, 1);
        g2.addEdge(0, 2);
        g2.addEdge(1, 2);
        g2.addEdge(1, 4);
        g2.addEdge(2, 4);
        g2.addEdge(4, 3);
        cout << "\nColoring of Graph 2 \n";
        g2.greedyColoring();

        return 0;
    }

Output:

    Coloring of Graph 1
    Vertex 0 --->  Color 0
    Vertex 1 --->  Color 1
    Vertex 2 --->  Color 2
    Vertex 3 --->  Color 0
    Vertex 4 --->  Color 1

    Coloring of Graph 2
    Vertex 0 --->  Color 0
    Vertex 1 --->  Color 1
    Vertex 2 --->  Color 2
    Vertex 3 --->  Color 0
    Vertex 4 --->  Color 3

Time Complexity: O(V^2 + E) in worst case.

**Analysis of Basic Algorithm**  
 The above algorithm doesn’t always use minimum number of colors. Also,
the number of colors used sometime depend on the order in which vertices
are processed. For example, consider the following two graphs. Note that
in graph on right side, vertices 3 and 4 are swapped. If we consider the
vertices 0, 1, 2, 3, 4 in left graph, we can color the graph using 3
colors. But if we consider the vertices 0, 1, 2, 3, 4 in right graph, we
need 4 colors.

[![graph\_coloring2](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/graph_coloring21-300x130.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/graph_coloring21.png)

[![graph\_coloring2](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/graph_coloring11-300x130.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/graph_coloring11.png)

 

 

 

   
 So the order in which the vertices are picked is important. Many people
have suggested different ways to find an ordering that work better than
the basic algorithm on average. The most common is [Welshâ€“Powell
Algorithm](http://mrsleblancsmath.pbworks.com/w/file/fetch/46119304/vertex%20coloring%20algorithm.pdf)
which considers vertices in descending order of degrees.

**How does the basic algorithm guarantee an upper bound of d+1?**  
 Here d is the maximum degree in the given graph. Since d is maximum
degree, a vertex cannot be attached to more than d vertices. When we
color a vertex, at most d colors could have already been used by its
adjacent. To color this vertex, we need to pick the smallest numbered
color that is not used by the adjacent vertices. If colors are numbered
like 1, 2, …., then the value of such smallest number must be between 1
to d+1 (Note that d numbers are already picked by adjacent vertices).  
 This can also be proved using induction. See
[this](http://www.youtube.com/watch?v=h9wxtqoa1jY)video lecture for
proof.

We will soon be discussing some interesting facts about chromatic number
and graph coloring.

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

   
Tags: [Graph](http://www.geeksforgeeks.org/tag/graph/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/>

Greedy Algorithms | Set 1 (Activity Selection Problem)
------------------------------------------------------

Greedy is an algorithmic paradigm that builds up a solution piece by
piece, always choosing the next piece that offers the most obvious and
immediate benefit.<span id="more-18528"></span> Greedy algorithms are
used for optimization problems. An optimization problem can be solved
using Greedy if the problem has the following property: *At every step,
we can make a choice that looks best at the moment, and we get the
optimal solution of the complete problem*.  
 If a Greedy Algorithm can solve a problem, then it generally becomes
the best method to solve that problem as the Greedy algorithms are in
general more efficient than other techniques like Dynamic Programming.
But Greedy algorithms cannot always be applied. For example, Fractional
Knapsack problem (See
[this](http://www.cs.binghamton.edu/~dima/cs333/knapsack.ppt)) can be
solved using Greedy, but [0-1
Knapsack](http://www.geeksforgeeks.org/archives/18430) cannot be solved
using Greedy.

Following are some standard algorithms that are Greedy algorithms.  
 **1) [Kruskal’s Minimum Spanning Tree
(MST)](http://en.wikipedia.org/wiki/Kruskal%27s_algorithm):** In
Kruskal’s algorithm, we create a MST by picking edges one by one. The
Greedy Choice is to pick the smallest weight edge that doesn’t cause a
cycle in the MST constructed so far.  
 **2) [Prim’s Minimum Spanning
Tree](http://en.wikipedia.org/wiki/Prim%27s_algorithm):** In Prim’s
algorithm also, we create a MST by picking edges one by one. We maintain
two sets: set of the vertices already included in MST and the set of the
vertices not yet included. The Greedy Choice is to pick the smallest
weight edge that connects the two sets.  
 **3) [Dijkstra’s Shortest
Path](http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm):** The
Dijkstra’s algorithm is very similar to Prim’s algorithm. The shortest
path tree is built up, edge by edge. We maintain two sets: set of the
vertices already included in the tree and the set of the vertices not
yet included. The Greedy Choice is to pick the edge that connects the
two sets and is on the smallest weight path from source to the set that
contains not yet included vertices.  
 **4) [Huffman Coding](http://en.wikipedia.org/wiki/Huffman_coding):**
Huffman Coding is a loss-less compression technique. It assigns variable
length bit codes to different characters. The Greedy Choice is to assign
least bit length code to the most frequent character.

The greedy algorithms are sometimes also used to get an approximation
for Hard optimization problems. For example, [Traveling Salesman
Problem](http://en.wikipedia.org/wiki/Travelling_salesman_problem) is a
NP Hard problem. A Greedy choice for this problem is to pick the nearest
unvisited city from the current city at every step. This solutions
doesn’t always produce the best optimal solution, but can be used to get
an approximate optimal solution.

Let us consider the [Activity Selection
problem](http://en.wikipedia.org/wiki/Activity_selection_problem) as our
first example of Greedy algorithms. Following is the problem
statement.  
 *You are given n activities with their start and finish times. Select
the maximum number of activities that can be performed by a single
person, assuming that a person can only work on a single activity at a
time.*  
 Example:

    Consider the following 6 activities. 
         start[]  =  {1, 3, 0, 5, 8, 5};
         finish[] =  {2, 4, 6, 7, 9, 9};
    The maximum set of activities that can be executed 
    by a single person is {0, 1, 3, 4}

The greedy choice is to always pick the next activity whose finish time
is least among the remaining activities and the start time is more than
or equal to the finish time of previously selected activity. We can sort
the activities according to their finishing time so that we always
consider the next activity as minimum finishing time activity.

1) Sort the activities according to their finishing time  
 2) Select the first activity from the sorted array and print it.  
 3) Do following for remaining activities in the sorted array.  
 …….a) If the start time of this activity is greater than the finish
time of previously selected activity then select this activity and print
it.

In the following C implementation, it is assumed that the activities are
already sorted according to their finish time.

    #include<stdio.h>

    // Prints a maximum set of activities that can be done by a single
    // person, one at a time.
    //  n   -->  Total number of activities
    //  s[] -->  An array that contains start time of all activities
    //  f[] -->  An array that contains finish time of all activities
    void printMaxActivities(int s[], int f[], int n)
    {
        int i, j;

        printf ("Following activities are selected \n");

        // The first activity always gets selected
        i = 0;
        printf("%d ", i);

        // Consider rest of the activities
        for (j = 1; j < n; j++)
        {
          // If this activity has start time greater than or equal to the finish
          // time of previously selected activity, then select it
          if (s[j] >= f[i])
          {
              printf ("%d ", j);
              i = j;
          }
        }
    }

    // driver program to test above function
    int main()
    {
        int s[] =  {1, 3, 0, 5, 8, 5};
        int f[] =  {2, 4, 6, 7, 9, 9};
        int n = sizeof(s)/sizeof(s[0]);
        printMaxActivities(s, f, n);
        getchar();
        return 0;
    }

Output:

    Following activities are selected
    0 1 3 4

**How does Greedy Choice work for Activities sorted according to finish
time?**  
 Let the give set of activities be S = {1, 2, 3, ..n} and activities be
sorted by finish time. The greedy choice is to always pick activity 1.
How come the activity 1 always provides one of the optimal solutions. We
can prove it by showing that if there is another solution B with first
activity other than 1, then there is also a solution A of same size with
activity 1 as first activity. Let the first activity selected by B be k,
then there always exist A = {B – {k}} U {1}.(Note that the activities in
B are independent and k has smallest finishing time among all. Since k
is not 1, finish(k) \>= finish(1)).

**References:**  
 [Introduction to Algorithms by Thomas H. Cormen, Charles E. Leiserson,
Ronald L. Rivest, Clifford Stein](http://mitpress.mit.edu/algorithms/)  
 [Algorithms by S. Dasgupta, C.H. Papadimitriou, and U.V.
Vazirani](http://www.cs.berkeley.edu/~vazirani/algorithms.html)  
 <http://en.wikipedia.org/wiki/Greedy_algorithm>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

   
Tags: [Activity Selection
Problem](http://www.geeksforgeeks.org/tag/activity-selection-problem/),
[Greedy](http://www.geeksforgeeks.org/tag/greedy/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-1-activity-selection-problem/>

Greedy Algorithms | Set 2 (Kruskalâ€™s Minimum Spanning Tree Algorithm)
-----------------------------------------------------------------------

*What is Minimum Spanning Tree?*  
 Given a connected and undirected graph, a *spanning tree* of that graph
is a subgraph that is a tree and connects all the vertices together.
<span id="more-26604"></span>A single graph can have many different
spanning trees. A *minimum spanning tree (MST)* or minimum weight
spanning tree for a weighted, connected and undirected graph is a
spanning tree with weight less than or equal to the weight of every
other spanning tree. The weight of a spanning tree is the sum of weights
given to each edge of the spanning tree.

*How many edges does a minimum spanning tree has?*  
 A minimum spanning tree has (V – 1) edges where V is the number of
vertices in the given graph.

*What are the applications of Minimum Spanning Tree?*  
 See [this](http://www.geeksforgeeks.org/archives/11110)for applications
of MST.

Below are the steps for finding MST using Kruskal’s algorithm

    1. Sort all the edges in non-decreasing order of their weight.

    2. Pick the smallest edge. Check if it forms a cycle with the spanning tree 
    formed so far. If cycle is not formed, include this edge. Else, discard it.  

    3. Repeat step#2 until there are (V-1) edges in the spanning tree.

The step\#2 uses [Union-Find
algorithm](http://www.geeksforgeeks.org/archives/26350) to detect cycle.
So we recommend to read following post as a prerequisite.  
 [Union-Find Algorithm | Set 1 (Detect Cycle in a
Graph)](http://www.geeksforgeeks.org/archives/26350)  
 [Union-Find Algorithm | Set 2 (Union By Rank and Path
Compression)](http://www.geeksforgeeks.org/archives/26489)

The algorithm is a Greedy Algorithm. The Greedy Choice is to pick the
smallest weight edge that does not cause a cycle in the MST constructed
so far. Let us understand it with an example: Consider the below input
graph.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-0-300x139.jpg "Fig 0")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-0.jpg)

The graph contains 9 vertices and 14 edges. So, the minimum spanning
tree formed will be having (9 – 1) = 8 edges.

    After sorting:
    Weight   Src    Dest
    1         7      6
    2         8      2
    2         6      5
    4         0      1
    4         2      5
    6         8      6
    7         2      3
    7         7      8
    8         0      7
    8         1      2
    9         3      4
    10        5      4
    11        1      7
    14        3      5

Now pick all edges one by one from sorted list of edges  
 **1.** *Pick edge 7-6:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-1.jpg "Fig 1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-1.jpg)

**2.** *Pick edge 8-2:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-2-241x300.jpg "Fig 2")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-2.jpg)

**3.** *Pick edge 6-5:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-3-300x232.jpg "Fig 3")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-3.jpg)

**4.** *Pick edge 0-1:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-4-300x175.jpg "Fig 4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-4.jpg)

**5.** *Pick edge 2-5:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-5-300x175.jpg "Fig 5")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-5.jpg)

**6.** *Pick edge 8-6:* Since including this edge results in cycle,
discard it.

**7.** *Pick edge 2-3:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-6-300x175.jpg "Fig 6")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-6.jpg)

**8.** *Pick edge 7-8:* Since including this edge results in cycle,
discard it.

**9.** *Pick edge 0-7:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-7-300x175.jpg "Fig 7")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-7.jpg)

**10.** *Pick edge 1-2:* Since including this edge results in cycle,
discard it.

**11.** *Pick edge 3-4:* No cycle is formed, include it.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig8new.jpeg "Fig 8")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig8new.jpeg)

Since the number of edges included equals (V – 1), the algorithm stops
here.

    // Kruskal's algortihm to find Minimum Spanning Tree of a given connected,
    // undirected and weighted graph
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    // a structure to represent a weighted edge in graph
    struct Edge
    {
        int src, dest, weight;
    };

    // a structure to represent a connected, undirected and weighted graph
    struct Graph
    {
        // V-> Number of vertices, E-> Number of edges
        int V, E;

        // graph is represented as an array of edges. Since the graph is
        // undirected, the edge from src to dest is also edge from dest
        // to src. Both are counted as 1 edge here.
        struct Edge* edge;
    };

    // Creates a graph with V vertices and E edges
    struct Graph* createGraph(int V, int E)
    {
        struct Graph* graph = (struct Graph*) malloc( sizeof(struct Graph) );
        graph->V = V;
        graph->E = E;

        graph->edge = (struct Edge*) malloc( graph->E * sizeof( struct Edge ) );

        return graph;
    }

    // A structure to represent a subset for union-find
    struct subset
    {
        int parent;
        int rank;
    };

    // A utility function to find set of an element i
    // (uses path compression technique)
    int find(struct subset subsets[], int i)
    {
        // find root and make root as parent of i (path compression)
        if (subsets[i].parent != i)
            subsets[i].parent = find(subsets, subsets[i].parent);

        return subsets[i].parent;
    }

    // A function that does union of two sets of x and y
    // (uses union by rank)
    void Union(struct subset subsets[], int x, int y)
    {
        int xroot = find(subsets, x);
        int yroot = find(subsets, y);

        // Attach smaller rank tree under root of high rank tree
        // (Union by Rank)
        if (subsets[xroot].rank < subsets[yroot].rank)
            subsets[xroot].parent = yroot;
        else if (subsets[xroot].rank > subsets[yroot].rank)
            subsets[yroot].parent = xroot;

        // If ranks are same, then make one as root and increment
        // its rank by one
        else
        {
            subsets[yroot].parent = xroot;
            subsets[xroot].rank++;
        }
    }

    // Compare two edges according to their weights.
    // Used in qsort() for sorting an array of edges
    int myComp(const void* a, const void* b)
    {
        struct Edge* a1 = (struct Edge*)a;
        struct Edge* b1 = (struct Edge*)b;
        return a1->weight > b1->weight;
    }

    // The main function to construct MST using Kruskal's algorithm
    void KruskalMST(struct Graph* graph)
    {
        int V = graph->V;
        struct Edge result[V];  // Tnis will store the resultant MST
        int e = 0;  // An index variable, used for result[]
        int i = 0;  // An index variable, used for sorted edges

        // Step 1:  Sort all the edges in non-decreasing order of their weight
        // If we are not allowed to change the given graph, we can create a copy of
        // array of edges
        qsort(graph->edge, graph->E, sizeof(graph->edge[0]), myComp);

        // Allocate memory for creating V ssubsets
        struct subset *subsets =
            (struct subset*) malloc( V * sizeof(struct subset) );

        // Create V subsets with single elements
        for (int v = 0; v < V; ++v)
        {
            subsets[v].parent = v;
            subsets[v].rank = 0;
        }

        // Number of edges to be taken is equal to V-1
        while (e < V - 1)
        {
            // Step 2: Pick the smallest edge. And increment the index
            // for next iteration
            struct Edge next_edge = graph->edge[i++];

            int x = find(subsets, next_edge.src);
            int y = find(subsets, next_edge.dest);

            // If including this edge does't cause cycle, include it
            // in result and increment the index of result for next edge
            if (x != y)
            {
                result[e++] = next_edge;
                Union(subsets, x, y);
            }
            // Else discard the next_edge
        }

        // print the contents of result[] to display the built MST
        printf("Following are the edges in the constructed MST\n");
        for (i = 0; i < e; ++i)
            printf("%d -- %d == %d\n", result[i].src, result[i].dest,
                                                       result[i].weight);
        return;
    }

    // Driver program to test above functions
    int main()
    {
        /* Let us create following weighted graph
                 10
            0--------1
            |  \     |
           6|   5\   |15
            |      \ |
            2--------3
                4       */
        int V = 4;  // Number of vertices in graph
        int E = 5;  // Number of edges in graph
        struct Graph* graph = createGraph(V, E);


        // add edge 0-1
        graph->edge[0].src = 0;
        graph->edge[0].dest = 1;
        graph->edge[0].weight = 10;

        // add edge 0-2
        graph->edge[1].src = 0;
        graph->edge[1].dest = 2;
        graph->edge[1].weight = 6;

        // add edge 0-3
        graph->edge[2].src = 0;
        graph->edge[2].dest = 3;
        graph->edge[2].weight = 5;

        // add edge 1-3
        graph->edge[3].src = 1;
        graph->edge[3].dest = 3;
        graph->edge[3].weight = 15;

        // add edge 2-3
        graph->edge[4].src = 2;
        graph->edge[4].dest = 3;
        graph->edge[4].weight = 4;

        KruskalMST(graph);

        return 0;
    }

    Following are the edges in the constructed MST
    2 -- 3 == 4
    0 -- 3 == 5
    0 -- 1 == 10

**Time Complexity:** O(ElogE) or O(ElogV). Sorting of edges takes
O(ELogE) time. After sorting, we iterate through all edges and apply
find-union algorithm. The find and union operations can take atmost
O(LogV) time. So overall complexity is O(ELogE + ELogV) time. The value
of E can be atmost V^2, so O(LogV) are O(LogE) same. Therefore, overall
time complexity is O(ElogE) or O(ElogV)

References:  
 <http://www.ics.uci.edu/~eppstein/161/960206.html>  
 <http://en.wikipedia.org/wiki/Minimum_spanning_tree>

This article is compiled by [Aashish
Barnwal](https://www.facebook.com/barnwal.aashish) and reviewed by
GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above.

   
Tags: [Graph](http://www.geeksforgeeks.org/tag/graph/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/),
[Kruskal](http://www.geeksforgeeks.org/tag/kruskal/),
[Kruskal'sAlgorithm](http://www.geeksforgeeks.org/tag/kruskalsalgorithm/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-2-kruskals-minimum-spanning-tree-mst/>

Greedy Algorithms | Set 4 (Efficient Huffman Coding for Sorted Input)
---------------------------------------------------------------------

We recommend to read following post as a prerequisite for this.

[Greedy Algorithms | Set 3 (Huffman
Coding)](http://www.geeksforgeeks.org/archives/26851)

Time complexity of the algorithm discussed in above post is O(nLogn).
<span id="more-26954"></span> If we know that the given array is sorted
(by non-decreasing order of frequency), we can generate Huffman codes in
O(n) time. Following is a O(n) algorithm for sorted input.

**1.** Create two empty queues.

**2.** Create a leaf node for each unique character and Enqueue it to
the first queue in non-decreasing order of frequency. Initially second
queue is empty.

**3.** Dequeue two nodes with the minimum frequency by examining the
front of both queues. Repeat following steps two times  
 …..**a)** If second queue is empty, dequeue from first queue.  
 …..**b)** If first queue is empty, dequeue from second queue.  
 …..**c)** Else, compare the front of two queues and dequeue the
minimum.

**4.** Create a new internal node with frequency equal to the sum of the
two nodes frequencies. Make the first Dequeued node as its left child
and the second Dequeued node as right child. Enqueue this node to second
queue.

**5.** Repeat steps\#3 and \#4 until there is more than one node in the
queues. The remaining node is the root node and the tree is complete.

    // C Program for Efficient Huffman Coding for Sorted input
    #include <stdio.h>
    #include <stdlib.h>

    // This constant can be avoided by explicitly calculating height of Huffman Tree
    #define MAX_TREE_HT 100

    // A node of huffman tree
    struct QueueNode
    {
        char data;
        unsigned freq;
        struct QueueNode *left, *right;
    };

    // Structure for Queue: collection of Huffman Tree nodes (or QueueNodes)
    struct Queue
    {
        int front, rear;
        int capacity;
        struct QueueNode **array;
    };

    // A utility function to create a new Queuenode
    struct QueueNode* newNode(char data, unsigned freq)
    {
        struct QueueNode* temp =
           (struct QueueNode*) malloc(sizeof(struct QueueNode));
        temp->left = temp->right = NULL;
        temp->data = data;
        temp->freq = freq;
        return temp;
    }

    // A utility function to create a Queue of given capacity
    struct Queue* createQueue(int capacity)
    {
        struct Queue* queue = (struct Queue*) malloc(sizeof(struct Queue));
        queue->front = queue->rear = -1;
        queue->capacity = capacity;
        queue->array =
          (struct QueueNode**) malloc(queue->capacity * sizeof(struct QueueNode*));
        return queue;
    }

    // A utility function to check if size of given queue is 1
    int isSizeOne(struct Queue* queue)
    {
        return queue->front == queue->rear && queue->front != -1;
    }

    // A utility function to check if given queue is empty
    int isEmpty(struct Queue* queue)
    {
        return queue->front == -1;
    }

    // A utility function to check if given queue is full
    int isFull(struct Queue* queue)
    {
        return queue->rear == queue->capacity - 1;
    }

    // A utility function to add an item to queue
    void enQueue(struct Queue* queue, struct QueueNode* item)
    {
        if (isFull(queue))
            return;
        queue->array[++queue->rear] = item;
        if (queue->front == -1)
            ++queue->front;
    }

    // A utility function to remove an item from queue
    struct QueueNode* deQueue(struct Queue* queue)
    {
        if (isEmpty(queue))
            return NULL;
        struct QueueNode* temp = queue->array[queue->front];
        if (queue->front == queue->rear)  // If there is only one item in queue
            queue->front = queue->rear = -1;
        else
            ++queue->front;
        return temp;
    }

    // A utility function to get from of queue
    struct QueueNode* getFront(struct Queue* queue)
    {
        if (isEmpty(queue))
            return NULL;
        return queue->array[queue->front];
    }

    /* A function to get minimum item from two queues */
    struct QueueNode* findMin(struct Queue* firstQueue, struct Queue* secondQueue)
    {
        // Step 3.a: If second queue is empty, dequeue from first queue
        if (isEmpty(firstQueue))
            return deQueue(secondQueue);

        // Step 3.b: If first queue is empty, dequeue from second queue
        if (isEmpty(secondQueue))
            return deQueue(firstQueue);

        // Step 3.c:  Else, compare the front of two queues and dequeue minimum
        if (getFront(firstQueue)->freq < getFront(secondQueue)->freq)
            return deQueue(firstQueue);

        return deQueue(secondQueue);
    }

    // Utility function to check if this node is leaf
    int isLeaf(struct QueueNode* root)
    {
        return !(root->left) && !(root->right) ;
    }

    // A utility function to print an array of size n
    void printArr(int arr[], int n)
    {
        int i;
        for (i = 0; i < n; ++i)
            printf("%d", arr[i]);
        printf("\n");
    }

    // The main function that builds Huffman tree
    struct QueueNode* buildHuffmanTree(char data[], int freq[], int size)
    {
        struct QueueNode *left, *right, *top;

        // Step 1: Create two empty queues
        struct Queue* firstQueue  = createQueue(size);
        struct Queue* secondQueue = createQueue(size);

        // Step 2:Create a leaf node for each unique character and Enqueue it to
        // the first queue in non-decreasing order of frequency. Initially second
        // queue is empty
        for (int i = 0; i < size; ++i)
            enQueue(firstQueue, newNode(data[i], freq[i]));

        // Run while Queues contain more than one node. Finally, first queue will
        // be empty and second queue will contain only one node
        while (!(isEmpty(firstQueue) && isSizeOne(secondQueue)))
        {
            // Step 3: Dequeue two nodes with the minimum frequency by examining
            // the front of both queues
            left = findMin(firstQueue, secondQueue);
            right = findMin(firstQueue, secondQueue);

            // Step 4: Create a new internal node with frequency equal to the sum
            // of the two nodes frequencies. Enqueue this node to second queue.
            top = newNode('$' , left->freq + right->freq);
            top->left = left;
            top->right = right;
            enQueue(secondQueue, top);
        }

        return deQueue(secondQueue);
    }

    // Prints huffman codes from the root of Huffman Tree.  It uses arr[] to
    // store codes
    void printCodes(struct QueueNode* root, int arr[], int top)
    {
        // Assign 0 to left edge and recur
        if (root->left)
        {
            arr[top] = 0;
            printCodes(root->left, arr, top + 1);
        }

        // Assign 1 to right edge and recur
        if (root->right)
        {
            arr[top] = 1;
            printCodes(root->right, arr, top + 1);
        }

        // If this is a leaf node, then it contains one of the input
        // characters, print the character and its code from arr[]
        if (isLeaf(root))
        {
            printf("%c: ", root->data);
            printArr(arr, top);
        }
    }

    // The main function that builds a Huffman Tree and print codes by traversing
    // the built Huffman Tree
    void HuffmanCodes(char data[], int freq[], int size)
    {
       //  Construct Huffman Tree
       struct QueueNode* root = buildHuffmanTree(data, freq, size);

       // Print Huffman codes using the Huffman tree built above
       int arr[MAX_TREE_HT], top = 0;
       printCodes(root, arr, top);
    }

    // Driver program to test above functions
    int main()
    {
        char arr[] = {'a', 'b', 'c', 'd', 'e', 'f'};
        int freq[] = {5, 9, 12, 13, 16, 45};
        int size = sizeof(arr)/sizeof(arr[0]);
        HuffmanCodes(arr, freq, size);
        return 0;
    }

Output:

    f: 0
    c: 100
    d: 101
    a: 1100
    b: 1101
    e: 111

***Time complexity:*** O(n)

If the input is not sorted, it need to be sorted first before it can be
processed by the above algorithm. Sorting can be done using heap-sort or
merge-sort both of which run in Theta(nlogn). So, the overall time
complexity becomes O(nlogn) for unsorted input.

***Reference:***  
 <http://en.wikipedia.org/wiki/Huffman_coding>

This article is compiled by [Aashish
Barnwal](https://www.facebook.com/barnwal.aashish) and reviewed by
GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above.

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/), [Huffman
Coding](http://www.geeksforgeeks.org/tag/huffman-coding/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-3-huffman-coding-set-2/>

Greedy Algorithms | Set 3 (Huffman Coding)
------------------------------------------

Huffman coding is a lossless data compression algorithm. The idea is to
assign variable-legth codes to input characters, lengths of the assigned
codes are based on the frequencies of corresponding characters.<span
id="more-26851"></span> The most frequent character gets the smallest
code and the least frequent character gets the largest code.  
 The variable-length codes assigned to input characters are [Prefix
Codes](http://en.wikipedia.org/wiki/Prefix_code), means the codes (bit
sequences) are assigned in such a way that the code assigned to one
character is not prefix of code assigned to any other character. This is
how Huffman Coding makes sure that there is no ambiguity when decoding
the generated bit stream.  
 Let us understand prefix codes with a counter example. Let there be
four characters a, b, c and d, and their corresponding variable length
codes be 00, 01, 0 and 1. This coding leads to ambiguity because code
assigned to c is prefix of codes assigned to a and b. If the compressed
bit stream is 0001, the de-compressed output may be “cccd” or “ccb” or
“acd” or “ab”.

See [this](http://en.wikipedia.org/wiki/Huffman_coding#Applications) for
applications of Huffman Coding.

There are mainly two major parts in Huffman Coding  
 **1)** Build a Huffman Tree from input characters.  
 **2)** Traverse the Huffman Tree and assign codes to characters.

***Steps to build Huffman Tree***  
 Input is array of unique characters along with their frequency of
occurrences and output is Huffman Tree.

**1.** Create a leaf node for each unique character and build a min heap
of all leaf nodes (Min Heap is used as a priority queue. The value of
frequency field is used to compare two nodes in min heap. Initially, the
least frequent character is at root)

**2.** Extract two nodes with the minimum frequency from the min heap.

**3.** Create a new internal node with frequency equal to the sum of the
two nodes frequencies. Make the first extracted node as its left child
and the other extracted node as its right child. Add this node to the
min heap.

**4.** Repeat steps\#2 and \#3 until the heap contains only one node.
The remaining node is the root node and the tree is complete.

Let us understand the algorithm with an example:

    character   Frequency
        a           5
        b           9
        c           12
        d           13
        e           16
        f           45

**Step 1.** Build a min heap that contains 6 nodes where each node
represents root of a tree with single node.

**Step 2** Extract two minimum frequency nodes from min heap. Add a new
internal node with frequency 5 + 9 = 14.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-1-300x129.jpeg "fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-1.jpeg)  
 Now min heap contains 5 nodes where 4 nodes are roots of trees with
single element each, and one heap node is root of tree with 3 elements

    character           Frequency
           c               12
           d               13
     Internal Node         14
           e               16
           f                45

**Step 3:** Extract two minimum frequency nodes from heap. Add a new
internal node with frequency 12 + 13 = 25  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-2-300x132.jpg "fig-2")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-2.jpg)  
 Now min heap contains 4 nodes where 2 nodes are roots of trees with
single element each, and two heap nodes are root of tree with more than
one nodes.

    character           Frequency
    Internal Node          14
           e               16
    Internal Node          25
           f               45

**Step 4:** Extract two minimum frequency nodes. Add a new internal node
with frequency 14 + 16 = 30  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-3-300x162.jpg "fig-3")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-3.jpg)  
 Now min heap contains 3 nodes.

    character          Frequency
    Internal Node         25
    Internal Node         30
          f               45 

**Step 5:** Extract two minimum frequency nodes. Add a new internal node
with frequency 25 + 30 = 55  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-4-300x121.jpg "fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-4.jpg)  
 Now min heap contains 2 nodes.

    character     Frequency
           f         45
    Internal Node    55

**Step 6:** Extract two minimum frequency nodes. Add a new internal node
with frequency 45 + 55 = 100  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-5-300x167.jpg "fig-5")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-5.jpg)  
 Now min heap contains only one node.

    character      Frequency
    Internal Node    100

Since the heap contains only one node, the algorithm stops here.

***Steps to print codes from Huffman Tree:***  
 Traverse the tree formed starting from the root. Maintain an auxiliary
array. While moving to the left child, write 0 to the array. While
moving to the right child, write 1 to the array. Print the array when a
leaf node is encountered.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-6-300x167.jpg "fig-6")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/fig-6.jpg)  
 The codes are as follows:

    character   code-word
        f          0
        c          100
        d          101
        a          1100
        b          1101
        e          111

    // C program for Huffman Coding
    #include <stdio.h>
    #include <stdlib.h>

    // This constant can be avoided by explicitly calculating height of Huffman Tree
    #define MAX_TREE_HT 100

    // A Huffman tree node
    struct MinHeapNode
    {
        char data;  // One of the input characters
        unsigned freq;  // Frequency of the character
        struct MinHeapNode *left, *right; // Left and right child of this node
    };

    // A Min Heap:  Collection of min heap (or Hufmman tree) nodes
    struct MinHeap
    {
        unsigned size;    // Current size of min heap
        unsigned capacity;   // capacity of min heap
        struct MinHeapNode **array;  // Attay of minheap node pointers
    };

    // A utility function allocate a new min heap node with given character
    // and frequency of the character
    struct MinHeapNode* newNode(char data, unsigned freq)
    {
        struct MinHeapNode* temp =
              (struct MinHeapNode*) malloc(sizeof(struct MinHeapNode));
        temp->left = temp->right = NULL;
        temp->data = data;
        temp->freq = freq;
        return temp;
    }

    // A utility function to create a min heap of given capacity
    struct MinHeap* createMinHeap(unsigned capacity)
    {
        struct MinHeap* minHeap =
             (struct MinHeap*) malloc(sizeof(struct MinHeap));
        minHeap->size = 0;  // current size is 0
        minHeap->capacity = capacity;
        minHeap->array =
         (struct MinHeapNode**)malloc(minHeap->capacity * sizeof(struct MinHeapNode*));
        return minHeap;
    }

    // A utility function to swap two min heap nodes
    void swapMinHeapNode(struct MinHeapNode** a, struct MinHeapNode** b)
    {
        struct MinHeapNode* t = *a;
        *a = *b;
        *b = t;
    }

    // The standard minHeapify function.
    void minHeapify(struct MinHeap* minHeap, int idx)
    {
        int smallest = idx;
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;

        if (left < minHeap->size &&
            minHeap->array[left]->freq < minHeap->array[smallest]->freq)
          smallest = left;

        if (right < minHeap->size &&
            minHeap->array[right]->freq < minHeap->array[smallest]->freq)
          smallest = right;

        if (smallest != idx)
        {
            swapMinHeapNode(&minHeap->array[smallest], &minHeap->array[idx]);
            minHeapify(minHeap, smallest);
        }
    }

    // A utility function to check if size of heap is 1 or not
    int isSizeOne(struct MinHeap* minHeap)
    {
        return (minHeap->size == 1);
    }

    // A standard function to extract minimum value node from heap
    struct MinHeapNode* extractMin(struct MinHeap* minHeap)
    {
        struct MinHeapNode* temp = minHeap->array[0];
        minHeap->array[0] = minHeap->array[minHeap->size - 1];
        --minHeap->size;
        minHeapify(minHeap, 0);
        return temp;
    }

    // A utility function to insert a new node to Min Heap
    void insertMinHeap(struct MinHeap* minHeap, struct MinHeapNode* minHeapNode)
    {
        ++minHeap->size;
        int i = minHeap->size - 1;
        while (i && minHeapNode->freq < minHeap->array[(i - 1)/2]->freq)
        {
            minHeap->array[i] = minHeap->array[(i - 1)/2];
            i = (i - 1)/2;
        }
        minHeap->array[i] = minHeapNode;
    }

    // A standard funvtion to build min heap
    void buildMinHeap(struct MinHeap* minHeap)
    {
        int n = minHeap->size - 1;
        int i;
        for (i = (n - 1) / 2; i >= 0; --i)
            minHeapify(minHeap, i);
    }

    // A utility function to print an array of size n
    void printArr(int arr[], int n)
    {
        int i;
        for (i = 0; i < n; ++i)
            printf("%d", arr[i]);
        printf("\n");
    }

    // Utility function to check if this node is leaf
    int isLeaf(struct MinHeapNode* root)
    {
        return !(root->left) && !(root->right) ;
    }

    // Creates a min heap of capacity equal to size and inserts all character of 
    // data[] in min heap. Initially size of min heap is equal to capacity
    struct MinHeap* createAndBuildMinHeap(char data[], int freq[], int size)
    {
        struct MinHeap* minHeap = createMinHeap(size);
        for (int i = 0; i < size; ++i)
            minHeap->array[i] = newNode(data[i], freq[i]);
        minHeap->size = size;
        buildMinHeap(minHeap);
        return minHeap;
    }

    // The main function that builds Huffman tree
    struct MinHeapNode* buildHuffmanTree(char data[], int freq[], int size)
    {
        struct MinHeapNode *left, *right, *top;

        // Step 1: Create a min heap of capacity equal to size.  Initially, there are
        // modes equal to size.
        struct MinHeap* minHeap = createAndBuildMinHeap(data, freq, size);

        // Iterate while size of heap doesn't become 1
        while (!isSizeOne(minHeap))
        {
            // Step 2: Extract the two minimum freq items from min heap
            left = extractMin(minHeap);
            right = extractMin(minHeap);

            // Step 3:  Create a new internal node with frequency equal to the
            // sum of the two nodes frequencies. Make the two extracted node as
            // left and right children of this new node. Add this node to the min heap
            // '$' is a special value for internal nodes, not used
            top = newNode('$', left->freq + right->freq);
            top->left = left;
            top->right = right;
            insertMinHeap(minHeap, top);
        }

        // Step 4: The remaining node is the root node and the tree is complete.
        return extractMin(minHeap);
    }

    // Prints huffman codes from the root of Huffman Tree.  It uses arr[] to
    // store codes
    void printCodes(struct MinHeapNode* root, int arr[], int top)
    {
        // Assign 0 to left edge and recur
        if (root->left)
        {
            arr[top] = 0;
            printCodes(root->left, arr, top + 1);
        }

        // Assign 1 to right edge and recur
        if (root->right)
        {
            arr[top] = 1;
            printCodes(root->right, arr, top + 1);
        }

        // If this is a leaf node, then it contains one of the input
        // characters, print the character and its code from arr[]
        if (isLeaf(root))
        {
            printf("%c: ", root->data);
            printArr(arr, top);
        }
    }

    // The main function that builds a Huffman Tree and print codes by traversing
    // the built Huffman Tree
    void HuffmanCodes(char data[], int freq[], int size)
    {
       //  Construct Huffman Tree
       struct MinHeapNode* root = buildHuffmanTree(data, freq, size);

       // Print Huffman codes using the Huffman tree built above
       int arr[MAX_TREE_HT], top = 0;
       printCodes(root, arr, top);
    }

    // Driver program to test above functions
    int main()
    {
        char arr[] = {'a', 'b', 'c', 'd', 'e', 'f'};
        int freq[] = {5, 9, 12, 13, 16, 45};
        int size = sizeof(arr)/sizeof(arr[0]);
        HuffmanCodes(arr, freq, size);
        return 0;
    }

    f: 0
    c: 100
    d: 101
    a: 1100
    b: 1101
    e: 111

***Time complexity:*** O(nlogn) where n is the number of unique
characters. If there are n nodes, extractMin() is called 2\*(n – 1)
times. extractMin() takes O(logn) time as it calles minHeapify(). So,
overall complexity is O(nlogn).

If the input array is sorted, there exists a linear time algorithm. We
will soon be discussing in our next post.

***Reference:***  
 <http://en.wikipedia.org/wiki/Huffman_coding>

This article is compiled by [Aashish
Barnwal](https://www.facebook.com/barnwal.aashish) and reviewed by
GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above.

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/), [Huffman
Coding](http://www.geeksforgeeks.org/tag/huffman-coding/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-3-huffman-coding/>

Greedy Algorithms | Set 5 (Primâ€™s Minimum Spanning Tree (MST))
----------------------------------------------------------------

We have discussedÂ [Kruskal’s algorithm for Minimum Spanning
Tree](http://www.geeksforgeeks.org/archives/26604). Like Kruskal’s
algorithm, Primâ€™s algorithm is also aÂ [Greedy
algorithm](http://www.geeksforgeeks.org/archives/18528). It starts with
an empty spanning tree.<span id="more-27455"></span> The idea is to
maintain two sets of vertices. The first set contains the vertices
already included in the MST, the other set contains the vertices not yet
included. At every step, it considers all the edges that connect the two
sets, and picks the minimum weight edge from these edges. After picking
the edge, it moves the other endpoint of the edge to the set containing
MST.  
 A group of edges that connects two set of vertices in a graph is
calledÂ [cut in graph
theory](http://en.wikipedia.org/wiki/Cut_%28graph_theory%29).Â *So, at
every step of Primâ€™s algorithm, we find a cut (of two sets, one
contains the vertices already included in MST and other contains rest of
the verices), pick the minimum weight edge from the cut and include this
vertex to MST Set (the set that contains already included vertices).*

***How does Prim’s Algorithm Work?*** The idea behind Prim’s algorithm
is simple, a spanning tree means all vertices must be connected. So the
two disjoint subsets (discussed above) of vertices must be connected to
make aÂ *SpanningÂ *Tree. And they must be connected with the minimum
weight edge to make it aÂ *MinimumÂ *Spanning Tree.

***Algorithm***  
 **1)** Create a set *mstSet* that keeps track of vertices already
included in MST.  
 **2)** Assign a key value to all vertices in the input graph.
Initialize all key values as INFINITE. Assign key value as 0 for the
first vertex so that it is picked first.  
 **3)** While mstSet doesn’t include all vertices  
 ….**a)** Pick a vertex *u* which is not there in *mstSet* and has
minimum key value.  
 ….**b)** Include *u* to mstSet.  
 ….**c)** Update key value of all adjacent vertices of *u*. To update
the key values, iterate through all adjacent vertices. For every
adjacent vertex *v*, if weight of edge *u-v* is less than the previous
key value of *v*, update the key value as weight of *u-v*

The idea of using key values is to pick the minimum weight edge from
[cut](http://en.wikipedia.org/wiki/Cut_(graph_theory)). The key values
are used only for vertices which are not yet included in MST, the key
value for these vertices indicate the minimum weight edges connecting
them to the set of vertices included in MST.

Let us understand with the following example:  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg)

The set *mstSet* is initially empty and keys assigned to vertices are
{0, INF, INF, INF, INF, INF, INF, INF} where INF indicates infinite. Now
pick the vertex with minimum key value. The vertex 0 is picked, include
it in *mstSet*. So *mstSet* becomes {0}. After including to *mstSet*,
update key values of adjacent vertices. Adjacent vertices of 0 are 1 and
7. The key values of 1 and 7 are updated as 4 and 8. Following subgraph
shows vertices and their key values, only the vertices with finite key
values are shown. The vertices included in MST are shown in green color.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg "Fig-2")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg)

Pick the vertex with minimum key value and not already included in MST
(not in mstSET). The vertex 1 is picked and added to mstSet. So mstSet
now becomes {0, 1}. Update the key values of adjacent vertices of 1. The
key value of vertex 2 becomes 8.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST2.jpg "Fig-3")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST2.jpg)

Pick the vertex with minimum key value and not already included in MST
(not in mstSET). We can either pick vertex 7 or vertex 2, let vertex 7
is picked. So mstSet now becomes {0, 1, 7}. Update the key values of
adjacent vertices of 7. The key value of vertex 6 and 8 becomes finite
(7 and 1 respectively).  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST3.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST3.jpg)

Pick the vertex with minimum key value and not already included in MST
(not in mstSET). Vertex 6 is picked. So mstSet now becomes {0, 1, 7, 6}.
Update the key values of adjacent vertices of 6. The key value of vertex
5 and 8 are updated.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST4.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST4.jpg)

We repeat the above steps until *mstSet* doesn’t include all vertices of
given graph. Finally, we get the following graph.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST5.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST5.jpg)

***How to implement the above algorithm?***  
 We use a boolean array mstSet[] to represent the set of vertices
included in MST. If a value mstSet[v] is true, then vertex v is included
in MST, otherwise not. Array key[] is used to store key values of all
vertices. Another array parent[] to store indexes of parent nodes in
MST. The parent array is the output array which is used to show the
constructed MST.

    // A C / C++ program for Prim's Minimum Spanning Tree (MST) algorithm. 
    // The program is for adjacency matrix representation of the graph

    #include <stdio.h>
    #include <limits.h>

    // Number of vertices in the graph
    #define V 5

    // A utility function to find the vertex with minimum key value, from
    // the set of vertices not yet included in MST
    int minKey(int key[], bool mstSet[])
    {
       // Initialize min value
       int min = INT_MAX, min_index;

       for (int v = 0; v < V; v++)
         if (mstSet[v] == false && key[v] < min)
             min = key[v], min_index = v;

       return min_index;
    }

    // A utility function to print the constructed MST stored in parent[]
    int printMST(int parent[], int n, int graph[V][V])
    {
       printf("Edge   Weight\n");
       for (int i = 1; i < V; i++)
          printf("%d - %d    %d \n", parent[i], i, graph[i][parent[i]]);
    }

    // Function to construct and print MST for a graph represented using adjacency
    // matrix representation
    void primMST(int graph[V][V])
    {
         int parent[V]; // Array to store constructed MST
         int key[V];   // Key values used to pick minimum weight edge in cut
         bool mstSet[V];  // To represent set of vertices not yet included in MST

         // Initialize all keys as INFINITE
         for (int i = 0; i < V; i++)
            key[i] = INT_MAX, mstSet[i] = false;

         // Always include first 1st vertex in MST.
         key[0] = 0;     // Make key 0 so that this vertex is picked as first vertex
         parent[0] = -1; // First node is always root of MST 

         // The MST will have V vertices
         for (int count = 0; count < V-1; count++)
         {
            // Pick thd minimum key vertex from the set of vertices
            // not yet included in MST
            int u = minKey(key, mstSet);

            // Add the picked vertex to the MST Set
            mstSet[u] = true;

            // Update key value and parent index of the adjacent vertices of
            // the picked vertex. Consider only those vertices which are not yet
            // included in MST
            for (int v = 0; v < V; v++)

               // graph[u][v] is non zero only for adjacent vertices of m
               // mstSet[v] is false for vertices not yet included in MST
               // Update the key only if graph[u][v] is smaller than key[v]
              if (graph[u][v] && mstSet[v] == false && graph[u][v] <  key[v])
                 parent[v]  = u, key[v] = graph[u][v];
         }

         // print the constructed MST
         printMST(parent, V, graph);
    }


    // driver program to test above function
    int main()
    {
       /* Let us create the following graph
              2    3
          (0)--(1)--(2)
           |   / \   |
          6| 8/   \5 |7
           | /     \ |
          (3)-------(4)
                9          */
       int graph[V][V] = {{0, 2, 0, 6, 0},
                          {2, 0, 3, 8, 5},
                          {0, 3, 0, 0, 7},
                          {6, 8, 0, 0, 9},
                          {0, 5, 7, 9, 0},
                         };

        // Print the solution
        primMST(graph);

        return 0;
    }

Output:

    Edge   Weight
    0 - 1    2
    1 - 2    3
    0 - 3    6
    1 - 4    5

Time Complexity of the above program is O(V^2). If the input [graph is
represented using adjacency
list](http://www.geeksforgeeks.org/archives/27134), then the time
complexity of Prim’s algorithm can be reduced to O(E log V) with the
help of binary heap. We will soon be discussing O(E Log V) algorithm as
a separate post.

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

   
Tags: [Graph](http://www.geeksforgeeks.org/tag/graph/),
[Greedy](http://www.geeksforgeeks.org/tag/greedy/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/), [Minimum
Spanning Tree](http://www.geeksforgeeks.org/tag/minimum-spanning-tree/),
[Prim's Algorithm](http://www.geeksforgeeks.org/tag/prims-algorithm/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-5-prims-minimum-spanning-tree-mst-2/>

Greedy Algorithms | Set 6 (Primâ€™s MST for Adjacency List Representation)
--------------------------------------------------------------------------

We recommend to read following two posts as a prerequisite of this
post.<span id="more-27580"></span>

**1.** [Greedy Algorithms | Set 5 (Primâ€™s Minimum Spanning Tree
(MST))](http://www.geeksforgeeks.org/archives/27455)  
 **2.** [Graph and its
representations](http://www.geeksforgeeks.org/archives/27134)

We have discussed [Prim’s algorithm and its implementation for adjacency
matrix representation of
graphs](http://www.geeksforgeeks.org/archives/27455). The time
complexity for the matrix representation is O(V^2). In this post,
O(ELogV) algorithm for adjacency list representation is discussed.  
 As discussed in the previous post, in Prim’s algorithm, two sets are
maintained, one set contains list of vertices already included in MST,
other set contains vertices not yet included. With adjacency list
representation, all vertices of a graph can be traversed in O(V+E) time
using [BFS](http://www.geeksforgeeks.org/archives/18382). The idea is to
traverse all vertices of graph using
[BFS](http://www.geeksforgeeks.org/archives/18382)and use a Min Heap to
store the vertices not yet included in MST. Min Heap is used as a
priority queue to get the minimum weight edge from the
[cut](http://en.wikipedia.org/wiki/Cut_%28graph_theory%29). Min Heap is
used as time complexity of operations like extracting minimum element
and decreasing key value is O(LogV) in Min Heap.

Following are the detailed steps.  
 **1)** Create a Min Heap of size V where V is the number of vertices in
the given graph. Every node of min heap contains vertex number and key
value of the vertex.  
 **2)** Initialize Min Heap with first vertex as root (the key value
assigned to first vertex is 0). The key value assigned to all other
vertices is INF (infinite).  
 **3)** While Min Heap is not empty, do following  
 …..**a)** Extract the min value node from Min Heap. Let the extracted
vertex be u.  
 …..**b)** For every adjacent vertex v of u, check if v is in Min Heap
(not yet included in MST). If v is in Min Heap and its key value is more
than weight of u-v, then update the key value of v as weight of u-v.

Let us understand the above algorithm with the following example:  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg)  
 Initially, key value of first vertex is 0 and INF (infinite) for all
other vertices. So vertex 0 is extracted from Min Heap and key values of
vertices adjacent to 0 (1 and 7) are updated. Min Heap contains all
vertices except vertex 0.  
 The vertices in green color are the vertices included in MST.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg "Fig-2")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg)  
 Since key value of vertex 1 is minimum among all nodes in Min Heap, it
is extracted from Min Heap and key values of vertices adjacent to 1 are
updated (Key is updated if the a vertex is not in Min Heap and previous
key value is greater than the weight of edge from 1 to the adjacent).
Min Heap contains all vertices except vertex 0 and 1.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST2.jpg "Fig-3")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST2.jpg)  
 Since key value of vertex 7 is minimum among all nodes in Min Heap, it
is extracted from Min Heap and key values of vertices adjacent to 7 are
updated (Key is updated if the a vertex is not in Min Heap and previous
key value is greater than the weight of edge from 7 to the adjacent).
Min Heap contains all vertices except vertex 0, 1 and 7.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST3.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST3.jpg)  
 Since key value of vertex 6 is minimum among all nodes in Min Heap, it
is extracted from Min Heap and key values of vertices adjacent to 6 are
updated (Key is updated if the a vertex is not in Min Heap and previous
key value is greater than the weight of edge from 6 to the adjacent).
Min Heap contains all vertices except vertex 0, 1, 7 and 6.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST4.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST4.jpg)  
 The above steps are repeated for rest of the nodes in Min Heap till Min
Heap becomes empty  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST5.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST5.jpg)

    // C / C++ program for Prim's MST for adjacency list representation of graph

    #include <stdio.h>
    #include <stdlib.h>
    #include <limits.h>

    // A structure to represent a node in adjacency list
    struct AdjListNode
    {
        int dest;
        int weight;
        struct AdjListNode* next;
    };

    // A structure to represent an adjacency liat
    struct AdjList
    {
        struct AdjListNode *head;  // pointer to head node of list
    };

    // A structure to represent a graph. A graph is an array of adjacency lists.
    // Size of array will be V (number of vertices in graph)
    struct Graph
    {
        int V;
        struct AdjList* array;
    };

    // A utility function to create a new adjacency list node
    struct AdjListNode* newAdjListNode(int dest, int weight)
    {
        struct AdjListNode* newNode =
                (struct AdjListNode*) malloc(sizeof(struct AdjListNode));
        newNode->dest = dest;
        newNode->weight = weight;
        newNode->next = NULL;
        return newNode;
    }

    // A utility function that creates a graph of V vertices
    struct Graph* createGraph(int V)
    {
        struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
        graph->V = V;

        // Create an array of adjacency lists.  Size of array will be V
        graph->array = (struct AdjList*) malloc(V * sizeof(struct AdjList));

         // Initialize each adjacency list as empty by making head as NULL
        for (int i = 0; i < V; ++i)
            graph->array[i].head = NULL;

        return graph;
    }

    // Adds an edge to an undirected graph
    void addEdge(struct Graph* graph, int src, int dest, int weight)
    {
        // Add an edge from src to dest.  A new node is added to the adjacency
        // list of src.  The node is added at the begining
        struct AdjListNode* newNode = newAdjListNode(dest, weight);
        newNode->next = graph->array[src].head;
        graph->array[src].head = newNode;

        // Since graph is undirected, add an edge from dest to src also
        newNode = newAdjListNode(src, weight);
        newNode->next = graph->array[dest].head;
        graph->array[dest].head = newNode;
    }

    // Structure to represent a min heap node
    struct MinHeapNode
    {
        int  v;
        int key;
    };

    // Structure to represent a min heap
    struct MinHeap
    {
        int size;      // Number of heap nodes present currently
        int capacity;  // Capacity of min heap
        int *pos;     // This is needed for decreaseKey()
        struct MinHeapNode **array;
    };

    // A utility function to create a new Min Heap Node
    struct MinHeapNode* newMinHeapNode(int v, int key)
    {
        struct MinHeapNode* minHeapNode =
               (struct MinHeapNode*) malloc(sizeof(struct MinHeapNode));
        minHeapNode->v = v;
        minHeapNode->key = key;
        return minHeapNode;
    }

    // A utilit function to create a Min Heap
    struct MinHeap* createMinHeap(int capacity)
    {
        struct MinHeap* minHeap =
             (struct MinHeap*) malloc(sizeof(struct MinHeap));
        minHeap->pos = (int *)malloc(capacity * sizeof(int));
        minHeap->size = 0;
        minHeap->capacity = capacity;
        minHeap->array =
             (struct MinHeapNode**) malloc(capacity * sizeof(struct MinHeapNode*));
        return minHeap;
    }

    // A utility function to swap two nodes of min heap. Needed for min heapify
    void swapMinHeapNode(struct MinHeapNode** a, struct MinHeapNode** b)
    {
        struct MinHeapNode* t = *a;
        *a = *b;
        *b = t;
    }

    // A standard function to heapify at given idx
    // This function also updates position of nodes when they are swapped.
    // Position is needed for decreaseKey()
    void minHeapify(struct MinHeap* minHeap, int idx)
    {
        int smallest, left, right;
        smallest = idx;
        left = 2 * idx + 1;
        right = 2 * idx + 2;

        if (left < minHeap->size &&
            minHeap->array[left]->key < minHeap->array[smallest]->key )
          smallest = left;

        if (right < minHeap->size &&
            minHeap->array[right]->key < minHeap->array[smallest]->key )
          smallest = right;

        if (smallest != idx)
        {
            // The nodes to be swapped in min heap
            MinHeapNode *smallestNode = minHeap->array[smallest];
            MinHeapNode *idxNode = minHeap->array[idx];

            // Swap positions
            minHeap->pos[smallestNode->v] = idx;
            minHeap->pos[idxNode->v] = smallest;

            // Swap nodes
            swapMinHeapNode(&minHeap->array[smallest], &minHeap->array[idx]);

            minHeapify(minHeap, smallest);
        }
    }

    // A utility function to check if the given minHeap is ampty or not
    int isEmpty(struct MinHeap* minHeap)
    {
        return minHeap->size == 0;
    }

    // Standard function to extract minimum node from heap
    struct MinHeapNode* extractMin(struct MinHeap* minHeap)
    {
        if (isEmpty(minHeap))
            return NULL;

        // Store the root node
        struct MinHeapNode* root = minHeap->array[0];

        // Replace root node with last node
        struct MinHeapNode* lastNode = minHeap->array[minHeap->size - 1];
        minHeap->array[0] = lastNode;

        // Update position of last node
        minHeap->pos[root->v] = minHeap->size-1;
        minHeap->pos[lastNode->v] = 0;

        // Reduce heap size and heapify root
        --minHeap->size;
        minHeapify(minHeap, 0);

        return root;
    }

    // Function to decreasy key value of a given vertex v. This function
    // uses pos[] of min heap to get the current index of node in min heap
    void decreaseKey(struct MinHeap* minHeap, int v, int key)
    {
        // Get the index of v in  heap array
        int i = minHeap->pos[v];

        // Get the node and update its key value
        minHeap->array[i]->key = key;

        // Travel up while the complete tree is not hepified.
        // This is a O(Logn) loop
        while (i && minHeap->array[i]->key < minHeap->array[(i - 1) / 2]->key)
        {
            // Swap this node with its parent
            minHeap->pos[minHeap->array[i]->v] = (i-1)/2;
            minHeap->pos[minHeap->array[(i-1)/2]->v] = i;
            swapMinHeapNode(&minHeap->array[i],  &minHeap->array[(i - 1) / 2]);

            // move to parent index
            i = (i - 1) / 2;
        }
    }

    // A utility function to check if a given vertex
    // 'v' is in min heap or not
    bool isInMinHeap(struct MinHeap *minHeap, int v)
    {
       if (minHeap->pos[v] < minHeap->size)
         return true;
       return false;
    }

    // A utility function used to print the constructed MST
    void printArr(int arr[], int n)
    {
        for (int i = 1; i < n; ++i)
            printf("%d - %d\n", arr[i], i);
    }

    // The main function that constructs Minimum Spanning Tree (MST)
    // using Prim's algorithm
    void PrimMST(struct Graph* graph)
    {
        int V = graph->V;// Get the number of vertices in graph
        int parent[V];   // Array to store constructed MST
        int key[V];      // Key values used to pick minimum weight edge in cut

        // minHeap represents set E
        struct MinHeap* minHeap = createMinHeap(V);

        // Initialize min heap with all vertices. Key value of
        // all vertices (except 0th vertex) is initially infinite
        for (int v = 1; v < V; ++v)
        {
            parent[v] = -1;
            key[v] = INT_MAX;
            minHeap->array[v] = newMinHeapNode(v, key[v]);
            minHeap->pos[v] = v;
        }

        // Make key value of 0th vertex as 0 so that it
        // is extracted first
        key[0] = 0;
        minHeap->array[0] = newMinHeapNode(0, key[0]);
        minHeap->pos[0]   = 0;

        // Initially size of min heap is equal to V
        minHeap->size = V;

        // In the followin loop, min heap contains all nodes
        // not yet added to MST.
        while (!isEmpty(minHeap))
        {
            // Extract the vertex with minimum key value
            struct MinHeapNode* minHeapNode = extractMin(minHeap);
            int u = minHeapNode->v; // Store the extracted vertex number

            // Traverse through all adjacent vertices of u (the extracted
            // vertex) and update their key values
            struct AdjListNode* pCrawl = graph->array[u].head;
            while (pCrawl != NULL)
            {
                int v = pCrawl->dest;

                // If v is not yet included in MST and weight of u-v is
                // less than key value of v, then update key value and
                // parent of v
                if (isInMinHeap(minHeap, v) && pCrawl->weight < key[v])
                {
                    key[v] = pCrawl->weight;
                    parent[v] = u;
                    decreaseKey(minHeap, v, key[v]);
                }
                pCrawl = pCrawl->next;
            }
        }

        // print edges of MST
        printArr(parent, V);
    }

    // Driver program to test above functions
    int main()
    {
        // Let us create the graph given in above fugure
        int V = 9;
        struct Graph* graph = createGraph(V);
        addEdge(graph, 0, 1, 4);
        addEdge(graph, 0, 7, 8);
        addEdge(graph, 1, 2, 8);
        addEdge(graph, 1, 7, 11);
        addEdge(graph, 2, 3, 7);
        addEdge(graph, 2, 8, 2);
        addEdge(graph, 2, 5, 4);
        addEdge(graph, 3, 4, 9);
        addEdge(graph, 3, 5, 14);
        addEdge(graph, 4, 5, 10);
        addEdge(graph, 5, 6, 2);
        addEdge(graph, 6, 7, 1);
        addEdge(graph, 6, 8, 6);
        addEdge(graph, 7, 8, 7);

        PrimMST(graph);

        return 0;
    }

Output:

    0 - 1
    5 - 2
    2 - 3
    3 - 4
    6 - 5
    7 - 6
    0 - 7
    2 - 8

**Time Complexity:** The time complexity of the above code/algorithm
looks O(V^2) as there are two nested while loops. If we take a closer
look, we can observe that the statements in inner loop are executed
O(V+E) times (similar to BFS). The inner loop has decreaseKey()
operation which takes O(LogV) time. So overall time complexity is
O(E+V)\*O(LogV) which is O((E+V)\*LogV) = O(ELogV) (For a connected
graph, V = O(E))

**References:**  
 [Introduction to Algorithms by Clifford Stein, Thomas H. Cormen,
Charles E. Leiserson, Ronald L.  
](http://www.flipkart.com/introduction-algorithms-8120340078/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)  

[http://en.wikipedia.org/wiki/Prim’s\_algorithm](http://en.wikipedia.org/wiki/Prim's_algorithm)

This article is compiled by [Aashish
Barnwal](https://www.facebook.com/barnwal.aashish) and reviewed by
GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above.

   
Tags: [Graph](http://www.geeksforgeeks.org/tag/graph/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-5-prims-mst-for-adjacency-list-representation/>

Greedy Algorithms | Set 7 (Dijkstra’s shortest path algorithm)
--------------------------------------------------------------

Given a graph and a source vertex in graph, find shortest paths from
source to all vertices in the given graph.<span id="more-27697"></span>

Dijkstra’s algorithm is very similar to [Prim’s algorithm for minimum
spanning tree](http://www.geeksforgeeks.org/archives/27455). Like Prim’s
MST, we generate a *SPT (shortest path tree)* with given source as root.
We maintain two sets, one set contains vertices included in shortest
path tree, other set includes vertices not yet included in shortest path
tree. At every step of the algorithm, we find a vertex which is in the
other set (set of not yet included) and has minimum distance from
source.

Below are the detailed steps used in Dijkstra’s algorithm to find the
shortest path from a single source vertex to all other vertices in the
given graph.  
 Algorithm  
 **1)** Create a set *sptSet* (shortest path tree set) that keeps track
of vertices included in shortest path tree, i.e., whose minimum distance
from source is calculated and finalized. Initially, this set is empty.  
 **2)** Assign a distance value to all vertices in the input graph.
Initialize all distance values as INFINITE. Assign distance value as 0
for the source vertex so that it is picked first.  
 **3)** While *sptSet* doesn’t include all vertices  
 â€¦.**a)** Pick a vertex u which is not there in *sptSet*and has
minimum distance value.  
 â€¦.**b)** Include u to *sptSet*.  
 â€¦.**c)** Update distance value of all adjacent vertices of u. To
update the distance values, iterate through all adjacent vertices. For
every adjacent vertex v, if sum of distance value of u (from source) and
weight of edge u-v, is less than the distance value of v, then update
the distance value of v.

Let us understand with the following example:  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg)

The set *sptSet*is initially empty and distances assigned to vertices
are {0, INF, INF, INF, INF, INF, INF, INF} where INF indicates infinite.
Now pick the vertex with minimum distance value. The vertex 0 is picked,
include it in *sptSet*. So *sptSet* becomes {0}. After including 0 to
*sptSet*, update distance values of its adjacent vertices. Adjacent
vertices of 0 are 1 and 7. The distance values of 1 and 7 are updated as
4 and 8. Following subgraph shows vertices and their distance values,
only the vertices with finite distance values are shown. The vertices
included in SPT are shown in green color.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg "Fig-2")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg)

Pick the vertex with minimum distance value and not already included in
SPT (not in sptSET). The vertex 1 is picked and added to sptSet. So
sptSet now becomes {0, 1}. Update the distance values of adjacent
vertices of 1. The distance value of vertex 2 becomes 12.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ2.jpg "Fig-3")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ2.jpg)

Pick the vertex with minimum distance value and not already included in
SPT (not in sptSET). Vertex 7 is picked. So sptSet now becomes {0, 1,
7}. Update the distance values of adjacent vertices of 7. The distance
value of vertex 6 and 8 becomes finite (15 and 9 respectively).  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ3.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ3.jpg)

Pick the vertex with minimum distance value and not already included in
SPT (not in sptSET). Vertex 6 is picked. So sptSet now becomes {0, 1, 7,
6}. Update the distance values of adjacent vertices of 6. The distance
value of vertex 5 and 8 are updated.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ4.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ4.jpg)

We repeat the above steps until *sptSet* doesn’t include all vertices of
given graph. Finally, we get the following Shortest Path Tree (SPT).

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ5.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ5.jpg)

***How to implement the above algorithm?***  
 We use a boolean array sptSet[] to represent the set of vertices
included in SPT. If a value sptSet[v] is true, then vertex v is included
in SPT, otherwise not. Array dist[] is used to store shortest distance
values of all vertices.

    // A C / C++ program for Dijkstra's single source shortest path algorithm.
    // The program is for adjacency matrix representation of the graph

    #include <stdio.h>
    #include <limits.h>

    // Number of vertices in the graph
    #define V 9

    // A utility function to find the vertex with minimum distance value, from
    // the set of vertices not yet included in shortest path tree
    int minDistance(int dist[], bool sptSet[])
    {
       // Initialize min value
       int min = INT_MAX, min_index;

       for (int v = 0; v < V; v++)
         if (sptSet[v] == false && dist[v] <= min)
             min = dist[v], min_index = v;

       return min_index;
    }

    // A utility function to print the constructed distance array
    int printSolution(int dist[], int n)
    {
       printf("Vertex   Distance from Source\n");
       for (int i = 0; i < V; i++)
          printf("%d \t\t %d\n", i, dist[i]);
    }

    // Funtion that implements Dijkstra's single source shortest path algorithm
    // for a graph represented using adjacency matrix representation
    void dijkstra(int graph[V][V], int src)
    {
         int dist[V];     // The output array.  dist[i] will hold the shortest
                          // distance from src to i

         bool sptSet[V]; // sptSet[i] will true if vertex i is included in shortest
                         // path tree or shortest distance from src to i is finalized

         // Initialize all distances as INFINITE and stpSet[] as false
         for (int i = 0; i < V; i++)
            dist[i] = INT_MAX, sptSet[i] = false;

         // Distance of source vertex from itself is always 0
         dist[src] = 0;

         // Find shortest path for all vertices
         for (int count = 0; count < V-1; count++)
         {
           // Pick the minimum distance vertex from the set of vertices not
           // yet processed. u is always equal to src in first iteration.
           int u = minDistance(dist, sptSet);

           // Mark the picked vertex as processed
           sptSet[u] = true;

           // Update dist value of the adjacent vertices of the picked vertex.
           for (int v = 0; v < V; v++)

             // Update dist[v] only if is not in sptSet, there is an edge from 
             // u to v, and total weight of path from src to  v through u is 
             // smaller than current value of dist[v]
             if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX 
                                           && dist[u]+graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
         }

         // print the constructed distance array
         printSolution(dist, V);
    }

    // driver program to test above function
    int main()
    {
       /* Let us create the example graph discussed above */
       int graph[V][V] = {{0, 4, 0, 0, 0, 0, 0, 8, 0},
                          {4, 0, 8, 0, 0, 0, 0, 11, 0},
                          {0, 8, 0, 7, 0, 4, 0, 0, 2},
                          {0, 0, 7, 0, 9, 14, 0, 0, 0},
                          {0, 0, 0, 9, 0, 10, 0, 0, 0},
                          {0, 0, 4, 0, 10, 0, 2, 0, 0},
                          {0, 0, 0, 14, 0, 2, 0, 1, 6},
                          {8, 11, 0, 0, 0, 0, 1, 0, 7},
                          {0, 0, 2, 0, 0, 0, 6, 7, 0}
                         };

        dijkstra(graph, 0);

        return 0;
    }

Output:

    Vertex   Distance from Source
    0                0
    1                4
    2                12
    3                19
    4                21
    5                11
    6                9
    7                8
    8                14

**Notes:**  
 **1)** The code calculates shortest distance, but doesn’t calculate the
path information. We can create a parent array, update the parent array
when distance is updated (like [prim’s
implementation](http://www.geeksforgeeks.org/archives/27455)) and use it
show the shortest path from source to different vertices.

**2)** The code is for undirected graph, same dijekstra function can be
used for directed graphs also.

**3)** The code finds shortest distances from source to all vertices. If
we are interested only in shortest distance from source to a single
target, we can break the for loop when the picked minimum distance
vertex is equal to target (Step 3.a of algorithm).

**4)** Time Complexity of the implementation is O(V^2). If the input
[graph is represented using adjacency
list](http://www.geeksforgeeks.org/archives/27134), it can be reduced to
O(E log V) with the help of binary heap. We will soon be discussing O(E
Log V) algorithm as a separate post.

**5)** Dijkstra’s algorithm doesn’t work for graphs with negative weight
edges. For graphs with negative weight edges, [Bellmanâ€“Ford
algorithm](http://en.wikipedia.org/wiki/Bellman-Ford_algorithm) can be
used, we will soon be discussing it as a separate post.  
 Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

   
Tags: [Dijkstra](http://www.geeksforgeeks.org/tag/dijkstra/),
[Graph](http://www.geeksforgeeks.org/tag/graph/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-6-dijkstras-shortest-path-algorithm/>

Greedy Algorithms | Set 8 (Dijkstraâ€™s Algorithm for Adjacency List Representation)
------------------------------------------------------------------------------------

We recommend to read following two posts as a prerequisite of this post.

**1.** [Greedy Algorithms | Set 7 (Dijkstraâ€™s shortest path
algorithm)](http://www.geeksforgeeks.org/archives/27697)  
 **2.**Â [Graph and its
representations](http://www.geeksforgeeks.org/archives/27134)<span
id="more-27753"></span>

We have discussed [Dijkstra’s algorithm and its implementation for
adjacency matrix representation of
graphs](http://www.geeksforgeeks.org/archives/27697). The time
complexity for the matrix representation is O(V^2). In this post,
O(ELogV) algorithm for adjacency list representation is discussed.

As discussed in the previous post, in Dijkstra’s algorithm, two sets are
maintained, one set contains list of vertices already included in SPT
(Shortest Path Tree), other set contains vertices not yet included. With
adjacency list representation, all vertices of a graph can be traversed
in O(V+E) time
usingÂ [BFS](http://www.geeksforgeeks.org/archives/18382). The idea is
to traverse all vertices of graph
usingÂ [BFSÂ ](http://www.geeksforgeeks.org/archives/18382)and use a Min
Heap to store the vertices not yet included in SPT (or the vertices for
which shortest distance is not finalized yet). Â Min Heap is used as a
priority queue to get the minimum distance vertex from set of not
yetÂ includedÂ vertices. Time complexity of operations like extract-min
and decrease-key value is O(LogV) for Min Heap.

Following are the detailed steps.  
 **1)Â **Create a Min Heap of size V where V is the number of vertices
in the given graph. Every node of min heap contains vertex number and
distance value of the vertex.  
 **2)**Â Initialize Min Heap with source vertex as root (the distance
value assigned to source vertex is 0). The distance value assigned to
all other vertices is INF (infinite).  
 **3)Â **While Min Heap is not empty, do following  
 â€¦..**a)**Â Extract the vertex with minimum distance value node from
Min Heap. Let the extracted vertex be u.  
 â€¦..**b)**Â For every adjacent vertex v of u, check if v is in Min
Heap. If v is in Min Heap and distance value is more than weight of u-v
plus distance value of u, then update the distance value of v.

Let us understand with the following example. Let the given source
vertex be 0  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Fig-11.jpg)

Initially, distance value of source vertex is 0 and INF (infinite) for
all other vertices. So source vertex is extracted from Min Heap and
distance values of vertices adjacent to 0 (1 and 7) are updated. Min
Heap contains all vertices except vertex 0.  
 The vertices in green color are the vertices for which minimum
distances are finalized and are not in Min Heap

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg "Fig-2")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/MST1.jpg)

Since distance value of vertex 1 is minimum among all nodes in Min Heap,
it is extracted from Min Heap and distance values of vertices adjacent
to 1 are updated (distance is updated if the a vertex is not in Min Heap
and distance through 1 is shorter than the previous distance). Min Heap
contains all vertices except vertex 0 and 1.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ2.jpg "Fig-3")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ2.jpg)

Pick the vertex with minimum distance value from min heap. Vertex 7 is
picked. So min heap now contains all vertices except 0, 1 and 7. Update
the distance values of adjacent vertices of 7. The distance value of
vertex 6 and 8 becomes finite (15 and 9 respectively).  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ3.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ3.jpg)

Pick the vertex with minimum distance from min heap. Vertex 6 is picked.
So min heap now contains all vertices except 0, 1, 7 and 6. Update the
distance values of adjacent vertices of 6. The distance value of vertex
5 and 8 are updated.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ4.jpg "Fig-4")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ4.jpg)

Above steps are repeated till min heap doesn’t become empty. Finally, we
get the following shortest path tree.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ5.jpg "Fig-1")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/DIJ5.jpg)

    // C / C++ program for Dijkstra's shortest path algorithm for adjacency
    // list representation of graph

    #include <stdio.h>
    #include <stdlib.h>
    #include <limits.h>

    // A structure to represent a node in adjacency list
    struct AdjListNode
    {
        int dest;
        int weight;
        struct AdjListNode* next;
    };

    // A structure to represent an adjacency liat
    struct AdjList
    {
        struct AdjListNode *head;  // pointer to head node of list
    };

    // A structure to represent a graph. A graph is an array of adjacency lists.
    // Size of array will be V (number of vertices in graph)
    struct Graph
    {
        int V;
        struct AdjList* array;
    };

    // A utility function to create a new adjacency list node
    struct AdjListNode* newAdjListNode(int dest, int weight)
    {
        struct AdjListNode* newNode =
                (struct AdjListNode*) malloc(sizeof(struct AdjListNode));
        newNode->dest = dest;
        newNode->weight = weight;
        newNode->next = NULL;
        return newNode;
    }

    // A utility function that creates a graph of V vertices
    struct Graph* createGraph(int V)
    {
        struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
        graph->V = V;

        // Create an array of adjacency lists.  Size of array will be V
        graph->array = (struct AdjList*) malloc(V * sizeof(struct AdjList));

         // Initialize each adjacency list as empty by making head as NULL
        for (int i = 0; i < V; ++i)
            graph->array[i].head = NULL;

        return graph;
    }

    // Adds an edge to an undirected graph
    void addEdge(struct Graph* graph, int src, int dest, int weight)
    {
        // Add an edge from src to dest.  A new node is added to the adjacency
        // list of src.  The node is added at the begining
        struct AdjListNode* newNode = newAdjListNode(dest, weight);
        newNode->next = graph->array[src].head;
        graph->array[src].head = newNode;

        // Since graph is undirected, add an edge from dest to src also
        newNode = newAdjListNode(src, weight);
        newNode->next = graph->array[dest].head;
        graph->array[dest].head = newNode;
    }

    // Structure to represent a min heap node
    struct MinHeapNode
    {
        int  v;
        int dist;
    };

    // Structure to represent a min heap
    struct MinHeap
    {
        int size;      // Number of heap nodes present currently
        int capacity;  // Capacity of min heap
        int *pos;     // This is needed for decreaseKey()
        struct MinHeapNode **array;
    };

    // A utility function to create a new Min Heap Node
    struct MinHeapNode* newMinHeapNode(int v, int dist)
    {
        struct MinHeapNode* minHeapNode =
               (struct MinHeapNode*) malloc(sizeof(struct MinHeapNode));
        minHeapNode->v = v;
        minHeapNode->dist = dist;
        return minHeapNode;
    }

    // A utility function to create a Min Heap
    struct MinHeap* createMinHeap(int capacity)
    {
        struct MinHeap* minHeap =
             (struct MinHeap*) malloc(sizeof(struct MinHeap));
        minHeap->pos = (int *)malloc(capacity * sizeof(int));
        minHeap->size = 0;
        minHeap->capacity = capacity;
        minHeap->array =
             (struct MinHeapNode**) malloc(capacity * sizeof(struct MinHeapNode*));
        return minHeap;
    }

    // A utility function to swap two nodes of min heap. Needed for min heapify
    void swapMinHeapNode(struct MinHeapNode** a, struct MinHeapNode** b)
    {
        struct MinHeapNode* t = *a;
        *a = *b;
        *b = t;
    }

    // A standard function to heapify at given idx
    // This function also updates position of nodes when they are swapped.
    // Position is needed for decreaseKey()
    void minHeapify(struct MinHeap* minHeap, int idx)
    {
        int smallest, left, right;
        smallest = idx;
        left = 2 * idx + 1;
        right = 2 * idx + 2;

        if (left < minHeap->size &&
            minHeap->array[left]->dist < minHeap->array[smallest]->dist )
          smallest = left;

        if (right < minHeap->size &&
            minHeap->array[right]->dist < minHeap->array[smallest]->dist )
          smallest = right;

        if (smallest != idx)
        {
            // The nodes to be swapped in min heap
            MinHeapNode *smallestNode = minHeap->array[smallest];
            MinHeapNode *idxNode = minHeap->array[idx];

            // Swap positions
            minHeap->pos[smallestNode->v] = idx;
            minHeap->pos[idxNode->v] = smallest;

            // Swap nodes
            swapMinHeapNode(&minHeap->array[smallest], &minHeap->array[idx]);

            minHeapify(minHeap, smallest);
        }
    }

    // A utility function to check if the given minHeap is ampty or not
    int isEmpty(struct MinHeap* minHeap)
    {
        return minHeap->size == 0;
    }

    // Standard function to extract minimum node from heap
    struct MinHeapNode* extractMin(struct MinHeap* minHeap)
    {
        if (isEmpty(minHeap))
            return NULL;

        // Store the root node
        struct MinHeapNode* root = minHeap->array[0];

        // Replace root node with last node
        struct MinHeapNode* lastNode = minHeap->array[minHeap->size - 1];
        minHeap->array[0] = lastNode;

        // Update position of last node
        minHeap->pos[root->v] = minHeap->size-1;
        minHeap->pos[lastNode->v] = 0;

        // Reduce heap size and heapify root
        --minHeap->size;
        minHeapify(minHeap, 0);

        return root;
    }

    // Function to decreasy dist value of a given vertex v. This function
    // uses pos[] of min heap to get the current index of node in min heap
    void decreaseKey(struct MinHeap* minHeap, int v, int dist)
    {
        // Get the index of v in  heap array
        int i = minHeap->pos[v];

        // Get the node and update its dist value
        minHeap->array[i]->dist = dist;

        // Travel up while the complete tree is not hepified.
        // This is a O(Logn) loop
        while (i && minHeap->array[i]->dist < minHeap->array[(i - 1) / 2]->dist)
        {
            // Swap this node with its parent
            minHeap->pos[minHeap->array[i]->v] = (i-1)/2;
            minHeap->pos[minHeap->array[(i-1)/2]->v] = i;
            swapMinHeapNode(&minHeap->array[i],  &minHeap->array[(i - 1) / 2]);

            // move to parent index
            i = (i - 1) / 2;
        }
    }

    // A utility function to check if a given vertex
    // 'v' is in min heap or not
    bool isInMinHeap(struct MinHeap *minHeap, int v)
    {
       if (minHeap->pos[v] < minHeap->size)
         return true;
       return false;
    }

    // A utility function used to print the solution
    void printArr(int dist[], int n)
    {
        printf("Vertex   Distance from Source\n");
        for (int i = 0; i < n; ++i)
            printf("%d \t\t %d\n", i, dist[i]);
    }

    // The main function that calulates distances of shortest paths from src to all
    // vertices. It is a O(ELogV) function
    void dijkstra(struct Graph* graph, int src)
    {
        int V = graph->V;// Get the number of vertices in graph
        int dist[V];      // dist values used to pick minimum weight edge in cut

        // minHeap represents set E
        struct MinHeap* minHeap = createMinHeap(V);

        // Initialize min heap with all vertices. dist value of all vertices 
        for (int v = 0; v < V; ++v)
        {
            dist[v] = INT_MAX;
            minHeap->array[v] = newMinHeapNode(v, dist[v]);
            minHeap->pos[v] = v;
        }

        // Make dist value of src vertex as 0 so that it is extracted first
        minHeap->array[src] = newMinHeapNode(src, dist[src]);
        minHeap->pos[src]   = src;
        dist[src] = 0;
        decreaseKey(minHeap, src, dist[src]);

        // Initially size of min heap is equal to V
        minHeap->size = V;

        // In the followin loop, min heap contains all nodes
        // whose shortest distance is not yet finalized.
        while (!isEmpty(minHeap))
        {
            // Extract the vertex with minimum distance value
            struct MinHeapNode* minHeapNode = extractMin(minHeap);
            int u = minHeapNode->v; // Store the extracted vertex number

            // Traverse through all adjacent vertices of u (the extracted
            // vertex) and update their distance values
            struct AdjListNode* pCrawl = graph->array[u].head;
            while (pCrawl != NULL)
            {
                int v = pCrawl->dest;

                // If shortest distance to v is not finalized yet, and distance to v
                // through u is less than its previously calculated distance
                if (isInMinHeap(minHeap, v) && dist[u] != INT_MAX && 
                                              pCrawl->weight + dist[u] < dist[v])
                {
                    dist[v] = dist[u] + pCrawl->weight;

                    // update distance value in min heap also
                    decreaseKey(minHeap, v, dist[v]);
                }
                pCrawl = pCrawl->next;
            }
        }

        // print the calculated shortest distances
        printArr(dist, V);
    }


    // Driver program to test above functions
    int main()
    {
        // create the graph given in above fugure
        int V = 9;
        struct Graph* graph = createGraph(V);
        addEdge(graph, 0, 1, 4);
        addEdge(graph, 0, 7, 8);
        addEdge(graph, 1, 2, 8);
        addEdge(graph, 1, 7, 11);
        addEdge(graph, 2, 3, 7);
        addEdge(graph, 2, 8, 2);
        addEdge(graph, 2, 5, 4);
        addEdge(graph, 3, 4, 9);
        addEdge(graph, 3, 5, 14);
        addEdge(graph, 4, 5, 10);
        addEdge(graph, 5, 6, 2);
        addEdge(graph, 6, 7, 1);
        addEdge(graph, 6, 8, 6);
        addEdge(graph, 7, 8, 7);

        dijkstra(graph, 0);

        return 0;
    }

Output:

    Vertex   Distance from Source
    0                0
    1                4
    2                12
    3                19
    4                21
    5                11
    6                9
    7                8
    8                14

**Time Complexity:**Â The time complexity of the above code/algorithm
looks O(V^2) as there are two nested while loops. If we take a closer
look, we can observe that the statements in inner loop are executed
O(V+E) times (similar to BFS). The inner loop has decreaseKey()
operation which takes O(LogV) time. So overall time complexity is
O(E+V)\*O(LogV) which is O((E+V)\*LogV) = O(ELogV)  
 Note that the above code uses Binary Heap for Priority Queue
implementation. Time complexity can be reduced to O(E + VLogV) using
Fibonacci Heap. The reason is, Fibonacci Heap takes O(1) time for
decrease-key operation while Binary Heap takes O(Logn) time.

**Notes:**  
 **1)**Â The code calculates shortest distance, but doesnâ€™t calculate
the path information. We can create a parent array, update the parent
array when distance is updated (likeÂ [primâ€™s
implementation](http://www.geeksforgeeks.org/archives/27580)) and use it
show the shortest path from source to different vertices.

**2)**Â The code is for undirected graph, same dijekstra function can be
used for directed graphs also.

**3)**Â The code finds shortest distances from source to all vertices.
If we are interested only in shortest distance from source to a single
target, we can break the for loop when the picked minimum distance
vertex is equal to target (Step 3.a of algorithm).

**4)**Â Dijkstraâ€™s algorithm doesn’t work for graphs with negative
weight edges. For graphs with negative weight edges,Â [Bellmanâ€“Ford
algorithm](http://en.wikipedia.org/wiki/Bellman-Ford_algorithm)Â can be
used, we will soon be discussing it as a separate post.

**References:**  
 [Introduction to Algorithms by Clifford Stein, Thomas H. Cormen,
Charles E. Leiserson, Ronald L.  
](http://www.flipkart.com/introduction-algorithms-8120340078/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)[Algorithms
by Sanjoy Dasgupta, Christos Papadimitriou, Umesh
Vazirani](http://www.flipkart.com/algorithms-0070636613/p/itmczynvb7p2zacz?pid=9780070636613&affid=sandeepgfg)

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

   
Tags: [Dijkstra](http://www.geeksforgeeks.org/tag/dijkstra/),
[Graph](http://www.geeksforgeeks.org/tag/graph/), [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/greedy-algorithms-set-7-dijkstras-algorithm-for-adjacency-list-representation/>

Job Sequencing Problem | Set 1 (Greedy Algorithm)
-------------------------------------------------

Given an array of jobs where every job has a deadline and associated
profit if the job is finished before the deadline. <span
id="more-132724"></span>It is also given that every job takes single
unit of time, so the minimum possible deadline for any job is 1. How to
maximize total profit if only one job can be scheduled at a time.

**Examples:**

    Input: Four Jobs with following deadlines and profits
      JobID    Deadline      Profit
        a        4            20   
        b        1            10
        c        1            40  
        d        1            30
    Output: Following is maximum profit sequence of jobs
            c, a   


    Input:  Five Jobs with following deadlines and profits
       JobID     Deadline     Profit
         a         2           100
         b         1           19
         c         2           27
         d         1           25
         e         3           15
    Output: Following is maximum profit sequence of jobs
            c, a, e

**We strongly recommend to minimize your browser and try this yourself
first.**

A **Simple Solution** is to generate all subsets of given set of jobs
and check individual subset for feasibility of jobs in that subset. Keep
track of maximum profit among all feasible subsets. The time complexity
of this solution is exponential.

This is a standard [Greedy
Algorithm](http://www.geeksforgeeks.org/greedy-algorithms-set-1-activity-selection-problem/)problem.
Following is algorithm.

    1) Sort all jobs in decreasing order of profit.
    2) Initialize the result sequence as first job in sorted jobs.
    3) Do following for remaining n-1 jobs
    .......a) If the current job can fit in the current result sequence 
              without missing the deadline, add current job to the result.
              Else ignore the current job.

The Following is C++ implementation of above algorithm.

    // Program to find the maximum profit job sequence from a given array
    // of jobs with deadlines and profits
    #include<iostream>
    #include<algorithm>
    using namespace std;

    // A structure to represent a job
    struct Job
    {
       char id;      // Job Id
       int dead;    // Deadline of job
       int profit;  // Profit if job is over before or on deadline
    };

    // This function is used for sorting all jobs according to profit
    bool comparison(Job a, Job b)
    {
         return (a.profit > b.profit);
    }

    // Returns minimum number of platforms reqquired
    void printJobScheduling(Job arr[], int n)
    {
        // Sort all jobs according to decreasing order of prfit
        sort(arr, arr+n, comparison);

        int result[n]; // To store result (Sequence of jobs)
        bool slot[n];  // To keep track of free time slots

        // Initialize all slots to be free
        for (int i=0; i<n; i++)
            slot[i] = false;

        // Iterate through all given jobs
        for (int i=0; i<n; i++)
        {
           // Find a free slot for this job (Note that we start
           // from the last possible slot)
           for (int j=min(n, arr[i].dead)-1; j>=0; j--)
           {
              // Free slot found
              if (slot[j]==false)
              {
                 result[j] = i;  // Add this job to result
                 slot[j] = true; // Make this slot occupied
                 break;
              }
           }
        }

        // Print the result
        for (int i=0; i<n; i++)
           if (slot[i])
             cout << arr[result[i]].id << " ";
    }

    // Driver program to test methods
    int main()
    {
        Job arr[5] = { {'a', 2, 100}, {'b', 1, 19}, {'c', 2, 27},
                       {'d', 1, 25}, {'e', 3, 15}};
        int n = sizeof(arr)/sizeof(arr[0]);
        cout << "Following is maximum profit sequence of jobs\n";
        printJobScheduling(arr, n);
        return 0;
    }

Output:

    Following is maximum profit sequence of jobs
    c a e

**Time Complexity** of the above solution is O(n<sup>2</sup>). It can be
optimized to almost O(n) by using [union-find data
structure](http://www.geeksforgeeks.org/union-find/). We will son be
discussing the optimized solution.

**Sources:**  

<http://ocw.mit.edu/courses/civil-and-environmental-engineering/1-204-computer-algorithms-in-systems-engineering-spring-2010/lecture-notes/MIT1_204S10_lec10.pdf>

This article is contributed by **Shubham**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above.

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/job-sequencing-problem-set-1-greedy-algorithm/>

Minimize Cash Flow among a given set of friends who have borrowed money from each other
---------------------------------------------------------------------------------------

Given a number of friends who have to give or take some amount of money
from one another. Design an algorithm by which the total cash flow among
all the friends is minimized. <span id="more-133526"></span>

Example:  
 Following diagram shows input debts to be settled.  

[![cashFlow](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/cashFlow.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/cashFlow.png)

Above debts can be settled in following optimized way  

[![cashFlow](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/cashFlow1.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/cashFlow1.png)

**We strongly recommend to minimize your browser and try this yourself
first.**  
 The idea is to use [Greedy
algorithm](http://www.geeksforgeeks.org/tag/Greedy-Algorithm/) where at
every step, settle all amounts of one person and recur for remaining n-1
persons.  
 How to pick the first person? To pick the first person, calculate the
net amount for every person where net amount is obtained by subtracting
all debts (amounts to pay) from all credits (amounts to be paid). Once
net amount for every person is evaluated, find two persons with maximum
and minimum net amounts. These two persons are the most creditors and
debtors. The person with minimum of two is our first person to be
settled and removed from list. Let the minimum of two amounts be x. We
pay ‘x’ amount from the maximum debtor to maximum creditor and settle
one person. If x is equal to the maximum debit, then maximum debtor is
settled, else maximum creditor is settled.

The following is detailed algorithm.

Do following for every person Pi where i is from 0 to n-1.  
 **1)** Compute the net amount for every person. The net amount for
person ‘i’ can be computed be subtracting sum of all debts from sum of
all credits.

**2)** Find the two persons that are maximum creditor and maximum
debtor. Let the maximum amount to be credited maximum creditor be
maxCredit and maximum amount to be debited from maximum debtor be
maxDebit. Let the maximum debtor be Pd and maximum creditor be Pc.

**3)** Find the minimum of maxDebit and maxCredit. Let minimum of two be
x. Debit ‘x’ from Pd and credit this amount to Pc

**4)** If x is equal to maxCredit, then remove Pc from set of persons
and recur for remaining (n-1) persons.  
 **  
 5)** If x is equal to maxDebit, then remove Pd from set of persons and
recur for remaining (n-1) persons.

Thanks to Balaji S for suggesting this method in a comment
[here](http://www.geeksforgeeks.org/amazon-interview-experience-set-165-sde/).

The following is C++ implementation of above algorithm.

    // C++ program to fin maximum cash flow among a set of persons
    #include<iostream>
    using namespace std;

    // Number of persons (or vertices in the graph)
    #define N 3

    // A utility function that returns index of minimum value in arr[]
    int getMin(int arr[])
    {
        int minInd = 0;
        for (int i=1; i<N; i++)
            if (arr[i] < arr[minInd])
                minInd = i;
        return minInd;
    }

    // A utility function that returns index of maximum value in arr[]
    int getMax(int arr[])
    {
        int maxInd = 0;
        for (int i=1; i<N; i++)
            if (arr[i] > arr[maxInd])
                maxInd = i;
        return maxInd;
    }

    // A utility function to return minimum of 2 values
    int minOf2(int x, int y)
    {
        return (x<y)? x: y;
    }

    // amount[p] indicates the net amount to be credited/debited
    // to/from person 'p'
    // If amount[p] is positive, then i'th person will amount[i]
    // If amount[p] is negative, then i'th person will give  -amount[i]
    void minCashFlowRec(int amount[])
    {
        // Find the indexes of minimum and maximum values in amount[]
        // amount[mxCredit] indicates the maximum amount to be given
        //                  (or credited) to any person .
        // And amount[mxDebit] indicates the maximum amount to be taken
        //                  (or debited) from any person.
        // So if there is a positive value in amount[], then there must
        // be a negative value
        int mxCredit = getMax(amount), mxDebit = getMin(amount);

        // If both amounts are 0, then all amounts are settled
        if (amount[mxCredit] == 0 && amount[mxDebit] == 0)
            return;

        // Find the minimum of two amounts
        int min = minOf2(-amount[mxDebit], amount[mxCredit]);
        amount[mxCredit] -= min;
        amount[mxDebit] += min;

        // If minimum is the maximum amount to be
        cout << "Person " << mxDebit << " pays " << min
             << " to " << "Person " << mxCredit << endl;

        // Recur for the amount array.  Note that it is guaranteed that
        // the recursion would terminate as either amount[mxCredit] 
        // or  amount[mxDebit] becomes 0
        minCashFlowRec(amount);
    }

    // Given a set of persons as graph[] where graph[i][j] indicates
    // the amount that person i needs to pay person j, this function
    // finds and prints the minimum cash flow to settle all debts.
    void minCashFlow(int graph[][N])
    {
        // Create an array amount[], initialize all value in it as 0.
        int amount[N] = {0};

        // Calculate the net amount to be paid to person 'p', and
        // stores it in amount[p]. The value of amount[p] can be
        // calculated by subtracting debts of 'p' from credits of 'p'
        for (int p=0; p<N; p++)
           for (int i=0; i<N; i++)
              amount[p] += (graph[i][p] -  graph[p][i]);

        minCashFlowRec(amount);
    }

    // Driver program to test above function
    int main()
    {
        // graph[i][j] indicates the amount that person i needs to
        // pay person j
        int graph[N][N] = { {0, 1000, 2000},
                            {0, 0, 5000},
                            {0, 0, 0},};

        // Print the solution
        minCashFlow(graph);
        return 0;
    }

Output:

    Person 1 pays 4000 to Person 2
    Person 0 pays 3000 to Person 2

**Algorithmic Paradigm:** Greedy  
 **Time Complexity:** O(N<sup>2</sup>) where N is the number of persons.

This article is contributed by **Gaurav**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/minimize-cash-flow-among-given-set-friends-borrowed-money/>

Minimum Number of Platforms Required for a Railway/Bus Station
--------------------------------------------------------------

Given arrival and departure times of all trains that reach a railway
station, find the minimum number of platforms required for the railway
station so that no train waits.<span id="more-132642"></span>  
 We are given two arrays which represent arrival and departure times of
trains that stop

Examples:

    Input:  arr[]  = {9:00,  9:40, 9:50,  11:00, 15:00, 18:00}
            dep[]  = {9:10, 12:00, 11:20, 11:30, 19:00, 20:00}
    Output: 3
    There are at-most three trains at a time (time between 11:00 to 11:20)

**We strongly recommend to minimize your browser and try this yourself
first.**  
 We need to find the maximum number of trains that are there on the
given railway station at a time. A **Simple Solution** is to take every
interval one by one and find the number of intervals that overlap with
it. Keep track of maximum number of intervals that overlap with an
interval. Finally return the maximum value. Time Complexity of this
solution is O(n<sup>2</sup>).

We can solve the above problem **in O(nLogn) time**. The idea is to
consider all evens in sorted order. Once we have all events in sorted
order, we can trace the number of trains at any time keeping track of
trains that have arrived, but not departed.

For example consider the above example.

        arr[]  = {9:00,  9:40, 9:50,  11:00, 15:00, 18:00}
        dep[]  = {9:10, 12:00, 11:20, 11:30, 19:00, 20:00}

    All events sorted by time.
    Total platforms at any time can be obtained by subtracting total 
    departures from total arrivals by that time.
     Time     Event Type     Total Platforms Needed at this Time                               
     9:00       Arrival                  1
     9:10       Departure                0
     9:40       Arrival                  1
     9:50       Arrival                  2
     11:00      Arrival                  3 
     11:20      Departure                2
     11:30      Departure                1
     12:00      Departure                0
     15:00      Arrival                  1
     18:00      Arrival                  2 
     19:00      Departure                1
     20:00      Departure                0

    Minimum Platforms needed on railway station = Maximum platforms 
                                                  needed at any time 
                                               = 3  

Following is C++ implementation of above approach. Note that the
implementation doesn’t create a single sorted list of all events, rather
it individually sorts arr[] and dep[] arrays, and then uses [merge
process of merge sort](http://geeksquiz.com/merge-sort/) to process them
together as a single sorted array.

    // Program to find minimum number of platforms required on a railway station
    #include<iostream>
    #include<algorithm>
    using namespace std;

    // Returns minimum number of platforms reqquired
    int findPlatform(int arr[], int dep[], int n)
    {
       // Sort arrival and departure arrays
       sort(arr, arr+n);
       sort(dep, dep+n);

       // plat_needed indicates number of platforms needed at a time
       int plat_needed = 1, result = 1;
       int i = 1, j = 0;

       // Similar to merge in merge sort to process all events in sorted order
       while (i < n && j < n)
       {
          // If next event in sorted order is arrival, increment count of
          // platforms needed
          if (arr[i] < dep[j])
          {
              plat_needed++;
              i++;
              if (plat_needed > result)  // Update result if needed
                  result = plat_needed;
          }
          else // Else decrement count of platforms needed
          {
              plat_needed--;
              j++;
          }
       }

       return result;
    }

    // Driver program to test methods of graph class
    int main()
    {
        int arr[] = {900, 940, 950, 1100, 1500, 1800};
        int dep[] = {910, 1200, 1120, 1130, 1900, 2000};
        int n = sizeof(arr)/sizeof(arr[0]);
        cout << "Minimum Number of Platforms Required = " 
             << findPlatform(arr, dep, n);
        return 0;
    }

Output:

    Minimum Number of Platforms Required = 3

Algorithmic Paradigm: Dynamic Programming

Time Complexity: O(nLogn), assuming that a O(nLogn) sorting algorithm
for sorting arr[] and dep[].

This article is contributed by **Shivam**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/minimum-number-platforms-required-railwaybus-station/>

Rearrange a string so that all same characters become d distance away
---------------------------------------------------------------------

Given a string and a positive integer d. Some characters may be repeated
in the given string.<span id="more-127370"></span> Rearrange characters
of the given string such that the same characters become d distance away
from each other. Note that there can be many possible rearrangements,
the output should be one of the possible rearrangements. If no such
arrangement is possible, that should also be reported.  
 Expected time complexity is O(n) where n is length of input string.

    Examples:
    Input:  "abb", d = 2
    Output: "bab"

    Input:  "aacbbc", d = 3
    Output: "abcabc"

    Input: "geeksforgeeks", d = 3
    Output: egkegkesfesor

    Input:  "aaa",  d = 2
    Output: Cannot be rearranged

***We strongly recommend to minimize the browser and try this yourself
first.***  
 ***Hint:*** Alphabet size may be assumed as constant (256) and extra
space may be used.

***Solution:*** The idea is to count frequencies of all characters and
consider the most frequent character first and place all occurrences of
it as close as possible. After the most frequent character is placed,
repeat the same process for remaining characters.

**1)** Let the given string be str and size of string be n

**2)** Traverse str, store all characters and their frequencies in a Max
Heap MH. The value of frequency decides the order in MH, i.e., the most
frequent character is at the root of MH.

**3)** Make all characters of str as ‘\\0′.

**4)** Do following while MH is not empty.  
 …**a)** Extract the Most frequent character. Let the extracted
character be x and its frequency be f.  
 …**b)** Find the first available position in str, i.e., find the first
‘\\0′ in str.  
 …**c)** Let the first position be p. Fill x at p, p+d,.. p+(f-1)d

Following is C++ implementation of above algorithm.

    // Rearrange a string so that all same characters become at least d 
    // distance away
    #include <iostream>
    #include <cstring>
    #include <cstdlib>
    #define MAX 256
    using namespace std;

    // A structure to store a character 'c' and its frequency 'f'
    // in input string
    struct charFreq {
        char c;
        int f;
    };

    // A utility function to swap two charFreq items.
    void swap(charFreq *x, charFreq *y) {
        charFreq z = *x;
        *x = *y;
        *y = z;
    }

    // A utility function to maxheapify the node freq[i] of a heap 
    // stored in freq[]
    void maxHeapify(charFreq freq[], int i, int heap_size)
    {
        int l = i*2 + 1;
        int r = i*2 + 2;
        int largest = i;
        if (l < heap_size && freq[l].f > freq[i].f)
            largest = l;
        if (r < heap_size && freq[r].f > freq[largest].f)
            largest = r;
        if (largest != i)
        {
            swap(&freq[i], &freq[largest]);
            maxHeapify(freq, largest, heap_size);
        }
    }

    // A utility function to convert the array freq[] to a max heap
    void buildHeap(charFreq freq[], int n)
    {
        int i = (n - 1)/2;
        while (i >= 0)
        {
            maxHeapify(freq, i, n);
            i--;
        }
    }

    // A utility function to remove the max item or root from max heap
    charFreq extractMax(charFreq freq[], int heap_size)
    {
        charFreq root = freq[0];
        if (heap_size > 1)
        {
            freq[0] = freq[heap_size-1];
            maxHeapify(freq, 0, heap_size-1);
        }
        return root;
    }

    // The main function that rearranges input string 'str' such that
    // two same characters become d distance away 
    void rearrange(char str[], int d)
    {
        // Find length of input string
        int n = strlen(str);

        // Create an array to store all characters and their
        // frequencies in str[]
        charFreq freq[MAX] = {{0, 0}};

        int m = 0; // To store count of distinct characters in str[]

        // Traverse the input string and store frequencies of all
        // characters in freq[] array.
        for (int i = 0; i < n; i++)
        {        
            char x = str[i];

            // If this character has occurred first time, increment m
            if (freq[x].c == 0)
                freq[x].c = x, m++;

            (freq[x].f)++;
            str[i] = '\0';  // This change is used later 
        }

        // Build a max heap of all characters
        buildHeap(freq, MAX);

        // Now one by one extract all distinct characters from max heap
        // and put them back in str[] with the d distance constraint
        for (int i = 0; i < m; i++)
        {
            charFreq x = extractMax(freq, MAX-i);

            // Find the first available position in str[]
            int p = i;
            while (str[p] != '\0')
                p++;

            // Fill x.c at p, p+d, p+2d, .. p+(f-1)d
            for (int k = 0; k < x.f; k++)
            {
                // If the index goes beyond size, then string cannot
                // be rearranged.
                if (p + d*k >= n)
                {
                    cout << "Cannot be rearranged";
                    exit(0);
                }
                str[p + d*k] = x.c;
            }
        }
    }

    // Driver program to test above functions
    int main()
    {
        char str[] = "aabbcc";
        rearrange(str, 3);
        cout << str;
    }

Output:

    abcabc

**Algorithmic Paradigm:** [Greedy
Algorithm](http://www.geeksforgeeks.org/greedy-algorithms-set-1-activity-selection-problem/)

**Time Complexity:** Time complexity of above implementation is O(n +
mLog(MAX)). Here n is the length of str, m is count of distinct
characters in str[] and MAX is maximum possible different characters.
MAX is typically 256 (a constant) and m is smaller than MAX. So the time
complexity can be considered as O(n).

**More Analysis:**  
 The above code can be optimized to store only m characters in heap, we
have kept it this way to keep the code simple. So the time complexity
can be improved to O(n + mLogm). It doesn’t much matter through as MAX
is a constant.

Also, the above algorithm can be implemented using a O(mLogm) sorting
algorithm. The first steps of above algorithm remain same. Instead of
building a heap, we can sort the freq[] array in non-increasing order of
frequencies and then consider all characters one by one from sorted
array.

We will soon be covering an extended version where same characters
should be moved at least d distance away.

This article is contributed by **Himanshu Gupta**. Please write comments
if you find anything incorrect, or you want to share more information
about the topic discussed above

   
Tags: [Greedy
Algorithm](http://www.geeksforgeeks.org/tag/greedy-algorithm/)

### Source:

<http://www.geeksforgeeks.org/rearrange-a-string-so-that-all-same-characters-become-at-least-d-distance-away/>


