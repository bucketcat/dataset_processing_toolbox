### What is this?`


Random tools I have used for processing datasets for machine learning. Processing large amounts of metadata, or simply wanting to ripgrep all mentions of a sequence of words and then trim+copy it to an output directory of your choice is also a good usecase. Such as when conducting Penetration testing or forensics on entire OS filesystems. 

Why? Python is OS agnostic. Does not matter if your are working in Linux, BSD, or Windows. Most systems that do not have Python in the path, can still often manage to get an interpreter by utilizing an IDEs venv (for penetration testing purposes specifically).


### recursve_csv_parsing

	```
    Process CSV files in the input directory (and optionally its subdirectories).
    Only lines containing the specified phrase are written to the output directory.
	Replace extension type and paths in the script depending on your needs. Add multithreading if performance is of importance VS stealth or background processing.
    ```