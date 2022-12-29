In the case_studies directory there are 5 vulnerable web apps, a data directory, and a credsweeper directory. 

In each web app directory (such as app1_cryptomg), there is 
-> a directory with the web app name (ex, CryptOMG), which contains the web app itself 
-> {appname}_HCC.txt are all hard-coded credentials found manually
-> {appname}_benign.txt are all benign examples found manuallu
-> {appname}_numFiles.txt is a list of all files and directories in the web app
-> benign_{category}.txt are the benign examples in that category (as listed in CredData) found manually
-> {category}.txt are the malicious examples in that category found manually
-> {appname}_{category}.json are malicious examples found by CredSweeper in that category
-> {appname}.json are all malicious examples found by CredSweeper

Essentially, all data is divided by the web app from which it name from in the web app directories.


In the data directory, all data found manually from all web apps are concatentated, then divided into HCC and benign, then further divided by category (note, NOT by web app).
In the data directory there is:
-> hcc, where all hard-coded credentials found manually are located
	-> {category}.txt files located in hcc/ contain all observations found manually that fall in that category (independent of which web app it is from)
-> benign, where all benign examples found manually are located
	-> benign_{category}.txt files located in benign/ contain all benign observations found manually that fall in that category (independent of which web app it is from)


Lastly, in the credsweeper directory there are all observations found by CredSweeper divided by category, NOT by web app.
In the credsweeper directory there is:
-> {category}.json where all observations found by CredSweeper that fall in that category are located 


Generic / Vague File Structure:
-> case_studies
	-> app#_{appname}/
		-> {appname}/
		-> {appname}_HCC.txt
		-> {appname}_benign.txt
		-> benign_{category}.txt         (NOTE, multiple of these to account of multiple categories)
		-> {category}.txt                (NOTE, multiple of these to account of multiple categories)
		-> {appname}_{category}.json     (NOTE, multiple of these to account of multiple categories)
		-> {appname}.json
	-> data/
		-> hcc/
			-> {category}.txt           (NOTE, multiple of these to account of multiple categories)
		-> benign/
			-> benign_{category}.txt    (NOTE, multiple of these to account of multiple categories)
	-> credsweeper
		-> {category}.json    (NOTE, multiple of these to account of multiple categories)  
