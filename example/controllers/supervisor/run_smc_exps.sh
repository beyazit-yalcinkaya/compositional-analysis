
for i in {1..10}
do
    echo "Iteration ${i}"
    mkdir smc_csvs
    python3.9 analyze.py smc compositional
    python3.9 analyze.py smc monolithic
    mv smc_csvs smc_csvs_${i}
done
