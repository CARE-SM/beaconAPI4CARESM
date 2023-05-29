from datetime import date, timedelta
import sys

class AgeCalculation():

    def calculateBirthdataRange(age, operator):
        currentdate = date.today()
        alphadate = currentdate - timedelta(days=200*365)
        enddate = currentdate - timedelta(days=age*365)
        startdate = enddate - timedelta(days=365)

        if operator == ">":
            return enddate, currentdate
        elif operator == ">=":
            return startdate, currentdate
        elif operator == "<":
            return alphadate, startdate
        elif operator == "<=":
            return alphadate, enddate
        elif operator == "=":
            return startdate, enddate
        else:
            sys.exit("There's a problem with your age/date or your operator used, please check the specifications to know why your data input is not valid")

    def calculateAgeRange(age, operator):

        if operator == ">":
            return age + 1, 110
        elif operator == ">=":
            return age, 110
        elif operator == "<":
            return 0, age - 1
        elif operator == "<=":
            return 0, age
        elif operator == "=":
            return age, age
        else:
            sys.exit("There's a problem with your age/date or your operator used, please check the specifications to know why your data input is not valid")