def wget( url, timeout ):
    return ['wget', '--no-verbose', '--no-clobber', '--timeout=' + str(timeout), url]