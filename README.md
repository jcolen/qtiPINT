qtiPINT
====

Description
===========

Qt Interface for PINT Pulsar timing

This is a graphical interface for the [PINT](https://github.com/NANOGrav/PINT/) Pulsar Timing packages. It is currently under construction.

It works with an embedded IPython kernel. That's where all the calculations are performed.

At the moment, not all the extended functions of Plk are implemented. If there is anything you especially want implemented, open an issue.

This project was previously under development at [vhaasteren/qtip](https://github.com/vhaasteren/qtip/) and was intended to interface with Tempo2, libstempo and Piccard too. Here, only PINT is supported.

Requirements:
=============

 * [numpy](http://numpy.scipy.org)
 * [scipy](http://numpy.scipy.org)
 * [matplotlib](http://matplotlib.org), for plotting only
 * [PINT](https://github.com/NANOGrav/PINT/)
 * PyQt4 (see below)
 * Qt version 4.x
 * IPython >= 2.0
 * pygments
 * pyzmq
 * jdcal
 * pyephem
 * h5py

PyQt on OSX
===========
Installing PyQt on OSX can best be done with macports or homebrew. If done with homebrew however, be aware that you need to add the libraries to your path by adding the following line to your .profile:

export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH


Background info
===============
Original qtip project website: http://vhaasteren.github.io/qtip

Contact
=======
 * [_Jonathan Colen_](mailto:jcolen19@gmail.com)

