;绘制TC个数、TC活动日数、降雪日数的年变化
;横向排列三条y轴,一左两右
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/TC_snowdays_annual.ncl

; xy_19.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/tc/"
  filename="TC_snowdays_annual"
  file_dir="/mnt/f/snow_sts_data/TC/"+filename+".txt"
  f       = asciiread(file_dir,-1,"string")
  year    = stringtointeger(str_get_field(f(1:),1," ")) 
  tc_days   = stringtofloat(str_get_field(f(1:),2," ")) 
  tc_num   = stringtofloat(str_get_field(f(1:),3," ")) 
  snow_days   = stringtofloat(str_get_field(f(1:),4," "))


; print(days)
; print(alldays)

;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+filename ) 


  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/4,7,13/)

  res   = True
  res@gsnScale = True 
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.43        ; Changes the aspect rate
  res@vpWidthF   = 0.85
  res@tmXTOn      = False ;关刻度
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode="Manual"   
  res@tmXBTickSpacingF=5
  res@tmXBMinorPerMajor=4      
  res@xyLineThicknesses =5

  resL=res
  resL@tmYROn      = False

  ;这三步只能在resL里打开
  resL@gsnMaximize = True 
  resL@trXMinF   = 1980       
  resL@trXMaxF   = 2021 

  resL@trYMinF   = 0        ; min value on y-axis
  resL@trYMaxF   = max(tc_num)+1        ; max value on y-axis
  resL@tmYLMode="Manual"   
  resL@tmYLMinorPerMajor=1 
  resL@tiYAxisString = "TCs" ; y-axis label
  resL@xyLineColors      = colors(0)                    ; line color

  resR1=res
  ; resR1@tmYROn    = True 
  ; resR1@tmYLOn    = False
  ; resR1@trYMinF   = 170        ; min value on y-axis
  resR1@trYMaxF   = max(tc_days)+1        ; max value on y-axis
  ; resR1@tmYRMode="Manual"   
  ; resR1@tmXBTickSpacingF=50
  ; ; resR1@tmYRMinorPerMajor=5
  resR1@tiYAxisString = "TC days" ; y-axis label
  resR1@xyLineColors      = colors(1)                    ; line color  

  resR2=res
  ; resR2@tmYROn    = True 
  ; resR2@tmYLOn    = False
  resR2@trYMinF   = 0.        ; min value on y-axis
  resR2@trYMaxF   = max(snow_days)+1        ; max value on y-axis
  ; resR2@tmYRMode="Manual"   
  ; ; resR2@tmYRMinorPerMajor=1 
  resR2@tiYAxisString = "Snowfall days" ; y-axis label
  resR2@xyLineColors      = colors(2)                    ; line color 

  ; resR2@amOrthogonalPosF = 0.72   
  ; Move "v" axis line to right a little.

plot = gsn_csm_xy3(wks,year,tc_num,tc_days,snow_days,resL,resR1,resR2) 



;图例
lbres                    = True          ; labelbar only resources
lbres@lgItemType = "Lines" 
lbres@lgLineColors = colors(::-1)
lbres@lgMonoDashIndex = True
lbres@lgDashIndex = 0
lbres@lgLineThicknessF = 5
lbres@vpWidthF = 0.2
lbres@vpHeightF = 0.09
lbres@lgPerimFill = 0
lbres@lgPerimFillColor = "Background"
lbres@lgLabelFontHeightF = 0.1        ; font height. default is small
lbres@lgPerimOn=False
strs=(/ "TCs","TC days","Snowfall days"/)

lbid = gsn_create_legend(wks, 3, strs(::-1), lbres)
 
; 将图例放置在图中
amres = True
amres@amParallelPosF =0.30 ;左右，正右左负
amres@amOrthogonalPosF = -0.36 ;上下，正下负上
dumLg = gsn_add_annotation(plot, lbid, amres)


draw(plot)
frame(wks)

end
 


 

