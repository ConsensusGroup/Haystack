#!/bin/sh
function Address_Generator () {
	Address_Generator_Script=$1
	Seed=$2
	output=$(ipython $Address_Generator_Script "$Seed")
	echo "$output"
}

