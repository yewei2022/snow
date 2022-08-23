;绘制降雪日数和影响降雪的风暴个数的年变化或风暴活动日数
; 一左一右两条轴
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/snow_annual.ncl
; xy7.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/"
  file_dir="/mnt/f/snow_sts_data/1981-2020/snow_days_annual.txt"
  f       = asciiread(file_dir,-1,"string")
  year    = stringtointeger(str_get_field(f(1:),1," ")) 
  days   = stringtointeger(str_get_field(f(1:),2," ")) 


  ; file_dir1="/mnt/f/snow_sts_data/TC/TC_number_annual.txt"
  ; f1       = asciiread(file_dir1,-1,"string")
  ; tc_num     = stringtointeger(str_get_field(f1(1:),2," ")) 

  file_dir1="/mnt/f/snow_sts_data/TC/TC_days_annual.txt"
  f1       = asciiread(file_dir1,-1,"string")
  tc_num     = stringtointeger(str_get_field(f1(1:),2," ")) 



;*********************************
; create plot
;********************************
; wks   = gsn_open_wks ("ps", pic_dir+"days_tcs_time" ) 
wks   = gsn_open_wks ("ps", pic_dir+"snowdays_tcdays_time" ) 


  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/5,13/)

  res   = True
  res@gsnScale = True 
  res@gsnMaximize = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.43        ; Changes the aspect ratio
  res@vpWidthF   = 0.85
  res@tmXTOn      = False ;关刻度
  res@tmXBLabelAngleF     = 45.   ;
  ; res@tmXBLabelStride =2 
  res@tmXBMode="Manual"   
  res@tmXBTickSpacingF=5
  res@tmXBMinorPerMajor=4      
  res@trXMinF   = 1980        ; min value on y-axis
  res@trXMaxF   = 2021
  res@xyLineThicknesses =5


  resL=res
  resL@tmYROn      = False 
  resL@trYMinF   = 0        ; min value on y-axis
  resL@trYMaxF   = 9        ; max value on y-axis
  resL@tmYLMode="Manual"   
  resL@tmYLMinorPerMajor=1 
  resL@tiYAxisString = "Snowfall days" ; y-axis label
  resL@xyLineColors      = colors(0)                    ; line color

  resR=res
  resR@tmYROn    = True 
  resR@tmYLOn    = False
  resR@trYMinF   = 0        ; min value on y-axis
  resR@trYMaxF   = 24        ; max value on y-axis
  resR@tmYRMode="Manual"   
  resR@tmYRMinorPerMajor=1 
  resR@tiYAxisString = "Days during TCs" ; y-axis label
  resR@xyLineColors      = colors(1)                    ; line color  


; posleft=fspan(0.87,11.878,12)
plot = gsn_csm_xy2(wks,year,days,tc_num,resL,resR) 

;图例
lbres                    = True          ; labelbar only resources
lbres@lgItemType = "Lines" 
lbres@lgLineColors = colors(::-1)
lbres@lgMonoDashIndex = True
lbres@lgDashIndex = 0
lbres@lgLineThicknessF = 5
lbres@vpWidthF = 0.25
lbres@vpHeightF = 0.08
lbres@lgPerimFill = 0
lbres@lgPerimFillColor = "Background"
lbres@lgLabelFontHeightF = 0.15        ; font height. default is small
lbres@lgPerimOn=False
strs=(/ "Snowfall days","Days during TCs "/)

lbid = gsn_create_legend(wks, 2, strs(::-1), lbres)
 
; 将图例放置在图中
amres = True
amres@amParallelPosF =0.30 ;左右，正右左负
amres@amOrthogonalPosF = -0.35 ;上下，正下负上
dumLg = gsn_add_annotation(plot, lbid, amres)
draw(plot)

frame(wks)

end
 


 

