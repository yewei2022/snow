;绘制不同type(3类)的月变化,只需要一个轴,每个x刻度对应三个柱
;  ncl /mnt/f/snow_related/code/by_ncl/CTC/mon_3type_in_3bar.ncl

; ; unique_5.ncl; xy_7.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

pic_dir ="/mnt/f/snow_related/pic/CTC/500_10m/snow_group/"

count=3
filename=(/"SF","PA","SDI","SD","Days"/)
delta=(/20,2,3,3,4/)
unit=(/" "," (mm)"," (cm)"," (cm)"," "/)

  file_dir1="/mnt/f/snow_sts_data/CTC/analysis/mon_"+filename(count)+"_type1.txt"
  f1       = asciiread(file_dir1,-1,"string")
  a1       = stringtofloat(str_get_field(f1(1:),2," ")) 

  file_dir2="/mnt/f/snow_sts_data/CTC/analysis/mon_"+filename(count)+"_type2.txt"
  f2       = asciiread(file_dir2,-1,"string")
  a2       = stringtofloat(str_get_field(f2(1:),2," ")) 

  file_dir3="/mnt/f/snow_sts_data/CTC/analysis/mon_"+filename(count)+"_type3.txt"
  f3       = asciiread(file_dir3,-1,"string")
  a3       = stringtofloat(str_get_field(f3(1:),2," ")) 


wks   = gsn_open_wks ("eps", pic_dir+"mon_"+filename(count)+"_type" )  ; send graphics to PNG file
gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/5,7,13/)

  sres = True
  sres@vpWidthF = 0.6
  sres@vpHeightF = 0.5
  sres@vpXF = .15
  sres@trXMinF = 0.4
  sres@trXMaxF = 8.6
  sres@trYMinF = 0
  sres@trYMaxF = max(a1)+delta(count)
  sres@gsnDraw = True
  sres@gsnFrame = False
  sres@tmXTOn=False
  sres@tmYROn=False
  sres@gsnXYBarChart = True
  sres@gsnXYBarChartBarWidth = 0.15           ; change bar widths
  sres@tmXBMode          = "Explicit"         ; explicit labels
  sres@tmXBValues        = (/1,2,3,4,5,6,7,8/)
  sres@tmXBLabels = (/"Feb","Apr","May","Jun","Sep","Oct","Nov","Dec"/)
  sres@tmXBLabelFontHeightF = 0.02
  sres@tmYLLabelFontHeightF = 0.02
  sres@tiMainFontHeightF = 0.025
  ; sres@tiMainFont = "helvetica"
  ; sres@tiMainString = "Nino3.4 Monthly Standard Deviation"
  sres@gsnRightString =""
  sres@tiYAxisString = filename(count)+unit(count)
 

  xpos=fspan(.855,7.85,8)   
  sres@gsnXYBarChartColors = colors(0) 
  plot1 = gsn_csm_xy(wks,xpos,a1,sres)   ; draw each time series
  sres@gsnXYBarChartColors = colors(1)          ; seperately, not
  plot2 = gsn_csm_xy(wks,xpos+0.15,a2,sres)   ; advancing the frame
  sres@gsnXYBarChartColors = colors(2)          ; but tweaking where
  plot3 = gsn_csm_xy(wks,xpos+0.3,a3,sres)    ; each time series is

  lbres                    = True          ; labelbar only resources
  lbres@vpWidthF           = 0.2           ; labelbar width
  lbres@vpHeightF          = 0.15           ; labelbar height
  lbres@lbBoxMajorExtentF  = 0.36          ; puts space between color boxes
  lbres@lbFillColors       = colors(::-1)
  lbres@lbMonoFillPattern  = True          ; Solid fill pattern
  lbres@lbLabelFontHeightF = 0.02         ; font height. default is small
  lbres@lbLabelJust        = "CenterLeft"  ; left justify labels
  lbres@lbPerimOn          = False
  lbres@lgPerimColor    = "white"
  labels = (/"P1","P2","P3"/)
  gsn_labelbar_ndc(wks,3,labels(::-1),0.15,0.8,lbres) ; draw right labelbar column

  ; lbres@lbFillColors       = colors(2:3:-1)
  ; labels = (/"P3","P4"/)
  ; gsn_labelbar_ndc(wks,2,labels(::-1),0.52,0.23,lbres) ; draw left labelbar column  

frame(wks) 
end
 


 

