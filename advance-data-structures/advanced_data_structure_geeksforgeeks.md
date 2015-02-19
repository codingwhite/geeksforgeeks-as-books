Design an efficient data structure for given operations
-------------------------------------------------------

Design a Data Structure for the following operations. The data structure
should be efficient enough to accommodate the operations according to
their frequency.<span id="more-114267"></span>

    1) findMin() : Returns the minimum item.
       Frequency: Most frequent

    2) findMax() : Returns the maximum item.
        Frequency: Most frequent

    3) deleteMin() : Delete the minimum item.
        Frequency: Moderate frequent 

    4) deleteMax() : Delete the maximum item.
        Frequency: Moderate frequent 

    5) Insert() : Inserts an item.
        Frequency: Least frequent

    6) Delete() : Deletes an item.
        Frequency: Least frequent. 

A **simple solution** is to maintain a sorted array where smallest
element is at first position and largest element is at last. The time
complexity of findMin(), findMAx() and deleteMax() is O(1). But time
complexities of deleteMin(), insert() and delete() will be O(n).

**Can we do the most frequent two operations in O(1) and other
operations in O(Logn) time?**.  
 The idea is to use two binary heaps (one max and one min heap). The
main challenge is, while deleting an item, we need to delete from both
min-heap and max-heap. So, we need some kind of mutual data structure.
In the following design, we have used doubly linked list as a mutual
data structure. The doubly linked list contains all input items and
indexes of corresponding min and max heap nodes. The nodes of min and
max heaps store addresses of nodes of doubly linked list. The root node
of min heap stores the address of minimum item in doubly linked list.
Similarly, root of max heap stores address of maximum item in doubly
linked list. Following are the details of operations.

**1) findMax():** We get the address of maximum value node from root of
Max Heap. So this is a O(1) operation.

**1) findMin():** We get the address of minimum value node from root of
Min Heap. So this is a O(1) operation.

**3) deleteMin()**: We get the address of minimum value node from root
of Min Heap. We use this address to find the node in doubly linked list.
From the doubly linked list, we get node of Max Heap. We delete node
from all three. We can delete a node from doubly linked list in O(1)
time. delete() operations for max and min heaps take O(Logn) time.

**4) deleteMax()**: is similar to deleteMin()

**5) Insert()** We always insert at the beginning of linked list in O(1)
time. Inserting the address in Max and Min Heaps take O(Logn) time. So
overall complexity is O(Logn)

**6) Delete()** We first search the item in Linked List. Once the item
is found in O(n) time, we delete it from linked list. Then using the
indexes stored in linked list, we delete it from Min Heap and Max Heaps
in O(Logn) time. *So overall complexity of this operation is O(n). The
Delete operation can be optimized to O(Logn) by using a balanced binary
search tree instead of doubly linked list as a mutual data structure.
Use of balanced binary search will not effect time complexity of other
operations as it will act as a mutual data structure like doubly Linked
List.*  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/data-structure1-1024x660.png "data structure")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/data-structure1.png)

Following is C implementation of the above data structure.

    // C program for efficient data structure
    #include <stdio.h>
    #include <stdlib.h>
    #include <limits.h>

    // A node of doubly linked list
    struct LNode
    {
        int data;
        int minHeapIndex;
        int maxHeapIndex;
        struct LNode *next, *prev;
    };

    // Structure for a doubly linked list
    struct List
    {
        struct LNode *head;
    };

    // Structure for min heap
    struct MinHeap
    {
        int size;
        int capacity;
        struct LNode* *array;
    };

    // Structure for max heap
    struct MaxHeap
    {
        int size;
        int capacity;
        struct LNode* *array;
    };

    // The required data structure
    struct MyDS
    {
        struct MinHeap* minHeap;
        struct MaxHeap* maxHeap;
        struct List* list;
    };

    // Function to swap two integers
    void swapData(int* a, int* b)
    { int t = *a;   *a = *b;   *b = t; }

    // Function to swap two List nodes
    void swapLNode(struct LNode** a, struct LNode** b)
    { struct LNode* t = *a; *a = *b; *b = t; }

    // A utility function to create a new List node
    struct LNode* newLNode(int data)
    {
        struct LNode* node =
            (struct LNode*) malloc(sizeof(struct LNode));
        node->minHeapIndex = node->maxHeapIndex = -1;
        node->data = data;
        node->prev = node->next = NULL;
        return node;
    }

    // Utility function to create a max heap of given capacity
    struct MaxHeap* createMaxHeap(int capacity)
    {
        struct MaxHeap* maxHeap =
         (struct MaxHeap*) malloc(sizeof(struct MaxHeap));
        maxHeap->size = 0;
        maxHeap->capacity = capacity;
        maxHeap->array =
         (struct LNode**) malloc(maxHeap->capacity * sizeof(struct LNode*));
        return maxHeap;
    }

    // Utility function to create a min heap of given capacity
    struct MinHeap* createMinHeap(int capacity)
    {
        struct MinHeap* minHeap =
           (struct MinHeap*) malloc(sizeof(struct MinHeap));
        minHeap->size = 0;
        minHeap->capacity = capacity;
        minHeap->array =
           (struct LNode**) malloc(minHeap->capacity * sizeof(struct LNode*));
        return minHeap;
    }

    // Utility function to create a List
    struct List* createList()
    {
        struct List* list =
          (struct List*) malloc(sizeof(struct List));
        list->head = NULL;
        return list;
    }

    // Utility function to create the main data structure
    // with given capacity
    struct MyDS* createMyDS(int capacity)
    {
        struct MyDS* myDS =
            (struct MyDS*) malloc(sizeof(struct MyDS));
        myDS->minHeap = createMinHeap(capacity);
        myDS->maxHeap = createMaxHeap(capacity);
        myDS->list = createList();
        return myDS;
    }

    // Some basic operations for heaps and List
    int isMaxHeapEmpty(struct MaxHeap* heap)
    {  return (heap->size == 0); }

    int isMinHeapEmpty(struct MinHeap* heap)
    {  return heap->size == 0; }

    int isMaxHeapFull(struct MaxHeap* heap)
    {  return heap->size == heap->capacity; }

    int isMinHeapFull(struct MinHeap* heap)
    {  return heap->size == heap->capacity; }

    int isListEmpty(struct List* list)
    {  return !list->head;   }

    int hasOnlyOneLNode(struct List* list)
    {    return !list->head->next && !list->head->prev; }


    // The standard minheapify function.  The only thing it does extra
    // is swapping indexes of heaps inside the List
    void minHeapify(struct MinHeap* minHeap, int index)
    {
        int smallest, left, right;
        smallest = index;
        left = 2 * index + 1;
        right = 2 * index + 2;

        if ( minHeap->array[left] &&
             left < minHeap->size &&
             minHeap->array[left]->data < minHeap->array[smallest]->data
           )
            smallest = left;

        if ( minHeap->array[right] &&
             right < minHeap->size &&
             minHeap->array[right]->data < minHeap->array[smallest]->data
           )
            smallest = right;

        if (smallest != index)
        {
            // First swap indexes inside the List using address
            // of List nodes
            swapData(&(minHeap->array[smallest]->minHeapIndex),
                     &(minHeap->array[index]->minHeapIndex));

            // Now swap pointers to List nodes
            swapLNode(&minHeap->array[smallest],
                      &minHeap->array[index]);

            // Fix the heap downward
            minHeapify(minHeap, smallest);
        }
    }

    // The standard maxHeapify function.  The only thing it does extra
    // is swapping indexes of heaps inside the List
    void maxHeapify(struct MaxHeap* maxHeap, int index)
    {
        int largest, left, right;
        largest = index;
        left = 2 * index + 1;
        right = 2 * index + 2;

        if ( maxHeap->array[left] &&
             left < maxHeap->size &&
             maxHeap->array[left]->data > maxHeap->array[largest]->data
           )
            largest = left;

        if ( maxHeap->array[right] &&
             right < maxHeap->size &&
             maxHeap->array[right]->data > maxHeap->array[largest]->data
           )
            largest = right;

        if (largest != index)
        {
            // First swap indexes inside the List using address
            // of List nodes
            swapData(&maxHeap->array[largest]->maxHeapIndex,
                     &maxHeap->array[index]->maxHeapIndex);

            // Now swap pointers to List nodes
            swapLNode(&maxHeap->array[largest],
                      &maxHeap->array[index]);

            // Fix the heap downward
            maxHeapify(maxHeap, largest);
        }
    }

    // Standard function to insert an item in Min Heap
    void insertMinHeap(struct MinHeap* minHeap, struct LNode* temp)
    {
        if (isMinHeapFull(minHeap))
            return;

        ++minHeap->size;
        int i = minHeap->size - 1;
        while (i && temp->data < minHeap->array[(i - 1) / 2]->data )
        {
            minHeap->array[i] = minHeap->array[(i - 1) / 2];
            minHeap->array[i]->minHeapIndex = i;
            i = (i - 1) / 2;
        }

        minHeap->array[i] = temp;
        minHeap->array[i]->minHeapIndex = i;
    }

    // Standard function to insert an item in Max Heap
    void insertMaxHeap(struct MaxHeap* maxHeap, struct LNode* temp)
    {
        if (isMaxHeapFull(maxHeap))
            return;

        ++maxHeap->size;
        int i = maxHeap->size - 1;
        while (i && temp->data > maxHeap->array[(i - 1) / 2]->data )
        {
            maxHeap->array[i] = maxHeap->array[(i - 1) / 2];
            maxHeap->array[i]->maxHeapIndex = i;
            i = (i - 1) / 2;
        }

        maxHeap->array[i] = temp;
        maxHeap->array[i]->maxHeapIndex = i;
    }


    // Function to find minimum value stored in the main data structure
    int findMin(struct MyDS* myDS)
    {
        if (isMinHeapEmpty(myDS->minHeap))
            return INT_MAX;

        return myDS->minHeap->array[0]->data;
    }

    // Function to find maximum value stored in the main data structure
    int findMax(struct MyDS* myDS)
    {
        if (isMaxHeapEmpty(myDS->maxHeap))
            return INT_MIN;

        return myDS->maxHeap->array[0]->data;
    }

    // A utility function to remove an item from linked list
    void removeLNode(struct List* list, struct LNode** temp)
    {
        if (hasOnlyOneLNode(list))
            list->head = NULL;

        else if (!(*temp)->prev) // first node
        {
            list->head = (*temp)->next;
            (*temp)->next->prev = NULL;
        }
        // any other node including last
        else
        {
            (*temp)->prev->next = (*temp)->next;
            // last node
            if ((*temp)->next)
                (*temp)->next->prev = (*temp)->prev;
        }
        free(*temp);
        *temp = NULL;
    }

    // Function to delete maximum value stored in the main data structure
    void deleteMax(struct MyDS* myDS)
    {
        MinHeap *minHeap = myDS->minHeap;
        MaxHeap *maxHeap = myDS->maxHeap;

        if (isMaxHeapEmpty(maxHeap))
            return;
        struct LNode* temp = maxHeap->array[0];

        // delete the maximum item from maxHeap
        maxHeap->array[0] =
            maxHeap->array[maxHeap->size - 1];
        --maxHeap->size;
        maxHeap->array[0]->maxHeapIndex = 0;
        maxHeapify(maxHeap, 0);

        // remove the item from minHeap
        minHeap->array[temp->minHeapIndex] = minHeap->array[minHeap->size - 1];
        --minHeap->size;
        minHeap->array[temp->minHeapIndex]->minHeapIndex = temp->minHeapIndex;
        minHeapify(minHeap, temp->minHeapIndex);

        // remove the node from List
        removeLNode(myDS->list, &temp);
    }

    // Function to delete minimum value stored in the main data structure
    void deleteMin(struct MyDS* myDS)
    {
        MinHeap *minHeap = myDS->minHeap;
        MaxHeap *maxHeap = myDS->maxHeap;

        if (isMinHeapEmpty(minHeap))
            return;
        struct LNode* temp = minHeap->array[0];

        // delete the minimum item from minHeap
        minHeap->array[0] = minHeap->array[minHeap->size - 1];
        --minHeap->size;
        minHeap->array[0]->minHeapIndex = 0;
        minHeapify(minHeap, 0);

        // remove the item from maxHeap
        maxHeap->array[temp->maxHeapIndex] = maxHeap->array[maxHeap->size - 1];
        --maxHeap->size;
        maxHeap->array[temp->maxHeapIndex]->maxHeapIndex = temp->maxHeapIndex;
        maxHeapify(maxHeap, temp->maxHeapIndex);

        // remove the node from List
        removeLNode(myDS->list, &temp);
    }

    // Function to enList an item to List
    void insertAtHead(struct List* list, struct LNode* temp)
    {
        if (isListEmpty(list))
            list->head = temp;

        else
        {
            temp->next = list->head;
            list->head->prev = temp;
            list->head = temp;
        }
    }

    // Function to delete an item from List. The function also
    // removes item from min and max heaps
    void Delete(struct MyDS* myDS, int item)
    {
        MinHeap *minHeap = myDS->minHeap;
        MaxHeap *maxHeap = myDS->maxHeap;

        if (isListEmpty(myDS->list))
            return;

        // search the node in List
        struct LNode* temp = myDS->list->head;
        while (temp && temp->data != item)
            temp = temp->next;

        // if item not found
        if (!temp || temp && temp->data != item)
            return;

        // remove item from min heap
        minHeap->array[temp->minHeapIndex] = minHeap->array[minHeap->size - 1];
        --minHeap->size;
        minHeap->array[temp->minHeapIndex]->minHeapIndex = temp->minHeapIndex;
        minHeapify(minHeap, temp->minHeapIndex);

        // remove item from max heap
        maxHeap->array[temp->maxHeapIndex] = maxHeap->array[maxHeap->size - 1];
        --maxHeap->size;
        maxHeap->array[temp->maxHeapIndex]->maxHeapIndex = temp->maxHeapIndex;
        maxHeapify(maxHeap, temp->maxHeapIndex);

        // remove node from List
        removeLNode(myDS->list, &temp);
    }

    // insert operation for main data structure
    void Insert(struct MyDS* myDS, int data)
    {
        struct LNode* temp = newLNode(data);

        // insert the item in List
        insertAtHead(myDS->list, temp);

        // insert the item in min heap
        insertMinHeap(myDS->minHeap, temp);

        // insert the item in max heap
        insertMaxHeap(myDS->maxHeap, temp);
    }

    // Driver program to test above functions
    int main()
    {
        struct MyDS *myDS = createMyDS(10);
        // Test Case #1
        /*Insert(myDS, 10);
        Insert(myDS, 2);
        Insert(myDS, 32);
        Insert(myDS, 40);
        Insert(myDS, 5);*/

        // Test Case #2
        Insert(myDS, 10);
        Insert(myDS, 20);
        Insert(myDS, 30);
        Insert(myDS, 40);
        Insert(myDS, 50);

        printf("Maximum = %d \n", findMax(myDS));
        printf("Minimum = %d \n\n", findMin(myDS));

        deleteMax(myDS);  // 50 is deleted
        printf("After deleteMax()\n");
        printf("Maximum = %d \n", findMax(myDS));
        printf("Minimum = %d \n\n", findMin(myDS));

        deleteMin(myDS); // 10 is deleted
        printf("After deleteMin()\n");
        printf("Maximum = %d \n", findMax(myDS));
        printf("Minimum = %d \n\n", findMin(myDS));

        Delete(myDS, 40); // 40 is deleted
        printf("After Delete()\n");
        printf("Maximum = %d \n", findMax(myDS));
        printf("Minimum = %d \n", findMin(myDS));

        return 0;
    }

Output:

    Maximum = 50
    Minimum = 10

    After deleteMax()
    Maximum = 40
    Minimum = 10

    After deleteMin()
    Maximum = 40
    Minimum = 20

    After Delete()
    Maximum = 30
    Minimum = 20

This article is compiled by [Aashish
Barnwal](https://www.facebook.com/barnwal.aashish?fref=ts) and reviewed
by GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/a-data-structure-question/>

AVL Tree | Set 1 (Insertion)
----------------------------

AVL tree is a self-balancing Binary Search Tree (BST) where the
difference between heights of left and right subtrees cannot be more
than one for all nodes.<span id="more-17679"></span>

**Why AVL Trees?**  
 Most of the BST operations (e.g., search, max, min, insert, delete..
etc) take O(h) time where h is the height of the BST. The cost of these
operations may become O(n) for a skewed Binary tree. If we make sure
that height of the tree remains O(Logn) after every insertion and
deletion, then we can guarantee an upper bound of O(Logn) for all these
operations. The height of an AVL tree is always O(Logn) where n is the
number of nodes in the tree (See
[this](http://www.youtube.com/watch?v=TbvhGcf6UJU)video lecture for
proof).

**Insertion**  
 To make sure that the given tree remains AVL after every insertion, we
must augment the standard BST insert operation to perform some
re-balancing. Following are two basic operations that can be performed
to re-balance a BST without violating the BST property (keys(left) 1)
Left Rotation  
 2) Right Rotation

    T1, T2 and T3 are subtrees of the tree rooted with y (on left side) 
    or x (on right side)           
                    y                               x
                   / \     Right Rotation          /  \
                  x   T3   – – – – – – – >        T1   y 
                 / \       
    Steps to follow for insertion

    Let the newly nserted node be w

    1) Perform standard BST insert for w.

    2) Starting from w, travel up and find the first unbalanced node.  Let z be the first unbalanced node, y be the child of z that comes on the path from w to z and x be the grandchild of z that comes on the path from w to z.

    3) Re-balance the tree by performing appropriate rotations on the subtree rooted with z. There can be 4 possible cases that needs to be handled as x, y and z can be arranged in 4 ways.  Following are the possible 4 arrangements:

    a) y is left child of z and x is left child of y (Left Left Case)

    b) y is left child of z and x is right child of y (Left Right Case)

    c) y is right child of z and x is right child of y (Right Right Case)

    d) y is right child of z and x is left child of y (Right Left Case)
    Following are the operations to be performed in above mentioned 4 cases. In all of the cases, we only need to re-balance the subtree rooted with z and the complete tree becomes balanced as the height of subtree (After appropriate rotations) rooted with z becomes same as it was before insertion. (See this video lecture for proof)
    a) Left Left Case

    T1, T2, T3 and T4 are subtrees.
             z                                      y 
            / \                                   /   \
           y   T4      Right Rotate (z)          x      z
          / \          - - - - - - - - ->      /  \    /  \ 
         x   T3                               T1  T2  T3  T4
        / \
      T1   T2

**b) Left Right Case**

         z                               z                           x
        / \                            /   \                        /  \ 
       y   T4  Left Rotate (y)        x    T4  Right Rotate(z)    y      z
      / \      - - - - - - - - ->    /  \      - - - - - - - ->  / \    / \
    T1   x                          y    T3                    T1  T2 T3  T4
        / \                        / \
      T2   T3                    T1   T2

**c) Right Right Case**

      z                                y
     /  \                            /   \ 
    T1   y     Left Rotate(z)       z      x
        /  \   - - - - - - - ->    / \    / \
       T2   x                     T1  T2 T3  T4
           / \
         T3  T4

**d) Right Left Case**

       z                            z                            x
      / \                          / \                          /  \ 
    T1   y   Right Rotate (y)    T1   x      Left Rotate(z)   z      y
        / \  - - - - - - - - ->     /  \   - - - - - - - ->  / \    / \
       x   T4                      T2   y                  T1  T2  T3  T4
      / \                              /  \
    T2   T3                           T3   T4

**C implementation**  
 Following is the C implementation for AVL Tree Insertion. The following
C implementation uses the recursive BST insert to insert a new node. In
the recursive BST insert, after insertion, we get pointers to all
ancestors one by one in bottom up manner. So we don’t need parent
pointer to travel up. The recursive code itself travels up and visits
all the ancestors of the newly inserted node.  
 1) Perform the normal BST insertion.  
 2) The current node must be one of the ancestors of the newly inserted
node. Update the height of the current node.  
 3) Get the balance factor (left subtree height – right subtree height)
of the current node.  
 4) If balance factor is greater than 1, then the current node is
unbalanced and we are either in Left Left case or left Right case. To
check whether it is left left case or not, compare the newly inserted
key with the key in left subtree root.  
 5) If balance factor is less than -1, then the current node is
unbalanced and we are either in Right Right case or Right Left case. To
check whether it is Right Right case or not, compare the newly inserted
key with the key in right subtree root.

    #include<stdio.h>
    #include<stdlib.h>

    // An AVL tree node
    struct node
    {
        int key;
        struct node *left;
        struct node *right;
        int height;
    };

    // A utility function to get maximum of two integers
    int max(int a, int b);

    // A utility function to get height of the tree
    int height(struct node *N)
    {
        if (N == NULL)
            return 0;
        return N->height;
    }

    // A utility function to get maximum of two integers
    int max(int a, int b)
    {
        return (a > b)? a : b;
    }

    /* Helper function that allocates a new node with the given key and
        NULL left and right pointers. */
    struct node* newNode(int key)
    {
        struct node* node = (struct node*)
                            malloc(sizeof(struct node));
        node->key   = key;
        node->left   = NULL;
        node->right  = NULL;
        node->height = 1;  // new node is initially added at leaf
        return(node);
    }

    // A utility function to right rotate subtree rooted with y
    // See the diagram given above.
    struct node *rightRotate(struct node *y)
    {
        struct node *x = y->left;
        struct node *T2 = x->right;

        // Perform rotation
        x->right = y;
        y->left = T2;

        // Update heights
        y->height = max(height(y->left), height(y->right))+1;
        x->height = max(height(x->left), height(x->right))+1;

        // Return new root
        return x;
    }

    // A utility function to left rotate subtree rooted with x
    // See the diagram given above.
    struct node *leftRotate(struct node *x)
    {
        struct node *y = x->right;
        struct node *T2 = y->left;

        // Perform rotation
        y->left = x;
        x->right = T2;

        //  Update heights
        x->height = max(height(x->left), height(x->right))+1;
        y->height = max(height(y->left), height(y->right))+1;

        // Return new root
        return y;
    }

    // Get Balance factor of node N
    int getBalance(struct node *N)
    {
        if (N == NULL)
            return 0;
        return height(N->left) - height(N->right);
    }

    struct node* insert(struct node* node, int key)
    {
        /* 1.  Perform the normal BST rotation */
        if (node == NULL)
            return(newNode(key));

        if (key < node->key)
            node->left  = insert(node->left, key);
        else
            node->right = insert(node->right, key);

        /* 2. Update height of this ancestor node */
        node->height = max(height(node->left), height(node->right)) + 1;

        /* 3. Get the balance factor of this ancestor node to check whether
           this node became unbalanced */
        int balance = getBalance(node);

        // If this node becomes unbalanced, then there are 4 cases

        // Left Left Case
        if (balance > 1 && key < node->left->key)
            return rightRotate(node);

        // Right Right Case
        if (balance < -1 && key > node->right->key)
            return leftRotate(node);

        // Left Right Case
        if (balance > 1 && key > node->left->key)
        {
            node->left =  leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Left Case
        if (balance < -1 && key < node->right->key)
        {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }

        /* return the (unchanged) node pointer */
        return node;
    }

    // A utility function to print preorder traversal of the tree.
    // The function also prints height of every node
    void preOrder(struct node *root)
    {
        if(root != NULL)
        {
            printf("%d ", root->key);
            preOrder(root->left);
            preOrder(root->right);
        }
    }

    /* Drier program to test above function*/
    int main()
    {
      struct node *root = NULL;

      /* Constructing tree given in the above figure */
      root = insert(root, 10);
      root = insert(root, 20);
      root = insert(root, 30);
      root = insert(root, 40);
      root = insert(root, 50);
      root = insert(root, 25);

      /* The constructed AVL Tree would be
                30
               /  \
             20   40
            /  \     \
           10  25    50
      */

      printf("Pre order traversal of the constructed AVL tree is \n");
      preOrder(root);

      return 0;
    }

Output:

      Pre order traversal of the constructed AVL tree is
      30 20 10 25 40 50

Time Complexity: The rotation operations (left and right rotate) take
constant time as only few pointers are being changed there. Updating the
height and getting the balance factor also take constant time. So the
time complexity of AVL insert remains same as BST insert which is O(h)
where h is height of the tree. Since AVL tree is balanced, the height is
O(Logn). So time complexity of AVL insert is O(Logn).

The AVL tree and other self balancing search trees like Red Black are
useful to get all basic operations done in O(Logn) time. The AVL trees
are more balanced compared to Red Black Trees, but they may cause more
rotations during insertion and deletion. So if your application involves
many frequent insertions and deletions, then Red Black trees should be
preferred. And if the insertions and deletions are less frequent and
search is more frequent operation, then AVL tree should be preferred
over Red Black Tree.

Following are some previous posts that have used self-balancing search
trees.

[Median in a stream of integers (running
integers)](http://www.geeksforgeeks.org/archives/14873)  
 [Maximum of all subarrays of size
k](http://www.geeksforgeeks.org/archives/11306)  
 [Count smaller elements on right
side](http://www.geeksforgeeks.org/archives/17235)

**References:**  
 [IITD Video Lecture on AVL Tree
Introduction](http://www.youtube.com/watch?v=mRGQylRWAsI&feature=relmfu)  
 [IITD Video Lecture on AVL Tree Insertion and
Deletion](http://www.youtube.com/watch?v=TbvhGcf6UJU)

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/)

### Source:

<http://www.geeksforgeeks.org/avl-tree-set-1-insertion/>

AVL Tree | Set 2 (Deletion)
---------------------------

We have discussed AVL insertion in the [previous
post](http://www.geeksforgeeks.org/archives/17679). In this post, we
will follow a similar approach for deletion.<span
id="more-18009"></span>

**Steps to follow for deletion**.  
 To make sure that the given tree remains AVL after every deletion, we
must augment the standard BST delete operation to perform some
re-balancing. Following are two basic operations that can be performed
to re-balance a BST without violating the BST property (keys(left) 1)
Left Rotation  
 2) Right Rotation

    T1, T2 and T3 are subtrees of the tree rooted with y (on left side)
    or x (on right side)
                    y                               x
                   / \     Right Rotation          /  \
                  x   T3   â – â – â – â >        T1   y
                 / \       
    Let w be the node to be deleted

    1) Perform standard BST delete for w.

    2) Starting from w, travel up and find the first unbalanced node. Let z be the first unbalanced node, y be the larger height child of z, and x be the larger height child of y.  Note that the definitions of x and y are different from insertion here.

    3) Re-balance the tree by performing appropriate rotations on the subtree rooted with z. There can be 4 possible cases that needs to be handled as x, y and z can be arranged in 4 ways. Following are the possible 4 arrangements:

    a) y is left child of z and x is left child of y (Left Left Case)

    b) y is left child of z and x is right child of y (Left Right Case)

    c) y is right child of z and x is right child of y (Right Right Case)

    d) y is right child of z and x is left child of y (Right Left Case)
    Like insertion, following are the operations to be performed in above mentioned 4 cases. Note that, unlike insertion, fixing the node z won’t fix the complete AVL tree. After fixing z, we may have to fix ancestors of z as well (See this video lecture for proof)
    a) Left Left Case

    T1, T2, T3 and T4 are subtrees.
             z                                      y 
            / \                                   /   \
           y   T4      Right Rotate (z)          x      z
          / \          - - - - - - - - ->      /  \    /  \ 
         x   T3                               T1  T2  T3  T4
        / \
      T1   T2

**b) Left Right Case**

         z                               z                           x
        / \                            /   \                        /  \ 
       y   T4  Left Rotate (y)        x    T4  Right Rotate(z)    y      z
      / \      - - - - - - - - ->    /  \      - - - - - - - ->  / \    / \
    T1   x                          y    T3                    T1  T2 T3  T4
        / \                        / \
      T2   T3                    T1   T2

**c) Right Right Case**

      z                                y
     /  \                            /   \ 
    T1   y     Left Rotate(z)       z      x
        /  \   - - - - - - - ->    / \    / \
       T2   x                     T1  T2 T3  T4
           / \
         T3  T4

**d) Right Left Case**

       z                            z                            x
      / \                          / \                          /  \ 
    T1   y   Right Rotate (y)    T1   x      Left Rotate(z)   z      x
        / \  - - - - - - - - ->     /  \   - - - - - - - ->  / \    / \
       x   T4                      T2   y                  T1  T2  T3  T4
      / \                              /  \
    T2   T3                           T3   T4

Unlike insertion, in deletion, after we perform a rotation at z, we may
have to perform a rotation at ancestors of z. Thus, we must continue to
trace the path until we reach the root.

**C implementation**  
 Following is the C implementation for AVL Tree Deletion. The following
C implementation uses the recursive BST delete as basis. In the
recursive BST delete, after deletion, we get pointers to all ancestors
one by one in bottom up manner. So we don’t need parent pointer to
travel up. The recursive code itself travels up and visits all the
ancestors of the deleted node.  
 **1)** Perform the normal BST deletion.  
 **2)** The current node must be one of the ancestors of the deleted
node. Update the height of the current node.  
 **3)** Get the balance factor (left subtree height – right subtree
height) of the current node.  
 **4)** If balance factor is greater than 1, then the current node is
unbalanced and we are either in Left Left case or Left Right case. To
check whether it is Left Left case or Left Right case, get the balance
factor of left subtree. If balance factor of the left subtree is greater
than or equal to 0, then it is Left Left case, else Left Right case.  
 **5)** If balance factor is less than -1, then the current node is
unbalanced and we are either in Right Right case or Right Left case. To
check whether it is Right Right case or Right Left case, get the balance
factor of right subtree. If the balance factor of the right subtree is
smaller than or equal to 0, then it is Right Right case, else Right Left
case.

    #include<stdio.h>
    #include<stdlib.h>

    // An AVL tree node
    struct node
    {
        int key;
        struct node *left;
        struct node *right;
        int height;
    };

    // A utility function to get maximum of two integers
    int max(int a, int b);

    // A utility function to get height of the tree
    int height(struct node *N)
    {
        if (N == NULL)
            return 0;
        return N->height;
    }

    // A utility function to get maximum of two integers
    int max(int a, int b)
    {
        return (a > b)? a : b;
    }

    /* Helper function that allocates a new node with the given key and
        NULL left and right pointers. */
    struct node* newNode(int key)
    {
        struct node* node = (struct node*)
                            malloc(sizeof(struct node));
        node->key   = key;
        node->left   = NULL;
        node->right  = NULL;
        node->height = 1;  // new node is initially added at leaf
        return(node);
    }

    // A utility function to right rotate subtree rooted with y
    // See the diagram given above.
    struct node *rightRotate(struct node *y)
    {
        struct node *x = y->left;
        struct node *T2 = x->right;

        // Perform rotation
        x->right = y;
        y->left = T2;

        // Update heights
        y->height = max(height(y->left), height(y->right))+1;
        x->height = max(height(x->left), height(x->right))+1;

        // Return new root
        return x;
    }

    // A utility function to left rotate subtree rooted with x
    // See the diagram given above.
    struct node *leftRotate(struct node *x)
    {
        struct node *y = x->right;
        struct node *T2 = y->left;

        // Perform rotation
        y->left = x;
        x->right = T2;

        //  Update heights
        x->height = max(height(x->left), height(x->right))+1;
        y->height = max(height(y->left), height(y->right))+1;

        // Return new root
        return y;
    }

    // Get Balance factor of node N
    int getBalance(struct node *N)
    {
        if (N == NULL)
            return 0;
        return height(N->left) - height(N->right);
    }

    struct node* insert(struct node* node, int key)
    {
        /* 1.  Perform the normal BST rotation */
        if (node == NULL)
            return(newNode(key));

        if (key < node->key)
            node->left  = insert(node->left, key);
        else
            node->right = insert(node->right, key);

        /* 2. Update height of this ancestor node */
        node->height = max(height(node->left), height(node->right)) + 1;

        /* 3. Get the balance factor of this ancestor node to check whether
           this node became unbalanced */
        int balance = getBalance(node);

        // If this node becomes unbalanced, then there are 4 cases

        // Left Left Case
        if (balance > 1 && key < node->left->key)
            return rightRotate(node);

        // Right Right Case
        if (balance < -1 && key > node->right->key)
            return leftRotate(node);

        // Left Right Case
        if (balance > 1 && key > node->left->key)
        {
            node->left =  leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Left Case
        if (balance < -1 && key < node->right->key)
        {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }

        /* return the (unchanged) node pointer */
        return node;
    }

    /* Given a non-empty binary search tree, return the node with minimum
       key value found in that tree. Note that the entire tree does not
       need to be searched. */
    struct node * minValueNode(struct node* node)
    {
        struct node* current = node;

        /* loop down to find the leftmost leaf */
        while (current->left != NULL)
            current = current->left;

        return current;
    }

    struct node* deleteNode(struct node* root, int key)
    {
        // STEP 1: PERFORM STANDARD BST DELETE

        if (root == NULL)
            return root;

        // If the key to be deleted is smaller than the root's key,
        // then it lies in left subtree
        if ( key < root->key )
            root->left = deleteNode(root->left, key);

        // If the key to be deleted is greater than the root's key,
        // then it lies in right subtree
        else if( key > root->key )
            root->right = deleteNode(root->right, key);

        // if key is same as root's key, then This is the node
        // to be deleted
        else
        {
            // node with only one child or no child
            if( (root->left == NULL) || (root->right == NULL) )
            {
                struct node *temp = root->left ? root->left : root->right;

                // No child case
                if(temp == NULL)
                {
                    temp = root;
                    root = NULL;
                }
                else // One child case
                 *root = *temp; // Copy the contents of the non-empty child

                free(temp);
            }
            else
            {
                // node with two children: Get the inorder successor (smallest
                // in the right subtree)
                struct node* temp = minValueNode(root->right);

                // Copy the inorder successor's data to this node
                root->key = temp->key;

                // Delete the inorder successor
                root->right = deleteNode(root->right, temp->key);
            }
        }

        // If the tree had only one node then return
        if (root == NULL)
          return root;

        // STEP 2: UPDATE HEIGHT OF THE CURRENT NODE
        root->height = max(height(root->left), height(root->right)) + 1;

        // STEP 3: GET THE BALANCE FACTOR OF THIS NODE (to check whether
        //  this node became unbalanced)
        int balance = getBalance(root);

        // If this node becomes unbalanced, then there are 4 cases

        // Left Left Case
        if (balance > 1 && getBalance(root->left) >= 0)
            return rightRotate(root);

        // Left Right Case
        if (balance > 1 && getBalance(root->left) < 0)
        {
            root->left =  leftRotate(root->left);
            return rightRotate(root);
        }

        // Right Right Case
        if (balance < -1 && getBalance(root->right) <= 0)
            return leftRotate(root);

        // Right Left Case
        if (balance < -1 && getBalance(root->right) > 0)
        {
            root->right = rightRotate(root->right);
            return leftRotate(root);
        }

        return root;
    }

    // A utility function to print preorder traversal of the tree.
    // The function also prints height of every node
    void preOrder(struct node *root)
    {
        if(root != NULL)
        {
            printf("%d ", root->key);
            preOrder(root->left);
            preOrder(root->right);
        }
    }

    /* Drier program to test above function*/
    int main()
    {
      struct node *root = NULL;

      /* Constructing tree given in the above figure */
        root = insert(root, 9);
        root = insert(root, 5);
        root = insert(root, 10);
        root = insert(root, 0);
        root = insert(root, 6);
        root = insert(root, 11);
        root = insert(root, -1);
        root = insert(root, 1);
        root = insert(root, 2);

        /* The constructed AVL Tree would be
                9
               /  \
              1    10
            /  \     \
           0    5     11
          /    /  \
         -1   2    6
        */

        printf("Pre order traversal of the constructed AVL tree is \n");
        preOrder(root);

        root = deleteNode(root, 10);

        /* The AVL Tree after deletion of 10
                1
               /  \
              0    9
            /     /  \
           -1    5     11
               /  \
              2    6
        */

        printf("\nPre order traversal after deletion of 10 \n");
        preOrder(root);

        return 0;
    }

Output:

    Pre order traversal of the constructed AVL tree is
    9 1 0 -1 5 2 6 10 11
    Pre order traversal after deletion of 10
    1 0 -1 9 5 2 6 11

Time Complexity: The rotation operations (left and right rotate) take
constant time as only few pointers are being changed there. Updating the
height and getting the balance factor also take constant time. So the
time complexity of AVL delete remains same as BST delete which is O(h)
where h is height of the tree. Since AVL tree is balanced, the height is
O(Logn). So time complexity of AVL delete is O(Logn).

**References:**  
 [IITD Video Lecture on AVL Tree Insertion and
Deletion](http://www.youtube.com/watch?v=TbvhGcf6UJU)

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/)

### Source:

<http://www.geeksforgeeks.org/avl-tree-set-2-deletion/>

B-Tree | Set 2 (Insert)
-----------------------

In the [previous
post](http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/), we
introduced B-Tree. We also discussed search() and traverse() functions.
<span id="more-116247"></span>  
 In this post, insert() operation is discussed. A new key is always
inserted at leaf node. Let the key to be inserted be k. Like BST, we
start from root and traverse down till we reach a leaf node. Once we
reach a leaf node, we insert the key in that leaf node. Unlike BSTs, we
have a predefined range on number of keys that a node can contain. So
before inserting a key to node, we make sure that the node has extra
space.  
 *How to make sure that a node has space available for key before the
key is inserted?* We use an operation called splitChild() that is used
to split a child of a node. See the following diagram to understand
split. In the following diagram, child y of x is being split into two
nodes y and z. Note that the splitChild operation moves a key up and
this is the reason B-Trees grow up unlike BSTs which grow down.

[![BTreeSplit](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeSplit-1024x321.jpg)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeSplit.jpg)

As discussed above, to insert a new key, we go down from root to leaf.
Before traversing down to a node, we first check if the node is full. If
the node is full, we split it to create space. Following is complete
algorithm.

**Insertion**  
 **1)** Initialize x as root.  
 **2)** While x is not leaf, do following  
 ..**a)** Find the child of x that is going to to be traversed next. Let
the child be y.  
 ..**b)** If y is not full, change x to point to y.  
 ..**c)** If y is full, split it and change x to point to one of the two
parts of y. If k is smaller than mid key in y, then set x as first part
of y. Else second part of y. When we split y, we move a key from y to
its parent x.  
 **3)** The loop in step 2 stops when x is leaf. x must have space for 1
extra key as we have been splitting all nodes in advance. So simply
insert k to x.

Note that the algorithm follows the Cormen book. It is actually a
proactive insertion algorithm where before going down to a node, we
split it if it is full. The advantage of splitting before is, we never
traverse a node twice. If we don’t split a node before going down to it
and split it only if new key is inserted (reactive), we may end up
traversing all nodes again from leaf to root. This happens in cases when
all nodes on the path from root to leaf are full. So when we come to the
leaf node, we split it and move a key up. Moving a key up will cause a
split in parent node (because parent was already full). This cascading
effect never happens in this proactive insertion algorithm. There is a
disadvantage of this proactive insertion though, we may do unnecessary
splits.

Let us understand the algorithm with an example tree of minimum degree
‘t’ as 3 and a sequence of integers 10, 20, 30, 40, 50, 60, 70, 80 and
90 in an initially empty B-Tree.

Initially root is NULL. Let us first insert 10.  

[![Btree1](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Btree1.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Btree1.png)

Let us now insert 20, 30, 40 and 50. They all will be inserted in root
because maximum number of keys a node can accommodate is 2\*t – 1 which
is 5.

[![BTree2Ins](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTree2Ins.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTree2Ins.png)

Let us now insert 60. Since root node is full, it will first split into
two, then 60 will be inserted into the appropriate child.  

[![BTreeIns3](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIns3.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIns3.png)

Let us now insert 70 and 80. These new keys will be inserted into the
appropriate leaf without any split.  

[![BTreeIns4](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIns4.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIns4.png)

Let us now insert 90. This insertion will cause a split. The middle key
will go up to the parent.  

[![BTreeIns6](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIns6.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIns6.png)

See [this](http://integrator-crimea.com/ddu0110.html)for more examples.

Following is C++ implementation of the above proactive algorithm.

    // C++ program for B-Tree insertion
    #include<iostream>
    using namespace std;

    // A BTree node
    class BTreeNode
    {
        int *keys;  // An array of keys
        int t;      // Minimum degree (defines the range for number of keys)
        BTreeNode **C; // An array of child pointers
        int n;     // Current number of keys
        bool leaf; // Is true when node is leaf. Otherwise false
    public:
        BTreeNode(int _t, bool _leaf);   // Constructor

        // A utility function to insert a new key in the subtree rooted with
        // this node. The assumption is, the node must be non-full when this
        // function is called
        void insertNonFull(int k);

        // A utility function to split the child y of this node. i is index of y in
        // child array C[].  The Child y must be full when this function is called
        void splitChild(int i, BTreeNode *y);

        // A function to traverse all nodes in a subtree rooted with this node
        void traverse();

        // A function to search a key in subtree rooted with this node.
        BTreeNode *search(int k);   // returns NULL if k is not present.

    // Make BTree friend of this so that we can access private members of this
    // class in BTree functions
    friend class BTree;
    };

    // A BTree
    class BTree
    {
        BTreeNode *root; // Pointer to root node
        int t;  // Minimum degree
    public:
        // Constructor (Initializes tree as empty)
        BTree(int _t)
        {  root = NULL;  t = _t; }

        // function to traverse the tree
        void traverse()
        {  if (root != NULL) root->traverse(); }

        // function to search a key in this tree
        BTreeNode* search(int k)
        {  return (root == NULL)? NULL : root->search(k); }

        // The main function that inserts a new key in this B-Tree
        void insert(int k);
    };

    // Constructor for BTreeNode class
    BTreeNode::BTreeNode(int t1, bool leaf1)
    {
        // Copy the given minimum degree and leaf property
        t = t1;
        leaf = leaf1;

        // Allocate memory for maximum number of possible keys
        // and child pointers
        keys = new int[2*t-1];
        C = new BTreeNode *[2*t];

        // Initialize the number of keys as 0
        n = 0;
    }

    // Function to traverse all nodes in a subtree rooted with this node
    void BTreeNode::traverse()
    {
        // There are n keys and n+1 children, travers through n keys
        // and first n children
        int i;
        for (i = 0; i < n; i++)
        {
            // If this is not leaf, then before printing key[i],
            // traverse the subtree rooted with child C[i].
            if (leaf == false)
                C[i]->traverse();
            cout << " " << keys[i];
        }

        // Print the subtree rooted with last child
        if (leaf == false)
            C[i]->traverse();
    }

    // Function to search key k in subtree rooted with this node
    BTreeNode *BTreeNode::search(int k)
    {
        // Find the first key greater than or equal to k
        int i = 0;
        while (i < n && k > keys[i])
            i++;

        // If the found key is equal to k, return this node
        if (keys[i] == k)
            return this;

        // If key is not found here and this is a leaf node
        if (leaf == true)
            return NULL;

        // Go to the appropriate child
        return C[i]->search(k);
    }

    // The main function that inserts a new key in this B-Tree
    void BTree::insert(int k)
    {
        // If tree is empty
        if (root == NULL)
        {
            // Allocate memory for root
            root = new BTreeNode(t, true);
            root->keys[0] = k;  // Insert key
            root->n = 1;  // Update number of keys in root
        }
        else // If tree is not empty
        {
            // If root is full, then tree grows in height
            if (root->n == 2*t-1)
            {
                // Allocate memory for new root
                BTreeNode *s = new BTreeNode(t, false);

                // Make old root as child of new root
                s->C[0] = root;

                // Split the old root and move 1 key to the new root
                s->splitChild(0, root);

                // New root has two children now.  Decide which of the
                // two children is going to have new key
                int i = 0;
                if (s->keys[0] < k)
                    i++;
                s->C[i]->insertNonFull(k);

                // Change root
                root = s;
            }
            else  // If root is not full, call insertNonFull for root
                root->insertNonFull(k);
        }
    }

    // A utility function to insert a new key in this node
    // The assumption is, the node must be non-full when this
    // function is called
    void BTreeNode::insertNonFull(int k)
    {
        // Initialize index as index of rightmost element
        int i = n-1;

        // If this is a leaf node
        if (leaf == true)
        {
            // The following loop does two things
            // a) Finds the location of new key to be inserted
            // b) Moves all greater keys to one place ahead
            while (i >= 0 && keys[i] > k)
            {
                keys[i+1] = keys[i];
                i--;
            }

            // Insert the new key at found location
            keys[i+1] = k;
            n = n+1;
        }
        else // If this node is not leaf
        {
            // Find the child which is going to have the new key
            while (i >= 0 && keys[i] > k)
                i--;

            // See if the found child is full
            if (C[i+1]->n == 2*t-1)
            {
                // If the child is full, then split it
                splitChild(i+1, C[i+1]);

                // After split, the middle key of C[i] goes up and
                // C[i] is splitted into two.  See which of the two
                // is going to have the new key
                if (keys[i+1] < k)
                    i++;
            }
            C[i+1]->insertNonFull(k);
        }
    }

    // A utility function to split the child y of this node
    // Note that y must be full when this function is called
    void BTreeNode::splitChild(int i, BTreeNode *y)
    {
        // Create a new node which is going to store (t-1) keys
        // of y
        BTreeNode *z = new BTreeNode(y->t, y->leaf);
        z->n = t - 1;

        // Copy the last (t-1) keys of y to z
        for (int j = 0; j < t-1; j++)
            z->keys[j] = y->keys[j+t];

        // Copy the last t children of y to z
        if (y->leaf == false)
        {
            for (int j = 0; j < t; j++)
                z->C[j] = y->C[j+t];
        }

        // Reduce the number of keys in y
        y->n = t - 1;

        // Since this node is going to have a new child,
        // create space of new child
        for (int j = n; j >= i+1; j--)
            C[j+1] = C[j];

        // Link the new child to this node
        C[i+1] = z;

        // A key of y will move to this node. Find location of
        // new key and move all greater keys one space ahead
        for (int j = n-1; j >= i; j--)
            keys[j+1] = keys[j];

        // Copy the middle key of y to this node
        keys[i] = y->keys[t-1];

        // Increment count of keys in this node
        n = n + 1;
    }

    // Driver program to test above functions
    int main()
    {
        BTree t(3); // A B-Tree with minium degree 3
        t.insert(10);
        t.insert(20);
        t.insert(5);
        t.insert(6);
        t.insert(12);
        t.insert(30);
        t.insert(7);
        t.insert(17);

        cout << "Traversal of the constucted tree is ";
        t.traverse();

        int k = 6;
        (t.search(k) != NULL)? cout << "\nPresent" : cout << "\nNot Present";

        k = 15;
        (t.search(k) != NULL)? cout << "\nPresent" : cout << "\nNot Present";

        return 0;
    }

Output:

    Traversal of the constucted tree is  5 6 7 10 12 17 20 30
    Present
    Not Present

**References:**  
 [Introduction to Algorithms 3rd Edition by Clifford Stein, Thomas H.
Cormen, Charles E. Leiserson, Ronald L.
Rivest](http://www.flipkart.com/introduction-algorithms-3rd/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)  
 <http://www.cs.utexas.edu/users/djimenez/utsa/cs3343/lecture17.html>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/b-tree-set-1-insert-2/>

B-Tree | Set 1 (Introduction)
-----------------------------

B-Tree is a self-balancing search tree. In most of the other
self-balancing search trees (like
[AVL](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/) and Red
Black Trees), it is assumed that everything is in main memory. To
understand use of B-Trees, we must think of huge amount of data that
cannot fit in main memory.<span id="more-117057"></span> When the number
of keys is high, the data is read from disk in the form of blocks. Disk
access time is very high compared to main memory access time. The main
idea of using B-Trees is to reduce the number of disk accesses. Most of
the tree operations (search, insert, delete, max, min, ..etc ) require
O(h) disk accesses where h is height of the tree. B-tree is a fat tree.
Height of B-Trees is kept low by putting maximum possible keys in a
B-Tree node. Generally, a B-Tree node size is kept equal to the disk
block size. Since h is low for B-Tree, total disk accesses for most of
the operations are reduced significantly compared to balanced Binary
Search Trees like AVL Tree, Red Black Tree, ..etc.

**Properties of B-Tree**  
 **1)** All leaves are at same level.  
 **2)** A B-Tree is defined by the term *minimum degree* ‘t’. The value
of t depends upon disk block size.  
 **3)** Every node except root must contain at least t-1 keys. Root may
contain minimum 1 key.  
 **4)** All nodes (including root) may contain at most 2t â€“ 1 keys.  
 **5)** Number of children of a node is equal to the number of keys in
it plus 1.  
 **6)** All keys of a node are sorted in increasing order. The child
between two keys k1 and k2 contains all keys in range from k1 and k2.  
 **7)** B-Tree grows and shrinks from root which is unlike Binary Search
Tree. Binary Search Trees grow downward and also shrink from downward.  
 **8)** Like other balanced Binary Search Trees, time complexity to
search, insert and delete is O(Logn).

Following is an example B-Tree of minimum degree 3. Note that in
practical B-Trees, the value of minimum degree is much more than 3.  

[![BTreeIntro](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIntro1.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeIntro1.png)

**Search**  
 Search is similar to search in Binary Search Tree. Let the key to be
searched be k. We start from root and recursively traverse down. For
every visited non-leaf node, if the node has key, we simply return the
node. Otherwise we recur down to the appropriate child (The child which
is just before the first greater key) of the node. If we reach a leaf
node and don’t find k in the leaf node, we return NULL.

**Traverse**  
 Traversal is also similar to Inorder traversal of Binary Tree. We start
from the leftmost child, recursively print the leftmost child, then
repeat the same process for remaining children and keys. In the end,
recursively print the rightmost child.

    // C++ implemntation of search() and traverse() methods
    #include<iostream>
    using namespace std;

    // A BTree node
    class BTreeNode
    {
        int *keys;  // An array of keys
        int t;      // Minimum degree (defines the range for number of keys)
        BTreeNode **C; // An array of child pointers
        int n;     // Current number of keys
        bool leaf; // Is true when node is leaf. Otherwise false
    public:
        BTreeNode(int _t, bool _leaf);   // Constructor

        // A function to traverse all nodes in a subtree rooted with this node
        void traverse();

        // A function to search a key in subtree rooted with this node.
        BTreeNode *search(int k);   // returns NULL if k is not present.

    // Make BTree friend of this so that we can access private members of this
    // class in BTree functions
    friend class BTree;
    };

    // A BTree
    class BTree
    {
        BTreeNode *root; // Pointer to root node
        int t;  // Minimum degree
    public:
        // Constructor (Initializes tree as empty)
        BTree(int _t)
        {  root = NULL;  t = _t; }

        // function to traverse the tree
        void traverse()
        {  if (root != NULL) root->traverse(); }

        // function to search a key in this tree
        BTreeNode* search(int k)
        {  return (root == NULL)? NULL : root->search(k); }
    };

    // Constructor for BTreeNode class
    BTreeNode::BTreeNode(int _t, bool _leaf)
    {
        // Copy the given minimum degree and leaf property
        t = _t;
        leaf = _leaf;

        // Allocate memory for maximum number of possible keys
        // and child pointers
        keys = new int[2*t-1];
        C = new BTreeNode *[2*t];

        // Initialize the number of keys as 0
        n = 0;
    }

    // Function to traverse all nodes in a subtree rooted with this node
    void BTreeNode::traverse()
    {
        // There are n keys and n+1 children, travers through n keys
        // and first n children
        int i;
        for (i = 0; i < n; i++)
        {
            // If this is not leaf, then before printing key[i],
            // traverse the subtree rooted with child C[i].
            if (leaf == false)
                C[i]->traverse();
            cout << " " << keys[i];
        }

        // Print the subtree rooted with last child
        if (leaf == false)
            C[i]->traverse();
    }

    // Function to search key k in subtree rooted with this node
    BTreeNode *BTreeNode::search(int k)
    {
        // Find the first key greater than or equal to k
        int i = 0;
        while (i < n && k > keys[i])
            i++;

        // If the found key is equal to k, return this node
        if (keys[i] == k)
            return this;

        // If key is not found here and this is a leaf node
        if (leaf == true)
            return NULL;

        // Go to the appropriate child
        return C[i]->search(k);
    }

The above code doesn’t contain driver program. We will be covering the
complete program in our next post on B-Tree Insertion.

There are two conventions to define a B-Tree, one is to define by
minimum degree (followed in [Cormen
book](http://www.flipkart.com/introduction-algorithms-3rd/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)),
second is define by order. We have followed the minimum degree
convention and will be following same in coming posts on B-Tree. The
variable names used in the above program are also kept same as Cormen
book for better readability.

**Insertion and Deletion**  
 [B-Trer
Insertion](http://www.geeksforgeeks.org/b-tree-set-1-insert-2/)  
 [B-Tree Deletion](http://www.geeksforgeeks.org/b-tree-set-3delete/)

**References:**  
 [Introduction to Algorithms 3rd Edition by Clifford Stein, Thomas H.
Cormen, Charles E. Leiserson, Ronald L.
Rivest](http://www.flipkart.com/introduction-algorithms-3rd/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/>

B-Tree | Set 3 (Delete)
-----------------------

It is recommended to refer following posts as prerequisite of this post.

[B-Tree | Set 1
(Introduction)](http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/)  
 [B-Tree | Set 2
(Insert)](http://www.geeksforgeeks.org/b-tree-set-1-insert-2/)<span
id="more-120244"></span>

B-Tree is a type of a multi-way search tree. So, if you are not familiar
with multi-way search trees in general, it is better to take a look at
[this video lecture from
IIT-Delhi](http://www.youtube.com/watch?v=JZhdUb5F7oY), before
proceeding further. Once you get the basics of a multi-way search tree
clear, B-Tree operations will be easier to understand.

Source of the following explanation and algorithm is [Introduction to
Algorithms 3rd Edition by Clifford Stein, Thomas H. Cormen, Charles E.
Leiserson, Ronald L.
Rivest](http://www.flipkart.com/introduction-algorithms-3/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)

**Deletion process:**  
 Deletion from a B-tree is more complicated than insertion, because we
can delete a key from any node-not just a leafâ€”and when we delete a
key from an internal node, we will have to rearrange the nodeâ€™s
children.

    As in insertion, we must make sure the deletion doesn’t violate the
[B-tree
properties](http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/).
Just as we had to ensure that a node didn’t get too big due to
insertion, we must ensure that a node doesn’t get too small during
deletion (except that the root is allowed to have fewer than the minimum
number t-1 of keys). Just as a simple insertion algorithm might have to
back up if a node on the path to where the key was to be inserted was
full, a simple approach to deletion might have to back up if a node
(other than the root) along the path to where the key is to be deleted
has the minimum number of keys.

    The deletion procedure deletes the key k from the subtree rooted at
x. This procedure guarantees that whenever it calls itself recursively
on a node x, the number of keys in x is at least the minimum degree t .
Note that this condition requires one more key than the minimum required
by the usual B-tree conditions, so that sometimes a key may have to be
moved into a child node before recursion descends to that child. This
strengthened condition allows us to delete a key from the tree in one
downward pass without having to “back up” (with one exception, which
weâ€™ll explain). You should interpret the following specification for
deletion from a B-tree with the understanding that if the root node x
ever becomes an internal node having no keys (this situation can occur
in cases 2c and 3b then we delete x, and xâ€™s only child x.c1 becomes
the new root of the tree, decreasing the height of the tree by one and
preserving the property that the root of the tree contains at least one
key (unless the tree is empty).

We sketch how deletion works with various cases of deleting keys from a
B-tree.

**1.** If the key k is in node x and x is a leaf, delete the key k from
x.

**2.** If the key k is in node x and x is an internal node, do the
following.

    **a)** If the child y that precedes k in node x has at least t keys,
then find the predecessor k0 of k in the sub-tree rooted at y.
Recursively delete k0, and replace k by k0 in x. (We can find k0 and
delete it in a single downward pass.)

    **b)** If y has fewer than t keys, then, symmetrically, examine the
child z that follows k in node x. If z has at least t keys, then find
the successor k0 of k in the subtree rooted at z. Recursively delete k0,
and replace k by k0 in x. (We can find k0 and delete it in a single
downward pass.)

     **c)** Otherwise, if both y and z have only t-1 keys, merge k and
all of z into y, so that x loses both k and the pointer to z, and y now
contains 2t-1 keys. Then free z and recursively delete k from y.

**3.** If the key k is not present in internal node x, determine the
root x.c(i) of the appropriate subtree that must contain k, if k is in
the tree at all. If x.c(i) has only t-1 keys, execute step 3a or 3b as
necessary to guarantee that we descend to a node containing at least t
keys. Then finish by recursing on the appropriate child of x.

    **a)** If x.c(i) has only t-1 keys but has an immediate sibling with
at least t keys, give x.c(i) an extra key by moving a key from x down
into x.c(i), moving a key from x.c(i) â€™s immediate left or right
sibling up into x, and moving the appropriate child pointer from the
sibling into x.c(i).

    **b)** If x.c(i) and both of x.c(i)’s immediate siblings have t-1
keys, merge x.c(i) with one sibling, which involves moving a key from x
down into the new merged node to become the median key for that node.

Since most of the keys in a B-tree are in the leaves, deletion
operations are most often used to delete keys from leaves. The recursive
delete procedure then acts in one downward pass through the tree,
without having to back up. When deleting a key in an internal node,
however, the procedure makes a downward pass through the tree but may
have to return to the node from which the key was deleted to replace the
key with its predecessor or successor (cases 2a and 2b).

The following figures from [CLRS
book](http://www.flipkart.com/introduction-algorithms-3/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)
explain the deletion porcess.  

[![BTreeDelet1](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeDelet1.jpg)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeDelet1.jpg)  

[![BTreeDelet2](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeDelet2.jpg)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BTreeDelet2.jpg)

**Implementation:**  
 Following is C++ implementation of deletion process.

    /* The following program performs deletion on a B-Tree. It contains functions
       specific for deletion along with all the other functions provided in the
       previous articles on B-Trees. See http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
       for previous article.

       The deletion function has been compartmentalized into 8 functions for ease
       of understanding and clarity

       The following functions are exclusive for deletion
       In class BTreeNode:
        1) remove
        2) removeFromLeaf
        3) removeFromNonLeaf
        4) getPred
        5) getSucc
        6) borrowFromPrev
        7) borrowFromNext
        8) merge
        9) findKey

       In class BTree:
         1) remove

      The removal of a key from a B-Tree is a fairly complicated process. The program handles
      all the 6 different cases that might arise while removing a key.

      Testing: The code has been tested using the B-Tree provided in the CLRS book( included
      in the main function ) along with other cases.

      Reference: CLRS3 - Chapter 18 - (499-502)
      It is advised to read the material in CLRS before taking a look at the code. */

    #include<iostream>
    using namespace std;

    // A BTree node
    class BTreeNode
    {
        int *keys;  // An array of keys
        int t;      // Minimum degree (defines the range for number of keys)
        BTreeNode **C; // An array of child pointers
        int n;     // Current number of keys
        bool leaf; // Is true when node is leaf. Otherwise false

    public:

        BTreeNode(int _t, bool _leaf);   // Constructor

        // A function to traverse all nodes in a subtree rooted with this node
        void traverse();

        // A function to search a key in subtree rooted with this node.
        BTreeNode *search(int k);   // returns NULL if k is not present.

        // A function that returns the index of the first key that is greater
        // or equal to k
        int findKey(int k);

        // A utility function to insert a new key in the subtree rooted with
        // this node. The assumption is, the node must be non-full when this
        // function is called
        void insertNonFull(int k);

        // A utility function to split the child y of this node. i is index
        // of y in child array C[].  The Child y must be full when this
        // function is called
        void splitChild(int i, BTreeNode *y);

        // A wrapper function to remove the key k in subtree rooted with
        // this node.
        void remove(int k);

        // A function to remove the key present in idx-th position in
        // this node which is a leaf
        void removeFromLeaf(int idx);

        // A function to remove the key present in idx-th position in
        // this node which is a non-leaf node
        void removeFromNonLeaf(int idx);

        // A function to get the predecessor of the key- where the key
        // is present in the idx-th position in the node
        int getPred(int idx);

        // A function to get the successor of the key- where the key
        // is present in the idx-th position in the node
        int getSucc(int idx);

        // A function to fill up the child node present in the idx-th
        // position in the C[] array if that child has less than t-1 keys
        void fill(int idx);

        // A function to borrow a key from the C[idx-1]-th node and place
        // it in C[idx]th node
        void borrowFromPrev(int idx);

        // A function to borrow a key from the C[idx+1]-th node and place it
        // in C[idx]th node
        void borrowFromNext(int idx);

        // A function to merge idx-th child of the node with (idx+1)th child of
        // the node
        void merge(int idx);

        // Make BTree friend of this so that we can access private members of
        // this class in BTree functions
        friend class BTree;
    };

    class BTree
    {
        BTreeNode *root; // Pointer to root node
        int t;  // Minimum degree
    public:

        // Constructor (Initializes tree as empty)
        BTree(int _t)
        {
            root = NULL;
            t = _t;
        }

        void traverse()
        {
            if (root != NULL) root->traverse();
        }

        // function to search a key in this tree
        BTreeNode* search(int k)
        {
            return (root == NULL)? NULL : root->search(k);
        }

        // The main function that inserts a new key in this B-Tree
        void insert(int k);

        // The main function that removes a new key in thie B-Tree
        void remove(int k);

    };

    BTreeNode::BTreeNode(int t1, bool leaf1)
    {
        // Copy the given minimum degree and leaf property
        t = t1;
        leaf = leaf1;

        // Allocate memory for maximum number of possible keys
        // and child pointers
        keys = new int[2*t-1];
        C = new BTreeNode *[2*t];

        // Initialize the number of keys as 0
        n = 0;
    }

    // A utility function that returns the index of the first key that is
    // greater than or equal to k
    int BTreeNode::findKey(int k)
    {
        int idx=0;
        while (idx<n && keys[idx] < k)
            ++idx;
        return idx;
    }

    // A function to remove the key k from the sub-tree rooted with this node
    void BTreeNode::remove(int k)
    {
        int idx = findKey(k);

        // The key to be removed is present in this node
        if (idx < n && keys[idx] == k)
        {

            // If the node is a leaf node - removeFromLeaf is called
            // Otherwise, removeFromNonLeaf function is called
            if (leaf)
                removeFromLeaf(idx);
            else
                removeFromNonLeaf(idx);
        }
        else
        {

            // If this node is a leaf node, then the key is not present in tree
            if (leaf)
            {
                cout << "The key "<< k <<" is does not exist in the tree\n";
                return;
            }

            // The key to be removed is present in the sub-tree rooted with this node
            // The flag indicates whether the key is present in the sub-tree rooted
            // with the last child of this node
            bool flag = ( (idx==n)? true : false );

            // If the child where the key is supposed to exist has less that t keys,
            // we fill that child
            if (C[idx]->n < t)
                fill(idx);

            // If the last child has been merged, it must have merged with the previous
            // child and so we recurse on the (idx-1)th child. Else, we recurse on the
            // (idx)th child which now has atleast t keys
            if (flag && idx > n)
                C[idx-1]->remove(k);
            else
                C[idx]->remove(k);
        }
        return;
    }

    // A function to remove the idx-th key from this node - which is a leaf node
    void BTreeNode::removeFromLeaf (int idx)
    {

        // Move all the keys after the idx-th pos one place backward
        for (int i=idx+1; i<n; ++i)
            keys[i-1] = keys[i];

        // Reduce the count of keys
        n--;

        return;
    }

    // A function to remove the idx-th key from this node - which is a non-leaf node
    void BTreeNode::removeFromNonLeaf(int idx)
    {

        int k = keys[idx];

        // If the child that precedes k (C[idx]) has atleast t keys,
        // find the predecessor 'pred' of k in the subtree rooted at
        // C[idx]. Replace k by pred. Recursively delete pred
        // in C[idx]
        if (C[idx]->n >= t)
        {
            int pred = getPred(idx);
            keys[idx] = pred;
            C[idx]->remove(pred);
        }

        // If the child C[idx] has less that t keys, examine C[idx+1].
        // If C[idx+1] has atleast t keys, find the successor 'succ' of k in
        // the subtree rooted at C[idx+1]
        // Replace k by succ
        // Recursively delete succ in C[idx+1]
        else if  (C[idx+1]->n >= t)
        {
            int succ = getSucc(idx);
            keys[idx] = succ;
            C[idx+1]->remove(succ);
        }

        // If both C[idx] and C[idx+1] has less that t keys,merge k and all of C[idx+1]
        // into C[idx]
        // Now C[idx] contains 2t-1 keys
        // Free C[idx+1] and recursively delete k from C[idx]
        else
        {
            merge(idx);
            C[idx]->remove(k);
        }
        return;
    }

    // A function to get predecessor of keys[idx]
    int BTreeNode::getPred(int idx)
    {
        // Keep moving to the right most node until we reach a leaf
        BTreeNode *cur=C[idx];
        while (!cur->leaf)
            cur = cur->C[cur->n];

        // Return the last key of the leaf
        return cur->keys[cur->n-1];
    }

    int BTreeNode::getSucc(int idx)
    {

        // Keep moving the left most node starting from C[idx+1] until we reach a leaf
        BTreeNode *cur = C[idx+1];
        while (!cur->leaf)
            cur = cur->C[0];

        // Return the first key of the leaf
        return cur->keys[0];
    }

    // A function to fill child C[idx] which has less than t-1 keys
    void BTreeNode::fill(int idx)
    {

        // If the previous child(C[idx-1]) has more than t-1 keys, borrow a key
        // from that child
        if (idx!=0 && C[idx-1]->n>=t)
            borrowFromPrev(idx);

        // If the next child(C[idx+1]) has more than t-1 keys, borrow a key
        // from that child
        else if (idx!=n && C[idx+1]->n>=t)
            borrowFromNext(idx);

        // Merge C[idx] with its sibling
        // If C[idx] is the last child, merge it with with its previous sibling
        // Otherwise merge it with its next sibling
        else
        {
            if (idx != n)
                merge(idx);
            else
                merge(idx-1);
        }
        return;
    }

    // A function to borrow a key from C[idx-1] and insert it
    // into C[idx]
    void BTreeNode::borrowFromPrev(int idx)
    {

        BTreeNode *child=C[idx];
        BTreeNode *sibling=C[idx-1];

        // The last key from C[idx-1] goes up to the parent and key[idx-1]
        // from parent is inserted as the first key in C[idx]. Thus, the  loses
        // sibling one key and child gains one key

        // Moving all key in C[idx] one step ahead
        for (int i=child->n-1; i>=0; --i)
            child->keys[i+1] = child->keys[i];

        // If C[idx] is not a leaf, move all its child pointers one step ahead
        if (!child->leaf)
        {
            for(int i=child->n; i>=0; --i)
                child->C[i+1] = child->C[i];
        }

        // Setting child's first key equal to keys[idx-1] from the current node
        child->keys[0] = keys[idx-1];

        // Moving sibling's last child as C[idx]'s first child
        if (!leaf)
            child->C[0] = sibling->C[sibling->n];

        // Moving the key from the sibling to the parent
        // This reduces the number of keys in the sibling
        keys[idx-1] = sibling->keys[sibling->n-1];

        child->n += 1;
        sibling->n -= 1;

        return;
    }

    // A function to borrow a key from the C[idx+1] and place
    // it in C[idx]
    void BTreeNode::borrowFromNext(int idx)
    {

        BTreeNode *child=C[idx];
        BTreeNode *sibling=C[idx+1];

        // keys[idx] is inserted as the last key in C[idx]
        child->keys[(child->n)] = keys[idx];

        // Sibling's first child is inserted as the last child
        // into C[idx]
        if (!(child->leaf))
            child->C[(child->n)+1] = sibling->C[0];

        //The first key from sibling is inserted into keys[idx]
        keys[idx] = sibling->keys[0];

        // Moving all keys in sibling one step behind
        for (int i=1; i<sibling->n; ++i)
            sibling->keys[i-1] = sibling->keys[i];

        // Moving the child pointers one step behind
        if (!sibling->leaf)
        {
            for(int i=1; i<=sibling->n; ++i)
                sibling->C[i-1] = sibling->C[i];
        }

        // Increasing and decreasing the key count of C[idx] and C[idx+1]
        // respectively
        child->n += 1;
        sibling->n -= 1;

        return;
    }

    // A function to merge C[idx] with C[idx+1]
    // C[idx+1] is freed after merging
    void BTreeNode::merge(int idx)
    {
        BTreeNode *child = C[idx];
        BTreeNode *sibling = C[idx+1];

        // Pulling a key from the current node and inserting it into (t-1)th
        // position of C[idx]
        child->keys[t-1] = keys[idx];

        // Copying the keys from C[idx+1] to C[idx] at the end
        for (int i=0; i<sibling->n; ++i)
            child->keys[i+t] = sibling->keys[i];

        // Copying the child pointers from C[idx+1] to C[idx]
        if (!child->leaf)
        {
            for(int i=0; i<=sibling->n; ++i)
                child->C[i+t] = sibling->C[i];
        }

        // Moving all keys after idx in the current node one step before -
        // to fill the gap created by moving keys[idx] to C[idx]
        for (int i=idx+1; i<n; ++i)
            keys[i-1] = keys[i];

        // Moving the child pointers after (idx+1) in the current node one
        // step before
        for (int i=idx+2; i<=n; ++i)
            C[i-1] = C[i];

        // Updating the key count of child and the current node
        child->n += sibling->n+1;
        n--;

        // Freeing the memory occupied by sibling
        delete(sibling);
        return;
    }

    // The main function that inserts a new key in this B-Tree
    void BTree::insert(int k)
    {
        // If tree is empty
        if (root == NULL)
        {
            // Allocate memory for root
            root = new BTreeNode(t, true);
            root->keys[0] = k;  // Insert key
            root->n = 1;  // Update number of keys in root
        }
        else // If tree is not empty
        {
            // If root is full, then tree grows in height
            if (root->n == 2*t-1)
            {
                // Allocate memory for new root
                BTreeNode *s = new BTreeNode(t, false);

                // Make old root as child of new root
                s->C[0] = root;

                // Split the old root and move 1 key to the new root
                s->splitChild(0, root);

                // New root has two children now.  Decide which of the
                // two children is going to have new key
                int i = 0;
                if (s->keys[0] < k)
                    i++;
                s->C[i]->insertNonFull(k);

                // Change root
                root = s;
            }
            else  // If root is not full, call insertNonFull for root
                root->insertNonFull(k);
        }
    }

    // A utility function to insert a new key in this node
    // The assumption is, the node must be non-full when this
    // function is called
    void BTreeNode::insertNonFull(int k)
    {
        // Initialize index as index of rightmost element
        int i = n-1;

        // If this is a leaf node
        if (leaf == true)
        {
            // The following loop does two things
            // a) Finds the location of new key to be inserted
            // b) Moves all greater keys to one place ahead
            while (i >= 0 && keys[i] > k)
            {
                keys[i+1] = keys[i];
                i--;
            }

            // Insert the new key at found location
            keys[i+1] = k;
            n = n+1;
        }
        else // If this node is not leaf
        {
            // Find the child which is going to have the new key
            while (i >= 0 && keys[i] > k)
                i--;

            // See if the found child is full
            if (C[i+1]->n == 2*t-1)
            {
                // If the child is full, then split it
                splitChild(i+1, C[i+1]);

                // After split, the middle key of C[i] goes up and
                // C[i] is splitted into two.  See which of the two
                // is going to have the new key
                if (keys[i+1] < k)
                    i++;
            }
            C[i+1]->insertNonFull(k);
        }
    }

    // A utility function to split the child y of this node
    // Note that y must be full when this function is called
    void BTreeNode::splitChild(int i, BTreeNode *y)
    {
        // Create a new node which is going to store (t-1) keys
        // of y
        BTreeNode *z = new BTreeNode(y->t, y->leaf);
        z->n = t - 1;

        // Copy the last (t-1) keys of y to z
        for (int j = 0; j < t-1; j++)
            z->keys[j] = y->keys[j+t];

        // Copy the last t children of y to z
        if (y->leaf == false)
        {
            for (int j = 0; j < t; j++)
                z->C[j] = y->C[j+t];
        }

        // Reduce the number of keys in y
        y->n = t - 1;

        // Since this node is going to have a new child,
        // create space of new child
        for (int j = n; j >= i+1; j--)
            C[j+1] = C[j];

        // Link the new child to this node
        C[i+1] = z;

        // A key of y will move to this node. Find location of
        // new key and move all greater keys one space ahead
        for (int j = n-1; j >= i; j--)
            keys[j+1] = keys[j];

        // Copy the middle key of y to this node
        keys[i] = y->keys[t-1];

        // Increment count of keys in this node
        n = n + 1;
    }

    // Function to traverse all nodes in a subtree rooted with this node
    void BTreeNode::traverse()
    {
        // There are n keys and n+1 children, travers through n keys
        // and first n children
        int i;
        for (i = 0; i < n; i++)
        {
            // If this is not leaf, then before printing key[i],
            // traverse the subtree rooted with child C[i].
            if (leaf == false)
                C[i]->traverse();
            cout << " " << keys[i];
        }

        // Print the subtree rooted with last child
        if (leaf == false)
            C[i]->traverse();
    }

    // Function to search key k in subtree rooted with this node
    BTreeNode *BTreeNode::search(int k)
    {
        // Find the first key greater than or equal to k
        int i = 0;
        while (i < n && k > keys[i])
            i++;

        // If the found key is equal to k, return this node
        if (keys[i] == k)
            return this;

        // If key is not found here and this is a leaf node
        if (leaf == true)
            return NULL;

        // Go to the appropriate child
        return C[i]->search(k);
    }

    void BTree::remove(int k)
    {
        if (!root)
        {
            cout << "The tree is empty\n";
            return;
        }

        // Call the remove function for root
        root->remove(k);

        // If the root node has 0 keys, make its first child as the new root
        //  if it has a child, otherwise set root as NULL
        if (root->n==0)
        {
            BTreeNode *tmp = root;
            if (root->leaf)
                root = NULL;
            else
                root = root->C[0];

            // Free the old root
            delete tmp;
        }
        return;
    }

    // Driver program to test above functions
    int main()
    {
        BTree t(3); // A B-Tree with minium degree 3

        t.insert(1);
        t.insert(3);
        t.insert(7);
        t.insert(10);
        t.insert(11);
        t.insert(13);
        t.insert(14);
        t.insert(15);
        t.insert(18);
        t.insert(16);
        t.insert(19);
        t.insert(24);
        t.insert(25);
        t.insert(26);
        t.insert(21);
        t.insert(4);
        t.insert(5);
        t.insert(20);
        t.insert(22);
        t.insert(2);
        t.insert(17);
        t.insert(12);
        t.insert(6);

        cout << "Traversal of tree constructed is\n";
        t.traverse();
        cout << endl;

        t.remove(6);
        cout << "Traversal of tree after removing 6\n";
        t.traverse();
        cout << endl;

        t.remove(13);
        cout << "Traversal of tree after removing 13\n";
        t.traverse();
        cout << endl;

        t.remove(7);
        cout << "Traversal of tree after removing 7\n";
        t.traverse();
        cout << endl;

        t.remove(4);
        cout << "Traversal of tree after removing 4\n";
        t.traverse();
        cout << endl;

        t.remove(2);
        cout << "Traversal of tree after removing 2\n";
        t.traverse();
        cout << endl;

        t.remove(16);
        cout << "Traversal of tree after removing 16\n";
        t.traverse();
        cout << endl;

        return 0;
    }

Output:

    Traversal of tree constructed is
     1 2 3 4 5 6 7 10 11 12 13 14 15 16 17 18 19 20 21 22 24 25 26
    Traversal of tree after removing 6
     1 2 3 4 5 7 10 11 12 13 14 15 16 17 18 19 20 21 22 24 25 26
    Traversal of tree after removing 13
     1 2 3 4 5 7 10 11 12 14 15 16 17 18 19 20 21 22 24 25 26
    Traversal of tree after removing 7
     1 2 3 4 5 10 11 12 14 15 16 17 18 19 20 21 22 24 25 26
    Traversal of tree after removing 4
     1 2 3 5 10 11 12 14 15 16 17 18 19 20 21 22 24 25 26
    Traversal of tree after removing 2
     1 3 5 10 11 12 14 15 16 17 18 19 20 21 22 24 25 26
    Traversal of tree after removing 16
     1 3 5 10 11 12 14 15 17 18 19 20 21 22 24 25 26

This article is contributed by
[**Balasubramanian.N**](http://in.linkedin.com/pub/balasubramanian-nagasundaram/3a/361/97b).
Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/b-tree-set-3delete/>

Binary Indexed Tree or Fenwick tree
-----------------------------------

Let us consider the following problem to understand Binary Indexed
Tree.<span id="more-133016"></span>

We have an array arr[0 . . . n-1]. We should be able to  
 **1** Find the sum of first i elements.  
 **2** Change value of a specified element of the array arr[i] = x where
0 \<= i \<= n-1.

A **simple solution** is to run a loop from 0 to i-1 and calculate sum
of elements. To update a value, simply do arr[i] = x. The first
operation takes O(n) time and second operation takes O(1) time. Another
simple solution is to create another array and store sum from start to i
at the i’th index in this array. Sum of a given range can now be
calculated in O(1) time, but update operation takes O(n) time now. This
works well if the number of query operations are large and very few
updates.

**Can we perform both the operations in O(log n) time once given the
array?**  
 One Efficient Solution is to use [Segment
Tree](http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/)
that does both operations in O(Logn) time.

*Using Binary Indexed Tree, we can do both tasks in O(Logn) time. The
advantages of Binary Indexed Tree over Segment are, requires less space
and very easy to implement.*.

**Representation**  
 Binary Indexed Tree is represented as an array. Let the array be
BITree[]. Each node of Binary Indexed Tree stores sum of some elements
of given array. Size of Binary Indexed Tree is equal to n where n is
size of input array. In the below code, we have used size as n+1 for
ease of implementation.

**Construction**  
 We construct the Binary Indexed Tree by first initializing all values
in BITree[] as 0. Then we call update() operation for all indexes to
store actual sums, update is discussed below.

**Operations**

    getSum(index): Returns sum of arr[0..index]
    // Returns sum of arr[0..index] using BITree[0..n].  It assumes that
    // BITree[] is constructed for given array arr[0..n-1]
    1) Initialize sum as 0 and index as index+1.
    2) Do following while index is greater than 0.
    ...a) Add BITree[index] to sum
    ...b) Go to parent of BITree[index].  Parent can be obtained by removing
         the last set bit from index, i.e., index = index - (index & (-index))
    3) Return sum.

[![BITSum](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BITSum.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BITSum.png)

The above diagram demonstrates working of getSum(). Following are some
important observations.

Node at index 0 is a dummy node.

A node at index y is parent of a node at index x, iff y can be obtained
by removing last set bit from binary representation of x.

A child x of a node y stores sum of elements from of y(exclusive y) and
of x(inclusive x).

 


    update(index, val): Updates BIT for operation arr[index] += val
    // Note that arr[] is not changed here.  It changes
    // only BI Tree for the already made change in arr[].
    1) Initialize index as index+1.
    2) Do following while index is smaller than or equal to n.
    ...a) Add value to BITree[index]
    ...b) Go to parent of BITree[index].  Parent can be obtained by removing
         the last set bit from index, i.e., index = index - (index & (-index))

[![BITUpdate1](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BITUpdate12.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BITUpdate12.png)

The update process needs to make sure that all BITree nodes that have
arr[i] as part of the section they cover must be updated. We get all
such nodes of BITree by repeatedly adding the decimal number
corresponding to the last set bit.

 

**How does Binary Indexed Tree work?**  
 The idea is based on the fact that all positive integers can be
represented as sum of powers of 2. For example 19 can be represented as
16 + 2 + 1. Every node of BI Tree stores sum of n elements where n is a
power of 2. For example, in the above first diagram for getSum(), sum of
first 12 elements can be obtained by sum of last 4 elements (from 9 to
12) plus sum of 8 elements (from 1 to 8). The number of set bits in
binary representation of a number n is O(Logn). Therefore, we traverse
at-most O(Logn) nodes in both getSum() and update() operations. Time
complexity of construction is O(nLogn) as it calls update() for all n
elements.

**Implementation:**  
 Following is C++ implementation of Binary Indexed Tree.

    // C++ code to demonstrate operations of Binary Index Tree
    #include <iostream>
    using namespace std;

    /*            n  --> No. of elements present in input array.   
        BITree[0..n] --> Array that represents Binary Indexed Tree.
        arr[0..n-1]  --> Input array for whic prefix sum is evaluated. */

    // Returns sum of arr[0..index]. This function assumes
    // that the array is preprocessed and partial sums of
    // array elements are stored in BITree[].
    int getSum(int BITree[], int n, int index)
    {
        int sum = 0; // Iniialize result

        // index in BITree[] is 1 more than the index in arr[]
        index = index + 1;

        // Traverse ancestors of BITree[index]
        while (index>0)
        {
            // Add current element of BITree to sum
            sum += BITree[index];

            // Move index to parent node
            index -= index & (-index);
        }
        return sum;
    }

    // Updates a node in Binary Index Tree (BITree) at given index
    // in BITree.  The given value 'val' is added to BITree[i] and 
    // all of its ancestors in tree.
    void updateBIT(int *BITree, int n, int index, int val)
    {
        // index in BITree[] is 1 more than the index in arr[]
        index = index + 1;

        // Traverse all ancestors and add 'val'
        while (index <= n)
        {
           // Add 'val' to current node of BI Tree
           BITree[index] += val;

           // Update index to that of parent
           index += index & (-index);
        }
    }

    // Constructs and returns a Binary Indexed Tree for given
    // array of size n.
    int *constructBITree(int arr[], int n)
    {
        // Create and initialize BITree[] as 0
        int *BITree = new int[n+1];
        for (int i=1; i<=n; i++)
            BITree[i] = 0;

        // Store the actual values in BITree[] using update()
        for (int i=0; i<n; i++)
            updateBIT(BITree, n, i, arr[i]);

        // Uncomment below lines to see contents of BITree[]
        //for (int i=1; i<=n; i++)
        //      cout << BITree[i] << " ";

        return BITree;
    }


    // Driver program to test above functions
    int main()
    {
        int freq[] = {2, 1, 1, 3, 2, 3, 4, 5, 6, 7, 8, 9};
        int n = sizeof(freq)/sizeof(freq[0]);
        int *BITree = constructBITree(freq, n);
        cout << "Sum of elements in arr[0..5] is "
             << getSum(BITree, n, 5);

        // Let use test the update operation
        freq[3] += 6;
        updateBIT(BITree, n, 3, 6); //Update BIT for above change in arr[]

        cout << "\nSum of elements in arr[0..5] after update is "
             << getSum(BITree, n, 5);

        return 0;
    }

Output:

    Sum of elements in arr[0..5] is 12
    Sum of elements in arr[0..5] after update is 18

**Can we extend the Binary Indexed Tree for range Sum in Logn time?**  
 This is simple to answer. The rangeSum(l, r) can be obtained as
getSum(r) – getSum(l-1).

**Applications:**  
 Used to implement the arithmetic coding algorithm. Development of
operations it supports were primarily motivated by use in that case. See
[this](http://en.wikipedia.org/wiki/Fenwick_tree#Applications)for more
details.

**References:**  
 <http://en.wikipedia.org/wiki/Fenwick_tree>  

<http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=binaryIndexedTrees>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/binary-indexed-tree-or-fenwick-tree-2/>

Binomial Heap
-------------

The main application of [Binary
Heap](http://geeksquiz.com/binary-heap/)is as implement priority queue.
Binomial Heap is an extension of [Binary
Heap](http://geeksquiz.com/binary-heap/)that provides faster union or
merge operation together with other operations provided by Binary
Heap.<span id="more-132305"></span>

*A Binomial Heap is a collection of Binomial Trees*

**What is a Binomial Tree?**  
 A Binomial Tree of order 0 has 1 node. A Binomial Tree of order k can
be constructed by taking two binomial trees of order k-1, and making one
as leftmost child of other.  
 A Binomial Tree of order k has following properties.  
 a) It has exactly 2<sup>k</sup> nodes.  
 b) It has depth as k.  
 c) There are exactly kCi nodes at depth i for i = 0, 1, . . . , k.  
 d) The root has degree k and children of root are themselves Binomial
Trees with order k-1, k-2,.. 0 from left to right.

The following diagram is taken from 2nd Edition of [CLRS
book](http://www.flipkart.com/introduction-algorithms-english-3rd/p/itmdwxyrafdburzg?pid=9788120340077&affid=sandeepgfg).

[![BinomialTree](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BinomialTree.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BinomialTree.png)

**Binomial Heap:**  
 A Binomial Heap is a set of Binomial Trees where each Binomial Tree
follows Min Heap property. And there can be at-most one Binomial Tree of
any degree.

**Examples Binomial Heap:**

    12------------10--------------------20
                 /  \                 /  | \
               15    50             70  50  40
               |                  / |    |
               30               80  85  65
                                |
                               100
    A Binomial Heap with 13 nodes. It is a collection of 3
    Binomial Trees of orders 0, 2 and 3 from left to right.

        10--------------------20
       /  \                 /  | \
     15    50             70  50  40
     |                  / |    |
     30               80  85  65
                      |
                     100

A Binomial Heap with 12 nodes. It is a collection of 2  
 Binomial Trees of orders 2 and 3 from left to right.

**Binary Representation of a number and Binomial Heaps**  
 A Binomial Heap with n nodes has number of Binomial Trees equal to the
number of set bits in Binary representation of n. For example let n be
13, there 3 set bits in binary representation of n (00001101), hence 3
Binomial Trees. We can also relate degree of these Binomial Trees with
positions of set bits. With this relation we can conclude that there are
O(Logn) Binomial Trees in a Binomial Heap with ‘n’ nodes.

**Operations of Binomial Heap:**  
 The main operation in Binomial Heap is union(), all other operations
mainly use this operation. The union() operation is to combine two
Binomial Heaps into one. Let us first discuss other operations, we will
discuss union later.

**1)** insert(H, k): Inserts a key ‘k’ to Binomial Heap ‘H’. This
operation first creates a Binomial Heap with single key ‘k’, then calls
union on H and the new Binomial heap.

**2)** getMin(H): A simple way to getMin() is to traverse the list of
root of Binomial Trees and return the minimum key. This implementation
requires O(Logn) time. It can be optimized to O(1) by maintaining a
pointer to minimum key root.

**3)** extractMin(H): This operation also uses union(). We first call
getMin() to find the minimum key Binomial Tree, then we remove the node
and create a new Binomial Heap by connecting all subtrees of the removed
minimum node. Finally we call union() on H and the newly created
Binomial Heap. This operation requires O(Logn) time.

**4)** delete(H): Like Binary Heap, delete operation first reduces the
key to minus infinite, then calls extractMin().

**5)** decreaseKey(H): decreaseKey() is also similar to Binary Heap. We
compare the decreases key with it parent and if parent’s key is less, we
swap keys and recur for parent. We stop when we either reach a node
whose parent has smaller key or we hit the root node. Time complexity of
decreaseKey() is O(Logn).

**Union operation in Binomial Heap:**  
 Given two Binomial Heaps H1 and H2, union(H1, H2) creates a single
Binomial Heap.  
 **1)** The first step is to simply merge the two Heaps in
non-decreasing order of degrees. In the following diagram, figure(b)
shows the result after merging.

**2)** After the simple merge, we need to make sure that there is
at-most one Binomial Tree of any order. To do this, we need to combine
Binomial Trees of same order. We traverse the list of merged roots, we
keep track of three pointers, prev, x and next-x. There can be following
4 cases when we traverse the list of roots.  
 —–Case 1: Orders of x and next-x are not same, we simply move ahead.  
 In following 3 cases orders of x and next-x are same.  
 —–Case 2: If order of next-next-x is also same, move ahead.  
 —–Case 3: If key of x is smaller than or equal to key of next-x, then
make next-x as a child of x by linking it with x.  
 —–Case 4: If key of x is greater, then make x as child of next.

The following diagram is taken from 2nd Edition of [CLRS
book](http://www.flipkart.com/introduction-algorithms-english-3rd/p/itmdwxyrafdburzg?pid=9788120340077&affid=sandeepgfg).  

[![BinomialHeapUnion](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BinomialHeapUnion.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/BinomialHeapUnion.png)

**How to represent Binomial Heap?**  
 A Binomial Heap is a set of Binomial Trees. A Binomial Tree must be
represented in a way that allows sequential access to all siblings,
starting from the leftmost sibling (We need this in and extractMin() and
delete()). The idea is to represent Binomial Trees as leftmost child and
right-sibling representation, i.e., every node stores two pointers, one
to the leftmost child and other to the right sibling.

We will soon be discussing implementation of Binomial Heap.

**Sources:**  
 [Introduction to Algorithms by Clifford Stein, Thomas H. Cormen,
Charles E. Leiserson, Ronald L.  
](http://www.flipkart.com/introduction-algorithms-8120340078/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)

This article is contributed by **Shivam**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/binomial-heap-2/>

Data Structure for Dictionary and Spell Checker?
------------------------------------------------

**Which data structure can be used for efficiently building a word
dictionary and [Spell
Checker](http://en.wikipedia.org/wiki/Spell_checker)?**<span
id="more-130790"></span>

The answer depends upon the functionalists required in Spell Checker and
availability of memory. For example following are few possibilities.

[**Hashing**](http://geeksquiz.com/hashing-set-1-introduction/)is one
simple option for this. We can put all words in a hash table. Refer
[this](http://www.cs.unc.edu/~plaisted/comp550/Neyer%20paper.pdf)paper
which compares hashing with self-balancing Binary Search Trees and Skip
List, and shows that hashing performs better.

Hashing doesn’t support operations like prefix search. Prefix search is
something where a user types a prefix and your dictionary shows all
words starting with that prefix. Hashing also doesn’t support efficient
printing of all words in dictionary in alphabetical order and nearest
neighbor search.

If we want both operations, look up and prefix search,
[**Trie**](http://www.geeksforgeeks.org/trie-insert-and-search/) is
suited. With Trie, we can support all operations like insert, search,
delete in O(n) time where n is length of the word to be processed.
Another advantage of Trie is, we can print all words in alphabetical
order which is not possible with hashing.

The disadvantage of Trie is, it requires lots of space. If space is
concern, then **[Ternary Search
Tree](http://www.geeksforgeeks.org/ternary-search-tree/)** can be
preferred. In Ternary Search Tree, time complexity of search operation
is O(h) where h is height of the tree. Ternary Search Trees also
supports other operations supported by Trie like prefix search,
alphabetical order printing and nearest neighbor search.

If we want to support suggestions, like google shows “*did you mean* …”,
then we need to find the closest word in dictionary. The closest word
can be defined as the word that can be obtained with minimum number of
character transformations (add, delete, replace). A Naive way is to take
the given word and generate all words which are 1 distance (1 edit or 1
delete or 1 replace) away and one by one look them in dictionary. If
nothing found, then look for all words which are 2 distant and so on.
There are many complex algorithms for this. As per[the wiki
page](http://en.wikipedia.org/wiki/Spell_checker), The most successful
algorithm to date is Andrew Golding and Dan Roth’s Window-based spelling
correction algorithm.

See [this](http://norvig.com/spell-correct.html)for a simple spell
checker implementation.

This article is compiled by **Piyush**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/data-structure-dictionary-spell-checker/>

Find the k most frequent words from a file
------------------------------------------

Given a book of words. Assume you have enough main memory to accommodate
all words. design a data structure to find top K maximum occurring
words. The data structure should be dynamic so that new words can be
added. <span id="more-24329"></span>

A simple solution is to **use Hashing**. Hash all words one by one in a
hash table. If a word is already present, then increment its count.
Finally, traverse through the hash table and return the k words with
maximum counts.

We can **use Trie and Min Heap** to get the k most frequent words
efficiently. The idea is to use Trie for searching existing words adding
new words efficiently. Trie also stores count of occurrences of words. A
Min Heap of size k is used to keep track of k most frequent words at any
point of time(Use of Min Heap is same as we used it to find k largest
elements in [this](http://www.geeksforgeeks.org/archives/2392) post).  
 Trie and Min Heap are linked with each other by storing an additional
field in Trie ‘indexMinHeap’ and a pointer ‘trNode’ in Min Heap. The
value of ‘indexMinHeap’ is maintained as -1 for the words which are
currently not in Min Heap (or currently not among the top k frequent
words). For the words which are present in Min Heap, ‘indexMinHeap’
contains, index of the word in Min Heap. The pointer ‘trNode’ in Min
Heap points to the leaf node corresponding to the word in Trie.

Following is the complete process to print k most frequent words from a
file.

Read all words one by one. For every word, insert it into Trie. Increase
the counter of the word, if already exists. Now, we need to insert this
word in min heap also. For insertion in min heap, 3 cases arise:

**1.** The word is already present. We just increase the corresponding
frequency value in min heap and call minHeapify() for the index obtained
by “indexMinHeap” field in Trie. When the min heap nodes are being
swapped, we change the corresponding minHeapIndex in the Trie. Remember
each node of the min heap is also having pointer to Trie leaf node.

**2.** The minHeap is not full. we will insert the new word into min
heap & update the root node in the min heap node & min heap index in
Trie leaf node. Now, call buildMinHeap().

**3.** The min heap is full. Two sub-cases arise.  
 ….**3.1** The frequency of the new word inserted is less than the
frequency of the word stored in the head of min heap. Do nothing.

….**3.2** The frequency of the new word inserted is greater than the
frequency of the word stored in the head of min heap. Replace & update
the fields. Make sure to update the corresponding min heap index of the
“word to be replaced” in Trie with -1 as the word is no longer in min
heap.

**4.** Finally, Min Heap will have the k most frequent words of all
words present in given file. So we just need to print all words present
in Min Heap.

    // A program to find k most frequent words in a file
    #include <stdio.h>
    #include <string.h>
    #include <ctype.h>

    # define MAX_CHARS 26
    # define MAX_WORD_SIZE 30

    // A Trie node
    struct TrieNode
    {
        bool isEnd; // indicates end of word
        unsigned frequency;  // the number of occurrences of a word
        int indexMinHeap; // the index of the word in minHeap
        TrieNode* child[MAX_CHARS]; // represents 26 slots each for 'a' to 'z'.
    };

    // A Min Heap node
    struct MinHeapNode
    {
        TrieNode* root; // indicates the leaf node of TRIE
        unsigned frequency; //  number of occurrences
        char* word; // the actual word stored
    };

    // A Min Heap
    struct MinHeap
    {
        unsigned capacity; // the total size a min heap
        int count; // indicates the number of slots filled.
        MinHeapNode* array; //  represents the collection of minHeapNodes
    };

    // A utility function to create a new Trie node
    TrieNode* newTrieNode()
    {
        // Allocate memory for Trie Node
        TrieNode* trieNode = new TrieNode;

        // Initialize values for new node
        trieNode->isEnd = 0;
        trieNode->frequency = 0;
        trieNode->indexMinHeap = -1;
        for( int i = 0; i < MAX_CHARS; ++i )
            trieNode->child[i] = NULL;

        return trieNode;
    }

    // A utility function to create a Min Heap of given capacity
    MinHeap* createMinHeap( int capacity )
    {
        MinHeap* minHeap = new MinHeap;

        minHeap->capacity = capacity;
        minHeap->count  = 0;

        // Allocate memory for array of min heap nodes
        minHeap->array = new MinHeapNode [ minHeap->capacity ];

        return minHeap;
    }

    // A utility function to swap two min heap nodes. This function
    // is needed in minHeapify
    void swapMinHeapNodes ( MinHeapNode* a, MinHeapNode* b )
    {
        MinHeapNode temp = *a;
        *a = *b;
        *b = temp;
    }

    // This is the standard minHeapify function. It does one thing extra.
    // It updates the minHapIndex in Trie when two nodes are swapped in
    // in min heap
    void minHeapify( MinHeap* minHeap, int idx )
    {
        int left, right, smallest;

        left = 2 * idx + 1;
        right = 2 * idx + 2;
        smallest = idx;
        if ( left < minHeap->count &&
             minHeap->array[ left ]. frequency <
             minHeap->array[ smallest ]. frequency
           )
            smallest = left;

        if ( right < minHeap->count &&
             minHeap->array[ right ]. frequency <
             minHeap->array[ smallest ]. frequency
           )
            smallest = right;

        if( smallest != idx )
        {
            // Update the corresponding index in Trie node.
            minHeap->array[ smallest ]. root->indexMinHeap = idx;
            minHeap->array[ idx ]. root->indexMinHeap = smallest;

            // Swap nodes in min heap
            swapMinHeapNodes (&minHeap->array[ smallest ], &minHeap->array[ idx ]);

            minHeapify( minHeap, smallest );
        }
    }

    // A standard function to build a heap
    void buildMinHeap( MinHeap* minHeap )
    {
        int n, i;
        n = minHeap->count - 1;

        for( i = ( n - 1 ) / 2; i >= 0; --i )
            minHeapify( minHeap, i );
    }

    // Inserts a word to heap, the function handles the 3 cases explained above
    void insertInMinHeap( MinHeap* minHeap, TrieNode** root, const char* word )
    {
        // Case 1: the word is already present in minHeap
        if( (*root)->indexMinHeap != -1 )
        {
            ++( minHeap->array[ (*root)->indexMinHeap ]. frequency );

            // percolate down
            minHeapify( minHeap, (*root)->indexMinHeap );
        }

        // Case 2: Word is not present and heap is not full
        else if( minHeap->count < minHeap->capacity )
        {
            int count = minHeap->count;
            minHeap->array[ count ]. frequency = (*root)->frequency;
            minHeap->array[ count ]. word = new char [strlen( word ) + 1];
            strcpy( minHeap->array[ count ]. word, word );

            minHeap->array[ count ]. root = *root;
            (*root)->indexMinHeap = minHeap->count;

            ++( minHeap->count );
            buildMinHeap( minHeap );
        }

        // Case 3: Word is not present and heap is full. And frequency of word
        // is more than root. The root is the least frequent word in heap,
        // replace root with new word
        else if ( (*root)->frequency > minHeap->array[0]. frequency )
        {

            minHeap->array[ 0 ]. root->indexMinHeap = -1;
            minHeap->array[ 0 ]. root = *root;
            minHeap->array[ 0 ]. root->indexMinHeap = 0;
            minHeap->array[ 0 ]. frequency = (*root)->frequency;

            // delete previously allocated memoory and
            delete [] minHeap->array[ 0 ]. word;
            minHeap->array[ 0 ]. word = new char [strlen( word ) + 1];
            strcpy( minHeap->array[ 0 ]. word, word );

            minHeapify ( minHeap, 0 );
        }
    }

    // Inserts a new word to both Trie and Heap
    void insertUtil ( TrieNode** root, MinHeap* minHeap,
                            const char* word, const char* dupWord )
    {
        // Base Case
        if ( *root == NULL )
            *root = newTrieNode();

        //  There are still more characters in word
        if ( *word != '\0' )
            insertUtil ( &((*root)->child[ tolower( *word ) - 97 ]),
                             minHeap, word + 1, dupWord );
        else // The complete word is processed
        {
            // word is already present, increase the frequency
            if ( (*root)->isEnd )
                ++( (*root)->frequency );
            else
            {
                (*root)->isEnd = 1;
                (*root)->frequency = 1;
            }

            // Insert in min heap also
            insertInMinHeap( minHeap, root, dupWord );
        }
    }


    // add a word to Trie & min heap.  A wrapper over the insertUtil
    void insertTrieAndHeap(const char *word, TrieNode** root, MinHeap* minHeap)
    {
        insertUtil( root, minHeap, word, word );
    }

    // A utility function to show results, The min heap
    // contains k most frequent words so far, at any time
    void displayMinHeap( MinHeap* minHeap )
    {
        int i;

        // print top K word with frequency
        for( i = 0; i < minHeap->count; ++i )
        {
            printf( "%s : %d\n", minHeap->array[i].word,
                                minHeap->array[i].frequency );
        }
    }

    // The main funtion that takes a file as input, add words to heap
    // and Trie, finally shows result from heap
    void printKMostFreq( FILE* fp, int k )
    {
        // Create a Min Heap of Size k
        MinHeap* minHeap = createMinHeap( k );
       
        // Create an empty Trie
        TrieNode* root = NULL;

        // A buffer to store one word at a time
        char buffer[MAX_WORD_SIZE];

        // Read words one by one from file.  Insert the word in Trie and Min Heap
        while( fscanf( fp, "%s", buffer ) != EOF )
            insertTrieAndHeap(buffer, &root, minHeap);

        // The Min Heap will have the k most frequent words, so print Min Heap nodes
        displayMinHeap( minHeap );
    }

    // Driver program to test above functions
    int main()
    {
        int k = 5;
        FILE *fp = fopen ("file.txt", "r");
        if (fp == NULL)
            printf ("File doesn't exist ");
        else
            printKMostFreq (fp, k);
        return 0;
    }

Output:

    your : 3
    well : 3
    and : 4
    to : 4
    Geeks : 6

The above output is for a file with following content.

    Welcome to the world of Geeks 
    This portal has been created to provide well written well thought and well explained 
    solutions for selected questions If you like Geeks for Geeks and would like to contribute 
    here is your chance You can write article and mail your article to contribute at 
    geeksforgeeks org See your article appearing on the Geeks for Geeks main page and help 
    thousands of other Geeks

  
 Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/)

### Source:

<http://www.geeksforgeeks.org/find-the-k-most-frequent-words-from-a-file/>

Given a sequence of words, print all anagrams together | Set 2
--------------------------------------------------------------

Given an array of words, print all anagrams together. For example, if
the given array is {â€œcatâ€?, â€œdogâ€?, â€œtacâ€?, â€œgodâ€?,
â€œactâ€?}, then output may be â€œcat tac act dog godâ€?.<span
id="more-26180"></span>

We have discussed two different methods in the [previous
post](http://www.geeksforgeeks.org/archives/26125). In this post, a more
efficient solution is discussed.

Trie data structure can be used for a more efficient solution. Insert
the sorted order of each word in the trie. Since all the anagrams will
end at the same leaf node. We can start a linked list at the leaf nodes
where each node represents the index of the original array of words.
Finally, traverse the Trie. While traversing the Trie, traverse each
linked list one line at a time. Following are the detailed steps.

**1)** Create an empty Trie  
 **2)** One by one take all words of input sequence. Do following for
each word  
 …**a)** Copy the word to a buffer.  
 …**b)** Sort the buffer  
 …**c)** Insert the sorted buffer and index of this word to Trie. Each
leaf node of Trie is head of a Index list. The Index list stores index
of words in original sequence. If sorted buffe is already present, we
insert index of this word to the index list.  
 **3)** Traverse Trie. While traversing, if you reach a leaf node,
traverse the index list. And print all words using the index obtained
from Index list.

    // An efficient program to print all anagrams together
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ctype.h>

    #define NO_OF_CHARS 26

    // Structure to represent list node for indexes of words in
    // the given sequence. The list nodes are used to connect
    // anagrams at leaf nodes of Trie
    struct IndexNode
    {
        int index;
        struct IndexNode* next;
    };

    // Structure to represent a Trie Node
    struct TrieNode
    {
        bool isEnd;  // indicates end of word
        struct TrieNode* child[NO_OF_CHARS]; // 26 slots each for 'a' to 'z'
        struct IndexNode* head; // head of the index list
    };


    // A utility function to create a new Trie node
    struct TrieNode* newTrieNode()
    {
        struct TrieNode* temp = new TrieNode;
        temp->isEnd = 0;
        temp->head = NULL;
        for (int i = 0; i < NO_OF_CHARS; ++i)
            temp->child[i] = NULL;
        return temp;
    }

    /* Following function is needed for library function qsort(). Refer
       http://www.cplusplus.com/reference/clibrary/cstdlib/qsort/ */
    int compare(const void* a, const void* b)
    {  return *(char*)a - *(char*)b; }

    /* A utility function to create a new linked list node */
    struct IndexNode* newIndexNode(int index)
    {
        struct IndexNode* temp = new IndexNode;
        temp->index = index;
        temp->next = NULL;
        return temp;
    }

    // A utility function to insert a word to Trie
    void insert(struct TrieNode** root, char* word, int index)
    {
        // Base case
        if (*root == NULL)
            *root = newTrieNode();

        if (*word != '\0')
            insert( &( (*root)->child[tolower(*word) - 'a'] ), word+1, index );
        else  // If end of the word reached
        {
            // Insert index of this word to end of index linked list
            if ((*root)->isEnd)
            {
                IndexNode* pCrawl = (*root)->head;
                while( pCrawl->next )
                    pCrawl = pCrawl->next;
                pCrawl->next = newIndexNode(index);
            }
            else  // If Index list is empty
            {
                (*root)->isEnd = 1;
                (*root)->head = newIndexNode(index);
            }
        }
    }

    // This function traverses the built trie. When a leaf node is reached,
    // all words connected at that leaf node are anagrams. So it traverses
    // the list at leaf node and uses stored index to print original words
    void printAnagramsUtil(struct TrieNode* root, char *wordArr[])
    {
        if (root == NULL)
            return;

        // If a lead node is reached, print all anagrams using the indexes
        // stored in index linked list
        if (root->isEnd)
        {
            // traverse the list
            IndexNode* pCrawl = root->head;
            while (pCrawl != NULL)
            {
                printf( "%s \n", wordArr[ pCrawl->index ] );
                pCrawl = pCrawl->next;
            }
        }

        for (int i = 0; i < NO_OF_CHARS; ++i)
            printAnagramsUtil(root->child[i], wordArr);
    }

    // The main function that prints all anagrams together. wordArr[] is input
    // sequence of words.
    void printAnagramsTogether(char* wordArr[], int size)
    {
        // Create an empty Trie
        struct TrieNode* root = NULL;

        // Iterate through all input words
        for (int i = 0; i < size; ++i)
        {
            // Create a buffer for this word and copy the word to buffer
            int len = strlen(wordArr[i]);
            char *buffer = new char[len+1];
            strcpy(buffer, wordArr[i]);

            // Sort the buffer
            qsort( (void*)buffer, strlen(buffer), sizeof(char), compare );

            // Insert the sorted buffer and its original index to Trie
            insert(&root,  buffer, i);
        }

        // Traverse the built Trie and print all anagrms together
        printAnagramsUtil(root, wordArr);
    }


    // Driver program to test above functions
    int main()
    {
        char* wordArr[] = {"cat", "dog", "tac", "god", "act", "gdo"};
        int size = sizeof(wordArr) / sizeof(wordArr[0]);
        printAnagramsTogether(wordArr, size);
        return 0;
    }

Output:

    cat
    tac
    act
    dog
    god
    gdo

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/)

### Source:

<http://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together-set-2/>

Implement LRU Cache
-------------------

How to implement LRU caching scheme? What data structures should be
used?

We are given total possible page numbers that can be referred. We are
also given cache (or memory) size (Number of page frames that cache can
hold at a time). The LRU caching scheme is to remove the least recently
used frame when the cache is full and a new page is referenced which is
not there in cache. Please see the Galvin book for more details (see the
LRU page replacement slide
[here](http://www.wiley.com/college/silberschatz6e/0471417432/slides/pdf2/mod10.2.pdf)).

We use two data structures to implement an LRU Cache.

**1.** A Queue which is implemented using a doubly linked list. The
maximum size of the queue will be equal to the total number of frames
available (cache size).  
 The most recently used pages will be near front end and least recently
pages will be near rear end.

**2.** A Hash with page number as key and address of the corresponding
queue node as value.

When a page is referenced, the required page may be in the memory. If it
is in the memory, we need to detach the node of the list and bring it to
the front of the queue.  
 If the required page is not in the memory, we bring that in memory. In
simple words, we add a new node to the front of the queue and update the
corresponding node address in the hash. If the queue is full, i.e. all
the frames are full, we remove a node from the rear of queue, and add
the new node to the front of queue.

Note: Initially no page is in the memory.

Below is C implementation:

    // A C program to show implementation of LRU cache
    #include <stdio.h>
    #include <stdlib.h>

    // A Queue Node (Queue is implemented using Doubly Linked List)
    typedef struct QNode
    {
        struct QNode *prev, *next;
        unsigned pageNumber;  // the page number stored in this QNode
    } QNode;

    // A Queue (A FIFO collection of Queue Nodes)
    typedef struct Queue
    {
        unsigned count;  // Number of filled frames
        unsigned numberOfFrames; // total number of frames
        QNode *front, *rear;
    } Queue;

    // A hash (Collection of pointers to Queue Nodes)
    typedef struct Hash
    {
        int capacity; // how many pages can be there
        QNode* *array; // an array of queue nodes
    } Hash;

    // A utility function to create a new Queue Node. The queue Node
    // will store the given 'pageNumber'
    QNode* newQNode( unsigned pageNumber )
    {
        // Allocate memory and assign 'pageNumber'
        QNode* temp = (QNode *)malloc( sizeof( QNode ) );
        temp->pageNumber = pageNumber;

        // Initialize prev and next as NULL
        temp->prev = temp->next = NULL;

        return temp;
    }

    // A utility function to create an empty Queue.
    // The queue can have at most 'numberOfFrames' nodes
    Queue* createQueue( int numberOfFrames )
    {
        Queue* queue = (Queue *)malloc( sizeof( Queue ) );

        // The queue is empty
        queue->count = 0;
        queue->front = queue->rear = NULL;

        // Number of frames that can be stored in memory
        queue->numberOfFrames = numberOfFrames;

        return queue;
    }

    // A utility function to create an empty Hash of given capacity
    Hash* createHash( int capacity )
    {
        // Allocate memory for hash
        Hash* hash = (Hash *) malloc( sizeof( Hash ) );
        hash->capacity = capacity;

        // Create an array of pointers for refering queue nodes
        hash->array = (QNode **) malloc( hash->capacity * sizeof( QNode* ) );

        // Initialize all hash entries as empty
        int i;
        for( i = 0; i < hash->capacity; ++i )
            hash->array[i] = NULL;

        return hash;
    }

    // A function to check if there is slot available in memory
    int AreAllFramesFull( Queue* queue )
    {
        return queue->count == queue->numberOfFrames;
    }

    // A utility function to check if queue is empty
    int isQueueEmpty( Queue* queue )
    {
        return queue->rear == NULL;
    }

    // A utility function to delete a frame from queue
    void deQueue( Queue* queue )
    {
        if( isQueueEmpty( queue ) )
            return;

        // If this is the only node in list, then change front
        if (queue->front == queue->rear)
            queue->front = NULL;

        // Change rear and remove the previous rear
        QNode* temp = queue->rear;
        queue->rear = queue->rear->prev;

        if (queue->rear)
            queue->rear->next = NULL;

        free( temp );

        // decrement the number of full frames by 1
        queue->count--;
    }

    // A function to add a page with given 'pageNumber' to both queue
    // and hash
    void Enqueue( Queue* queue, Hash* hash, unsigned pageNumber )
    {
        // If all frames are full, remove the page at the rear
        if ( AreAllFramesFull ( queue ) )
        {
            // remove page from hash
            hash->array[ queue->rear->pageNumber ] = NULL;
            deQueue( queue );
        }

        // Create a new node with given page number,
        // And add the new node to the front of queue
        QNode* temp = newQNode( pageNumber );
        temp->next = queue->front;

        // If queue is empty, change both front and rear pointers
        if ( isQueueEmpty( queue ) )
            queue->rear = queue->front = temp;
        else  // Else change the front
        {
            queue->front->prev = temp;
            queue->front = temp;
        }

        // Add page entry to hash also
        hash->array[ pageNumber ] = temp;

        // increment number of full frames
        queue->count++;
    }

    // This function is called when a page with given 'pageNumber' is referenced
    // from cache (or memory). There are two cases:
    // 1. Frame is not there in memory, we bring it in memory and add to the front
    //    of queue
    // 2. Frame is there in memory, we move the frame to front of queue
    void ReferencePage( Queue* queue, Hash* hash, unsigned pageNumber )
    {
        QNode* reqPage = hash->array[ pageNumber ];

        // the page is not in cache, bring it
        if ( reqPage == NULL )
            Enqueue( queue, hash, pageNumber );

        // page is there and not at front, change pointer
        else if (reqPage != queue->front)
        {
            // Unlink rquested page from its current location
            // in queue.
            reqPage->prev->next = reqPage->next;
            if (reqPage->next)
               reqPage->next->prev = reqPage->prev;

            // If the requested page is rear, then change rear
            // as this node will be moved to front
            if (reqPage == queue->rear)
            {
               queue->rear = reqPage->prev;
               queue->rear->next = NULL;
            }

            // Put the requested page before current front
            reqPage->next = queue->front;
            reqPage->prev = NULL;

            // Change prev of current front
            reqPage->next->prev = reqPage;

            // Change front to the requested page
            queue->front = reqPage;
        }
    }

    // Driver program to test above functions
    int main()
    {
        // Let cache can hold 4 pages
        Queue* q = createQueue( 4 );

        // Let 10 different pages can be requested (pages to be
        // referenced are numbered from 0 to 9
        Hash* hash = createHash( 10 );

        // Let us refer pages 1, 2, 3, 1, 4, 5
        ReferencePage( q, hash, 1);
        ReferencePage( q, hash, 2);
        ReferencePage( q, hash, 3);
        ReferencePage( q, hash, 1);
        ReferencePage( q, hash, 4);
        ReferencePage( q, hash, 5);

        // Let us print cache frames after the above referenced pages
        printf ("%d ", q->front->pageNumber);
        printf ("%d ", q->front->next->pageNumber);
        printf ("%d ", q->front->next->next->pageNumber);
        printf ("%d ", q->front->next->next->next->pageNumber);

        return 0;
    }

Output:

    5 4 1 3

This article is compiled by [Aashish
Barnwal](https://www.facebook.com/barnwal.aashish)and reviewed by
GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/),
[Queue](http://www.geeksforgeeks.org/tag/queue/)

### Source:

<http://www.geeksforgeeks.org/implement-lru-cache/>

How to Implement Reverse DNS Look Up Cache?
-------------------------------------------

Reverse DNS look up is using an internet IP address to find a domain
name. For example, if you type 74.125.200.106 in browser, it
automatically redirects to google.in. <span id="more-133039"></span>

How to implement Reverse DNS Look Up cache? Following are the operations
needed from cache.  
 1) Add a IP address to URL Mapping in cache.  
 2) Find URL for a given IP address.

One solution is to use
[Hashing](http://geeksquiz.com/hashing-set-1-introduction/).

In this post, a
[Trie](http://www.geeksforgeeks.org/trie-insert-and-search/)based
solution is discussed. One advantage of Trie based solutions is, worst
case upper bound is O(1) for Trie, for hashing, the best possible
average case time complexity is O(1). Also, with Trie we can implement
prefix search (finding all urls for a common prefix of IP addresses).  
 The general disadvantage of Trie is large amount of memory requirement,
this is not a major problem here as the alphabet size is only 11 here.
Ten characters are needed for digits from ‘0’ to ‘9’ and one for dot
(‘.’).  
 The idea is to store IP addresses in Trie nodes and in the last node we
store the corresponding domain name. Following is C style implementation
in C++.

    // C based program to implement reverse DNS lookup
    #include<stdio.h>
    #include<stdlib.h>
    #include<string.h>

    // There are atmost 11 different chars in a valid IP address
    #define CHARS 11

    // Maximum length of a valid IP address
    #define MAX 50

    // A utility function to find index of child for a given character 'c'
    int getIndex(char c) { return (c == '.')? 10: (c - '0'); }

    // A utility function to find character for a given child index.
    char getCharFromIndex(int i) { return (i== 10)? '.' : ('0' + i); }

    // Trie Node.
    struct trieNode
    {
        bool isLeaf;
        char *URL;
        struct trieNode *child[CHARS];
    };

    // Function to create a new trie node.
    struct trieNode *newTrieNode(void)
    {
        struct trieNode *newNode = new trieNode;
        newNode->isLeaf = false;
        newNode->URL = NULL;
        for (int i=0; i<CHARS; i++)
            newNode->child[i] = NULL;
        return newNode;
    }

    // This method inserts an ip address and the corresponding
    // domain name in the trie. The last node in Trie contains the URL.
    void insert(struct trieNode *root, char *ipAdd, char *URL)
    {
        // Length of the ip address
        int len = strlen(ipAdd);
        struct trieNode *pCrawl = root;

        // Traversing over the length of the ip address.
        for (int level=0; level<len; level++)
        {
            // Get index of child node from current character
            // in ipAdd[].  Index must be from 0 to 10 where
            // 0 to 9 is used for digits and 10 for dot
            int index = getIndex(ipAdd[level]);

            // Create a new child if not exist already
            if (!pCrawl->child[index])
                pCrawl->child[index] = newTrieNode();

            // Move to the child
            pCrawl = pCrawl->child[index];
        }

        //Below needs to be carried out for the last node.
        //Save the corresponding URL of the ip address in the
        //last node of trie.
        pCrawl->isLeaf = true;
        pCrawl->URL = new char[strlen(URL) + 1];
        strcpy(pCrawl->URL, URL);
    }

    // This function returns URL if given IP address is present in DNS cache.
    // Else returns NULL
    char  *searchDNSCache(struct trieNode *root, char *ipAdd)
    {
        // Root node of trie.
        struct trieNode *pCrawl = root;
        int  len = strlen(ipAdd);

        // Traversal over the length of ip address.
        for (int level=0; level<len; level++)
        {
            int index = getIndex(ipAdd[level]);
            if (!pCrawl->child[index])
                return NULL;
            pCrawl = pCrawl->child[index];
        }

        // If we find the last node for a given ip address, print the URL.
        if (pCrawl!=NULL && pCrawl->isLeaf)
            return pCrawl->URL;

        return NULL;
    }

    //Driver function.
    int main()
    {
        /* Change third ipAddress for validation */
        char ipAdd[][MAX] = {"107.108.11.123", "107.109.123.255",
                             "74.125.200.106"};
        char URL[][50] = {"www.samsung.com", "www.samsung.net",
                          "www.google.in"};
        int n = sizeof(ipAdd)/sizeof(ipAdd[0]);
        struct trieNode *root = newTrieNode();

        // Inserts all the ip address and their corresponding
        // domain name after ip address validation.
        for (int i=0; i<n; i++)
            insert(root,ipAdd[i],URL[i]);

        // If reverse DNS look up succeeds print the domain
        // name along with DNS resolved.
        char ip[] = "107.108.11.123";
        char *res_url = searchDNSCache(root, ip);
        if (res_url != NULL)
            printf("Reverse DNS look up resolved in cache:\n%s --> %s",
                    ip, res_url);
        else
            printf("Reverse DNS look up not resolved in cache ");
        return 0;
    }

Output:

    Reverse DNS look up resolved in cache:
    107.108.11.123 --> www.samsung.com

Note that the above implementation of Trie assumes that the given IP
address does not contain characters other than {‘0′, ‘1’,….. ‘9’, ‘.’}.
What if a user gives an invalid IP address that contains some other
characters? This problem can be resolved by [validating the input IP
address](http://www.geeksforgeeks.org/program-to-validate-an-ip-address/)
before inserting it into Trie. We can use the approach discussed
[here](http://www.geeksforgeeks.org/program-to-validate-an-ip-address/)for
IP address validation.

This article is contributed by **Kumar Gautam**. Please write comments
if you find anything incorrect, or you want to share more information
about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/implement-reverse-dns-look-cache/>

Interval Tree
-------------

Consider a situation where we have a set of intervals and we need
following operations to be implemented efficiently. <span
id="more-125741"></span>  
 **1)** Add an interval  
 **2)** Remove an interval  
 **3)** Given an interval x, find if x overlaps with any of the existing
intervals.

***Interval Tree:*** The idea is to augment a self-balancing Binary
Search Tree (BST) like [Red Black
Tree](http://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/),
[AVL Tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/), etc
to maintain set of intervals so that all operations can be done in
O(Logn) time.

Every node of Interval Tree stores following information.  
 a) **i**: An interval which is represented as a pair *[low, high]*  
 b) **max**: Maximum *high* value in subtree rooted with this node.

The low value of an interval is used as key to maintain order in BST.
The insert and delete operations are same as insert and delete in
self-balancing BST used.

[![IntervalSearcTree](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/IntervalSearcTree.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/IntervalSearcTree.png)

The main operation is to search for an overlapping interval. Following
is algorithm for searching an overlapping interval *x* in an Interval
tree rooted with *root*.

    Interval overlappingIntervalSearch(root, x)
    1) If x overlaps with root's interval, return the root's interval.

    2) If left child of root is not empty and the max  in left child 
    is greater than x's low value, recur for left child

    3) Else recur for right child.

***How does the above algorithm work?***  
 Let the interval to be searched be x. We need to prove this in for
following two cases.

***Case 1:*** *When we go to right subtree, one of the following must be
true.*  
 a) There is an overlap in right subtree: This is fine as we need to
return one overlapping interval.  
 b) There is no overlap in either subtree: We go to right subtree only
when either left is NULL or maximum value in left is smaller than
*x.low*. So the interval cannot be present in left subtree.

***Case 2:*** *When we go to left subtree, one of the following must be
true.*  
 a) There is an overlap in left subtree: This is fine as we need to
return one overlapping interval.  
 b) There is no overlap in either subtree: This is the most important
part. We need to consider following facts.  
 … We went to left subtree because *x.low in left subtree  
 …. max in left subtree is a high of one of the intervals let us say
*[a, max]* in left subtree.  
 …. Since *x* doesn’t overlap with any node in left subtree *x.low* must
be smaller than ‘*a*‘.  
 …. All nodes in BST are ordered by low value, so all nodes in right
subtree must have low value greater than ‘*a*‘.  
 …. From above two facts, we can say all intervals in right subtree have
low value greater than *x.low*. So *x* cannot overlap with any interval
in right subtree.*

**Implementation of Interval Tree:**  
 Following is C++ implementation of Interval Tree. The implementation
uses basic [insert operation of
BST](http://geeksquiz.com/binary-search-tree-set-1-search-and-insertion/)
to keep things simple. Ideally it should be [insertion of AVL
Tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/) or
[insertion of Red-Black
Tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/). [Deletion
from BST](http://geeksquiz.com/binary-search-tree-set-2-delete/) is left
as an exercise.

    #include <iostream>
    using namespace std;

    // Structure to represent an interval
    struct Interval
    {
        int low, high;
    };

    // Structure to represent a node in Interval Search Tree
    struct ITNode
    {
        Interval *i;  // 'i' could also be a normal variable
        int max;
        ITNode *left, *right;
    };

    // A utility function to create a new Interval Search Tree Node
    ITNode * newNode(Interval i)
    {
        ITNode *temp = new ITNode;
        temp->i = new Interval(i);
        temp->max = i.high;
        temp->left = temp->right = NULL;
    };

    // A utility function to insert a new Interval Search Tree Node
    // This is similar to BST Insert.  Here the low value of interval
    // is used tomaintain BST property
    ITNode *insert(ITNode *root, Interval i)
    {
        // Base case: Tree is empty, new node becomes root
        if (root == NULL)
            return newNode(i);

        // Get low value of interval at root
        int l = root->i->low;

        // If root's low value is smaller, then new interval goes to
        // left subtree
        if (i.low < l)
            root->left = insert(root->left, i);

        // Else, new node goes to right subtree.
        else
            root->right = insert(root->right, i);

        // Update the max value of this ancestor if needed
        if (root->max < i.high)
            root->max = i.high;

        return root;
    }

    // A utility function to check if given two intervals overlap
    bool doOVerlap(Interval i1, Interval i2)
    {
        if (i1.low <= i2.high && i2.low <= i1.high)
            return true;
        return false;
    }

    // The main function that searches a given interval i in a given
    // Interval Tree.
    Interval *overlapSearch(ITNode *root, Interval i)
    {
        // Base Case, tree is empty
        if (root == NULL) return NULL;

        // If given interval overlaps with root
        if (doOVerlap(*(root->i), i))
            return root->i;

        // If left child of root is present and max of left child is
        // greater than or equal to given interval, then i may
        // overlap with an interval is left subtree
        if (root->left != NULL && root->left->max >= i.low)
            return overlapSearch(root->left, i);

        // Else interval can only overlap with right subtree
        return overlapSearch(root->right, i);
    }

    void inorder(ITNode *root)
    {
        if (root == NULL) return;

        inorder(root->left);

        cout << "[" << root->i->low << ", " << root->i->high << "]"
             << " max = " << root->max << endl;

        inorder(root->right);
    }

    // Driver program to test above functions
    int main()
    {
        // Let us create interval tree shown in above figure
        Interval ints[] = {{15, 20}, {10, 30}, {17, 19},
            {5, 20}, {12, 15}, {30, 40}
        };
        int n = sizeof(ints)/sizeof(ints[0]);
        ITNode *root = NULL;
        for (int i = 0; i < n; i++)
            root = insert(root, ints[i]);

        cout << "Inorder traversal of constructed Interval Tree is\n";
        inorder(root);

        Interval x = {6, 7};

        cout << "\nSearching for interval [" << x.low << "," << x.high << "]";
        Interval *res = overlapSearch(root, x);
        if (res == NULL)
            cout << "\nNo Overlapping Interval";
        else
            cout << "\nOverlaps with [" << res->low << ", " << res->high << "]";
        return 0;
    }

Output:

    Inorder traversal of constructed Interval Tree is
    [5, 20] max = 20
    [10, 30] max = 30
    [12, 15] max = 15
    [15, 20] max = 40
    [17, 19] max = 40
    [30, 40] max = 40

    Searching for interval [6,7]
    Overlaps with [5, 20]

**Applications of Interval Tree:**  
 Interval tree is mainly a geometric data structure and often used for
windowing queries, for instance, to find all roads on a computerized map
inside a rectangular viewport, or to find all visible elements inside a
three-dimensional scene (Source
[Wiki](http://en.wikipedia.org/wiki/Interval_tree)).

**Interval Tree vs [Segment
Tree](http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/)**  
 Both segment and interval trees store intervals. Segment tree is mainly
optimized for queries for a given point, and interval trees are mainly
optimized for overlapping queries for a given interval.

**Exercise:**  
 1) Implement delete operation for interval tree.  
 2) Extend the intervalSearch() to print all overlapping intervals
instead of just one.

<http://en.wikipedia.org/wiki/Interval_tree>  
 <http://www.cse.unr.edu/~mgunes/cs302/IntervalTrees.pptx>  
 [Introduction to Algorithms 3rd Edition by Clifford Stein, Thomas H.
Cormen, Charles E. Leiserson, Ronald L.
Rivest](http://www.flipkart.com/introduction-algorithms-3rd/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)  
 <https://www.youtube.com/watch?v=dQF0zyaym8A>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/interval-tree/>

K Dimensional Tree
------------------

A K-D Tree(also called as K-Dimensional Tree) is a binary search tree
where data in each node is a K-Dimensional point in space. <span
id="more-132156"></span>In short, it is a space partitioning(details
below) data structure for organizing points in a K-Dimensional space.

A non-leaf node in K-D tree divides the space into two parts, called as
half-spaces.

Points to the left of this space are represented by the left subtree of
that node and points to the right of the space are represented by the
right subtree. We will soon be explaining the concept on how the space
is divided and tree is formed.

For the sake of simplicity, let us understand a 2-D Tree with an
example.

The root would have an x-aligned plane, the root’s children would both
have y-aligned planes, the root’s grandchildren would all have x-aligned
planes, and the root’s great-grandchildren would all have y-aligned
planes and so on.

**Generalization:**  
 Let us number the planes as 0, 1, 2, â€¦(K â€“ 1). From the above
example, it is quite clear that a point (node) at depth D will have A
aligned plane where A is calculated as:

A = D mod K

**How to determine if a point will lie in the left subtree or in right
subtree?**

If the root node is aligned in planeA, then the left subtree will
contain all points whose coordinates in that plane are smaller than that
of root node. Similarly, the right subtree will contain all points whose
coordinates in that plane are greater-equal to that of root node.

**Creation of a 2-D Tree:**  
 Consider following points in a 2-D plane:  
 (3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)

1.  Insert (3, 6): Since tree is empty, make it the root node.
2.  Insert (17, 15): Compare it with root node point. Since root node is
    X-aligned, the X-coordinate value will be compared to determine if
    it lies in the rightsubtree or in the right subtree. This point will
    be Y-aligned.
3.  Insert (13, 15): X-value of this point is greater than X-value of
    point in root node. So, this will lie in the right subtree of (3,
    6). Again Compare Y-value of this point with the Y-value of point
    (17, 15) (Why?). Since, they are equal, this point will lie in the
    right subtree of (17, 15). This point will be X-aligned.
4.  Insert (6, 12): X-value of this point is greater than X-value of
    point in root node. So, this will lie in the right subtree of (3,
    6). Again Compare Y-value of this point with the Y-value of point
    (17, 15) (Why?). Since, 12 \< 15, this point will lie in the left
    subtree of (17, 15). This point will be X-aligned.
5.  Insert (9, 1):Similarly, this point will lie in the right of (6,
    12).
6.  Insert (2, 7):Similarly, this point will lie in the left of (3, 6).
7.  Insert (10, 19): Similarly, this point will lie in the left of (13,
    15).

[![1](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/11.jpg)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/11.jpg)

**How is space partitioned?**  
 All 7 points will be plotted in the X-Y plane as follows:

1.  Point (3, 6) will divide the space into two parts: Draw line X =
    3.  

    [![Figure3](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure3.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure3.png)
2.  Point (2, 7) will divide the space to the left of line X = 3 into
    two parts horizontally.  
     Draw line Y = 7 to the left of line X = 3.  

    [![Figure4](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure4.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure4.png)
3.  Point (17, 15) will divide the space to the right of line X = 3 into
    two parts horizontally.  
     Draw line Y = 15 to the right of line X = 3.  

    [![Figure5](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure5.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure5.png)

 

-   Point (6, 12) will divide the space below line Y = 15 and to the
    right of line X = 3 into two parts.  
     Draw line X = 6 to the right of line X = 3 and below line Y = 15.  

    [![Figure6](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure6.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure6.png)

 

-   Point (13, 15) will divide the space below line Y = 15 and to the
    right of line X = 6 into two parts.  
     Draw line X = 13 to the right of line X = 6 and below line Y =
    15.  

    [![Figure7](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure7.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure7.png)
-   Point (9, 1) will divide the space between lines X = 3, X = 6 and Y
    = 15 into two parts.  
     Draw line Y = 1 between lines X = 3 and X = 6.  

    [![Figure8](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure8.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure8.png)
-   Point (10, 19) will divide the space to the right of line X = 3 and
    above line Y = 15 into two parts.  
     Draw line Y = 19 to the right of line X = 3 and above line Y =
    15.  

    [![Figure9](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure9.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Figure9.png)

Following is C++ implementation of KD Tree basic operations like search,
insert and delete.

    // A C++ program to demonstrate operations of KD tree
    #include <iostream>
    #include <cstdio>
    #include <cassert>
    #include <cstdlib>
    using namespace std;

    // A structure to represent a point in K dimensional space
    // k: K dimensional space
    // coord: An array to represent position of point
    struct Point
    {
        unsigned k;
        int* coord; // Coordinate (A pointer to array of size k)
    };

    // A structure to represent the Input
    // n: Number of points in space
    // pointArray: An array to keep information of each point
    struct Input
    {
        // n --> NUMBER OF POINTS
        unsigned n;
        Point* *pointArray;
    };

    // A structure to represent node of 2 dimensional tree
    struct Node
    {
        Point point;
        Node *left, *right;
    };

    // Creates and return a Point structure
    Point* CreatePoint(unsigned k)
    {
        Point* point = new Point;

        // Memory allocation failure
        assert(NULL != point);

        point->k = k;
        point->coord = new int[k];

        // Memory allocation failure
        assert(NULL != point->coord);

        return point;
    }

    // Creates and returns an Input structure
    struct Input* CreateInput(unsigned k, unsigned n)
    {
        struct Input* input = new Input;

        // Memory allocation failure
        assert(NULL != input);

        input->n = n;
        input->pointArray = new Point*[n];

        // Memory allocation failure
        assert(NULL != input->pointArray);

        return input;
    }

    // A method to create a node of K D tree
    struct Node* CreateNode(struct Point* point)
    {
        struct Node* tempNode = new Node;

        // Memory allocation failure
        assert(NULL != tempNode);

        // Avoid shallow copy [We could have directly use
        // the below assignment, But didn't, why?]
        /*tempNode->point = point;*/
        (tempNode->point).k = point->k;
        (tempNode->point).coord = new int[point->k];

        // Copy coordinate values
        for (int i=0; i<(tempNode->point).k; ++i)
            (tempNode->point).coord[i] = point->coord[i];

        tempNode->left = tempNode->right = NULL;
        return tempNode;
    }

    // Root is passed as pointer to pointer so that
    // The parameter depth is used to decide axis of comparison
    void InsertKDTreeUtil(Node * * root, Node* newNode, unsigned depth)
    {
        // Tree is empty?
        if (!*root)
        {
            *root = newNode;
            return;
        }

        // Calculate axis of comparison to determine left/right
        unsigned axisOfComparison = depth % (newNode->point).k;

        // Compare the new point with root and decide the left or
        // right subtree
        if ((newNode->point).coord[axisOfComparison] <
                        ((*root)->point).coord[axisOfComparison])
            InsertKDTreeUtil(&((*root)->left), newNode, depth + 1);
        else
            InsertKDTreeUtil(&((*root)->right), newNode, depth + 1);
    }

    // Function to insert a new point in KD Tree. It mainly uses
    // above recursive function "InsertKDTreeUtil()"
    void InsertKDTree(Node* *root, Point* point)
    {
        Node* newNode = CreateNode(point);
        unsigned zeroDepth = 0;
        InsertKDTreeUtil(root, newNode, zeroDepth);
    }

    // A utility method to determine if two Points are same
    // in K Dimensional space
    int ArePointsSame(Point firstPoint, Point secondPoint)
    {
        if (firstPoint.k != secondPoint.k)
            return 0;

        // Compare individual coordinate values
        for (int i = 0; i < firstPoint.k; ++i)
            if (firstPoint.coord[i] != secondPoint.coord[i])
                return 0;

        return 1;
    }

    // Searches a Point in the K D tree. The parameter depth is used
    // to determine current axis.
    int SearchKDTreeUtil(Node* root, Point point, unsigned depth)
    {
        if (!root)
            return 0;

        if (ArePointsSame(root->point, point))
            return 1;

        unsigned axisOfComparison = depth % point.k;

        if (point.coord[axisOfComparison] <
                          (root->point).coord[axisOfComparison])
            return SearchKDTreeUtil(root->left, point, depth + 1);

        return SearchKDTreeUtil(root->right, point, depth + 1);
    }

    // Searches a Point in the K D tree. It mainly uses
    // SearchKDTreeUtil()
    int SearchKDTree(Node* root, Point point)
    {
        unsigned zeroDepth = 0;
        return SearchKDTreeUtil(root, point, zeroDepth);
    }

    // Creates a KD tree from given input points. It mainly
    // uses InsertKDTree
    Node* CreateKDTree(Input* input)
    {
        Node* root = NULL;
        for (int i = 0; i < input->n; ++i)
            InsertKDTree(&root, input->pointArray[i]);
        return root;
    }

    // A utility function to print an array
    void PrintArray(int* array, unsigned size)
    {
        for (unsigned i = 0; i < size; ++i)
            cout << array[i];
        cout << endl;
    }

    // A utility function to do inorder tree traversal
    void inorderKD(Node* root)
    {
        if (root)
        {
            inorderKD(root->left);
            PrintArray((root->point).coord, (root->point).k);
            inorderKD(root->right);
        }
    }

    // Driver program to test above functions
    int main()
    {
        // 2 Dimensional tree [For the sake of simplicity]
        unsigned k = 2;

        // Total number of Points is 7
        unsigned n = 7;
        Input* input = CreateInput(k, n);

        // itc --> ITERATOR for coord
        // itp --> ITERATOR for POINTS
        for (int itp = 0; itp < n; ++itp)
        {
            input->pointArray[itp] = CreatePoint(k);

            for (int itc = 0; itc < k; ++itc)
                input->pointArray[itp]->coord[itc] = rand() % 20;

            PrintArray(input->pointArray[itp]->coord, k);
        }

        Node* root = CreateKDTree(input);

        cout << "Inorder traversal of K-D Tree created is:\n";
        inorderKD(root);

        return 0;
    }
     

Output:

    17
    140
    94
    1818
    24
    55
    17
    Inorder traversal of K-D Tree created is:
    17
    140
    24
    17
    55
    94
    1818

This article is compiled by [**Aashish
Barnwal**](http://facebook.com/barnwal.aashish). Please write comments
if you find anything incorrect, or you want to share more information
about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/k-dimensional-tree/>

Longest prefix matching – A Trie based solution in Java
-------------------------------------------------------

Given a dictionary of words and an input string, find the longest prefix
of the string which is also a word in dictionary.<span
id="more-117275"></span>

**Examples:**

    Let the dictionary contains the following words:
    {are, area, base, cat, cater, children, basement}

    Below are some input/output examples:
    --------------------------------------
    Input String            Output
    --------------------------------------
    caterer                 cater
    basemexy                base
    child                   

**Solution**  
 We build a Trie of all dictionary words. Once the Trie is built,
traverse through it using characters of input string. If prefix matches
a dictionary word, store current length and look for a longer match.
Finally, return the longest match.  
 Following is Java implementation of the above solution based.

    import java.util.HashMap;
      
    // Trie Node, which stores a character and the children in a HashMap
    class TrieNode {           
        public TrieNode(char ch)  {
            value = ch;
            children = new HashMap<>();
            bIsEnd = false;
        }    
        public HashMap<Character,TrieNode> getChildren() {   return children;  }    
        public char getValue()                           {   return value;     }    
        public void setIsEnd(boolean val)                {   bIsEnd = val;     }    
        public boolean isEnd()                           {   return bIsEnd;    }
          
        private char value;    
        private HashMap<Character,TrieNode> children;
        private boolean bIsEnd;  
    }
      
    // Implements the actual Trie
    class Trie {        
        // Constructor
        public Trie()   {     root = new TrieNode((char)0);       }    
      
        // Method to insert a new word to Trie
        public void insert(String word)  {
              
            // Find length of the given word
            int length = word.length();        
            TrieNode crawl = root;
              
            // Traverse through all characters of given word
            for( int level = 0; level < length; level++)
            {
                HashMap<Character,TrieNode> child = crawl.getChildren();            
                char ch = word.charAt(level);
                  
                // If there is already a child for current character of given word 
                if( child.containsKey(ch))
                    crawl = child.get(ch);
                else   // Else create a child
                {              
                    TrieNode temp = new TrieNode(ch);
                    child.put( ch, temp );
                    crawl = temp;
                }
            }
              
            // Set bIsEnd true for last character
            crawl.setIsEnd(true);
        }
          
        // The main method that finds out the longest string 'input'
        public String getMatchingPrefix(String input)  {
            String result = ""; // Initialize resultant string
            int length = input.length();  // Find length of the input string       
              
            // Initialize reference to traverse through Trie
            TrieNode crawl = root;   
             
            // Iterate through all characters of input string 'str' and traverse 
            // down the Trie
            int level, prevMatch = 0; 
            for( level = 0 ; level < length; level++ )
            {    
                // Find current character of str
                char ch = input.charAt(level);    
                 
                // HashMap of current Trie node to traverse down
                HashMap<Character,TrieNode> child = crawl.getChildren();                        
                
                // See if there is a Trie edge for the current character
                if( child.containsKey(ch) )
                {
                   result += ch;          //Update result
                   crawl = child.get(ch); //Update crawl to move down in Trie
                    
                   // If this is end of a word, then update prevMatch
                   if( crawl.isEnd() ) 
                        prevMatch = level + 1;
                }            
                else  break;
            }
             
            // If the last processed character did not match end of a word, 
            // return the previously matching prefix
            if( !crawl.isEnd() )
                    return result.substring(0, prevMatch);        
            
            else return result;
        }
          
        private TrieNode root;      
    }
      
    // Testing class
    public class Test {
       public static void main(String[] args) {
            Trie dict = new Trie();        
            dict.insert("are");
            dict.insert("area");
            dict.insert("base");
            dict.insert("cat");
            dict.insert("cater");        
            dict.insert("basement");
            
            String input = "caterer";
            System.out.print(input + ":   ");
            System.out.println(dict.getMatchingPrefix(input));              

            input = "basement";
            System.out.print(input + ":   ");
            System.out.println(dict.getMatchingPrefix(input));                      
            
            input = "are";
            System.out.print(input + ":   ");
            System.out.println(dict.getMatchingPrefix(input));              

            input = "arex";
            System.out.print(input + ":   ");
            System.out.println(dict.getMatchingPrefix(input));              

            input = "basemexz";
            System.out.print(input + ":   ");
            System.out.println(dict.getMatchingPrefix(input));                      
            
            input = "xyz";
            System.out.print(input + ":   ");
            System.out.println(dict.getMatchingPrefix(input));                      
        }
    }

Output:

    caterer:   cater
    basement:   basement
    are:   are
    arex:   are
    basemexz:   base
    xyz:   

Time Complexity: Time complexity of finding the longest prefix is O(n)
where n is length of the input string. Refer
[this](http://www.geeksforgeeks.org/trie-insert-and-search/)for time
complexity of building the Trie.

This article is compiled by **Ravi Chandra Enaganti**. Please write
comments if you find anything incorrect, or you want to share more
information about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Java](http://www.geeksforgeeks.org/tag/java/)

### Source:

<http://www.geeksforgeeks.org/longest-prefix-matching-a-trie-based-solution-in-java/>

Pattern Searching | Set 8 (Suffix Tree Introduction)
----------------------------------------------------

Given a text txt[0..n-1] and a pattern pat[0..m-1], write a function
search(char pat[], char txt[]) that prints all occurrences of pat[] in
txt[]. You may assume that n \> m.<span id="more-29117"></span>

**Preprocess Pattern or Preoprocess Text?**  
 We have discussed the following algorithms in the previous posts:

[KMP Algorithm](http://www.geeksforgeeks.org/archives/11902)  
 [Rabin Karp Algorithm](http://www.geeksforgeeks.org/archives/11937)  
 [Finite Automata based
Algorithm](http://www.geeksforgeeks.org/archives/18919)  
 [Boyer Moore
Algorithm](http://www.geeksforgeeks.org/pattern-searching-set-7-boyer-moore-algorithm-bad-character-heuristic/)

All of the above algorithms preprocess the pattern to make the pattern
searching faster. The best time complexity that we could get by
preprocessing pattern is O(n) where n is length of the text. In this
post, we will discuss an approach that preprocesses the text. A suffix
tree is built of the text. After preprocessing text (building suffix
tree of text), we can search any pattern in O(m) time where m is length
of the pattern.  
 Imagine you have stored complete work of [William
Shakespeare](http://en.wikipedia.org/wiki/William_Shakespeare) and
preprocessed it. You can search any string in the complete work in time
just proportional to length of the pattern. This is really a great
improvement because length of pattern is generally much smaller than
text.  
 Preprocessing of text may become costly if the text changes frequently.
It is good for fixed text or less frequently changing text though.

**A Suffix Tree for a given text is a compressed trie for all suffixes
of the given text**. We have discussed [Standard
Trie](http://www.geeksforgeeks.org/trie-insert-and-search/). Let us
understand **Compressed Trie** with the following array of words.

    {bear, bell, bid, bull, buy, sell, stock, stop}

Following is standard trie for the above input set of words.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/standardtrieNew.png "standardtrie")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/standardtrie.png)

Following is the compressed trie. Compress Trie is obtained from
standard trie by joining chains of single nodes. The nodes of a
compressed trie can be stored by storing index ranges at the nodes.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/CompressedTrieNew.png "Compressed Trie")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Compressed-Trie.png)

**How to build a Suffix Tree for a given text?**  
 As discussed above, Suffix Tree is compressed trie of all suffixes, so
following are very abstract steps to build a suffix tree from given
text.  
 1) Generate all suffixes of given text.  
 2) Consider all suffixes as individual words and build a compressed
trie.

Let us consider an example text “banana\\0″ where ‘\\0′ is string
termination character. Following are all suffixes of “banana\\0″

    banana\0
    anana\0
    nana\0
    ana\0
    na\0
    a\0
    \0

If we consider all of the above suffixes as individual words and build a
trie, we get following.  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/suffixtrie.png "suffixtrie")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/suffixtrie.png)

If we join chains of single nodes, we get the following compressed trie,
which is the Suffix Tree for given text “banana\\0″  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/suffix-tree.png "suffix tree")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/suffix-tree.png)

Please note that above steps are just to manually create a Suffix Tree.
We will be discussing actual algorithm and implementation in a separate
post.

**How to search a pattern in the built suffix tree?**  
 We have discussed above how to build a Suffix Tree which is needed as a
preprocessing step in pattern searching. Following are abstract steps to
search a pattern in the built Suffix Tree.  
 **1)** Starting from the first character of the pattern and root of
Suffix Tree, do following for every character.  
 …..**a)** For the current character of pattern, if there is an edge
from the current node of suffix tree, follow the edge.  
 …..**b)** If there is no edge, print “pattern doesn’t exist in text”
and return.  
 **2)** If all characters of pattern have been processed, i.e., there is
a path from root for characters of the given pattern, then print
“Pattern found”.

Let us consider the example pattern as “nan” to see the searching
process. Following diagram shows the path followed for searching “nan”
or “nana”.

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/suffixTreeSearch.png "suffixTreeSearch")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/suffixTreeSearch.png)

**How does this work?**  
 Every pattern that is present in text (or we can say every substring of
text) must be a prefix of one of all possible suffixes. The statement
seems complicated, but it is a simple statement, we just need to take an
example to check validity of it.

**Applications of Suffix Tree**  
 Suffix tree can be used for a wide range of problems. Following are
some famous problems where Suffix Trees provide optimal time complexity
solution.  
 1) Pattern Searching  
 2) [Finding the longest repeated
substring](http://en.wikipedia.org/wiki/Longest_repeated_substring_problem)  
 3) [Finding the longest common
substring](http://en.wikipedia.org/wiki/Longest_common_substring_problem)  
 4) [Finding the longest palindrome in a
string](http://en.wikipedia.org/wiki/Longest_palindromic_substring)

There are many more applications. See
[this](http://en.wikipedia.org/wiki/Suffix_tree#Functionality)for more
details.

Ukkonenâ€™s Suffix Tree Construction is discussed in following
articles:  
 [Ukkonenâ€™s Suffix Tree Construction â€“ Part
1](http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-1/ "Ukkonenâs Suffix Tree Construction â Part 1")  
 [Ukkonenâ€™s Suffix Tree Construction â€“ Part
2](http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-2/ "Ukkonenâs Suffix Tree Construction â Part 2")  
 [Ukkonenâ€™s Suffix Tree Construction â€“ Part
3](http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-3/ "Ukkonenâs Suffix Tree Construction â Part 3")  
 [Ukkonenâ€™s Suffix Tree Construction â€“ Part
4](http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-4/ "Ukkonenâs Suffix Tree Construction â Part 4")  
 [Ukkonenâ€™s Suffix Tree Construction â€“ Part
5](http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-5/ "Ukkonenâs Suffix Tree Construction â Part 5")  
 [Ukkonenâ€™s Suffix Tree Construction â€“ Part
6](http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-6/ "Ukkonenâs Suffix Tree Construction â Part 6")

**References:**  

<http://fbim.fh-regensburg.de/~saj39122/sal/skript/progr/pr45102/Tries.pdf>  
 <http://www.cs.ucf.edu/~shzhang/Combio12/lec3.pdf>  
 <http://www.allisons.org/ll/AlgDS/Tree/Suffix/>

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/),
[Pattern Searching](http://www.geeksforgeeks.org/tag/pattern-searching/)

### Source:

<http://www.geeksforgeeks.org/pattern-searching-set-8-suffix-tree-introduction/>

Print unique rows in a given boolean matrix
-------------------------------------------

Given a binary matrix, print all unique rows of the given matrix. <span
id="more-24561"></span>

    Input:
        {0, 1, 0, 0, 1}
            {1, 0, 1, 1, 0}
            {0, 1, 0, 0, 1}
            {1, 1, 1, 0, 0}
    Output:
        0 1 0 0 1 
        1 0 1 1 0 
        1 1 1 0 0 

**Method 1 (Simple)**  
 A simple approach is to check each row with all processed rows. Print
the first row. Now, starting from the second row, for each row, compare
the row with already processed rows. If the row matches with any of the
processed rows, don’t print it. If the current row doesn’t match with
any row, print it.

Time complexity: O( ROW^2 x COL )  
 Auxiliary Space: O( 1 )

**Method 2 (Use Binary Search Tree)**  
 Find the decimal equivalent of each row and insert it into BST. Each
node of the BST will contain two fields, one field for the decimal
value, other for row number. Do not insert a node if it is duplicated.
Finally, traverse the BST and print the corresponding rows.

Time complexity: O( ROW x COL + ROW x log( ROW ) )  
 Auxiliary Space: O( ROW )

This method will lead to Integer Overflow if number of columns is large.

**Method 3 (Use Trie data structure)**  
 Since the matrix is boolean, a variant of Trie data structure can be
used where each node will be having two children one for 0 and other for
1. Insert each row in the Trie. If the row is already there, don’t print
the row. If row is not there in Trie, insert it in Trie and print it.

Below is C implementation of method 3.

    //Given a binary matrix of M X N of integers, you need to return only unique rows of binary array
    #include <stdio.h>
    #include <stdlib.h>
    #include <stdbool.h>

    #define ROW 4
    #define COL 5

    // A Trie node
    typedef struct Node
    {
        bool isEndOfCol;
        struct Node *child[2]; // Only two children needed for 0 and 1
    } Node;


    // A utility function to allocate memory for a new Trie node
    Node* newNode()
    {
        Node* temp = (Node *)malloc( sizeof( Node ) );
        temp->isEndOfCol = 0;
        temp->child[0] = temp->child[1] = NULL;
        return temp;
    }

    // Inserts a new matrix row to Trie.  If row is already
    // present, then returns 0, otherwise insets the row and
    // return 1
    bool insert( Node** root, int (*M)[COL], int row, int col )
    {
        // base case
        if ( *root == NULL )
            *root = newNode();

        // Recur if there are more entries in this row
        if ( col < COL )
            return insert ( &( (*root)->child[ M[row][col] ] ), M, row, col+1 );

        else // If all entries of this row are processed
        {
            // unique row found, return 1
            if ( !( (*root)->isEndOfCol ) )
                return (*root)->isEndOfCol = 1;

            // duplicate row found, return 0
            return 0;
        }
    }

    // A utility function to print a row
    void printRow( int (*M)[COL], int row )
    {
        int i;
        for( i = 0; i < COL; ++i )
            printf( "%d ", M[row][i] );
        printf("\n");
    }

    // The main function that prints all unique rows in a
    // given matrix.
    void findUniqueRows( int (*M)[COL] )
    {
        Node* root = NULL; // create an empty Trie
        int i;

        // Iterate through all rows
        for ( i = 0; i < ROW; ++i )
            // insert row to TRIE
            if ( insert(&root, M, i, 0) )
                // unique row found, print it
                printRow( M, i );
    }

    // Driver program to test above functions
    int main()
    {
        int M[ROW][COL] = {{0, 1, 0, 0, 1},
            {1, 0, 1, 1, 0},
            {0, 1, 0, 0, 1},
            {1, 0, 1, 0, 0}
        };

        findUniqueRows( M );

        return 0;
    }

Time complexity: O( ROW x COL )  
 Auxiliary Space: O( ROW x COL )

This method has better time complexity. Also, relative order of rows is
maintained while printing.

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/print-unique-rows/>

Red-Black Tree | Set 1 (Introduction)
-------------------------------------

Red-Black Tree is a self-balancing Binary Search Tree (BST) where every
node follows following rules.<span id="more-125964"></span>  

[![RedBlackTree](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/RedBlackTree.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/RedBlackTree.png)  
 **1)** Every node has a color either red or black.

**2)** Root of tree is always black.

**3)** There are no two adjacent red nodes (A red node cannot have a red
parent or red child).

**4)** Every path from root to a NULL node has same number of black
nodes.

**Why Red-Black Trees?**  
 Most of the BST operations (e.g., search, max, min, insert, delete..
etc) take O(h) time where h is the height of the BST. The cost of these
operations may become O(n) for a skewed Binary tree. If we make sure
that height of the tree remains O(Logn) after every insertion and
deletion, then we can guarantee an upper bound of O(Logn) for all these
operations. The height of a Red Black tree is always O(Logn) where n is
the number of nodes in the tree.

**Comparison with[AVL
Tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/)**  
 The AVL trees are more balanced compared to Red Black Trees, but they
may cause more rotations during insertion and deletion. So if your
application involves many frequent insertions and deletions, then Red
Black trees should be preferred. And if the insertions and deletions are
less frequent and search is more frequent operation, then AVL tree
should be preferred over Red Black Tree.

**How does a Red-Black Tree ensure balance?**  
 A simple example to understand balancing is, a chain of 3 nodes is not
possible in red black tree. We can try any combination of colors and see
all of them violate Red-Black tree property.

    A chain of 3 nodes is nodes is not possible in Red-Black Trees.
    Following are NOT Red-Black Trees
            30             30               30       
           / \            /  \             /  \
         20  NIL         20   NIL         20   NIL
        / \             / \              /  \
      10  NIL          10  NIL          10  NIL
    Violates          Violates        Violates
    Property 4.      Property 4       Property 3

    Following are different possible Red-Black Trees with above 3 keys
             20                           20
           /   \                        /   \
         10     30                    10     30
        /  \   /  \                 /  \    /  \
     NIL  NIL NIL NIL             NIL  NIL NIL NIL

*  
* From the above examples, we get some idea how Red-Black trees ensure
balance. Following is an important fact about balancing in Red-Black
Trees.*  
 **  
 Every Red Black Tree with **n** nodes has height \<=***
![2\\log\_2(n+1)](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-24ee68d811af592ded4217a4f755a02b_l3.png "Rendered by QuickLaTeX.com")

This can be proved using following facts:  
 1) For a general Binary Tree, let **k** be the minimum number of nodes
on all root to NULL paths, then n \>= 2<sup>k</sup> – 1 (Ex. If k is 3,
then n is atleast 7). This expression can also be written as k
\<=![2\\log\_2(n+1)](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-24ee68d811af592ded4217a4f755a02b_l3.png "Rendered by QuickLaTeX.com")

2) From property 4 of Red-Black trees and above claim, we can say in a
Red-Black Tree with n nodes, there is a root to leaf path with at-most
![\\log\_2(n+1)](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-26bfcc79e12ab13a01cb78305538b87f_l3.png "Rendered by QuickLaTeX.com")
black nodes.

3) From property 3 of Red-Black trees, we can claim that the number
black nodes in a Red-Black tree is at least ![\\lfloor n/2
\\rfloor](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-ea53c7e192b148cdd15fc823d6c642d8_l3.png "Rendered by QuickLaTeX.com")
where n is total number of nodes.

From above 2 points, we can conclude the fact that Red Black Tree with
**n** nodes has height \<=
![2\\log\_2(n+1)](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-24ee68d811af592ded4217a4f755a02b_l3.png "Rendered by QuickLaTeX.com")

In this post, we introduced Red-Black trees and discussed how balance is
ensured. The hard part is to maintain balance when keys are added and
removed. We will soon be discussing insertion and deletion operations in
coming posts on Red-Black tree.

**Exercise:**  
 **1)** Is it possible to have all black nodes in a Red-Black tree?  
 **2)** Draw a Red-Black Tree that is not an [AVL
tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/) structure
wise?

**Insertion and Deletion**  
 [Red Black Tree
Insertion](http://www.geeksforgeeks.org/red-black-tree-set-2-insert/)  
 [Red-Black Tree
Deletion](http://www.geeksforgeeks.org/red-black-tree-set-3-delete-2/)

**References:**  
 [Introduction to Algorithms 3rd Edition by Clifford Stein, Thomas H.
Cormen, Charles E. Leiserson, Ronald L.
Rivest](http://www.flipkart.com/introduction-algorithms-3/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)  
 <http://en.wikipedia.org/wiki/Red%E2%80%93black_tree>  
 [Video Lecture on Red-Black Tree by Tim
Roughgarden](http://www.youtube.com/watch?v=4slgC3UOXc0http://)  
 [MIT Video Lecture on Red-Black
Tree](http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-introduction-to-algorithms-sma-5503-fall-2005/video-lectures/lecture-10-red-black-trees-rotations-insertions-deletions/)  
 [MIT Lecture Notes on Red Black
Tree](http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-introduction-to-algorithms-sma-5503-fall-2005/video-lectures/lecture-10-red-black-trees-rotations-insertions-deletions/lec10.pdf)

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/>

Red-Black Tree | Set 2 (Insert)
-------------------------------

In the [previous
post](http://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/),
we discussed introduction to Red-Black Trees. In this post, insertion is
discussed.<span id="more-126793"></span>

In[AVL tree
insertion](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/), we
used rotation as a tool to do balancing after insertion caused
imbalance. In Red-Black tree, we use two tools to do balancing.

**1)** Recoloring  
 **2)** [Rotation](http://en.wikipedia.org/wiki/Tree_rotation)

We try recoloring first, if recoloring doesn’t work, then we go for
rotation. Following is detailed algorithm. The algorithms has mainly two
cases depending upon the color of uncle. If uncle is red, we do
recoloring. If uncle is black, we do rotations and/or recoloring.

Color of a NULL node is considered as BLACK.

Let x be the newly inserted node.  
 **1)** Perform [standard BST
insertion](http://geeksquiz.com/binary-search-tree-set-1-search-and-insertion/)
and make the color of newly inserted nodes as RED.

**2)** Do following if color of x’s parent is not BLACK or x is not
root.  
 ….**a)** **If x’s uncle is** **<span>RED</span>** (Grand parent must
have been black from [property
4](http://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/))  
 ……..**(i)** Change color of parent and uncle as BLACK.  
 ……..**(ii)** color of grand parent as RED.  
 ……..**(iii)** Change x = x’s grandparent, repeat steps 2 and 3 for new
x.  

[![redBlackCase2](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase2.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase2.png)

….**b)** **If x’s uncle is BLACK**, then there can be four
configurations for x, x’s parent (**p**) and x’s grandparent (**g**)
(This is similar to[AVL
Tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/))  
 ……..**i)** Left Left Case (p is left child of g and x is left child of
p)  
 ……..**ii)** Left Right Case (p is left child of g and x is right child
of p)  
 ……..**iii)** Right Right Case (Mirror of case a)  
 ……..**iv)** Right Left Case (Mirror of case c)

**3)** If x is root, change color of x as BLACK (Black height of
complete tree increases by 1).

Following are operations to be performed in four subcases when uncle is
BLACK.

All four cases when Uncle is BLACK
----------------------------------

**Left Left Case (See g, p and x)**  

[![redBlackCase3a](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3a1.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3a1.png)

**Left Right Case (See g, p and x)**  

[![redBlackCase3b](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3b.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3b.png)

**Right Right Case (See g, p and x)**  

[![redBlackCase3c](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3c.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3c.png)

**Right Left Case (See g, p and x)**  

[![redBlackCase3d](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3d.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/redBlackCase3d.png)

Examples of Insertion
---------------------

[![Examples](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Examples_new.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Examples.png)

Please refer [C Program for Red Black Tree
Insertion](http://geeksquiz.com/c-program-red-black-tree-insertion/) for
complete implementation of above algorithm.

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/red-black-tree-set-2-insert/>

Red-Black Tree | Set 3 (Delete)
-------------------------------

We have discussed following topics on Red-Black tree in previous posts.
We strongly recommend to refer following post as prerequisite of this
post.<span id="more-126866"></span>

[Red-Black Tree
Introduction](http://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/)  
 [Red Black Tree
Insert](http://www.geeksforgeeks.org/red-black-tree-set-2-insert/)

**Insertion Vs Deletion:**  
 Like Insertion, recoloring and rotations are used to maintain the
Red-Black properties.

In insert operation, we check color of uncle to decide the appropriate
case. In delete operation, ***we check color of sibling*** to decide the
appropriate case.

The main property that violates after insertion is two consecutive reds.
In delete, the main violated property is, change of black height in
subtrees as deletion of a black node may cause reduced black height in
one root to leaf path.

Deletion is fairly complex process.Â  To understand deletion, notion of
double black is used.Â  When a black node is deleted and replaced by a
black child, the child is marked as ***double black***. The main task
now becomes to convert this double black to single black.

**Deletion Steps**  
 Following are detailed steps for deletion.

**1)** Perform [standard BST
delete](http://geeksquiz.com/binary-search-tree-set-2-delete/). When we
perform standard delete operation in BST, we always end up deleting a
node which is either leaf or has only one child (For an internal node,
we copy the successor and then recursively call delete for successor,
successor is always a leaf node or a node with one child). So we only
need to handle cases where a node is leaf or has one child. Let v be the
node deleted and u be the child that replaces v.

**2) Simple Case: If either u or v is red,** we mark the replaced child
as black (No change in black height). Note that both u and v cannot be
red as v is parent of u and two consecutive reds are not allowed in
red-black tree.  

[![rbdelete11](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete11.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete11.png)

**3)** **If Both u and v are Black**.

**3.1)** Color u as double black.Â  Now our task reduces to convert this
double black to single black. Note that If v is leaf, then u is NULL and
color of NULL is considered as black. So the deletion of a black leaf
also causes a double black.

[![rbdelete12\_new](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete12_new.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete12_new.png)

**3.2)** Do following while the current node u is double black or it is
not root. Let sibling of node be **s**.  
 ….**(a): If sibling s is black and at least one of sibling’s children
is <span>red</span>**, perform rotation(s). Let the red child of s be
**<span>r</span>**. This case can be divided in four subcases depending
upon positions of s and r.

…………..**(i)** Left Left Case (s is left child of its parent and r is
left child of s or both children of s are red). This is mirror of right
right case shown in below diagram.

…………..**(ii)** Left Right Case (s is left child of its parent and r is
right child). This is mirror of right left case shown in below diagram.

…………..**(iii)** Right Right Case (s is right child of its parent and r
is right child of s or both children of s are red)  

[![rbdelete13New](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete13New.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete13New.png)

…………..**(iv)** Right Left Case (s is right child of its parent and r is
left child of s)  

[![rbdelete14](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete14.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete14.png)

…..**(b): If sibling is black and its both children are black**, perform
recoloring, and recur for the parent if parent is black.  

[![rbdelete15](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete15.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete15.png)  
 In this case, if parent was red, then we didn’t need to recur for
prent, we can simply make it black (red + double black = single black)

…..**(c): If sibling is <span>red</span>**, perform a rotation to move
old sibling up, recolor the old sibling and parent. The new sibling is
always black (See the below diagram). This mainly converts the tree to
black sibling case (by rotation) andÂ  leads to case (a) or (b). This
case can be divided in two subcases.  
 …………..**(i)** Left Case (s is left child of its parent). This is mirror
of right right case shown in below diagram. We right rotate the parent
p.  
 …………..**(iii)** Right Case (s is right child of its parent). We left
rotate the parent p.  

[![rbdelete16](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete16.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/rbdelete16.png)

**3.3)** If u is root, make it single black and return (Black height of
complete tree reduces by 1).

**References:**  
 <https://www.cs.purdue.edu/homes/ayg/CS251/slides/chap13c.pdf>  
 [Introduction to Algorithms 3rd Edition by Clifford Stein, Thomas H.
Cormen, Charles E. Leiserson, Ronald L.
Rivest](http://www.flipkart.com/introduction-algorithms-3rd/p/itmczynzhyhxv2gs?pid=9788120340077&affid=sandeepgfg)

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/red-black-tree-set-3-delete-2/>

Segment Tree | Set 2 (Range Minimum Query)
------------------------------------------

We have introduced [segment tree with a simple
example](http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/)
in the previous post. In this post, [Range Minimum
Query](http://en.wikipedia.org/wiki/Range_Minimum_Query) problem is
discussed as another example where Segment Tree can be used.<span
id="more-113981"></span> Following is problem statement.

We have an array arr[0 . . . n-1]. We should be able to efficiently find
the minimum value from index *qs* (query start) to *qe* (query end)
where *0 . The array is static (elements are not deleted and inserted
during the series of queries).*

A **simple solution** is to run a loop from *qs* to *qe* and find
minimum element in given range. This solution takes O(n) time in worst
case.

**Another solution** is to create a 2D array where an entry [i, j]
stores the minimum value in range arr[i..j]. Minimum of a given range
can now be calculated in O(1) time, but preprocessing takes O(n^2) time.
Also, this approach needs O(n^2) extra space which may become huge for
large input arrays.

[**Segment
tree**](http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/ "Segment Tree")
can be used to do preprocessing and query in moderate time. With segment
tree, preprocessing time is O(n) and time to for range minimum query is
O(Logn). The extra space required is O(n) to store the segment tree.

Representation of Segment trees  
 **1.** Leaf Nodes are the elements of the input array.  
 **2.** Each internal node represents minimum of all leaves under it.

An array representation of tree is used to represent Segment Trees. For
each node at index i, the left child is at index 2\*i+1, right child at
2\*i+2 and the parent is at ![\\lfloor (i-1)/2
\\rfloor](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-2cfd252ac5fd2f0f89149a5989c14e25_l3.png "Rendered by QuickLaTeX.com").

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/RangeMinimumQuery.png "RangeMinimumQuery")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/RangeMinimumQuery.png)

**Construction of Segment Tree from given array**  
 We start with a segment arr[0 . . . n-1]. and every time we divide the
current segment into two halves(if it has not yet become a segment of
length 1), and then call the same procedure on both halves, and for each
such segment, we store the minimum value in a segment tree node.  
 All levels of the constructed segment tree will be completely filled
except the last level. Also, the tree will be a [Full Binary
Tree](http://en.wikipedia.org/wiki/Binary_tree#Types_of_binary_trees)
because we always divide segments in two halves at every level. Since
the constructed tree is always full binary tree with n leaves, there
will be n-1 internal nodes. So total number of nodes will be 2\*n – 1.  
 Height of the segment tree will be ![\\lceil \\log\_2{n}
\\rceil](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-450213a0ead2f203224923ed77bbc1e5_l3.png "Rendered by QuickLaTeX.com").
Since the tree is represented using array and relation between parent
and child indexes must be maintained, size of memory allocated for
segment tree will be ![2 \* 2 ^{\\lceil \\log\_2{n} \\rceil} -
1](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-5faa912d34391d3c73250f145b106a73_l3.png "Rendered by QuickLaTeX.com").

**Query for minimum value of given range**  
 Once the tree is constructed, how to do range minimum query using the
constructed segment tree. Following is algorithm to get the minimum.

    // qs --> query start index, qe --> query end index
    int RMQ(node, qs, qe) 
    {
       if range of node is within qs and qe
            return value in node
       else if range of node is completely outside qs and qe
            return INFINITE
       else
        return min( RMQ(node's left child, qs, qe), RMQ(node's right child, qs, qe) )
    }

**Implementation:**

    // Program for range minimum query using segment tree
    #include <stdio.h>
    #include <math.h>
    #include <limits.h>

    // A utility function to get minimum of two numbers
    int minVal(int x, int y) { return (x < y)? x: y; }

    // A utility function to get the middle index from corner indexes.
    int getMid(int s, int e) {  return s + (e -s)/2;  }

    /*  A recursive function to get the minimum value in a given range of array
        indexes. The following are parameters for this function.

        st    --> Pointer to segment tree
        index --> Index of current node in the segment tree. Initially 0 is
                 passed as root is always at index 0
        ss & se  --> Starting and ending indexes of the segment represented by
                     current node, i.e., st[index]
        qs & qe  --> Starting and ending indexes of query range */
    int RMQUtil(int *st, int ss, int se, int qs, int qe, int index)
    {
        // If segment of this node is a part of given range, then return the
        // min of the segment
        if (qs <= ss && qe >= se)
            return st[index];

        // If segment of this node is outside the given range
        if (se < qs || ss > qe)
            return INT_MAX;

        // If a part of this segment overlaps with the given range
        int mid = getMid(ss, se);
        return minVal(RMQUtil(st, ss, mid, qs, qe, 2*index+1),
                      RMQUtil(st, mid+1, se, qs, qe, 2*index+2));
    }

    // Return minimum of elements in range from index qs (quey start) to
    // qe (query end).  It mainly uses RMQUtil()
    int RMQ(int *st, int n, int qs, int qe)
    {
        // Check for erroneous input values
        if (qs < 0 || qe > n-1 || qs > qe)
        {
            printf("Invalid Input");
            return -1;
        }

        return RMQUtil(st, 0, n-1, qs, qe, 0);
    }

    // A recursive function that constructs Segment Tree for array[ss..se].
    // si is index of current node in segment tree st
    int constructSTUtil(int arr[], int ss, int se, int *st, int si)
    {
        // If there is one element in array, store it in current node of
        // segment tree and return
        if (ss == se)
        {
            st[si] = arr[ss];
            return arr[ss];
        }

        // If there are more than one elements, then recur for left and
        // right subtrees and store the minimum of two values in this node
        int mid = getMid(ss, se);
        st[si] =  minVal(constructSTUtil(arr, ss, mid, st, si*2+1),
                         constructSTUtil(arr, mid+1, se, st, si*2+2));
        return st[si];
    }

    /* Function to construct segment tree from given array. This function
       allocates memory for segment tree and calls constructSTUtil() to
       fill the allocated memory */
    int *constructST(int arr[], int n)
    {
        // Allocate memory for segment tree
        int x = (int)(ceil(log2(n))); //Height of segment tree
        int max_size = 2*(int)pow(2, x) - 1; //Maximum size of segment tree
        int *st = new int[max_size];

        // Fill the allocated memory st
        constructSTUtil(arr, 0, n-1, st, 0);

        // Return the constructed segment tree
        return st;
    }

    // Driver program to test above functions
    int main()
    {
        int arr[] = {1, 3, 2, 7, 9, 11};
        int n = sizeof(arr)/sizeof(arr[0]);

        // Build segment tree from given array
        int *st = constructST(arr, n);

        int qs = 1;  // Starting index of query range
        int qe = 5;  // Ending index of query range

        // Print minimum value in arr[qs..qe]
        printf("Minimum of values in range [%d, %d] is = %d\n",
                               qs, qe, RMQ(st, n, qs, qe));

        return 0;
    }

Output:

     
    Minimum of values in range [1, 5] is = 2

**Time Complexity:**  
 Time Complexity for tree construction is O(n). There are total 2n-1
nodes, and value of every node is calculated only once in tree
construction.

Time complexity to query is O(Logn). To query a range minimum, we
process at most two nodes at every level and number of levels is
O(Logn).

Please refer following links for more solutions to range minimum query
problem.  

<http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=lowestCommonAncestor#Range_Minimum_Query_(RMQ)>  
 <http://wcipeg.com/wiki/Range_minimum_query>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/segment-tree-set-1-range-minimum-query/>

Segment Tree | Set 1 (Sum of given range)
-----------------------------------------

Let us consider the following problem to understand Segment Trees.

We have an array arr[0 . . . n-1]. We should be able to  
 **1** Find the sum of elements from index l to r where 0 **2** Change
value of a specified element of the array arr[i] = x where 0

A **simple solution** is to run a loop from l to r and calculate sum of
elements in given range. To update a value, simply do arr[i] = x. The
first operation takes O(n) time and second operation takes O(1) time.

**Another solution** is to create another array and store sum from start
to i at the ith index in this array. Sum of a given range can now be
calculated in O(1) time, but update operation takes O(n) time now. This
works well if the number of query operations are large and very few
updates.

What if the number of query and updates are equal? **Can we perform both
the operations in O(log n) time once given the array?** We can use a
Segment Tree to do both operations in O(Logn) time.

**Representation of Segment trees**  
 **1.** Leaf Nodes are the elements of the input array.  
 **2.** Each internal node represents some merging of the leaf nodes.
The merging may be different for different problems. For this problem,
merging is sum of leaves under a node.

An array representation of tree is used to represent Segment Trees. For
each node at index i, the left child is at index 2\*i+1, right child at
2\*i+2 and the parent is at ![\\lfloor (i-1)/2
\\rfloor](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-2cfd252ac5fd2f0f89149a5989c14e25_l3.png "Rendered by QuickLaTeX.com").

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/segment-tree1.png "segment-tree")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/segment-tree1.png)

**Construction of Segment Tree from given array**  
 We start with a segment arr[0 . . . n-1]. and every time we divide the
current segment into two halves(if it has not yet become a segment of
length 1), and then call the same procedure on both halves, and for each
such segment we store the sum in corresponding node.  
 All levels of the constructed segment tree will be completely filled
except the last level. Also, the tree will be a [Full Binary
Tree](http://en.wikipedia.org/wiki/Binary_tree#Types_of_binary_trees)
because we always divide segments in two halves at every level. Since
the constructed tree is always full binary tree with n leaves, there
will be n-1 internal nodes. So total number of nodes will be 2\*n – 1.  
 Height of the segment tree will be ![\\lceil \\log\_2{n}
\\rceil](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-450213a0ead2f203224923ed77bbc1e5_l3.png "Rendered by QuickLaTeX.com").
Since the tree is represented using array and relation between parent
and child indexes must be maintained, size of memory allocated for
segment tree will be ![2 \* 2 ^{\\lceil \\log\_2{n} \\rceil} -
1](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-5faa912d34391d3c73250f145b106a73_l3.png "Rendered by QuickLaTeX.com").

**Query for Sum of given range**  
 Once the tree is constructed, how to get the sum using the constructed
segment tree. Following is algorithm to get the sum of elements.

    int getSum(node, l, r) 
    {
       if range of node is within l and r
            return value in node
       else if range of node is completely outside l and r
            return 0
       else
        return getSum(node's left child, l, r) + 
               getSum(node's right child, l, r)
    }

**Update a value**  
 Like tree construction and query operations, update can also be done
recursively. We are given an index which needs to updated. Let *diff* be
the value to be added. We start from root of the segment tree, and add
*diff* to all nodes which have given index in their range. If a node
doesn’t have given index in its range, we don’t make any changes to that
node.

**Implementation:**  
 Following is implementation of segment tree. The program implements
construction of segment tree for any given array. It also implements
query and update operations.

    // Program to show segment tree operations like construction, query and update
    #include <stdio.h>
    #include <math.h>

    // A utility function to get the middle index from corner indexes.
    int getMid(int s, int e) {  return s + (e -s)/2;  }

    /*  A recursive function to get the sum of values in given range of the array.
        The following are parameters for this function.

        st    --> Pointer to segment tree
        index --> Index of current node in the segment tree. Initially 0 is
                 passed as root is always at index 0
        ss & se  --> Starting and ending indexes of the segment represented by
                     current node, i.e., st[index]
        qs & qe  --> Starting and ending indexes of query range */
    int getSumUtil(int *st, int ss, int se, int qs, int qe, int index)
    {
        // If segment of this node is a part of given range, then return the 
        // sum of the segment
        if (qs <= ss && qe >= se)
            return st[index];

        // If segment of this node is outside the given range
        if (se < qs || ss > qe)
            return 0;

        // If a part of this segment overlaps with the given range
        int mid = getMid(ss, se);
        return getSumUtil(st, ss, mid, qs, qe, 2*index+1) +
               getSumUtil(st, mid+1, se, qs, qe, 2*index+2);
    }

    /* A recursive function to update the nodes which have the given index in
       their range. The following are parameters
        st, index, ss and se are same as getSumUtil()
        i    --> index of the element to be updated. This index is in input array.
       diff --> Value to be added to all nodes which have i in range */
    void updateValueUtil(int *st, int ss, int se, int i, int diff, int index)
    {
        // Base Case: If the input index lies outside the range of this segment
        if (i < ss || i > se)
            return;

        // If the input index is in range of this node, then update the value
        // of the node and its children
        st[index] = st[index] + diff;
        if (se != ss)
        {
            int mid = getMid(ss, se);
            updateValueUtil(st, ss, mid, i, diff, 2*index + 1);
            updateValueUtil(st, mid+1, se, i, diff, 2*index + 2);
        }
    }

    // The function to update a value in input array and segment tree.
    // It uses updateValueUtil() to update the value in segment tree
    void updateValue(int arr[], int *st, int n, int i, int new_val)
    {
        // Check for erroneous input index
        if (i < 0 || i > n-1)
        {
            printf("Invalid Input");
            return;
        }

        // Get the difference between new value and old value
        int diff = new_val - arr[i];

        // Update the value in array
        arr[i] = new_val;

        // Update the values of nodes in segment tree
        updateValueUtil(st, 0, n-1, i, diff, 0);
    }

    // Return sum of elements in range from index qs (quey start) to
    // qe (query end).  It mainly uses getSumUtil()
    int getSum(int *st, int n, int qs, int qe)
    {
        // Check for erroneous input values
        if (qs < 0 || qe > n-1 || qs > qe)
        {
            printf("Invalid Input");
            return -1;
        }

        return getSumUtil(st, 0, n-1, qs, qe, 0);
    }

    // A recursive function that constructs Segment Tree for array[ss..se].
    // si is index of current node in segment tree st
    int constructSTUtil(int arr[], int ss, int se, int *st, int si)
    {
        // If there is one element in array, store it in current node of
        // segment tree and return
        if (ss == se)
        {
            st[si] = arr[ss];
            return arr[ss];
        }

        // If there are more than one elements, then recur for left and
        // right subtrees and store the sum of values in this node
        int mid = getMid(ss, se);
        st[si] =  constructSTUtil(arr, ss, mid, st, si*2+1) +
                  constructSTUtil(arr, mid+1, se, st, si*2+2);
        return st[si];
    }

    /* Function to construct segment tree from given array. This function
       allocates memory for segment tree and calls constructSTUtil() to
       fill the allocated memory */
    int *constructST(int arr[], int n)
    {
        // Allocate memory for segment tree
        int x = (int)(ceil(log2(n))); //Height of segment tree
        int max_size = 2*(int)pow(2, x) - 1; //Maximum size of segment tree
        int *st = new int[max_size];

        // Fill the allocated memory st
        constructSTUtil(arr, 0, n-1, st, 0);

        // Return the constructed segment tree
        return st;
    }

    // Driver program to test above functions
    int main()
    {
        int arr[] = {1, 3, 5, 7, 9, 11};
        int n = sizeof(arr)/sizeof(arr[0]);

        // Build segment tree from given array
        int *st = constructST(arr, n);

        // Print sum of values in array from index 1 to 3
        printf("Sum of values in given range = %d\n", getSum(st, n, 1, 3));

        // Update: set arr[1] = 10 and update corresponding segment
        // tree nodes
        updateValue(arr, st, n, 1, 10);

        // Find sum after the value is updated
        printf("Updated sum of values in given range = %d\n",
                                                      getSum(st, n, 1, 3));

        return 0;
    }

Output:

     
    Sum of values in given range = 15
    Updated sum of values in given range = 22

**Time Complexity:**  
 Time Complexity for tree construction is O(n). There are total 2n-1
nodes, and value of every node is calculated only once in tree
construction.

Time complexity to query is O(Logn). To query a sum, we process at most
four nodes at every level and number of levels is O(Logn).

The time complexity of update is also O(Logn). To update a leaf value,
we process one node at every level and number of levels is O(Logn).

**[  
 Segment Tree | Set 2 (Range Minimum
Query)](http://www.geeksforgeeks.org/segment-tree-set-1-range-minimum-query/)**

**References:**  
 <http://www.cse.iitk.ac.in/users/aca/lop12/slides/06.pdf>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/),
[SegmentTree](http://www.geeksforgeeks.org/tag/segmenttree/)

### Source:

<http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/>

Sort numbers stored on different machines
-----------------------------------------

Given N machines. Each machine contains some numbers in sorted form. But
the amount of numbers, each machine has is not fixed. Output the numbers
from all the machine in sorted non-decreasing form.<span
id="more-24463"></span>

    Example:
           Machine M1 contains 3 numbers: {30, 40, 50}
           Machine M2 contains 2 numbers: {35, 45} 
           Machine M3 contains 5 numbers: {10, 60, 70, 80, 100}
           
           Output: {10, 30, 35, 40, 45, 50, 60, 70, 80, 100}

Representation of stream of numbers on each machine is considered as
linked list. A Min Heap can be used to print all numbers in sorted
order.

Following is the detailed process

**1.** Store the head pointers of the linked lists in a minHeap of size
N where N is number of machines.

**2.** Extract the minimum item from the minHeap. Update the minHeap by
replacing the head of the minHeap with the next number from the linked
list or by replacing the head of the minHeap with the last number in the
minHeap followed by decreasing the size of heap by 1.

**3.** Repeat the above step 2 until heap is not empty.

Below is C++ implementation of the above approach.

    // A program to take numbers from different machines and print them in sorted order
    #include <stdio.h>

    // A Linked List node
    struct ListNode
    {
        int data;
        struct ListNode* next;
    };

    // A Min Heap Node
    struct MinHeapNode
    {
        ListNode* head;
    };

    // A Min Heao (Collection of Min Heap nodes)
    struct MinHeap
    {
        int count;
        int capacity;
        MinHeapNode* array;
    };

    // A function to create a Min Heap of given capacity
    MinHeap* createMinHeap( int capacity )
    {
        MinHeap* minHeap = new MinHeap;
        minHeap->capacity = capacity;
        minHeap->count = 0;
        minHeap->array = new MinHeapNode [minHeap->capacity];
        return minHeap;
    }

    /* A utility function to insert a new node at the begining
       of linked list */
    void push (ListNode** head_ref, int new_data)
    {
        /* allocate node */
        ListNode* new_node = new ListNode;

        /* put in the data  */
        new_node->data  = new_data;

        /* link the old list off the new node */
        new_node->next = (*head_ref);

        /* move the head to point to the new node */
        (*head_ref)    = new_node;
    }

    // A utility function to swap two min heap nodes. This function
    // is needed in minHeapify
    void swap( MinHeapNode* a, MinHeapNode* b )
    {
        MinHeapNode temp = *a;
        *a = *b;
        *b = temp;
    }

    // The standard minHeapify function.
    void minHeapify( MinHeap* minHeap, int idx )
    {
        int left, right, smallest;
        left = 2 * idx + 1;
        right = 2 * idx + 2;
        smallest = idx;

        if ( left < minHeap->count &&
             minHeap->array[left].head->data <
             minHeap->array[smallest].head->data
           )
            smallest = left;

        if ( right < minHeap->count &&
             minHeap->array[right].head->data <
             minHeap->array[smallest].head->data
           )
            smallest = right;

        if( smallest != idx )
        {
            swap( &minHeap->array[smallest], &minHeap->array[idx] );
            minHeapify( minHeap, smallest );
        }
    }

    // A utility function to check whether a Min Heap is empty or not
    int isEmpty( MinHeap* minHeap )
    {
        return (minHeap->count == 0);
    }

    // A standard function to build a heap
    void buildMinHeap( MinHeap* minHeap )
    {
        int i, n;
        n = minHeap->count  - 1;
        for( i = (n - 1) / 2; i >= 0; --i )
            minHeapify( minHeap, i );
    }

    // This function inserts array elements to heap and then calls
    // buildHeap for heap property among nodes
    void populateMinHeap( MinHeap* minHeap, ListNode* *array, int n )
    {
        for( int i = 0; i < n; ++i )
            minHeap->array[ minHeap->count++ ].head = array[i];

        buildMinHeap( minHeap );
    }

    // Return minimum element from all linked lists
    ListNode* extractMin( MinHeap* minHeap )
    {
        if( isEmpty( minHeap ) )
             return NULL;

        // The root of heap will have minimum value
        MinHeapNode temp = minHeap->array[0];

        // Replace root either with next node of the same list.
        if( temp.head->next )
            minHeap->array[0].head = temp.head->next;
        else // If list empty, then reduce heap size
        {
            minHeap->array[0] = minHeap->array[ minHeap->count - 1 ];
            --minHeap->count;
        }

        minHeapify( minHeap, 0 );
        return temp.head;
    }

    // The main function that takes an array of lists from N machines
    // and generates the sorted output
    void externalSort( ListNode *array[], int N )
    {
        // Create a min heap of size equal to number of machines
        MinHeap* minHeap = createMinHeap( N );

        // populate first item from all machines
        populateMinHeap( minHeap, array, N );

        while ( !isEmpty( minHeap ) )
        {
            ListNode* temp = extractMin( minHeap );
            printf( "%d ",temp->data );
        }
    }

    // Driver program to test above functions
    int main()
    {
        int N = 3; // Number of machines

        // an array of pointers storing the head nodes of the linked lists
        ListNode *array[N];

        // Create a Linked List 30->40->50 for first machine
        array[0] = NULL;
        push (&array[0], 50);
        push (&array[0], 40);
        push (&array[0], 30);

        // Create a Linked List 35->45 for second machine
        array[1] = NULL;
        push (&array[1], 45);
        push (&array[1], 35);

        // Create Linked List 10->60->70->80 for third machine
        array[2] = NULL;
        push (&array[2], 100);
        push (&array[2], 80);
        push (&array[2], 70);
        push (&array[2], 60);
        push (&array[2], 10);

        // Sort all elements
        externalSort( array, N );

        return 0;
    }

Output:

    10 30 35 40 45 50 60 70 80 100

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/sort-numbers-stored-on-different-machines/>

Splay Tree | Set 1 (Search)
---------------------------

The worst case time complexity of Binary Search Tree (BST) operations
like search, delete, insert is O(n). The worst case occurs when the tree
is skewed. We can get the worst case time complexity as O(Logn) with
[AVL](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/) and
Red-Black Trees. <span id="more-125429"></span>

**Can we do better than AVL or Red-Black trees in practical
situations?**  
 Like [AVL](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/)and
Red-Black Trees, Splay tree is also [self-balancing
BST](http://en.wikipedia.org/wiki/Self-balancing_binary_search_tree).
The main idea of splay tree is to bring the recently accessed item to
root of the tree, this makes the recently searched item to be accessible
in O(1) time if accessed again. The idea is to use locality of reference
(In a typical application, 80% of the access are to 20% of the items).
Imagine a situation where we have millions or billions of keys and only
few of them are accessed frequently, which is very likely in many
practical applications.

All splay tree operations run in O(log n) time on average, where n is
the number of entries in the tree. Any single operation can take
Theta(n) time in the worst case.

**Search Operation**  
 The search operation in Splay tree does the standard BST search, in
addition to search, it also splays (move a node to the root). If the
search is successful, then the node that is found is splayed and becomes
the new root. Else the last node accessed prior to reaching the NULL is
splayed and becomes the new root.

There are following cases for the node being accessed.

**1)** **Node is root** We simply return the root, don’t do anything
else as the accessed node is already root.

**2) Zig:** ***Node is child of root*** (the node has no grandparent).
Node is either a left child of root (we do a right rotation) or node is
a right child of its parent (we do a left rotation).  
 T1, T2 and T3 are subtrees of the tree rooted with y (on left side) or
x (on right side)

                    y                                     x
                   / \     Zig (Right Rotation)          /  \
                  x   T3   â - â - â - â - - ->         T1   y 
                 / \       
    3) Node has both parent and grandparent.  There can be following subcases.

    ........3.a) Zig-Zig and Zag-Zag Node is left child of parent and parent is also left child of grand parent (Two right rotations) OR node is right child of its parent and parent is also right child of grand parent (Two Left Rotations).  

    Zig-Zig (Left Left Case):
           G                        P                           X       
          / \                     /   \                        / \      
         P  T4   rightRotate(G)  X     G     rightRotate(P)  T1   P     
        / \      ============>  / \   / \    ============>       / \    
       X  T3                   T1 T2 T3 T4                      T2  G
      / \                                                          / \ 
     T1 T2                                                        T3  T4 

    Zag-Zag (Right Right Case):
      G                          P                           X       
     /  \                      /   \                        / \      
    T1   P     leftRotate(G)  G     X     leftRotate(P)    P   T4
        / \    ============> / \   / \    ============>   / \   
       T2   X               T1 T2 T3 T4                  G   T3
           / \                                          / \ 
          T3 T4                                        T1  T2

........**3.b) Zig-Zag and Zag-Zig** Node is left child of parent and
parent is right child of grand parent (Left Rotation followed by right
rotation) OR node is right child of its parent and parent is left child
of grand parent (Right Rotation followed by left rotation).

    Zig-Zag (Left Right Case):
           G                        G                            X       
          / \                     /   \                        /   \      
         P   T4  leftRotate(P)   X     T4    rightRotate(G)   P     G     
       /  \      ============>  / \          ============>   / \   /  \    
      T1   X                   P  T3                       T1  T2 T3  T4 
          / \                 / \                                       
        T2  T3              T1   T2                                     

    Zag-Zig (Right Left Case):
      G                          G                           X       
     /  \                      /  \                        /   \      
    T1   P    rightRotate(P)  T1   X     leftRotate(P)    G     P
        / \   =============>      / \    ============>   / \   / \   
       X  T4                    T2   P                 T1  T2 T3  T4
      / \                           / \                
     T2  T3                        T3  T4  

**Example:**

     
             100                      100                       [20]
             /  \                    /   \                        \ 
           50   200                50    200                      50
          /          search(20)    /          search(20)         /  \  
         40          ======>     [20]         ========>         30   100
        /            1. Zig-Zig    \          2. Zig-Zig         \     \
       30               at 40       30            at 100         40    200  
      /                               \     
    [20]                              40

The important thing to note is, the search or splay operation not only
brings the searched key to root, but also balances the BST. For example
in above case, height of BST is reduced by 1.

**Implementation:**

    // The code is adopted from http://goo.gl/SDH9hH
    #include<stdio.h>
    #include<stdlib.h>

    // An AVL tree node
    struct node
    {
        int key;
        struct node *left, *right;
    };

    /* Helper function that allocates a new node with the given key and
        NULL left and right pointers. */
    struct node* newNode(int key)
    {
        struct node* node = (struct node*)malloc(sizeof(struct node));
        node->key   = key;
        node->left  = node->right  = NULL;
        return (node);
    }

    // A utility function to right rotate subtree rooted with y
    // See the diagram given above.
    struct node *rightRotate(struct node *x)
    {
        struct node *y = x->left;
        x->left = y->right;
        y->right = x;
        return y;
    }

    // A utility function to left rotate subtree rooted with x
    // See the diagram given above.
    struct node *leftRotate(struct node *x)
    {
        struct node *y = x->right;
        x->right = y->left;
        y->left = x;
        return y;
    }

    // This function brings the key at root if key is present in tree.
    // If key is not present, then it brings the last accessed item at
    // root.  This function modifies the tree and returns the new root
    struct node *splay(struct node *root, int key)
    {
        // Base cases: root is NULL or key is present at root
        if (root == NULL || root->key == key)
            return root;

        // Key lies in left subtree
        if (root->key > key)
        {
            // Key is not in tree, we are done
            if (root->left == NULL) return root;

            // Zig-Zig (Left Left)
            if (root->left->key > key)
            {
                // First recursively bring the key as root of left-left
                root->left->left = splay(root->left->left, key);

                // Do first rotation for root, second rotation is done after else
                root = rightRotate(root);
            }
            else if (root->left->key < key) // Zig-Zag (Left Right)
            {
                // First recursively bring the key as root of left-right
                root->left->right = splay(root->left->right, key);

                // Do first rotation for root->left
                if (root->left->right != NULL)
                    root->left = leftRotate(root->left);
            }

            // Do second rotation for root
            return (root->left == NULL)? root: rightRotate(root);
        }
        else // Key lies in right subtree
        {
            // Key is not in tree, we are done
            if (root->right == NULL) return root;

            // Zag-Zig (Right Left)
            if (root->right->key > key)
            {
                // Bring the key as root of right-left
                root->right->left = splay(root->right->left, key);

                // Do first rotation for root->right
                if (root->right->left != NULL)
                    root->right = rightRotate(root->right);
            }
            else if (root->right->key < key)// Zag-Zag (Right Right)
            {
                // Bring the key as root of right-right and do first rotation
                root->right->right = splay(root->right->right, key);
                root = leftRotate(root);
            }

            // Do second rotation for root
            return (root->right == NULL)? root: leftRotate(root);
        }
    }

    // The search function for Splay tree.  Note that this function
    // returns the new root of Splay Tree.  If key is present in tree
    // then, it is moved to root.
    struct node *search(struct node *root, int key)
    {
        return splay(root, key);
    }

    // A utility function to print preorder traversal of the tree.
    // The function also prints height of every node
    void preOrder(struct node *root)
    {
        if (root != NULL)
        {
            printf("%d ", root->key);
            preOrder(root->left);
            preOrder(root->right);
        }
    }

    /* Drier program to test above function*/
    int main()
    {
        struct node *root = newNode(100);
        root->left = newNode(50);
        root->right = newNode(200);
        root->left->left = newNode(40);
        root->left->left->left = newNode(30);
        root->left->left->left->left = newNode(20);

        root = search(root, 20);
        printf("Preorder traversal of the modified Splay tree is \n");
        preOrder(root);
        return 0;
    }

Output:

    Preorder traversal of the modified Splay tree is
    20 50 30 40 100 200

**Summary**  
 **1)** Splay trees have excellent locality properties. Frequently
accessed items are easy to find. Infrequent items are out of way.

**2)** All splay tree operations take O(Logn) time on average. Splay
trees can be rigorously shown to run in O(log n) average time per
operation, over any sequence of operations (assuming we start from an
empty tree)

**3)** Splay trees are simpler compared to
[AVL](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/)and
Red-Black Trees as no extra field is required in every tree node.

**4)** Unlike [AVL
tree](http://www.geeksforgeeks.org/avl-tree-set-1-insertion/), a splay
tree can change even with read-only operations like search.

**Applications of Splay Trees**  
 Splay trees have become the most widely used basic data structure
invented in the last 30 years, because they're the fastest type of
balanced search tree for many applications.  
 Splay trees are used in Windows NT (in the virtual memory, networking,
and file system code), the gcc compiler and GNU C++ library, the sed
string editor, Fore Systems network routers, the most popular
implementation of Unix malloc, Linux loadable kernel modules, and in
much other software (Source:
<http://www.cs.berkeley.edu/~jrs/61b/lec/36>)

We will soon be discussing insert and delete operations on splay trees.

**References:**  
 <http://www.cs.berkeley.edu/~jrs/61b/lec/36>  

<http://www.cs.cornell.edu/courses/cs3110/2009fa/recitations/rec-splay.html>  

<http://courses.cs.washington.edu/courses/cse326/01au/lectures/SplayTrees.ppt>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/splay-tree-set-1-insert/>

Splay Tree | Set 2 (Insert)
---------------------------

It is recommended to refer following post as prerequisite of this post.

[Splay Tree | Set 1
(Search)](http://www.geeksforgeeks.org/splay-tree-set-1-insert/)<span
id="more-125549"></span>

As discussed in the [previous
post](http://www.geeksforgeeks.org/splay-tree-set-1-insert/), Splay tree
is a self-balancing data structure where the last accessed key is always
at root. The insert operation is similar to Binary Search Tree insert
with additional steps to make sure that the newly inserted key becomes
the new root.

Following are different cases to insert a key k in splay tree.

**1)** Root is NULL: We simply allocate a new node and return it as
root.

**2)** [Splay](http://www.geeksforgeeks.org/splay-tree-set-1-insert/)the
given key k. If k is already present, then it becomes the new root. If
not present, then last accessed leaf node becomes the new root.

**3)** If new root’s key is same as k, don’t do anything as k is already
present.

**4)** Else allocate memory for new node and compare root’s key with
k.  
 …….**4.a)** If k is smaller than root’s key, make root as right child
of new node, copy left child of root as left child of new node and make
left child of root as NULL.  
 …….**4.b)** If k is greater than root’s key, make root as left child of
new node, copy right child of root as right child of new node and make
right child of root as NULL.

**5)** Return new node as new root of tree.

**Example:**

     
              100                  [20]                             25     
              /  \                   \                             /  \
            50   200                  50                          20   50 
           /          insert(25)     /  \        insert(25)           /  \  
          40          ======>      30   100      ========>           30  100    
         /          1. Splay(25)    \     \      2. insert 25         \    \
        30                          40    200                         40   200   
       /                                                          
     [20] 

    // This code is adopted from http://algs4.cs.princeton.edu/33balanced/SplayBST.java.html
    #include<stdio.h>
    #include<stdlib.h>

    // An AVL tree node
    struct node
    {
        int key;
        struct node *left, *right;
    };

    /* Helper function that allocates a new node with the given key and
        NULL left and right pointers. */
    struct node* newNode(int key)
    {
        struct node* node = (struct node*)malloc(sizeof(struct node));
        node->key   = key;
        node->left  = node->right  = NULL;
        return (node);
    }

    // A utility function to right rotate subtree rooted with y
    // See the diagram given above.
    struct node *rightRotate(struct node *x)
    {
        struct node *y = x->left;
        x->left = y->right;
        y->right = x;
        return y;
    }

    // A utility function to left rotate subtree rooted with x
    // See the diagram given above.
    struct node *leftRotate(struct node *x)
    {
        struct node *y = x->right;
        x->right = y->left;
        y->left = x;
        return y;
    }

    // This function brings the key at root if key is present in tree.
    // If key is not present, then it brings the last accessed item at
    // root.  This function modifies the tree and returns the new root
    struct node *splay(struct node *root, int key)
    {
        // Base cases: root is NULL or key is present at root
        if (root == NULL || root->key == key)
            return root;

        // Key lies in left subtree
        if (root->key > key)
        {
            // Key is not in tree, we are done
            if (root->left == NULL) return root;

            // Zig-Zig (Left Left)
            if (root->left->key > key)
            {
                // First recursively bring the key as root of left-left
                root->left->left = splay(root->left->left, key);

                // Do first rotation for root, second rotation is done after else
                root = rightRotate(root);
            }
            else if (root->left->key < key) // Zig-Zag (Left Right)
            {
                // First recursively bring the key as root of left-right
                root->left->right = splay(root->left->right, key);

                // Do first rotation for root->left
                if (root->left->right != NULL)
                    root->left = leftRotate(root->left);
            }

            // Do second rotation for root
            return (root->left == NULL)? root: rightRotate(root);
        }
        else // Key lies in right subtree
        {
            // Key is not in tree, we are done
            if (root->right == NULL) return root;

            // Zig-Zag (Right Left)
            if (root->right->key > key)
            {
                // Bring the key as root of right-left
                root->right->left = splay(root->right->left, key);

                // Do first rotation for root->right
                if (root->right->left != NULL)
                    root->right = rightRotate(root->right);
            }
            else if (root->right->key < key)// Zag-Zag (Right Right)
            {
                // Bring the key as root of right-right and do first rotation
                root->right->right = splay(root->right->right, key);
                root = leftRotate(root);
            }

            // Do second rotation for root
            return (root->right == NULL)? root: leftRotate(root);
        }
    }

    // Function to insert a new key k in splay tree with given root
    struct node *insert(struct node *root, int k)
    {
        // Simple Case: If tree is empty
        if (root == NULL) return newNode(k);

        // Bring the closest leaf node to root
        root = splay(root, k);

        // If key is already present, then return
        if (root->key == k) return root;

        // Otherwise allocate memory for new node
        struct node *newnode  = newNode(k);

        // If root's key is greater, make root as right child
        // of newnode and copy the left child of root to newnode
        if (root->key > k)
        {
            newnode->right = root;
            newnode->left = root->left;
            root->left = NULL;
        }

        // If root's key is smaller, make root as left child
        // of newnode and copy the right child of root to newnode
        else
        {
            newnode->left = root;
            newnode->right = root->right;
            root->right = NULL;
        }

        return newnode; // newnode becomes new root
    }

    // A utility function to print preorder traversal of the tree.
    // The function also prints height of every node
    void preOrder(struct node *root)
    {
        if (root != NULL)
        {
            printf("%d ", root->key);
            preOrder(root->left);
            preOrder(root->right);
        }
    }

    /* Drier program to test above function*/
    int main()
    {
        struct node *root = newNode(100);
        root->left = newNode(50);
        root->right = newNode(200);
        root->left->left = newNode(40);
        root->left->left->left = newNode(30);
        root->left->left->left->left = newNode(20);
        root = insert(root, 25);
        printf("Preorder traversal of the modified Splay tree is \n");
        preOrder(root);
        return 0;
    }

Output:

    Preorder traversal of the modified Splay tree is
    25 20 50 30 40 100 200

This article is compiled by **Abhay Rathi**. Please write comments if
you find anything incorrect, or you want to share more information about
the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/splay-tree-set-2-insert-delete/>

Suffix Array | Set 1 (Introduction)
-----------------------------------

We strongly recommend to read following post on suffix trees as a
pre-requisite for this post.<span id="more-125731"></span>

[Pattern Searching | Set 8 (Suffix Tree
Introduction)](http://www.geeksforgeeks.org/pattern-searching-set-8-suffix-tree-introduction/)

***A suffix array is a sorted array of all suffixes of a given
string***. The definition is similar to [Suffix Tree which is compressed
trie of all suffixes of the given
text](http://www.geeksforgeeks.org/pattern-searching-set-8-suffix-tree-introduction/).
Any suffix tree based algorithm can be replaced with an algorithm that
uses a suffix array enhanced with additional information and solves the
same problem in the same time complexity (Source
[Wiki](http://en.wikipedia.org/wiki/Suffix_array)).  
 A suffix array can be constructed from Suffix tree by doing a DFS
traversal of the suffix tree. In fact Suffix array and suffix tree both
can be constructed from each other in linear time.  
 Advantages of suffix arrays over suffix trees include improved space
requirements, simpler linear time construction algorithms (e.g.,
compared to Ukkonen’s algorithm) and improved cache locality (Source:
[Wiki](http://en.wikipedia.org/wiki/Suffix_array#Correspondence_to_suffix_trees))

***Example:***

    Let the given string be "banana".

    0 banana                          5 a
    1 anana     Sort the Suffixes     3 ana
    2 nana      ---------------->     1 anana
    3 ana        alphabetically       0 banana
    4 na                              4 na
    5 a                               2 nana

    So the suffix array for "banana" is {5, 3, 1, 0, 4, 2}

***Naive method to build Suffix Array***  
 A simple method to construct suffix array is to make an array of all
suffixes and then sort the array. Following is implementation of simple
method.

    // Naive algorithm for building suffix array of a given text
    #include <iostream>
    #include <cstring>
    #include <algorithm>
    using namespace std;

    // Structure to store information of a suffix
    struct suffix
    {
        int index;
        char *suff;
    };

    // A comparison function used by sort() to compare two suffixes
    int cmp(struct suffix a, struct suffix b)
    {
        return strcmp(a.suff, b.suff) < 0? 1 : 0;
    }

    // This is the main function that takes a string 'txt' of size n as an
    // argument, builds and return the suffix array for the given string
    int *buildSuffixArray(char *txt, int n)
    {
        // A structure to store suffixes and their indexes
        struct suffix suffixes[n];

        // Store suffixes and their indexes in an array of structures.
        // The structure is needed to sort the suffixes alphabatically
        // and maintain their old indexes while sorting
        for (int i = 0; i < n; i++)
        {
            suffixes[i].index = i;
            suffixes[i].suff = (txt+i);
        }

        // Sort the suffixes using the comparison function
        // defined above.
        sort(suffixes, suffixes+n, cmp);

        // Store indexes of all sorted suffixes in the suffix array
        int *suffixArr = new int[n];
        for (int i = 0; i < n; i++)
            suffixArr[i] = suffixes[i].index;

        // Return the suffix array
        return  suffixArr;
    }

    // A utility function to print an array of given size
    void printArr(int arr[], int n)
    {
        for(int i = 0; i < n; i++)
            cout << arr[i] << " ";
        cout << endl;
    }

    // Driver program to test above functions
    int main()
    {
        char txt[] = "banana";
        int n = strlen(txt);
        int *suffixArr = buildSuffixArray(txt,  n);
        cout << "Following is suffix array for " << txt << endl;
        printArr(suffixArr, n);
        return 0;
    }

Output:

    Following is suffix array for banana
    5 3 1 0 4 2

The time complexity of above method to build suffix array is
O(n<sup>2</sup>Logn) if we consider a O(nLogn) algorithm used for
sorting. The sorting step itself takes O(n<sup>2</sup>Logn) time as
every comparison is a comparison of two strings and the comparison takes
O(n) time.  
 There are many efficient algorithms to build suffix array. We will soon
be covering them as separate posts.

***Search a pattern using the built Suffix Array***  
 To search a pattern in a text, we preprocess the text and build a
suffix array of the text. Since we have a sorted array of all suffixes,
[Binary Search](http://geeksquiz.com/binary-search/) can be used to
search. Following is the search function. Note that the function doesn’t
report all occurrences of pattern, it only report one of them.

    // This code only contains search() and main. To make it a complete running
    // above code or see http://ideone.com/1Io9eN

    // A suffix array based search function to search a given pattern
    // 'pat' in given text 'txt' using suffix array suffArr[]
    void search(char *pat, char *txt, int *suffArr, int n)
    {
        int m = strlen(pat);  // get length of pattern, needed for strncmp()

        // Do simple binary search for the pat in txt using the
        // built suffix array
        int l = 0, r = n-1;  // Initilize left and right indexes
        while (l <= r)
        {
            // See if 'pat' is prefix of middle suffix in suffix array
            int mid = l + (r - l)/2;
            int res = strncmp(pat, txt+suffArr[mid], m);

            // If match found at the middle, print it and return
            if (res == 0)
            {
                cout << "Pattern found at index " << suffArr[mid];
                return;
            }

            // Move to left half if pattern is alphabtically less than
            // the mid suffix
            if (res < 0) r = mid - 1;

            // Otherwise move to right half
            else l = mid + 1;
        }

        // We reach here if return statement in loop is not executed
        cout << "Pattern not found";
    }

    // Driver program to test above function
    int main()
    {
        char txt[] = "banana";  // text
        char pat[] = "nan";   // pattern to be searched in text

        // Build suffix array
        int n = strlen(txt);
        int *suffArr = buildSuffixArray(txt, n);

        // search pat in txt using the built suffix array
        search(pat, txt, suffArr, n);

        return 0;
    }

Output:

    Pattern found at index 2

The time complexity of the above search function is O(mLogn). There are
more efficient algorithms to search pattern once the suffix array is
built. In fact there is a O(m) suffix array based algorithm to search a
pattern. We will soon be discussing efficient algorithm for search.

***Applications of Suffix Array***  
 Suffix array is an extremely useful data structure, it can be used for
a wide range of problems. Following are some famous problems where
Suffix array can be used.  
 1) Pattern Searching  
 2) [Finding the longest repeated
substring](http://en.wikipedia.org/wiki/Longest_repeated_substring_problem)  
 3) [Finding the longest common
substring](http://en.wikipedia.org/wiki/Longest_common_substring_problem)  
 4) [Finding the longest palindrome in a
string](http://en.wikipedia.org/wiki/Longest_palindromic_substring)

See [this](http://www.stanford.edu/class/cs97si/suffix-array.pdf) for
more problems where Suffix arrays can be used.

This post is a simple introduction. There is a lot to cover in Suffix
arrays. We have discussed [a O(nLogn) algorithm for Suffix Array
construction](http://www.geeksforgeeks.org/suffix-array-set-2-a-nlognlogn-algorithm/)
[here](http://www.geeksforgeeks.org/suffix-array-set-2-a-nlognlogn-algorithm/).
We will soon be discussing more efficient suffix array algorithms.

**References:**  
 <http://www.stanford.edu/class/cs97si/suffix-array.pdf>  
 <http://en.wikipedia.org/wiki/Suffix_array>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/),
[Pattern Searching](http://www.geeksforgeeks.org/tag/pattern-searching/)

### Source:

<http://www.geeksforgeeks.org/suffix-array-set-1-introduction/>

Suffix Array | Set 2 (nLogn Algorithm)
--------------------------------------

**A suffix array is a sorted array of all suffixes of a given
string.**<span id="more-125782"></span> The definition is similar to
[Suffix
Tree](http://www.geeksforgeeks.org/pattern-searching-set-8-suffix-tree-introduction/)
which is compressed trie of all suffixes of the given text.

    Let the given string be "banana".

    0 banana                          5 a
    1 anana     Sort the Suffixes     3 ana
    2 nana      ---------------->     1 anana
    3 ana        alphabetically       0 banana
    4 na                              4 na
    5 a                               2 nana

    The suffix array for "banana" is {5, 3, 1, 0, 4, 2} 

We have discussed **[Naive
algorithm](http://www.geeksforgeeks.org/suffix-array-set-1-introduction/)**
for construction of suffix array. The Naive algorithm is to consider all
suffixes, sort them using a O(nLogn) sorting algorithm and while
sorting, maintain original indexes. Time complexity of the Naive
algorithm is O(n<sup>2</sup>Logn) where n is the number of characters in
the input string.

In this post, a **O(nLogn) algorithm** for suffix array construction is
discussed. Let us first discuss a O(n \* Logn \* Logn) algorithm for
simplicity. The idea is to use the fact that strings that are to be
sorted are suffixes of a single string.  
 We first sort all suffixes according to first character, then according
to first 2 characters, then first 4 characters and so on while the
number of characters to be considered is smaller than 2n. The important
point is, if we have sorted suffixes according to first 2<sup>i</sup>
characters, then we can sort suffixes according to first 2<sup>i+1</sup>
characters in O(nLogn) time using a nLogn sorting algorithm like Merge
Sort. This is possible as two suffixes can be compared in O(1) time (we
need to compare only two values, see the below example and code).  
 The sort function is called O(Logn) times (Note that we increase number
of characters to be considered in powers of 2). Therefore overall time
complexity becomes O(nLognLogn). See
<http://www.stanford.edu/class/cs97si/suffix-array.pdf> for more
details.

Let us build suffix array the example string “banana” using above
algorithm.

**Sort according to first two characters** Assign a rank to all suffixes
using ASCII value of first character. A simple way to assign rank is to
do “str[i] – ‘a'” for ith suffix of strp[]

    Index     Suffix            Rank
     0        banana             1
     1        anana              0
     2        nana               13
     3        ana                0
     4        na                 13
     5        a                  0 

For every character, we also store rank of next adjacent character,
i.e., the rank of character at str[i + 1] (This is needed to sort the
suffixes according to first 2 characters). If a character is last
character, we store next rank as -1

    Index    Suffix            Rank          Next Rank
     0       banana             1              0
     1       anana              0              13
     2       nana               13             0
     3       ana                0              13
     4       na                 13             0
     5       a                  0             -1 

Sort all Suffixes according to rank and adjacent rank. Rank is
considered as first digit or MSD, and adjacent rank is considered as
second digit.

    Index    Suffix            Rank          Next Rank
     5        a                  0              -1
     1        anana              0               13
     3        ana                0               13
     0        banana             1               0
     2        nana               13              0
     4        na                 13              0  

**Sort according to first four character**  
 Assign new ranks to all suffixes. To assign new ranks, we consider the
sorted suffixes one by one. Assign 0 as new rank to first suffix. For
assigning ranks to remaining suffixes, we consider rank pair of suffix
just before the current suffix. If previous rank pair of a suffix is
same as previous rank of suffix just before it, then assign it same
rank. Otherwise assign rank of previous suffix plus one.

    Index       Suffix          Rank
      5          a               0     [Assign 0 to first]
      1          anana           1     (0, 13) is different from previous
      3          ana             1     (0, 13) is same as previous
      0          banana          2     (1, 0) is different from previous
      2          nana            3     (13, 0) is different from previous
      4          na              3     (13, 0) is same as previous      

For every suffix str[i], also store rank of next suffix at str[i + 2].
If there is no next suffix at i + 2, we store next rank as -1

    Index       Suffix          Rank        Next Rank
      5          a               0             -1
      1          anana           1              1
      3          ana             1              0
      0          banana          2              3
      2          nana            3              3
      4          na              3              -1       

Sort all Suffixes according to rank and next rank.

    Index       Suffix          Rank        Next Rank
      5          a               0             -1
      3          ana             1              0
      1          anana           1              1
      0          banana          2              3
      4          na              3             -1
      2          nana            3              3       

    // C++ program for building suffix array of a given text
    #include <iostream>
    #include <cstring>
    #include <algorithm>
    using namespace std;

    // Structure to store information of a suffix
    struct suffix
    {
        int index; // To store original index
        int rank[2]; // To store ranks and next rank pair
    };

    // A comparison function used by sort() to compare two suffixes
    // Compares two pairs, returns 1 if first pair is smaller
    int cmp(struct suffix a, struct suffix b)
    {
        return (a.rank[0] == b.rank[0])? (a.rank[1] < b.rank[1] ?1: 0):
                   (a.rank[0] < b.rank[0] ?1: 0);
    }

    // This is the main function that takes a string 'txt' of size n as an
    // argument, builds and return the suffix array for the given string
    int *buildSuffixArray(char *txt, int n)
    {
        // A structure to store suffixes and their indexes
        struct suffix suffixes[n];

        // Store suffixes and their indexes in an array of structures.
        // The structure is needed to sort the suffixes alphabatically
        // and maintain their old indexes while sorting
        for (int i = 0; i < n; i++)
        {
            suffixes[i].index = i;
            suffixes[i].rank[0] = txt[i] - 'a';
            suffixes[i].rank[1] = ((i+1) < n)? (txt[i + 1] - 'a'): -1;
        }

        // Sort the suffixes using the comparison function
        // defined above.
        sort(suffixes, suffixes+n, cmp);

        // At his point, all suffixes are sorted according to first
        // 2 characters.  Let us sort suffixes according to first 4
        // characters, then first 8 and so on
        int ind[n];  // This array is needed to get the index in suffixes[]
                     // from original index.  This mapping is needed to get
                     // next suffix.
        for (int k = 4; k < 2*n; k = k*2)
        {
            // Assigning rank and index values to first suffix
            int rank = 0;
            int prev_rank = suffixes[0].rank[0];
            suffixes[0].rank[0] = rank;
            ind[suffixes[0].index] = 0;

            // Assigning rank to suffixes
            for (int i = 1; i < n; i++)
            {
                // If first rank and next ranks are same as that of previous
                // suffix in array, assign the same new rank to this suffix
                if (suffixes[i].rank[0] == prev_rank &&
                        suffixes[i].rank[1] == suffixes[i-1].rank[1])
                {
                    prev_rank = suffixes[i].rank[0];
                    suffixes[i].rank[0] = rank;
                }
                else // Otherwise increment rank and assign
                {
                    prev_rank = suffixes[i].rank[0];
                    suffixes[i].rank[0] = ++rank;
                }
                ind[suffixes[i].index] = i;
            }

            // Assign next rank to every suffix
            for (int i = 0; i < n; i++)
            {
                int nextindex = suffixes[i].index + k/2;
                suffixes[i].rank[1] = (nextindex < n)?
                                      suffixes[ind[nextindex]].rank[0]: -1;
            }

            // Sort the suffixes according to first k characters
            sort(suffixes, suffixes+n, cmp);
        }

        // Store indexes of all sorted suffixes in the suffix array
        int *suffixArr = new int[n];
        for (int i = 0; i < n; i++)
            suffixArr[i] = suffixes[i].index;

        // Return the suffix array
        return  suffixArr;
    }

    // A utility function to print an array of given size
    void printArr(int arr[], int n)
    {
        for (int i = 0; i < n; i++)
            cout << arr[i] << " ";
        cout << endl;
    }

    // Driver program to test above functions
    int main()
    {
        char txt[] = "banana";
        int n = strlen(txt);
        int *suffixArr = buildSuffixArray(txt,  n);
        cout << "Following is suffix array for " << txt << endl;
        printArr(suffixArr, n);
        return 0;
    }

Output:

    Following is suffix array for banana
    5 3 1 0 4 2

Note that the above algorithm uses standard sort function and therefore
time complexity is O(nLognLogn). We can use [Radix
Sort](http://www.geeksforgeeks.org/radix-sort/) here to reduce the time
complexity to O(nLogn).

Please note that suffx arrays can be constructed in O(n) time also. We
will soon be discussing O(n) algorithms.

**References:**  
 <http://www.stanford.edu/class/cs97si/suffix-array.pdf>  
 <http://www.cbcb.umd.edu/confcour/Fall2012/lec14b.pdf>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/suffix-array-set-2-a-nlognlogn-algorithm/>

Ternary Search Tree
-------------------

A ternary search tree is a special trie data structure where the child
nodes of a standard trie are ordered as a binary search tree. <span
id="more-29447"></span>

**Representation of ternary search trees:**  
 Unlike trie(standard) data structure where each node contains 26
pointers for its children, each node in a ternary search tree contains
only 3 pointers:  
 1. The left pointer points to the node whose value is less than the
value in the current node.  
 2. The equal pointer points to the node whose value is equal to the
value in the current node.  
 3. The right pointer points to the node whose value is greater than the
value in the current node.

Apart from above three pointers, each node has a field to indicate
data(character in case of dictionary) and another field to mark end of a
string.  
 So, more or less it is similar to BST which stores data based on some
order. However, data in a ternary search tree is distributed over the
nodes. e.g. It needs 4 nodes to store the word “Geek”.  
 Below figure shows how exactly the words in a ternary search tree are
stored?  

[![](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Ternary-Search-Tree.png "Ternary Search Tree")](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/Ternary-Search-Tree.png)

One of the advantage of using ternary search trees over tries is that
ternary search trees are a more space efficient (involve only three
pointers per node as compared to 26 in standard tries). Further, ternary
search trees can be used any time a hashtable would be used to store
strings.

Tries are suitable when there is a proper distribution of words over the
alphabets so that spaces are utilized most efficiently. Otherwise
ternary search trees are better. Ternary search trees are efficient to
use(in terms of space) when the strings to be stored share a common
prefix.

**Applications of ternary search trees:**  
 **1.** Ternary search trees are efficient for queries like “Given a
word, find the next word in dictionary(near-neighbor lookups)” or “Find
all telephone numbers starting with 9342 or “typing few starting
characters in a web browser displays all website names with this
prefix”(Auto complete feature)”.

**2.** Used in spell checks: Ternary search trees can be used as a
dictionary to store all the words. Once the word is typed in an editor,
the word can be parallely searched in the ternary search tree to check
for correct spelling.

**Implementation:**  
 Following is C implementation of ternary search tree. The operations
implemented are, search, insert and traversal.

    // C program to demonstrate Ternary Search Tree (TST) insert, travese 
    // and search operations
    #include <stdio.h>
    #include <stdlib.h>
    #define MAX 50

    // A node of ternary search tree
    struct Node
    {
        char data;

        // True if this character is last character of one of the words
        unsigned isEndOfString: 1;

        struct Node *left, *eq, *right;
    };

    // A utility function to create a new ternary search tree node
    struct Node* newNode(char data)
    {
        struct Node* temp = (struct Node*) malloc(sizeof( struct Node ));
        temp->data = data;
        temp->isEndOfString = 0;
        temp->left = temp->eq = temp->right = NULL;
        return temp;
    }

    // Function to insert a new word in a Ternary Search Tree
    void insert(struct Node** root, char *word)
    {
        // Base Case: Tree is empty
        if (!(*root))
            *root = newNode(*word);

        // If current character of word is smaller than root's character,
        // then insert this word in left subtree of root
        if ((*word) < (*root)->data)
            insert(&( (*root)->left ), word);

        // If current character of word is greate than root's character,
        // then insert this word in right subtree of root
        else if ((*word) > (*root)->data)
            insert(&( (*root)->right ), word);

        // If current character of word is same as root's character,
        else
        {
            if (*(word+1))
                insert(&( (*root)->eq ), word+1);

            // the last character of the word
            else
                (*root)->isEndOfString = 1;
        }
    }

    // A recursive function to traverse Ternary Search Tree
    void traverseTSTUtil(struct Node* root, char* buffer, int depth)
    {
        if (root)
        {
            // First traverse the left subtree
            traverseTSTUtil(root->left, buffer, depth);

            // Store the character of this node
            buffer[depth] = root->data;
            if (root->isEndOfString)
            {
                buffer[depth+1] = '\0';
                printf( "%s\n", buffer);
            }

            // Traverse the subtree using equal pointer (middle subtree)
            traverseTSTUtil(root->eq, buffer, depth + 1);

            // Finally Traverse the right subtree
            traverseTSTUtil(root->right, buffer, depth);
        }
    }

    // The main function to traverse a Ternary Search Tree.
    // It mainly uses traverseTSTUtil()
    void traverseTST(struct Node* root)
    {
        char buffer[MAX];
        traverseTSTUtil(root, buffer, 0);
    }

    // Function to search a given word in TST
    int searchTST(struct Node *root, char *word)
    {
        if (!root)
            return 0;

        if (*word < (root)->data)
            return searchTST(root->left, word);

        else if (*word > (root)->data)
            return searchTST(root->right, word);

        else
        {
            if (*(word+1) == '\0')
                return root->isEndOfString;

            return searchTST(root->eq, word+1);
        }
    }

    // Driver program to test above functions
    int main()
    {
        struct Node *root = NULL;

        insert(&root, "cat");
        insert(&root, "cats");
        insert(&root, "up");
        insert(&root, "bug");

        printf("Following is traversal of ternary search tree\n");
        traverseTST(root);

        printf("\nFollowing are search results for cats, bu and cat respectively\n");
        searchTST(root, "cats")? printf("Found\n"): printf("Not Found\n");
        searchTST(root, "bu")?   printf("Found\n"): printf("Not Found\n");
        searchTST(root, "cat")?  printf("Found\n"): printf("Not Found\n");

        return 0;
    }

Output:

    Following is traversal of ternary search tree
    bug
    cat
    cats
    up

    Following are search results for cats, bu and cat respectively
    Found
    Not Found
    Found

**Time Complexity:** The time complexity of the ternary search tree
operations is similar to that of binary search tree. i.e. the insertion,
deletion and search operations take time proportional to the height of
the ternary search tree. The space is proportional to the length of the
string to be stored.

**Reference:**  
 <http://en.wikipedia.org/wiki/Ternary_search_tree>

This article is compiled by **[Aashish
Barnwal](https://www.facebook.com/barnwal.aashish)**and reviewed by
GeeksforGeeks team. Please write comments if you find anything
incorrect, or you want to share more information about the topic
discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/),
[Advanced Data
Structures](http://www.geeksforgeeks.org/tag/advanced-data-structures/)

### Source:

<http://www.geeksforgeeks.org/ternary-search-tree/>

Trie | (Delete)
---------------

In the [previous post](http://www.geeksforgeeks.org/archives/13067) on
[trie](http://en.wikipedia.org/wiki/Trie) we have described how to
insert and search a node in trie. Here is an algorithm how to delete a
node from trie.<span id="more-15886"></span>

During delete operation we delete the key in bottom up manner using
recursion. The following are possible conditions when deleting key from
trie,

1.  Key may not be there in trie. Delete operation should not modify
    trie.
2.  Key present as unique key (no part of key contains another key
    (prefix), nor the key itself is prefix of another key in trie).
    Delete all the nodes.
3.  Key is prefix key of another long key in trie. Unmark the leaf node.
4.  Key present in trie, having atleast one other key as prefix key.
    Delete nodes from end of key until first leaf node of longest prefix
    key.

The highlighted code presents algorithm to implement above conditions.
(One may be in dilemma how a pointer passed to delete helper is
reflecting changes from deleteHelper to deleteKey. Note that we are
holding trie as an ADT in trie\_t node, which is passed by reference or
pointer).

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    #define ARRAY_SIZE(a) sizeof(a)/sizeof(a[0])

    // Alphabet size (# of symbols)

    #define ALPHABET_SIZE (26)
    #define INDEX(c) ((int)c - (int)'a')

    #define FREE(p) \
        free(p);    \
        p = NULL;

    // forward declration
    typedef struct trie_node trie_node_t;

    // trie node
    struct trie_node
    {
        int value; // non zero if leaf
        trie_node_t *children[ALPHABET_SIZE];
    };

    // trie ADT
    typedef struct trie trie_t;

    struct trie
    {
        trie_node_t *root;
        int count;
    };

    trie_node_t *getNode(void)
    {
        trie_node_t *pNode = NULL;

        pNode = (trie_node_t *)malloc(sizeof(trie_node_t));

        if( pNode )
        {
            int i;

            pNode->value   = 0;

            for(i = 0; i < ALPHABET_SIZE; i++)
            {
                pNode->children[i] = NULL;
            }
        }

        return pNode;
    }

    void initialize(trie_t *pTrie)
    {
        pTrie->root = getNode();
        pTrie->count = 0;
    }

    void insert(trie_t *pTrie, char key[])
    {
        int level;
        int length = strlen(key);
        int index;
        trie_node_t *pCrawl;

        pTrie->count++;
        pCrawl = pTrie->root;

        for( level = 0; level < length; level++ )
        {
            index = INDEX(key[level]);

            if( pCrawl->children[index] )
            {
                // Skip current node
                pCrawl = pCrawl->children[index];
            }
            else
            {
                // Add new node
                pCrawl->children[index] = getNode();
                pCrawl = pCrawl->children[index];
            }
        }

        // mark last node as leaf (non zero)
        pCrawl->value = pTrie->count;
    }

    int search(trie_t *pTrie, char key[])
    {
        int level;
        int length = strlen(key);
        int index;
        trie_node_t *pCrawl;

        pCrawl = pTrie->root;

        for( level = 0; level < length; level++ )
        {
            index = INDEX(key[level]);

            if( !pCrawl->children[index] )
            {
                return 0;
            }

            pCrawl = pCrawl->children[index];
        }

        return (0 != pCrawl && pCrawl->value);
    }

    int leafNode(trie_node_t *pNode)
    {
        return (pNode->value != 0);
    }

    int isItFreeNode(trie_node_t *pNode)
    {
        int i;
        for(i = 0; i < ALPHABET_SIZE; i++)
        {
            if( pNode->children[i] )
                return 0;
        }

        return 1;
    }

    bool deleteHelper(trie_node_t *pNode, char key[], int level, int len)
    {
        if( pNode )
        {
            // Base case
            if( level == len )
            {
                if( pNode->value )
                {
                    // Unmark leaf node
                    pNode->value = 0;

                    // If empty, node to be deleted
                    if( isItFreeNode(pNode) )
                    {
                        return true;
                    }

                    return false;
                }
            }
            else // Recursive case
            {
                int index = INDEX(key[level]);

                if( deleteHelper(pNode->children[index], key, level+1, len) )
                {
                    // last node marked, delete it
                    FREE(pNode->children[index]);

                    // recursively climb up, and delete eligible nodes
                    return ( !leafNode(pNode) && isItFreeNode(pNode) );
                }
            }
        }

        return false;
    }

    void deleteKey(trie_t *pTrie, char key[])
    {
        int len = strlen(key);

        if( len > 0 )
        {
            deleteHelper(pTrie->root, key, 0, len);
        }
    }

    int main()
    {
        char keys[][8] = {"she", "sells", "sea", "shore", "the", "by", "sheer"};
        trie_t trie;

        initialize(&trie);

        for(int i = 0; i < ARRAY_SIZE(keys); i++)
        {
            insert(&trie, keys[i]);
        }

        deleteKey(&trie, keys[0]);

        printf("%s %s\n", "she", search(&trie, "she") ? "Present in trie" : "Not present in trie");

        return 0;
    }

â€”Â **[Venki](http://www.linkedin.com/in/ramanawithu)**. Please write
comments if you find anything incorrect, or you want to share more
information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/)

### Source:

<http://www.geeksforgeeks.org/trie-delete/>

Trie | (Insert and Search)
--------------------------

[Trie](http://en.wikipedia.org/wiki/Trie) is an efficient information
re***trie***val data structure. Using trie, search complexities can be
brought to optimal limit (key length). <span id="more-13067"></span>If
we store keys in binary search tree, a well balanced BST will need
timeÂ proportionalÂ to **M \* log N**, where M is maximum string length
and N is number of keys in tree. Using trie, we can search the key in
O(M) time. However the penalty is on trie storage requirements.

Every node of trie consists of multiple branches. Each branch represents
a possible character of keys. We need to mark the last node of every key
as leaf node. A trie node field *value* will be used to distinguish the
node as leaf node (there are other uses of the *value* field). A simple
structure to represent nodes of English alphabet can be as following,

`struct` `trie_node`

`{`

`Â Â Â Â ``int` `value; /* Used to mark leaf nodes */`

`Â Â Â Â ``trie_node_t *children[ALPHABET_SIZE];`

`};`

Inserting a key into trie is simple approach. Every character of input
key is inserted as an individual trie node. Note that the *children* is
an array of pointers to next level trie nodes. The key character acts as
an index into the array *children*. If the input key is new or an
extension of existing key, we need to construct non-existing nodes of
the key, and mark leaf node. If the input key is prefix of existing key
in trie, we simply mark the last node of key as leaf. The key length
determines trie depth.

Searching for a key is similar to insert operation, however we only
compare the characters and move down. The search can terminate due to
end of string or lack of key in trie. In theÂ formerÂ case, if the
*value* field of last node is non-zero then the key exists in trie. In
the second case, the search terminates without examining all the
characters of key, since the key is not present in trie.

The following picture explains construction of trie using keys given in
the example below,

                           root
                        /   \    \
                        t   a     b
                        |   |     |
                        h   n     y
                        |   |  \  |
                        e   s  y  e
                     /  |   |
                     i  r   w
                     |  |   |
                     r  e   e
                            |
                            r

In the picture, every character is of typeÂ *trie\_node\_t*. For
example, the *root* is of typeÂ trie\_node\_t, and it’s children *a*,
*b* and *t* are filled, all other nodes of root will be NULL. Similarly,
“a” at the next level is having only one child (“n”), all other children
are NULL. The leaf nodes are in <span>blue</span>.

Insert and search costs **O(key\_length)**, however the memory
requirements of trie is **O(ALPHABET\_SIZE \* key\_length \* N)**Â where
N is number of keys in trie. There are efficient representation of trie
nodes (e.g. compressed trie,Â [ternaryÂ search
tree](http://en.wikipedia.org/wiki/Ternary_search_tree), etc.)
toÂ minimizeÂ memory requirements of trie.

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    #define ARRAY_SIZE(a) sizeof(a)/sizeof(a[0])

    // Alphabet size (# of symbols)
    #define ALPHABET_SIZE (26)
    // Converts key current character into index
    // use only 'a' through 'z' and lower case
    #define CHAR_TO_INDEX(c) ((int)c - (int)'a')

    // trie node
    typedef struct trie_node trie_node_t;
    struct trie_node
    {
        int value;
        trie_node_t *children[ALPHABET_SIZE];
    };

    // trie ADT
    typedef struct trie trie_t;
    struct trie
    {
        trie_node_t *root;
        int count;
    };

    // Returns new trie node (initialized to NULLs)
    trie_node_t *getNode(void)
    {
        trie_node_t *pNode = NULL;

        pNode = (trie_node_t *)malloc(sizeof(trie_node_t));

        if( pNode )
        {
            int i;

            pNode->value = 0;

            for(i = 0; i < ALPHABET_SIZE; i++)
            {
                pNode->children[i] = NULL;
            }
        }

        return pNode;
    }

    // Initializes trie (root is dummy node)
    void initialize(trie_t *pTrie)
    {
        pTrie->root = getNode();
        pTrie->count = 0;
    }

    // If not present, inserts key into trie
    // If the key is prefix of trie node, just marks leaf node
    void insert(trie_t *pTrie, char key[])
    {
        int level;
        int length = strlen(key);
        int index;
        trie_node_t *pCrawl;

        pTrie->count++;
        pCrawl = pTrie->root;

        for( level = 0; level < length; level++ )
        {
            index = CHAR_TO_INDEX(key[level]);
            if( !pCrawl->children[index] )
            {
                pCrawl->children[index] = getNode();
            }

            pCrawl = pCrawl->children[index];
        }

        // mark last node as leaf
        pCrawl->value = pTrie->count;
    }

    // Returns non zero, if key presents in trie
    int search(trie_t *pTrie, char key[])
    {
        int level;
        int length = strlen(key);
        int index;
        trie_node_t *pCrawl;

        pCrawl = pTrie->root;

        for( level = 0; level < length; level++ )
        {
            index = CHAR_TO_INDEX(key[level]);

            if( !pCrawl->children[index] )
            {
                return 0;
            }

            pCrawl = pCrawl->children[index];
        }

        return (0 != pCrawl && pCrawl->value);
    }

    // Driver
    int main()
    {
        // Input keys (use only 'a' through 'z' and lower case)
        char keys[][8] = {"the", "a", "there", "answer", "any", "by", "bye", "their"};
        trie_t trie;

        char output[][32] = {"Not present in trie", "Present in trie"};

        initialize(&trie);

        // Construct trie
        for(int i = 0; i < ARRAY_SIZE(keys); i++)
        {
            insert(&trie, keys[i]);
        }

        // Search for different keys
        printf("%s --- %s\n", "the", output[search(&trie, "the")] );
        printf("%s --- %s\n", "these", output[search(&trie, "these")] );
        printf("%s --- %s\n", "their", output[search(&trie, "their")] );
        printf("%s --- %s\n", "thaw", output[search(&trie, "thaw")] );

        return 0;
    }

—Â **[Venki](http://www.linkedin.com/in/ramanawithu)**. Please write
comments if you find anything incorrect, or you want to share more
information about the topic discussed above.

         
Tags: [Advance Data
Structures](http://www.geeksforgeeks.org/tag/advance-data-structures/)

### Source:

<http://www.geeksforgeeks.org/trie-insert-and-search/>


