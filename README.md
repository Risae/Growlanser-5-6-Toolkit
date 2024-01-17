Work-In-Progress Growlanser 5 and 6 Toolkit, written in Python. Only tested on Windows x64.

The following dependencies exist in order for the Toolkit to work:

- `GL 5/6 Toolkit` = [Python 3.11.7](https://www.python.org/)
- [abcde](https://www.romhacking.net/utilities/1392/) = [Strawberry Perl 5.32.1.1](https://strawberryperl.com/) (or Linux package)
- [quickBMS](http://aluigi.altervista.org/quickbms.htm) = Windows / Linux x64

Directory structure:

    /.github/workflows      contains the GitHub Workflow file, which automatically creates xDelta patches
    /3rdparty               holds the 3rd party programs, which are used for Growlanser file extraction/modification
    /source                 directory which contains the Python scripts
    /source/functions       directory which contains the Python functions

`abcde` & `quickBMS` are inside the folder `3rdparty`. You need to extract `Strawberry Perl Portable` inside the `3rdparty`. After that, everything "should" work out of the box. Temporary PATHs will be created that point to the programs inside the folder `3rdparty` so Perl (`abcde`) scripts work.

Growlanser 6 English Translation blog: https://growlanser6english.blogspot.com/<br>
Growlanser 6 Discord: https://discord.gg/59Nw2U2<br>
Growlanserver Discord: https://discord.gg/uVh3XxRGtG<br>
Growlanser 6 English Translation GitHub: https://github.com/Risae/Growlanser-6-English-Translation