;绘制站点累计高原总降雪日数、风暴影响下累计降雪日数
;高原总体累计大雪日数  风暴影响下累计大雪日数
;纵向排列4条y轴
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/snow_all/snow_heavysnow_annual.ncl

; xy_19.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

  pic_dir ="/mnt/f/snow_related/pic/snow_all/"

  file_dir1="/mnt/f/snow_sts_data/1981-2020/heavysnow_annual_all.txt"
  f1       = asciiread(file_dir1,-1,"string")
  year     = stringtointeger(str_get_field(f1(1:),1," ")) 
  snow_all = stringtofloat(str_get_field(f1(1:),3," ")) 

  snow_all_rc =  regline_stats(year,snow_all) ; linear regression coef
  npts    = dimsizes(snow_all)
  snow_all_arry = new ( (/2,npts/), float)
  snow_all_arry(0,:) = snow_all                                 ; use markers
  snow_all_arry(1,:) = snow_all_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  snow_all_pr     = rtest(snow_all_rc@bstd(1), snow_all_rc@N, 0)    ; ===> pr=0.041
  if (snow_all_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if
  print("总降雪日数"+snow_all_rc@b(1))

  heavysnow_all  = stringtofloat(str_get_field(f1(1:),2," "))

  heavysnow_all_rc =  regline_stats(year,heavysnow_all) ; linear regression coef
  heavysnow_all_arry = new ( (/2,npts/), float)
  heavysnow_all_arry(0,:) = heavysnow_all                                 ; use markers
  heavysnow_all_arry(1,:) = heavysnow_all_rc@Yest
  ;显著性检验
  heavysnow_all_pr     = rtest(heavysnow_all_rc@bstd(1), heavysnow_all_rc@N, 0)    ; ===> pr=0.041
  if (heavysnow_all_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if 
  print("总大雪日数"+heavysnow_all_rc@b(1))


  file_dir2="/mnt/f/snow_sts_data/1981-2020/heavysnow_annual.txt"
  f2      = asciiread(file_dir2,-1,"string")
  snow     = stringtofloat(str_get_field(f2(1:),3," "))

  snow_rc =  regline_stats(year,snow) ; linear regression coef
  snow_arry = new ( (/2,npts/), float)
  snow_arry(0,:) = snow                                 ; use markers
  snow_arry(1,:) = snow_rc@Yest
  ;显著性检验
  snow_pr     = rtest(snow_rc@bstd(1), snow_rc@N, 0)    ; ===> pr=0.041
  if (snow_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if 
  print("风暴降雪日数"+snow_rc@b(1))

  heavy_snow      = stringtofloat(str_get_field(f2(1:),2," "))

  heavy_snow_rc =  regline_stats(year,heavy_snow) ; linear regression coef
  heavy_snow_arry = new ( (/2,npts/), float)
  heavy_snow_arry(0,:) = heavy_snow                                 ; use markers
  heavy_snow_arry(1,:) = heavy_snow_rc@Yest
  ;显著性检验
  heavy_snow_pr     = rtest(heavy_snow_rc@bstd(1), heavy_snow_rc@N, 0)    ; ===> pr=0.041
  if (heavy_snow_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if
  print("风暴大雪日数"+heavy_snow_rc@b(1)) 

; print(snow_all)
; print(alldays)

;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+"snow_heavysnow_annual" ) 
plotxy =new(4, graphic)

  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/5,7/)
  lineDashPattern=(/0,2/)
  snow_max=max(snow)
  snow_all_max=max(snow_all)
  heavy_snow_max=max(heavy_snow)
  heavysnow_all_max=max(heavysnow_all)

  ;四幅图的共同参数
  res   = True
  res@gsnMaximize = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.1        ; Changes the aspect ratio
  res@vpWidthF   = 0.3
  res@tmXTOn      = False ;关刻度
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode="Manual"   
  res@tmXBTickSpacingF=5
  res@tmXBMinorPerMajor=4 
  res@trXMinF   = 1980       
  res@trXMaxF   = 2021      
  res@xyLineThicknesses =(/5,4/) ;画两条线 
  res@tiYAxisFont =22


  res13=res
  res13@tmYROn      = False
  res13@xyDashPattern=lineDashPattern(0)
  res13@tiYAxisString = "SF" ; y-axis label


  res24=res
  ; res24@tmYUseLeft=False ;这个不是必要的
  res24@tiYAxisSide="right"
  res24@tmXTOn               = False
  res24@tmYLOn               = False
  res24@tmYLLabelsOn         = False
  res24@tmYRLabelsOn         = True
  res24@xyDashPattern=lineDashPattern(1) ;虚线
  res24@tiYAxisString = "HSF" ; y-axis label



  ;分别复制上述共用参数，绘制每个图形
  res1=res13
  res2=res24
  res3=res13
  res4=res24

  res1@xyLineColor=colors(0) ;蓝色，TC影响
  res1@tiYAxisFontColor=colors(0)
  res1@trYMaxF =snow_all_max+1
  plotxy(0)=gsn_csm_xy(wks,year,snow_all_arry,res1)

  res2@xyLineColor=colors(0) ;蓝色，TC影响
  res2@tiYAxisFontColor=colors(0)
  res2@trYMaxF =heavysnow_all_max
  plotxy(1)=gsn_csm_xy(wks,year,heavysnow_all_arry,res2)

  res3@xyLineColor=colors(1) ;蓝色，TC影响
  res3@tiYAxisFontColor=colors(1)
  res3@trYMaxF =snow_max+1
  res3@trYMinF =min(snow)
  plotxy(2)=gsn_csm_xy(wks,year,snow_arry,res3)

  res4@xyLineColor =colors(1) ;绿色，影响
  res4@tiYAxisFontColor=colors(1)
  res4@trYMaxF =heavy_snow_max+0.1
  plotxy(3)=gsn_csm_xy(wks,year,heavy_snow_arry,res4)

  ;堆叠
  attachres1=True
  attachres1@gsnAttachBorderOn =False
  attachres2=True
  attachres2@gsnAttachPlotsXAxis =True 

attachid1=gsn_attach_plots(plotxy(0), plotxy(1:3), attachres1, attachres2)

draw(plotxy(0))
frame(wks)

; (0)     significant
; (0)     总降雪日数-120.079
; (0)     significant
; (0)     总大雪日数-1.66848
; (0)     NOT significant
; (0)     风暴降雪日数-0.508443
; (0)     NOT significant
; (0)     风暴大雪日数-0.0250469
end
 


 

