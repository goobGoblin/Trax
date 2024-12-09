pip install -r fbRequirements.txt

echo "I would recommend setting a limit on how many items(Tracks) you want to migrate. You may run out of free usage."
echo "Please enter the number of items you would like to migrate(0 - for all): "
read limit

if python3 data_handling/scripts/migrateDB.py $limit || python data_handling/scripts/migrateDB.py $limit;
then python3 data_handling/scripts/fireBaseUpdateLinks.py || python data_handling/scripts/fireBaseUpdateLinks.py
else echo "Error: Could not migrate data."
fi