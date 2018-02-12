#include <limits>
#include <cmath>
#include <random>
#include <iostream>
#include <Eigen/Dense>

using namespace std;
using Eigen::Vector2d;
using Eigen::Vector3d;


inline Vector3d random_dir_uniform() {
	Vector3d v;
	double   n;
	do {
		v = Vector3d::Random();
		n = v.squaredNorm();
	} while( n < numeric_limits<double>::min() || 1.0 < n );
	return v.normalized();
}

inline Vector3d random_dir_cos_weighted() {
	Vector2d v;
	double   n;
	do {
		v = Vector2d::Random();
		n = v.squaredNorm();
	} while( n > 1.0 );
	return Vector3d( v(0), v(1), sqrt( 1.0 - n ) );
}

int main() {
	size_t n_samples  = 1 << 24;
	size_t n_division = 1000;

	//vector<size_t> dist( 16, 0.0 );
	mt19937_64 rng;

	for( size_t j = 0; j < n_division; ++j ) {
		double ks = double( j ) / double( n_division );
		double ka = 1.0 - ks;
		exponential_distribution<double> s_dist( ks );
		exponential_distribution<double> a_dist( ka );

		size_t count = 0;
		for( size_t i = 0; i < n_samples; ++i ) {
			Vector3d x = Vector3d::Zero();
			Vector3d v = random_dir_cos_weighted();
			while( true ) {
				double s_len = s_dist( rng );
				double a_len = a_dist( rng );
				x += min( s_len, a_len ) * v;
				if( x(2) < 0.0 ) {
					// escaped.
					assert( v(2) <= 0.0 );
					++count;
					//double angle = ((2.0 / M_PI) * dist.size()) * acos( -v(2) );
					//++dist[size_t( angle )];
					break;
				}
				if( a_len < s_len ) {
					// absorbed.
					break;
				}
				else {
					// scattered.
					v = random_dir_uniform();
				}
			}
		}
		cout << ks << ' ' << double( count ) / double( n_samples ) << endl;

		//for( size_t i = 0; i < dist.size(); ++i ) {
		//	double t0 = (M_PI / (2.0 * dist.size())) * (i + 0.0);
		//	double t1 = (M_PI / (2.0 * dist.size())) * (i + 1.0);
		//	double dt = cos( t0 ) - cos( t1 );
		//	cout << 0.5 * (t0 + t1) << ' ' << (2.0 / (M_PI * n_samples * dt)) * dist[i] << '\n';
		//}
	}
	cout << "1 1" << endl;

	return 0;
}
