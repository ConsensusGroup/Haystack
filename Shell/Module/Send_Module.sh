#!/bin/sh
#!/bin/ipython

Sender_Module=$1
Receive=$2
Seed=$3
Message=$4
Sender_Address=$5

python $Sender_Module "$Seed" "$Receive" "$Message" "$Sender_Address"
