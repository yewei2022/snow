;绘制风暴影响的降水/雪占当月百分比平均值
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/per_pre_gss_mon.ncl

; ; unique_5.ncl; xy_7.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_byTC/"
  file_dir1="/mnt/f/snow_sts_data/1981-2020/per_pre_gss_mon.txt"
  f1    = asciiread(file_dir1,-1,"string")
  pre   = stringtofloat(str_get_field(f1(1:),2," "))*100 
  gss   = stringtofloat(str_get_field(f1(1:),4," "))*100 

;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+"per_pre_gss_mon" )  ; send graphics to PNG file

gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/7,13/)

sres = True
sres@gsnDraw               = False
sres@gsnFrame              = False
sres@gsnXRefLine           = 0
sres@tmYROn=False
sres@tmXTOn=False

sres@vpWidthF              = 0.3
sres@vpHeightF             = 0.6

sres@trYMinF               = 0.4
sres@trYMaxF               = 8.6
sres@trXMinF               = 0
sres@trXMaxF               = 80

sres@gsnXYBarChart         = True
sres@gsnXYBarChartBarWidth = 0.25           ; change bar widths

sres@tmYLMode              = "Explicit"         ; explicit labels
sres@tmYLValues            = ispan(1,8,1)
sres@tmYLLabels            = (/"Feb","Apr","May","Jun","Sep", \
                              "Oct","Nov","Dec"/)

; sres@tmYLLabelFontHeightF  = 0.0205
; sres@tmYRLabelFontHeightF  = 0.0205
; sres@tmXBLabelFontHeightF  = 0.0225

sres@gsnRightString        = ""
sres@tiXAxisString         = "Percentage(%)"
sres@tiXAxisFontHeightF    =0.015
  
plots = new(2,graphic)

xpos=fspan(.875,7.875,8)

sres@gsnXYBarChartColors = colors(0)
plots(0) = gsn_csm_xy(wks,pre,xpos,sres)

sres@gsnXYBarChartColors = colors(1)
plots(1) = gsn_csm_xy(wks,gss,xpos+0.25,sres)


overlay(plots(0),plots(1))
draw(plots)

; ; Create some labelbars for a legend
; lbres                    = True          ; labelbar only resources
; lbres@vpWidthF           = 0.1           ; labelbar width
; lbres@vpHeightF          = 0.2           ; labelbar height
; lbres@lbBoxMajorExtentF  = 0.15          ; puts space between color boxes
; lbres@lbMonoFillPattern  = True          ; Solid fill pattern
; lbres@lbLabelFontHeightF = 0.015         ; font height. default is small
; lbres@lbLabelJust        = "CenterLeft"  ; left justify labels
; lbres@lbPerimOn          = False

; labels = (/"Prep", "Snow"/)
; xpos1   = 0.23

; lbres@lbFillColors       = colors(0)
; gsn_labelbar_ndc(wks,1,labels(0),xpos1,0.23,lbres) ; draw left labelbar column
; lbres@lbFillColors       = colors(1)
; gsn_labelbar_ndc(wks,1,labels(1),xpos1+0.32,0.23,lbres) ; draw left labelbar column

frame(wks) 
end
 


 

