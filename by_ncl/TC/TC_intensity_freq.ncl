; TC强度频率住张图
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/TC/TC_intensity_freq.ncl


begin

pic_dir = "/mnt/f/snow_related/pic/TC/"
filename="TC_intensity_freq"
file_dir="/mnt/f/snow_sts_data/TC/"+filename+".txt" ;所有
f1      = asciiread(file_dir,-1,"string")
per_max     = stringtofloat(str_get_field(f1(1:),4," "))*100  ;读取站号
per_dot     = stringtofloat(str_get_field(f1(1:),5," "))*100 
stdarr = new((/7,2/),"float")
; print(per_max)
; exit
stdarr(:,0)=per_max
stdarr(:,1)=per_dot

wks = gsn_open_wks("eps",pic_dir+filename)  ; send graphics to PNG file  
gsn_define_colormap(wks,"wgne15")
colors=(/7,13/)


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
sres@vpXF = .15
sres@trXMinF = 0.4
sres@trXMaxF = 7.6
sres@trYMinF = 0
sres@trYMaxF = 60
sres@gsnDraw = True
sres@gsnFrame = False
sres@gsnXYBarChart = True
sres@gsnXYBarChartBarWidth = 0.25           ; change bar widths
sres@tmXBMode          = "Explicit"         ; explicit labels
sres@tmXBValues        = ispan(1, 7, 1)
sres@tmXBLabels = (/"TD","TS","H1","H2","H3","H4","H5"/)
sres@tmEqualizeXYSizes=True
sres@tmXBLabelFontHeightF=0.018
sres@tmXBLabelAngleF=45
sres@gsnLeftStringFontHeightF=0.018
sres@tiYAxisString="Percentage(%)"

; sres@gsnLeftString="(d)"
; sres@gsnLeftStringOrthogonalPosF=-0.15
; sres@gsnLeftStringParallelPosF =0.018
; sres@txPerimOn=True

xpos1=fspan(0.751,6.758,7) ;位置调整，先定头，再定尾
intep=sres@gsnXYBarChartBarWidth
  
sres@gsnXYBarChartColors = colors(0)
plot1 = gsn_csm_xy(wks,xpos1,stdarr(:,0),sres)   ; draw each time series
sres@gsnXYBarChartColors = colors(1)         ; seperately, not
plot2 = gsn_csm_xy(wks,xpos1+intep,stdarr(:,1),sres)   ; advancing the frame        ; but tweaking where


draw(plot1)
draw(plot2)

frame(wks)      
end