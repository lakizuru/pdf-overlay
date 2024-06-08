# PDF Overlay
```
   _____  _____  ______    ____                 _             
  |  __ \|  __ \|  ____|  / __ \               | |            
  | |__) | |  | | |__    | |  | |_   _____ _ __| | __ _ _   _ 
  |  ___/| |  | |  __|   | |  | \ \ / / _ \ '__| |/ _` | | | |
  | |    | |__| | |      | |__| |\ V /  __/ |  | | (_| | |_| |
  |_|    |_____/|_|       \____/  \_/ \___|_|  |_|\__,_|\__, |
                                                         __/ |
                                                        |___/ 
```

A Python script which processes a multi-page PDF to remove white backgrounds from its pages and overlays them onto another PDF which is optimized for reduced file size while maintaining acceptable image quality through JPEG compression and resolution adjustment. Perfect for merging annotated or highlighted documents onto standardized templates.

#### Developed by Lakisuru Semasinghe (https://github.com/lakizuru)

## Use Case

You have PDF1 with some content as shown in Image 1.
You also have PDF2 with the annotations for the PDF1 as shown in Image 2.
You need to overlay PDF2 content on PDF1 as shown in Image 3.

| PDF1 (Background) | PDF2 (Foreground) | Output (Overlayed PDF) |
| -------- | ------- | ------- |
| <img src="docs\background_test1.jpg" alt="Image 1" width="200"/> | <img src="docs\foreground_test1.jpg" alt="Image 1" width="200"/> | <img src="docs\output_test1.jpg" alt="Image 1" width="200"/> |

To fulfill this requirement, you can use **PDF Overlay**.



## Prerequisites
To use PDF Overlay CLI, the following dependancies have to be satisfied.
- Python3
- PIP3
- GhostScript
- PyMuPDF
- Pillow
- tqdm
- pyfiglet

Also, PDF Overlay only supports PDF files with **same pages count**.

## How to Use

To overlay PDFs, follow the steps below. (You may skip the steps if you have already fulfilled them earlier)
 1. Install Python3 and PIP
 ```
sudo apt update
sudo apt install python3 python3-pip ghostscript
```
 2. Install the following PIP3 modules.
 ```
pip install PyMuPDF Pillow pyfiglet tqdm
 ```
 3. Run the script.py as follows.
 ```
 python3 script.py <foreground_pdf_path> <background_pdf_path> <output_pdf_path>
 ```

<img src="docs\Screenshot.jpg" alt="Screenshot"/>

 For quick help, use `python3 script.py -h`