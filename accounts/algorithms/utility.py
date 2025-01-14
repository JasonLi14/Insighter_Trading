from datetime import date, timedelta
import csv

# Finds the dates that users can set predictions on
# This is mainly to ensure that there are enough predictions per date
def predictionDates(current_date:date=date.today()):
    # Tomorrow
    tomorrow = current_date + timedelta(1)
    # End of Week
    start = current_date - timedelta(days=current_date.weekday())
    week_end = start + timedelta(days=6)  # 6 for sunday
    # Last day of month
    month_end = date(current_date.year + current_date.month // 12, current_date.month % 12 + 1, 1)
    # Last day of year
    year_end = date(current_date.year, 12, 31) + timedelta(1)
    dates =  [tomorrow, week_end, month_end, year_end]
    dates = list(set(dates))
    dates.sort()  # Sort the dates

    # Ensure all the dates are not the same date as today
    for i in range(len(dates) - 1, -1, -1):
        if dates[i] == current_date:
            dates.pop(i)
            
    return dates


# This is to round a dictionary
def roundDict(old_dict:dict, digits:int=2):
    new_dict= {}
    for info in old_dict:  # Round everything to two digits:
        new_dict[info] = old_dict[info]
        if type(old_dict[info]) == float:
            new_dict[info] = '{:.2f}'.format(round(old_dict[info], digits))
    return new_dict


# For getting all the possible stocks
def stocksFromCsv(csv_file_path="accounts/static/stock_info.csv"):
    stocks_list = []
    with open(csv_file_path, 'r', newline='') as csv_file:
        stocks_csv = csv.reader(csv_file)
        for row in stocks_csv:
            stocks_list.append(row)
    return stocks_list


if __name__ == "__main__":
    stocksFromCsv()
