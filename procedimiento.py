notaInicial='''
        Procedimiento del programa:\n
        1-Se debe seleccionar el operador
        2-Se debe rellenar con el lugar del escaneo
          -Una vez realizado 1 y 2 se podrán cargar los archivos
        3-cargar los archivos con denominación "landmarkNombreNumero.xyz"
          -Cada archivo "landmarkNombreNumero.xyz" tiene asociado un archivo 
          de escaneo del tipo "NombreNumero.xyz" con los datos del escaneo
          -En caso de que falta el archivo "NombreNumero.xyz" el programa salteará el archivo
          y se informará el faltante.
        4-Presionar el boton "Analizar y extraer medidas" para obtener las medidas
          -En caso de encontrarse un error dentro de los datos se informará el error
          correspondiente. De cualquier manera se informará el error en un registro.
          En ocasiones el error podría llegar a arreglarse con mediciones "insitu".
        5-Para poder acceder a al información abrir el archivo dfMedicion.csv
          -En caso de cargar 2 veces el mismo "landmarkNombreNumero.xyz el programa
           mostrará en el archivo csv el TAG con un ".duplicado" al final.'''