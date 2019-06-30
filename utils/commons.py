import random, datetime

def get_now():
    return '%s' % datetime.datetime.now().strftime('%y%m%d%H%M%S')

def get_now_and_four_randint():
    return '%s%04d' % (datetime.datetime.now().strftime('%y%m%d%H%M%S'), random.randint(0, 9999))

if __name__ == '__main__':
    print(get_now())
    print(get_now_and_four_randint())