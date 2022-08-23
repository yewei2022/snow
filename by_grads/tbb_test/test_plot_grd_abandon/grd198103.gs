'reinit'
'open H:/tbb_test/datasets/grd/grd.ctl'
'enable print F:\snow_related\pic\tbb\198103_grd.gmf'
*
'set lon 80.5 120.5'
'set lat -0.5 45.5'
i=1
while(i<=53) 
'set t 'i''
'set gxout shaded'
'set mpdset cnworld '
'set csmooth on'
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
*'printim F:\snow_related\grads\pic\out.png x1000 y800 white'
