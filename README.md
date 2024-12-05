# Instruction✨  
1. Download given data base
2. The folder must follow following files structure :
   - .vscode  
   - 2018  
   - 2019  
   - 2020  
   - 2021  
   - 2022
   - 2023
   - Classify
       - Preprocess.py (Extract and Preapre data for classifying)
   - Extracting_part
       - Author_country_city
           - Unique_country_city
               - Unique_country_city.py (Extract unique countries and cities list for over 6 year(2018-2023))
           - Extract_country_city (Extract countries and cities list of each year)
       - Author_organization
           - Unique_organization
               - Unique_org.py (Extract unique organizations list for over 6 year(2018-2023))
           - Extract_organization.py (Extract organizations list of each year)
   - .gitignore
   - DBStructure_Overview.txt  
3. Create and activate .venv  
4. Run all .py (Run Extract_... before Unique_...)  
