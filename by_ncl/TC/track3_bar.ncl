
;画3类不同路径数量柱状图
;  ncl /mnt/f/snow_related/code/by_ncl/TC/track3_bar.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

; bar_10.ncl
;
; Concepts illustrated:
;   - Drawing horizontal filled bars using gsnXYBarChart
;   - Changing the aspect ratio of a bar plot
;   - Setting the minimum/maximum value of the X and Y axis in a bar plot
;   - Explicitly setting tickmarks and labels on the left Y axis
;   - Turning off tickmarks, but not the labels
;   - Overlaying XY plots on each other
;   - Drawing grid lines on an XY plot
;*************************************************
; This script requires NCL V6.4.0 or later to 
; run. See bar_old_10.ncl for an older way of
; creating this plot.
;*************************************************
; This file is loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"

begin

pic_dir = "/mnt/f/snow_related/pic/TC/track/"
data1 = (/54,46,41/)
data2 = (/27,2,21/)
values=(/"50%","4%","51%"/)
stdarr = new((/3,2/),"integer")
stdarr(:,0)=data1
stdarr(:,1)=data2

wks = gsn_open_wks("eps",pic_dir+"track_bar")  ; send graphics to PNG file  
gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/5,13/)

     sres = True
     sres@vpWidthF = 0.5
     sres@vpHeightF = 0.5
     sres@tmXTOn=False
     sres@tmYROn=False
     ; sres@vpXF = .15
     sres@trXMinF = 0.4
     sres@trXMaxF = 3.6
     sres@trYMinF = 0
     sres@trYMaxF = 65
     sres@gsnDraw = True
     sres@gsnFrame = False
     sres@gsnXYBarChart = True
     sres@gsnXYBarChartBarWidth = 0.15           ; change bar widths
     sres@tmXBMode          = "Explicit"         ; explicit labels
     sres@tmXBValues        = (/1,2,3/)
     sres@tmXBLabels = (/"NW","W","NE"/)
     sres@gsnRightString = ""
     sres@tmXBLabelFontHeightF=0.015
     sres@tiYAxisString="Frequency"

        
     sres@gsnXYBarChartColors = colors(0)
     xpos1=fspan(0.926,2.92,3)
     plot1 = gsn_csm_xy(wks,xpos1,stdarr(:,0),sres)   ; draw each time series
     sres@gsnXYBarChartColors = colors(1)         ; seperately, not
     plot2 = gsn_csm_xy(wks,xpos1+0.15,stdarr(:,1),sres)   ; advancing the frame        ; but tweaking where

; add text labels
;**********************************************************  
txres                     = True                 ; text mods desired
txres@txFontHeightF       = 0.015                ; default size is HUGE!
; txres@txAngleF            = 52.                  ; text angle
txres@txJust              = "CenterLeft"         ; puts text on top of bars

do n = 1,3
  gsn_text(wks,plot2,values(n-1),n,data2(n-1)+1.5,txres) ; add labels
end do

;Í¼Àý
lbres                    = True          ; labelbar only resources
lbres@vpWidthF           = 0.2           ; labelbar width
lbres@vpHeightF          = 0.08           ; labelbar height
lbres@lbBoxMajorExtentF  = 0.32          ; puts space between color boxes
lbres@lbMonoFillPattern  = True          ; Solid fill pattern
lbres@lbLabelFontHeightF = 0.015        ; font height. default is small
lbres@lbLabelJust        = "CenterLeft"  ; left justify labels
lbres@lbPerimOn          = False
lbres@lgPerimColor      = "white"
lbres@lbFillColors       = colors(0)
gsn_labelbar_ndc(wks,1,"All TCs",0.2,0.8,lbres) ; draw left labelbar column
lbres@lbFillColors       = colors(1)
gsn_labelbar_ndc(wks,1,"TCs affecting TP",0.41,0.8,lbres) ; draw left labelbar column
frame(wks)      
end