for i in 16 32 64 128 256 512
do
	echo "Dimension $i"
	for j in 60 61 62 63 64 65 66 67
	do
		python strassen.py $j $i sample.txt
	done
done