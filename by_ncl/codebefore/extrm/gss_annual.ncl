;极端降雪事件频次、极端降雪事件频次占风暴站点累计降雪日数比例的年变化
;-根据积雪
;纵向排列三条y轴
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
; https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
; ncl /mnt/f/snow_related/code/by_ncl/extrm/gss_annual.ncl

; xy_19.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/extrm/"
  file_dir1="/mnt/f/snow_sts_data/extrm_events/freq_annual.txt"
  f1       = asciiread(file_dir1,-1,"string")
  year    = stringtointeger(str_get_field(f1(1:),1," ")) 
  gss     = stringtofloat(str_get_field(f1(1:),2," ")) 
  ratio    = stringtofloat(str_get_field(f1(1:),3," "))
  ; gss     =where(gss.ne.0,ratio,ratio@_FillValue)
  ; ratio     =where(ratio.ne.0,ratio,ratio@_FillValue)
  ; gss@_FillValue=32700
  ; ratio@_FillValue=32700

  gss_rc =  regline_stats(year,gss) ; linear regression coef
  npts    = dimsizes(gss)
  gss_arry = new ( (/2,npts/), float)
  gss_arry(0,:) = gss                                 ; use markers
  gss_arry(1,:) = gss_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  gss_pr     = rtest(gss_rc@bstd(1), gss_rc@N, 0)    ; ===> pr=0.041
  print(gss_rc@b(1))
  if (gss_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if

  ratio_rc =  regline_stats(year,ratio) ; linear regression coef
  ratio_arry = new ( (/2,npts/), float)
  ratio_arry(0,:) = ratio                                 ; use markers
  ratio_arry(1,:) = ratio_rc@Yest
  ;显著性检验
  ratio_pr     = rtest(ratio_rc@bstd(1), ratio_rc@N, 0)    ; ===> pr=0.041
  print(ratio_rc@b(1))
  if (ratio_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if


;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("ps", pic_dir+"gss_annual" ) 


gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/2,3/)

plotxy =new(2, graphic)


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
  ; res@xyLineThicknesses =5
  res@xyLineThicknesses =(/5,4/) ;画两条线 
  res@xyDashPatterns= 0            ; solid line
  res@tiYAxisFont =22


  res13=res
  res13@tmYROn      = False

  res24=res
  ; res24@tmYUseLeft=False ;这个不是必要的
  res24@tiYAxisSide="right"
  res24@tmXTOn               = False
  res24@tmYLOn               = False
  res24@tmYLLabelsOn         = False
  res24@tmYRLabelsOn         = True


  ;分别复制上述共用参数，绘制每个图形
  res1=res13
  res2=res24
  res3=res13

  res1@xyLineColor=colors(0) 
  res1@tiYAxisFontColor=colors(0)
  res1@trYMaxF =max(gss)+1
  res1@tiYAxisString = "Events" ; y-axis label

  plotxy(0)=gsn_csm_xy(wks,year,gss_arry,res1)

  res2@xyLineColor=colors(1) 
  res2@tiYAxisFontColor=colors(1)
  res2@trYMaxF =max(ratio)+0.2
  res2@tiYAxisString = "Ratio" ; y-axis label

  plotxy(1)=gsn_csm_xy(wks,year,ratio_arry,res2)


  ;堆叠
  attachres1=True
  attachres1@gsnAttachBorderOn =False
  attachres2=True
  attachres2@gsnAttachPlotsXAxis =True 

attachid1=gsn_attach_plots(plotxy(0), plotxy(1), attachres1, attachres2)

draw(plotxy(0))
frame(wks)

; (0)     -0.03180113
; (0)     NOT significant
; (0)     -1.127674
; (0)     significant
; (0)     -0.0002025463
; (0)     NOT significant

end
 


 

