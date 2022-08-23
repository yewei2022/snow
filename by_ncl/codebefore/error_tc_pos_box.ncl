;*********************************************
;这个箱线图我完全不能接受。。。。感觉是错的
; box_4.ncl
;
; Concepts illustrated:
;   - Drawing box plots
;   - Adding text to a box plot
;   - Setting the color of individual boxes in a box plot
;   - Setting the width of individual boxes in a box plot
;
;*********************************************
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;
; This file still has to be loaded manually
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/tc_pos_box.ncl

;*********************************************
begin
;**********************************************
; Create some fake data
;**********************************************
pic_dir = "/mnt/f/snow_related/pic/tc/"
f3= asciiread("/mnt/f/snow_sts_data/TC/tc_pos_infl_all.txt",-1,"string")
lon_dot   = stringtofloat(str_get_field(f3(1:),3," "))
lat_dot   = stringtofloat(str_get_field(f3(1:),4," "))
npts=numAsciiRow("/mnt/f/snow_sts_data/TC/tc_pos_infl_all.txt")-1
yval1 = new((/2,npts/),"float",-999.)
yval1(0,:)=lon_dot

x = (/0,1/)		
;**********************************************
; create plot
;**********************************************
  wks = gsn_open_wks("x11",pic_dir+"box")               ; send graphics to PNG file
;**********************************************
; resources for plot background
;**********************************************
  res            = True                         ; plot mods desired
  res@tmXBLabels = (/"Lon","Lat"/) ; labels for each box
  ; res@trYMinF     = 85.      
  ; res@trYMaxF     = 95.        ; max value on y-axis
;**********************************************
; resources for polylines that draws the boxes
;**********************************************  
  llres                   = True			
  llres@gsLineThicknessF  = 1.5                 ; line thickness 
;**********************************************
; resources that control color and width of boxes
;**********************************************  
  opti          = True			
  opti@boxWidth = 1.2				; Width of box (x units)
  opti@boxColors = (/"blue","red"/)  	; Color of box(es)
;***********************************************
  plot = boxplot(wks,x,yval1,opti,res,llres)	; All 3 options used...

  draw(plot)
  frame(wks)
  
end

	