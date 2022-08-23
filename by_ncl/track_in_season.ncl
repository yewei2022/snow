; 各个季节的track

;  ncl /mnt/f/snow_related/code/by_ncl/track_in_season.ncl

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
file_name=(/"winter","premon","monsoon","postmon"/)
pic_str=(/"Winter","Pre-monsoon","Monsoon","Post-monsoon"/)
mon_name=(/"(1-2)","(3-5)","(6-9)","(10-12)"/)
TC_file_path= "/mnt/f/snow_sts_data/TC/track_in_season.txt"
nfil        =numAsciiRow(TC_file_path)-1
files       = asciiread(TC_file_path, -1, "string")
TC          = str_get_field(files(1:),4," ")
TC_season   = str_get_field(files(1:),3," ")
extrm_file_path= "/mnt/f/snow_sts_data/TC/TC_dot_extrm_season.txt"
extrm_files    = asciiread(extrm_file_path, -1, "string")
lon_extrm            = stringtofloat(str_get_field(extrm_files(1:),2," ")) 
lat_extrm            = stringtofloat(str_get_field(extrm_files(1:),3," "))
dot_season        = str_get_field(extrm_files(1:),6," ")


wks = gsn_open_wks("eps", pic_dir+file_name(count)+"_track")
 
  res = True
  res@gsnLeftString = pic_str(count)+mon_name(count)
  res@gsnLeftStringFontHeightF=0.02
  res@gsnLeftStringOrthogonalPosF=0.012
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
  res@mpMinLonF = 74.
  res@mpMaxLonF = 105.
  res@gsnMajorLonSpacing    =5 
  res@gsnMinorLonSpacing    =1  
  res@gsnMajorLatSpacing    =5 
  res@gsnMinorLatSpacing    =1

  res@mpDataSetName = "/mnt/d/ChinaMap/Earth..4"
  res@mpFillOn      = False
  res@mpOutlineBoundarySets = "National"
  res@mpDataBaseVersion = "MediumRes"

; ;------------------------------画路径--------------------------
  map = gsn_csm_map(wks,res)
color="black"
  do i=0,nfil-1
    if (TC_season(i).eq.file_name(count)) then
    plot_track(wks,TC(i),map,color)  
    end if   
  end do

 
; ; ; ==============================»绘制极端降雪时的TC位置======================
; ; count=0 时没有数据
;   season_ind=str_match_ind(dot_season, file_name(count))
;   lon_dot=lon_extrm(season_ind)
;   lat_dot=lat_extrm(season_ind)

;   txres               = True                     ; text mods desired
;   txres@txFontHeightF = 0.02                     ; font smaller. default big
;   txres@txFontThicknessF=1.2
;   txres@txFontColor="red"
;   dum_tc = gsn_add_text(wks,map,"~F37~p",lon_dot,lat_dot,txres) 

; 高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 8.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)

end
