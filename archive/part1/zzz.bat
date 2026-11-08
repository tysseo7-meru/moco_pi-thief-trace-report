@echo off

rem ls out_2312/G* | wc -l
rem ls out_2401/G* | wc -l
rem ls out_2402/G* | wc -l
rem ls out_2403/G* | wc -l


rem python v3.06.py  -sa GA24VWX6H2PTW6VQOCFR3K23IGP224H5A4MUCDRE4QXH5JWWOVKUPWHA
rem python v3.06.py  -sa GA67YLGF4GKPGZGKXWRLG72F7OITFXB2CNQGSVS2VVPLRWPCNKUJ6NSM
rem python v3.06.py  -o out_2310 -d 2023/10/01
rem python v3.06.py  -o out_2311 -d 2023/11/01
rem python v3.06.py  -o out_2312 -d 2023/12/01
rem python v3.06.py  -o out_2401 -d 2024/01/01
rem python v3.06.py  -o out_2402 -d 2024/02/01
rem python v3.06.py  -o out_2403 -d 2024/03/01

rem python v3.06.py  -o out_2310.d -sp 259200
rem python v3.06.py  -o out_2311.d -sp 259200
rem python v3.06.py  -o out_2312.d -sp 259200
rem python v3.06.py  -o out_2401.d -sp 259200
rem python v3.06.py  -o out_2402.d -sp 259200
rem python v3.06.py  -o out_2403.d -sp 259200

rem python v3.06.py  -o out_2310.d -plot
rem python v3.06.py  -o out_2311.d -plot
rem python v3.06.py  -o out_2312.d -plot
rem python v3.06.py  -o out_2401.d -plot
rem python v3.06.py  -o out_2402.d -plot
rem python v3.06.py  -o out_2403.d -plot

rem python v3.06.py  -o out_2310.d.sp.3.0day -plot
rem python v3.06.py  -o out_2311.d.sp.3.0day -plot
rem python v3.06.py  -o out_2312.d.sp.3.0day -plot
rem python v3.06.py  -o out_2401.d.sp.3.0day -plot
rem python v3.06.py  -o out_2402.d.sp.3.0day -plot
rem python v3.06.py  -o out_2403.d.sp.3.0day -plot


rem python v3_11.py  -o out_test -d 2024/03/01
rem python v3_11.py  -o out_test.d -sp 259200
python v3_11.py  -o out_test.d.sp.3.0day -plot

rem v3.05.py  -sa GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL
rem v3.05.py  -sa GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW