from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import argparse
import collections


def main():

    parser = argparse.ArgumentParser(description='Calculates the mortage payments on loan with principle extra payments')
    parser.add_argument('--price', help='House price', type=float, nargs=1)
    parser.add_argument('--downPayment', help='Down payment amount', type=float, nargs=1)
    parser.add_argument('--interest', help='Annual interest rate [%]', type=float, nargs=1)
    parser.add_argument('--term', help='Loan term [yrs]', type=float, nargs=1)
    parser.add_argument('--extra', help='Monthly principle extra', type=float, nargs=1)
    args = parser.parse_args()

    # Default values
    if args.price is None:
        args.price = [250000.0]
    if args.downPayment is None:
        args.downPayment = [50000.0]
    if args.interest is None:
        args.interest = [3.625]
    if args.term is None:
        args.term = [10.0]

    # Calclate monthly payment and total contribution over term
    payment = calculateMonthlyPayment(price=args.price[0], downPayment=args.downPayment[0], annualInterest=args.interest[0], loanTerm=args.term[0])
    monthlyPayment = payment.monthly
    cumulativeSum = payment.cumulative

    print("")
    print("Home Price: ${:,.0f}    Down Payment: ${:,.0f}".format(args.price[0],args.downPayment[0]))
    print("Principle:              ${:,.0f}".format(args.price[0]-args.downPayment[0]))
    print("Monthly Payment:        ${:,.0f}".format(monthlyPayment))
    print("Cumulative Sum:         ${:,.0f}".format(cumulativeSum))
    print("")

    # Calculate payment history with extra principle contribution
    if args.extra is not None:
        finished = loanFinished(principle=(args.price[0]-args.downPayment[0]), monthlyPayment=monthlyPayment, extra=args.extra[0], annualInterest=args.interest[0])

        print("")
        print("With Monthly Payment of ${:,.0f},".format(monthlyPayment+args.extra[0]))
        print("Paid off Loan in {:.0f} months".format(finished))
        print("              vs {:.0f} months".format(args.term[0]*12))
        print("Saving: ${:,.0f}".format(cumulativeSum - int(monthlyPayment+args.extra[0])*finished))
        print("")


def calculateMonthlyPayment(price, downPayment, annualInterest, loanTerm):
    monthlyInterest = annualInterest / 1200
    principle = price - downPayment
    monthlyPayment = principle * monthlyInterest * np.power(1.0 + monthlyInterest, loanTerm*12) / (np.power(1.0+monthlyInterest, loanTerm*12) - 1.0)

    cumulativeSum = loanTerm * 12 * monthlyPayment
    Payment = collections.namedtuple('Payment', ['monthly', 'cumulative'])

    return Payment(monthly=monthlyPayment, cumulative=cumulativeSum)


def loanFinished(principle, monthlyPayment, extra, annualInterest):
    monthlyInterest = annualInterest / 1200
    b = (monthlyPayment + extra) / (monthlyPayment + extra - principle * monthlyInterest)
    finished = np.ceil( np.log(b) / np.log(1.0+monthlyInterest) )

    return finished


if __name__ == "__main__":
    main()
