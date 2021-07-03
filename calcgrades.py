import csv
import math
import numpy as np
import pandas
import scipy.optimize
import sys
import argparse


def ineq_constraint_1(v):
    return np.array([vi for vi in v])


def ineq_constraint_2(v):
    return np.array([-vi + 30 for vi in v])


class WeightAverage:

    def __init__(self, mean, csv):
        self.df = pandas.read_csv(csv)
        self.course = self.df['name']
        self.expected_mean = mean
        self.credits = self.df[['credits', 'grade']].query('grade == 0')[['credits']].transpose().to_numpy()[0]
        self.grade_initial_sol = np.array([mean for _ in range(0, len(self.credits))])
        self.owned_credits = self.df[['credits', 'grade']].query('grade > 0')[['credits']].transpose().to_numpy()[0]
        self.owned_grades = self.df[['grade']].query('grade > 0').transpose().to_numpy()[0]
        self.tot_credits = sum(self.owned_credits) + sum(self.credits)

    def weight_average(self, v):
        term1 = 0
        term2 = 0
        for i in range(0, len(self.owned_grades)):
            term1 = term1 + self.owned_grades[i] * self.owned_credits[i]
        for i in range(0, len(v)):
            term2 = term2 + v[i] * self.credits[i]
        return (term1 + term2) / self.tot_credits

    def eq_constraint(self, v):
        return self.weight_average(v) - self.expected_mean

    def solve(self):
        cons = (
            {'type': 'eq', 'fun': self.eq_constraint},
            {'type': 'ineq', 'fun': ineq_constraint_1},
            {'type': 'ineq', 'fun': ineq_constraint_2})
        res = scipy.optimize.minimize(self.weight_average, self.grade_initial_sol, method='SLSQP', constraints=cons)
        if not res.success:
            return None
        return res.x


def error_no_solution():
    print("Mean not possible with current vote :(")
    exit(0)


def output_result(solver, sol):
    avg = solver.weight_average(sol)
    df = solver.df
    print(f"Expected mean: {avg} -> {int(round(avg / 30 * 110, 0))} / 110")
    if sol is None:
        print("Not Possible with current grades :(")
        exit()
    for index, row in df.query('grade > 0').iterrows():
        print(f"'{row['name']}', credits: {row['credits']}, grade  {row['grade']}")
    i = 0
    for index, row in df.query('grade == 0').iterrows():
        print(f"'{row['name']}', credits: {row['credits']}, grade  {int(sol[i])}")
        i += 1
    return 0


def main():
    name = "calcGrades"
    description = """CalcGrades is an utility which purpose is to compute the minimum
                     grades required to get a certain weight average of the grades over the credits,
                     given the desired output and the grades already owned."""
    parser = argparse.ArgumentParser(name, description=description)
    parser.add_argument('mean', metavar='M', type=float, nargs='+', help='The expected mean')
    parser.add_argument('--file',dest='file', default='courses.csv', type=str,
                        help='path to the csv file containing the courses (default: courses.csv)')
    parser.add_argument('--floor', default=False, action='store_true',
                        help='apply floor operation instead of round to solution')
    parser.add_argument('--ceil', default=False, action='store_true',
                        help='apply ceil operation instead of round to solution')
    args = parser.parse_args()
    mean = args.mean
    courses = args.file
    solver = WeightAverage(mean, courses)
    sol = solver.solve()
    if sol is None:
        error_no_solution()
    if args.ceil:
        sol = [math.ceil(x) for x in sol]
    elif args.floor:
        sol = [math.floor(x) for x in sol]
    else:
        sol = [round(x) for x in sol]
    output_result(solver, sol)
    return 0


if __name__ == '__main__':
    main()
