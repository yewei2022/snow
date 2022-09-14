;绘制风暴年份，月份分布
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/TC/tcs_xy.ncl
;
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/TC/"
  filename="tc_date_infl"
  file_dir="/mnt/f/snow_sts_data/TC/"+filename+".txt" ;所有

  ; file_dir="/mnt/f/snow_sts_data/TC/tc_date_heavypre.txt" 
  f       = asciiread(file_dir,-1,"string")
  year    = stringtointeger(str_get_field(f(1:),4," ")) 
  mon     = stringtointeger(str_get_field(f(1:),5," ")) 
  wind    = stringtointeger(str_get_field(f(1:),3," ")) 
  mon@_FillValue =  32700

  npts = numAsciiRow(file_dir)-1 ;获取行数-1=站点数
  levels  = (/34,64,83,96,113,136/)
  nlevels = dimsizes(levels)
  num_distinct_markers = nlevels+1        ; number of distinct markers
  labels = new(num_distinct_markers,string)  ; Labels for legend.
  labels =(/"TD","TS","H1","H2","H3","H4","H5"/)

  TD=where(wind.lt.levels(0), mon, mon@_FillValue)
  TS=where(wind.ge.levels(0).and.wind.lt.levels(1), mon, mon@_FillValue)
  H1=where(wind.ge.levels(1).and.wind.lt.levels(2), mon, mon@_FillValue)
  H2=where(wind.ge.levels(2).and.wind.lt.levels(3), mon, mon@_FillValue)
  H3=where(wind.ge.levels(3).and.wind.lt.levels(4), mon, mon@_FillValue)
  H4=where(wind.ge.levels(4).and.wind.lt.levels(5), mon, mon@_FillValue)
  H5=where(wind.ge.levels(5), mon, mon@_FillValue)

  print(npts-num(ismissing(TD)))
  print(npts-num(ismissing(TS)))
  print(npts-num(ismissing(H1)))
  print(npts-num(ismissing(H2)))
  print(npts-num(ismissing(H3)))
  print(npts-num(ismissing(H4)))
  print(npts-num(ismissing(H5)))
  ; print(mon)
  ; exit

  data = new((/num_distinct_markers,npts/),integer)
  data(0,:) = TD
  data(1,:) = TS
  data(2,:) = H1
  data(3,:) = H2
  data(4,:) = H3
  data(5,:) = H4
  data(6,:) = H5
  data!1="year"
  data&year=year


wks  = gsn_open_wks("eps",pic_dir+filename)  
gsn_define_colormap(wks, "wgne15")

Markers=(/2,4,6,7,8,10,13/)
colors=(/4,7,12,13,16,14,15/)


;---------------------------------------------------------
  Tres=True
  ; Tres@gsnLeftString ="(a)"
  ; Tres@gsnLeftStringFontHeightF=0.02
  Tres@xyMarkLineMode = "Markers"               ; Markers *and* lines
  Tres@xyMarkerThicknessF=6
  Tres@xyMarkerSizeF=16
  Tres@trYMaxF=12;扩大y轴便签显示的最大值
  Tres@trYMinF=1
  Tres@tmYLMinorPerMajor=1
  Tres@tmYLValues=(/2,4,6,9,10,12/)
  Tres@tmXBMinorPerMajor=9

  Tres@tmXTOn = False ;关刻度
  Tres@tmYROn = False
  Tres@gsnDraw = False
  Tres@gsnFrame=False
  Tres@tiYAxisString="Month"
  Tres@tiXAxisString="Year"
  Tres@tiXAxisFontHeightF=0.018
  Tres@tiYAxisFontHeightF=0.018


  ; Tres@tmXBLabelAngleF = 48.   ;角度
  Tres@tmEqualizeXYSizes =True
  Tres@tmXBLabelFontHeightF = 0.018 ; x轴标签字号

  Tres@tmXMajorGrid                = True          ; implement x grid 
  Tres@tmXMajorGridThicknessF      = 1.0           ; 2.0 is default
  Tres@tmXMajorGridLineDashPattern = 2             ; select short dash lines  
  Tres@tmYMajorGrid                = True          ; implement y grid
  Tres@tmYMajorGridThicknessF      = 1.0           ; 2.0 is default
  Tres@tmYMajorGridLineDashPattern = 2             ; select short dash lines
  Tres@tmXMinorGrid                = True          ; implement x grid 
  Tres@tmXMinorGridThicknessF      = 1.0           ; 2.0 is default
  Tres@tmXMinorGridLineDashPattern = 2             ; select short dash lines  
  Tres@tmYMinorGrid                = True          ; implement y grid
  Tres@tmYMinorGridThicknessF      = 1.0           ; 2.0 is default
  Tres@tmYMinorGridLineDashPattern = 2             ; select short dash lines

plot=new(num_distinct_markers, graphic)
Tres0=Tres
Tres0@xyMarkerColor=colors(0)
Tres0@xyMarker=Markers(0)
plot(0)= gsn_csm_xy (wks,data&year,data(0,:),Tres0) ; create plot
do i=1,num_distinct_markers-1
  Tres@xyMarkerColor=colors(i)
  Tres@xyMarker=Markers(i)
  plot(i)= gsn_csm_xy (wks,data&year,data(i,:),Tres) ; create plot
  overlay(plot(0), plot(i))
end do
draw(plot(0))

; 绘制图例
  resLg = True
  resLg@gsMarkerSizeF = 0.018 
  resLg@gsMarkerThicknessF =5
  txres               = True
  txres@txFontHeightF = 0.015


  xleg=fspan(0.15, 0.7, 7)
  xleg=xleg+0.06
  xtxt=xleg+0.03
  yleg=fspan(0.18, 0.18, 7)
  yleg=yleg-0.1
  ytxt = yleg   ; strings.

  do i = 0,num_distinct_markers-1
    resLg@gsMarkerIndex  = Markers(i)
    resLg@gsMarkerColor  = colors(i)
    gsn_polymarker_ndc(wks,xleg(i),yleg(i),resLg)
    gsn_text_ndc      (wks,labels(i),xtxt(i),ytxt(i),txres)
  end do

frame(wks)
end

 


 

