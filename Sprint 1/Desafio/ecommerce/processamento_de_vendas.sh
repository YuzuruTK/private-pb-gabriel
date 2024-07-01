#!/bin/bash

if ! [ -d ./vendas ]
then
mkdir vendas
echo "Pasta Vendas criada"
fi

cp dados_de_vendas.csv ./vendas/dados_de_vendas.csv

actual_date=$(date +"%Y%m%d")

if ! [ -d ./vendas/backup ]
then
mkdir vendas/backup
echo "Pasta Backup criada"
fi

cd vendas

cp ./dados_de_vendas.csv ./backup/dados-$actual_date.csv

cd backup

mv dados-$actual_date.csv backup-dados-$actual_date.csv

touch relatorio-$actual_date.txt

echo $(date +"%Y/%m/%d %H:%M") >> relatorio-$actual_date.txt

firstLine=$(head backup-dados-$actual_date.csv -n 2 | tail -n 1)
initialDate=$(echo ${firstLine} | cut -d ',' -f 5)

lastLine=$(tail backup-dados-$actual_date.csv -n 1)
lastDate=$(echo $lastLine | cut -d ',' -f 5)

lines_of_file=$(cat backup-dados-$actual_date.csv -n | tail -n 1 | cut -f 1)

lines_to_use=$(($lines_of_file - 1))

total_quant=0

tail backup-dados-$actual_date.csv -n $lines_to_use | while IFS=',' read -r id product quant price date;
do
total_quant=$(($total_quant + $quant))
echo $total_quant > sum.txt
done

total_quant=$(cat sum.txt)
rm sum.txt

different_items=$(tail backup-dados-$actual_date.csv -n $lines_to_use | cut -d ',' -f 2 | sort | uniq | wc -l )

echo "Data do primeiro registro: ${initialDate}" >> relatorio-$actual_date.txt
echo "Data do ultimo registro: ${lastDate}" >> relatorio-$actual_date.txt
echo "Quantidade Total de itens: ${total_quant}" >> relatorio-$actual_date.txt
echo "Quantidade Total de Registros: ${lines_to_use}" >> relatorio-$actual_date.txt
echo "Quantidade de Itens Diferentesl: ${different_items}" >> relatorio-$actual_date.txt
echo "Primeiros 10 registros: \n" >> relatorio-$actual_date.txt

(head backup-dados-$actual_date.csv -n 11 | tail -n 10) >> relatorio-$actual_date.txt

echo "Relatorio do dia ${actual_date} criado"

zip backup-dados-$actual_date.zip backup-dados-$actual_date.csv

rm ../dados_de_vendas.csv ./backup-dados-$actual_date.csv