
def getTime(time):
    
    if time < 60:
        s = str(int(time)) + 's'
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
            + str(int((time % 3600) / 60)) + 'm, '
            + str(int(time % 60)) + 's')
    return s

def printTime(time):
    
    if time < 60:
        print(
            'Runtime: %d seconds'
            % (time))
    elif time < 3600:
        print(
            'Runtime: %d minutes and %d seconds'
            % (time / 60,
                time % 60))
    elif time < 86400:
        print(
            'Runtime: %d hours, %d minutes and %d seconds'
            % (time / 3600,
                (time % 3600) / 60,
                time % 60))
    else:
        print(
            'Runtime: %d days, %d hours, %d minutes and %d seconds'
            % (time / 86400,
            (time % 86400) / 3600,
            (time % 3600) / 60,
            time % 60))

#