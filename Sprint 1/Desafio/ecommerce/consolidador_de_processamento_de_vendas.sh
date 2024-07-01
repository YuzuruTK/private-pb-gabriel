#!/bin/bash

cd vendas/backup/

filenames=`ls ./*.txt`

touch relatorio_final.txt

for eachfile in $filenames
do

chmod 664 $eachfile

echo $(cat $eachfile) >> relatorio_final.txt
echo "" >> relatorio_final.txt
done
