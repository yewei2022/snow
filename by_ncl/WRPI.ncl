;读取TC所有活动日（包含顺延一天) ERA5 500hPa nc资料
; 读取py生成的nc文件时间
; 计算西脊点
;寻找区域最大值

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/WRPI.ncl

begin

pic_dir  = "/mnt/f/snow_related/pic/atmos_env/" 

; 1 read ERA5
name1=(/"geo500","u500","v500"/)
count:=0
data_dir0 ="/mnt/f/snow_sts_data/ERA5/pick/"+name1(count)+"_alltcdays.nc" 
; count:=1
; data_dir1 ="/mnt/f/snow_sts_data/ERA5/pick/"+name1(count)+"_6h.nc" 
; count:=2
; data_dir2 ="/mnt/f/snow_sts_data/ERA5/pick/"+name1(count)+"_6h.nc" 

; 1 读数据
data0    = addfile(data_dir0, "r")
; data1    = addfile(data_dir1, "r")
; data2    = addfile(data_dir2, "r")

z = data0->z(:,{10:50},{90:140})
; u = data1->u(:,{500},:,:)
; v = data2->v(:,{500},:,:)

z = z/98.
; 读取时间 py转换过的只能先转成integer再读取
time0        = tointeger(z&time)
time0@units  =  "days since 1981-10-25 00:00:0.0"
date = cd_calendar(time0, -2) ;到日

; ; ; ; ====================测试单个 画图查看==============================
; ; ; ; 挑选特定时间  特定值放后面 
; need_date = 20200518
; date_ind_TC = str_match_ind(date,tostring(need_date))
; z_need1 = z(date_ind_TC,:,:) ;TC

; ==========循环着来=============
lon_arr = new(dimsizes(date), float)

do i = 0, dimsizes(date)-1

  need_date := date(i)
  z_need1 := z(i,:,:) ;TC
  z_need1@_FillValue := 32700.
  ; printVarSummary(z_need1)
  ; exit
  value_min := 587.5
  value_max := 588.5

  min_lon := 32700.
  do while (min_lon .eq. 32700.)
    ; ; z_mask 用于绘图看588线
    ; z_mask = where((z_need1.ge.value_min) .and. (z_need1.lt.value_max),\
    ; z_need1, z_need1@_FillValue)
    ; 找西脊点位置
    lon := conform(z_need1, z_need1&longitude, 1)
    copy_VarCoords(z_need1, lon)
    ; 测试lon 对不对
    ; printVarSummary(lon(0,5))
    ; printVarSummary(lon(40,5))
    ; lon@_FillValue := 32700.
    lon_mask := where((z_need1.ge.value_min) .and. (z_need1.lt.value_max),\
    lon, 32700.)
    copy_VarCoords(z_need1, lon_mask)
    min_lon := min(lon_mask)
    print("======"+tostring(need_date)+"=MIN=====")
    print(tostring(min_lon))
    print("========================")
    value_min := value_min-1.
    value_max := value_max-1. 
  end do  
  print("======"+tostring(need_date)+"=MIN=final=====")
  print(tostring(min_lon))
  print("========================")
lon_arr(i) = min_lon
end do 

; ; 写入二进制文件 记得把原文件删掉 不然运行一次接着写入一次
  fout_name = "/mnt/f/snow_sts_data/ERA5/deal/WRPI_alltcdays.txt"
  print("--------------------------------------")
  print("start writing output files: " + fout_name + " ......")
  asciiwrite(fout_name,  sprintf("%5.2f", lon_arr ))
  print("finish writing output files: " + fout_name + " ......")
  print("--------------------------------------")


; ;  绘图
; ; delete([/data0/])

; wks = gsn_open_wks("x11", pic_dir+"geo500"+"_"+tostring(need_date))


; ;---Set up some map resources.
;   res                       = True
;   ; res@gsnMaximize           = True             ; Maximize plot in frame.
;   res@gsnDraw               = False            ; Will draw later
;   res@gsnFrame              = False            ; Don't advance the frame
;   res@gsnLeftString         = ""
;   res@gsnRightString        = ""
;   res@tmYROn                =False
;   res@tmXTOn                =False
;   res@gsnAddCyclic          =False
;   res@tmEqualizeXYSizes     =True
;   ; res@tmXBLabelFontHeightF  =0.02

;   mpres                       =res
;   mpres@mpMinLatF             = 10.
;   mpres@mpMaxLatF             = 50.
;   mpres@mpMinLonF             = 90
;   mpres@mpMaxLonF             = 140
;   mpres@gsnMajorLonSpacing    =10. 
;   mpres@gsnMinorLonSpacing    =5.    
;   mpres@gsnMajorLatSpacing    =10. 
;   mpres@gsnMinorLatSpacing    =5

;   mpres@mpFillOn=False

;   mpres@mpDataBaseVersion       = "MediumRes"
;   mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
;   mpres@mpOutlineSpecifiers     = (/"China:states"/)

; ;--------------叠加高度场--------------

; 	cnres1 = res
; 	cnres1@cnFillOn        = False  ;cn means ContourPlot
; 	cnres1@cnLinesOn       = True   
; 	;cnres1@cnMonoLineColor= False
; 	cnres1@cnLineColor     ="blue"
; 	;cnres1@cnSpanLinePalette = True
; 	;cnres1@cnLinePalette     = "rainbow"
; 	cnres1@cnLineLabelsOn     = True  
; 	cnres1@cnInfoLabelOn      = False ; set false will not set an information label
; 	cnres1@cnLevelSelectionMode = "ManualLevels" 
; 	; cnres1@cnMinLevelValF      = 550
; 	cnres1@cnMaxLevelValF      = 592
; 	cnres1@cnLevelSpacingF      = 1
; 	cnres1@cnLineThicknessF     = 3
; 	cnres1@cnLineLabelFontHeightF=0.015
;   cnres1@cnLineLabelFormat ="3.3f"
; 	;cnres1@gsnSpreadColorStart = 1
; 	;cnres1@gsnSpreadColorStart = 17
; 	;cnres1@gsnSpreadColors     = True ; 6.1.0



; ; 填色
; cnres2                    = res
;   cnres2@cnFillOn           = True  ;cn means ContourPlot
;   cnres2@cnLinesOn          = False   
;   cnres2@cnInfoLabelOn        = False

;   ; ; 试一下取值范围
;   ; cmap  = read_colormap_file("BlAqGrWh2YeOrReVi22")
;   ; id=ispan(2, 18, 1)
;   ; cmap1= cmap(id,:)
;   ; colors=cmap1
;   ; cnres2@cnFillPalette       =colors
;   ; cnres2@cnLevelSelectionMode = "ManualLevels" 

;   cnres2@cnFillPalette        = "BlAqGrWh2YeOrReVi22"
;   cnres2@cnLevelSelectionMode = "ExplicitLevels"  
;   cnres2@cnLevels             = ispan(-10, 40, 10)
;   cnres2@cnFillColors         = (/2,3,4,6,12,16,17/)
;   cnres2@cnFillOpacityF       = 0.8

;   cnres2@lbLabelFontHeightF  = 0.02
;   cnres2@lbBoxLinesOn        = True ; Label bar
;   ; cnres2@lbLabelStride =2 ;每两个一个标签
;   ; cnres2@lbLabelAutoStride    = True               ; let NCL determine label spacing
;   ; cnres2@lbOrientation        = "Vertical"         ; vertical label bar
;   ; cnres2@pmLabelBarWidthF     = 0.05    
;   cnres2@pmLabelBarHeightF    = 0.1
;   cnres2@pmLabelBarOrthogonalPosF  = 0.1 ;色标离图的距离
;   cnres2@lbBoxEndCapStyle = "TriangleBothEnds"


; ;--------------矢量图--------------

; windRes = res
; ;windRes@vcGlyphStyle            = "FillArrow"   ; turn on curly vectors
; windRes@vcGlyphStyle    = "LineArrow"
; windRes@vcLineArrowThicknessF = 3
; windRes@vcMinDistanceF = 0.04
; windRes@vcRefMagnitudeF = 5.
; windRes@vcRefLengthF    = 0.02
; windRes@vcRefAnnoOn = True
; windRes@vcRefAnnoFontHeightF =0.015
; windRes@vcRefAnnoZone = 1
; windRes@vcRefAnnoSide = "Top"
; windRes@vcRefAnnoJust = "TopRight"
; windRes@vcRefAnnoString1 = "5 m/s"
; windRes@vcRefAnnoString2On = False
; windRes@vcLineArrowHeadMaxSizeF = 0.01
; windRes@vcLineArrowHeadMinSizeF = 0.01
; windRes@vcRefAnnoOrthogonalPosF=0
; windRes@vcRefAnnoPerimSpaceF=0.1
; windRes@vcRefAnnoArrowSpaceF=1


; ;绘图

; map = gsn_csm_map(wks, mpres)
; contour_avg = gsn_csm_contour(wks,z_need1, cnres1)
; ; windPlot = gsn_csm_vector(wks, u_avg , v_avg , windRes)


; ; overlay(map, windPlot)
; overlay(map, contour_avg)


; ; ; 读取并绘制风暴位置
; ; file_tc= asciiread("/mnt/f/snow_sts_data/TC/TC_dot_REOF.txt",-1,"string")
; ; lon_tc   = stringtofloat(str_get_field(file_tc(1:),3," "))
; ; lat_tc   = stringtofloat(str_get_field(file_tc(1:),4," "))
; ; type_tc  = str_get_field(file_tc(1:),7," ")

; ; tc_ind=str_match_ind(type_tc, tostring(typelabel))
; ; lon_dot=lon_tc(tc_ind)
; ; lat_dot=lat_tc(tc_ind)

; ; txres               = True                     ; text mods desired
; ; txres@txFontHeightF = 0.01                     ; font smaller. default big
; ; txres@txFontThicknessF=1.2
; ; txres@txFontColor="red"
; ; dum_tc = gsn_add_text(wks,map,"~F37~p",lon_dot,lat_dot,txres) 

; ;高原轮廓线
;   shpfile  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"
;   lnres                  = True     
;   lnres@gsLineColor      ="orange"
;   lnres@gsLineThicknessF = 6.0           ; 6x thickness  
;   shp_plot               = gsn_add_shapefile_polylines(wks,map,shpfile,lnres) 

; draw(map)
; frame(wks)

end