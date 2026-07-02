Algoritmus pracuje pozpátku a hledá všechny historické předky pro zadanou skupinu infikovaných uzlů `{D, E, F}`. Když se podíváme na schéma naší sítě, zjistíme, že:
* **Z počítače `B`** vedou orientované cesty do všech nakažených míst (přímo na `D` a `E`, a přes uzel `E` se nákaza dostane i na `F`). Takže `B` mohl celou infekci spustit sám.
* **Uzel `A`** je na tom dost podobně. Vidí na `D` i `E` přes uzel `B`, a na stroj `F` se dokáže dostat dvěma cestami (buď přes `C -> F`, nebo přes `B -> E -> F`).

Protože oba uzly splňují podmínku, že z nich nákaza mohla doputovat do úplně každého infikovaného počítače, závěrečný průnik množin nám musel vrátit oba dva. V praxi je to obrovská pomoc, protože se analytikům zúžil okruh podezřelých na infekční řetězec `A -> B`. Abychom pak mezi nimi stoprocentně určili jednoho vítěze, museli bychom se podívat ještě na časová razítka (timestamps) v logu a zjistit, u kterého stroje začala ta aktivita dřív.

### Popis a fungování kódu

Samotný program v Pythonu jsme rozdělili do tří logických kroků:

1. **Reprezentace sítě:** Topologie je zapsaná pomocí klasického slovníku (`dict`), kde klíče jsou jednotlivé počítače a hodnoty v seznamech představují orientované hrany – síťové logy o tom, kam odcházela komunikace.
2. **Reverze grafu:** Nejdůležitější věc v rámci celého programu. Vytvořili jsme prázdnou strukturu `obraceny_graf` a pomocí dvou cyklů `for` byly prohozeny směry všech hran. Pokud v logu bylo, že počítač `A` kontaktoval `B`, v novém grafu vede cesta z `B` do `A`. Díky tomu můžeme historii sítě prohledávat pozpátku proti směru původního toku dat.
3. **Retrospektivní BFS a průnik:** Program vezme seznam nakažených uzlů a pro každý z nich spustí samostatné hledání. Používáme k tomu frontu `deque`, která je optimalizovaná na rychlost a pro tento úkol nezbytný. Algoritmus z vybraného uzlu skáče po otočených hranách do minulosti a všechny nalezené počítače ukládá do množiny `predci_uzlu`. Nakonec k nim přidá i startovní uzel sám o sobě, protože musíme počítat s variantou, že nákaza vznikla přímo na něm (třeba z infikované flashky).

Na úplném konci program provede funkci `set.intersection`, což je průnik všech nalezených množin. Pacientem Nula totiž může být pouze ten počítač, který se objevil v historii úplně všech nakažených stanic. S využitím fronty má celé tohle hledání optimální časovou složitost $O(|V| + |E|)$, takže by skript bleskově prohledal i obrovskou infrastrukturu.



**autoři**: Tomáš Rataj a Pavel Hovjadský
