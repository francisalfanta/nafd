.. NAFD Logbook documentation master file, created by
   sphinx-quickstart on Wed Apr 16 12:25:37 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NAFD Logbook's documentation!
========================================

Contents:

.. toctree::
   :maxdepth: 2

   intro
   user_manual  
   dev_manual
   nafd_glossary    

NAFD Flow chart
^^^^^^^^^^^^^^^

.. blockdiag::

	diagram {
		Application -> "Checking requirement" -> "Issuance of SOA"-> Payment;
	}

.. blockdiag::

	diagram {
		Payment -> Evaluation;
	}

.. blockdiag::
	
	diagram {
		Evaluation -> Endorsement -> Encoding;
		Evaluation -> Encoding;
		Evaluation -> Pending;		
	}

.. blockdiag::

	diagram {
		Encoding -> Review -> "Signature of Approval";
	}

.. blockdiag::

	diagram {
		"Engr Approval" -> "NAFD Chief Approval" -> "RB Director Approval";
	}

.. blockdiag::

	diagram {
		"RB Director Apporval" -> "Cashier Stamp" -> "Release-Secretariat";
	}

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`




