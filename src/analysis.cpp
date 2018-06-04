/*
 * analysis.cpp
 *
 *  Created on: Apr 2, 2018
 *      Author: kaess
 *
 *      Commented for Matt, who doesn't use C++
 */

#include <iostream> //Import input-output library (for cout)
#include <iterator> //Import iterators
#include <CCfits> //Import ALL of CCfits. Necessary, if unfortunate.
#include <vector>
#include <valarray>

using namespace std;
//This allows me to use things like 'cout' instead of 'std::cout'
using namespace CCfits;
//Ditto for CCFits

valarray<double> generateWeights(long n, double dt = 1.0) {
	valarray<double> retVal(n);
	const double coefficient = 12 / (dt * n * (n * n - 1));
	const double otherval = (n + 1) / 2.0;
#pragma omp parallel for
	for (long i = 0; i < n; i++) {
		retVal[i] = coefficient * (i + 1 - otherval);
	}
	return retVal;
}

double upTheRampWeight(int i, int n, double dt = 1.0) {
	//I will eventually extract these two when I create a class
	//they will be precomputed
	double coefficient = 12 / (dt * n * (n * n - 1));
	double otherval = (n + 1) / 2.0;
	return coefficient * (i - otherval);
}

template<typename T>
valarray<T> fitRamp(valarray<T> values, const vector<long> & axes) {
	const long X_AXIS = axes[0];
	const long Y_AXIS = axes[1];
	const long Z_AXIS = axes[2];

	const long PLATE_SIZE = X_AXIS * Y_AXIS;

	valarray<double> weights = generateWeights(Z_AXIS);
	valarray<T> output(PLATE_SIZE);
#pragma omp parallel for collapse(2)
	for (long i = 0; i < X_AXIS; i++) {
		for (long j = 0; j < Y_AXIS; j++) {
			for (long k = 0; k < Z_AXIS; k++) {
				output[j * X_AXIS + 1] += weights[k]
						* values[k * PLATE_SIZE + j * X_AXIS + i];
			}
//			auto column = values[slice(j * X_AXIS + i, Z_AXIS, PLATE_SIZE)];
//			output[j * X_AXIS + i] = (weights * column).sum();
			//This is an alternate way of dealing with the inner for loop
		}
	}
	return output;
}

int main(int argc, char ** argv) {

	FITS fitsFile("TestFile.fits", RWmode::Write); //Create a blank FITS file

	fitsFile.flush(); //Attempt to write the FITS file to disk (empty).

	FITS fitsFile2("./fakespots/spot1.fits", RWmode::Read);

	PHDU & spotImage = fitsFile2.pHDU();

	cout << spotImage << endl;

	cout << spotImage.axes() << endl;

	long naxes = spotImage.axes();

	for (long i = 0; i < naxes; i++) {
		cout << spotImage.axis(i) << endl;
	}

	FITS fitsFile3("./fakespots/spot2.fits", RWmode::Read);

	PHDU & spotImage2 = fitsFile3.pHDU();

	cout << spotImage2 << endl;

	long naxes2 = spotImage2.axes();
	long size = 1;
	vector<long> axes(naxes2);

	for (long i = 0; i < naxes2; i++) {
		size *= axes[i] = spotImage2.axis(i);
	}

	valarray<double> image2Data(size);
	spotImage2.readAllKeys();
	spotImage2.read(image2Data);
	valarray<double> output = fitRamp(image2Data, axes);

	for (long i = 0; i < 1024 * 1024; i++) {
		cout << output[i] << "\t";
	}
	cout << endl;
	//main has type int, and should return an int. 0 indicates normal termination of main.
	//Compiler would auto-generate this return if I didn't write it.
	return 0;
}
