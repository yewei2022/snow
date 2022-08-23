;单层水汽通量图  
;join或者cat数据后，hgt u v 需要循环读入数据uv数据读出来才是对的
;; snow 118  extrm 64
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "/mnt/h/d/ncl_related/code/shapefile_utils.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/plot_qu_qv.ncl

begin

type="4"
pth="snow"
pic_dir ="/mnt/f/snow_related/pic/CTC/500hPa/"+pth +"_mydown/"
data_dir="/mnt/f/snow_sts_data/ERA5/"+pth +"_mydown/"

date_dir ="/mnt/f/snow_sts_data/CTC/"+pth +"/"+pth+"_CTC_mydown.txt"
datefile = asciiread(date_dir,-1,"string")
label    = str_get_field(datefile(1:),2," ") 
  
u_files = systemfunc("ls "+data_dir+"u/u_component_of_wind_*.nc")
u_f     = addfiles(u_files,"r") 
ListSetType(u_f,"join")
v_files = systemfunc("ls "+data_dir+"v/v_component_of_wind_*.nc")
v_f     = addfiles(v_files,"r") 
ListSetType(v_f,"join")
q_files = systemfunc("ls "+data_dir+"q/Specific_humidity_*.nc")
q_f     = addfiles(q_files,"r") 
ListSetType(q_f,"join")

samps=118
u1    = new((/samps,201,321/), float)
v1    = new((/samps,201,321/), float)

q0 =q_f[:]->q
q1  = short2flt(q0(:,12,{500},{0:50},{50:130}))


;法一 hgt u1 v1 循环读取 才正确
do i =0,samps-1
    u1(i,:,:)  = short2flt(u_f[:]->u(i,12,{500},{0:50},{50:130}))
    v1(i,:,:)  = short2flt(v_f[:]->v(i,12,{500},{0:50},{50:130}))
end do

;基本处理
q1=q1*1000
qu1= q1*u1/9.8
qv1= q1*v1/9.8
copy_VarCoords(q1,qu1)
copy_VarCoords(q1,qv1)

type_ind=str_match_ind(label, type)
qu_need  =qu1(type_ind,:,:)
qv_need  =qv1(type_ind,:,:)

dim=dimsizes(qu_need)

qu_need!0 = "time"
qv_need!0 = "time"


qu_avg  =dim_avg_n_Wrap(qu_need, 0)
qv_avg  =dim_avg_n_Wrap(qv_need, 0)

mm=sqrt(qu_avg^2+qv_avg^2) ;水汽通量大小
copy_VarCoords(qu_avg,mm)

vapdiv=uv2dvF_Wrap(qu_avg, qv_avg) ;为什么这两个函数算出来完全相反
vapdiv=vapdiv*1.e6

; ;mask掉高原以外的vapdiv
  shp_filename  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp" 
  vapdiv_mask =new(dimsizes(vapdiv),typeof(vapdiv),vapdiv@_FillValue)
  vapdiv_mask =shapefile_mask_data(vapdiv,shp_filename,True) 

wks = gsn_open_wks("x11", pic_dir+"vap_P"+type)

res = True
res@gsnDraw = False
res@gsnFrame = False
; res@gsnMaximize=True
res@gsnLeftString =""
res@gsnRightString = ""
res@tmYROn=False
res@tmXTOn=False
res@tmBorderThicknessF  =2.5    ; border 6x as thick,图框粗细
res@tmXBMajorThicknessF =2.5
res@tmXBMinorThicknessF =2.5
res@tmYLMajorThicknessF =2.5 
res@tmYLMinorThicknessF =2.5  

; ;坐标轴标签大小
; res@tmEqualizeXYSizes   =True 
; ; 现在一个坐标轴设置好后，
; ;(tmXBLabelFontHeightF,(tmXBMajorLengthF,(tmXBMinorLengthF
; ; 其他坐标轴就不用重复设置了
; res@tmXBLabelFontHeightF = 0.02 ; x轴标签字号

;设置地图
mpres = res
mpres@mpFillOn                = False
mpres@mpMinLatF               = 5.
mpres@mpMaxLatF               = 45.
mpres@mpMinLonF               = 65.
mpres@mpMaxLonF               = 110.
mpres@gsnMajorLatSpacing    =10. 
mpres@gsnMinorLatSpacing    =5
mpres@gsnMajorLonSpacing    =10 
mpres@gsnMinorLonSpacing    =5   
mpres@mpDataSetName              = "/mnt/h/d/ChinaMap/Earth..4"
mpres@mpDataBaseVersion          = "MediumRes"
mpres@mpOutlineSpecifiers        = (/"China","China:Provinces"/)


;--------------风矢量图--------------
windRes = res
windRes@gsnLeftString ="P"+type
windRes@gsnLeftStringFontHeightF=0.024
windRes@gsnLeftStringOrthogonalPosF=0.015
windRes@vcGlyphStyle    = "LineArrow"
windRes@vcLineArrowThicknessF = 2.5
windRes@vcMinDistanceF = 0.03
windRes@vcRefMagnitudeF = 2.
windRes@vcRefLengthF    = 0.02
windRes@vcRefAnnoOn = True
windRes@vcRefAnnoFontHeightF =0.015
windRes@vcRefAnnoZone = 1
windRes@vcRefAnnoSide = "Top"
windRes@vcRefAnnoJust = "TopRight"
windRes@vcRefAnnoString1 = "2"
windRes@vcRefAnnoString2On = False
windRes@vcLineArrowHeadMaxSizeF = 0.01
windRes@vcLineArrowHeadMinSizeF = 0.01


;填色-----------------------------------------
  cnres=res
  cnres@cnFillOn        = True                    ; turn on color
  cnres@cnLinesOn       = False                   ; turn off contour lines
  cnres@cnLineLabelsOn  = False                   ; tuen off line labels
  cnres@cnInfoLabelOn   = False 

  ; cnres@cnLevelSelectionMode  ="ExplicitLevels" 
  ; cnres@cnFillPalette       = "perc2_9lev"  ;水汽通量填色
  ; cnres@cnLevels              =fspan(2, 6, 9)
  ; cnres@cnFillColors          =(/-1,1,2,3,4,5,6,7,8,9/)

  cnres@cnFillPalette       = "BlueWhiteOrangeRed"  ;水汽通量散度填色BlueRed
  cnres@cnLevelSelectionMode = "ManualLevels" 
  cnres@cnMinLevelValF = -4
  cnres@cnMaxLevelValF = 4
  cnres@cnLevelSpacingF= 0.5

  cnres@pmLabelBarHeightF     = 0.08
  cnres@lbLabelStride         = 2         ; 两个level只标一个标签
  ; cnres@lbLabelAutoStride   = True            ; let NCL determine label spacing
  cnres@lbBoxLinesOn          = True ; 色标之间分界线
  cnres@lbBoxEndCapStyle      = "TriangleBothEnds"
  cnres@lbLabelFontHeightF    = 0.02 
  cnres@pmLabelBarOrthogonalPosF = 0.1;色标条的位置


;绘图
map = gsn_csm_map(wks, mpres)

plot_wind = gsn_csm_vector(wks, qu_avg, qv_avg, windRes)
plot_cn = gsn_csm_contour(wks, vapdiv_mask, cnres)

overlay(map, plot_cn)
overlay(map, plot_wind)

;高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)
end