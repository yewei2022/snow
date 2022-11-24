; 影响高原的TC个数，影响个数占总个数比例年变化，wind不画
;纵向排列2条y轴
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/TC/TC_annual.ncl

; xy_19.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

  pic_dir ="/mnt/f/snow_related/pic/TC/"

  file_dir1="/mnt/f/snow_sts_data/TC/TC_annual.txt"
  f1       = asciiread(file_dir1,-1,"string")
  year     = stringtointeger(str_get_field(f1(1:),1," ")) 
  TC_num   = stringtofloat(str_get_field(f1(1:),2," ")) 

  TC_num_rc =  regline_stats(year,TC_num) ; linear regression coef
  npts    = dimsizes(TC_num)
  TC_num_arry = new ( (/2,npts/), float)
  TC_num_arry(0,:) = TC_num                                 ; use markers
  TC_num_arry(1,:) = TC_num_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  TC_num_pr     = rtest(TC_num_rc@bstd(1), TC_num_rc@N, 0)    ; ===> pr=0.041
  if (TC_num_pr.lt.siglvl) then
      TC_num_sig="Sig."
  else
      TC_num_sig="Insig."
  end if

  rate     = stringtofloat(str_get_field(f1(1:),5," "))

  rate_rc =  regline_stats(year,rate) ; linear regression coef
  rate_arry = new ( (/2,npts/), float)
  rate_arry(0,:) = rate                                 ; use markers
  rate_arry(1,:) = rate_rc@Yest
  ;显著性检验
  rate_pr     = rtest(rate_rc@bstd(1), rate_rc@N, 0)    ; ===> pr=0.041
  if (rate_pr.lt.siglvl) then
      rate_sig="Sig."
  else
      rate_sig="Insig."
  end if 


;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+"TC_annual" ) 
plotxy =new(3, graphic)

  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/4,7,13/)
  ; lineDashPattern=(/0,0,0/)

  ;四幅图的共同参数
  res   = True
  res@gsnMaximize = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF           = .2                    ;
  res@vpWidthF            = .5
  res@tmXTOn      = False ;关刻度
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode="Manual"   
  res@tmXBTickSpacingF=5
  res@tmXBMinorPerMajor=4 
  res@trXMinF   = 1980       
  res@trXMaxF   = 2021      
  res@xyLineThicknesses =(/5,4/) ;画两条线 
  res@tiYAxisFont =22
  res@gsnStringFontHeightF=0.012
  res@gsnLeftStringOrthogonalPosF=-0.125
  res@gsnLeftStringParallelPosF=0.02
  res@gsnRightStringOrthogonalPosF=-0.125
  res@gsnRightStringParallelPosF=0.98


  res13=res
  res13@tmYROn      = False
  ; res13@xyDashPattern=lineDashPattern(0)
  res13@tiYAxisString = "TC frequency" ; y-axis label


  res24=res
  ; res24@tmYUseLeft=False ;这个不是必要的
  res24@tiYAxisSide="right"
  res24@tmXTOn               = False
  res24@tmYLOn               = False
  res24@tmYLLabelsOn         = False
  res24@tmYRLabelsOn         = True
  ; res24@xyDashPattern=lineDashPattern(1) ;关掉这个就有虚线了


  ;分别复制上述共用参数，绘制每个图形
  res1=res13
  res2=res24

  b1=sprintf("%.3f",TC_num_rc@b(1))
  b0=sprintf("%.3f",TC_num_rc@b(0))
  res1@gsnLeftString="y="+tostring(b1)+"x+"+tostring(b0)+""
  res1@gsnRightString=TC_num_sig

  res1@xyLineColor=colors(0) ;蓝色，TC影响
  res1@tiYAxisFontColor=colors(0)
  res1@trYMaxF =max(TC_num)+1
  plotxy(0)=gsn_csm_xy(wks,year,TC_num_arry,res1)

  b1=sprintf("%.3f",rate_rc@b(1))
  b0=sprintf("%.3f",rate_rc@b(0))
  res2@gsnLeftString="y="+tostring(b1)+"x+"+tostring(b0)+""
  res2@gsnRightString=rate_sig

  res2@tiYAxisString = "Relative frequency" ; y-axis label
  res2@xyLineColor=colors(1) ;蓝色，TC影响
  res2@tiYAxisFontColor=colors(1)
  res2@trYMaxF =max(rate)+0.15
  plotxy(1)=gsn_csm_xy(wks,year,rate_arry,res2)


  ;堆叠
  attachres1=True
  attachres1@gsnAttachBorderOn =False
  attachres2=True
  attachres2@gsnAttachPlotsXAxis =True 

attachid1=gsn_attach_plots(plotxy(0), plotxy(1), attachres1, attachres2)

draw(plotxy(0))
frame(wks)

end
 


 

