
for i in {1..10}
do
   echo "Iteration ${i}"
   mkdir falsify_csvs
   python3.9 analyze.py falsify compositional 0.05 0.1 0.05
   python3.9 analyze.py falsify monolithic 0.05 0.1 0.05
   mv falsify_csvs falsify_csvs_${i}
done
