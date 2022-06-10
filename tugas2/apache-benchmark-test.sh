#!/bin/sh

# $1 -> url
apache_benchmark()
{
	echo saving log to $2
	echo 10
	ab -n 10 -c 1 $1 | awk -f report_parser.awk > $2
	ab -n 10 -c 5 $1| awk -f report_parser.awk >> $2
	ab -n 10 -c 10 $1| awk -f report_parser.awk >> $2

	echo 50
	ab -n 50 -c 1 $1| awk -f report_parser.awk >> $2
	ab -n 50 -c 5 $1| awk -f report_parser.awk >> $2
	ab -n 50 -c 10 $1| awk -f report_parser.awk >> $2

	echo 100
	ab -n 100 -c 1 $1| awk -f report_parser.awk >> $2
	ab -n 100 -c 5 $1| awk -f report_parser.awk >> $2
	ab -n 100 -c 10 $1| awk -f report_parser.awk >> $2

	echo 500
	ab -n 500 -c 1 $1| awk -f report_parser.awk >> $2
	ab -n 500 -c 5 $1| awk -f report_parser.awk >> $2
	ab -n 500 -c 10 $1| awk -f report_parser.awk >> $2
}

#echo http://172.16.16.101:8889/
#apache_benchmark http://172.16.16.101:8889/ "./report_regular.csv"
 
#echo http://172.16.16.101:8889/rfc2616.pdf
#apache_benchmark http://172.16.16.101:8889/rfc2616.pdf "./report_pdf.csv"

#echo http://172.16.16.101:8889/testing.txt
#apache_benchmark http://172.16.16.101:8889/testing.txt "./report_txt.csv"

echo http://172.16.16.101:8889/pokijan.jpg
apache_benchmark http://172.16.16.101:8889/pokijan.jpg "./report_jpg.csv"
