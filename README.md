# Redof
### Routine to download files from the DOF Yucatan, in bulk, directly or via scraping.

# Requirements.
- **request**
- **BeautifulSoup**

## Parameters

- **begin_date: Beginning date**
- **end_date: end date**
- **path: Directory path where the files will be downloaded.**


## How to use
Enter the date range for the logs to be retrieved, and the download path.
Upon completion, a window will appear with the number of files downloaded.


![Pantalla principal](assets/descarga_dof.png)

# DOF Reader
### Routine for searching for information or files in the official journal publications.

# Requirements.
- **Pymupdf**
- **Pandas**
- **openpyxl**

## How to use
To search, you must provide the path to the official gazette files in PDF format.

The program will display the results.

![Pantalla principal](assets/reader.png)

You have the option to export search results to an Excel file.
Simply right-click on the search and select the appropriate option.

![Pantalla principal](assets/reader_export.png)

![Pantalla principal](assets/reader_export2.png)

### Export to Excel
![Pantalla principal](assets/export_xls.png)

Enjoy
@crowslayer
