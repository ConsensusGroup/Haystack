#!/bin/sh
#!/bin/ipython

function Receiver_Module_Function() {
	Receiver_Module=$1
	Seed=$2
	output=$(ipython $Receiver_Module "$Seed")
	echo "$output"
}

