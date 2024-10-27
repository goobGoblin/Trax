from git import Repo
import os

# Navigate to the script's directory
script_dir = os.path.dirname(__file__)  # Gets the directory where the script is located

# Construct the path to the repository root
# Assumes the script is run from within the 'Report' directory and the repo root is one level up
repo_path = os.path.abspath(os.path.join(script_dir, os.pardir))
# Path to your repository
repo = Repo(repo_path)

commits = list(repo.iter_commits('main', max_count=100))  # Adjust branch and count as needed

# Prepare the LaTeX table code
latex_table = "\\begin{tabular}{|c|c|c|}\n\\hline\n"
latex_table += "Author & Date & Message \\\\\n\\hline\n"

# Loop through each commit to extract details
for commit in commits:
    message = commit.message.strip().replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
    # Skip commits whose message starts with 'merge' (case-insensitive)
    if message.lower().startswith('merge'):
        continue
    # Replace 'goobGoblin' with 'Zai Erb' in the author's name
    author = commit.author.name.replace('goobGoblin', 'Zai Erb')
    # Add each filtered and cleaned commit's details to the table
    latex_table += f"{author} & {commit.authored_datetime.strftime('%Y-%m-%d')} & {message} \\\\\n"

latex_table += "\\hline\n\\end{tabular}"

# Write the LaTeX table to a file
with open('commits.tex', 'w') as file:
    file.write(latex_table)