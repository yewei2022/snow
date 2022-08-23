;结合了days_pre_gss_annual.ncl
;绘制总降雪日数，降水量、gss年变化 标准化距平 原始数据的xy折线 线性趋势图
; bar4.ncl
; These files are loaded by default in NCL V6.2.0 and newer
;  ncl /mnt/f/snow_related/code/by_ncl/snow_all/stddev_snow_annual.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_all/stddev/"

count=0
pic_name=(/"days","dailypre","gssinc","gss"/)
ymin=(/-3,-2,-2,-2/)
ymax=(/3.2,4,4,6.5/)
axis_name=(/"SF","PA(mm)","SDI(cm)","SD(cm)"/)
ymax_delta=(/1200,0.2,0.05,0.5/) ;用于折线图
ymin_delta=(/1200,0.2,0.05,0.5/) ;用于折线图


  file_dir="/mnt/f/snow_sts_data/1981-2020/days_pre_gss_annual_all.txt"
  f1       = asciiread(file_dir,-1,"string")
  year    = stringtointeger(str_get_field(f1(1:),1," "))
  var     = stringtofloat(str_get_field(f1(1:),count+2," "))
  std_anoma_var = dim_standardize_n(var, 1, 0)

  var_rc =  regline_stats(year,var) ; linear regression coef
  npts    = dimsizes(var)
  var_arry = new ( (/2,npts/), float)
  var_arry(0,:) = var                                 ; use markers
  var_arry(1,:) = var_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  var_pr     = rtest(var_rc@bstd(1), var_rc@N, 0)    ; ===> pr=0.041
  if (var_pr.lt.siglvl) then
      if_sig="Sig."
  else
      if_sig="Insig."
  end if
  print("回归系数"+var_rc@b(1))

printMinMax(var, 0)

;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("x11", pic_dir+pic_name(count)+"_all") 
  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/5,13/)

  res   = True
  res@gsnScale = True 
  res@gsnMaximize = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.43        ; Changes the aspect ratio
  res@vpWidthF   = 0.85
  res@tmXTOn      = False ;关刻度
  res@tmXBLabelAngleF     = 45.   ;
  ; res@tmXBLabelStride =2 
  res@tmXBMode="Manual"   
  res@tmXBTickSpacingF=5
  res@tmXBMinorPerMajor=4     
  res@trXMinF   = 1980        ; min value on y-axis
  res@tiXAxisString = ""      


  resbar=res 
  resbar@tmYROn      = False  
  resbar@gsnXYBarChart         = True            ; create bar chart 
  resbar@gsnYRefLine           = 0.              ; reference line 
  resbar@gsnAboveYRefLineColor = colors(1)          ; above ref line fill red
  resbar@gsnBelowYRefLineColor = colors(0)           ; below ref line fill blue

  resbar@trYMinF   = ymin(count)        ; min value on y-axis
  resbar@trYMaxF   = ymax(count)      ; max value on y-axis
  resbar@tiYAxisString = "Standardized anomaly"
  ; resbar@xyLineColors=(/"red","blue"/) ;bar的轮廓线颜色

; ;绘图
; plot = gsn_csm_xy (wks,year,std_anoma_var,resbar)

;**********************************************************************
; polyres                  = True
; polyres@gsLineThicknessF = 3.0
; polyres@gsLineColor="black"
; polyres@gsLineDashPattern=2
; gsn_polyline(wks,plot,year,std_anoma_var_arry(1,:),polyres) ; add polyline
;**********************************************************************
;以上弃用原因：线在bar之下，无法调节

resline                   = res
b1=sprintf("%.3f",var_rc@b(1))
b0=sprintf("%.3f",var_rc@b(0))
space=(/"+","","",""/)
resline@gsnLeftString="y="+tostring(b1)+"x"+space(count)+tostring(b0)+""
resline@gsnLeftStringOrthogonalPosF=-0.1
resline@gsnLeftStringParallelPosF=0.05
resline@gsnRightString=if_sig
resline@gsnRightStringOrthogonalPosF=-0.1
resline@gsnRightStringParallelPosF=0.98
; resline@tiYAxisFont =22
resline@xyLineThicknesses = (/4,5/) 
resline@tiYAxisSide="right"
resline@trYMinF     = min(var)-ymin_delta(count)     
resline@trYMaxF =max(var)+ymax_delta(count)
resline@tmYLOn               = False
resline@tmYLLabelsOn         = False
resline@tmYRLabelsOn         = True
; resline@xyDashPattern=lineDashPattern(1) 
resline@tiYAxisString = axis_name(count) ; y-axis label

plot=gsn_csm_xy2(wks, year, std_anoma_var, var_arry, resbar, resline)

; plot_line=gsn_csm_xy(wks, year, var_arry, polyres)
; overlay(plot, plot_line)


draw(plot)
frame(wks)

end
 


 

