# Welcome!

This is a game to teach you the basics of using a POSIX (Linux, BSD, UNIX) terminal.

## Download and unpack

If you haven't downloaded Bashcrawl yet, go to https://gitlab.com/slackermedia/bashcrawl/-/releases and download the `Source code (zip)` file.

Once the ZIP file has been downloaded to your computer, unzip it as usual.

Now it's time to try it out on your computer.

## Try it on your computer

To start playing, open a terminal.

Type the letters `cd` (just the letters and a space, not the quote marks) into the terminal...

Then a space (press the spacebar)...

Then drag and drop the `entrance` directory from this folder into your terminal.

If your terminal asks you what you want to do with what you have just dragged into it, select "Paste location".
If it doesn't ask, then expect it to paste the file path of the folder you just dragged into it.

You now have something like this in your terminal window:

```
$ cd /home/your_username/Downloads/bashcrawl/entrance
```

(The exact path to the entrance varies, depending on where you saved the file, so it's OK if it looks a little different on your computer.)

Press RETURN on your keyboard.

Your first move is very important.
Type this into your terminal:

```
cat scroll
```

You are now playing the game.
May the gods save you.

## Restarting the game

If you want a fresh start, the easiest way to start over is to trash the `bashcrawl` folder and unzip a fresh copy.

## Try it online with mybinder

- Follow this link: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/slackermedia%2Fbashcrawl/HEAD).
- Wait a few seconds to a minute until the launcher appears.
- Click on the Terminal icon.

Note: mybinder sessions are temporary; the game is reinitialized each
time you disconnect.
[Learn more about the mybinder service](https://mybinder.readthedocs.io/en/latest/).

## NOTES FOR macOS X

It appears that there is a problem with the standard `Archive Utility` that is called from `Finder` when a zip archive is double-clicked to extract to the current folder, if you're downloading the archive from GitLab rather than using git's `clone` facility to download the game.  You may find that all of the files in the destination folder are set to be executable.  This will cause great confusion as you play the game as intended, because every plain text file will be indistiguishable from executable scripts.  Here's how to avoid this problem:

1.  Open your favorite terminal emulator app (for example, `Terminal.app` or `iTerm2`).
1.  Navigate to the directory where you want to unpack the zip archive:
    ```
    cd /path/to/destination
    ```
    Replace `/path/to/destination` with the relative (does not start with slash `/`) or absolute (starts with slash `/`) path to your desired destination.
1.  Type `unzip ` (that's `unzip` followed by a *space*)
1.  From the `Finder`, drag the `bashcrawl-master.zip` to your terminal emulator window.  The absolute path to your downloaded archive is pasted into your terminal window, leaving you with:
    ```
    unzip /Users/your_username/Downloads/bashcrawl-master.zip
    ```
1.  Press RETURN on your keyboard to unpack the contents of the zip archive.
1.  In the terminal window, change directory to `bashcrawl-master/entrance`:
    ```
    cd bashcrawl-master/entrance
    ```

Now you're in the game!  Have fun!
