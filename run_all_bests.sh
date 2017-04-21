echo "Computing best stats for baseline"
bash ./baseline/run.sh

echo "Computing best stats for method_1"
cd ./method_1
bash ./run_best.sh
cd ..

echo "Computing best stats for method_2"
cd ./method_2
bash ./run_best.sh
cd ..

echo "Computing best stats for method_3"
cd ./method_3
bash ./run_best.sh
cd ..

echo "Computing best stats for method_4"
cd ./method_4
bash ./run_best.sh
cd ..
