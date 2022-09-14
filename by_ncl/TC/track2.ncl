; 绘制多条TC路径 不同颜色代表不同分类

;  ncl /mnt/f/snow_related/code/by_ncl/track2.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;********************************************************
undef("plot_track")
  procedure plot_track(wks,fiTC,map,color)
  local i,data,nrow,lat_tc,lon_tc,resLine,dumLine
  begin
  data = asciiread(fiTC, -1, "string")
  nrow = numAsciiRow(fiTC)
  lat_tc = new(nrow, "float")
  lon_tc = new(nrow, "float")
  lat_tc = stringtofloat(str_get_field(data, 7, ",")) *0.1
  lon_tc = stringtofloat(str_get_field(data, 8, ",")) *0.1
  resLine = True
  resLine@gsLineColor=color
  resLine@gsLineThicknessF = 6
  dumLine = new(nrow, graphic) 
  ;»æÖÆÏß
  do i = 0, nrow-2
    xx = (/ lon_tc(i), lon_tc(i+1)/)
    yy = (/ lat_tc(i), lat_tc(i+1)/) 
    dumLine(i) = gsn_add_polyline(wks, map, xx, yy, resLine)
  end do
  ;»æÖÆµã
  resDot =True
  resDot@gsMarkerIndex = 1
  resDot@gsMarkerSizeF = 0.025
  resDot@gsMarkerColor = color
  dumDot = gsn_add_polymarker(wks, map, lon_tc(0), lat_tc(0), resDot)
  map@$unique_string("dumDot")$ = dumDot
  map@$unique_string("dumLine")$ = dumLine
  end

begin

pic_dir = "/mnt/f/snow_related/pic/tc/"
count=0
file_name=(/"tc","extrm_tc"/)
label_name=(/"tp","extrm"/)
fil_list= "/mnt/f/snow_sts_data/TC/"+file_name(count)+"_file_list.txt"
tp_TC_files= asciiread(fil_list, -1, "string")
nfil = numAsciiRow(fil_list)
label_list= "/mnt/f/snow_sts_data/TC/"+label_name(count)+"_tc_label.txt"
f       = asciiread(label_list,-1,"string")
label   = stringtointeger(str_get_field(f(1:),2," "))
; print(label)
; exit

  wks = gsn_open_wks("x11", pic_dir+file_name(count)+"_track")
  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/14,7/)
 
  res = True
  ; res@gsnLeftString ="(c)"
  ; res@gsnLeftStringFontHeightF=0.02
  res@gsnDraw = False
  res@gsnFrame = False
  res@gsnMaximize=True
  res@gsnAddCyclic=False
  res@vpWidthF=0.5
  res@vpHeightF=0.6


  ;¹Ø¿Ì¶È
  res@tmXTOn = False 
  res@tmYROn = False
; ÉèÖÃµØÍ¼±ß½ç
  res@mpMinLatF = 0
  res@mpMaxLatF = 30
  res@mpMinLonF = 72.
  res@mpMaxLonF = 104.
  res@gsnMajorLonSpacing    =5 
  res@gsnMinorLonSpacing    =1.    
  res@gsnMajorLatSpacing    =5 
  res@gsnMinorLatSpacing    =1

  res@mpDataSetName = "/mnt/d/ChinaMap/Earth..4"
  res@mpFillOn      = False
  res@mpOutlineBoundarySets = "National"
  res@mpDataBaseVersion = "MediumRes"

; ;------------------------------»æÖÆ·ç±©Â·¾¶--------------------------
  map = gsn_csm_map(wks,res)

  do i=0,nfil-1
    if (label(i).eq.0) then
      color = colors(0)
    end if
    if (label(i) .eq.1 ) then
      color = colors(1)
    end if
    plot_track(wks,tp_TC_files(i),map,color)     
  end do

 
; 绘制全部TC路径，无论有无影响
  ; all_TC_dir="/mnt/f/snow_sts_data/BOB/"
  ; all_TC_files = systemfunc("ls "+all_TC_dir+"*.txt");Éú³ÉÎÄ¼þÂ·¾¶ÁÐ±í
  ; all_nfil = dimsizes(all_TC_files)
  ; all_label_list= "/mnt/f/snow_sts_data/TC/all_tc_label.txt"
  ; f2       = asciiread(all_label_list,-1,"string")
  ; all_label   = stringtointeger(str_get_field(f2(1:),2," "))
  ; print(all_TC_files)
  ; exit
  ;   do i=0,all_nfil-1
  ;   if (all_label(i).eq.0) then
  ;     color = colors(0)
  ;   end if
  ;   if (all_label(i) .eq.1 ) then
  ;     color = colors(1)
  ;   end if
  ;   plot_track(wks,all_TC_files(i),map,color)
  ; end do


; ; ==============================»绘制影响降雪时的TC位置======================

  ; ; 影响降雪时的TC位置
  ; f3= asciiread("/mnt/f/snow_sts_data/TC/TC_dot.txt",-1,"string")
  ; lon_dot   = stringtofloat(str_get_field(f3(1:),3," "))
  ; lat_dot   = stringtofloat(str_get_field(f3(1:),4," "))
  ; resDot=True
  ; resDot@gsMarkerIndex = 1
  ; resDot@gsMarkerSizeF = 0.02

  ; dumDot= gsn_add_polymarker(wks, map, lon_dot, lat_dot, resDot)

;¸ßÔ­ÂÖÀªÏß
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 8.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

; »æÖÆÍ¼Àý
  lgcolors=colors
  resLg = True 
  resLg@lgItemType = "Lines"
  resLg@lgMonoMarkerIndex = True
  resLg@lgMonoDashIndex = True
  resLg@lgDashIndex = 0
  resLg@lgLineColors = lgcolors(::-1)
  resLg@lgLineThicknessF = 6
  resLg@vpWidthF = 0.2
  resLg@vpHeightF = 0.2
  resLg@lgPerimFill = 0
  resLg@lgPerimFillColor = "Background"
  resLg@lgLabelFontHeightF = 0.09
  ; resLg@lgTitleFontHeightF = 0.018
  ; resLg@lgTitleString = ""
  lgstr=(/"Track A","Track B"/) 
  lbid = gsn_create_legend(wks, 2, lgstr(::-1), resLg)
 
; ½«Í¼Àý·ÅÖÃÔÚÍ¼ÖÐ
  amres = True
  amres@amParallelPosF = -0.358 ;×óÓÒ£¬ÕýÓÒ×ó¸º
  amres@amOrthogonalPosF = 0.338 ;ÉÏÏÂ£¬ÕýÏÂ¸ºÉÏ
  dumLg = gsn_add_annotation(map, lbid, amres)
draw(map)
frame(wks)

end
