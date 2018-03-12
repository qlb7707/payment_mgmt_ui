import time

#given a timestamp,return year,month,day
def parse_timestamp(ts):
	tl = time.localtime(ts)
	year = tl.tm_year
	month = tl.tm_mon
	day = tl.tm_mday
	return year,month,day

def time_str_to_int(time_str):
	return time.mktime(time.strptime(time_str,'%Y-%m-%d'))
	 
