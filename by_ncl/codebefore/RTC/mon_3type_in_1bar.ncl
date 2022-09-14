;绘制不同子区域(3类)的月变化,只需要一个轴,每个x刻度对应1个柱
;  ncl /mnt/e/f/snow_related/code/by_ncl/RTC/mon_3type_in_1bar.ncl

; ; https://www.ncl.ucar.edu/Applications/Scripts/bar_16.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

pic_dir ="/mnt/e/f/snow_related/pic/RTC/"

count=0
filename=(/"Days","PA","SD"/)
unit=(/" "," (mm)"," (cm)"/)

  file_dir1="/mnt/f/f/snow_sts_data/RTC/mon_"+filename(count)+"_1.txt"
  f1       = asciiread(file_dir1,-1,"string")
  a1       = stringtofloat(str_get_field(f1(1:),2," ")) 

  file_dir2="/mnt/f/f/snow_sts_data/RTC/mon_"+filename(count)+"_2.txt"
  f2       = asciiread(file_dir2,-1,"string")
  a2       = stringtofloat(str_get_field(f2(1:),2," ")) 

  file_dir3="/mnt/f/f/snow_sts_data/RTC/mon_"+filename(count)+"_3.txt"
  f3       = asciiread(file_dir3,-1,"string")
  a3       = stringtofloat(str_get_field(f3(1:),2," ")) 


wks   = gsn_open_wks ("png", pic_dir+"mon_"+filename(count)+"_in_1bar" )  ; send graphics to PNG file
gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/5,7,13/)

  sres = True
  sres@gsnDraw = True
  sres@gsnFrame = False
  sres@vpWidthF = 0.6
  sres@vpHeightF = 0.5
  sres@tmXTOn=False
  sres@tmYROn=False
  sres@gsnRightString =""
  sres@tiYAxisString = filename(count)+unit(count)

  ; sres@vpXF = .15 ;不需要定位置

  ;---Set axes limits. Add extra space for X max.
  sres@trXMinF = 0.4
  sres@trXMaxF = 8.6
  sres@trYMinF = 0
  sres@trYMaxF = (max(a1) + max(a2)+max(a3))*1.1
  ; sres@tmXBLabelJust  = "BottomCenter" ;这个打开之后x轴标签七上八下

  ; sres@gsnScale       = True    ; Make labels on axes same size

  ;---Put labels on X axis
  sres@tmXBMode          = "Explicit"         ; explicit labels
  sres@tmXBValues        = (/1,2,3,4,5,6,7,8/)
  sres@tmXBLabels = (/"Feb","Apr","May","Jun","Sep","Oct","Nov","Dec"/)
  sres@tmXBLabelFontHeightF = 0.02
  sres@tmYLLabelFontHeightF = 0.02
  sres@tiMainFontHeightF = 0.025

 
; 绘图
;---Create blank plot without Y grid lines
  plot_without_xgrid = gsn_csm_blank_plot(wks,sres)

;---Create blank plot with Y grid lines
  sres@tmYMajorGrid                = True    ; Turn on grid lines
  sres@tmYMajorGridLineDashPattern = 2       ; Dashed lines
  sres@tmYMajorGridThicknessF      = 1.0     ; default is 2 (?)
  plot_with_xgrid = gsn_csm_blank_plot(wks,sres)

;---Arrays to hold the bar values and the bars themselves.
  nmonth=dimsizes(sres@tmXBValues)
  dum1 = new(nmonth,graphic)
  dum2 = new(nmonth,graphic)
  dum3 = new(nmonth,graphic)

;---Set some resources for the bars.
  bres           = True
  bres@gsEdgesOn = True      ; Outline the polygons (bars)
;
; Loop through each city and attach bar to plot that
; doesn't have grid lines.

  do i=1,nmonth
    bres@gsFillColor           = colors(0)
      
    ybar      = (/0,a1(i-1),a1(i-1),0,0/)
    xbar      = (/i-0.25,i-0.25,i+0.25,i+0.25,i-0.25/)
    dum1(i-1) = gsn_add_polygon(wks,plot_without_xgrid,xbar,ybar,bres)

    bres@gsFillColor          = colors(1)
    
    ybar      = (/a1(i-1),a2(i-1)+a1(i-1),a2(i-1)+a1(i-1),a1(i-1),a1(i-1)/)
    dum2(i-1) = gsn_add_polygon(wks,plot_without_xgrid,xbar,ybar,bres)
    
    bres@gsFillColor          = colors(2)

    ybar      = (/a1(i-1)+a2(i-1),a3(i-1)+a2(i-1)+a1(i-1),\
                  a3(i-1)+a2(i-1)+a1(i-1),a1(i-1)+a2(i-1),\
                  a1(i-1)+a2(i-1)/)
    dum3(i-1) = gsn_add_polygon(wks,plot_without_xgrid,xbar,ybar,bres)
 
  end do

;
; Drawing the plot will draw all the attached bars. Have to draw
; the plot twice: one with the X grid lines and one without, in
; order to make sure the X grid lines are behind the bars.
;
; Couldn't see how else to do this.
;
  draw(plot_with_xgrid)
  draw(plot_without_xgrid)


; 图例
  lbres                    = True          ; labelbar only resources
  lbres@vpWidthF           = 0.2           ; labelbar width
  lbres@vpHeightF          = 0.2           ; labelbar height
  lbres@lbBoxMajorExtentF  = 0.36          ; puts space between color boxes
  lbres@lbFillColors       = colors(::-1)
  lbres@lbMonoFillPattern  = True          ; Solid fill pattern
  lbres@lbLabelFontHeightF = 0.02         ; font height. default is small
  lbres@lbLabelJust        = "CenterLeft"  ; left justify labels
  lbres@lbPerimOn          = False
  lbres@lgPerimColor    = "white"
  labels = (/"E","C","S"/)
  gsn_labelbar_ndc(wks,3,labels(::-1),0.2,0.8,lbres) ; draw right labelbar column

  ; lbres@lbFillColors       = colors(2:3:-1)
  ; labels = (/"P3","P4"/)
  ; gsn_labelbar_ndc(wks,2,labels(::-1),0.52,0.23,lbres) ; draw left labelbar column  

frame(wks) 
end
 


 

