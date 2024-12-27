import dns.resolver
import argparse

#Definimos el nombre de dominio
def main(target_domain):
    record_types = ["A", "AAAA", "CNAME", "NS", "MX", "SOA", "TXT"]

    #Creamos un DNS resolver
    resolver = dns.resolver.Resolver()

    for record_type in record_types:
        try:
            answers = resolver.resolve(target_domain, record_type)
        except dns.resolver.NoAnswer:
            continue
        
        #Mostramos la informacion de ese registro
        print(f"------{record_type} registros para {target_domain} --------")
        for data in answers:
            print(f"{data}")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta para visualizar los tipos de registros de recurso")
    parser.add_argument("-t","--target_domain", type=str, required=True, help="Introduzca el link target ejemplo = 'example.com'")
    
    args = parser.parse_args()
    
    main(target_domain=args.target_domain)