from datetime import date, timedelta


# Finds the dates that users can set predictions on
# This is mainly to ensure that there are enough predictions per date
def predictionDates(current_date:date=date.today()):
    # Tomorrow
    tomorrow = current_date + timedelta(1)
    # End of Week
    start = current_date - timedelta(days=current_date.weekday())
    week_end = start + timedelta(days=6)  # 6 for saturday
    # Last day of month
    month_end = date(current_date.year + current_date.month // 12, current_date.month % 12 + 1, 1)
    # Last day of year
    year_end = date(current_date.year, 12, 31) + timedelta(1)
    dates =  [tomorrow, week_end, month_end, year_end]
    dates = list(set(dates))
    dates.sort()  # Sort the dates
    return dates


# This is to round a dictionary
def roundDict(old_dict:dict, digits:int=2):
    new_dict= {}
    for info in old_dict:  # Round everything to two digits:
        new_dict[info] = old_dict[info]
        if type(old_dict[info]) == float:
            new_dict[info] = '{:.2f}'.format(round(old_dict[info], digits))

