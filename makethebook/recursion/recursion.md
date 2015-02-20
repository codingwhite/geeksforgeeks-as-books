Check if a number is Palindrome
-------------------------------

Given an integer, write a function that returns true if the given number
is palindrome, else false. For example, 12321 is palindrome, but 1451 is
not palindrome. <span id="more-116532"></span>

Let the given number be *num*. A simple method for this problem is to
first [reverse digits of
*num*](http://www.geeksforgeeks.org/write-a-c-program-to-reverse-digits-of-a-number/),
then compare the reverse of *num* with *num*. If both are same, then
return true, else false.

Following is an interesting method inspired from method\#2 of
[this](http://www.geeksforgeeks.org/function-to-check-if-a-singly-linked-list-is-palindrome/)post.
The idea is to create a copy of *num* and recursively pass the copy by
reference, and pass *num* by value. In the recursive calls, divide *num*
by 10 while moving down the recursion tree. While moving up the
recursion tree, divide the copy by 10. When they meet in a function for
which all child calls are over, the last digit of *num* will be ith
digit from the beginning and the last digit of copy will be ith digit
from the end.

    // A recursive C++ program to check whether a given number is
    // palindrome or not
    #include <stdio.h>

    // A function that reurns true only if num contains one digit
    int oneDigit(int num)
    {
        // comparison operation is faster than division operation.
        // So using following instead of "return num / 10 == 0;"
        return (num >= 0 && num < 10);
    }

    // A recursive function to find out whether num is palindrome
    // or not. Initially, dupNum contains address of a copy of num.
    bool isPalUtil(int num, int* dupNum)
    {
        // Base case (needed for recursion termination): This statement
        // mainly compares the first digit with the last digit
        if (oneDigit(num))
            return (num == (*dupNum) % 10);

        // This is the key line in this method. Note that all recursive
        // calls have a separate copy of num, but they all share same copy
        // of *dupNum. We divide num while moving up the recursion tree
        if (!isPalUtil(num/10, dupNum))
            return false;

        // The following statements are executed when we move up the
        // recursion call tree
        *dupNum /= 10;

        // At this point, if num%10 contains i'th digit from beiginning,
        // then (*dupNum)%10 contains i'th digit from end
        return (num % 10 == (*dupNum) % 10);
    }

    // The main function that uses recursive function isPalUtil() to
    // find out whether num is palindrome or not
    int isPal(int num)
    {
        // If num is negative, make it positive
        if (num < 0)
           num = -num;

        // Create a separate copy of num, so that modifications made
        // to address dupNum don't change the input number.
        int *dupNum = new int(num); // *dupNum = num

        return isPalUtil(num, dupNum);
    }

    // Driver program to test above functions
    int main()
    {
        int n = 12321;
        isPal(n)? printf("Yes\n"): printf("No\n");

        n = 12;
        isPal(n)? printf("Yes\n"): printf("No\n");

        n = 88;
        isPal(n)? printf("Yes\n"): printf("No\n");

        n = 8999;
        isPal(n)? printf("Yes\n"): printf("No\n");
        return 0;
    }

Output:

    Yes
    No
    Yes
    No

This article is compiled by[Aashish
Barnwal](https://www.facebook.com/barnwal.aashish?fref=ts). Please write
comments if you find anything incorrect, or you want to share more
information about the topic discussed above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/check-if-a-number-is-palindrome/>

Practice questions for Linked List and Recursion
------------------------------------------------

Assume the structure of a Linked List node is as follows. <span
id="more-6803"></span>

    struct node
    {
      int data;
      struct node *next;
    };

Explain the functionality of following C functions.

**1. What does the following function do for a given Linked List?**

    void fun1(struct node* head)
    {
      if(head == NULL)
        return;
     
      fun1(head->next);
      printf("%d  ", head->data);
    }

fun1() prints the given Linked List in reverse manner. For Linked List
1-\>2-\>3-\>4-\>5, fun1() prints 5-\>4-\>3-\>2-\>1.

  
 **2. What does the following function do for a given Linked List ?**

    void fun2(struct node* head)
    {
      if(head== NULL)
        return;
      printf("%d  ", head->data); 

      if(head->next != NULL )
        fun2(head->next->next);
      printf("%d  ", head->data);   
    }

fun2() prints alternate nodes of the given Linked List, first from head
to end, and then from end to head. If Linked List has even number of
nodes, then fun2() skips the last node. For Linked List
1-\>2-\>3-\>4-\>5, fun2() prints 1 3 5 5 3 1. For Linked List
1-\>2-\>3-\>4-\>5-\>6, fun2() prints 1 3 5 5 3 1.

Below is a complete running program to test above functions.

    #include<stdio.h>
    #include<stdlib.h>

    /* A linked list node */
    struct node
    {
      int data;
      struct node *next;
    };


    /* Prints a linked list in reverse manner */
    void fun1(struct node* head)
    {
      if(head == NULL)
        return;

      fun1(head->next);
      printf("%d  ", head->data);
    }

    /* prints alternate nodes of a Linked List, first 
      from head to end, and then from end to head. */
    void fun2(struct node* start)
    {
      if(start == NULL)
        return;
      printf("%d  ", start->data); 

      if(start->next != NULL )
        fun2(start->next->next);
      printf("%d  ", start->data);
    }

    /* UTILITY FUNCTIONS TO TEST fun1() and fun2() */
    /* Given a reference (pointer to pointer) to the head
      of a list and an int, push a new node on the front
      of the list. */
    void push(struct node** head_ref, int new_data)
    {
      /* allocate node */
      struct node* new_node =
              (struct node*) malloc(sizeof(struct node));
     
      /* put in the data  */
      new_node->data  = new_data;
     
      /* link the old list off the new node */
      new_node->next = (*head_ref);
     
      /* move the head to point to the new node */
      (*head_ref)    = new_node;
    }
     
    /* Drier program to test above functions */
    int main()
    {
      /* Start with the empty list */
      struct node* head = NULL;

      /* Using push() to construct below list
        1->2->3->4->5  */
      push(&head, 5);
      push(&head, 4);
      push(&head, 3);
      push(&head, 2);
      push(&head, 1);   
     
      printf("\n Output of fun1() for list 1->2->3->4->5 \n");
      fun1(head);

      printf("\n Output of fun2() for list 1->2->3->4->5 \n"); 
      fun2(head);
            
      getchar();
      return 0;
    }

Please write comments if you find any of the answers/explanations
incorrect, or you want to share more information about the topics
discussed above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-linked-list-and-recursion/>

Practice Questions for Recursion | Set 2
----------------------------------------

Explain the functionality of following functions. <span
id="more-7553"></span>

**Question 1**

    /* Assume that n is greater than or equal to 1 */
    int fun1(int n)
    {
      if(n == 1)
         return 0;
      else
         return 1 + fun1(n/2);
    } 

Answer: The function calculates and returns ![\\lfloor\\log \_2 \\left(
n
\\right)\\rfloor](http://d2o58evtke57tz.cloudfront.net/wp-content/ql-cache/quicklatex.com-4cd233403b8ed2d918d2b2fc609b1575_l3.png "Rendered by QuickLaTeX.com").
For example, if n is between 8 and 15 then fun1() returns 3. If n is
between 16 to 31 then fun1() returns 4.

  
 **Question 2**

    /* Assume that n is greater than or equal to 0 */
    void fun2(int n)
    {
      if(n == 0)
        return;

      fun2(n/2);
      printf("%d", n%2);
    }  

Answer: The function fun2() prints binary equivalent of n. For example,
if n is 21 then fun2() prints 10101.

Note that above functions are just for practicing recursion, they are
not the ideal implementation of the functionality they provide.

Please write comments if you find any of the answers/codes incorrect.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion-set-2/>

Practice Questions for Recursion | Set 3
----------------------------------------

Explain the functionality of below recursive functions. <span
id="more-8095"></span>

**Question 1**

    void fun1(int n)
    {
       int i = 0;  
       if (n > 1)
         fun1(n-1);
       for (i = 0; i < n; i++)
         printf(" * ");
    }

Answer: Total numbers of stars printed is equal to 1 + 2 + â€¦. (n-2) +
(n-1) + n, which is n(n+1)/2.

  
 **Question 2**

    #define LIMIT 1000
    void fun2(int n)
    {
      if (n <= 0)
         return;
      if (n > LIMIT)
        return;
      printf("%d ", n);
      fun2(2*n);
      printf("%d ", n);
    }   

Answer: For a positive n, fun2(n) prints the values of n, 2n, 4n, 8n â€¦
while the value is smaller than LIMIT. After printing values in
increasing order, it prints same numbers again in reverse order. For
example fun2(100) prints 100, 200, 400, 800, 800, 400, 200, 100.  
 If n is negative, then it becomes a non-terminating recursion and
causes overflow.

Please write comments if you find any of the answers/codes incorrect, or
you want to share more information about the topics discussed above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion-set-3/>

Practice Questions for Recursion | Set 4
----------------------------------------

**Question 1**  
 Predict the output of following program. <span id="more-8953"></span>

    #include<stdio.h>
    void fun(int x)
    {
      if(x > 0)
      {
         fun(--x);
         printf("%d\t", x);
         fun(--x);
      }
    }

    int main()
    {
      int a = 4;
      fun(a);
      getchar();
      return 0;
    }

Output: 0 1 2 0 3 0 1

     
                       fun(4);
                       /
                    fun(3), print(3), fun(2)(prints 0 1)
                   /
               fun(2), print(2), fun(1)(prints 0)
               /
           fun(1), print(1), fun(0)(does nothing)
           /
        fun(0), print(0), fun(-1) (does nothing)

**Question 2**  
 Predict the output of following program. What does the following fun()
do in general?

    int fun(int a[],int n)
    {
      int x;
      if(n == 1)
        return a[0];
      else
        x = fun(a, n-1);
      if(x > a[n-1])
        return x;
      else
        return a[n-1];
    }

    int main()
    {
      int arr[] = {12, 10, 30, 50, 100};
      printf(" %d ", fun(arr, 5));
      getchar();
      return 0;
    }

Output: 100  
 fun() returns the maximum value in the input array a[] of size n.

**Question 3**  
 Predict the output of following program. What does the following fun()
do in general?

    int fun(int i)
    {
      if ( i%2 ) return (i++);
      else return fun(fun( i - 1 ));
    }

    int main()
    {
      printf(" %d ", fun(200));
      getchar();
      return 0;
    }

Output: 199  
 If n is odd then returns n, else returns (n-1). Eg., for n = 12, you
get 11 and for n = 11 you get 11. The statement *â€œreturn i++;â€?*
returns value of i only as it is a post increment.

Please write comments if you find any of the answers/codes incorrect, or
you want to share more information/questions about the topics discussed
above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion-set-4/>

Practice Questions for Recursion | Set 5
----------------------------------------

**Question 1**

Predict the output of following program. What does the following fun()
do in general? <span id="more-11559"></span>

    #include<stdio.h>

    int fun(int a, int b) 
    {
       if (b == 0)
           return 0;
       if (b % 2 == 0)
           return fun(a+a, b/2);

       return fun(a+a, b/2) + a;
    }

    int main()
    {
      printf("%d", fun(4, 3));
      getchar();
      return 0;
    }

Output: 12

It calulates a\*b (a multipied b).

  
 **Question 2**  
 In question 1, if we replace + with \* and replace return 0 with return
1, then what does the changed function do? Following is the changed
function.

    #include<stdio.h>

    int fun(int a, int b)
    {
       if (b == 0)
           return 1;
       if (b % 2 == 0)
           return fun(a*a, b/2);

       return fun(a*a, b/2)*a;
    }

    int main()
    {
      printf("%d", fun(4, 3));
      getchar();
      return 0;
    }

Output: 64  
 It calulates a^b (a raised to power b).

  
 **Question 3**  
 Predict the output of following program. What does the following fun()
do in general?

    #include<stdio.h>

     int fun(int n)
     {
       if (n > 100)
         return n - 10;
       return fun(fun(n+11));
     }

    int main()
    {
      printf(" %d ", fun(99));
      getchar();
      return 0;
    }

Output: 91

    fun(99) = fun(fun(110)) since 99 ? 100
               = fun(100)    since 110 > 100
               = fun(fun(111)) since 100 ? 100
               = fun(101)    since 111 > 100
               = 91        since 101 > 100

Returned value of fun() is 91 for all integer rguments n 101. This
function is known as [McCarthy 91
function](http://en.wikipedia.org/wiki/McCarthy_91_function).

Please write comments if you find any of the answers/codes incorrect, or
you want to share more information/questions about the topics discussed
above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion-set-5/>

Practice Questions for Recursion | Set 6
----------------------------------------

**Question 1**  
 Consider the following recursive C function. Let *len* be the length of
the string s and *num* be the number of characters printed on the
screen<span id="more-14124"></span>, give the relation between *num* and
*len* where *len* is always greater than 0.

    void abc(char *s)
    {
        if(s[0] == '\0')
            return;

        abc(s + 1);
        abc(s + 1);
        printf("%c", s[0]);    
    }

Following is the relation between *num* and *len*.

     num = 2^len-1 

    s[0] is 1 time printed
    s[1] is 2 times printed
    s[2] is 4 times printed
    s[i] is printed 2^i times
    s[strlen(s)-1] is printed 2^(strlen(s)-1) times
    total = 1+2+....+2^(strlen(s)-1)
          = (2^strlen(s)) - 1 

For example, the following program prints 7 characters.

    #include<stdio.h>

    void abc(char *s)
    {
        if(s[0] == '\0')
            return;

        abc(s + 1);
        abc(s + 1);
        printf("%c", s[0]);
    }

    int main()
    {
        abc("xyz");
        return 0;
    }

Thanks to [bharat
nag](http://geeksforgeeks.org/forum/topic/microsoft-interview-question-for-software-engineerdeveloper-fresher-about-cpuzzles-5#post-30273)
for suggesting this solution.

  
 **Question 2**

    #include<stdio.h>
    int fun(int count)
    {
        printf("%d\n", count);
        if(count < 3)
        {
          fun(fun(fun(++count)));
        }
        return count;
    }

    int main()
    {
        fun(1);
        return 0;
    }

Output:

     1
     2
     3
     3
     3
     3
     3

The main() function calls fun(1). fun(1) prints â€œ1â€? and calls
fun(fun(fun(2))). fun(2) prints â€œ2â€? and calls fun(fun(fun(3))). So
the function call sequence becomes fun(fun(fun(fun(fun(3))))). fun(3)
prints â€œ3â€? and returns 3 (note that count is not incremented and no
more functions are called as the if condition is not true for count 3).
So the function call sequence reduces to fun(fun(fun(fun(3)))). fun(3)
again prints â€œ3â€? and returns 3. So the function call again reduces
to fun(fun(fun(3))) which again prints â€œ3â€? and reduces to
fun(fun(3)). This continues and we get â€œ3â€? printed 5 times on the
screen.

Please write comments if you find any of the answers/codes incorrect, or
you want to share more information/questions about the topics discussed
above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion-set-6/>

Practice Questions for Recursion | Set 7
----------------------------------------

**Question 1** Predict the output of the following program. What does
the following fun() do in general? <span id="more-15391"></span>

    #include <stdio.h>

    int fun ( int n, int *fp )
    {
        int t, f;

        if ( n <= 1 )
        {
            *fp = 1;
            return 1;
        }
        t = fun ( n-1, fp );
        f = t + *fp;
        *fp = t;
        return f;
    }

    int main()
    {
        int x = 15;
        printf("%d\n",fun(5, &x));

        return 0;
    }

Output:

    8 

The program calculates nth Fibonacci Number. The statement t = fun (
n-1, fp ) gives the (n-1)th Fibonacci number and \*fp is used to store
the (n-2)th Fibonacci Number. Initial value of \*fp (which is 15 in the
above prgram) doesnâ€™t matter. Following recursion tree shows all steps
from 1 to 10, for exceution of fun(5, &x).

                                  (1) fun(5, fp)
                                  /           \
                             (2) fun(4, fp)  (10) t = 5, f = 8, *fp = 5
                             /          \
                       (3) fun(3, fp)  (9) t = 3, f = 5, *fp = 3
                      /            \
               (4) fun(2, fp)      (8) t = 2, f = 3, *fp = 2
              /          \
       (5) fun(1, fp)   (7) t = 1, f = 2, *fp = 1
       /
    (6) *fp = 1

  
 **Question 2:** Predict the output of the following program.

    #include <stdio.h>

    void fun(int n)
    {
        if(n > 0)
        {
            fun(n-1);
            printf("%d ", n);
            fun(n-1);
        }
    }

    int main()
    {
        fun(4);
        return 0;
    }

Output

    1 2 1 3 1 2 1 4 1 2 1 3 1 2 1

                         fun(4)
                       /
                    fun(3), print(4), fun(3) [fun(3) prints 1 2 1 3 1 2 1]
                   /
               fun(2), print(3), fun(2) [fun(2) prints 1 2 1]
               /
           fun(1), print(2), fun(1) [fun(1) prints 1]
           /
        fun(0), print(1), fun(0) [fun(0) does nothing]

Please write comments if you find any of the answers/codes incorrect, or
you want to share more information/questions about the topics discussed
above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion-set-7/>

Practice Questions for Recursion | Set 1
----------------------------------------

Explain the functionality of following functions. <span
id="more-6941"></span>

**Question 1**

    int fun1(int x, int y) 
    {
      if(x == 0)
        return y;
      else
        return fun1(x - 1,  x + y);
    }

Answer: The function fun() calculates and returns ((1 + 2 Ã¢Â€Â¦ + x-1 +
x) +y) which is x(x+1)/2 + y. For example if x is 5 and y is 2, then fun
should return 15 + 2 = 17.

  
 **Question 2**

    void fun2(int arr[], int start_index, int end_index)
    {
      if(start_index >= end_index)   
         return;
      int min_index; 
      int temp; 

      /* Assume that minIndex() returns index of minimum value in 
        array arr[start_index...end_index] */
      min_index = minIndex(arr, start_index, end_index);

      temp = arr[start_index];
      arr[start_index] = arr[min_index];
      arr[min_index] = temp;        

      fun2(arr, start_index + 1, end_index);
    }     

Answer: The function fun2() is a recursive implementation of [Selection
Sort](http://en.wikipedia.org/wiki/Selection_sort).

Please write comments if you find any of the answers/codes incorrect, or
you want to share more information about the topics discussed above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/practice-questions-for-recursion/>

Print all possible strings of length k that can be formed from a set of n characters
------------------------------------------------------------------------------------

Given a set of characters and a positive integer k, print all possible
strings of length k that can be formed from the given set.<span
id="more-119940"></span>

Examples:

    Input: 
    set[] = {'a', 'b'}, k = 3

    Output:
    aaa
    aab
    aba
    abb
    baa
    bab
    bba
    bbb


    Input: 
    set[] = {'a', 'b', 'c', 'd'}, k = 1
    Output:
    a
    b
    c
    d

For a given set of size n, there will be n^k possible strings of length
k. The idea is to start from an empty output string (we call it *prefix*
in following code). One by one add all characters to *prefix*. For every
character added, print all possible strings with current prefix by
recursively calling for k equals to k-1.  
 Following is Java implementation for same.

    // Java program to print all possible strings of length k
    class PrintAllKLengthStrings {

        // Driver method to test below methods
        public static void main(String[] args) {             
            System.out.println("First Test");
            char set1[] = {'a', 'b'};
            int k = 3;
            printAllKLength(set1, k);
            
            System.out.println("\nSecond Test");
            char set2[] = {'a', 'b', 'c', 'd'};
            k = 1;
            printAllKLength(set2, k);        
        }    

        // The method that prints all possible strings of length k.  It is
        //  mainly a wrapper over recursive function printAllKLengthRec()
        static void printAllKLength(char set[], int k) {
            int n = set.length;        
            printAllKLengthRec(set, "", n, k);
        }

        // The main recursive method to print all possible strings of length k
        static void printAllKLengthRec(char set[], String prefix, int n, int k) {
            
            // Base case: k is 0, print prefix
            if (k == 0) {
                System.out.println(prefix);
                return;
            }

            // One by one add all characters from set and recursively 
            // call for k equals to k-1
            for (int i = 0; i < n; ++i) {
                
                // Next character of input added
                String newPrefix = prefix + set[i]; 
                
                // k is decreased, because we have added a new character
                printAllKLengthRec(set, newPrefix, n, k - 1); 
            }
        }
    }

Output:

    First Test
    aaa
    aab
    aba
    abb
    baa
    bab
    bba
    bbb

    Second Test
    a
    b
    c
    d

The above solution is mainly generalization of [this
post](http://www.geeksforgeeks.org/print-all-permutations-with-repetition-of-characters/).

This article is contriibuted by **[Abhinav
Ramana](https://plus.google.com/104230157879525004164/posts)**. Please
write comments if you find anything incorrect, or you want to share more
information about the topic discussed above

Â  Â 
Tags: [combionatrics](http://www.geeksforgeeks.org/tag/combionatrics/),
[Java](http://www.geeksforgeeks.org/tag/java/),
[Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/print-all-combinations-of-given-length/>

Print all possible combinations of r elements in a given array of size n
------------------------------------------------------------------------

Given an array of size n, generate and print all possible combinations
of r elements in array. For example, if input array is {1, 2, 3, 4} and
r is 2, then output should be {1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4} and
{3, 4}.<span id="more-118604"></span>

Following are two methods to do this.

**Method 1 (Fix Elements and Recur)**  
 We create a temporary array â€˜data[]â€™ which stores all outputs one
by one. The idea is to start from first index (index = 0) in data[], one
by one fix elements at this index and recur for remaining indexes. Let
the input array be {1, 2, 3, 4, 5} and r be 3. We first fix 1 at index 0
in data[], then recur for remaining indexes, then we fix 2 at index 0
and recur. Finally, we fix 3 and recur for remaining indexes. When
number of elements in data[] becomes equal to r (size of a combination),
we print data[].

Following diagram shows recursion tree for same input.

[![combination](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/combination.png)](http://d2o58evtke57tz.cloudfront.net/wp-content/uploads/combination.png)

Following is C++ implementation of above approach.

    // Program to print all combination of size r in an array of size n
    #include <stdio.h>
    void combinationUtil(int arr[], int data[], int start, int end, int index, int r);

    // The main function that prints all combinations of size r
    // in arr[] of size n. This function mainly uses combinationUtil()
    void printCombination(int arr[], int n, int r)
    {
        // A temporary array to store all combination one by one
        int data[r];

        // Print all combination using temprary array 'data[]'
        combinationUtil(arr, data, 0, n-1, 0, r);
    }

    /* arr[]  ---> Input Array
       data[] ---> Temporary array to store current combination
       start & end ---> Staring and Ending indexes in arr[]
       index  ---> Current index in data[]
       r ---> Size of a combination to be printed */
    void combinationUtil(int arr[], int data[], int start, int end, int index, int r)
    {
        // Current combination is ready to be printed, print it
        if (index == r)
        {
            for (int j=0; j<r; j++)
                printf("%d ", data[j]);
            printf("\n");
            return;
        }

        // replace index with all possible elements. The condition
        // "end-i+1 >= r-index" makes sure that including one element
        // at index will make a combination with remaining elements
        // at remaining positions
        for (int i=start; i<=end && end-i+1 >= r-index; i++)
        {
            data[index] = arr[i];
            combinationUtil(arr, data, i+1, end, index+1, r);
        }
    }

    // Driver program to test above functions
    int main()
    {
        int arr[] = {1, 2, 3, 4, 5};
        int r = 3;
        int n = sizeof(arr)/sizeof(arr[0]);
        printCombination(arr, n, r);
    }

Output:

    1 2 3
    1 2 4
    1 2 5
    1 3 4
    1 3 5
    1 4 5
    2 3 4
    2 3 5
    2 4 5
    3 4 5

*How to handle duplicates?*  
 Note that the above method doesnâ€™t handle duplicates. For example, if
input array is {1, 2, 1} and r is 2, then the program prints {1, 2} and
{2, 1} as two different combinations. We can avoid duplicates by adding
following two additional things to above code.  
 1) Add code to sort the array before calling combinationUtil() in
printCombination()  
 2) Add following lines at the end of for loop in combinationUtil()

            // Since the elements are sorted, all occurrences of an element
            // must be together
            while (arr[i] == arr[i+1])
                 i++; 

See **[this](http://ideone.com/ywsqBz)**for an implementation that
handles duplicates.

  
 **Method 2 (Include and Exclude every element)**  
 Like the above method, We create a temporary array data[]. The idea
here is similar to [Subset Sum
Problem](http://www.geeksforgeeks.org/dynamic-programming-subset-sum-problem/).
We one by one consider every element of input array, and recur for two
cases:

1) The element is included in current combination (We put the element in
data[] and increment next available index in data[])  
 2) The element is excluded in current combination (We do not put the
element and do not change index)

When number of elements in data[] become equal to r (size of a
combination), we print it.

This method is mainly based on [Pascalâ€™s
Identity](http://en.wikipedia.org/wiki/Pascal's_rule), i.e.
**n<sub>c<sub>r</sub></sub> = n-1<sub>c<sub>r</sub></sub> +
n-1<sub>c<sub>r-1</sub></sub>**

Following is C++ implementation of method 2.

    // Program to print all combination of size r in an array of size n
    #include<stdio.h>
    void combinationUtil(int arr[],int n,int r,int index,int data[],int i);

    // The main function that prints all combinations of size r
    // in arr[] of size n. This function mainly uses combinationUtil()
    void printCombination(int arr[], int n, int r)
    {
        // A temporary array to store all combination one by one
        int data[r];

        // Print all combination using temprary array 'data[]'
        combinationUtil(arr, n, r, 0, data, 0);
    }

    /* arr[]  ---> Input Array
       n      ---> Size of input array
       r      ---> Size of a combination to be printed
       index  ---> Current index in data[]
       data[] ---> Temporary array to store current combination
       i      ---> index of current element in arr[]     */
    void combinationUtil(int arr[], int n, int r, int index, int data[], int i)
    {
        // Current cobination is ready, print it
        if (index == r)
        {
            for (int j=0; j<r; j++)
                printf("%d ",data[j]);
            printf("\n");
            return;
        }

        // When no more elements are there to put in data[]
        if (i >= n)
            return;

        // current is included, put next at next location
        data[index] = arr[i];
        combinationUtil(arr, n, r, index+1, data, i+1);

        // current is excluded, replace it with next (Note that
        // i+1 is passed, but index is not changed)
        combinationUtil(arr, n, r, index, data, i+1);
    }

    // Driver program to test above functions
    int main()
    {
        int arr[] = {1, 2, 3, 4, 5};
        int r = 3;
        int n = sizeof(arr)/sizeof(arr[0]);
        printCombination(arr, n, r);
        return 0;
    }

Output:

    1 2 3
    1 2 4
    1 2 5
    1 3 4
    1 3 5
    1 4 5
    2 3 4
    2 3 5
    2 4 5
    3 4 5

*How to handle duplicates in method 2?*  
 Like method 1, we can following two things to handle duplicates.  
 1) Add code to sort the array before calling combinationUtil() in
printCombination()  
 2) Add following lines between two recursive calls of combinationUtil()
in combinationUtil()

            // Since the elements are sorted, all occurrences of an element
            // must be together
            while (arr[i] == arr[i+1])
                 i++; 

See **[this](http://ideone.com/91MYjB)**for an implementation that
handles duplicates.

This article is contributed by **Bateesh**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above

Â  Â 
Tags:
[MathematicalAlgo](http://www.geeksforgeeks.org/tag/mathematicalalgo/),
[Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-a-given-array-of-size-n/>

Print all increasing sequences of length k from first n natural numbers
-----------------------------------------------------------------------

Given two positive integers n and k, print all increasing sequences of
length k such that the elements in every sequence are from first n
natural numbers.<span id="more-131805"></span>

Examples:

    Input: k = 2, n = 3
    Output: 1 2
            1 3
            2 3 

    Input: k = 5, n = 5
    Output: 1 2 3 4 5

    Input: k = 3, n = 5
    Output: 1 2 3
            1 2 4
            1 2 5
            1 3 4
            1 3 5
            1 4 5
            2 3 4
            2 3 5
            2 4 5
            3 4 5

**We strongly recommend to minimize the browser and try this yourself
first.**

Itâ€™s a good recursion question. The idea is to create an array of
length k. The array stores current sequence. For every position in
array, we check the previous element and one by one put all elements
greater than the previous element. If there is no previous element
(first position), we put all numbers from 1 to n.

Following is C++ implementation of above idea.

    // C++ program to  print all increasing sequences of
    // length 'k' such that the elements in every sequence
    // are from first 'n' natural numbers.
    #include<iostream>
    using namespace std;

    // A utility function to print contents of arr[0..k-1]
    void printArr(int arr[], int k)
    {
        for (int i=0; i<k; i++)
            cout << arr[i] << " ";
        cout << endl;
    }

    // A recursive function to print all increasing sequences
    // of first n natural numbers.  Every sequence should be
    // length k. The array arr[] is used to store current
    // sequence.
    void printSeqUtil(int n, int k, int &len, int arr[])
    {
        // If length of current increasing sequence becomes k,
        // print it
        if (len == k)
        {
            printArr(arr, k);
            return;
        }

        // Decide the starting number to put at current position:
        // If length is 0, then there are no previous elements
        // in arr[].  So start putting new numbers with 1.
        // If length is not 0, then start from value of
        // previous element plus 1.
        int i = (len == 0)? 1 : arr[len-1] + 1;

        // Increase length
        len++;

        // Put all numbers (which are greater than the previous
        // element) at new position.
        while (i<=n)
        {
            arr[len-1] = i;
            printSeqUtil(n, k, len, arr);
            i++;
        }

        // This is important. The variable 'len' is shared among
        // all function calls in recursion tree. Its value must be
        // brought back before next iteration of while loop
        len--;
    }

    // This function prints all increasing sequences of
    // first n natural numbers. The length of every sequence
    // must be k.  This function mainly uses printSeqUtil()
    void printSeq(int n, int k)
    {
        int arr[k];  // An array to store individual sequences
        int len = 0; // Initial length of current sequence
        printSeqUtil(n, k, len, arr);
    }

    // Driver program to test above functions
    int main()
    {
        int k = 3, n = 7;
        printSeq(n, k);
        return 0;
    }

Output:

    1 2 3
    1 2 4
    1 2 5
    1 2 6
    1 2 7
    1 3 4
    1 3 5
    1 3 6
    1 3 7
    1 4 5
    1 4 6
    1 4 7
    1 5 6
    1 5 7
    1 6 7
    2 3 4
    2 3 5
    2 3 6
    2 3 7
    2 4 5
    2 4 6
    2 4 7
    2 5 6
    2 5 7
    2 6 7
    3 4 5
    3 4 6
    3 4 7
    3 5 6
    3 5 7
    3 6 7
    4 5 6
    4 5 7
    4 6 7
    5 6 7

This article is contributed by **Arjun**. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/print-increasing-sequences-length-k-first-n-natural-numbers/>

**[Recursion](http://en.wikipedia.org/wiki/Recursion_(computer_science)):**

In programming terms a recursive function can be defined as a routine
that calls itself directly or indirectly.<span id="more-9154"></span>

Using recursive algorithm, certain problems can be solved quite easily.
[Towers of Hanoi (TOH)](http://en.wikipedia.org/wiki/Tower_of_Hanoi)is
one such programming exercise. Try to write an *iterative* algorithm for
TOH. Moreover, every recursive program can be written using iterative
methods (Refer Data Structures by Lipschutz).

Mathematically recursion helps to solve few puzzles easily.

For example, a routine interview question,

In a party of N people, each person will shake her/his hand with each
other person only once. On total how many hand-shakes would happen?

***Solution:***

It can be solved in different ways, graphs, recursion, etc. Let us see,
how recursively it can be solved.

There are N persons. Each personÃ‚Â shake-handÃ‚Â with each other only
once. Considering N-th person, (s)he has toÃ‚Â shake-handÃ‚Â with (N-1)
persons. Now the problem reduced to small instance of (N-1) persons.
Assuming T<sub>N</sub> as totalÃ‚Â shake-hands, it can
beÃ‚Â formulatedÃ‚Â recursively.

T<sub>N</sub> = (N-1) + T<sub>N-1</sub> [T<sub>1</sub> = 0, i.e. the
last person have already shook-hand with every one]

Solving it recursivelyÃ‚Â yieldsÃ‚Â an arithmetic series, which can be
evaluated to N(N-1)/2.

*Exercise: In a party of N couples, only one gender (either male or
female) can shake hand with every one. How many shake-hands would
happen?*

**Usually recursive programs results in poor time complexities. An
example is Fibonacci series.Ã‚Â The time complexity of calculating
n-thÃ‚Â FibonacciÃ‚Â number using recursion is approximately
1.6<sup>n</sup>. It means the same computer takes almost 60% more time
for nextÃ‚Â FibonacciÃ‚Â number. RecursiveÃ‚Â FibonacciÃ‚Â algorithm has
overlapped subproblems. There are other techniques like *dynamic
programming* to improve such overlapped algorithms.

However, few algorithms, (e.g. merge sort, quick sort, etcâ€¦) results
in optimal time complexity using recursion.

**Base Case:**

One critical requirement of recursive functions is termination point or
base case. Every recursive program must have base case to make sure that
the function will terminate. MissingÃ‚Â base case results in unexpected
behaviour.

**Different Ways of Writing Recursive Functions in C/C++:**

**<span> *Function calling itself: (Direct way)*  
 </span>**

Most of us aware atleast two different ways ofÃ‚Â writingÃ‚Â recursive
programs. Given below is towers ofÃ‚Â HanoiÃ‚Â code. It is an example of
direct calling.

    // Assuming n-th disk is bottom disk (count down)
    void tower(int n, char sourcePole, char destinationPole, char auxiliaryPole)
    {
       // Base case (termination condition)
       if(0 == n)
         return;

       // Move first n-1 disks from source pole
       // to auxiliary pole using destination as
       // temporary pole
       tower(n-1, sourcePole, auxiliaryPole,
          destinationPole);
       
    // Move the remaining disk from source
       // pole to destination pole
       printf("Move the disk %d from %c to %c\n", n,
         sourcePole, destinationPole);

       // Move the n-1 disks from auxiliary (now source)
       // pole to destination pole using source pole as
       // temporary (auxiliary) pole
       tower(n-1, auxiliaryPole, destinationPole,
         sourcePole);
    }

    void main()
    {
       tower(3, 'S', 'D', 'A');
    }

The time complexity of TOH can be calculated by formulating number of
moves.

We need to move the first N-1 disks from Source to Auxiliary and from
Auxiliary to Destination, i.e. the first N-1 disks requires two
moves.Ã‚Â One more move of last disk from Source to
Destination.Ã‚Â Mathematically it can be defined recursively.

M<sub>N</sub> = 2M<sub>N-1</sub> + 1.

We can easily solve the above recursive relation (2<sup>N</sup>-1),
which is exponential.  
 <span>  
 ***Recursion using mutual function call: (Indirect way)***  
 </span>  
 Indirect calling. Though least pratical, a function [funA()] can call
another function [funB()] which inturn calls
[funA()]Ã‚Â formerÃ‚Â function. In this case both the functions should
have the base case.

***Defensive Programming:***

We can combine defensive coding techniques with recursion for graceful
functionality of application. Usually recursive programming is not
allowed in safety critical applications, such as flight controls, health
monitoring, etc. However, one can use a static count technique to avoid
uncontrolled calls (NOT in safety critical systems, may be used in soft
real time systems).

    void recursive(int data)
    {
       static callDepth;
       if(callDepth > MAX_DEPTH)
          return;

       // Increase call depth
       callDepth++;

       // do other processing
       recursive(data);

       // do other processing
       // Decrease call depth
       callDepth--;
    }

callDepth depth depends on function stack frame size and maximum stack
size.

<span> ***Recursion using function pointers: (Indirect way)***  
 </span>  
 Recursion can also implemented with function pointers. An example is
signal handler in POSIX complaint systems. If the handler causes to
trigger same event due to which the handler being called, the function
will reenter.

*We will cover function pointer approach and iterative solution to TOH
puzzle in later article.*

Thanks to Venki for writing the above post. Please write comments if you
find anything incorrect, or you want to share more information about the
topic discussed above.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/recursive-functions/>

Reverse a stack using recursion
-------------------------------

You are not allowed to use loop constructs like while, for..etc, and you
can only use the following ADT functions on Stack S:  
 isEmpty(S)  
 push(S)  
 pop(S)<span id="more-6921"></span>

**Solution:**  
 The idea of the solution is to hold all values in Function Call Stack
until the stack becomes empty. When the stack becomes empty, insert all
held items one by one at the bottom of the stack.

For example, let the input stack be

        1  

    First 4 is inserted at the bottom.
        4 
    So we need a function that inserts at the bottom of a stack using the above given basic stack function. //Below is a recursive function that inserts an element at the bottom of a stack.

    void insertAtBottom(struct sNode** top_ref, int item)
    {
       int temp;  
       if(isEmpty(*top_ref))
       {  
           push(top_ref, item); 
       }
       else
       {
        
         /* Hold all items in Function Call Stack until we reach end of 
           the stack. When the stack becomes empty, the isEmpty(*top_ref) 
           becomes true, the above if part is executed and the item is 
           inserted at the bottom */
         temp = pop(top_ref);
         insertAtBottom(top_ref, item);

         /* Once the item is inserted at the bottom, push all the
              items held in Function Call Stack */
         push(top_ref, temp);
       }             
    }     

**//Below is the function that reverses the given stack using
insertAtBottom()**

    void reverse(struct sNode** top_ref)
    {
      int temp;   
      if(!isEmpty(*top_ref))
      {
        
        /* Hold all items in Function Call Stack until we reach end of 
         the stack */
        temp = pop(top_ref);                        
        reverse(top_ref);

        /* Insert all the items (held in Function Call Stack) one by one 
           from the bottom to top. Every item is inserted at the bottom */
        insertAtBottom(top_ref, temp);
      }      
    }     

**//Below is a complete running program for testing above functions.**

    #include<stdio.h>
    #include<stdlib.h>
    #define bool int

    /* structure of a stack node */
    struct sNode
    {
       char data;
       struct sNode *next;
    };

    /* Function Prototypes */
    void push(struct sNode** top_ref, int new_data);
    int pop(struct sNode** top_ref);
    bool isEmpty(struct sNode* top);
    void print(struct sNode* top);

    /* Driveer program to test above functions */
    int main()
    {
      struct sNode *s = NULL;
      push(&s, 4);
      push(&s, 3);
      push(&s, 2);
      push(&s, 1);  

      printf("\n Original Stack ");
      print(s);
      reverse(&s);
      printf("\n Reversed Stack ");  
      print(s);
      getchar();
    }    

    /* Function to check if the stack is empty */
    bool isEmpty(struct sNode* top)
    {
      return (top == NULL)? 1 : 0;
    }

    /* Function to push an item to stack*/
    void push(struct sNode** top_ref, int new_data)
    {
      /* allocate node */
      struct sNode* new_node =
                (struct sNode*) malloc(sizeof(struct sNode));

      if(new_node == NULL)
      {
         printf("Stack overflow \n");
         getchar();
         exit(0);
      }          

      /* put in the data  */
      new_node->data  = new_data;

      /* link the old list off the new node */
      new_node->next = (*top_ref); 

      /* move the head to point to the new node */
      (*top_ref)    = new_node;
    }

    /* Function to pop an item from stack*/
    int pop(struct sNode** top_ref)
    {
      char res;
      struct sNode *top;

      /*If stack is empty then error */
      if(*top_ref == NULL)
      {
         printf("Stack overflow \n");
         getchar();
         exit(0);
      }
      else
      {
         top = *top_ref;
         res = top->data;
         *top_ref = top->next;
         free(top);
         return res;
      }
    }

    /* Functrion to pront a linked list */
    void print(struct sNode* top)
    {
      printf("\n");
      while(top != NULL)
      {
        printf(" %d ", top->data);
        top =  top->next;
      }
    }     

Please write comments if you find any bug in above code/algorithm, or
find other ways to solve the same problem.

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/reverse-a-stack-using-recursion/>

Tail Recursion
--------------

**What is tail recursion?**  
 A recursive function is tail recursive when recursive call is the last
thing executed by the function. <span id="more-127367"></span> For
example the following C++ function print() is tail recursive.

    // An example of tail recursive function
    void print(int n)
    {
        if (n < 0)  return;
        cout << " " << n;

        // The last executed statement is recursive call
        print(n-1);
    }

**Why do we care?**  
 The tail recursive functions considered better than non tail recursive
functions as tail-recursion can be optimized by compiler. The idea used
by compilers to optimize tail-recursive functions is simple, since the
recursive call is the last statement, there is nothing left to do in the
current function, so saving the current functionâ€™s stack frame is of
no use.

**Can a non-tail recursive function be written as tail-recursive to
optimize it?**  
 Consider the following function to calculate factorial of n. It is a
non-tail-recursive function. Although it looks like a tail recursive at
first look. If we take a closer look, we can see that the value returned
by fact(n-1) is used in fact(n), so the call to fact(n-1) is not the
last thing done by fact(n)

    #include<iostream>
    using namespace std;

    // A NON-tail-recursive function.  The function is not tail
    // recursive because the value returned by fact(n-1) is used in
    // fact(n) and call to fact(n-1) is not the last thing done by fact(n)
    unsigned int fact(unsigned int n)
    {
        if (n == 0) return 1;

        return n*fact(n-1);
    }

    // Driver program to test above function
    int main()
    {
        cout << fact(5);
        return 0;
    }

The above function can be written as a tail recursive function. The idea
is to use one more argument and accumulate the factorial value in second
argument. When n reaches 0, return the accumulated value.

    #include<iostream>
    using namespace std;

    // A tail recursive function to calculate factorial
    unsigned factTR(unsigned int n, unsigned int a)
    {
        if (n == 0)  return a;

        return factTR(n-1, n*a);
    }

    // A wrapper over factTR
    unsigned int fact(unsigned int n)
    {
       return factTR(n, 1);
    }

    // Driver program to test above function
    int main()
    {
        cout << fact(5);
        return 0;
    }

We will soon be discussing more on tail recursion.

**References:**  
 <http://en.wikipedia.org/wiki/Tail_call>  
 <http://c2.com/cgi/wiki?TailRecursion>

Please write comments if you find anything incorrect, or you want to
share more information about the topic discussed above

Â  Â 
Tags: [Recursion](http://www.geeksforgeeks.org/tag/recursion/)

### Source:

<http://www.geeksforgeeks.org/tail-recursion/>
