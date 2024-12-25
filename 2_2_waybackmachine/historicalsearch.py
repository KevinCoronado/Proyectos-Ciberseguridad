from waybackpy import WaybackMachineCDXServerAPI
from datetime import datetime, timedelta
import requests
import argparse

class HistoricalSearch:
    #Inicializamos la clase con el metodo constructor que inicia el url y el user agent
    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent

    #El metodo search snapshot que realiza la busqueda basica en el sitio
    def search_snapshot(self, years_ago=10, download_filename=None):
        """Buscar y opcionalmente guardar una captura de una fecha específica"""
        target_date = datetime.now() - timedelta(days=365 * years_ago)
        year, month, day = target_date.year, target_date.month, target_date.day

        cdx_api = WaybackMachineCDXServerAPI(self.url, self.user_agent)
        snapshot = cdx_api.near(year=year, month=month, day=day)

        if snapshot:
            print(f"Fecha: {snapshot.timestamp}, URL: {snapshot.archive_url}")
            if download_filename:
                self.download_snapshot(snapshot.archive_url, download_filename)
        else:
            print("No se encontró ninguna captura con la fecha especificada")

    def download_snapshot(self, archive_url, filename):
        """Descargar el HTML de la página"""
        response = requests.get(archive_url)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf8') as file:
                file.write(response.text)
            print(f"Documento guardado exitosamente en {filename}")
        else:
            print(f"Error al descargar la página: {response.status_code}")

    def search_snapshot_by_extensions(self, years_ago=4, days_interval=30, extensions=None):
        """Buscar capturas de archivos con extensiones específicas"""
        if extensions is None:
            extensions = ["pdf", "doc", "docx", "ppt", "xls", "xlsx", "txt"]

        today = datetime.now()
        start_period = (today - timedelta(days=365 * years_ago)).strftime('%Y%m%d')
        end_period = (today - timedelta(days=(365 * years_ago) - days_interval)).strftime('%Y%m%d')

        cdx_api = WaybackMachineCDXServerAPI(self.url, self.user_agent, start_timestamp=start_period, end_timestamp=end_period)
        snapshots = cdx_api.snapshots()

        for snapshot in snapshots:
            if any(snapshot.archive_url.endswith(ext) for ext in extensions):
                print(f"Fecha: {snapshot.timestamp}, URL: {snapshot.archive_url}")

def main(url, user_agent, args):
    searcher = HistoricalSearch(url, user_agent)

    #Si la busqueda es por extension se separa de la normal
    if args.historicalsearchbyextension:
        extensions = args.historicalsearchbyextension.split(',')
        searcher.search_snapshot_by_extensions(
            years_ago=int(args.years_ago or 4),
            days_interval=int(args.days_interval or 30),
            extensions=extensions
        )
    else:
        searcher.search_snapshot(
            years_ago=int(args.years_ago or 10),
            download_filename=args.download
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta para hacer búsqueda OSINT mediante Wayback Machine")
    parser.add_argument("-u", "--url", type=str, required=True, help="Especifica la URL")
    parser.add_argument("-dw", "--download", type=str, help="Descarga la snapshot y guarda con el nombre especificado")
    parser.add_argument("-hsbe", "--historicalsearchbyextension", type=str, help="Realiza una búsqueda por extensión, por ejemplo: txt,pdf,doc")
    parser.add_argument("-ya", "--years_ago", type=int, help="Años atrás (predeterminado: 10 años)")
    parser.add_argument("-d", "--days_interval", type=int, help="Días de intervalo (predeterminado: 30 días)")

    args = parser.parse_args()
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    main(url=args.url, 
         user_agent=user_agent, 
         args=args)
