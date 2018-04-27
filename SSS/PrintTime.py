
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