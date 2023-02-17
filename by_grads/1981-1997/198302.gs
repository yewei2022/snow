'reinit'
'open F:\snow_related\code\by_grads\tbb_test\tbb.ctl'
'enable print F:\snow_related\pic\tbb\198302.gmf'
'set lon 80.5 120.5'
'set lat -0.5 45.5'
i=2185
while(i<=2217) 
'set t 'i''
'set gxout shaded'
'set mpdset cnworld '
'set csmooth on'
'set grid on 3'
'set xlint 2.5'
'set ylint 2.5'
'set clevs -60 -50 -40 -30 -20 -10'
'set ccols 9 2 5 4 3 10 0'
'd tbb+100-273'
'cbarn'
'q time'
res=subwrd(result,3)
'draw title 'res
'print'
'c'
 i=i+1 
endwhile

'disable print'
;

