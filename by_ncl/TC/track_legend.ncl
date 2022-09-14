;画个关于强度的图例
 ; ncl /mnt/f/snow_related/code/by_ncl/track_legend.ncl
;
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

pic_dir ="/mnt/f/snow_related/pic/tc/"
wks  = gsn_open_wks("eps",pic_dir+"track_legend")  
gsn_define_colormap(wks, "wgne15")

colors=(/4,7,12,13,16,14,15/)
labels =(/"TD","TS","H1","H2","H3","H4","H5"/)

; 绘制图例
  txres               = True
  txres@txFontHeightF = 0.02
  txres1               = True
  txres1@txFontHeightF = 0.02
  txres1@txFontColor  = "black"


  xleg=fspan(0.15, 0.7, 7)
  xleg=xleg+0.06
  xtxt=xleg+0.03
  yleg=fspan(0.38, 0.38, 7)
  yleg=yleg-0.1
  ytxt = yleg   ; strings.

  do i = 0,6
    txres@txFontColor  = colors(i)
    gsn_text_ndc(wks,"~F37~p",xleg(i),yleg(i),txres)
    gsn_text_ndc(wks,labels(i),xtxt(i),ytxt(i),txres1)
  end do
    txres1@txFontColor  = "blue"
    txres1@txFontThicknessF=3
    gsn_text_ndc(wks,"~F37~p",0.3,0.5,txres1)
frame(wks)
end

 


 

