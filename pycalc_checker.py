import sys
import subprocess
from math import *
from distutils.util import strtobool


PYCALC_UTIL_NAME = "pycalc"
RETURN_CODE = 0


UNARY_OPERATORS = {
    "-13": -13,
    "6-(-13)": 6-(-13),
    "1---1": 1---1,
    "-+---+-1": -+---+-1,
}

OPERATION_PRIORITY = {
    "1+2*2": 1+2*2,
    "1+(2+3*2)*3": 1+(2+3*2)*3,
    "10*(2+1)": 10*(2+1),
    "10^(2+1)": 10**(2+1),
    "100/3^2": 100/3**2,
    "100/3%2^2": 100/3%2**2,
}


FUNCTIONS_AND_CONSTANTS = {
    "pi+e": pi+e,
    "log(e)": log(e),
    "sin(pi/2)": sin(pi/2),
    "log10(100)": log10(100),
    "sin(pi/2)*111*6": sin(pi/2)*111*6,
    "2*sin(pi/2)": 2*sin(pi/2),
}

ASSOCIATIVE = {
    "102%12%7": 102%12%7,
    "100/4/3": 100/4/3,
    "2^3^4": 2**3**4,
}


COMPARISON_OPERATORS = {
    "1+2*3==1+2*3": eval("1+2*3==1+2*3"),
    "e^5>=e^5+1": eval("e**5>=e**5+1"),
    "1+2*4/3+1!=1+2*4/3+2": eval("1+2*4/3+1!=1+2*4/3+2"),
}


COMMON_TESTS = {
    "(100)": (100),
    "666": 666,
    "10(2+1)": 10*(2+1),
    "-.1": -.1,
    "1/3": 1/3,
    "1.0/3.0": 1.0/3.0,
    ".1 * 2.0^56.0": .1 * 2.0**56.0,
    "e^34": e**34,
    "(2.0^(pi/pi+e/e+2.0^0.0))": (2.0**(pi/pi+e/e+2.0**0.0)),
    "(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)": (2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0),
    "sin(pi/2^1) + log(1*4+2^2+1, 3^2)": sin(pi/2**1) + log(1*4+2**2+1, 3**2),
    "10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5": 10*e**0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5,
    "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)": sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0),
    "2.0^(2.0^2.0*2.0^2.0)": 2.0**(2.0**2.0*2.0**2.0),
    "sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))": sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e))),
}


ERROR_CASES = [
    "",
    "+",
    "1-",
    "1 2",
    "ee",
    "==7",
    "1 + 2(3 * 4))",
    "((1+2)",
    "1 + 1 2 3 4 5 6 ",
    "log100(100)",
    "------",
    "5 > = 6",
    "5 / / 6",
    "6 < = 6",
    "6 * * 6",
    "(((((",
    # "abs",
    # "pow(2, 3, 4)",
]


def trunc_string(string):
    return (string[:15] + '..') if len(string) > 15 else string


def call_command(command, args):
    result = subprocess.run([command, "--", args], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def check_results(keys: dict):
    global RETURN_CODE
    for command, expected_result in keys.items():
        result = call_command(PYCALC_UTIL_NAME, command)
        try:
            converted_result = float(result)
        except Exception:
            try:
                converted_result = bool(strtobool(result[:-1]))
            except Exception:
                print("{: <20} | Result: {}".format(
                    command,
                    "Fail: Invalid output: {} | Expected: {}".format(result, expected_result))
                )
                RETURN_CODE = 1
                continue

        if round(expected_result, 2) == round(converted_result, 2):
            print("{: <20} | Result: {}".format(trunc_string(command), "Pass"))
        else:
            print("{: <20} | Result: {}".format(
                command,
                "Fail: Invalid output: {} | Expected: {}".format(result, expected_result))
            )
            RETURN_CODE = 1


def check_error_results(keys: list):
    global RETURN_CODE
    for command in keys:
        result = call_command(PYCALC_UTIL_NAME, command)
        if result.startswith("ERROR:"):
            print("{: <20} | Result: {}".format(trunc_string(command), "Pass"))
        else:
            print("{: <20} | Result: {}".format(trunc_string(command), "Fail, expected correct error handling"))
            RETURN_CODE = 1


def main():
    print("Checking unary operators...")
    check_results(UNARY_OPERATORS)
    print()

    print("Checking operation priority...")
    check_results(OPERATION_PRIORITY)
    print()

    print("Checking functions and constants...")
    check_results(FUNCTIONS_AND_CONSTANTS)
    print()

    print("Checking associative...")
    check_results(ASSOCIATIVE)
    print()

    print("Checking comparison operators...")
    check_results(COMPARISON_OPERATORS)
    print()

    print("Checking common tests...")
    check_results(COMMON_TESTS)
    print()

    print("Checking error cases...")
    check_error_results(ERROR_CASES)

    sys.exit(RETURN_CODE)


if __name__ == '__main__':
    main()
