#!/usr/bin/env python3
# by Yasuhiro Fujii <http://mimosa-pudica.net>, public domain.

import math
import numpy
import scipy.optimize


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
    ra = (ka / (ks + ka)) ** alpha
    rc = (1.0 - ra) / (1.0 + ra)
    return rc ** beta

def formula1( ks, ka, delta ):
    ra = numpy.sqrt( ka / (ks + ka) )
    rc = (1.0 - ra) / (1.0 + ra)
    return (1.0 - delta) * rc + delta * rc ** 2

def formula2( ks, ka, gamma ):
    ra = numpy.sqrt( ka / (ks + ka) )
    rc = (1.0 - ra) / (1.0 + gamma * ra)
    return rc

def formula3( ks, ka, a, b ):
    ra = ka / (ks + ka)
    rb = numpy.sqrt( ra )
    rc = (1.0 - rb) / (1.0 + a * ra + b * rb)
    return rc

def formula4( ks, ka, gamma ):
    ra = numpy.sqrt( ka / (gamma * ks + ka) )
    rc = (1.0 - ra) / (1.0 + ra)
    return rc

def formula1_inv( r, delta ):
    ka = ((1.0 - r) / (1.0 + r)) ** 2
    return (1.0 - delta) * ka + delta * ka ** 2

def print_errors( xs, ys ):
        print( "abs avg: %f" % math.sqrt( error_lin    ( xs, ys ) ) )
        print( "abs max: %f" % math.sqrt( error_lin_max( xs, ys ) ) )
        print( "rel avg: %f" % math.exp( math.sqrt( error_log    ( xs, ys ) ) ) )
        print( "rel max: %f" % math.exp( math.sqrt( error_log_max( xs, ys ) ) ) )

def optimize( formula, x0 ):
    data = numpy.loadtxt( "build/data.txt" )
    ks = data[:, 0]
    rs = data[:, 1]
    ka = 1.0 - ks

    for error_func in [ error_lin, error_log, error_lin_max, error_log_max ]:
        result = scipy.optimize.basinhopping( 
            lambda x: error_func( rs, formula( ks, ka, *x ) ), x0
        )
        print( error_func.__name__, result.x )
        print_errors( rs, formula( ks, ka, *result.x ) )

def plot( formula, x ):
    from matplotlib import pyplot

    data = numpy.loadtxt( "build/data_m075.txt" )
    ks = data[:, 0]
    rs = data[:, 1]
    ka = 1.0 - ks

    g = -0.75
    #a = 0.5 - math.asin( 0.96 * g ) * (0.5 / math.asin( 0.96 ))
    a = 0.8 - g + 0.2 * g * g
    ra = formula( a * ks, ka, 1.0 )
    print_errors( rs, ra )

    xs = 0.0

    #pyplot.rc( "text", usetex = True )
    pyplot.xlabel( "$ k_\mathrm{s}, 1 - k_\mathrm{a} $" )
    pyplot.ylabel( "Reflectance" )
    pyplot.xlim( 0.0, 1.0 )
    pyplot.ylim( 0.0, 1.0 )
    pyplot.plot( ks, ra, label = "$ \~R $" )
    pyplot.plot( ks, rs, label = "Monte Carlo" )
    pyplot.legend()
    #pyplot.savefig( "build/plot.pdf" )
    pyplot.show()
    #pyplot.yscale( "log" )
    #pyplot.plot( ks, ra )
    #pyplot.plot( ks[::50], rs[::50], "+" )
    #pyplot.show()


def main():
    #optimize( formula0, [ 0.5, 1.0 ] )
    #optimize( formula1, [ 0.0 ] )
    #optimize( formula2, [ 1.0 ] )
    #optimize( formula3, [ 0.0, 1.0 ] )
    #optimize( formula4, [ 1.0 ] )
    plot( formula4, [ 0.8 ] )
    #plot( formula2, [ 1.4 ] )


main()
