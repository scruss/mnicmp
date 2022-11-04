# mnicmp

Stewart C. Russell - scruss.com
2017-02

a 7-pin dot matrix font based on the DECwriter II output, with some
international characters added from the DECwriter III character set,
and then some additional ones created by me.

## Name

Digital Equipment Corporation (DEC) used to make minicomputers. The
older ones of these only supported 6.2 file names, so the word
‘minicomputer’ would have to be rendered as ‘mnicmp’.

Few of them supported lower-case, so let's just skip that detail.

## Coverage

*Most* of ISO-8859-15, but not all of it. The DECwriter II only
supported a subset of ASCII, and the DECwriter III added a very few
European characters

## Design Size

If printed at 12 pt with no additional line spacing, you should match
the DECwriter's 10 cpi horizontally and 6 lpi vertically.

## Variants

While the DECwriter only had one type style, I added more:

* **Italic** — this is done by shearing the array of points and
  replacing them with circular dots. Using a regular italicize
  function produces ugly oval dots.
  
* **Bold** — this mimics double-striking, with the second character
  offset ½ of the dot width. It looks better than it should.
  
* **Bold Italic** — skewed and double-struck.

* **Light** and **Light Italic** — lightened the font by making the
  circles smaller. As none of the dots overlap, this might make a
  decent stencil font.

Noticing that the dots could be arbitrary shapes, I got a bit carried
away:

* **Diamond-shaped dots** - the matrix is made of rounded diamonds
  instead of circles. Also provided in italic.
  
* **Square dots** — very blocky indeed. Also provided in italic.

* **Star-shaped dots** — exceedingly silly and twinkly. Would have
  been a great way to punch holes in paper on a real dot matrix
  printer. Also provided in italic.
  
And then there's [LoveMatrix](https://fontlibrary.org/en/font/lovematrix), which uses the same dot matrix layout but with tiny hearts ...

## Source

Source to all fonts is included in FontForge format. The small Python
program used to create the fonts from JSON data is also included. You
may create your own new variants/characters **provided that** that you
do *not* use the reserved name ‘mnicmp’.

If you wish to make you own characters, the JSON structure is a
hash/dictionary of dot bitmap arrays against unicode character:

     chars = {
              ...
              'A':  ['...#...',
                     '..#.#..',
                     '.#...#.',
                     '#.....#',
                     '#.#.#.#',
                     '#.....#',
                     '#.....#'],
              ...
             }

Everything that's a # counts as a dot; everything else is
ignored. Character order doesn't matter.

If you wish to preserve the original DECwriter look, remember that it
couldn't have two adjacent horizontal pixels struck across a 7 pixel
character. So the most pixels you can have struck across is character
is 4 out of 7.

## Licence

Copyright © 2017, Stewart C. Russell (scruss.com),
with Reserved Font Name mnicmp.

This Font Software is licensed under the SIL Open Font Licence, Version 1.1.
This licence is included, and is also available with a FAQ at:
http://scripts.sil.org/OFL

[I do not agree with SIL's missionary work in any way, and the use of
this licence is in no way an endorsement of SIL.]

## Reference

* **ASCII char matrics** — LA36 DECwriter II Maintenance Manual,
pub. Digital Equipment Corporation - Maynard, MA; First Edition,
June 1975. Copyright © 1975 by Digital Equipment Corporation, part no
EK-LA36-MM-001. URL:
http://www.textfiles.com/bitsavers/pdf/dec/terminal/la36/EK-LA36-MM-001_LA36_DECwriter_II_Maintenance_Manual_Jul75.pdf. See
Table 1-1 Standard ASCII Character Set and Code (p.1-2 - folio 15) - [page image](https://archive.org/details/bitsavers_dectermina6DECwriterIIMaintenanceManualJul75_44563519/page/n14/mode/1up)

* **Intl char matrices, print sizes** — LA120 Technical Manual,
Digital Equipment Corporation - Maynard, MA; First Edition,
January 1980. Copyright © 1980 by Digital Equipment Corporation, part
no EK-LA120-TM-001. URL:
ftp://bitsavers.informatik.uni-stuttgart.de/www.computer.museum.uq.edu.au/pdf/EK-LA120-TM-001%20LA120%20Technical%20Manual.pdf. See
Table 3-3 Code Differences Among National Character Sets (p.3-7  - folio 51)

## A note on underlining, overstriking and bold

If in doubt, don't. The DECwriter supported none of these. It had 7 vertical pin positions and no descenders. Its underline row was the baseline of all characters. Its minus character was at roughly x-height, so is not useful for overstriking. To illustrate this, here are the pin maps of `-`, `m` and `_`:

```
       .......          .......          .......  
       .......          .......          .......  
       .......          #.#.#..          .......  
       #.#.#.#          #..#..#          .......  
       .......          #..#..#          .......  
       .......          #..#..#          .......  
       .......          #..#..#          #.#.#.#  
```

Note that there are no pin positions below the baseline. The fonts all include the standard algorithmic outline underbar/underline at 100 units below the standard baseline (200 units) in a 1000 unit em. It looks nothing like anything the DECwriter could do. You can't *not* have an underline position in a font, so it had to go somewhere

## Other cuts by other people

* [Sevenpins](http://fontstruct.com/fontstructions/show/1156146/sevenpins_1 "Sevenpins") is also based on DECwriter matrices, but with different spacing.
