# Theorem Prover for a subset of First Order Logic 

#### Problem Statement 

- Given a Knowledge Base in Conjunctive Normal Form: 
  - For Example: 
      - Predicates: buy woman truck dog man person animal acquire human 
      - Variables: x3 x4 y0 x2 x5 x0 x1 
      - Constants: Kim SK1 Mike Kelly SK0 
      - Functions: 
      - Clauses:
      - !buy(x4,y0) acquire(x4,y0) 
      - dog(Kim) 
      - !man(x5) person(x5) 
      - !dog(x0) animal(x0) 
      - !human(x1) animal(x1) 
      - !man(x2) human(x2) 
      - !woman(x3) human(x3) 
      - man(Mike) 
      - person(Kelly) 
      - truck(SK0) 
      - buy(Mike,SK0) 
      - truck(SK1) 
      - buy(Kelly,SK1) 
  - The file first lists the predicates, variables, constants, and functions used in the knowledge base. 
  - It will then list the clauses on each line with whitespace separating each literal.


  - The program determines if the KB is satisfiable by applying PL Resolution and Unification logic 


#### Design Considerations

  - Custom data structures were designed to represent and store the following:
    - Clauses: which are composed of predicates
    - Predicates: which could be negated and have several types of arguments
    - Terms: which form the arguments for predicates and functions:
      - Constants
      - Variables
      - Functions
  - Decided how the unification function will look and developed wrapper functions to be able to print the data structures
  - Decided how to apply the substitutions to predicates and functions




   
