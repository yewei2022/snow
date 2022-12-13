;绘制降雪日数 降水量 积雪深度 的 月变化
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/days_pre_gss_mon.ncl

; ; unique_5.ncl; xy_7.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_TC/"
  file_dir1="/mnt/f/snow_sts_data/1981-2020/days_pre_gss_mon.txt"
  f1    = asciiread(file_dir1,-1,"string")
  days  = stringtointeger(str_get_field(f1(1:),2," ")) 
  pre  = stringtofloat(str_get_field(f1(1:),3," ")) 
  gss   = stringtofloat(str_get_field(f1(1:),5," ")) 
  mon=ispan(1, 12, 1)
  days_fill=(/0,0,0,0,0,0,0,0,0,0,0,0/)
  pre_fill=(/0,0,0,0,0,0,0,0,0,0,0,0/)
  gss_fill=(/0,0,0,0,0,0,0,0,0,0,0,0/)

; print(gss)
; exit

;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+"days_pre_gss_mon" )  ; send graphics to PNG file


gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/5,7,13/)

  res   = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.4       ; Changes the aspect ratio
  res@vpWidthF   = 0.6
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode          = "Explicit"         ; explicit labels
  res@tmXBValues  = mon
  res@tmXBLabels  = (/"Jan","Feb","Mar","Apr","May","Jun",\
                     "Jul","Aug","Sep","Oct","Nov","Dec"/) 

  res@gsnXYBarChart = True
  res@gsnXYBarChartBarWidth = 0.25           ; change bar widths
  res@tiYAxisFontHeightF=0.02
 

  resL = res
  resL@tmXTOn      = False ;关刻度
  resL@tmYROn      = False 
  resL@gsnMaximize = True

  resL@trXMinF = 0.2
  resL@trXMaxF = 12.8
  resL@trYMinF   = 0       ; min value on y-axis
  resL@trYMaxF   = max(days)+1       ; max value on y-axis  
  resL@gsnXYBarChartColors =colors(0)
  resL@tmYLMode="Manual"   
  resL@tmYLTickSpacingF=5
  resL@tmYLMinorPerMajor=4   
  resL@tiYAxisString = "SF" ; y-axis label
 
;resR1，resR2用来作坐标轴；resR11,resR22用来画图
  resR1 =res
  resR1@trYMinF     = 0.      
  resR1@trYMaxF     = max(pre)+1        ; max value on y-axis
  ; resR1@gsnXYBarChartColors = colors(1)       ; seperately, not
  resR1@tiYAxisString = "PA (mm)" ; y-axis label

  resR11 =res
  resR11@tmYROn      = False 
  resR11@trYMinF     = 0.      
  resR11@trYMaxF     = max(pre)+1        ; max value on y-axis
  resR11@gsnXYBarChartColors = colors(1)       ; seperately, not
  resR11@tiYAxisString = "" ; y-axis label


  resR2 =res
  resR2@trYMinF     = 0      
  resR2@trYMaxF     = max(gss)+0.5        ; max value onS y-axis
  ; resR2@gsnXYBarChartColors = colors(2)       ; seperately, not
  resR2@tiYAxisString = "SD (cm)" ; y-axis label
  resR2@amOrthogonalPosF = 0.72   ; Move "v" axis line to right a little.


  resR22 =res
  resR22@tmYROn      = False
  resR22@trYMinF     = 0      
  resR22@trYMaxF     = max(gss)+0.5        ; max value on y-axis
  resR22@gsnXYBarChartColors = colors(2)       ; seperately, not
  resR22@tiYAxisString = "" ; y-axis label


posleft=fspan(0.74,11.75,12)

plot1 = gsn_csm_xy3(wks,posleft,days,pre_fill,gss_fill,resL,resR1,resR2)  ;画轴 
; ; draw(plot1)

plot2 = gsn_csm_xy2(wks,posleft+0.25,days_fill,pre,resL,resR11)   
; ; draw(plot2)

plot3 = gsn_csm_xy2(wks,posleft+0.5,days_fill,gss,resL,resR22)   
; draw(plot3)

overlay(plot1, plot2)
overlay(plot1, plot3)
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
poslb1=0.120
gsn_labelbar_ndc(wks,1,"SF",poslb1,0.28,lbres) ; draw left labelbar column
lbres@lbFillColors       = colors(1)
gsn_labelbar_ndc(wks,1,"PA",poslb1+0.2,0.28,lbres) ; draw left labelbar column
lbres@lbFillColors       = colors(2)
gsn_labelbar_ndc(wks,1,"SD",poslb1+0.4,0.28,lbres) ; draw left labelbar column


frame(wks) 
end
 


 

