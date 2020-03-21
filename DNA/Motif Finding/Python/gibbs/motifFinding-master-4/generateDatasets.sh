#python benchmark_code.py ICPC ML SL SC

rm -r dataset*

ICPC_def=2
ML_def=8
SL_def=500
SC_def=10

#for i in {1..10};
#do	
#	python benchmark_code.py $ICPC_def $ML_def $SL_def $SC_def
#	mv dataset dataset_${ICPC_def}_${ML_def}_${SL_def}_${SC_def}_${i}
#done

for icpc in {1,1.5};
do	
	for i in {1..10};
	do
		python generateData.py $icpc $ML_def $SL_def $SC_def
		mv dataset dataset_${icpc}_${ML_def}_${SL_def}_${SC_def}_${i}
	done
done

for ml in {6,7};
do	
	for i in {1..10};
	do
		python generateData.py $ICPC_def $ml $SL_def $SC_def
		mv dataset dataset_${ICPC_def}_${ml}_${SL_def}_${SC_def}_${i}
	done
done

for sc in {5,10,20};
do	
	for i in {1..10};
	do
		python generateData.py $ICPC_def $ML_def $SL_def $sc
		mv dataset dataset_${ICPC_def}_${ML_def}_${SL_def}_${sc}_${i}
	done
done
