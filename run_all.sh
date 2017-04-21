echo "Computing stats for baseline"
bash ./baseline/run.sh

echo "Computing stats for method_1"
cd ./method_1
bash ./run.sh
cd ..

echo "Computing stats for method_2"
cd ./method_2
bash ./run.sh
cd ..

echo "Computing stats for method_3"
cd ./method_3
bash ./run.sh
cd ..

echo "Computing stats for method_4"
cd ./method_4
bash ./run.sh
cd ..
