#!/bin/bash

X_OFFSET=96
Y_OFFSET=229
FRAME=nexus-6p-frame.png
WIDTH=220

# Clean up old output files
rm -f *_framed.png morph_*.png anim.gif anim-shrunk.gif

# Overlay screenshots onto frame
for file in [0-9][0-9]_*.png
do
    base=`basename $file .png`
    composite -geometry +${X_OFFSET}+${Y_OFFSET} $file $FRAME ${base}_framed.png
done

# Create fades
convert *_framed.png 00_*_framed.png -resize ${WIDTH}x -morph 2 -adjoin morph_%02d.png
rm *_framed.png

# Create animation
convert morph_*.png +delete -set delay '%[fx:(t%3==0)?200:10]' -loop 0 anim.gif
rm morph_*.png

# Optimise animation
gifsicle -O3 --careful --colors 256 < anim.gif > anim-shrunk.gif

