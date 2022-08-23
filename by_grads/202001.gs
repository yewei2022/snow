'reinit'
name='202001'
max=79
'open F:\snow_related\code\by_grads\'name'.ctl'
'enable print F:\snow_related\pic\tbb\'name'.gmf'
'set lon 75 120'
'set lat 0 45'
i=1
while(i<=max) 
'set t 'i''
'set gxout shaded'
'set mpdset cnworld '
'set csmooth on'
'set grid on 3'
'set xlint 2.5'
'set ylint 2.5'
'set clevs -60 -50 -40 -30 -20 -10'
'set ccols 9 2 5 4 3 10 0'
'd tbb'
'cbarn'
'q time'
res=subwrd(result,3)
'draw title 'res
'print'
'c'
 i=i+3 
endwhile

'disable print'
;

