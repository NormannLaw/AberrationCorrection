# AberrationCorrection

## Overview
The goal is implement my novel aberration correction method, which is based on Cizmar-Mazilu's method (https://doi.org/10.1038/nphoton.2010.85). Currently, a python 
program (Exhaustive.py) has been written to project blazing patterns onto the spatial light modulator (SLM) to do phase modulations for 532 nm laser beam. The 
implementation of this program is based on Bresenham's line algorithm. Also, I have designed an algorithm to grade the laser focus spots. An integrated version of these
two programs is now under lab testing. If succeeds, it will be used to correct the aberrations resulted from the rubber lenses I made and help me reduce the cost of 
optical trapping.

## Blazing pattern generator: Exhaustive.py
The program tries all the possible phase modulation patterns of every mode. It allows the user to change the precisions in the process of aberration correction. That is, 
the number of modes, the increment in rotation, blazing width, and maximum width are adjustable. In the lab version, which is now under testing, it is integrated with
some camera image detection codes as well as my laser spot grading algorithm. Ideally, it will complete the aberration correction by optimizing the phase modulation
patterns for each mode.

## Grading algorithm implementation: SpotScore.py
The algorithm requires 4 parameters: a 2D array that represents the image to be "graded", a user selected center, a starting radius, and a maximum radius. The algorithm
starts with the starting radius, and calculate the total pixel values inside and outside this radius from the center. A score is then calculated using the formula
          score = (inside - outside) / radius
The score is then recorded with its radius. (Note: in the implementation, the radius is in pixels)

We repeat this process by growing the radius, with increment 1 pixel length, until it reaches the maximum radius. The highest score and its corresponding radius is then
selected as the output.

Given a n pixels by n pixels mode, the algorithm's runtime is O(n^3). In the lab implementation, the user may "crop" the image before grading to speed up.
