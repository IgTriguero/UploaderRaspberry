# Instalar UnRaR ultima version: http://ftp.es.debian.org/debian/pool/non-free/u/unrar-nonfree/unrar_5.3.2-1+deb9u1_armhf.deb
import os

class bcolors:
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'

def descomprimir(desde, nombre):
   """
   Descomprime el archivo dentro de la carpeta <desde><nombre>

   Parametros: \n
   desde -- directorio hasta la raiz de peliculas descargadas: /home/pi/HDD1/finalizados/ \n
   nombre -- nombre de la carpeta
   """
   for indice in paraSubir:
      descomprimido = nombre + "VersionDescomprimida" #peliculaVersionDescomprimida

      for file in os.listdir(f'{desde}{nombre}'):
         print(file)
         if file.endswith(".rar"):
            resultado = os.path.join(f'{desde}{nombre}', file)
            print(f'sudo mkdir "{desde}{nombre}/{descomprimido}"')
            os.system(f'sudo mkdir "{desde}{nombre}/{descomprimido}"')
            print(f'sudo unrar x "{resultado}" "{desde}{nombre}/{descomprimido}"')
            os.system(f'sudo unrar x "{resultado}" "{desde}{nombre}/{descomprimido}"')
            for archivo in os.listdir(f'{desde}{nombre}'):
               if archivo.endswith(".srt") or archivo.endswith(".jpgs") or archivo.endswith(".png"):
                  resultadoFinal = os.path.join(f'{desde}{nombre}', archivo)
                  os.system(f'sudo cp -v "{resultadoFinal}" "{desde}{nombre}/{descomprimido}"')
            break
               
   
def detectCompressed(directorio):
   """
   Detecta si en el <directorio> hay una archivo comprimido en .rar
   
   Parametros:\n
   directorio -- El directorio donde busca si hay un archivo .rar

   Return:\n
   booleano -- True si lo hay, False si no lo hay
   """
   if os.path.isdir(directorio):
      for file in os.listdir(directorio):
         if file.endswith(".rar"):
            respBol = input(f"{bcolors.BOLD}{bcolors.WARNING}Se ha detectado un archivo comprimido. {bcolors.OKGREEN}¿Quieres descomprimirlo?{bcolors.ENDC} (Y/n) ")
            if respBol.lower() == "y" or respBol.lower() == "":
               return True
            else:
               break
   return False
   
direcciones = {
   "4k": "Drive:Multimedia/Peliculas/4k/",
   "1080": "Drive:Multimedia/Peliculas/1080/",
   "Series": "Drive:Multimedia/Series/"
} #Aqui cambias a donde quieres copiar tus torrents
desde = "/home/pi/HDD1/finalizados/" #Aqui cambias a donde se guardan tus torrents

directorios = []

i = 0
for file in os.listdir(desde):
   directorios.append({
      'index': i,
      'name': file
   })
   i += 1

respuesta = ' '
paraSubir = []
while respuesta.lower() != "":
   for directorio in directorios:
      if not(int(directorio["index"]) in paraSubir):
         print(f'{bcolors.BOLD}{bcolors.HEADER if directorio["index"] % 2 == 0 else bcolors.WARNING}{directorio["index"]}/{bcolors.ENDC}\t{directorio["name"]}')
   respuesta = input(f"{bcolors.BOLD}{bcolors.OKGREEN}¿Que quieres subir?{bcolors.ENDC} (ENTER para continuar): ")
   if(respuesta.lower() != ""):
      paraSubir.append(int(respuesta))
      
   print()

comandos = []
print(f"{bcolors.BOLD}{bcolors.HEADER}Vas a subir las siguientes carpetas:{bcolors.ENDC}")
for indice in paraSubir:
   print(f'{directorios[indice]["name"]}')
   if detectCompressed(f'{desde}{directorios[indice]["name"]}'):
      pathParaSubir = direcciones[input(f"{bcolors.BOLD}{bcolors.OKGREEN}¿A donde quieres subirlo?: {bcolors.ENDC}")]
      comando = f'sudo rclone copyto "{desde}{directorios[indice]["name"]}" "{pathParaSubir}{directorios[indice]["name"]}" ' 
      appends = '-P --drive-chunk-size=256M --fast-list --transfers 1' if pathParaSubir != direcciones['Series'] else '-P --fast-list'
      comandos.append(
         {
            'comprimido': True,
            'desde': f'{desde}',
            'nombre': f'{directorios[indice]["name"]}',
            'comando': comando + appends
         }
      )
   else:
      pathParaSubir = direcciones[input(f"{bcolors.BOLD}{bcolors.OKGREEN}¿A donde quieres subirlo?: {bcolors.ENDC}")]
      comando = f'sudo rclone copyto "{desde}{directorios[indice]["name"]}" "{pathParaSubir}{directorios[indice]["name"]}" ' 
      appends = '-P --drive-chunk-size=256M --fast-list --transfers 1' if pathParaSubir != direcciones['Series'] else ' -P --fast-list'
      comandos.append(
         {
            'comprimido': False,
            'comando': comando + appends
         }
      )
   print()

if(input(f"{bcolors.BOLD}{bcolors.OKGREEN}ENTER{bcolors.ENDC} para subir los archivos, escribe {bcolors.BOLD}{bcolors.FAIL}cancel{bcolors.ENDC} para cancelar").lower() != "cancel"):
   for comando in comandos:
      print(comando['comando'])
      if(comando['comprimido']):
         descomprimir(comando['desde'], comando['nombre'])
      os.system(comando['comando'])
