;--------------------------------------------------------------------
; wavelet_3.ncl
;
; Concepts illustrated:
;   - Computing wavelets
;   - Overlaying a stipple pattern to show area of interest
;   - Overlaying a hatch pattern to show area of interest
;   - Changing the size of the dot fill pattern in gsn_contour_shade
;   - Increasing the density of fill patterns

;  ncl /mnt/f/snow_related/code/by_ncl/TC/wavelet.ncl

;--------------------------------------------------------------------
;
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"



;--------------------------------------------------------------------
; CREATE SAME WAVELET FIGURE AS TORRENCE & COMPO using seasonal Nino3
; from 1871-1997
;--------------------------------------------------------------------

begin

  pic_dir ="/mnt/f/snow_related/pic/TC/"

  file_dir1="/mnt/f/snow_sts_data/TC/TC_annual.txt"
  f1       = asciiread(file_dir1,-1,"string")
  timeo    = stringtofloat(str_get_field(f1(1:),1," ")) 
  TC_num   = stringtofloat(str_get_field(f1(1:),2," ")) 

  TC_num!0 = "time"
  TC_num&time = timeo
  time  = timeo
  N     = dimsizes(time)
;************************************
; compute wavelet
;************************************
  mother  = 0
  param   = 6.0
  dt      = 1    ;timesteps in units of years
  s0      = dt
  dj      = 0.25
  jtot    = 1+floattointeger(((log10(N*dt/s0))/dj)/log10(2.))
  npad    = N
  nadof   = 0
  noise   = 1
  siglvl  = .05
  isigtest= 0

  w = wavelet(TC_num,mother,dt,param,s0,dj,jtot,npad,noise,isigtest,siglvl,nadof)
;************************************
; create coodinate arrays for plot
;************************************
  power            = onedtond(w@power,(/jtot,N/))
  power!0          = "period"                        ; Y axis
  power&period     = w@period                      ; convert period to units of years

  power!1          = "time"                          ; X axis
  power&time       = time

  power@long_name  = "Power Spectrum"
  power@units      = "1/unit-freq"

; compute significance ( >= 1 is significant)
  SIG              = power                            ; transfer meta data
  SIG              = power/conform (power,w@signif,0)
  SIG@long_name    = "Significance"
  SIG@units        = " "

  var=dim_sum_n_Wrap(power, 1)
  print(w@period)
  print(var)

;********************************************************************************
; initial resource settings
;********************************************************************************
  wks = gsn_open_wks("eps",pic_dir+"wavelet2")             ; send graphics to PNG file

  res                     = True                  ; plot mods desired
  res@gsnMaximize         = True
  res@gsnDraw             = False                 ; Do not draw plot
  res@gsnFrame            = False                 ; Do not advance frome
  res@tmXTOn  =False
  res@tmEqualizeXYSizes     =True
  res@tmXBLabelFontHeightF  =0.018
  res@tiYAxisFontHeightF   = 0.018
  res@gsnStringFontHeightF = 0.015
  res@vpHeightF           = .4                    ;
  res@vpWidthF            = .7
  res@trYReverse          = True                  ; reverse y-axis
  res@tmXBLabelAngleF     = 45.   ;

  ; res@gsnYAxisIrregular2Linear = True    ;3.Log Convert Y axis to logarithmic;Linear 
yval=ispan(0, 14, 2)
  res@tmYLMode            = "Explicit"
  res@tmYLValues          = yval
  res@tmYLLabels          = "" + res@tmYLValues
  ; res1@tmLabelAutoStride   = True


  res1=res
  res1@cnFillOn            = True                  ; turn on color
  res1@cnFillPalette       = "temp_19lev"           ; set color map
  ; res1@cnFillMode          = "RasterFill"          ; turn on raster mode
  ; res1@cnFillOpacityF      = 0.50                  ; make partially transparent
  res1@cnRasterSmoothingOn = True                  ; turn on raster smoothing
  res1@cnLinesOn           = False                 ; turn off contour lines
  res1@cnLineLabelsOn      = False
  res1@cnInfoLabelOn       = False
  res1@pmLabelBarHeightF   = 0.08
  res1@lbBoxEndCapStyle    = "TriangleBothEnds"
  res1@cnLineLabelFormat   ="0@;*.2f"
  res1@lbLabelFontHeightF  =0.018
  res1@cnFillDrawOrder     ="PreDraw"

  res1@cnLevelSelectionMode = "ExplicitLevels"       ; set manual contour levels
  res1@cnLevels             = (/0.5,1,2,4/)
  res1@cnFillColors         =(/-1,11,12,14,15/)

  res1@gsnLeftString        = ""
  ; res1@gsnLeftStringOrthogonalPosF=0.03
  res1@gsnRightString       =""
  res1@tiYAxisString        = "Period(a)"
  res1@tmYROn               =False
  res1@tmYLOn               =True

  res2 = res                            ; res2 probability plots
  res2@cnLevelSelectionMode = "ManualLevels" ; set manual contour levels
  res2@cnMinLevelValF      = 1.00        ; set min contour level
  ; res2@cnMaxLevelValF      = 2.00        ; set max contour level
  ; res2@cnLevelSpacingF     = 1.00        ; set contour spacing
  res2@cnInfoLabelOn       = False
  res2@cnLinesOn           = False       ; do not draw contour lines
  res2@cnLineLabelsOn      = False       ; do not draw contour labels
  res2@gsnLeftString       = ""
  res2@gsnRightString      = ""



; 绘图 wavelet1
  ; plot_hatch_def = gsn_csm_contour(wks,power({1:15},:),res1)

  ; iplot_hatch_def = gsn_csm_contour(wks,SIG({1:15},:),res2)

  ; opt                      = True
  ; opt@gsnShadeHigh         = 17           ; cross hatch pattern
  ; opt@gsnShadeFillType     = "pattern"
  ; opt@gsnShadeFillScaleF   = 1         ; add extra density
  ; opt@gsnShadeFillDotSizeF = 0.006      ; make dots larger
  ; iplot_hatch_def = gsn_contour_shade(iplot_hatch_def,0, 1, opt)

  ; overlay(plot_hatch_def,iplot_hatch_def)

  ; draw(plot_hatch_def)
  ; polyres                  = True
  ; polyres@gsLineThicknessF = 4.0
  ; polyres@gsLineColor      ="black"
  ; polyres@gsLineDashPattern=0
  ; gsn_polyline(wks,plot_hatch_def,timeo,w@coi,polyres) ; add polyline
  ; frame(wks)



; 绘图 wavelet2

  gsn_define_colormap(wks, "temp_19lev")       ; send graphics to PNG file
  color3=(/17/)
  res3   = True
  res3@gsnMaximize = True
  res3@gsnDraw  = False
  res3@gsnFrame = False
  res3@vpHeightF  = 0.4        ; Changes the aspect ratio
  res3@vpWidthF   = 0.7
  res3@tmXTOn      = False ;关刻度
  res3@tmYROn      = False
  res3@tmXBMode="Manual"   
  res3@tmXBTickSpacingF=4
  ; res3@tmXBMinorPerMajor=4 
  res3@trXMinF   = 1       
  res3@trXMaxF   = 15  
  res3@trYMaxF   =140    
  res3@tiYAxisString = "Variance" ; y-axis label
  res3@tiXAxisString = "Time scale (a)" ; y-axis label
  res3@xyDashPattern  = 0                         ; Make curves all solid
  res3@xyLineThicknessF= 4
  res3@xyLineColor=color3
  res3@xyMarkLineMode = "Lines"               ; Markers *and* lines
  plotxy=gsn_csm_xy(wks,w@period,var,res3)
  draw(plotxy)
  frame(wks)

end