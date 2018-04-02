/*
 * analysis.cpp
 *
 *  Created on: Apr 2, 2018
 *      Author: kaess
 *
 *      Commented for Matt, who doesn't use C++
 */

#include <iostream> //Import input-output library (for cout)
#include <FITS.h> //Import CCFits, you need CCFits-devel installed

using namespace std;
//This allows me to use things like 'cout' instead of 'std::cout'
using namespace CCfits;
//Ditto for CCFits

int main(int argc, char ** argv) {

	cout << "Hello, world!" << endl; //Send "Hello, world!" to standard out, followed by newline and flush.

	FITS fitsFile("TestFile.fits", RWmode::Write); //Create a blank FITS file

	fitsFile.flush(); //Attempt to write the FITS file to disk (empty).

	//main has type int, and should return an int. 0 indicates normal termination of main.
	//Compiler would auto-generate this return if I didn't write it.
	return 0;
}
