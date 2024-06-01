import datetime #import timedelta

# a function that takes a datetime object and adds 1hr to it
def add_one_hr(dt):
    return dt + datetime.timedelta(hours=1)


# a function that takes a date time in ISO8601 format to datetime object
def str_to_datetime(dt):
    return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
     





print(datetime.datetime.now())
test = add_one_hr(datetime.datetime.now())
print(test)

print(type(str_to_datetime("2024-06-02T12:00:00")))