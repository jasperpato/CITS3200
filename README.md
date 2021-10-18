# Search algorithm for FAQs

## Introduction

This program returns posts from an input file that are similar in meaning to an input post.

## Procedure to run program

1. Clone this repository using
> git clone https://github.com/jasperpato/CITS3200.git

2. (optional) Create a python virtual environment and install required packages
> python3 -m venv venv

3. (optional) Enter the virtual environment
> source venv/bin/activate

4. Navigate to CITS3200 directory
> cd CITS3200

5. Download requirements
> python3 -m pip install -r requirements.txt

6. (optional) Run bash script to install the pretrained model for USE (1.5GB)
> ./install_USE.sh

7. (optional) Run --help command for program usage
> python3 similarity.py --help

8. Run program on command line
> python3 similarity.py [input file name] [number of posts] -[options]

9. OR import and use the <i>similar()</i> function from this package
> similar_posts = similar(filename, subject, payload, n)

## Overview of Program

### Algorithms
The different algorithms for similarity scoring are Cosine, Jaccard,
Term Frequency–Inverse Document Frequency (TFIDF), and Universal Sentence
Encoder (USE). These can be chosen individually, or used together and averaged.
Based on manual tagging tests, our recommendation is to use the default option
of TFIDF for calculating similarity scores between posts.

For the functioning of USE, a pretrained model is required, which 
may be installed via the supplied bash script.

### Usage

The intended usage is to call similar() from similarity.py from an outer
program. The signature is:
> **similar(filename, subject, payload, algos=[Tfidf], N=3, use_spellcheck=False, W=0.1)**
>
>> #### Parameter info:
>>
>> - **Filename** is the name of the txt file that contains a series of posts in rfc2822 
>>   format.
>> 
>> - **Subject** and **payload** are strings containing the subject and payload text of an
>>  input post for which similar posts are to be found.
>>
>> - **N** is the number of similar posts to be returned.
>>
>> - **Algos** is a list of similarity algorithm names as strings. It can contain any
>>   combination of ['Cosine', 'Jaccard', 'Tfidf', 'Use'].
>>
>> - **Use_spellcheck** specifies whether to implement spell correction during
>>   pre-processing. It can yield more accurate results, however takes more time.
>>
>> - **W** is the weighting of the subject similarity. The weighting of the payload
>>   similarity will be (1-**W**). It is recommended not to alter W from the default value of 0.1.

Import this function into your python program by including this statement:

> from CITS3200 import similar

View example.py for an example.

## Clustering

Seperate from the main program there are functions provided to generate clusters relating to the similarity of a group of posts.

These functions are useful for creating a list of Frequently Asked Questions.

In their current state these functions are not fully polished and can be considered mildly inconvenient to use for a non-technical user.

### Clustering Functions

simple_clustering()

simple_verified_clustering()

affinity_clustering()

All clustering functions take the same parameters and return the same outputs

eg.
> example_clustering(threads, alg, cleaners, filters, n)

>> #### Parameter info:
>> - **threads** the list of threads as returned from the function parse_file(filename)
>>
>> - **alg** the object created from the desired similarity algorithm class
>>
>> - **cleaners** the tuple of functions used to clean up the text eg. to_lower
>>
>> - **filters** the tuple of functions used to filter out unwanted characters eg. remove_non_alphabet
>>
>> - **n** the number of Frequently Asked Questions to be returned

View cluster_tester.py for an example.





