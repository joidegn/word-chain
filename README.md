#word chains
###python shell script to calculate word chains using a dictionary.
expects pairs of words as input and finds out if these are connected by a word chain. e.g. "cat" and "dog" are connected via cat, cot, cog and dog

see here: http://socialcam.com/jobs/problems

##install
word chain is a shell script so place it in $PATH and then just run it from the command line.

usage:
wordchain.py -h

If you want to calculate several word chains you should consider hashing the dictionary file using --create-hash but note that this can take a while for medium to large dictionaries.

author Johannes Degn <j@degn.de> 
http://joi.degn.de 
https://twitter.com/JoiDegn
