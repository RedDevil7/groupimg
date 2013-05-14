#!/bin/bash
ext="jpg;png;gif"
filelist_prefix="filelist_"

folder="$1"
if [ ! -d "$folder" ]; then
	[ -n "$folder" ] && (echo Error: folder \""$folder"\" does not exist. >&2)
	echo Usage: "$0" FOLDER >&2
	exit 1
fi

find_expr=$(sed 's/;/ -or -iname \\*./g;s/^/-iname *./g' <<< $ext)
find "$folder" -type f $find_expr|split -d - "$filelist_prefix"

subscript='
while read path; do
	hash=0
	echo -e "$path\t$hash"
done <$0
'

parallel sh -c "$subscript" -- "$filelist_prefix"*
rm -- "$filelist_prefix"* 2>/dev/null
