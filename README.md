# Majority_illusions

This repository contains all code that was used for my Master's thesis:
"Extending the Graph Theory of Majority Illusions" by Naomï Broersma
Supervisors: dr. Z.L. Christoff and prof. dr. D. Grossi 

## HOW TO RUN THE CODE
Run any of the files from the correct folder ../Majority_illusions_code with the command python3 FILE_NAME
where the FILE_NAME can be
- directed_no_majority_illusion.py
- dynamic_illusions.py
- examples_paper.py
- multiple_colours.py
- regular_graph_maj_maj_illusion.py

## A SHORT DESCRIPTION PER FILE
### figures
A folder with figures that were later used as examples in my thesis.

### directed_no_majority_illusion.py
A code that checks randomly generated digraphs with a certain number of nodes until a digraph is found without 
majority-weak-majority illusion. I determined that a 3-cycle is such a digraph, so currently the code outputs only this example,
unless it is specified that other graphs need to be checked by setting check_random = True.

### dynamic_illusions.py
Code that updates the colouring of a generated graph using a majority threshold update. 
This was used as a starting point to obtain ideas about when majority-majority illusions would remain and dissapear.

### examples_paper.py
This code generates examples and plots that are relevant for my thesis. The figures can be found in the figures folder.

### multiple_colours.py
This code deals with plurality and quota illusions. It was used as a starting point to find results.
I attempted to find a counter-example to prove:
There exists a digraph for which no 1/4-weak-plurality illusion is possible. 
The code only works for relatively small graphs and so far no counter-example has been found.

### regular_graph_maj_maj_illusion.py
This code generates a regular graph with a majority-majority illusion according to theorem 3 from
Venema-Los et al. (2023). This was used in the dynamic_illusions.py file to determine how the graph changes over time.