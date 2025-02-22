### What is this?`


Random tools I have used for processing datasets for machine learning. Processing large amounts of metadata, or simply wanting to ripgrep all mentions of a sequence of words and then trim+copy it to an output directory of your choice is also a good usecase. Such as when conducting Penetration testing or forensics on entire OS filesystems. 

Why? Python is OS agnostic. Does not matter if your are working in Linux, BSD, or Windows. Most systems that do not have Python in the path, can still often manage to get an interpreter by utilizing an IDEs venv (for penetration testing purposes specifically).


### recursve_csv_parsing

```
	
	Process CSV files in the input directory (and optionally its subdirectories).
	Only lines containing the specified phrase are written to the output directory.

	Replace extension type and paths in the script depending on your needs.
	Add multithreading if performance is of importance VS stealth or background processing.
    
```

### hf-recursivesubdir

```
		this downloads only a folder and all subfolders from a huggingface repo. 
		This is useful if the dataset contains many terabytes of data.
	
```	

### selective_tarball_ripper

```

	You need to change the column corresponding to the column in the medata.csv. For me, it was column 7.
	
	You also need to set git credentials hugging face token for Windows. For Linux, set it as an env var or in the gnome authentication key ring. Or just hardcode it (don't, this is a terrible idea unless you manually revoke the access token once done).
	
	This script is used after the recursive cloning of the metadata, and cleaning of the metadata using hf-recursivesubdir.sh and selective_tarball_ripper.py

	This script is used to recursively match and download the data from datasets stored inside tarballs (tar.gz) files on huggingface dataset repositories.
	
	This should work on other LFS git-sites. Note that this might be easier to perform using specific streamed, split code such as in the repo I used. You might need to adjust the hugging face logic, and authentication env variables, obviously.
	
	But it is not universal, and for file extraction, the old fashioned way of selective and recursive ripping is consistent.

```
