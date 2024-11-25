#this script is used to run the tests 
#for the database and the soundcloud scraper
#Please note if there is a difference because of the datetime, 
#this should be ignored, as there is a slight variance between host machines
#datetime and the servers datetime 

python3 ../data_handling/scripts/soundcloud/scraper.py $1
python3 dataBaseTests.py
make