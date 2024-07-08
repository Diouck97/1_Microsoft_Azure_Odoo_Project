Goal : The goal of this project was to retrieve data from Odoo CRM and then analyze the data with Power BI. Power BI does not have a connector for Odoo so in order to retrieve
the data a python script is necessary. 

When using a python script in Power BI a personnal Gateway is necessary to retrieve the data everyday. Another solution is to host the python script in the cloud 
and run it daily. This is the solution selected in this case. A Microsoft Azure Function App has been created to run the script with as TimerTrigger to run the script
everyday at 7 am. 

The data is then stored using Microsoft Azure Blob Storage container. Power BI has a Microsoft Blob Storage connector so we can easily configure a scheduled refresh of 
the dataset daily.

In this repository you will find the "_init_.py" file that has been used to connect to the Odoo CRM and get data from the database. Once we get the data we use a key
to connect to Azure and store the data to Azure Storage. The TimerTrigger is configured in the "functions.json" file.

