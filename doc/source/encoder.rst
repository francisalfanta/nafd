=======
Encoder
=======

About :term:`NAFD` Encoder: assign by the Network and Facility Division Chief to carry out clerical task such as Encoding Licenses and Permits.


:term:`NAFD` :term:`Work flow`
------------------------------

	===  =========================  =========  
	ID   Task                       Encoder  
	===  =========================  =========  
	1    :ref:`checklist-reqd`      \          
	2    :ref:`checklist-soa`       \          
	3    :ref:`checklist-payment`   \        
	4    :ref:`checklist-eval`      \          
	5    :ref:`checklist-endorse`   \          
	6    :ref:`checklist-encoding`  |check|          
	7    :ref:`checklist-review`    \          
	8    :ref:`checklist-sign`      \          
	9    :ref:`checklist-chief`     \        
	10   :ref:`checklist-direct`    \        
	11   :ref:`checklist-cashier`   \        
	12   :ref:`checklist-release`   \        
	===  =========================  ========= 

.. |check| image:: /images/check.png
   :height: 25px
   :width: 25px
   :alt: Check

.. _checklist-encoding:

Encoding
^^^^^^^^
	
	Assign by an Engineer to process Licenses or Permits required by applications.

	This is a segment in :term:`work flow` to upload the encoded records found in MS-Excel or MS-Word. 

	Listed below are guides to what to upload depending on the application type. 
	
	For MS-Excel the application types are as follows:
		#. :term:`NEW`
		#. :term:`MOD`
		#. :term:`REN` /:term:`MOD`
		#. Permit to Possess (Storage) only

	For MS-Word the application types are the details of Permits encoded such as:
		#. Permit to Purchase only
		#. Permit to Possess only
		#. Demo Permit only
		#. Temporary Permit only

	Once you are done signing the printed documents, click the check box and press submit button.

	.. image:: /images/encoder/encoding.png
		:width: 834px
		:align: center
		:height: 151px
		:alt: Status: Encoding

Uploading files
^^^^^^^^^^^^^^^
	
	For MS-Word:

		#. Click *Upload MS-Word* found under Action column. You will be forwarded to *Permit Files* list page.

			.. image:: /images/encoder/upload_word_1.png
				:width: 469px
				:align: center
				:height: 229px
				:alt: Permit Files page 

		#. Click *Add Permit* button to add new.

			.. note:: Only MS-Word is accepted.

			.. image:: /images/encoder/upload_word_2.png
				:width: 247px
				:align: center
				:height: 119px
				:alt: Add File

		#. You have an option to click Logbook No to edit existing file.

			.. image:: /images/encoder/upload_word_21.png
				:width: 438px
				:align: center
				:height: 69px
				:alt: Edit File

		#. Click *Save* button once all information are properly supplied.

			.. hint:: If you want to save then create new entry click *Save and add another*. If you want to save then continue working click *Save and continue editing*

	For MS-Excel:

		#. Click *Upload MS-Excel* found under Action column. You will be forwarded to Logbook page. 

			.. image:: /images/encoder/upload_excel_1.png
				:width: 394px
				:align: center
				:height: 251px
				:alt: Action button to upload page 

		#. Below the Logbook page a button for uploading PPP or RSL can be found. Click the appropriate button for what is required to accomplish.

			.. image:: /images/encoder/upload_excel_2.png
				:width: 461px
				:align: center
				:height: 53px
				:alt: Upload button for PPP or RSL

		#. A pop-window will appear with a submit button. Click the *Choose File* button to select your file. 

			.. note:: Only MS-Excel file with pre define column format will be accepted.

			.. image:: /images/encoder/upload_excel_3.png
				:width: 366px
				:align: center
				:height: 151px
				:alt: Choose File

		#. Click *Load data* button to upload the data on the pop up window.

		#. The uploaded file will be displayed for final checking. Verify encoded data according to data type columns.

			.. caution::  MS-Excel Date column is in format of *mm/dd/yy*. MS-Excel Number column should not contain character or special character such as dash or comma.


		#. If the data *Is good* click the check box to confirm and press submit button.

			.. hint:: Uploaded information will be displayed in Logbook page after successful upload.

			.. image:: /images/encoder/upload_excel_4.png
				:width: 366px
				:align: center
				:height: 141px
				:alt: Choose File


Adding Records Manually
^^^^^^^^^^^^^^^^^^^^^^^

	Application filed can contain many equipment. Upon importing RSL or PPP using the *Uploading files* instruction fail or with other reason you want to add new record you have an option to manually type the information.

	Here's the instruction for adding *new*  **Equipment**.		

		.. image:: /images/encoder/equipment.png
				:width: 465px
				:align: center
				:height: 31px
				:alt: Equipment

		1. Go to *Home page* then find the name called Equipment.

		.. important:: Supply the information on the following relevant fields found in the Equipment page. All of these fields are required unless stated optional.

		2. *Call-Sign*

		3. *Status*

		4. *Make/Model* 

		5. *Serial No.* - type one serial number per equipment

		6. *Power* - the numerical power value of the equipment

		7. *Unit* - the power unit

		8. *Bandwidth* - the field for bandwidth together with emission type

		9. *Equipment Usage* - choose between *Main* as the primary equipment or *Protection* as a backup equipment

		10. *Frequency Range* - all values should be decimal or integer.

		11. *Transmit/Recieved* - all values should be decimal or integer.

		12. *Permits* - the issued control No Permits.

		13. *Public Telecom Entity* - type Company name

		14. *Antenna Details* - type the antenna type

			.. important:: Check the particular of antenna information if it match the Antenna details.


	Here's the instruction for adding *new*  **Radio Station License**.

		.. image:: /images/encoder/rsl.png
				:width: 468px
				:align: center
				:height: 31px
				:alt: Latest Radio Station License

		1. Go to *Home page* then find the name called Latest Radio Station License.

		.. important:: Supply the information on the following relevant fields found in the Radio Station License page. All of these fields are required unless stated optional.

		2. *Logbook*

		3. *Public Telecom Entity*

			type Company name

		4. *Status*

		5. *Date Issued*

		6. *License No.*

		7. *Form Serial No.*

		8. *Capacity*

		9. *Class of Station*

		10. *License to Operate*

			auto-fill up fields

		10. *Nature of Service*

		11. *Point of Service*

		12. *Sitename*

		13. *Steet* 

			auto-fill up fields depending on Sitename

		14. *City*

			auto-fill up fields depending on Sitename

		15. *Province*

			auto-fill up fields depending on Sitename

		16. *Region*

			auto-fill up fields depending on Sitename

		17. *Longitude*

			auto-fill up fields depending on Sitename

		18. *Latitude*

			auto-fill up fields depending on Sitename

		19. *Remarks*

		20. *Encoder*

			add by searching username or first name

		21. *Evaluator*

			add by searching username or first name

		22. *Signatory*

			the Deparment Head name, add by searching username or first name

		23. *Related Equiments*

			click *add another Equipment for RSL* then search by serial no or call-sign

		24. *Related Official Receipts*

			click *add another Official Receipt for RSL* then search by O.R. number.


