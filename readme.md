# calcgrades
`calcgrades` is an utility which purpose is to compute the minimum
grades required to get a certain weight average of the grades over the credits,
given the desired output and the grades already owned.
# Dependency
```
numpy
pandas
scipy
```
# Usage
```
usage: calcGrades [-h] [--file FILE] [--floor] [--ceil] M [M ...]

CalcGrades is an utility which purpose is to compute the minimum grades required to get a certain weight average of the grades over the credits, given the desired output and the grades already owned.

positional arguments:
  M            The expected mean

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  path to the csv file containing the courses (default: courses.csv)
  --floor      apply floor operation instead of round to solution
  --ceil       apply ceil operation instead of round to solution
```
it need in input the desired mean and a csv file of the format:
``` csv
name,credits,grade
course_1, course_credit_1, owned_grade_1
course_2, course_credit_2, ownewd_grade_2
course_3, course_credit_3, 0
course_4, course_credit_4, 0
```
The '0' means that the grade is not already owned and must be computed.
The option 'ceil' and 'floor' indicate that the solver will compute real solution
but a vote is an integer, so the vote shall be rounded by default,
if one want to ceil or floor all votes, has to specifiy it in the command.
