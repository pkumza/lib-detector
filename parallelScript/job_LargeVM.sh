#!/bin/bash
NOW=$(date +"%Y%m%d%H%M")
Today=$(date +"%Y%m%d")

#instanceArray stores all instance public ip
instanceArray=()
instanceArray[0]="52.4.183.137"
instanceArray[1]="52.5.179.64"
instanceArray[2]="52.5.153.6"
instanceArray[3]="52.5.180.77"
instanceArray[4]="52.3.29.217"
instanceArray[5]="52.5.177.238"
instanceArray[6]="52.3.12.143"
instanceArray[7]="52.4.175.252"
instanceArray[8]="52.3.169.252"
instanceArray[9]="52.5.3.74"
instanceArray[10]="52.5.178.11"
instanceArray[11]="52.5.178.240"
instanceArray[12]="52.4.243.43"
instanceArray[13]="52.5.183.128"
instanceArray[14]="52.5.183.140"
instanceArray[15]="52.4.149.95"
echo ${instanceArray[*]}

i=0
while [ $i -lt ${#instanceArray[@]} ]; do
  scp -i ~/maza_aws_virginia.pem setup.py ubuntu@${instanceArray[$i]}:
  ssh -i ~/maza_aws_virginia.pem ubuntu@${instanceArray[$i]} "python ~/setup.py"
  echo $i
  ssh -i ~/maza_aws_virginia.pem ubuntu@${instanceArray[$i]} "sudo mkdir -p /home/ubuntu/parallelLog/$NOW/instance-$i/ "
  ssh -i ~/maza_aws_virginia.pem ubuntu@${instanceArray[$i]} "sudo touch /home/ubuntu/parallelLog/$NOW/instance-$i/filelist.txt"
  ssh -f -i ~/maza_aws_virginia.pem ubuntu@${instanceArray[$i]} "screen -dm sudo python /home/ubuntu/python_static_analyzer/main_LargeVM.py /home/ubuntu/parallelLog/$NOW/instance-$i/ /home/ubuntu/python_static_analyzer/parallelScript/notAnalyzed/$Today/instance-$i"
  let i=i+1
done
