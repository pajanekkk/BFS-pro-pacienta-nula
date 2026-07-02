from collections import deque

# 1. Tvorba sítě z logů
# Hrany jsou orientované a představují zaznamenanou síťovou komunikaci (odkud -> kam)
# Například: Počítač 'A' se chtěl spojit na 'B' a 'C'.
sitove_logy = {
    'A': ['B', 'C'],       
    'B': ['D', 'E'],  
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def najdi_pacienta_nula(graf, infikovane_uzly):
    print("--- SPUŠTĚNÍ RETROSPEKTIVNÍ ANALÝZY (BFS) ---")
    
    # Vytvoří se obrácený graf (reverzní hrany)
    # Potřebuje se jít proti směru původní komunikace, aby se našel zdroj.
    obraceny_graf = {uzel: [] for uzel in graf}
    for uzel, sousedi in graf.items():
        for soused in sousedi:
            obraceny_graf[soused].append(uzel)
            
    vsechny_mnoziny_predku = []
    
    # Pro každý detekovaný infikovaný uzel se spustí BFS pozpátku
    for start_uzel in infikovane_uzly:
        predci_uzlu = set()
        fronta = deque([start_uzel])
        navstivene = {start_uzel}
        
        while fronta:
            aktualni = fronta.popleft()
            
            # Procházení sousedů v obráceném grafu
            for rodic in obraceny_graf[aktualni]:
                if rodic not in navstivene:
                    navstivene.add(rodic)
                    predci_uzlu.add(rodic)
                    fronta.append(rodic)
        
        # Každý uzel mohl nákazu spustit i sám u sebe (přidání do potenciálních zdrojů)
        predci_uzlu.add(start_uzel)
        vsechny_mnoziny_predku.append(predci_uzlu)
        print(f" -> Možní původci nákazy pro stroj '{start_uzel}': {predci_uzlu}")
        
    # Pacient nula musí být společným předkem VŠECH infikovaných uzlů.
    # Udělá se průnik všech nalezených množin předků.
    potencialni_pacienti_nula = set.intersection(*vsechny_mnoziny_predku)
    
    return potencialni_pacienti_nula

# --- SCÉNÁŘ ---
# Bezpečnostní systém detekoval ransomware na těchto třech stanicích:
detekovana_infekce = ['D', 'E', 'F']

print("--- DETEKCE INCIDENTU ---")
print(f"Systém hlásí aktivní ransomware na počítačích: {detekovana_infekce}\n")

# Spuštění algoritmu z příkladu 5.1 v rešerši
vysledek = najdi_pacienta_nula(sitove_logy, detekovana_infekce)

print("\n--- VÝSLEDEK ANALÝZY TOPOLOGIE ---")
if vysledek:
    print(f"Identifikován Pacient Nula (společný kořen grafu): {vysledek}")
    print("Doporučení: Okamžitě odříznout tento uzel od sítě a zkontrolovat logy přihlášení.")
else:
    print("Chyba: Společný původce nebyl nalezen.")