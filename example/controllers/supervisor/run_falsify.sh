
for i in {1..10}
do
   python3.9 analyze.py falsify 2 1.0
   mv falsify_csvs falsify_csvs_${i}
done
