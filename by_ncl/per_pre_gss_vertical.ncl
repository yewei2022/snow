;绘制风暴影响的降水、积雪占当月百分比平均值 竖条
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/per_pre_gss_vertical.ncl

; ; unique_5.ncl; xy_7.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_TC/"
  file_dir1="/mnt/f/snow_sts_data/1981-2020/per_pre_gss_mon.txt"
  f1    = asciiread(file_dir1,-1,"string")
  pre   = stringtofloat(str_get_field(f1(1:),2," "))*100 
  gss   = stringtofloat(str_get_field(f1(1:),4," "))*100 


wks   = gsn_open_wks ("eps", pic_dir+"per_pre_gss_vertical" )  ; send graphics to PNG file


gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/7,13/)

  res   = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.4       ; Changes the aspect ratio
  res@vpWidthF   = 0.6
  res@tmXTOn      = False ;关刻度
  res@tmYROn      = False 
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode          = "Explicit"         ; explicit labels
  res@tmXBValues        = ispan(1,8,1)
  res@tmXBLabels        =(/"Feb","Apr","May","Jun","Sep", \
                              "Oct","Nov","Dec"/)
  res@trXMinF = 0.4
  res@trXMaxF = 8.6
  res@trYMinF               = 0
  res@trYMaxF               = 80
  res@gsnXYBarChart = True
  res@gsnXYBarChartBarWidth = 0.25           ; change bar widths 

  res@gsnRightString        = ""
  res@tiYAxisString         = "Percentage(%)"
  ; res@tiYAxisFontHeightF    =0.015


plots = new(2,graphic)

xpos=fspan(.875,7.875,8)

res@gsnXYBarChartColors = colors(0)
plots(0) = gsn_csm_xy(wks,xpos,pre,res)

res@gsnXYBarChartColors = colors(1)
plots(1) = gsn_csm_xy(wks,xpos+0.25,gss,res)


overlay(plots(0),plots(1))
draw(plots)


;图例
lbres                    = True          ; labelbar only resources
lbres@vpWidthF           = 0.2           ; labelbar width
lbres@vpHeightF          = 0.05           ; labelbar height
lbres@lbBoxMajorExtentF  = 0.32          ; puts space between color boxes
lbres@lbMonoFillPattern  = True          ; Solid fill pattern
lbres@lbLabelFontHeightF = 0.018        ; font height. default is small
lbres@lbLabelJust        = "CenterLeft"  ; left justify labels
lbres@lbPerimOn          = False
lbres@lgPerimColor      = "white"
lbres@lbFillColors       = colors(0)
poslb1=0.28
gsn_labelbar_ndc(wks,1,"PA",poslb1,0.34,lbres) ; draw left labelbar column
lbres@lbFillColors       = colors(1)
gsn_labelbar_ndc(wks,1,"SD",poslb1+0.25,0.34,lbres) ; draw left labelbar column

frame(wks) 
end
 


 

