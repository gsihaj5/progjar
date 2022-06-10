BEGIN {
	failed_request=-1
	complete_requests=-1
	time_request=-1
	transfer_rate=-1
	connect_time=-1
	processing_time=-1
	waiting_time=-1
}

{
	if($1 == "Complete")
		complete_requests=$3

	if($1 == "Total" && $2 == "of")
		complete_requests=$3

	if($4 == "patient)...Total")
		complete_requests=$6

	if($1 == "Failed" && $2 == "requests:")
		failed_request=$3

	if($1 == "Time" && $2 == "per" && time_request == -1)
		time_request=$4

	if($1 == "Transfer" )
		transfer_rate=$3

	if($1 == "Connect:" )
		connect_time=$3

	if($1 == "Processing:")
		processing_time=$3

	if($1 == "Waiting:")
		waiting_time=$3
}

END {
	print complete_requests ","  \
			failed_request "," \
			time_request "," \
			transfer_rate "," \
			connect_time "," \
			processing_time "," \
			waiting_time
}
