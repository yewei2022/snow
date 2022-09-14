;不画水汽通量图 根据分类结果，绘制各类的u，v，且位势高度 填色
;join或者cat数据后，hgt u v 需要循环读入数据uv数据读出来才是对的
;; snow 118  extrm 64
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/plot_uvgeo_mydown3.ncl


begin

type="4"
; type_revise="2"
pth="snow"
pic_dir ="/mnt/f/snow_related/pic/CTC/500hPa/"+pth +"_mydown/"
data_dir="/mnt/f/snow_sts_data/ERA5/"+pth +"_mydown/"

date_dir ="/mnt/f/snow_sts_data/CTC/"+pth +"/"+pth+"_CTC_mydown.txt"
datefile = asciiread(date_dir,-1,"string")
label    = str_get_field(datefile(1:),2," ") 
  

hgt_files = systemfunc("ls "+data_dir+"geopotential/geopotential_*.nc")
hgt_f = addfiles(hgt_files,"r") 
ListSetType(hgt_f,"join")
u_files = systemfunc("ls "+data_dir+"u/u_component_of_wind_*.nc")
u_f     = addfiles(u_files,"r") 
ListSetType(u_f,"join")
v_files = systemfunc("ls "+data_dir+"v/v_component_of_wind_*.nc")
v_f     = addfiles(v_files,"r") 
ListSetType(v_f,"join")

samps=118
hgt1  = new((/samps,201,321/), float)
u1    = new((/samps,201,321/), float)
v1    = new((/samps,201,321/), float)

;法一 hgt u1 v1 循环读取 才正确 读数据时经纬度范围随意 画图时调整显示范围即可
do i =0,samps-1
    hgt1(i,:,:)= short2flt(hgt_f[:]->z(i,12,{500},{0:50},{50:130}))
    u1(i,:,:)  = short2flt(u_f[:]->u(i,12,{500},{0:50},{50:130}))
    v1(i,:,:)  = short2flt(v_f[:]->v(i,12,{500},{0:50},{50:130}))
end do

;基本处理
hgt1      = hgt1/9.8


type_ind=str_match_ind(label, type)
hgt_need=hgt1(type_ind,:,:)
u_need  =u1(type_ind,:,:)
v_need  =v1(type_ind,:,:)

dim=dimsizes(hgt_need)
per=tofloat(dim(0))/tofloat(samps)
per=per-0.001 ;为了使四舍五入后总和为1
print(per)
performat=sprintf("%2.0f",per*100.) ;四舍五入
per_str=tostring(performat)

hgt_need!0 = "time"
u_need!0 = "time"
v_need!0 = "time"


hgt_avg=dim_avg_n_Wrap(hgt_need, 0)
u_avg  =dim_avg_n_Wrap(u_need, 0)
v_avg  =dim_avg_n_Wrap(v_need, 0)


wks = gsn_open_wks("eps", pic_dir+"P"+type+"_"+pth+"_mydown")

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
windRes@gsnLeftString ="P"+type+"("+per_str+"%)"
; windRes@gsnLeftString ="Type"+type_revise+"("+per_str+"%)"

windRes@gsnLeftStringFontHeightF=0.024
windRes@gsnLeftStringOrthogonalPosF=0.015
windRes@vcGlyphStyle    = "FillArrow"
windRes@vcLineArrowThicknessF = 2.5
windRes@vcMinDistanceF = 0.03
windRes@vcRefMagnitudeF = 10.
windRes@vcRefLengthF    = 0.02
windRes@vcRefAnnoOn = True
windRes@vcRefAnnoFontHeightF =0.015
windRes@vcRefAnnoZone = 1
windRes@vcRefAnnoSide = "Top"
windRes@vcRefAnnoJust = "TopRight"
windRes@vcRefAnnoString1 = "10 m/s"
windRes@vcRefAnnoString2On = False
windRes@vcLineArrowHeadMaxSizeF = 0.01
windRes@vcLineArrowHeadMinSizeF = 0.01

;--------------叠加高度场--------------
hgtRes = res
hgtRes@cnFillOn  = False  ;cn means ContourPlot
hgtRes@cnLinesOn = True   
;hgtRes@cnMonoLineColor = False
hgtRes@cnLineColor="blue"
hgtRes@cnLineLabelsOn = True  
hgtRes@cnLineLabelFontHeightF=0.015
hgtRes@cnInfoLabelOn  = False ; set false will not set an information label
hgtRes@cnLineThicknessF = 4
; hgtRes@cnLevelSelectionMode = "ManualLevels" 
; hgtRes@cnMinLevelValF = 5520
; hgtRes@cnMaxLevelValF = 5920
hgtRes@cnLevelSpacingF  = 20
hgtRes@cnLineLabelDensityF=0.5

;--------------加粗588线--------------
hgt588Res = res
hgt588Res@cnFillOn  = False  ;cn means ContourPlot
hgt588Res@cnLinesOn = True   
; hgt588Res@cnMonoLineColor = False
hgt588Res@cnLineColor="red4"
hgt588Res@cnLineLabelsOn = True  
hgt588Res@cnLineLabelFontHeightF=0.015
hgt588Res@cnInfoLabelOn  = False ; set false will not set an information label
hgt588Res@cnLineThicknessF = 5
hgt588Res@cnLevelSelectionMode = "ExplicitLevels" 
hgt588Res@cnLevels=(/5880/)
hgt588Res@cnLineLabelsOn=False

  ;填色-----------------------------------------
  cnres=res
  cnres@cnFillOn        = True                    ; turn on color
  cnres@cnLinesOn       = True                   ; turn off contour lines
  cnres@cnLineLabelsOn  = False                   ; tuen off line labels
  cnres@cnInfoLabelOn   = False 
  cnres@cnLineColor="white"

  ; ;填色
  cnres@cnFillPalette       = "temp_19lev"  
  ; cnres@cnLevelSelectionMode  ="ExplicitLevels" 
  ; cnres@cnLevels              = ispan(5640, 5920, 20)
  ; cnres@cnFillColors          =(/-1,1,2,3,4,5,6,7,8,9/)
  cnres@cnFillOpacityF      = 0.80                  ; make partially transparent

  cnres@cnLevelSelectionMode = "ManualLevels" 
  cnres@cnMinLevelValF = 5640
  cnres@cnMaxLevelValF = 5880
  cnres@cnLevelSpacingF= 20

  cnres@pmLabelBarHeightF     = 0.08
  cnres@lbLabelStride         = 2         ; 两个level只标一个标签
  ; cnres@lbLabelAutoStride   = True            ; let NCL determine label spacing
  cnres@lbBoxLinesOn          = True ; 色标之间分界线
  cnres@lbBoxEndCapStyle      = "TriangleBothEnds"
  cnres@lbLabelFontHeightF    = 0.02 
  cnres@pmLabelBarOrthogonalPosF = 0.1;色标条的位置


;绘图
map = gsn_csm_map(wks, mpres)

plot_wind = gsn_csm_vector(wks, u_avg, v_avg, windRes)
plot_hgt = gsn_csm_contour(wks,hgt_avg, cnres)
; plot_hgt588 = gsn_csm_contour(wks,hgt_avg, hgt588Res)

overlay(map, plot_hgt)
overlay(map, plot_wind)

; overlay(map, plot_hgt588)

; 读取并绘制风暴位置
file_tc= asciiread("/mnt/f/snow_sts_data/TC/TC_dot_CTC.txt",-1,"string")
lon_tc   = stringtofloat(str_get_field(file_tc(1:),3," "))
lat_tc   = stringtofloat(str_get_field(file_tc(1:),4," "))
type_tc  = str_get_field(file_tc(1:),6," ")

tc_ind=str_match_ind(type_tc, type)
lon_dot=lon_tc(tc_ind)
lat_dot=lat_tc(tc_ind)

txres               = True                     ; text mods desired
txres@txFontHeightF = 0.01                     ; font smaller. default big
txres@txFontThicknessF=1.2
txres@txFontColor="blue"
dum_tc = gsn_add_text(wks,map,"~F37~p",lon_dot,lat_dot,txres) 

;高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)
end