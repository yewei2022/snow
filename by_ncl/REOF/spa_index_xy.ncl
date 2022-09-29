;;
;  ncl /mnt/f/snow_related/code/by_ncl/REOF/spa_index_xy.ncl

; bar4.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"



begin
;---Generate random data with an average of 10 and a stddev of 3.
pic_dir ="/mnt/f/snow_related/pic/snow_TC/REOF/"
  file_dir="/mnt/f/snow_sts_data/REOF/spa_index.txt"
  f1       = asciiread(file_dir,-1,"string")
  year    = stringtointeger(str_get_field(f1(1:),1," "))
  s_index     = stringtofloat(str_get_field(f1(1:),2," "))
  n_index     = stringtofloat(str_get_field(f1(1:),3," "))
  npts        =  numAsciiRow(file_dir)-1
;---Create new 2D array to hold groupings of values   
data2d = new((/2,npts/),typeof(s_index))
data2d(0,:) = s_index
data2d(1,:) = n_index

;********************************
wks   = gsn_open_wks ("eps", pic_dir+"spa_index_xy")  ; send graphics to PNG file

colors=(/"blue","red"/)
labels=(/"S-Index","W-Index"/)  
Markers =(/15,9/) 

;---Create a scatter plot
  res                    = True                   ; plot mods desired
  res@gsnFrame           =False
  res@gsnDraw            =False
  ; res@tiMainString       = "Scatter plot with grouped markers"
  res@trXMaxF            =75
  res@tmXTOn             =False
  res@tmYROn             =False
  res@tmXBMinorPerMajor  =19
  res@vpWidthF   =0.6
  res@vpHeightF =0.4

;---Set some legend resurces
  ; res@pmLegendDisplayMode    = "Always"         ; Turn on the legend
  ; res@lgOrientation          = "horizontal"     ; Default is vertical
  ; res@pmLegendWidthF         = 0.75             ; Make it wider
  ; res@pmLegendOrthogonalPosF = -0.1             ; Move it up slightly
  ; res@lgPerimOn              = False            ; Turn off the perimeter box
  ; res@xyExplicitLabels       = labels         ; Set the legend labels

;---Set some marker resources
  res@xyMarkLineMode     = "Markers"
  res@xyMarkerThicknessF = 2
  res@xyMarkerColors     = colors   ; It's okay to list more than you need here
;
; Set the marker indexes. There are 17 predefined ones at:
;
;   http://www.ncl.ucar.edu/Document/Graphics/Images/markers.png
;
; or you can define your own with NhNewMarker:
;   http://www.ncl.ucar.edu/Document/Functions/Built-in/NhlNewMarker.shtml
  res@xyMarkers          = Markers ; Again, you can list more than you need.
  ; res@xyMarkerSizeF      =0.008
  ;添加辅助线
  res@gsnYRefLine =0
  res@gsnYRefLineDashPattern=4
  res@gsnYRefLineThicknessF=3
  res@gsnYRefLineColor  ="green"


  plot  = gsn_csm_y (wks,data2d,res)


; 绘制图例
  resLg = True
  resLg@gsMarkerSizeF = 0.018 
  resLg@gsMarkerThicknessF =2
  txres               = True
  txres@txFontHeightF = 0.018
  xleg=fspan(0.25, 0.5, 2)
  xleg=xleg
  xtxt=xleg+0.06
  yleg=fspan(0.85, 0.85, 2)
  yleg=yleg-0.1
  ytxt = yleg   ; strings.
  do i = 0,1
    resLg@gsMarkerIndex  = Markers(i)
    resLg@gsMarkerColor  = colors(i)
    gsn_polymarker_ndc(wks,xleg(i),yleg(i),resLg)
    gsn_text_ndc      (wks,labels(i),xtxt(i),ytxt(i),txres)
  end do

; 画类似误差条
  polyres                   = True       ; marker resources
  polyres@gsLineDashPattern = 0
  polyres@gsLineColor       = "black"
  polyres@gsLineThicknessF  = 2.0 ;3.0
  polyres@PreDraw = True

error_bar = new(npts,graphic)
do t = 0, npts-1  ;按照横轴点数来循环
  p_min :=where(data2d(0,t).lt.data2d(1,t), data2d(0,t), data2d(1,t))
  p_max :=where(data2d(0,t).gt.data2d(1,t), data2d(0,t), data2d(1,t))
  ; print(p_min)
  ; print(p_max)
  error_bar(t) = gsn_add_polyline(wks,plot,(/t,t/),\
                                  (/p_min,p_max/),polyres)
end do

draw(plot)
frame(wks)
end
 


 

