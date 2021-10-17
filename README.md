# Search algorithm for FAQs

## Introduction

This program returns posts from an input file that are similar in meaning to an input post.

## Procedure to run program

1. Clone this repository using
> git clone https://github.com/jasperpato/CITS3200.git

2. (optional) Create a python virtual environment
> python3 -m venv venv

3. (optional) Enter the virtual environment
> source venv/bin/activate

4. Navigate to CITS3200 directory
> cd CITS3200

5. Download requirements
> python3 -m pip install -r requirements.txt

6. Run demo program
> python3 similarity.py

## Overview of Program

### Algorithms
The different algorithms for similarity scoring are Cosine, Jaccard,
Term Frequency–Inverse Document Frequency (TFIDF), and Universal Sentence
Encoder (USE). These can be chosen individually, or used together and averaged.
Based on manual tagging tests, our recommendation is to use the default option
of TFIDF for calculating similarity scores between posts.

** Insert info about Use here. It requires downloading the pretrained model
from somewhere and placing in correct directory **

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

> from CITS3200.similarity import similar

Use in a program:

> filename = 'help2002-2019.txt'
> subject  = 'help me!'
> payload  = 'I need help. Has anyone asked this question before?'
> n        = 6
> similar_posts = similar(filename, subject, payload, n)

View example.py for an example.






