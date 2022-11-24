!------------------------------------------------------
!PGM��ʽ��ͼת��Ϊ������Χ��0.05�ȷֱ��ʵ�TBB����λΪ���϶ȣ�����
!����:
!  channel*3: the Channel name,one of IR1,IR2,IR3, and IR4
!  flpgm*80:��ͼ�ļ���
!  flcal*80: cal�ļ���
!  fltbb*80:TBB�ļ���
!  lat1,lat2,lon1,lon2: ����Χlat1<lat2,lon1<lon2
!  idate: ����
!�����
!  ifok���Ƿ���������ָ����1������0������
!  nx,ny��������
!  �޸�ʽ��TBB�ļ���nx*(ny+1),tbbout(1,ny+1):���ڣ�idate��,tbbout(2,ny+1):���ȷ�����������nx��,
!	 tbbout(3,ny+1)=dlon ����ֱ��ʣ�0.05�ȣ�
!	 tbbout(4,ny+1)=lon1 ��㾭��(���½ǵ�)
!	 tbbout(5,ny+1)=lon2 �յ㾭��(���Ͻǵ�)
!	 tbbout(6,ny+1)=ny   γ�ȷ�����������ny��
!	 tbbout(7,ny+1)=dlat γ��ֱ��ʣ�0.05�ȣ�
!	 tbbout(8,ny+1)=lat1 ���γ��(���½ǵ�)
!	 tbbout(9,ny+1)=lat2 �յ�γ��(���Ͻǵ�)

      program main
      character*80 flcal,flpgm,fltbb
      real lat1,lat2,lon1,lon2
      character channel*3
      CHARACTER*8 ITIME(483)
      integer funm
      open(1,file='F:\snow_sts_data\2020_tctimfortbb.txt')
      do i=1,483
        read(1,'(a8)') ITIME(i)
        print*,ITIME(i)
      end do
      lat1=0
      lat2=50
      lon1=70
      lon2=130
      DO 22 Km=1,483
        flpgm='G:\data\TBB\2020\2020_pgm\HMW8'
     &  //ITIME(Km)//'IR1.pgm'
        flcal='G:\data\TBB\2020\2020_cal\HMW8'
     &  //ITIME(Km)//'CAL.dat'
      fltbb='H:\TBB-from-1998-of-BOB-TC\new-grd\TBB_'
     &  //ITIME(Km)//'.grd'
      !!!!!!!!!!!!!�ַ���ת��Ϊ����
      !!!!write(fnum,'(I4)')ITIME(Km)
      read(ITIME(Km),'(I8)') funm
      idate=funm
      channel='IR1'
      call readgms5_area(channel,flpgm,flcal,fltbb,
     &lat1,lat2,lon1,lon2,idate,nx,ny,ifok,rlack)
   22	CONTINUE
      write(*,*)'ifok=',ifok,'   nx=',nx,'    ny=',ny,'    ny+1=',ny+1
      write(*,*)'idate',idate
!     pause
      end 


!-------------------------------------------------------      
      subroutine readgms5_area(channel,flpgm,flcal,fltbb,
     &lat1,lat2,lon1,lon2,idate,nx,ny,ifok,rlack)
      parameter(lon0=70,dlon=0.05,lat0=-20,dlat=0.05)
      dimension tbb(1800,1800),tbbout(1801,1801),tbb2(1800,1800)
      real lat1,lat2,lon1,lon2
      character*80 flcal,flpgm,fltbb
      character channel*3
      integer ifok
      !	write(*,*)trim(flpgm)
      !	write(*,*)trim(flcal) 
      !	write(*,*)trim(fltbb)
      ix1=nint((lon1-lon0)/dlon)+1
      ix2=nint((lon2-lon0)/dlon)+1
      iy1=nint((lat1-lat0)/dlat)+1
      iy2=nint((lat2-lat0)/dlat)+1
      nx=ix2-ix1+1
      ny=iy2-iy1+1
      if(nx.gt.1801.or.ny.gt.1801) then
      write(*,*)'��Χ̫�󣬳����жϣ��뽫��Χ������1800��1800�������ڡ�'
      stop
      endif
      call readgms5(channel,tbb,ifok,flpgm,flcal,rlack)
      if(ifok.eq.0) goto 100
      write(*,*) 'ifok=',ifok
      write(*,*)'nx=',nx,'    lon:',lon1,'-',lon2
      write(*,*)'ny=',ny,'    lat:',lat1,'-',lat2
      do i=1,1800
        do j=1,1800
          tbb2(i,j)=tbb(i,1800-j+1)
          tbbout(i,j)=rlack
        enddo
      enddo
      do i=1,1801
        do j=1,1801
          tbbout(i,j)=rlack
        enddo
      enddo
      do 70 i=ix1,ix2
      do 80 j=iy1,iy2
      if(i.lt.1.or.i.gt.1800.or.j.lt.1.or.j.gt.1800) then
      else
      ii=i-ix1+1
      jj=j-iy1+1
      tbbout(ii,jj)=tbb2(i,j)-273.15
      endif
   80 continue
   70 continue
      tbbout(1,ny+1)=idate*1.
      tbbout(2,ny+1)=nx
      tbbout(3,ny+1)=dlon
      tbbout(4,ny+1)=lon1
      tbbout(5,ny+1)=lon2
      tbbout(6,ny+1)=ny
      tbbout(7,ny+1)=dlat
      tbbout(8,ny+1)=lat1
      tbbout(9,ny+1)=lat2
      open(10,file=fltbb,form='binary')
      write(10,rec=1) ((tbbout(i,j),i=1,nx),j=1,ny+1)
      close(10)
      write(*,*)trim(fltbb)
      write(*,*)    'write data ok!'
  100 continue
      end

      subroutine readgms5(channel,tbb,ifok,flname,flname2,rlack)
      character*80 flname,flname2
      character channel*3
      character*255 inte
      dimension cal(0:255)
      integer*1 img(1800,1800)
      dimension tbb(1800,1800)
      integer ifok
      ifok=1
      ipgm=0
      ical=0
      write(*,*)'OK'//trim(flname)
      open(11,file=flname,form='binary',status='old',err=1000)
      do i=1,255
        read(11,err=1000,end=1000) inte(i:i)
        if(i.gt.13) then
          if(inte(i-7:i-4).eq."1800".and.inte(i-2:i).eq."255") then
            read(11,err=1000,end=1000) inte(i+1:i+1)
          goto 1010
          endif
        endif
      enddo
 1010 continue
      read(11,err=1000,end=1000) ((img(i,j),i=1,1800),j=1,1800)
      close(11)
      ipgm=1
      open(12,file=flname2,status='old',err=1000)
      do i=1,100000
        read(12,*,err=1000,end=1000) (inte(1:3))
        !        if(inte(1:3).eq."IR1") then
        if(inte(1:3).eq.channel) then
        goto 1011
        endif
      enddo
 1011 continue
      do i=1,256
        read(12,*,err=1000,end=1000) inte,inte,inte,
     &               index,inte,cal(index)
      !       write(*,*) i,cal(index),index
      enddo
      close(12)
      do i=1,1800
        do j=1,1800
          if(img(i,j).ge.0) then
            tbb(i,j)=cal(img(i,j))
          else
            tbb(i,j)=cal(256+img(i,j))
          if(img(i,j).eq.0.) tbb(i,j)=rlack !cal(255)
          endif
        enddo
      enddo
      ical=1
      goto 1012
 1000       continue
      ifok=0
      if(ipgm.eq.0)  write(*,*)'no '//trim(flname)//'file!'
      pause 10
      if(ical.eq.0) write(*,*)'no '//trim(flname2)//' file!'
 1012 continue
      end


