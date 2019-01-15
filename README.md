# inTriplicate
## A Python script used to fix my dad's SD-card-as-archive habit.

## What problem does this solve?

SD Cards and flash memory store data in the form of charged cells. If the cells are not written every four years or so, there is a chance the data in those cells could be lost to the sands of time.

My father has a habit of taking the SD Cards from digital cameras and putting them on a shelf as flash media. Eventually, due to charge degradation, these will be useless. The idea here is to make it easy for him to label what he has, refresh the flash media, made multiple copies of the data (parity/optical/hard disk/cloud), and move on to the next card in an automated fashion. 

## Prerequisites

Python installed. I am using anaconda available from [[https://www.anaconda.com/download/]]
Install the following pip packages
```
pip install burn              #for cd/dvd/dvd-dl burning
pip install par2deep (--user) #for parity file generation
```

## Usage

This will guide you through the process with a text driven prompt that will ask what options you want turned on:
```
py inTriplicate.py
```

This will run with minimum prompts, and all options turned on:
```
py inTriplicate.py --source=/media/myFlashdrive --burn-cd --copy-to=/mnt/sdb1/pictures --refreshFlash --generate-galleries --generate-parity
```


###  The Process, in Plain English.

(Steps 2-6 are automated by this script)

0) Manual. Run inTriplicate with the options you want.
1) Manual. Take an SD card and put it in the computer. Figure out approximately what time the pics were taken using the files date stamps, and write a description of the contents and the dates on a post it note.
2)  Automated. Use a parity program to add some parity files to the SD card. These are small files that provide redundancy information in case a specific file gets damaged.
3)  Automated. Run a program to generate a photo gallery such as a web page with image previews, to the SD Card
4)  Automated. Run flash refresher, to restore the charge on the SD card and give it another four years.
5)  Automated. Copy the contents of the SD card into a folder on a removeable hard drive such as the one you bought for the pogo plug. This hard drive will eventually be stored in a place seperate from the CD binder. 
6)  Automated with prompt to insert disc. Burn the contents of the SD card to a single CD or DVD. Prefer CD over DVD and DVD over DVD-DL if its small enough. Write what you have on the post it on the disc as well with sharpie.
7) Manual. Place the post-it, SD card, and disc into the CD binder in a pocket in a place that makes sense (have tabs like the year the pictures were taken)

