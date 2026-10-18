TEJ Linux Offline Kit
=====================

This folder is designed to be copied to a USB drive and used without Internet access.

START HERE
----------

Copy TEJ-Linux-Offline-Kit.zip from the class USB drive to Downloads and extract it. Open START-HERE.html in the extracted folder. It works without Internet, links to every assignment, and explains which file to use.
Print PRINTABLE-QUICK-START.pdf when students need the same instructions on paper.

WHAT IS INCLUDED
----------------

assignments/
  Editable DOCX and ODT copies of the three student assignments, plus PDF reference copies.

answers/
  Plain-text answer sheets for students who do not have an office program.

bashcrawl/
  A complete offline copy of Bashcrawl. Git and Internet access are not needed.

tej-xfce-style.sh
  The Linux Mint Xfce appearance script. It changes only the signed-in user's Xfce settings and never uses sudo.

WHICH DOCUMENT FORMAT SHOULD I USE?
-----------------------------------

Linux Mint normally includes LibreOffice Writer. Use the ODT file in LibreOffice when possible. DOCX also works in LibreOffice, Microsoft Word, and many other office programs. PDF is for reading or printing and is not the preferred editable submission.

If no office program is installed, open the matching file in answers/ with a text editor, type underneath each prompt, and save it with your name in the filename.

QUICK SOFTWARE CHECK
--------------------

On Linux Mint, open Terminal and run:

  libreoffice --version

If a LibreOffice version appears, it is ready. If the command is missing and the computer is offline, use the plain-text answer sheet. Do not install unknown software from the USB drive.

START BASHCRAWL OFFLINE
-----------------------

1. Copy the complete bashcrawl folder from the extracted kit.
2. In Files, open Home, create a folder named Games, and paste bashcrawl inside it.
3. Open Terminal with Ctrl + Alt + T in Linux Mint, including a live USB session.
4. Move into the entrance folder. For example:

   cd ~/Games/bashcrawl/entrance

5. Start the game:

   cat scroll

Hidden folders are part of the game. Copy the entire bashcrawl folder, including files whose names begin with a dot.

CHROMEBOOK
----------

On a personal Chromebook or owner account, enable the Linux development environment while Internet access is available:

  Settings > About ChromeOS > Developers > Linux development environment > Set up

Open Terminal from the Launcher. In the Files app, move the complete bashcrawl folder into Linux files. A school-managed Chromebook may block Linux. Do not use Developer Mode to bypass that restriction.

PHONE OR TABLET
---------------

Using a phone is slower and more difficult than using a computer, but it works. A Bluetooth keyboard makes the work easier.

Android: install Termux from F-Droid. Terminal Quest works directly in Termux. For Bashcrawl, run pkg update and then pkg install git while Internet access is available.

iPhone or iPad: install iSH Shell. Run apk update, apk add bash git, and then bash while Internet access is available.

If you are waiting for a classroom computer or Internet connection, use your phone to begin or continue the assignment instead of doing nothing.

SUBMITTING LATER
----------------

Save completed work locally. When Internet access returns, upload the completed DOCX, ODT, or TXT file to the Google Classroom assignment. Do not include passwords, tokens, Wi-Fi credentials, or other private information.

LICENSING
---------

Technology Commons teaching materials are CC BY-SA 4.0. Bashcrawl is included unmodified under GNU GPL v3; its original LICENSE and README are preserved inside the bashcrawl folder. See SOURCES.txt for source links and version details.
