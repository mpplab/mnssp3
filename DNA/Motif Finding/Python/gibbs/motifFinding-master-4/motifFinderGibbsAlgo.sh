ls -d */ > listDatasets

while read line;
do
	folder=$line
	echo $folder
	cp gibbs.py $folder
	cd $folder
	## Run the gibbs.py in the folder, 10 time
	outputfolder=gibbs_output
	mkdir $outputfolder
	for i in 0{1..9} {10..10};
	do
		python gibbs.py
		mv predictedmotif.txt $outputfolder/gibbs_${i}_predictedmotif.txt
		mv predictedsites.txt $outputfolder/gibbs_${i}_predictedsites.txt
		mv IC.npy $outputfolder/gibbs_${i}_IC.npy
	done
	cd ..
done < listDatasets
