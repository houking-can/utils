if [ $# -eq 0 ];then
	echo "usage: bert_service.sh run device_id\n       bert_service.sh stop"
	exit
fi


if [ "$1" = "stop" ];then
	echo "stop bert service..."
	pids=$(ps -aux | grep bert_service | grep -v "grep" | awk '{print $2}')
	for pid in $pids
	do
		echo "kill process $pid"
		pstree $pid -p| awk -F"[()]" '{print $2}'| xargs kill -9
	done
	exit
fi

if [ "$1" = "run" ];then

	tmp="/home/yhj/bert_service/tmp"
	if [ ! -d $tmp ]; then
	  mkdir $tmp
	else
		rm -rf $tmp
		mkdir $tmp
	fi
	cd $tmp
	if [ $# -ne 2 ];then
		echo "miss device id."
		exit
	fi
	nohup /home/yhj/anaconda3/envs/tensorflow/bin/bert-serving-start -model_dir "/home/yhj/bert_service/bert_ckpt" -num_worker=6 -device_map $2 -graph_tmp_dir $tmp >> log &
fi