@echo off



rem python piTracePayments.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU > o.csv

rem python piTracePayments.py GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF > o2.csv

rem python f.py

rem python t.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU > t.csv


rem python t.py GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF > t2.csv

rem python t.py GALIT7MEVQ5RTSFJKXLBO2NV3IQ2TVL4KTYFZEFGXTTWA3PGO6SKH7SG > t3.csv

rem python searchPath.py





rem python searchPath.py

rem python exPath.py

rem python countSpamScore.py > countSpamScore_to.csv
rem python countSpamScore.py > countSpamScore_from.csv
rem python countSpamScore.py > countSpamScore_gafyto.csv


rem python piTracePayments.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU -from >from.csv


rem python piTracePayments.py  GB6EJFHQFGGUZ27LYXKOUE3OBLI6WOBUORADGU6WLTMZKBITVS2UUU73 -to > GB6E-to.csv

rem python piTracePayments.py  GB6EJFHQFGGUZ27LYXKOUE3OBLI6WOBUORADGU6WLTMZKBITVS2UUU73 -from > GB6E-from.csv


rem  python piTracePayments.py GCTDVU23QTRGEEK2ZM4NHLKLUKXNZEAAKWA5Y5CM2LFQVMBJZXWQNHC -to > GCTD-to-reddit.csv

rem  python piTracePayments.py GB6EJFHQFGGUZ27LYXKOUE3OBLI6WOBUORADGU6WLTMZKBITVS2UUU73 -from > GB6EJ-from.csv

rem python piTracePayments.py GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF -from > GDGV-from.csv

rem piTracePayments_ATH30_0409.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU -to > to_ATH30_0409.csv

rem python piTracePayments.py GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF -to > GDGV-to.csv

rem python piTracePayments_ATH30_0409.py GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF -to > GDGV-to_ATH30_0409.csv

rem python bat.py > bat.csv




rem python piTracePayments.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU -to >to_0421.csv


rem python searchPath.py
rem python a.py
rem python exPath.py



rem python piTracePayments.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU  -ath 1000 -from >  from_0430.csv

rem python piTracePayments.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU  -ath 1000 -to >  to_0501.csv
rem python countSpamScore.py > countSpamScore_to0501.csv

rem python piTraceLockPeriod.py > piTraceLockPeriod.csv
rem python piTraceLockPeriod.py > piTraceLockPeriod.csv

rem python piTracePayments.py GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU  -ath 1000 -to
rem python countSpamScore.py > countSpamScore-GC3Z.csv

rem countSpamScoreV02.py > countSpamScoreV02-GAJ4.csv






rem python piTracePayments.py GAFYXHBXYNDLKLZXBZSR6MLCNA4QJ4CPT3NDPV56AU5BIGGZ7CJOWRZ5 -to -ath 1000 >@gafy-to-ath1000.csv
rem python piTracePayments.py GAFYXHBXYNDLKLZXBZSR6MLCNA4QJ4CPT3NDPV56AU5BIGGZ7CJOWRZ5 -to -ath 200 >@gafy-to-ath200.csv


rem python mkBlkAdr.py gcp-to_0516_ath490.csv

rem python test.py > res_prStolenAdrsInfo.csv

rem python v3.04.py  -o out_2310.d -plot

rem sed -e "s/'//g" -e "s/: /,/g" -e "s/{//g" -e "s/}//g" a.csv > b.csv

rem python v3.05.py  -o out_2401 -d 2024/01/01

rem python v3.05.py  -o out_2402 -d 2024/02/01
rem python v3.05.py  -o out_2402.d -plot

rem python v3.05.py  -o out_2402 -d 2024/02/01
rem python v3.05.py  -o out_2402.d -sp 259200
rem python v3.05.py  -o out_2402.d.sp.3.0day -plot


rem python v3.05.py  -omig migList1.txt -blk 13564200 -stop 2024/03/11




grep -f  from_GING.txt bk305_out/out_2310/G*
grep -f  from_GING.txt bk305_out/out_2311/G*
grep -f  from_GING.txt bk305_out/out_2312/G*
grep -f  from_GING.txt bk305_out/out_2401/G*
grep -f  from_GING.txt bk305_out/out_2402/G*
grep -f  from_GING.txt bk305_out/out_2403/G*


