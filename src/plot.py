import sys
import numpy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot


gamma = 0.80

def reflectance_approx( ks, ka, g ):
    P = numpy.sqrt( ka / (gamma * (1.0 - g) * ks + ka) )
    return (1.0 - P) / (1.0 + P)

def plot_r_of_ks_naive():
    pyplot.xlim( 0.0, 1.0 )
    pyplot.ylim( 0.0, 1.0 )
    ks = numpy.linspace( 0.0, 1.0, 256 )
    P = numpy.sqrt( 1.0 - ks )
    R = (1.0 - P) / (1.0 + P)
    pyplot.plot( ks, R )

    data = numpy.loadtxt( "data/r_of_ks_g_00.txt" )
    pyplot.plot( data[:, 0], data[:, 1], "+" )

    pyplot.savefig( "data/r_of_ks_naive.pdf" )
    pyplot.close()

def plot_h_of_g_integrated():
    pyplot.xlim( -1.0, 1.0 )
    pyplot.ylim( 0.0, 1.0 )
    data = numpy.loadtxt( "data/h_of_g_integrated.txt" )
    pyplot.plot( data[:, 0], data[:, 1] )

    pyplot.savefig( "data/h_of_g_integrated.pdf" )
    pyplot.close()

def plot_h_of_g_inversed():
    pyplot.xlim( -1.0, 1.0 )
    pyplot.ylim( 0.0, 1.0 )
    g = numpy.linspace( -1.0, 1.0, 256 )
    h = (gamma / 2.0) * (1.0 - g)
    pyplot.plot( g, h )

    data = numpy.loadtxt( "data/h_of_g_inversed.txt" )
    pyplot.plot( data[:, 0], data[:, 1], "+" )

    pyplot.savefig( "data/h_of_g_inversed.pdf" )
    pyplot.close()

def plot_r_of_g( ks, label ):
    pyplot.xlim( -1.0, 1.0 )
    pyplot.ylim( 0.0, 0.5 )
    g = numpy.linspace( -1.0, 1.0, 256 )
    R = reflectance_approx( ks, 1.0 - ks, g )
    pyplot.plot( g, R )

    data = numpy.loadtxt( "data/r_of_g_" + label + ".txt" )
    pyplot.plot( data[:, 0], data[:, 1], "+" )

    pyplot.savefig( "data/r_of_g_" + label + ".pdf" )
    pyplot.close()

def plot_r_of_ks( g, label ):
    pyplot.xlim( 0.0, 1.0 )
    pyplot.ylim( 0.0, 1.0 )
    ks = numpy.linspace( 0.0, 1.0, 256 )
    R = reflectance_approx( ks, 1.0 - ks, g )
    pyplot.plot( ks, R )

    data = numpy.loadtxt( "data/r_of_ks_" + label + ".txt" )
    pyplot.plot( data[:, 0], data[:, 1], "+" )

    pyplot.savefig( "data/r_of_ks_" + label + ".pdf" )
    pyplot.close()

def main():
    plot_r_of_ks_naive()
    plot_h_of_g_integrated()
    plot_h_of_g_inversed()
    plot_r_of_ks( -0.5, "g_m5" )
    plot_r_of_ks(  0.0, "g_00" )
    plot_r_of_ks( +0.5, "g_p5" )
    plot_r_of_g( 0.25, "ks_25" )
    plot_r_of_g( 0.50, "ks_50" )
    plot_r_of_g( 0.75, "ks_75" )

main()
