#!/bin/bash

## Pipemenu to browse folders recursively
## ENV
SAVEIFS=$IFS;
IFS=$(echo -en "\n\b");
SCRIPT=$0;
DIR_PATH=$1;
DIR_PATH=${DIR_PATH/\~/$HOME};
[ "$DIR_PATH" == "" ] && DIR_PATH=$HOME"/";
[ "${DIR_PATH: -1}" != "/" ] && DIR_PATH=$DIR_PATH"/";


## Configuration
SHOW_HIDDEN=false;
SHOW_FULLPATH=false;

## General functions
function find_cmd(){
	# $1 -> folder to read
	# $2 -> type of file to get
	if [ -z "$2" ]; then file_type="f";
	else file_type=$2;
	fi

	hidden_files="";
	if [ "$SHOW_HIDDEN" == "false" ]; then hidden_files='-not -name ".*" ';
	fi

	cmd=( find );
	cmd+=( "$1" );
	cmd+=( -maxdepth 1 );
	[ "$SHOW_HIDDEN" == "false" ] && cmd+=( -not -name '.*' );
	cmd+=( -type "$file_type" );
	cmd+=( -printf %f\\n );

	exec "${cmd[@]}" | sort;
}

## Formating functions
function sanitize(){
	output=$1;

	output=${output//&/&amp;};
	output=${output//</&lt;};
	output=${output//>/&gt;};
	output=${output//\'/&apos;};
	output=${output//\"/&quot;};
	output=${output//\~>/&#126;};

	echo $output;
}

function folder_label(){
	# $1 -> folder path
	output=$1;
	[ "${output: -1}" == "/" ] && output=${output: : -1};
	if [ "$SHOW_FULLPATH" == "false" ]; then
		output=$(basename $output);
	fi;
	echo $output;
}


## XML functions
function generate_main(){
	# $1 -> folder to read
	if [ -z "$1" ]; then
		echo "<item label=\"Empty folder\"></item>"
	else
		folders=$(generate_folders $1);
		files=$(generate_files $1);
		xml="<separator label=\"$(sanitize $(folder_label $1))\" />";
		if [ -z "$folders" ] && [ -z "$files" ]; then
			xml=$xml"<item label=\"Empty folder\"></item>";
		else
			xml=$xml$folders;
			if [ ! -z "$folders" ] && [ ! -z "$files" ]; then
				xml=$xml"<separator />";
			fi
			xml=$xml$files;
		fi
		echo $xml;
	fi
}

function generate_folders(){
	# $1 -> folder to read
	out="";
	for x in $(find_cmd $1 d); do
		[ "${x: -1}" == "/" ] && continue;
		out=$out"<menu id=\"db-menu-$(sanitize $x)\" label=\"$(sanitize $x)\" execute=\"'$SCRIPT' '$(sanitize $1$x)'\" />";
	done
	echo $out;
}

function generate_files(){
	# $1 -> folder to read
	output="";
	for x in $(find_cmd $1 f); do
		output=$output"<item label=\"$(sanitize $x)\">"
		output=$output"<action name=\"execute\">";
		output=$output"<execute>";
		output=$output"xdg-open '$(sanitize $1$x)'";
		output=$output"</execute>";
		output=$output"</action>";
		output=$output"</item>";
	done
	echo $output;
}


out="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
out=$out"<openbox_pipe_menu>";
out=$out$(generate_main $DIR_PATH);
out=$out"</openbox_pipe_menu>";


echo $out;
IFS=$SAVEIFS;
