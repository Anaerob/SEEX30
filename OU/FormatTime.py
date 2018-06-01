
def getString(time):
    
    if 1000 * time < 1:
        s = str(int(1000 * 1000 * time)) + 'µs'
    elif time < 1:
        s = (str(int(1000 * time)) + 'ms, '
            + str(int(1000 * (1000 * time % 1))) + 'µs')
    elif time < 60:
        s = (str(int(time)) + 's, '
            + str(int(1000 * (time % 1))) + 'ms')
    elif time < 3600:
        s = (str(int(time / 60)) + 'm, '
            + str(int(time % 60)) + 's')
    elif time < 86400:
        s = (str(int(time / 3600)) + 'h, '
            + str(int((time % 3600) / 60)) + 'm, '
            + str(int(time % 60)) + 's')
    else:
        s = (str(int(time / 86400)) + 'd, '
            + str(int((time % 86400) / 3600)) + 'h, '
            + str(int((time % 3600) / 60)) + 'm')
    return s

def getMilliSeconds(time):
    
    if time < 1 / 1000:
        return 0
    else:
        return int(1000 * (time))

def getSeconds(time):
    
    if time < 1:
        return 0
    else:
        return int(time)

def getMinutes(time):
    
    if time < 60:
        return 0
    else:
        return int(time / 60)

def getHours(time):
    
    if time < 3600:
        return 0
    else:
        return int(time / 3600)

def getDays(time):
    
    if time < 86400:
        return 0
    else:
        return int(time / 86400)

#