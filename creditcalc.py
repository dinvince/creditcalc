import argparse
import math


parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str,
                    help='What type of the calc? Can choose annuity or diff')
parser.add_argument('--principal', type=int,
                    help='What is the credit principal?')
parser.add_argument('--payment', type=int,
                    help='What is the monthly payment?')
parser.add_argument('--periods', type=int,
                    help='How many months you need to repay the credit.')
parser.add_argument('--interest', type=float,
                    help='What is the interest rate?')


def nums_of_months_for_print(months):
    # months is integer >= 1
    years = months // 12
    num_of_months = months % 12
    if years == 0:
        if num_of_months == 1:
            return "You need 1 month to repay this credit!"
        else:
            return f"You need {num_of_months} months to repay this credit!"
    elif years == 1:
        if num_of_months == 0:
            return "You need 1 year to repay this credit!"
        elif num_of_months == 1:
            return "You need 1 year and 1 month to repay this credit!"
        else:
            return f"You need 1 year and {num_of_months} months to repay this credit!"
    else:
        if num_of_months == 0:
            return f"You need {years} years to repay this credit!"
        elif num_of_months == 1:
            return f"You need {years} years and 1 month to repay this credit!"
        else:
            return f"You need {years} years and {num_of_months} months to repay this credit!"


def calculate_differentiated_payment(principal, num_of_months, rate):
    monthly_payments = []
    i = rate / 12 / 100
    for m in range(1, num_of_months + 1):
        monthly_payments.append(math.ceil(principal / num_of_months + i * (
                                principal - principal * (m - 1) / num_of_months))
                                )
    return monthly_payments


def calculate_count_of_months(principal, payment, rate):
    i = rate / 12 / 100
    num_of_months = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
    return num_of_months


def calculate_annuity_monthly_payment(principal, num_of_months, rate):
    i = rate / 12 / 100
    return math.ceil(principal * i * math.pow(1 + i, num_of_months) / (pow(1 + i, num_of_months) - 1))


def calculate_credit_principal(payment, num_of_months, rate):
    i = rate / 12 / 100
    return math.floor(payment / ((i * math.pow(1 + i, num_of_months)) / (pow(1 + i, num_of_months) - 1)))


def annuity_overpayment(principal, payment, num_of_months):
    return payment * num_of_months - principal


def diff_overpayment(principal, num_of_months, rate):
    return sum(calculate_differentiated_payment(principal, num_of_months, rate)) - principal


def has_negative_argument(arguments):
    if arguments.principal and arguments.principal <= 0:
        return True
    if arguments.periods and arguments.periods <= 0:
        return True
    if arguments.payment and arguments.payment <= 0:
        return True
    if arguments.interest and arguments.interest <= 0:
        return True


args = parser.parse_args()

if has_negative_argument(args):
    print("Incorrect parameters")
    exit()

if args.type == "annuity":
    if args.principal and args.periods and args.interest and not args.payment:
        annuity_payment = calculate_annuity_monthly_payment(args.principal, args.periods, args.interest)
        print(f"Your annuity payment = {annuity_payment}!")
        overpayment = annuity_overpayment(args.principal, annuity_payment, args.periods)
        print(f"Overpayment = {overpayment}")
    elif args.principal and args.payment and args.interest and not args.periods:
        count_of_months = calculate_count_of_months(args.principal, args.payment, args.interest)
        print(nums_of_months_for_print(count_of_months))
        overpayment = annuity_overpayment(args.principal, args.payment, count_of_months)
        print(f"Overpayment = {overpayment}")
    elif args.payment and args.periods and args.interest and not args.principal:
        credit_principal = calculate_credit_principal(args.payment, args.periods, args.interest)
        print(f"Your credit principal = {credit_principal}!")
        overpayment = annuity_overpayment(credit_principal, args.payment, args.periods)
        print(f"Overpayment = {overpayment}")
    else:
        print("Incorrect parameters")
elif args.type == "diff":
    if args.principal and args.periods and args.interest and not args.payment:
        diff_monthly_payments = calculate_differentiated_payment(args.principal, args.periods, args.interest)
        numbers = range(1, len(diff_monthly_payments) + 1)
        for each in zip(numbers, diff_monthly_payments):
            print(f"Month {each[0]}: paid out {each[1]}")
        overpayment = sum(diff_monthly_payments) - args.principal
        print(f"\nOverpayment = {overpayment}")
    else:
        print("Incorrect parameters")
elif not args.interest:
    print("Incorrect parameters")
else:
    print("Incorrect parameters")
