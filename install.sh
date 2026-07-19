#!/data/data/com.termux/files/usr/bin/bash


TARGET="$PREFIX/bin/anbe"


cp launcher.py "$TARGET"


chmod +x "$TARGET"


echo
echo "ANBE installed:"
echo "$TARGET"
echo
echo "Usage:"
echo "  anbe build ~/project"

