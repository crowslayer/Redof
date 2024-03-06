# Redof
### Routine to download files from the DOF Yucatan, in bulk, directly or via scraping.

# Requirements.
- **request**
- **tqdm**
- **BeautifulSoup**

## Parameters

- **begin_date: Beginning date**
- **end_date: end date**
- **path: Directory path where the files will be downloaded.**


## How to use

```
C:\Proyectos\Python\Redof\venv\Scripts\python.exe C:\Proyectos\Python\Redof\dof.py 
c:/temp/masive/2024-02-29_1.pdf: 100%|██████████| 2.30M/2.30M [00:03<00:00, 756kB/s] 
c:/temp/masive/2024-02-29_2.pdf: 100%|██████████| 331k/331k [00:00<00:00, 397kB/s]
c:/temp/masive/2024-02-29_3.pdf: 100%|██████████| 159k/159k [00:00<00:00, 291kB/s]
c:/temp/masive/2024-02-29_4.pdf: 100%|██████████| 3.63M/3.63M [00:07<00:00, 488kB/s]
c:/temp/masive/2024-03-01_1.pdf: 100%|██████████| 1.11M/1.11M [00:02<00:00, 485kB/s]
```
# DOF Reader

# Requirements.
- **Pymupdf**
- **Pandas**
- **openpyxl**

### Routine to read the newspapers in pdf format and return the files found according to the search criteria. An excel file is generated with the results.

## How to use

```
Introduce la ruta donde se encuentran los DOF c:/temp/dof/2024/02
Introduce el numero de expediente a buscar: 314/2024 314/2021
Introduce la ruta de destino en caso de haber coincidencias: 
Introduce el nombre del archivo donde se almacenaran las coincidencias: 

```
### Example
```
Se encontraron 2 coincidencias en DOF No. 35,303  de fecha Mérida, Yuc., Martes 6 de Febrero de 2024
Se encontraron 1 coincidencias en DOF No. 35,307  de fecha Mérida, Yuc., Viernes 9 de Febrero de 2024
Se encontraron 1 coincidencias en DOF No. 35,312  de fecha Mérida, Yuc., Jueves 15 de Febrero de 2024
Se encontraron 1 coincidencias en DOF No. 35,318  de fecha Mérida, Yuc., Martes 20 de Febrero de 2024
Se encontraron 1 coincidencias en DOF No. 35,324  de fecha Mérida, Yuc., Martes 27 de Febrero de 2024
Se encontraron 1 coincidencias en DOF No. 35,327  de fecha Mérida, Yuc., Jueves 29 de Febrero de 2024
-----------------------------------------------

Consulta el archivo c:/temp/dof/2024/02/finding/resultado.xlsx para revisar los detalles

Process finished with exit code 200


```


Enjoy
@crowslayer
