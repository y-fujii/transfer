// by Yasuhiro Fujii <http://mimosa-pudica.net>, public domain.
#include <limits>
#include <cmath>
#include <random>
#include <iostream>
#include <Eigen/Dense>

using namespace std;
using Eigen::Vector2d;
using Eigen::Vector3d;


inline Vector3d random_dir_hemi() {
	Vector3d v;
	double   n;
	do {
		v = Vector3d::Random();
		v(2) = 0.5 * (v(2) + 1.0);
		n = v.squaredNorm();
	} while( n <= numeric_limits<double>::min() || 1.0 <= n );
	return v.normalized();
}

inline Vector3d random_dir_cos_weighted() {
	Vector2d v;
	double   n;
	do {
		v = Vector2d::Random();
		n = v.squaredNorm();
	} while( n >= 1.0 );
	return Vector3d( v(0), v(1), sqrt( 1.0 - n ) );
}

template<class Rng>
Vector3d scatter( double g, Vector3d const& ez, Rng& rng ) {
	static uniform_real_distribution<double> u01; // XXX

	double s = 2.0 * u01( rng ) - 1.0;
	double cos_t;
	if( g * g <= numeric_limits<double>::epsilon() ) {
		cos_t = s - (3.0 / 2.0) * g * (s * s - 1.0);
	}
	else {
		// Ref. <https://www.astro.umd.edu/~jph/HG_note.pdf>.
		double v = (1.0 - g * g) / (1.0 + g * s);
		cos_t = (1.0 + g * g - v * v) / (2.0 * g);
	}

	double sin_t = sqrt( 1.0 - cos_t * cos_t );
	double phi = (2.0 * M_PI) * u01( rng );
	Vector3d ex = ez.unitOrthogonal();
	Vector3d ey = ez.cross( ex );
	return cos_t * ez + sin_t * (cos( phi ) * ex + sin( phi ) * ey);
}

template<class Rng>
double reflectance( double g, double ks, double ka, size_t n_samples, Rng& rng ) {
	exponential_distribution<double> s_dist( ks );
	exponential_distribution<double> a_dist( ka );

	//vector<size_t> dist( 16, 0.0 );

	size_t count = 0;
	for( size_t i = 0; i < n_samples; ++i ) {
		Vector3d x = Vector3d::Zero();
		Vector3d v = random_dir_cos_weighted();
		while( true ) {
			double s_len = s_dist( rng );
			double a_len = a_dist( rng );
			x += min( s_len, a_len ) * v;
			if( x(2) < 0.0 ) {
				// Escaped.
				assert( v(2) <= 0.0 );
				++count;
				//double angle = ((2.0 / M_PI) * dist.size()) * acos( -v(2) );
				//++dist[size_t( angle )];
				break;
			}
			if( a_len < s_len ) {
				// Absorbed.
				break;
			}
			else {
				// Scattered.
				v = scatter( g, v, rng );
			}
		}
	}
	//for( size_t i = 0; i < dist.size(); ++i ) {
	//	double t0 = (M_PI / (2.0 * dist.size())) * (i + 0.0);
	//	double t1 = (M_PI / (2.0 * dist.size())) * (i + 1.0);
	//	double dt = cos( t0 ) - cos( t1 );
	//	cout << 0.5 * (t0 + t1) << ' ' << (2.0 / (M_PI * n_samples * dt)) * dist[i] << '\n';
	//}
	return double( count ) / double( n_samples );
}

template<class Rng>
void plot_ks_r( double g, size_t n_samples, size_t n_division, Rng& rng ) {
	for( size_t j = 0; j < n_division; ++j ) {
		double ks = double( j ) / double( n_division );
		double r = reflectance( g, ks, 1.0 - ks, n_samples, rng );
		cout << ks << ' ' << r << endl;
	}
	cout << "1 1" << endl;
}

template<class Rng>
void plot_g_r( double ks, size_t n_samples, size_t n_division, Rng& rng ) {
	for( size_t j = 0; j < n_division; ++j ) {
		double g = (2.0 / n_division) * double( j ) - 1.0;
		double r = reflectance( g, ks, 1.0 - ks, n_samples, rng );
		cout << g << ' ' << r << endl;
	}
}

template<class Rng>
void plot_h( size_t n_samples, size_t div_g, size_t div_k, Rng& rng ) {
	cout << -1.0 << ' ' << 1.0 << endl;
	for( size_t i = 1; i < div_g; ++i ) {
		double g = (2.0 / div_g) * i - 1.0;
		for( size_t j = 1; j < div_k; ++j ) {
			double ks = double( j ) / double( div_k );
			double r = reflectance( g, ks, 1.0 - ks, n_samples, rng );
			double p = (1.0 + r) / (1.0 - r);
			double h = (p * p - 1.0) * (1.0 - ks) / (2.0 * ks);
			cout << g << ' ' << h << endl;
		}
	}
	cout << +1.0 << ' ' << 0.0 << endl;
}

template<class Rng>
void integrate_phase_function( size_t n_samples, size_t n_division, Rng& rng ) {
	for( size_t i = 0; i < n_division; ++i ) {
		double g = (2.0 / n_division) * i - 1.0;
		size_t count = 0;
		for( size_t j = 0; j < n_samples; ++j ) {
			Vector3d dir_i = random_dir_hemi();
			Vector3d dir_o = scatter( g, dir_i, rng );
			if( dir_o(2) < 0.0 ) {
				++count;
			}
		}
		cout << g << ' ' << double( count ) / double( n_samples ) << endl;
	}
	cout << "1 0" << endl;
}

int main() {
	size_t n_samples  = 1 << 20;
	size_t n_division = 1 <<  5;

	mt19937_64 rng;
	plot_ks_r( -0.5, n_samples, n_division, rng );
	//plot_g_r( 0.5, n_samples, n_division, rng );
	//integrate_phase_function( n_samples, n_division, rng );
	//plot_h( n_samples, n_division, 1 << 3, rng );

	return 0;
}
