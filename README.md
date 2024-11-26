Toto je repozitář s kódem pro ESP32-S uvnitř hodin v učebně 222

Konstrukce se skládá z 110 krabiček, 110 difuzorů, 110 víček s písmenkem 4 límců a jedné krabičky na ESP, což vše bylo vytištěno na 3D tiskárně.
Poté je v konstrukci dohromady přes 200 ledek a jedno tlačítko.
Ve finální verzi hodiny mají ješte odpočet, ale protože jsou na místě, kde na tlačítko nejde došáhnout, tak je tato funkce vypnutá.

Inspirace:
![210136_nastenne-hodiny-qlocktwo-earth-45-black-pepper-white](https://github.com/user-attachments/assets/98c2e873-6666-45c1-977e-5ef554eaf76a)

Tento projekt mi byl zadán Panem učitelem Jelínkem v druhé polovině školního roku 2023/2024. Měl jsem se na něm naučit programovat.
Měl to být jednoduchý projekt dokonce roku, nakonec se z toho stalo něco většího do čeho jsem utopil vyšší desítky hodin a dokončil jsem ho až v listopadu školního roku 2024/2025.

Projekt začal naprogramováním jednoduchého prototypu, co vypisoval do konzole. Poté jsem předělal program aby fungoval jako TRUE a FALSE listy (true-rozsvícená ledka, false-vypnutá). Toto platí pro vypisování hlavních časů. 
Protože jsou hodiny po pěti minutách, tak v rozích jsou modré ledky. Které ukazují kolik je minut navíc (což je i v inspiraci). Do našeho designu jsme ale přidali i sekundy. Každá jedna další rozsvícená ledka v rámu je sekunda, která uběhla.
Celý tento kód jsem měl udělaný rychle, zabral mi nějaké 2 týdny od prvního prototypu po finální produkt (6-8 hodin čisté práce).

Nejnáročnější bylo udělat modely, vytisknout a vše slepit dohromady. 3D modely jsem dělal s Panem Jelínkem, vše jsme se snažili tisknout na, co největší průměr otvoru tiskové hlavice, aby tisk byl co nejdříve.  

3D Modelování a tisknutí prototypů - 14-16 hodin čisté práce
Tisk - přes 100 hodin (práce tiskárny)
Kompletace - 4 hodiny

Po vyrobení kostry jsem musel nahrát program do mikročipu a spájet všechny kabely a nalepit ledky (100 + 10 + 130).

ESP32-S:
![obrazek](https://github.com/user-attachments/assets/0bf003e8-25d6-4cf0-9866-38a38a8d16c2)

Měl jsem k dispozici řetěz o 100 ledkách a potom proužek s 10 metry.
Pro písmenka jsem použil těch 100 ledek a půjčil jsem si 10 jednotlivých ledek z proužku.
Do rámu jsem dal jenom proužek.

Tuto fázi jsem dělal 2 krát kvůli kompikacím s ledproužkem (myšlenka byla je dopájet v rozích proužku kabílky, ale ledka se stále trhala, takže jsme to museli celé strhnout a dát tam celý pásek v celku, který je jenom zohýbaný, a pouze jsme si udělali slovník, kde jsou napsané správné indexy ledek, slovník můžete najít v kódu pod názvem demon)
Také se rozsvěcuje jen lichá ledka, protože ty sudé jsou jako ambientní osvětlení, které je ale vypnuté.

Lepení - 5 hodin
Komplikace - 20 hodin 

Poté stačilo jen vše spájet. 

Pájení - 15 hodin 

Po spájení se vše jen muselo zfinalizovat a doladit.

Zde je schéma:
![obrazek](https://github.com/user-attachments/assets/1a2e7f90-493a-4326-8ef4-6244d18e9c00)

Finalizace - 5 hodin

Celkové materiály, co jsem použil:

Přes 1,5 KG Prusa PLA Galaxy Black filamentu - 1000 Kč,-
300 g Prusa PLA bílého filamentu - 250 Kč,-
4 m Programovatelného RGB pásku - 800 Kč,-
Celý 100 ledkový GRB vánoční řetěz - 250 Kč,- 
ESP32-S - 150 Kč,-
Tlačítko z Kail Box White Switche - 25 Kč,-
Dále přes 3 m ethernetového kabelu na dělání vodičů - 70 Kč,-
0,6 m elektirckého kabelu na větší vodiče - 10 Kč,-

Mikropájka, tavná pistole
Celková cena byla přibližně 2555 Kč,-

Kdybych tento projekt dělal teď tak si rozhodně udělám lépe kostru aby to do sebe lépe zapadalo a nemusel jsem tolik lepit. Dále bych si vybral nějaký jiný druh kabeláže než pájení. 

Výsledek mojí práce je teď v učebně 222

Výsledek:
![obrazek](https://github.com/user-attachments/assets/e77b8391-7378-4c6a-9adc-8286b84a32a7)

Pro zájemce můžu individuálně poslat všechny 3D modely, nebo zodpovědět na jakýkoliv dotaz okolo mého projektu, máte k dispozici zdrojový kód, kde je vše popsané.
Pro kontakt: eduard.wojnar@student.gmh.cz, nebo se mě zeptejte na chodbě školy

Rád bych poděkoval Panu učiteli Jelínkovi a Vodvářkovi za podporu a vedení.
Speciálně bych chtěl poděkovat Honzovi Studničnému za pomoc při pájení.
