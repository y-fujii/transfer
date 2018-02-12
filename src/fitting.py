#!/usr/bin/env python3
# by Yasuhiro Fujii <http://mimosa-pudica.net>, public domain.

import math
import numpy
import scipy.optimize
from matplotlib import pyplot


def error_lin( xs, ys ):
    return numpy.mean( (xs - ys) ** 2 )

def error_log( xs, ys ):
    xs_log = numpy.log( xs[1:-1] )
    ys_log = numpy.log( ys[1:-1] )
    return numpy.mean( (xs_log - ys_log) ** 2 )

def error_lin_max( xs, ys ):
    return numpy.max( (xs - ys) ** 2 )

def error_log_max( xs, ys ):
    xs_log = numpy.log( xs[1:-1] )
    ys_log = numpy.log( ys[1:-1] )
    return numpy.max( (xs_log - ys_log) ** 2 )

def formula0( ks, ka, alpha, beta ):
    rc = ((ks + ka) ** alpha - ka ** alpha) / ((ks + ka) ** alpha + ka ** alpha)
    return rc ** beta

def formula1( ks, ka, delta ):
    ra = ka / (ks + ka)
    rc = (1.0 - numpy.sqrt( ra )) / (1.0 + numpy.sqrt( ra ))
    return (1.0 - delta) * rc + delta * rc ** 2

def formula1_inv( r, delta ):
    ka = ((1.0 - r) / (1.0 + r)) ** 2
    return (1.0 - delta) * ka + delta * ka ** 2

def print_errors( xs, ys ):
        print( "abs avg: %f" % math.sqrt( error_lin    ( xs, ys ) ) )
        print( "abs max: %f" % math.sqrt( error_lin_max( xs, ys ) ) )
        print( "rel avg: %f" % math.exp( math.sqrt( error_log    ( xs, ys ) ) ) )
        print( "rel max: %f" % math.exp( math.sqrt( error_log_max( xs, ys ) ) ) )

def optimize( formula, x0 ):
    data = numpy.loadtxt( "data.txt" )
    ks = data[:, 0]
    rs = data[:, 1]
    ka = 1.0 - ks

    for error_func in [ error_lin, error_log, error_lin_max, error_log_max ]:
        result = scipy.optimize.basinhopping( 
            lambda x: error_func( rs, formula( ks, ka, *x ) ), x0
        )
        print( error_func.__name__, result.x )
        print_errors( rs, formula( ks, ka, *result.x ) )

def plot():
    data = numpy.loadtxt( "data.txt" )
    ks = data[:, 0]
    rs = data[:, 1]
    ka = 1.0 - ks

    ra = formula1( ks, ka, 0.170 )
    print_errors( rs, ra )

    pyplot.rc( "text", usetex = True )
    pyplot.xlabel( "$ k_\mathrm{s}, 1 - k_\mathrm{a} $" )
    pyplot.ylabel( "$ R $" )
    pyplot.xlim( 0.0, 1.0 )
    pyplot.ylim( 0.0, 1.0 )
    pyplot.plot( ks, ra )
    pyplot.plot( ks[::50], rs[::50], "+" )
    pyplot.savefig( "build/plot.pdf" )
    pyplot.show()
    #pyplot.yscale( "log" )
    #pyplot.plot( ks, ra )
    #pyplot.plot( ks[::50], rs[::50], "+" )
    #pyplot.show()


def main():
    #optimize( formula1, [ 0.0 ] )
    plot()


main()
