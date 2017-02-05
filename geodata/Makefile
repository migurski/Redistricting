all: tl_2016_all_sldu.shp tl_2016_all_sldl.shp

tl_2016_all_sldu.shp: tl_2016_01_sldu.zip tl_2016_02_sldu.zip tl_2016_04_sldu.zip tl_2016_05_sldu.zip \
                      tl_2016_06_sldu.zip tl_2016_08_sldu.zip tl_2016_09_sldu.zip tl_2016_10_sldu.zip \
                      tl_2016_12_sldu.zip tl_2016_13_sldu.zip tl_2016_15_sldu.zip tl_2016_16_sldu.zip \
                      tl_2016_17_sldu.zip tl_2016_18_sldu.zip tl_2016_19_sldu.zip tl_2016_20_sldu.zip \
                      tl_2016_21_sldu.zip tl_2016_22_sldu.zip tl_2016_23_sldu.zip tl_2016_24_sldu.zip \
                      tl_2016_25_sldu.zip tl_2016_26_sldu.zip tl_2016_27_sldu.zip tl_2016_28_sldu.zip \
                      tl_2016_29_sldu.zip tl_2016_30_sldu.zip tl_2016_32_sldu.zip tl_2016_33_sldu.zip \
                      tl_2016_34_sldu.zip tl_2016_35_sldu.zip tl_2016_36_sldu.zip tl_2016_37_sldu.zip \
                      tl_2016_38_sldu.zip tl_2016_39_sldu.zip tl_2016_40_sldu.zip tl_2016_41_sldu.zip \
                      tl_2016_42_sldu.zip tl_2016_44_sldu.zip tl_2016_45_sldu.zip tl_2016_46_sldu.zip \
                      tl_2016_47_sldu.zip tl_2016_48_sldu.zip tl_2016_49_sldu.zip tl_2016_50_sldu.zip \
                      tl_2016_51_sldu.zip tl_2016_53_sldu.zip tl_2016_54_sldu.zip tl_2016_55_sldu.zip \
                      tl_2016_56_sldu.zip tl_2016_72_sldu.zip
	./merge-slds.sh sldu

tl_2016_all_sldl.shp: tl_2016_01_sldl.zip tl_2016_02_sldl.zip tl_2016_04_sldl.zip tl_2016_05_sldl.zip \
                      tl_2016_06_sldl.zip tl_2016_08_sldl.zip tl_2016_09_sldl.zip tl_2016_10_sldl.zip \
                      tl_2016_12_sldl.zip tl_2016_13_sldl.zip tl_2016_15_sldl.zip tl_2016_16_sldl.zip \
                      tl_2016_17_sldl.zip tl_2016_18_sldl.zip tl_2016_19_sldl.zip tl_2016_20_sldl.zip \
                      tl_2016_21_sldl.zip tl_2016_22_sldl.zip tl_2016_23_sldl.zip tl_2016_24_sldl.zip \
                      tl_2016_25_sldl.zip tl_2016_26_sldl.zip tl_2016_27_sldl.zip tl_2016_28_sldl.zip \
                      tl_2016_29_sldl.zip tl_2016_30_sldl.zip tl_2016_32_sldl.zip tl_2016_33_sldl.zip \
                      tl_2016_34_sldl.zip tl_2016_35_sldl.zip tl_2016_36_sldl.zip tl_2016_37_sldl.zip \
                      tl_2016_38_sldl.zip tl_2016_39_sldl.zip tl_2016_40_sldl.zip tl_2016_41_sldl.zip \
                      tl_2016_42_sldl.zip tl_2016_44_sldl.zip tl_2016_45_sldl.zip tl_2016_46_sldl.zip \
                      tl_2016_47_sldl.zip tl_2016_48_sldl.zip tl_2016_49_sldl.zip tl_2016_50_sldl.zip \
                      tl_2016_51_sldl.zip tl_2016_53_sldl.zip tl_2016_54_sldl.zip tl_2016_55_sldl.zip \
                      tl_2016_56_sldl.zip tl_2016_72_sldl.zip
	./merge-slds.sh sldl

tl_2016_us_cd115.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2016/CD/tl_2016_us_cd115.zip

tl_2016_%_sldu.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2016/SLDU/tl_2016_$*_sldu.zip

tl_2016_%_sldl.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2016/SLDL/tl_2016_$*_sldl.zip
