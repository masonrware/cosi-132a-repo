# COSI 132 REPO
This is the codebase for the following class:
COSI 132A, Peter Anick, Brandeis Univeristy


**Title:** COSI 132A Spring 2022 Information Retrieval Final Project: RealView

**Author:** Drew Gottlieb, Jordan Blatter, Mason Ware, and Sarah Kosowsky

**Date:** May 10, 2022


**Description:** A sentence or two describing what the program does at a high level

**Dependencies:** List all software required to run the system. Include version and, where appropriate, a
url where the software was obtained. Please avoid code or dependencies that are operating system
dependent. Code should run identically under OSX and Windows. Python has OS independent ways of
handling pathnames.

**Build Instructions:** Describe clearly how to build the system as a sequence of explicit steps/commands.

**Run Instructions:** Describe how to run the system. What is the input and output produced? If there is a
user interface, describe how to use it. What is legal input? How does the system handle boundary
conditions or inappropriate input?

**Testing:** Briefly indicate how the system was tested to ensure it is working properly.

**Examples of queries/interactions that work over the test subset:** 

**Code submitted by:** which names the team member responsible for submitting the code and powerpoint slides into latte

**Team Member Contributions:** which includes a personalized paragraph
or two from each teammember which describe the parts of the code you were primarily
responsible for.
Drew -

Jordan - I was responsible for implementing the logistic regression model in Python to classify sentiment of movie reviews. The reviews were classified on a scale from 0-1. I retrieved the data from the NLTK movie corpus and split it into training, dev, and test sets. After training the model, it can be called on to classify a single review.
I also implemented the aspect extractor for reviews. This function extracts sentences containing mentions of aspects of movies like acting or visual effects and classifies the sentiment of the sentence containing the aspect word.


Mason - 

Sarah -

