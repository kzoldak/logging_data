import numpy as np

def _check_error_type(x, xerr):
    """
    Checks error type; confidence intervals or margins of error. 
    
    Returns
    --------
    'ci' if your errors are confidence intervals.
    'moe' if your errors are margins of error. 
    
    Function raises an excpetion if your errors are bad. 
    - 
    
    """
    x = np.asarray(x)
    xerr = np.asarray(xerr)
    if xerr.ndim != 2:
        raise Exception('xerr should have 2 dimensions, [ErrLo, errUp]')
    xerrLo = xerr[0]
    xerrUp = xerr[1]
    if (any(x > xerrLo) or any(xerrUp > x)) and (all(x > xerrLo) and all(xerrUp > x)):
        # You have confidence intervals
        print('You have Confidence Intervals')
        return('ci')
    elif all(abs(xerrLo) < abs(x)) and all(abs(xerrUp) < abs(x)):
        # all errors lower than the values indicates margins of error. 
        print('You have Margins of Error')
        return('moe')
    else:
        print('You have problems with your errors. ')
        raise Exception('You have problems with your errors.')
        

        
def to_log(x, xerr, which='both', errTypeReturn='moe'):
    """
    Take linear data and uncertainties and transform them to log
    values.
    
    Parameters
    ----------
    x : array of floats
        measurements of which to take logarithms
        
    xerr : array of floats
        uncertainties on x. Can pass errors with either 1 or 2 dimensions. 
        Note that 1d errors will be assumed to be Margins of Error and symmetric 
        when linear. Symmetry is not preserved when logging, so output will be 
        slightly asymmetric. 
        
    which : str, 'lower', 'upper', 'both', or 'average'
        Which uncertainty to return. Default is 'both'.
        
        Note that when converting to/from
        linear and logarithmic spaces, errorbar symmetry is not
        preserved. You can no log margins of error. You must first 
        find the confidence intervals, log the values and the confidence 
        intervals, then take the differences to get the logged margins 
        of error. 
        
    errTypeReturn : str, 'moe' or 'ci'
       'moe' returns logged margins of error.
       'ci' returns logged confidence intervals. 
       Note that which='average' can not be used with errTypeReturn='ci' 
       since you can not have averaged confidence intervals. 
        

    Returns
    -------
    logx : array of floats
    logxLo : array of floats
    logxUp : array of floats
    
    Notes:
    ------
    Note that 1d errors (xerr) will be assumed to be Margins of Error and symmetric 
        when linear. Symmetry is not preserved when logging, so output will be 
        slightly asymmetric. 
    
    This function uses another function to check whether your xerr are Confidence Intervals 
        or Margin of Error. 
    '_check_error_type(x, xerr=xerr)' returns a string of either 'ci' or 'moe'.
    
    """
    x = np.asarray(x)
    xerr = np.asarray(xerr)
    
    if xerr.ndim == 1:
        # If xerr is only 1 dimension, then you MUST have Margin of Error (MOE). 
        # Can't log MOE, convert to Confidence Intervals (CI) before logging.
        logxLo, logx, logxUp = np.log10([x-xerr, x, x+xerr])
        
    elif xerr.ndim == 2:
        # If xerr is 2 dimensions, you could have MOE or CI. 
        errtype = _check_error_type(x, xerr=xerr)  # check error type. 
        if errtype == 'moe':
            # If you have margins of error.
            moeLo,moeUp = xerr
            logxLo, logx, logxUp = np.log10([x-moeLo, x, x+moeUp])
        else:
            # If you have confidence intervals.
            ciLo,ciUp = xerr
            logxLo, logx, logxUp = np.log10([ciLo, x, ciUp])
    else:
        raise Exception('xerr must be 1 or 2 dimensions.')
    
    # logxLo and logxUp are currently in Conf Intv form. Convert to Marg of Err here, if desired.
    
    if errTypeReturn == 'moe':
        # logxLo and logxUp are currently in Conf Intv form. Convert to Marg of Err here, if desired.
        logxLo = logx-logxLo
        logxUp = logxUp-logx     
        if which == 'average':
            return logx, 0.5*(logxLo+logxUp)
        elif which == 'lower':
            return logx, logxLo
        elif which == 'upper':
            return logx, logxUp
        else:
            return logx, logxLo, logxUp
    if errTypeReturn == 'ci':
        if which == 'average':
            raise Exception("Can't return Confidence Intervals that are averaged.")
        elif which == 'lower':
            return logx, logxLo
        elif which == 'upper':
            return logx, logxUp
        else:
            return logx, logxLo, logxUp
