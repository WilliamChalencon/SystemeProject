echo "Enter your directory containing the vcf files ?"
read route
echo "Processing..."
mkdir ./result
python3 parcourir.py $route


