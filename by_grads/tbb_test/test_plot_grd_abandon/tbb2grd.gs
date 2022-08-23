'reinit'
'open H:/tbb_test/datasets/tbb.ctl'
'set fwrite H:/JMA-TBB-1981-1997/grd/1981.grd'
'set gxout fwrite'
i=1
while(i<=2920) 
'set t 'i''
'set x 1 120'
'set y 1 120'
'd tbb'
i=i+1 
endwhile
'disable fwrite'


