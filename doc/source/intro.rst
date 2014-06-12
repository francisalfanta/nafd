============
Introduction
============


Parts of Logbook page
---------------------


Navigation bar
^^^^^^^^^^^^^^
  
	
	.. image:: /images/navigation.png
		:width: 225px
		:align: left
		:height: 178px
		:alt: Logbook Navigation bars

	.. container:: custom

		**Task**

		A list of task currently assign to you. 
		The tasks were arranged as latest entry on top.

		**Processing**

		A list of task received for processing.
		This contains the task assign to you and other member’s task.
		The lists are arranged by self priority.

		**Pending**

		This are lists of application with pending status.

		**Unassign**

		This are lists of application with no personnel in charge.

		**Completed**

		This are applications that were completed for the last 30 days.	

Key Performance Indicator
^^^^^^^^^^^^^^^^^^^^^^^^^
	
	.. image:: /images/kpi_legend.png
		:width: 227px
		:align: left
		:height: 260px
		:alt: KPI Legend

	.. container:: custom

		**Permit to Purchase/Possess**

		This is a color *light green* progress bar located on the top most.

		**Construction Permit**

		This is a color *gold* progress bar located as the second top most.

		**Radio Station License**

		This is a color *light blue* progress bar located below Construction Permit bar.

		**Modification RSL**

		This is a color *yellow* progress bar located below RSL bar.

		**Permit for Storage**

		This is a color *silver* progress bar located below Modification RSL bar.

		**Temporary Permit**

		This is a color *orange* progress bar located below Permit for Storage.

		**Demo Permit**
		
		This is a color *violet* progress bar located below Permit for Temporary Permit.

		**Duplicate RSL**
	
		This is a color *brown* progress bar located below Permit for Demo Permit.				

		.. note:: Color *Red* progress bar means the application was processed beyond specified due date.

	.. image:: /images/kpi_graph_title.png
		:width: 628px
		:align: left
		:height: 34px
		:alt: KPI Graph Title

	**Graph Title**
		*Username* - (e.g. *Erwin*) the progress report for this user.

		*Total value* 

			dividend or numerator (e.g. *286*) - the total number of units/stations processed so far.
			
			divisor or denominator(e.g. *5000*) - the user's over-all KPI target for that year.

	

Log Entry
^^^^^^^^^

	.. image:: /images/log_entry.png
		:width: 838px
		:align: center
		:height: 158px
		:alt: Log Entry

	.. container:: custom

		**Control No**

			* Each Applications contain *unique number*.
			* *Status*

				* The current progress of the application.
				* It is currently assign to whom.

		**Task**

		The task column contains essential information to distinctly identify the contents of each application.

			* *Applicant name*
			* *Type of application*
			* *Number of units* applied 
			* *Number of Station License* applied
			* *PPP details*

				* Information details for Permit to Purchase/Possess if already uploaded to the database.				
				* Clickable if the type of application falls within PPP and Storage.

			* *CP/RSL details*

				* Information details for Construction Permit and Radio Station License if already uploaded to the database.
				* Clickable if the type of application falls within CP and RSL.

		**Action**

			* An upload button or select button for the users to finished the task. 
			* This varies from the current progress of the application and user permission doing the task.
			* It also has links for uploaded file.

			* :term:`Due date` can be seen in the lower right of the column.

				* The application processing allotted time frame computed according to CSC Citizen Charter.
				* Holidays and weekend are not included when counting processing time.
		
		**Progress Bar**

		* Bar indicator for application progress report.

		.. image:: /images/task_legend.png
			:width: 225px
			:align: center
			:height: 172px
			:alt: Log Entry			

		* Color coding
				
				*Orange*
					indicates an incoming application task.

				*Green*
					indicates currently processed by you.

				*Yellow*
					indicates the application task will return to you.

				*Red*
					indicates pending application according to the reason noted by the Engr.

				*Gray*
					indicates the application has completed the process according to the Division work flow.


NAFD :term:`Work flow` and Permission level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	===  =========================  =========  =======  ========
	ID   Task                       Secretary  Encoder  Engineer
	===  =========================  =========  =======  ========
	1    :ref:`checklist-reqd`      \          \        |check|  
	2    :ref:`checklist-soa`       \          \        |check| 
	3    :ref:`checklist-payment`   |check|    \ 	    \ 	
	4    :ref:`checklist-eval`      \          \        |check|
	5    :ref:`checklist-endorse`   \          \        |check|
	6    :ref:`checklist-encoding`  \          |check|     \ 
	7    :ref:`checklist-review`    \          \        |check|
	8    :ref:`checklist-sign`      \          \        |check|
	9    :ref:`checklist-chief`     |check|    \        \   
	10   :ref:`checklist-direct`    |check|    \        \  
	11   :ref:`checklist-cashier`   |check|    \        \  
	12   :ref:`checklist-release`   |check|    \        \  	
	===  =========================  =========  =======  ========

.. |check| image:: /images/check.png
   :height: 25px
   :width: 25px
   :alt: Check

CSC Citizen Charter
^^^^^^^^^^^^^^^^^^^

	pass








