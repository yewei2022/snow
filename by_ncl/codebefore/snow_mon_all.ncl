;绘制高原总降雪日数 和降水量两个变量的月变化
;两个纵轴横向排列
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/snow_all/snow_mon.ncl

; ; unique_5.ncl; xy_7.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_all/"
  file_dir="/mnt/f/snow_sts_data/1981-2020/snow_mon_all.txt"
  f       = asciiread(file_dir,-1,"string")
  days   = stringtointeger(str_get_field(f(1:),1," ")) 
  amts   = stringtofloat(str_get_field(f(1:),2," ")) 
  days@_FillValue =  32700
  amts@_FillValue =  32700.
  npts = numAsciiRow(file_dir)-1 ;获取行数-1=站点数
  mon=ispan(1, 12, 1)
  days_fill=(/0,0,0,0,0,0,0,0,0,0,0,0/)
  amts_fill=(/0,0,0,0,0,0,0,0,0,0,0,0/)


;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("ps", pic_dir+"mon_bar_all" )  ; send graphics to PNG file


gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/5,13/)

  res   = True
  ; res@gsnScale = True 
  res@gsnMaximize = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.5       ; Changes the aspect ratio
  res@vpWidthF   = 0.6
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode          = "Explicit"         ; explicit labels
  res@tmXBValues  = mon
  res@tmXBLabels  = (/"Jan","Feb","Mar","Apr","May","Jun",\
                     "Jul","Aug","Sep","Oct","Nov","Dec"/) 
  res@trXMinF = 0.4
  res@trXMaxF = 12.6
  res@gsnXYBarChart = True
  res@gsnXYBarChartBarWidth = 0.25           ; change bar widths 

  resL = res
  resL@tmXTOn      = False ;关刻度
  resL@tmYROn      = False 
  resL@trYMinF   = 1500      ; min value on y-axis
  resL@trYMaxF   = 33000        ; max value on y-axis  
  resL@gsnXYBarChartColors =colors(0)
  resL@tmYLMode="Manual"   
  resL@tmYLTickSpacingF=5000
  resL@tmYLMinorPerMajor=4   
  resL@tiYAxisString = "Number of snowfall days (d)" ; y-axis label
 

  resR =res
  resR@tmXTOn      = False ;关刻度
  resR@tmYROn      = True 
  resR@tmYLMode="Manual"   
  resR@tmYLTickSpacingF=1
  resR@tmYLMinorPerMajor=5 
  resR@trYMinF     = 0.      
  resR@trYMaxF     = 6.5        ; max value on y-axis
  resR@gsnXYBarChartColors = colors(1)       ; seperately, not
  resR@tiYAxisString = "Snowfall (mm)" ; y-axis label
  resR@tmYRMode="Manual"   
  resR@tmYRTickSpacingF=2
  resR@tmYRMinorPerMajor=3  

posleft=fspan(0.87,11.878,12)
plot1 = gsn_csm_xy2(wks,posleft,days,amts_fill,resL,resR)   
; ; draw(plot1)

plot2 = gsn_csm_xy2(wks,posleft+0.25,days_fill,amts,resL,resR)   
; draw(plot2)

overlay(plot1, plot2)
draw(plot1)

;图例
lbres                    = True          ; labelbar only resources
lbres@vpWidthF           = 0.2           ; labelbar width
lbres@vpHeightF          = 0.05           ; labelbar height
lbres@lbBoxMajorExtentF  = 0.32          ; puts space between color boxes
lbres@lbMonoFillPattern  = True          ; Solid fill pattern
lbres@lbLabelFontHeightF = 0.015        ; font height. default is small
lbres@lbLabelJust        = "CenterLeft"  ; left justify labels
lbres@lbPerimOn          = False
lbres@lgPerimColor      = "white"
lbres@lbFillColors       = colors(0)
poslb1=0.240
gsn_labelbar_ndc(wks,1,"Number of snowfall days",poslb1,0.18,lbres) ; draw left labelbar column
lbres@lbFillColors       = colors(1)
gsn_labelbar_ndc(wks,1,"Snowfall ",poslb1+0.32,0.18,lbres) ; draw left labelbar column
frame(wks) 
end
 


 

