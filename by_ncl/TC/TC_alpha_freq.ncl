; TC强度频率住张图
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/TC/TC_alpha_freq.ncl


begin

pic_dir = "/mnt/f/snow_related/pic/TC/"
filename="TC_alpha_freq"
file_dir="/mnt/f/snow_sts_data/TC/"+filename+".txt" ;所有
f1      = asciiread(file_dir,-1,"string")
per_all = stringtofloat(str_get_field(f1(1:),4," ")) 
per_infl= stringtofloat(str_get_field(f1(1:),5," "))
count_all = str_get_field(f1(1:),2," ")
count_infl= str_get_field(f1(1:),3," ")
per_all@_FillValue = 32700.
per_infl@_FillValue = 32700.
count_all@_FillValue = "32700"
count_infl@_FillValue = "32700"

nlevel = 6
stdarr = new((/nlevel,2/),"float")
; print(per_all
; exit
stdarr(:,0)=per_all
stdarr(:,1)=per_infl
stdarr=stdarr*100

wks = gsn_open_wks("eps",pic_dir+filename)  ; send graphics to PNG file  
gsn_define_colormap(wks,"wgne15")
colors=(/5,13/)


; ;========若是柱子在时刻之间，8个数据=========================
; sres@trXMinF = 1
; sres@trXMaxF = 9
; sres@tmXBValues        = ispan(1, 9, 1)
; sres@tmXBLabels = (/"26/00","26/06","26/12","26/18","27/00","27/06","27/12","27/18","28/00"/)
; xpos1=fspan(1.35,8.36,8) ;位置调整，先定头，再定尾


;===============若是柱子在时刻上===============================
sres = True
sres@vpWidthF = 0.5
sres@vpHeightF = 0.4
sres@tmXTOn=False
sres@tmYROn=False
sres@vpXF = 0.15
sres@trXMinF = 0.4
sres@trXMaxF = tofloat(nlevel)+0.6
sres@trYMinF = 0
sres@trYMaxF = 95
sres@gsnDraw = True
sres@gsnFrame = False
sres@gsnXYBarChart = True
sres@gsnXYBarChartBarWidth = 0.4          ; change bar widths
sres@tmXBMode          = "Explicit"         ; explicit labels
sres@tmXBValues        = ispan(1, nlevel, 1)
sres@tmXBLabels = (/"<20","20-40","40-60","60-80","80-100",">100"/)
sres@tmEqualizeXYSizes=True
sres@tmXBLabelFontHeightF=0.015
; sres@tmXBLabelAngleF=45
sres@gsnLeftStringFontHeightF=0.015
sres@tiYAxisString="Percentage (%)"
sres@tiXAxisString="Asymmetry index ~F33~a~F~ (km)"
 
sres@tmYMajorGrid                = True          ; implement y grid
sres@tmYMajorGridThicknessF      = 1.0           ; 2.0 is default
sres@tmYMajorGridLineDashPattern = 2             ; select short dash lines


; sres@gsnLeftString="(d)"
; sres@gsnLeftStringOrthogonalPosF=-0.15
; sres@gsnLeftStringParallelPosF =0.018
; sres@txPerimOn=True

xpos1=fspan(0.8,tofloat(nlevel-1)+0.8,nlevel) ;位置调整，先定头，再定尾
intep=sres@gsnXYBarChartBarWidth
  
sres@gsnXYBarChartColors = colors(0)
plot1 = gsn_csm_xy(wks,xpos1,stdarr(:,0),sres)   ; draw each time series
sres@gsnXYBarChartColors = colors(1)         ; seperately, not
plot2 = gsn_csm_xy(wks,xpos1+intep,stdarr(:,1),sres)   ; advancing the frame        ; but tweaking where

; add text labels
;**********************************************************  
txres                     = True                 ; text mods desired
txres@txFontHeightF       = 0.015                ; default size is HUGE!
; txres@txAngleF            = 52.                  ; text angle
txres@txJust              = "CenterCenter"         ; puts text on top of bars

plot11=gsn_add_text(wks, plot1, count_all, xpos1, stdarr(:,0)+2, txres)
plot22=gsn_add_text(wks, plot2, count_infl, xpos1+intep,\
 stdarr(:,1)+2, txres)  


draw(plot1)
draw(plot2)

frame(wks)      
end